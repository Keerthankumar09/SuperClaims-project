### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        User Upload                          │
│                    (Multiple PDF Files)                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Server                            │
│              POST /process-claim endpoint                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Orchestrator Agent                         │
│           (Coordinates entire workflow)                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
┌─────────────┐ ┌──────────┐ ┌──────────────┐
│   Extract   │ │ Classify │ │   Process    │
│   Text      │ │ Document │ │   by Type    │
│             │ │          │ │              │
│ pdfplumber  │ │ Pattern  │ │ Bill/        │
│ + Gemini    │ │ Match +  │ │ Discharge/   │
│ Vision OCR  │ │ Gemini   │ │ ID Card      │
│             │ │ LLM      │ │ (Gemini LLM) │
└─────────────┘ └──────────┘ └──────────────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Validator Agent                            │
│         (Check completeness & consistency)                  │
│                   (Gemini LLM)                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                 Structured JSON Response                    │
│   - Extracted documents with structured data                │
│   - Validation results                                      │
│   - Claim decision (approved/rejected/pending)              │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. **FastAPI Server** (`app/main.py`)
- **REST API Endpoint:** `POST /process-claim`
- **Input:** Multiple PDF files (multipart/form-data)
- **Output:** Structured JSON with extracted data and validation
- **Features:** CORS enabled, health check endpoint, Swagger documentation

### 2. **Orchestrator** (`app/services/orchestrator.py`)
- **Role:** Coordinates all agents and manages workflow
- **Process Flow:**
  1. Receives uploaded PDF files
  2. Extracts text from each PDF
  3. Classifies document type
  4. Routes to appropriate processor agent
  5. Aggregates all processed documents
  6. Validates completeness and consistency
  7. Returns structured response

### 3. **PDF Text Extraction** (`app/utils/pdf_utils.py`)
- **Text PDFs:** Uses `pdfplumber` for direct text extraction
- **Image PDFs (Scanned):** Uses Gemini Vision API for OCR
- **Smart Fallback:** Automatically detects low text extraction and switches to Vision API
- **Performance:** Converts PDF pages to images at 200 DPI for optimal OCR



## Technology Stack

- **Framework:** FastAPI
- **AI Model:** Google Gemini 2.0 Flash (text) + Gemini Vision (OCR)
- **PDF Processing:** pdfplumber, Pillow
- **Language:** Python 3.9+
- **Environment:** python-dotenv

---

## Setup & Installation

### 1. Install Dependencies

pip install -r requirements.txt



### 2. Configure Environment

Create `.env` file:
GOOGLE_API_KEY=your_gemini_api_key_here
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760



### 3. Run Server

uvicorn app.main:app --reload



Server runs at: `http://localhost:8000`

### 4. Access API Documentation

Swagger UI: `http://localhost:8000/docs`

---

## Testing

import requests

url = "http://localhost:8000/process-claim"

with open('bill.pdf', 'rb') as f1,
open('discharge_summary.pdf', 'rb') as f2,
open('id_card.pdf', 'rb') as f3:

text
files = [
    ('files', ('bill.pdf', f1, 'application/pdf')),
    ('files', ('discharge_summary.pdf', f2, 'application/pdf')),
    ('files', ('id_card.pdf', f3, 'application/pdf'))
]

response = requests.post(url, files=files)
print(response.json())
text

---

## Agentic Workflow Benefits

1. **Autonomous Processing:** Each agent independently handles its specialized task
2. **Scalability:** Easy to add new document types or validation rules
3. **Flexibility:** Agents can be updated or replaced without affecting others
4. **Fault Tolerance:** Errors in one agent don't crash the entire pipeline
5. **Transparency:** Each agent logs its decisions for auditing

---

## Future Enhancements

- [ ] Add support for additional document types (prescriptions, lab reports)
- [ ] Implement caching for repeated document processing
- [ ] Add support for multiple languages
- [ ] Enhance validation with medical code verification (ICD-10, CPT)
- [ ] Add user authentication and claim tracking
