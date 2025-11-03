import requests
import json

url = "http://localhost:8000/process-claim"
pdf_path = "test.pdf"

try:
    print(f"Testing file: {pdf_path}")
    
    # Open and send the PDF file
    with open(pdf_path, 'rb') as pdf_file:
        files = {'file': ('test.pdf', pdf_file, 'application/pdf')}
        response = requests.post(url, files=files)
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        print("\n✅ SUCCESS!")
        result = response.json()
        print("\nExtracted Information:")
        print(json.dumps(result, indent=2))
    else:
        print("\n❌ ERROR:")
        print(response.text)
        
except FileNotFoundError:
    print(f"\n❌ File not found: {pdf_path}")
    print("\nMake sure the PDF file exists in the project directory")
except Exception as e:
    print(f"\n❌ Error: {e}")