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

### Test with Python Script

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
