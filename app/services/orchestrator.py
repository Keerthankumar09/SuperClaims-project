from typing import List, Dict, Any
from app.agents.classifier import DocumentClassifier
from app.agents.processor import BillProcessor, DischargeSummaryProcessor, IDCardProcessor
from app.agents.validator import ClaimValidator
from app.utils.pdf_utils import extract_text_from_pdf
import logging

logger = logging.getLogger(__name__)

class ClaimOrchestrator:
    """Orchestrates the multi-agent workflow"""
    
    def __init__(self):
        self.classifier = DocumentClassifier()
        self.bill_processor = BillProcessor()
        self.discharge_processor = DischargeSummaryProcessor()
        self.id_processor = IDCardProcessor()
        self.validator = ClaimValidator()
    
    async def process_claim(self, files: List[tuple]) -> Dict[str, Any]:
        """
        Main orchestration method
        files: List of (filename, file_bytes) tuples
        """
        processed_documents = []
        
        # Step 1: Extract and Classify each document
        for filename, file_bytes in files:
            logger.info(f"Processing file: {filename}")
            
            # Extract text
            text = await extract_text_from_pdf(file_bytes, filename)
            
            # DEBUG: Log extracted text preview
            if text:
                logger.info(f"Extracted {len(text)} chars from {filename}")
                logger.info(f"Text preview: {text[:300]}...")
            else:
                logger.warning(f"No text extracted from {filename}")
                continue
            
            # Classify document
            doc_type = await self.classifier.classify(filename, text)
            logger.info(f"Classified {filename} as: {doc_type}")
            
            # Process based on type
            if doc_type == "bill":
                doc_data = await self.bill_processor.process(text)
            elif doc_type == "discharge_summary":
                doc_data = await self.discharge_processor.process(text)
            elif doc_type == "id_card":
                doc_data = await self.id_processor.process(text)
            else:
                logger.warning(f"Unknown document type: {doc_type}")
                continue
            
            logger.info(f"Processed {filename}: {doc_data}")
            processed_documents.append(doc_data)
        
        logger.info(f"Total documents processed: {len(processed_documents)}")
        
        # Step 2: Validate all documents together
        validation_result = await self.validator.validate(processed_documents)
        
        # Step 3: Structure final response
        return {
            "documents": processed_documents,
            "validation": {
                "missing_documents": validation_result["missing_documents"],
                "discrepancies": validation_result["discrepancies"]
            },
            "claim_decision": validation_result["claim_decision"]
        }
