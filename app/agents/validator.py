from dotenv import load_dotenv
import os

load_dotenv()

import google.generativeai as genai
import json
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class ClaimValidator:
    """Agent to validate claim completeness and consistency"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    async def validate(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate documents for completeness and consistency"""
        
        # Check for required document types
        doc_types = [doc.get("type") for doc in documents]
        required_types = ["bill", "discharge_summary", "id_card"]
        missing_docs = [dt for dt in required_types if dt not in doc_types]
        
        logger.info(f"Document types found: {doc_types}")
        logger.info(f"Missing documents: {missing_docs}")
        
        if not documents:
            return {
                "missing_documents": missing_docs,
                "discrepancies": ["No documents were successfully processed"],
                "claim_decision": {
                    "status": "rejected",
                    "reason": "No documents provided or all documents failed processing"
                }
            }
        
        # Prepare validation prompt
        prompt = f"""
You are an insurance claim validator. Analyze these documents and check for discrepancies.

Documents:
{json.dumps(documents, indent=2)}

Check for:
1. Name consistency across documents
2. Date consistency (discharge date should be after admission date)
3. Missing critical information
4. Any suspicious patterns

Return ONLY valid JSON with this structure:
{{
  "discrepancies": ["list of issues found"],
  "approval_recommendation": "approved" or "rejected" or "pending",
  "reason": "explanation for the decision"
}}

Respond with ONLY the JSON object:
"""
        
        try:
            response = self.model.generate_content(prompt)
            raw_text = response.text.strip()
            
            logger.info(f"Validator raw response: {raw_text[:200]}...")
            
            # Clean potential markdown formatting
            if raw_text.startswith("```"):
                raw_text = raw_text.split("```")[1]
                if raw_text.startswith("json"):
                    raw_text = raw_text[4:]
            
            validation_result = json.loads(raw_text.strip())
            
            return {
                "missing_documents": missing_docs,
                "discrepancies": validation_result.get("discrepancies", []),
                "claim_decision": {
                    "status": validation_result.get("approval_recommendation", "pending"),
                    "reason": validation_result.get("reason", "Validation completed")
                }
            }
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return {
                "missing_documents": missing_docs,
                "discrepancies": ["Could not perform automated validation"],
                "claim_decision": {
                    "status": "pending",
                    "reason": "Manual review required due to validation errors"
                }
            }
