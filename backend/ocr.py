import pytesseract
from PIL import Image
import pdfplumber

def extract_text_from_image(image_path):
    try:
        import pytesseract
        from PIL import Image
        return pytesseract.image_to_string(Image.open(image_path))
    except Exception as e:
        return ""


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text
