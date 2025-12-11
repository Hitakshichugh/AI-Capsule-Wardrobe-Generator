🎀 AI Capsule Wardrobe Generator

Generate 30-day outfit ideas from photos of your own clothes using CLIP + Color Harmony + Style Similarity.

🧠 Overview

This project creates a personalized capsule wardrobe using images uploaded by the user.
You upload photos of your tops, bottoms, dresses, rompers, skirts, and jackets — the system automatically:

✔ classifies each clothing item (top/bottom/skirt/dress/romper/jacket)
✔ extracts CLIP embeddings for style similarity
✔ analyzes colors for harmony
✔ mixes and matches items into valid outfits
✔ scores each outfit using color + style
✔ creates a 30-day outfit calendar
✔ displays the outfits visually side-by-side

✨ Features

Upload any number of clothing images

Automatic category detection using CLIP

Color harmony estimation

Style similarity using CLIP embeddings

Smart outfit generator:

top + bottom

top + skirt

dresses + jackets

rompers + jackets

Rank outfits by style + color

View each outfit visually

Auto-generate a 30-day capsule

🗂 Folder Structure
├── outfitgenerator.ipynb
├── uploads/               # user-uploaded clothing images
├── README.md
└── requirements.txt

Tech Stack

Python

PyTorch

OpenAI CLIP

Transformers

Pandas

NumPy

OpenCV

Matplotlib

🧑‍🤝‍🧑 Team

Built by:

Hitakshi

Khushi

Navya

Jacob

📌 Future Improvements

Fully interactive UI

Drag-and-drop web upload

PDF export of outfit calendar

Outfit filters (formal/casual/weather)
