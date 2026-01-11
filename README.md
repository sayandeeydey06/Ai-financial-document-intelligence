📄 AI Financial Document Intelligence Platform :

An AI-powered web application that extracts structured financial data from invoices (PDFs and images), including totals, tax, invoice numbers, risk indicators, and document classification.

✨ Features :

Upload invoice images or PDFs

OCR-based text extraction

AI-powered financial field detection

Invoice number, date, total, tax, vendor extraction

Confidence scoring

Risk flag detection

Document classification (Invoice / Receipt / Unknown)

Editable extracted data

JSON & CSV export

Cloud deployment (Vercel + Render)

🧠 How It Works :

User uploads a document

OCR converts the document into raw text

Rule-based AI extracts financial fields

Confidence score and risk flags are calculated

Results are displayed and can be edited or exported

⚠️ Production OCR Limitation :

This project uses Tesseract OCR locally for high-accuracy image text extraction.

In cloud deployments (Vercel/Render), system-level OCR binaries are restricted.
To handle this, the system implements a graceful fallback mode:

        1.PDF documents with text → fully supported
        2.Image OCR → safely disabled in cloud
        3.The system returns structured placeholders instead of crashing

This design reflects real-world production constraints and demonstrates cloud-safe AI engineering.


🛠️ Tech Stack :

Frontend: React (Vercel)

Backend: FastAPI (Render)

AI: OCR + Rule-based NLP

Language: Python, JavaScript

Export: CSV, JSON

Deployment: Cloud-hosted REST architecture