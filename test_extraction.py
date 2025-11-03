import asyncio
from app.agents.processor import DischargeSummaryProcessor

async def test():
    processor = DischargeSummaryProcessor()
    
    # Sample text
    text = """
    DISCHARGE SUMMARY
    Patient Name: John Doe
    Diagnosis: Fracture
    Admission Date: 2024-04-01
    Discharge Date: 2024-04-10
    Doctor: Dr. Smith
    """
    
    result = await processor.process(text)
    print(result)

asyncio.run(test())
