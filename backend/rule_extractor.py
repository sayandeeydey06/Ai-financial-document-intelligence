import re

def safe_search(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None


def calculate_confidence(data):
    score = 0
    for key in ["invoice_number", "total_amount", "tax_amount", "invoice_date"]:
        if data.get(key):
            score += 0.25
    return round(score, 2)


def generate_summary(data):
    return (
        f"Invoice {data.get('invoice_number', 'unknown')} "
        f"from {data.get('vendor_name') or 'unknown vendor'} "
        f"dated {data.get('invoice_date') or 'unknown date'}. "
        f"Total amount is {data.get('currency')} {data.get('total_amount')} "
        f"with tax {data.get('tax_amount')}."
    )


def detect_risks(data):
    risks = []

    if not data.get("vendor_name"):
        risks.append("Missing vendor name")

    if not data.get("invoice_date"):
        risks.append("Invoice date missing")

    if data.get("total_amount"):
        amount = float(data["total_amount"].replace(",", ""))
        if amount > 10000:
            risks.append("High value invoice")

    if data.get("tax_amount") and data.get("total_amount"):
        tax = float(data["tax_amount"].replace(",", ""))
        total = float(data["total_amount"].replace(",", ""))
        if tax / total > 0.25:
            risks.append("Unusually high tax amount")

    return risks

def classify_document(text):
    text = text.lower()

    if "invoice" in text and "total" in text:
        return "Invoice"
    if "receipt" in text or "thank you for your purchase" in text:
        return "Receipt"
    if "bill to" in text and "due date" in text:
        return "Invoice"

    return "Unknown"



def extract_financial_data_rule_based(text):
    data = {
        "invoice_number": safe_search(r"Invoice\s*#?\s*(\w+)", text),
        "vendor_name": safe_search(r"Your Company Name\s*\|\s*(.+)", text),
        "invoice_date": safe_search(r"Date[:\s]*([A-Za-z0-9 ,]+)", text),
        "total_amount": safe_search(r"Total\s*\$?([\d,]+\.\d{2})", text),
        "tax_amount": safe_search(r"Tax.*?\$?([\d,]+\.\d{2})", text),
        "currency": "USD",
        "extraction_method": "rule-based"
    }

    data["confidence"] = calculate_confidence(data)
    data["summary"] = generate_summary(data)
    data["risk_flags"] = detect_risks(data)

    data["document_type"] = classify_document(text)

    return data
