from PIL import Image
import pytesseract
import pdfplumber
from pdf2image import convert_from_path
import tempfile
import os

def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        return pytesseract.image_to_string(img)
    except:
        return ""

def extract_text_from_pdf(pdf_path):
    text = ""

    # 1️⃣ Try normal text PDF
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    # 2️⃣ If no text → OCR the PDF pages
    if not text.strip():
        images = convert_from_path(pdf_path)
        for img in images:
            text += pytesseract.image_to_string(img)

    return text

