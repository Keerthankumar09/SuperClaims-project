# test_api.py
from dotenv import load_dotenv
import os
import requests

# Load .env with explicit path
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

# Test if API key is loaded
api_key = os.getenv("GOOGLE_API_KEY")  # ← FIXED: Use the variable NAME, not the value
if api_key:
    print(f"✅ API Key loaded successfully!")
    print(f"   First 10 chars: {api_key[:10]}")
    print(f"   Last 4 chars: ...{api_key[-4:]}")
else:
    print("❌ API Key NOT found!")
    print(f"   Tried loading from: {env_path}")
    print(f"   File exists: {os.path.exists(env_path)}")
    exit(1)

print("\n" + "="*50)
print("Testing API Endpoint...")
print("="*50 + "\n")

url = "http://localhost:8000/process-claim"

# Replace with actual file paths
files = [
    ('files', open('bill.pdf', 'rb')),
    ('files', open('discharge_summary.pdf', 'rb')),
    ('files', open('id_card.pdf', 'rb'))
]

try:
    response = requests.post(url, files=files)
    print("Status Code:", response.status_code)
    print("\nResponse:")
    print(response.json())
except FileNotFoundError as e:
    print(f"❌ Error: PDF file not found - {e}")
    print("   Make sure PDF files are in the current directory or update the file paths")
except requests.exceptions.ConnectionError:
    print("❌ Error: Cannot connect to server")
    print("   Make sure uvicorn is running: uvicorn app.main:app --reload")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    for _, file in files:
        file.close()
