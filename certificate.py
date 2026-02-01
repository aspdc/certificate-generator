import os
import sys
import time
from io import BytesIO
from concurrent.futures import ProcessPoolExecutor
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

# Import configuration
try:
    import config
except ImportError:
    print("Error: config.py not found!")
    print("Please copy config.example.py to config.py and configure it.")
    sys.exit(1)

# Load configuration values
FONT_PATH = config.FONT_PATH
FONT_NAME = config.FONT_NAME
FONT_COLOR = config.FONT_COLOR
FONT_SIZE = config.FONT_SIZE
MAX_NAME_WIDTH = config.MAX_NAME_WIDTH

template_path = config.TEMPLATE_PATH_WITH_QR
output_folder = config.OUTPUT_FOLDER_WITH_QR
os.makedirs(output_folder, exist_ok=True)

# Register font once (for all processes)
pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))


def calculate_font_size(name, canvas_obj, max_width=MAX_NAME_WIDTH, initial_size=FONT_SIZE):
    canvas_obj.setFont(FONT_NAME, initial_size)
    text_width = pdfmetrics.stringWidth(name, FONT_NAME, initial_size)
    while text_width > max_width and initial_size > 10:
        initial_size -= 1
        text_width = pdfmetrics.stringWidth(name, FONT_NAME, initial_size)
    return initial_size




QR_FOLDER = config.QR_FOLDER



def generate_certificate(name):
    name = name.strip().title() if config.AUTO_TITLE_CASE else name.strip()
    base_output_path = os.path.join(output_folder, f"{name}.pdf")
    output_path = base_output_path
    counter = 1
    while os.path.exists(output_path):
        output_path = os.path.join(output_folder, f"{name}_{counter}.pdf")
        counter += 1

    # Load template
    pdf_r = PdfReader(template_path)
    page = pdf_r.pages[0]
    pdf_w = PdfWriter()

    # Create overlay
    packet = BytesIO()
    can = canvas.Canvas(packet)
    name_font_size = calculate_font_size(name, can)

    can.setFont(FONT_NAME, name_font_size)
    can.setFillColorRGB(*FONT_COLOR)
    #### !THIS IS FOR NAME (x,y)
    can.drawCentredString(*config.NAME_POSITION_WITH_QR, name)

    qr_path = os.path.join(QR_FOLDER, f"{name}.png")
    if os.path.exists(qr_path):
        # Adjust these coordinates to match your bottom box position
        # QR size is set to 100x100 points, adjust as needed
        ###! THIS FOR QR (x,y)
        can.drawImage(ImageReader(qr_path), config.QR_POSITION_X, config.QR_POSITION_Y, 
                      width=config.QR_WIDTH, height=config.QR_HEIGHT)
    else:
        print(f"\nWarning: QR code not found for {name}")


    can.save()
    packet.seek(0)

    overlay = PdfReader(packet).pages[0]
    page.merge_page(overlay)
    pdf_w.add_page(page)

    with open(output_path, "wb") as out_f:
        pdf_w.write(out_f)

    return name


def main():
    with open(config.NAMES_FILE, "r") as f:
        names = f.readlines()

    print(f"Generating certificates for {len(names)} people...")

    if config.ENABLE_PARALLEL_PROCESSING:
        with ProcessPoolExecutor() as executor:
            for i, name in enumerate(executor.map(generate_certificate, names), 1):
                sys.stdout.write(f"\r[{i}/{len(names)}] Processed: {name}.pdf")
                sys.stdout.flush()
    else:
        for i, name in enumerate(names, 1):
            processed = generate_certificate(name)
            sys.stdout.write(f"\r[{i}/{len(names)}] Processed: {processed}.pdf")
            sys.stdout.flush()

    print("\n✅ All certificates have been generated successfully!")


if __name__ == "__main__":
    main()
