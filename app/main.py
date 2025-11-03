from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from app.services.orchestrator import ClaimOrchestrator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Superclaims Backend",
    description="AI-Driven Claims Processing API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = ClaimOrchestrator()

@app.get("/")
async def root():
    return {"message": "Superclaims Backend API"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "superclaims-backend"}

@app.post("/process-claim")
async def process_claim(files: List[UploadFile] = File(...)):
    """Process insurance claim documents"""
    try:
        # Read uploaded files
        file_data = []
        for file in files:
            content = await file.read()
            file_data.append((file.filename, content))
        
        # Process through orchestrator
        result = await orchestrator.process_claim(file_data)
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing claim: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
