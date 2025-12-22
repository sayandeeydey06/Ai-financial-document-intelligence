# AI Financial Document Intelligence Platform

An end-to-end AI system that extracts structured financial data from invoice images and PDFs.

## 🚀 Features
- OCR-based text extraction (Image & PDF)
- Invoice data extraction (Invoice No, Total, Tax, Date)
- Document type classification
- Confidence scoring
- Editable AI results (Human-in-the-loop)
- Export extracted data (JSON / CSV)
- FastAPI backend + React frontend

## 🧠 Tech Stack
- Backend: FastAPI, Python
- Frontend: React + Vite
- OCR: Tesseract
- AI Logic: Rule-based extraction
- UI: Editable AI output

## 📸 Demo
Upload an invoice image or PDF and get structured financial data instantly.

## 🏁 Run Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
