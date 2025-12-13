# client.py
"""
Simple Python web client for your Capsule Wardrobe API.

What it does:
1. Sends an image file to the Flask /upload endpoint.
2. Fetches the /capsule page after upload.
3. Saves the HTML of the capsule page to capsule_snapshot.html
   so you can open it in a browser and verify the outfit updates.
"""

import sys
from pathlib import Path

import requests

BASE_URL = "http://127.0.0.1:5000"


def upload_item(image_path: Path):
    """POST one wardrobe image to the /upload endpoint."""
    if not image_path.exists():
        print(f"[CLIENT] File not found: {image_path}")
        return False

    url = f"{BASE_URL}/upload"
    print(f"[CLIENT] Uploading {image_path} to {url}")

    with image_path.open("rb") as f:
        files = {"item_image": (image_path.name, f, "image/jpeg")}
        response = requests.post(url, files=files)

    print(f"[CLIENT] Upload response: {response.status_code} {response.reason}")
    # Flask redirects to /capsule, so 302/200 are both fine
    return response.ok or response.status_code in (301, 302)


def fetch_capsule_html():
    """GET the /capsule page and save it as an HTML file."""
    url = f"{BASE_URL}/capsule"
    print(f"[CLIENT] Fetching capsule view from {url}")

    response = requests.get(url)
    print(f"[CLIENT] Capsule response: {response.status_code} {response.reason}")

    out_file = Path("capsule_snapshot.html")
    out_file.write_text(response.text, encoding="utf-8")
    print(f"[CLIENT] Saved capsule page to {out_file.resolve()}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py path/to/wardrobe_image.jpg")
        sys.exit(1)

    image_path = Path(sys.argv[1])

    if upload_item(image_path):
        fetch_capsule_html()
    else:
        print("[CLIENT] Upload failed; not fetching capsule.")


if __name__ == "__main__":
    main()
