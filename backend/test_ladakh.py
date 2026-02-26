import requests
import json

url = "http://127.0.0.1:8000/api/v1/climate-risk/risk-score"

# Ladakh coordinates
payload = {
    "latitude": 34.1526,
    "longitude": 77.5771,
    "temperature_increase": 2.0,
    "precipitation_change": 10.0
}

print("Verifying Air Quality for Ladakh (Real-World Data)...")
response = requests.post(url, json=payload)
data = response.json()
print(f"Air Quality Risk Score: {data['air_quality_risk_score']}/100")
print(f"Total Composite Score: {data['composite_risk_score']}")
print(f"Risk Drivers: {json.dumps(data['risk_drivers'], indent=2)}")
