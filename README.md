# 🎀 AI Capsule Wardrobe Generator

Generate 30-day outfit ideas from photos of your own clothes using CLIP + Color Harmony + Style Similarity.

## 🧠 Overview

The AI Capsule Wardrobe Generator automatically creates a 30-day personalized outfit calendar using photos of your own clothing items.
Users upload pictures of their wardrobe (tops, bottoms, skirts, dresses, rompers, jackets), and the system intelligently:

✔ classifies each clothing item (top/bottom/skirt/dress/romper/jacket) <br>
✔ extracts CLIP embeddings for style similarity <br>
✔ analyzes colors for harmony <br>
✔ mixes and matches items into valid outfits <br>
✔ scores each outfit using color + style <br>
✔ creates a 30-day outfit calendar <br>
✔ displays the outfits visually side-by-side <br>

## 🎯 Core Features

👗 Intelligent Clothing Classification
The system recognizes:  
Tops (shirts, blouses, hoodies, sweaters) <br>
Bottoms (jeans, trousers, pants, shorts) <br>
Skirts <br>
Dresses <br>
Rompers / Jumpsuits <br>
Jackets / Outerwear <br>

## 🎨 Color Harmony Estimation
Using OpenCV + HSV color space, each item is mapped into three broad groups:  
Warm <br>
Cool <br>
Neutral <br>

Color compatibility scoring follows:
Neutral + anything → strong match <br> 
Warm + warm or cool + cool → good match <br>
Warm + cool → moderate match <br>

## 🪄 Outfit Generation Logic
The system automatically generates combinations:  
Top + Bottom (+ optional Jacket) <br>
Top + Skirt (+ Jacket) <br>
Dress (+ Jacket) <br>
Romper (+ Jacket) <br>

📁 Folder Structure

```txt
├── outfitgenerator.ipynb      # Main notebook with CLIP + CV pipeline  
├── uploads/                   # User-uploaded clothing images  
├── README.md  
└── requirements.txt
```
## 🧪 Technical Architecture
🏗 Model Components

| Component              | Purpose                           |
| ---------------------- | --------------------------------- |
| **CLIP Image Encoder** | Extract style embeddings          |
| **CLIP Text Encoder**  | Zero-shot category classification |
| **OpenCV + HSV**       | Dominant color detection          |
| **KMeans (optional)**  | Color clustering                  |
| **Pandas / NumPy**     | Data organization                 |
| **Matplotlib**         | Outfit visualization              |

## 🛠 Step-by-Step Installation
1. Clone the Repository
```bash
git clone https://github.com/<yourusername>/<your-repo>.git
cd <your-repo>
```
2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Run the Notebook
```bash
jupyter notebook outfitgenerator.py
```
## 🌐 Future Improvements

✔ Web UI (drag & drop uploads) <br>
✔ Flask API integration <br>
⏳ Weather-based outfit suggestions <br>
⏳ Formal / casual / sporty filters <br>
⏳ Export full capsule as PDF <br>
⏳ Add garment segmentation (remove backgrounds) <br>

## 👥 Team

Developed by:
Hitakshi Chugh - Model architecture and Implementation <br>
Khushi Navadiya - Front-end UI building <br>
Navyasri Edara - Technical reporting and documentation. <br>
Jacob Raj - Cloud Deployment <br>

A collaborative project blending AI, fashion, and data science.


