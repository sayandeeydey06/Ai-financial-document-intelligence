import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/text-bison-001")

def extract_financial_data_gemini(text: str):
    prompt = f"""
Extract the following fields from the invoice text.
Return ONLY valid JSON.

Fields:
- invoice_number
- vendor_name
- invoice_date
- total_amount
- tax_amount
- currency

Invoice Text:
{text}
"""

    response = model.generate_content(prompt)
    output = response.text

    match = re.search(r'\{.*\}', output, re.DOTALL)
    if not match:
        return {
            "error": "No JSON detected",
            "raw_output": output
        }

    return json.loads(match.group())
