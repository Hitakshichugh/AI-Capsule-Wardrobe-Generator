# app.py
import os
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

import wardrobe_model  # your model / AI logic

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    """Serve uploaded images so they can be shown in the capsule page."""
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/", methods=["GET"])
def home():
    """
    Landing page:
    - About text
    - Upload wardrobe form
    """
    return render_template("home.html")


@app.route("/upload", methods=["POST"])
def upload_item():
    """
    Handle upload form from the home page.
    """
    image_file = request.files.get("item_image")
    category = request.form.get("category")

    if not image_file or image_file.filename == "" or not category:
        print("[FLASK] Missing image or category")
        return redirect(url_for("home"))

    save_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(save_path)
    print(f"[FLASK] Saved file to {save_path}")

    wardrobe_model.handle_new_item(save_path, category)

    return redirect(url_for("home"))


@app.route("/capsule", methods=["GET"])
def capsule():
    """30-day capsule calendar view."""

    # require at least 10 items before generating capsule
    if wardrobe_model.get_item_count() < 2:
        msg = "Please upload at least 10 wardrobe pieces (tops, bottoms, jackets) to generate a full 30-day capsule ✨"
        return render_template(
            "capsule.html",
            days=[],
            items={},
            month_name="December",
            year=2025,
            message=msg,
        )

    # get outfits + items from model
    outfits, items_map = wardrobe_model.generate_capsule()

    month = 12
    year = 2025
    month_name = "December"

    cute_quotes = [
        "Romanticize your everyday.",
        "Dress like you already made it.",
        "Soft outfit, sharp mind.",
        "You are the main character.",
        "One outfit at a time.",
        "Effortless, not careless.",
        "Cute clothes, serious goals.",
    ]

    calendar_days = []
    for idx, outfit in enumerate(outfits):
        # one outfit per day
        day_num = idx + 1
        d = date(year, month, day_num)
        quote = cute_quotes[idx % len(cute_quotes)]
        calendar_days.append(
            {
                "day_number": d.day,
                "weekday": d.strftime("%A"),
                "quote": quote,
                "outfit": outfit,
            }
        )

    return render_template(
        "capsule.html",
        days=calendar_days,
        items=items_map,
        month_name=month_name,
        year=year,
        message=None,
    )


if __name__ == "__main__":
    app.run(debug=True)
