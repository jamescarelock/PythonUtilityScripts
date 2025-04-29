import sys
import os
import pytesseract
from pdf2image import convert_from_path

def pdf_to_text(pdf_path):
    # Optional: If Tesseract is not in PATH, set it explicitly:
    # pytesseract.pytesseract.tesseract_cmd = r'"C:\Users\jcarelock\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"'

    if not os.path.isfile(pdf_path):
        print(f"Error: File '{pdf_path}' not found.")
        return

    print(f"Processing PDF: {pdf_path}")
    images = convert_from_path(pdf_path)
    print(f"Converted {len(images)} pages to images.")

    text_output = []
    for i, image in enumerate(images):
        print(f"OCR on page {i + 1}...")
        text = pytesseract.image_to_string(image)
        text_output.append(f"--- Page {i + 1} ---\n{text}\n")

    output_path = os.path.splitext(pdf_path)[0] + ".txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(text_output)

    print(f"OCR complete. Output saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pdf_ocr.py <path_to_pdf>")
    else:
        pdf_to_text(sys.argv[1])
