import requests
import json

url = "http://127.0.0.1:8000/api/v1/climate-risk/risk-score"

# Test 3 coordinates in Dubai within 50-100m of each other
test_points = [
    {"lat": 25.2048, "lon": 55.2708},
    {"lat": 25.2045, "lon": 55.2705},
    {"lat": 25.2049, "lon": 55.2709}
]

print("Verifying Stability for Dubai...")
for i, pt in enumerate(test_points):
    payload = {
        "latitude": pt["lat"],
        "longitude": pt["lon"],
        "temperature_increase": 2.0,
        "precipitation_change": 10.0
    }
    response = requests.post(url, json=payload)
    data = response.json()
    print(f"Click {i+1}: Score = {data['composite_risk_score']}, Category = {data['risk_category']}")
