import requests
import json

url = "http://127.0.0.1:8000/api/v1/climate-risk/risk-score"
payload = {
    "latitude": 28.6139,
    "longitude": 77.2090,
    "temperature_increase": 2.0,
    "precipitation_change": 10.0
}

try:
    print(f"Sending request to {url}...")
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Success!")
        print(json.dumps(response.json(), indent=2))
    else:
        print("Error Response:")
        print(response.text)
except Exception as e:
    print(f"Connection failed: {e}")
