import json
import os
import sys
from typing import List, Dict

import qrcode
from PIL import Image

# Import configuration
try:
    import config
except ImportError:
    print("Error: config.py not found!")
    print("Please copy config.example.py to config.py and configure it.")
    sys.exit(1)

# Constants to align with certificate.py usage
QR_FOLDER = config.QR_FOLDER
OUTPUT_DPI = config.OUTPUT_DPI
# certificate.py draws QR at width=75, height=75 points. 1 point = 1/72 inch.
# At 300 DPI, pixels = inches * DPI = (points/72) * DPI = 75/72*300 ≈ 312.5 -> 313 px
QR_SIZE_PX = config.QR_SIZE_PX

# Map error correction string to qrcode constant
ERROR_CORRECTION_MAP = {
    "L": qrcode.constants.ERROR_CORRECT_L,
    "M": qrcode.constants.ERROR_CORRECT_M,
    "Q": qrcode.constants.ERROR_CORRECT_Q,
    "H": qrcode.constants.ERROR_CORRECT_H,
}
QR_ERROR_CORRECTION = ERROR_CORRECTION_MAP.get(
    config.QR_ERROR_CORRECTION, qrcode.constants.ERROR_CORRECT_M
)


def ensure_output_dir() -> None:
    os.makedirs(QR_FOLDER, exist_ok=True)


def title_case_filename(name: str) -> str:
    # Match certificate.py behavior
    return name.strip().title() if config.AUTO_TITLE_CASE else name.strip()


def load_participants(json_path: str) -> List[Dict[str, str]]:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def make_qr_image(data: str) -> Image.Image:
    # Configure QR to produce a crisp image that resizes well
    qr = qrcode.QRCode(
        version=None,  # automatic size
        error_correction=QR_ERROR_CORRECTION,
        box_size=config.QR_BOX_SIZE,
        border=config.QR_BORDER,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    # Resize to exact pixel size using high-quality resampling
    img = img.resize((QR_SIZE_PX, QR_SIZE_PX), resample=Image.LANCZOS)
    return img


def save_qr(img: Image.Image, path: str) -> None:
    # Save PNG with DPI metadata so layout tools preserve size when needed
    img.save(path, format="PNG", dpi=(OUTPUT_DPI, OUTPUT_DPI))


def generate_all(json_path: str = None) -> None:
    if json_path is None:
        json_path = config.PARTICIPANTS_JSON
    ensure_output_dir()
    participants = load_participants(json_path)

    for entry in participants:
        name = entry.get("name", "").strip()
        link = entry.get("link", "").strip()
        if not name or not link:
            print(f"Skipping entry due to missing name/link: {entry}")
            continue
        filename = f"{title_case_filename(name)}.png"
        out_path = os.path.join(QR_FOLDER, filename)
        img = make_qr_image(link)
        save_qr(img, out_path)
        print(f"Saved {out_path}")


if __name__ == "__main__":
    generate_all()
