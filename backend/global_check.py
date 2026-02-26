import requests
import json

url = "http://127.0.0.1:8000/api/v1/climate-risk/risk-score"

locations = [
    {"name": "Andaman Islands", "lat": 11.6234, "lon": 92.7265},
    {"name": "Swiss Alps (Zermatt)", "lat": 46.0207, "lon": 7.7491},
    {"name": "Amazon Rainforest", "lat": -3.4653, "lon": -60.0217},
    {"name": "Tokyo (High Density)", "lat": 35.6895, "lon": 139.6917}
]

def audit():
    for loc in locations:
        payload = {
            "latitude": loc["lat"],
            "longitude": loc["lon"],
            "temperature_increase": 1.5,
            "precipitation_change": 5.0
        }
        resp = requests.post(url, json=payload)
        data = resp.json()
        print(f"\n--- {loc['name']} ---")
        print(f"AQ Risk: {data['air_quality_risk_score']}")
        print(f"Flood Risk: {data['flood_risk_score']}")
        print(f"Heat Risk: {data['heat_risk_score']}")
        print(f"Drivers: {json.dumps(data['risk_drivers'], indent=2)}")

if __name__ == "__main__":
    audit()
