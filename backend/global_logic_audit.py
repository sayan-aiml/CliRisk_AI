import requests
import json

url = "http://127.0.0.1:8000/api/v1/climate-risk/risk-score"

locations = [
    {
        "name": "Rajasthan (Jaisalmer Desert)",
        "lat": 26.9157,
        "lon": 70.9083,
        "tags": ["Desert", "Arid"]
    },
    {
        "name": "Mumbai (Coastal Mega-City)",
        "lat": 19.0760,
        "lon": 72.8777,
        "tags": ["Coastal", "High Density"]
    },
    {
        "name": "Ladakh (High Altitude)",
        "lat": 34.1526,
        "lon": 77.5771,
        "tags": ["Mountain", "Pristine"]
    },
    {
        "name": "Lucknow (Tier 2 Inland City)",
        "lat": 26.8467,
        "lon": 80.9462,
        "tags": ["Inland", "Urban"]
    }
]

def run_audit():
    print("="*60)
    print("GLOBAL GEOGRAPHIC LOGIC AUDIT")
    print("="*60)
    
    for loc in locations:
        payload = {
            "latitude": loc["lat"],
            "longitude": loc["lon"],
            "temperature_increase": 2.0,
            "precipitation_change": 10.0
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                print(f"   [ERROR] API {response.status_code}: {response.text}")
                continue
                
            data = response.json()
            
            print(f"\nLocation: {loc['name']} ({', '.join(loc['tags'])})")
            print(f"   - Heat Risk: {data['heat_risk_score']:.1f}")
            print(f"   - Flood Risk: {data['flood_risk_score']:.1f}")
            print(f"   - AQ Risk: {data['air_quality_risk_score']:.1f}")
            print(f"   - Water Scarcity: {data['water_scarcity_risk_score']:.1f}")
            print(f"   - Composite: {data['composite_risk_score']:.1f} ({data['risk_category']})")
            print(f"   - Drivers: {json.dumps(data['risk_drivers'], indent=2)}")
            
            # Logic Guardrails
            if loc["name"] == "Rajasthan (Jaisalmer Desert)":
                if data["flood_risk_score"] > 30: 
                    print("   [LOGIC FAIL] Desert should not have high flood risk.")
                if data["water_scarcity_risk_score"] < 40:
                    print("   [LOGIC FAIL] Desert should have high scarcity.")
            
            if loc["name"] == "Ladakh (High Altitude)":
                if data["air_quality_risk_score"] > 40:
                    print("   [LOGIC FAIL] Ladakh should have low AQ risk.")

        except Exception as e:
            print(f"   [CLIENT ERROR] {loc['name']}: {e}")

if __name__ == "__main__":
    run_audit()
