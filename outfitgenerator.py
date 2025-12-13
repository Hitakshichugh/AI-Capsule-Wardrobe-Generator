# outfitgenerator.py
"""
Clean version of the model helper file for Flask.

Provides:
    - load_clip_model(device=None)
    - get_image_embedding(model, processor, device, image)
    - get_dominant_color_bgr(image_bgr, k=4, crop_size=0.6)
    - categorize_color(hsv)
    - bgr_to_hsv(bgr)

NO dataset loading, NO zip extraction, NO notebook display code.
"""

from pathlib import Path
from typing import Tuple

import torch
import numpy as np
from PIL import Image
from transformers import CLIPModel, CLIPProcessor
import cv2
from sklearn.cluster import KMeans


# ----------------- 1. CLIP MODEL LOADING -----------------

def load_clip_model(device: str | None = None):
    """
    Load CLIP model + processor.

    Returns:
        model, processor, device
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    print("[outfitgenerator] using device:", device)

    model_name = "openai/clip-vit-base-patch32"
    model = CLIPModel.from_pretrained(model_name).to(device)
    processor = CLIPProcessor.from_pretrained(model_name)

    model.eval()
    return model, processor, device


def get_image_embedding(model, processor, device: str, image: Image.Image) -> torch.Tensor:
    """
    Compute a normalized CLIP image embedding for a single PIL image.
    """
    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        feats = model.get_image_features(**inputs)
    feats = feats / feats.norm(dim=-1, keepdim=True)
    return feats.squeeze(0).cpu()  # 1D tensor


# ----------------- 2. COLOR UTILS -----------------

def get_dominant_color_bgr(
    image_bgr: np.ndarray,
    k: int = 4,
    crop_size: float = 0.6
) -> Tuple[int, int, int]:
    """
    Find a dominant BGR color in an image using KMeans.

    1) Optionally crop to the center to reduce background.
    2) Downscale for speed.
    3) Run KMeans.
    4) Pick the cluster with the highest saturation in HSV.
    """
    h, w, _ = image_bgr.shape

    # center crop
    if 0 < crop_size < 1.0:
        ch, cw = int(h * crop_size), int(w * crop_size)
        y1 = (h - ch) // 2
        x1 = (w - cw) // 2
        image_bgr = image_bgr[y1:y1 + ch, x1:x1 + cw]

    # downscale
    img_small = cv2.resize(image_bgr, (150, 150), interpolation=cv2.INTER_AREA)
    pixels = img_small.reshape(-1, 3)

    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(pixels)

    centers = kmeans.cluster_centers_.astype(np.uint8)  # (k, 3) BGR

    # convert centers to HSV
    centers_hsv = cv2.cvtColor(
        centers.reshape(-1, 1, 3),
        cv2.COLOR_BGR2HSV
    ).reshape(-1, 3)
    sats = centers_hsv[:, 1]

    # pick cluster with highest saturation
    idx = int(np.argmax(sats))
    b, g, r = centers[idx]
    return int(b), int(g), int(r)


def categorize_color(hsv: Tuple[int, int, int]) -> str:
    """
    Map HSV to warm / cool / neutral.
    OpenCV hue is [0, 179].
    """
    h, s, v = hsv

    # very low saturation or very dark -> neutral
    if s < 15 or v < 20:
        return "neutral"

    # strong reds -> warm
    if (0 <= h <= 15 or 160 <= h <= 179) and s > 40:
        return "warm"

    # oranges / yellows
    if 15 < h <= 45:
        return "warm"

    # greens / cyans / blues (cool tones)
    if 45 < h <= 120:
        return "cool"

    # blue-magenta-ish, still treated as cool
    if 120 < h <= 179:
        return "cool"

    # fallback
    return "neutral"


def bgr_to_hsv(bgr: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """
    Convert a BGR tuple (as used in OpenCV) to HSV tuple.
    """
    color_bgr = np.uint8([[list(bgr)]])
    hsv = cv2.cvtColor(color_bgr, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[0, 0]
    return int(h), int(s), int(v)

