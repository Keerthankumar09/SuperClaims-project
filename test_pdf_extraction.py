# test_pdf_extraction.py
import asyncio
import sys
sys.path.insert(0, '.')
from app.utils.pdf_utils import extract_text_from_pdf

async def test():
    with open('bill.pdf', 'rb') as f:
        pdf_bytes = f.read()
    
    print(f"PDF size: {len(pdf_bytes)} bytes")
    text = await extract_text_from_pdf(pdf_bytes, 'bill.pdf')
    print(f"\nExtracted {len(text)} characters")
    print(f"\nText:\n{text[:1000]}")

asyncio.run(test())
