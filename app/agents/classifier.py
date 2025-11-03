from dotenv import load_dotenv
import os

load_dotenv()

import google.generativeai as genai
from typing import Literal
import json
import logging

logger = logging.getLogger(__name__)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class DocumentClassifier:
    """Agent to classify document type"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    async def classify(self, filename: str, text_preview: str) -> str:
        """Classify document based on filename and text content"""
        
        # First try direct pattern matching
        text_preview_lower = text_preview.lower()
        
        if "bill no" in text_preview_lower and ("amount" in text_preview_lower or "charges" in text_preview_lower):
            logger.info("Classified as bill based on pattern match")
            return "bill"
        
        if "discharge summary" in text_preview_lower or "discharged" in text_preview_lower:
            logger.info("Classified as discharge_summary based on pattern match")
            return "discharge_summary"
        
        if "policy" in text_preview_lower and "insurance" in text_preview_lower:
            logger.info("Classified as id_card based on pattern match")
            return "id_card"
        
        # If pattern matching fails, use AI classification
        prompt = f"""
You are a document classification expert for insurance claims.

Text to classify:
{text_preview[:1000]}

Choose ONE category:
- bill (if you see: bill number, charges, amounts, hospital fees)
- discharge_summary (if you see: discharge date, diagnosis, treatment)
- id_card (if you see: policy number, insurance details)
- other

Return ONLY the category name, nothing else.
"""
        
        try:
            response = self.model.generate_content(prompt)
            doc_type = response.text.strip().lower()
            
            logger.info(f"Classifier raw response: {response.text}")
            
            # Validate response
            valid_types = ["bill", "discharge_summary", "id_card", "other"]
            if doc_type not in valid_types:
                logger.warning(f"Invalid classification: {doc_type}, defaulting to 'other'")
                doc_type = "other"
            
            return doc_type
        except Exception as e:
            logger.error(f"Classification error: {str(e)}")
            return "other"
