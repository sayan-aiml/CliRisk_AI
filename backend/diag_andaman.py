import asyncio
import json
import sys
import os

# Add the backend directory to sys.path
sys.path.append(os.path.abspath("."))

from app.services.data_providers.open_meteo import open_meteo_provider

async def main():
    lat, lon = 11.6234, 92.7265
    aq = await open_meteo_provider.get_air_quality(lat, lon)
    
    print(f"Air Quality Raw: {json.dumps(aq, indent=2)}")
    
    # Simulate risk calc logic
    no2_val = aq.get("no2", 0)
    if no2_val > 40: urban_density = 0.9
    elif no2_val > 20: urban_density = 0.65
    elif no2_val > 10: urban_density = 0.4
    else: urban_density = 0.15
    
    is_remote = (urban_density < 0.3)
    aqi_value = aq.get("aqi", 20)
    
    effective_aqi = aqi_value
    if is_remote and aqi_value > 40:
        effective_aqi = 30 + (aqi_value - 40) * 0.3
        
    aqi_risk = min(100, (effective_aqi / 80) * 100)
    final_aq_score = (aqi_risk * 0.8) + (urban_density * 20)
    
    print(f"NO2 Value: {no2_val}")
    print(f"Urban Density: {urban_density}")
    print(f"Is Remote: {is_remote}")
    print(f"Effective AQI: {effective_aqi}")
    print(f"AQ Risk (Normalized): {aqi_risk}")
    print(f"Final AQ Score: {final_aq_score}")

if __name__ == "__main__":
    asyncio.run(main())
