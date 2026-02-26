import requests
import json

url = "http://127.0.0.1:8000/api/v1/climate-risk/risk-score"

locations = [
    {"name": "New York (Coastal)", "lat": 40.7128, "lon": -74.0060},
    {"name": "Dubai (Extreme Heat)", "lat": 25.2048, "lon": 55.2708},
    {"name": "New Delhi (Tropical/Dense)", "lat": 28.6139, "lon": 77.2090}
]

def audit_location(loc):
    payload = {
        "latitude": loc["lat"],
        "longitude": loc["lon"],
        "temperature_increase": 2.0,
        "precipitation_change": 10.0
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"\n--- {loc['name']} ---")
            print(f"Composite Risk: {data['composite_risk_score']}")
            print(f"Heat Risk: {data['heat_risk_score']}")
            print(f"Flood Risk: {data['flood_risk_score']}")
            print(f"Category: {data['risk_category']}")
            return data
        else:
            print(f"Error for {loc['name']}: {response.text}")
    except Exception as e:
        print(f"Failed for {loc['name']}: {e}")

print("Starting Commercial Accuracy Audit...")
for loc in locations:
    audit_location(loc)
