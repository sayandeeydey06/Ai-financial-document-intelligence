import re

def extract_financial_data(text):
    # Find amounts like ₹4500, $1200.50, 4500.00
    amounts = re.findall(r'(₹|\$)?\s?\d+[,.]?\d*', text)

    # Find dates like 12/09/2024 or 2024-09-12
    dates = re.findall(r'\d{2}[/-]\d{2}[/-]\d{4}', text)

    # Find invoice number (basic)
    invoice_no = re.findall(r'Invoice\s*No[:\s]*([A-Za-z0-9-]+)', text, re.IGNORECASE)

    return {
        "amounts": list(set(amounts)),
        "dates": list(set(dates)),
        "invoice_number": invoice_no[0] if invoice_no else None
    }
