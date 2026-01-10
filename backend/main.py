from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import os
import csv
import json
import uuid

from ocr import extract_text_from_image, extract_text_from_pdf
from rule_extractor import extract_financial_data_rule_based

app = FastAPI()

# -------------------- CORS --------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- DIRECTORIES --------------------

UPLOAD_DIR = "uploads"
EXPORT_DIR = "exports"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

# -------------------- HOME --------------------

@app.get("/")
def home():
    return {"message": "AI Financial Document Intelligence API running"}

# -------------------- ANALYZE DOCUMENT --------------------

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    try:
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # OCR
        if file.filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        else:
            text = extract_text_from_image(file_path)

        # ---------------- SAFETY CHECK ----------------
        if not text or not text.strip():
            extracted_data = {
                "invoice_number": None,
                "vendor_name": None,
                "invoice_date": None,
                "total_amount": None,
                "tax_amount": None,
                "currency": "USD",
                "confidence": 0,
                "extraction_method": "rule-based",
                "summary": "OCR unavailable in deployment environment",
                "risk_flags": ["OCR not available"],
                "document_type": "Unknown"
            }

            return {
                "status": "success",
                "file_id": file_id,
                "filename": file.filename,
                "document_type": "Unknown",
                "extracted_data": extracted_data
            }

        # ---------------- NORMAL EXTRACTION ----------------
        extracted_data = extract_financial_data_rule_based(text)

        return {
            "status": "success",
            "file_id": file_id,
            "filename": file.filename,
            "document_type": extracted_data.get("document_type", "Unknown"),
            "extracted_data": extracted_data
        }

    except Exception as e:
        print("\n🔥 ERROR INSIDE /analyze 🔥\n", str(e))
        return {
            "status": "error",
            "message": str(e)
        }

# -------------------- EXPORT JSON --------------------

@app.post("/export/json/{file_id}")
def export_json(file_id: str, data: dict):
    file_path = os.path.join(EXPORT_DIR, f"{file_id}.json")

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    return FileResponse(
        path=file_path,
        media_type="application/json",
        filename=f"{file_id}.json"
    )

# -------------------- EXPORT CSV --------------------

@app.post("/export/csv/{file_id}")
def export_csv(file_id: str, data: dict):
    file_path = os.path.join(EXPORT_DIR, f"{file_id}.csv")

    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Field", "Value"])
        for key, value in data.items():
            writer.writerow([key, value])

    return FileResponse(
        path=file_path,
        media_type="text/csv",
        filename=f"{file_id}.csv"
    )

# -------------------- LOCAL RUN --------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
