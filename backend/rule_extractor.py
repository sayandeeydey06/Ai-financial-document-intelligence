import re

# ---------- SAFE REGEX SEARCH ----------
def safe_search(pattern, text):
    if not text:
        return None
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None


# ---------- CONFIDENCE SCORE ----------
def calculate_confidence(data):
    score = 0
    fields = ["invoice_number", "total_amount", "tax_amount", "invoice_date"]

    for key in fields:
        if data.get(key):
            score += 1

    return round(score / len(fields), 2)


# ---------- SUMMARY ----------
def generate_summary(data):
    return (
        f"Invoice {data.get('invoice_number') or 'N/A'} "
        f"from {data.get('vendor_name') or 'unknown vendor'} "
        f"dated {data.get('invoice_date') or 'unknown date'}. "
        f"Total amount is {data.get('currency')} {data.get('total_amount') or 'N/A'} "
        f"with tax {data.get('tax_amount') or 'N/A'}."
    )


# ---------- RISK DETECTION ----------
def detect_risks(data):
    risks = []

    if not data.get("vendor_name"):
        risks.append("Missing vendor name")

    if not data.get("invoice_date"):
        risks.append("Invoice date missing")

    try:
        if data.get("total_amount"):
            amount = float(data["total_amount"].replace(",", ""))
            if amount > 10000:
                risks.append("High value invoice")
    except:
        pass

    try:
        if data.get("tax_amount") and data.get("total_amount"):
            tax = float(data["tax_amount"].replace(",", ""))
            total = float(data["total_amount"].replace(",", ""))
            if total > 0 and (tax / total) > 0.25:
                risks.append("Unusually high tax amount")
    except:
        pass

    return risks


# ---------- DOCUMENT CLASSIFICATION ----------
def classify_document(text):
    if not text:
        return "Unknown"

    t = text.lower()

    if "invoice" in t and ("total" in t or "bill to" in t):
        return "Invoice"
    if "receipt" in t or "thank you for your purchase" in t:
        return "Receipt"

    return "Unknown"


# ---------- MAIN EXTRACTION ----------
def extract_financial_data_rule_based(text):
    data = {
        "invoice_number": safe_search(r"invoice\s*#?\s*(\d+)", text),
        "vendor_name": safe_search(
            r"(?:from|vendor|company|seller|billed by)\s*[:\-]?\s*(.+)",
            text
        ),
        "invoice_date": safe_search(
            r"(?:date|invoice date)\s*[:\-]?\s*([A-Za-z0-9 ,]+)",
            text
        ),
        "total_amount": safe_search(
            r"(?:total amount|total)\s*\$?\s*([\d,]+\.\d{2})",
            text
        ),
        "tax_amount": safe_search(
            r"(?:tax|gst|vat)\s*\$?\s*([\d,]+\.\d{2})",
            text
        ),
        "currency": "USD",
        "extraction_method": "rule-based"
    }

    data["confidence"] = calculate_confidence(data)
    data["summary"] = generate_summary(data)
    data["risk_flags"] = detect_risks(data)
    data["document_type"] = classify_document(text)

    return data
