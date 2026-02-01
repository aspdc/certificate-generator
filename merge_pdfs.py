import os
from PyPDF2 import PdfReader, PdfWriter

def merge_pdfs(source_folder, output_filename):
    if not os.path.exists(source_folder):
        print(f"Error: Folder '{source_folder}' does not exist.")
        return

    pdf_writer = PdfWriter()
    
    # Get all PDF files and sort them
    pdf_files = [f for f in os.listdir(source_folder) if f.lower().endswith('.pdf')]
    pdf_files.sort()
    
    if not pdf_files:
        print(f"No PDF files found in '{source_folder}'.")
        return

    print(f"Found {len(pdf_files)} PDF files. Merging...")
    
    count = 0
    for filename in pdf_files:
        file_path = os.path.join(source_folder, filename)
        try:
            pdf_reader = PdfReader(file_path)
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)
            count += 1
            print(f"[{count}/{len(pdf_files)}] Added: {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    output_path = output_filename
    with open(output_path, 'wb') as out_file:
        pdf_writer.write(out_file)
    
    print(f"\n✅ All {count} PDFs merged into '{output_path}'")

if __name__ == "__main__":
    SOURCE_FOLDER = "./participants-odoo"
    OUTPUT_FILE = "merged_participants_odoo.pdf"
    merge_pdfs(SOURCE_FOLDER, OUTPUT_FILE)
