import pdfplumber
import io
from typing import Optional
import logging
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

async def extract_text_from_pdf(pdf_bytes: bytes, filename: str) -> str:
    """Extract text from PDF - supports both text and image PDFs"""
    try:
        text = ""
        
        # Try normal text extraction first
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    text += page_text + "\n"
        
        # If no text found (or very little), use Gemini Vision for OCR
        if len(text.strip()) < 50:
            logger.info(f"Minimal text extracted from {filename} ({len(text)} chars), using Gemini Vision OCR...")
            text = await extract_text_with_vision(pdf_bytes, filename)
        else:
            logger.info(f"Successfully extracted {len(text)} chars from {filename} using text extraction")
        
        return text.strip()
        
    except Exception as e:
        logger.error(f"Error in extract_text_from_pdf for {filename}: {str(e)}")
        # Try Vision API as fallback
        try:
            logger.info(f"Falling back to Vision API for {filename}")
            return await extract_text_with_vision(pdf_bytes, filename)
        except Exception as ve:
            logger.error(f"Vision API also failed for {filename}: {str(ve)}")
            return ""


async def extract_text_with_vision(pdf_bytes: bytes, filename: str) -> str:
    """Use Gemini Vision to extract text from image-based PDFs"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        text = ""
        
        # Convert PDF pages to images
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            total_pages = len(pdf.pages)
            logger.info(f"Processing {total_pages} pages with Gemini Vision...")
            
            for i, page in enumerate(pdf.pages):
                try:
                    # Convert page to PIL image
                    pil_image = page.to_image(resolution=200).original
                    
                    # Use Gemini Vision to extract text
                    prompt = """
Extract ALL text from this document image exactly as it appears.
Include:
- Patient names
- Bill numbers, policy numbers
- All amounts and charges
- All dates
- Doctor names
- Diagnoses
- Any other text visible

Return only the extracted text in a clear, organized format.
"""
                    
                    response = model.generate_content([prompt, pil_image])
                    page_text = response.text.strip()
                    
                    if page_text:
                        logger.info(f"Gemini Vision extracted {len(page_text)} chars from page {i+1}/{total_pages}")
                        text += f"\n--- Page {i+1} ---\n{page_text}\n"
                    else:
                        logger.warning(f"No text extracted from page {i+1}/{total_pages}")
                        
                except Exception as pe:
                    logger.error(f"Error processing page {i+1}: {str(pe)}")
                    continue
        
        return text.strip()
        
    except Exception as e:
        logger.error(f"Vision OCR error for {filename}: {str(e)}")
        return ""
