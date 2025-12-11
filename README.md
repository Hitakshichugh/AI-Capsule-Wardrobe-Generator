🎀 AI Capsule Wardrobe Generator

Generate 30-day outfit ideas from photos of your own clothes using CLIP + Color Harmony + Style Similarity.

🧠 Overview

The AI Capsule Wardrobe Generator automatically creates a 30-day personalized outfit calendar using photos of your own clothing items.
Users upload pictures of their wardrobe (tops, bottoms, skirts, dresses, rompers, jackets), and the system intelligently:

✔ classifies each clothing item (top/bottom/skirt/dress/romper/jacket)
✔ extracts CLIP embeddings for style similarity
✔ analyzes colors for harmony
✔ mixes and matches items into valid outfits
✔ scores each outfit using color + style
✔ creates a 30-day outfit calendar
✔ displays the outfits visually side-by-side

🎯 Core Features

👗 Intelligent Clothing Classification
The system recognizes:
Tops (shirts, blouses, hoodies, sweaters)
Bottoms (jeans, trousers, pants, shorts)
Skirts
Dresses
Rompers / Jumpsuits
Jackets / Outerwear

🎨 Color Harmony Estimation
Using OpenCV + HSV color space, each item is mapped into three broad groups:
Warm
Cool
Neutral

Color compatibility scoring follows:
Neutral + anything → strong match
Warm + warm or cool + cool → good match
Warm + cool → moderate match

🪄 Outfit Generation Logic
The system automatically generates combinations:
Top + Bottom (+ optional Jacket)
Top + Skirt (+ Jacket)
Dress (+ Jacket)
Romper (+ Jacket)

## 📁 Folder Structure
├── outfitgenerator.ipynb    # Main notebook with CLIP + CV pipeline
├── uploads/                 # User-uploaded clothing images
├── README.md
└── requirements.txt

