import os
import sys
import time
from io import BytesIO
from concurrent.futures import ProcessPoolExecutor
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


FONT_PATH = "./Monotype Corsiva/Monotype-Corsiva-Regular.ttf"
FONT_NAME = "Monotype Corsiva"
FONT_COLOR = (17/255, 74/255, 156/255)
FONT_SIZE = 23
MAX_NAME_WIDTH = 500  # in points

template_path = "./p1.pdf"
output_folder = "participants-odoo"
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


def generate_certificate(name):
    name = name.strip().title()
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
    can.drawCentredString(410, 280, name)  # center at x=350, y=225

    # QR code generation part removed

    can.save()
    packet.seek(0)

    overlay = PdfReader(packet).pages[0]
    page.merge_page(overlay)
    pdf_w.add_page(page)

    with open(output_path, "wb") as out_f:
        pdf_w.write(out_f)

    return name


def main():
    with open("./names.txt", "r") as f:
        names = [line for line in f.readlines() if line.strip()]

    print(f"Generating certificates for {len(names)} people...")

    with ProcessPoolExecutor() as executor:
        for i, name in enumerate(executor.map(generate_certificate, names), 1):
            sys.stdout.write(f"\r[{i}/{len(names)}] Processed: {name}.pdf")
            sys.stdout.flush()

    print("\n✅ All certificates have been generated successfully!")


if __name__ == "__main__":
    main()
