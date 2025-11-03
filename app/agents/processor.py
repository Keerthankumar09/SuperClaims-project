from dotenv import load_dotenv
import os

load_dotenv()

import google.generativeai as genai
import json
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class BillProcessor:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    async def process(self, text: str) -> Dict[str, Any]:
        prompt = f"""
You are a data extraction expert. Extract EXACT information from this hospital bill.

TEXT:
{text[:3000]}

Extract these fields:
- hospital_name: Name of the hospital/medical facility
- total_amount: Total bill amount as a NUMBER (no currency symbols)
- date_of_service: Date in YYYY-MM-DD format

IMPORTANT: Return ONLY valid JSON in this exact format:
{{
  "hospital_name": "extracted name or null",
  "total_amount": 12500,
  "date_of_service": "2024-04-10"
}}

If you cannot find a field, use null. Do NOT include any explanation or markdown.
"""
        try:
            response = self.model.generate_content(prompt)
            raw_text = response.text.strip()
            logger.info(f"BillProcessor raw: {raw_text}")
            
            # Clean markdown
            if raw_text.startswith("```"):
                lines = raw_text.split("\n")
                raw_text = "\n".join(lines[1:-1])
                if raw_text.startswith("json"):
                    raw_text = raw_text[4:]
            
            result = json.loads(raw_text.strip())
            result["type"] = "bill"
            result["items"] = []
            return result
        except Exception as e:
            logger.error(f"BillProcessor error: {e}")
            logger.error(f"Raw response was: {raw_text if 'raw_text' in locals() else 'N/A'}")
            return {"type": "bill", "hospital_name": None, "total_amount": None, "date_of_service": None, "items": []}


class DischargeSummaryProcessor:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    async def process(self, text: str) -> Dict[str, Any]:
        prompt = f"""
You are a data extraction expert. Extract EXACT information from this discharge summary.

TEXT:
{text[:3000]}

Extract these fields:
- patient_name: Full name of the patient
- diagnosis: Primary diagnosis or medical condition
- admission_date: Date admitted in YYYY-MM-DD format
- discharge_date: Date discharged in YYYY-MM-DD format
- doctor_name: Name of attending physician/doctor

IMPORTANT: Return ONLY valid JSON in this exact format:
{{
  "patient_name": "extracted name or null",
  "diagnosis": "extracted diagnosis or null",
  "admission_date": "2024-04-01",
  "discharge_date": "2024-04-10",
  "doctor_name": "Dr. Name or null"
}}

If you cannot find a field, use null. Do NOT include any explanation or markdown.
"""
        try:
            response = self.model.generate_content(prompt)
            raw_text = response.text.strip()
            logger.info(f"DischargeSummaryProcessor raw: {raw_text}")
            
            # Clean markdown
            if raw_text.startswith("```"):
                lines = raw_text.split("\n")
                raw_text = "\n".join(lines[1:-1])
                if raw_text.startswith("json"):
                    raw_text = raw_text[4:]
            
            result = json.loads(raw_text.strip())
            result["type"] = "discharge_summary"
            return result
        except Exception as e:
            logger.error(f"DischargeSummaryProcessor error: {e}")
            logger.error(f"Raw response was: {raw_text if 'raw_text' in locals() else 'N/A'}")
            return {"type": "discharge_summary", "patient_name": None, "diagnosis": None, "admission_date": None, "discharge_date": None, "doctor_name": None}


class IDCardProcessor:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    async def process(self, text: str) -> Dict[str, Any]:
        prompt = f"""
You are a data extraction expert. Extract EXACT information from this insurance ID card.

TEXT:
{text[:3000]}

Extract these fields:
- policy_number: Insurance policy number
- patient_name: Name of the insured member
- dob: Date of birth in YYYY-MM-DD format
- insurance_provider: Name of insurance company

IMPORTANT: Return ONLY valid JSON in this exact format:
{{
  "policy_number": "extracted number or null",
  "patient_name": "extracted name or null",
  "dob": "1985-05-15",
  "insurance_provider": "company name or null"
}}

If you cannot find a field, use null. Do NOT include any explanation or markdown.
"""
        try:
            response = self.model.generate_content(prompt)
            raw_text = response.text.strip()
            logger.info(f"IDCardProcessor raw: {raw_text}")
            
            # Clean markdown
            if raw_text.startswith("```"):
                lines = raw_text.split("\n")
                raw_text = "\n".join(lines[1:-1])
                if raw_text.startswith("json"):
                    raw_text = raw_text[4:]
            
            result = json.loads(raw_text.strip())
            result["type"] = "id_card"
            return result
        except Exception as e:
            logger.error(f"IDCardProcessor error: {e}")
            logger.error(f"Raw response was: {raw_text if 'raw_text' in locals() else 'N/A'}")
            return {"type": "id_card", "policy_number": None, "patient_name": None, "dob": None, "insurance_provider": None}
