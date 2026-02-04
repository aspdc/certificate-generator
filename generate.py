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

# Register font once (for all processes)
pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))


def calculate_font_size(name, canvas_obj, max_width=MAX_NAME_WIDTH, initial_size=FONT_SIZE):
    canvas_obj.setFont(FONT_NAME, initial_size)
    text_width = pdfmetrics.stringWidth(name, FONT_NAME, initial_size)
    while text_width > max_width and initial_size > 10:
        initial_size -= 1
        text_width = pdfmetrics.stringWidth(name, FONT_NAME, initial_size)
    return initial_size


def generate_certificate_with_qr(data):
    name, serial_number = data
    name = name.strip().title() if config.AUTO_TITLE_CASE else name.strip()
    output_folder = config.OUTPUT_FOLDER_WITH_QR
    template_path = config.TEMPLATE_PATH_WITH_QR
    
    os.makedirs(output_folder, exist_ok=True)
    
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
    can.drawCentredString(*config.NAME_POSITION_WITH_QR, name)

    # Add serial number if position is configured
    if hasattr(config, 'SERIAL_NUMBER_POSITION_WITH_QR') and config.SERIAL_NUMBER_POSITION_WITH_QR:
        sr_font_size = getattr(config, 'SERIAL_NUMBER_FONT_SIZE', 10)
        can.setFont(FONT_NAME, sr_font_size)
        can.drawString(*config.SERIAL_NUMBER_POSITION_WITH_QR, serial_number.strip())

    qr_path = os.path.join(config.QR_FOLDER, f"{name}.png")
    if os.path.exists(qr_path):
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


def generate_certificate_no_qr(data):
    name, serial_number = data
    name = name.strip().title() if config.AUTO_TITLE_CASE else name.strip()
    output_folder = config.OUTPUT_FOLDER_NO_QR
    template_path = config.TEMPLATE_PATH_NO_QR
    
    os.makedirs(output_folder, exist_ok=True)
    
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
    can.drawCentredString(*config.NAME_POSITION_NO_QR, name)

    # Add serial number if position is configured
    if hasattr(config, 'SERIAL_NUMBER_POSITION_NO_QR') and config.SERIAL_NUMBER_POSITION_NO_QR:
        sr_font_size = getattr(config, 'SERIAL_NUMBER_FONT_SIZE', 10)
        can.setFont(FONT_NAME, sr_font_size)
        can.drawString(*config.SERIAL_NUMBER_POSITION_NO_QR, serial_number.strip())

    can.save()
    packet.seek(0)

    overlay = PdfReader(packet).pages[0]
    page.merge_page(overlay)
    pdf_w.add_page(page)

    with open(output_path, "wb") as out_f:
        pdf_w.write(out_f)

    return name


def main():
    # Ask user for certificate type
    print("Certificate Generator")
    print("=" * 50)
    print("\n1. Generate certificates WITH QR codes")
    print("2. Generate certificates WITHOUT QR codes")
    print("\nEnter your choice (1 or 2): ", end="")
    
    choice = input().strip()
    
    if choice == "1":
        use_qr = True
        generator_func = generate_certificate_with_qr
        print("\nGenerating certificates WITH QR codes...")
    elif choice == "2":
        use_qr = False
        generator_func = generate_certificate_no_qr
        print("\nGenerating certificates WITHOUT QR codes...")
    else:
        print("Invalid choice. Please run again and select 1 or 2.")
        sys.exit(1)

    # Read names
    with open(config.NAMES_FILE, "r") as f:
        names = [line for line in f.readlines() if line.strip()]

    # Read serial numbers if file exists
    serial_numbers_file = getattr(config, 'SERIAL_NUMBERS_FILE', './sr-no.txt')
    if os.path.exists(serial_numbers_file):
        with open(serial_numbers_file, "r") as f:
            serial_numbers = [line for line in f.readlines() if line.strip()]
        
        # Ensure we have same number of serial numbers as names
        if len(serial_numbers) < len(names):
            print(f"Warning: Only {len(serial_numbers)} serial numbers found for {len(names)} names.")
            print("Padding with empty serial numbers.")
            serial_numbers.extend([''] * (len(names) - len(serial_numbers)))
        elif len(serial_numbers) > len(names):
            print(f"Warning: {len(serial_numbers)} serial numbers found for {len(names)} names.")
            print("Using only the first {len(names)} serial numbers.")
            serial_numbers = serial_numbers[:len(names)]
    else:
        # No serial numbers file, use empty strings
        serial_numbers = [''] * len(names)

    # Create pairs of (name, serial_number)
    data_pairs = list(zip(names, serial_numbers))

    print(f"Found {len(names)} names to process...")

    if config.ENABLE_PARALLEL_PROCESSING:
        with ProcessPoolExecutor() as executor:
            for i, name in enumerate(executor.map(generator_func, data_pairs), 1):
                sys.stdout.write(f"\r[{i}/{len(names)}] Processed: {name}.pdf")
                sys.stdout.flush()
    else:
        for i, data in enumerate(data_pairs, 1):
            processed = generator_func(data)
            sys.stdout.write(f"\r[{i}/{len(names)}] Processed: {processed}.pdf")
            sys.stdout.flush()

    print("\nAll certificates have been generated successfully!")
    
    # Ask if user wants to merge PDFs
    print("\nDo you want to merge all PDFs into a single file? (y/n): ", end="")
    merge_choice = input().strip().lower()
    
    if merge_choice in ['y', 'yes']:
        from merge_pdfs import merge_pdfs
        source_folder = config.OUTPUT_FOLDER_WITH_QR if use_qr else config.OUTPUT_FOLDER_NO_QR
        output_file = f"merged_{'with_qr' if use_qr else 'no_qr'}.pdf"
        print(f"\nMerging PDFs from {source_folder}...")
        merge_pdfs(source_folder, output_file)
    else:
        print("\nSkipping PDF merge.")


if __name__ == "__main__":
    main()
