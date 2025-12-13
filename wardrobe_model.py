# wardrobe_model.py
"""
Bridge between Flask and your model code in outfitgenerator.py.

You already have:
    - load_clip_model
    - get_image_embedding
    - get_dominant_color_bgr
    - bgr_to_hsv
    - categorize_color

Here we:
    - Load the CLIP model once
    - For each upload: compute embedding + color group
    - Store items in memory
    - Build 30 outfits using color + style scores
    - Return data in the format your Flask / templates expect
"""

from typing import List, Dict, Tuple

import torch
import torch.nn.functional as F
from PIL import Image
import numpy as np
import cv2
import os

import outfitgenerator as og  # <-- YOUR model file (outfitgenerator.py)


# ----------------- 1. MODEL LOADING -----------------

print("[WARDROBE_MODEL] Loading model via outfitgenerator.load_clip_model() ...")
# your function signature: load_clip_model(device=None) -> (model, processor, device)
MODEL, PROCESSOR, DEVICE = og.load_clip_model()
print(f"[WARDROBE_MODEL] Model loaded on device = {DEVICE}")


# ----------------- 2. INTERNAL STORAGE -----------------
# We keep everything in memory for this mini project.

_ITEMS: List[Dict] = []   # each item: {id, image_path, category, color_group, embedding}


def _pil_to_bgr(pil_img: Image.Image) -> np.ndarray:
    """Convert a PIL image (RGB) to OpenCV BGR array."""
    rgb = np.array(pil_img)  # HWC, RGB
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    return bgr


# ----------------- 3. PUBLIC API: called by Flask -----------------

def handle_new_item(image_path: str, category: str) -> str:
    """
    Called by Flask after each upload (in /upload route).

    Steps:
      - open image
      - get CLIP embedding via outfitgenerator.get_image_embedding
      - compute dominant color & color group
      - store item info + embedding in memory
    """
    item_id = f"item{len(_ITEMS) + 1}"

    # 1) open image
    pil_img = Image.open(image_path).convert("RGB")

    # 2) embedding via your notebook function:
    #    get_image_embedding(model, processor, device, image)
    embedding = og.get_image_embedding(MODEL, PROCESSOR, DEVICE, pil_img)
    # ensure 1D tensor
    if embedding.ndim > 1:
        embedding = embedding.squeeze()

    # 3) dominant color + color_group using your color helpers
    #    get_dominant_color_bgr(image_bgr), bgr_to_hsv, categorize_color
    bgr = _pil_to_bgr(pil_img)
    dom_bgr = og.get_dominant_color_bgr(bgr)          # (B, G, R)
    dom_hsv = og.bgr_to_hsv(dom_bgr)                  # (H, S, V)
    color_group = og.categorize_color(dom_hsv)        # "warm" / "cool" / "neutral"

    _ITEMS.append({
        "id": item_id,
        "image_path": image_path,
        "filename": os.path.basename(image_path),
        "category": category.lower().strip(),  # "top" / "bottom" / "jacket"
        "color_group": color_group,
        "embedding": embedding,               # 1D torch tensor
    })

    print(f"[WARDROBE_MODEL] Stored {item_id} ({category}, {color_group}) at {image_path}")
    return item_id


def generate_capsule() -> Tuple[List[Dict], Dict[str, Dict]]:
    """
    Called by Flask when /capsule is opened.

    Returns:
      outfits:   list of {"day": int, "items": [item_ids]}
      items_map: dict {item_id: item_info}
    """
    if not _ITEMS:
        return [], {}

    items_map = {item["id"]: item for item in _ITEMS}
    outfits_item_ids = _build_30_outfits(_ITEMS)

    outfits: List[Dict] = []
    for day, item_ids in enumerate(outfits_item_ids, start=1):
        outfits.append({
            "day": day,
            "items": item_ids,
        })

    return outfits, items_map


# ----------------- 4. OUTFIT SCORING (color + style) -----------------

def _pair_color_score(g1: str, g2: str) -> float:
    """
    Reuse your notebook's logic:

      - if any is neutral  -> 3.0
      - if same group      -> 2.5
      - otherwise          -> 1.0
    """
    if g1 == "neutral" or g2 == "neutral":
        return 3.0
    if g1 == g2:
        return 2.5
    return 1.0


def _outfit_color_score(groups: List[str]) -> float:
    """Sum pairwise color compatibility inside an outfit."""
    score = 0.0
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            score += _pair_color_score(groups[i], groups[j])
    return score


def _cosine_sim(e1: torch.Tensor, e2: torch.Tensor) -> float:
    """Cosine similarity between two 1D embeddings."""
    return float(F.cosine_similarity(e1.unsqueeze(0), e2.unsqueeze(0)).item())


def _outfit_style_score(embeddings: List[torch.Tensor]) -> float:
    """
    Average pairwise cosine similarity between embeddings in the outfit.
    Higher = more stylistically coherent.
    """
    sims = []
    for i in range(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            sims.append(_cosine_sim(embeddings[i], embeddings[j]))
    if not sims:
        return 0.0
    return float(np.mean(sims))


# ----------------- 5. BUILD 30 OUTFITS -----------------

def _build_30_outfits(items: List[Dict]) -> List[List[str]]:
    """
    Build up to 30 outfits using:
      - tops
      - bottoms
      - jackets (optional)

    Strategy:
      - generate all valid combos (top+bottom, with/without jacket)
      - score each combo using color + style
      - pick the top 30
    """
    tops = [it for it in items if it["category"] == "top"]
    bottoms = [it for it in items if it["category"] == "bottom"]
    jackets = [it for it in items if it["category"] == "jacket"]

    combos = []  # each combo: {"ids": [...], "groups": [...], "embeds": [...]}

    # Only tops/bottoms/jackets if available
    if tops and bottoms:
        for t in tops:
            for b in bottoms:
                # combo without jacket
                combos.append(_make_combo([t, b]))
                # combos with each jacket
                for j in jackets:
                    combos.append(_make_combo([t, b, j]))
    else:
        # fallback: just pair any items we have
        n = len(items)
        for i in range(n):
            for j in range(i + 1, n):
                combos.append(_make_combo([items[i], items[j]]))

    if not combos:
        # in absolute worst case, pick single items as outfits
        return [[it["id"]] for it in items][:30]

    # score combos
    w_color = 0.6
    w_style = 0.4
    scored = []
    for combo in combos:
        c_score = _outfit_color_score(combo["groups"])
        s_score = _outfit_style_score(combo["embeds"])
        total = w_color * c_score + w_style * s_score
        scored.append((total, combo["ids"]))

    # sort by total score, descending
    scored.sort(key=lambda x: x[0], reverse=True)

    # pick top-30 (or fewer if not enough combos)
    top_k = min(31, len(scored))
    best = [ids for (_, ids) in scored[:top_k]]

    # if we have fewer than 30 combos, repeat from start until we reach 30
    while len(best) < 31 and best:
        best.extend(best[: (31 - len(best))])

    return best[:31]


def _make_combo(item_list: List[Dict]) -> Dict:
    """Helper: build structure for one outfit combo."""
    ids = [it["id"] for it in item_list]
    groups = [it["color_group"] for it in item_list]
    embeds = [it["embedding"] for it in item_list]
    return {"ids": ids, "groups": groups, "embeds": embeds}

def get_item_count() -> int:
    return len(_ITEMS)
