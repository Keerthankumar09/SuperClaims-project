import requests

url = "http://localhost:8000/process-claim"

with open('bill.pdf', 'rb') as f1:
    files = [
        ('files', ('bill.pdf', f1, 'application/pdf'))
    ]
    
    print("Uploading Apollo hospital bill...")
    response = requests.post(url, files=files)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("\n✅ SUCCESS!")
        import json
        print(json.dumps(response.json(), indent=2))
    else:
        print("\n❌ ERROR:")
        print(response.text)
