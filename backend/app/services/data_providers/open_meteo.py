import httpx
import logging
import json
import redis.asyncio as redis
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from app.core.config import settings

logger = logging.getLogger(__name__)

class OpenMeteoProvider:
    """
    Client for Open-Meteo APIs (Historical, Elevation, and Climate Projections)
    """
    
    BASE_URL_ELEVATION = "https://api.open-meteo.com/v1/elevation"
    BASE_URL_HISTORICAL = "https://archive-api.open-meteo.com/v1/archive"
    BASE_URL_CLIMATE = "https://climate-api.open-meteo.com/v1/climate"
    BASE_URL_AIR_QUALITY = "https://air-quality-api.open-meteo.com/v1/air-quality"

    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout
        try:
            self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
            self.redis_available = True
        except Exception:
            logger.warning("Redis not available. Data will not be cached.")
            self.redis_available = False
        self.cache_expiry = 86400  # 24 hours

    async def get_elevation(self, lat: float, lon: float) -> Optional[float]:
        """Fetch elevation for coordinates (with Redis caching)"""
        cache_key = f"elevation:{round(float(lat), 4)}:{round(float(lon), 4)}"
        try:
            # Check cache
            if self.redis_available:
                cached = await self.redis.get(cache_key)
                if cached:
                    return float(cached)

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                params = {"latitude": lat, "longitude": lon}
                response = await client.get(self.BASE_URL_ELEVATION, params=params)
                response.raise_for_status()
                data = response.json()
                elevation = data.get("elevation", [None])[0]
                
                if elevation is not None and self.redis_available:
                    await self.redis.setex(cache_key, self.cache_expiry, str(elevation))
                return elevation
        except Exception as e:
            logger.error(f"Error fetching elevation: {e}")
            return None

    async def get_historical_averages(self, lat: float, lon: float) -> Dict[str, Any]:
        """Fetch historical weather averages (with Redis caching)"""
        cache_key = f"hist_avg:{round(float(lat), 3)}:{round(float(lon), 3)}"
        try:
            # Check cache
            if self.redis_available:
                cached = await self.redis.get(cache_key)
                if cached:
                    return json.loads(cached)

            # Get data for the last 10 years as a baseline
            end_date = datetime.now() - timedelta(days=365)
            start_date = end_date - timedelta(days=3650)
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                params = {
                    "latitude": lat,
                    "longitude": lon,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "daily": "temperature_2m_max,precipitation_sum",
                    "timezone": "auto"
                }
                logger.debug(f"Fetching historical data: {self.BASE_URL_HISTORICAL} with {params}")
                response = await client.get(self.BASE_URL_HISTORICAL, params=params)
                response.raise_for_status()
                data = response.json()
                
                daily = data.get("daily", {})
                temps = [t for t in daily.get("temperature_2m_max", []) if t is not None]
                precip = [p for p in daily.get("precipitation_sum", []) if p is not None]
                
                result = {
                    "avg_max_temp": sum(temps) / len(temps) if temps else 0,
                    "total_annual_precip": (sum(precip) / len(precip) * 365) if precip else 0,
                    "data_points": len(temps)
                }
                
                if self.redis_available:
                    await self.redis.setex(cache_key, self.cache_expiry, json.dumps(result))
                logger.debug(f"Historical data processed: {result}")
                return result
        except Exception as e:
            logger.error(f"Error fetching historical data: {e}")
            return {"avg_max_temp": 0, "total_annual_precip": 0, "data_points": 0}

    async def get_climate_projections(self, lat: float, lon: float, models: str = "EC_Earth3P_HR") -> Dict[str, Any]:
        """Fetch CMIP6 climate projections (with Redis caching)"""
        cache_key = f"climate_proj:{round(float(lat), 3)}:{round(float(lon), 3)}:{models}"
        try:
            # Check cache
            if self.redis_available:
                cached = await self.redis.get(cache_key)
                if cached:
                    return json.loads(cached)

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                params = {
                    "latitude": lat,
                    "longitude": lon,
                    "start_date": "2025-01-01",
                    "end_date": "2050-12-31",
                    "models": models,
                    "daily": "temperature_2m_max,precipitation_sum"
                }
                logger.debug(f"Fetching climate projections: {self.BASE_URL_CLIMATE} with {params}")
                response = await client.get(self.BASE_URL_CLIMATE, params=params)
                response.raise_for_status()
                data = response.json()
                
                daily = data.get("daily", {})
                temps = [t for t in daily.get("temperature_2m_max", []) if t is not None]
                precip = [p for p in daily.get("precipitation_sum", []) if p is not None]
                
                result = {
                    "projected_avg_temp": sum(temps) / len(temps) if temps else 0,
                    "projected_annual_precip": (sum(precip) / len(precip) * 365) if precip else 0,
                    "model_used": models
                }
                
                if self.redis_available:
                    await self.redis.setex(cache_key, self.cache_expiry, json.dumps(result))
                logger.debug(f"Climate projections processed: {result}")
                return result
        except Exception as e:
            logger.error(f"Error fetching climate projections: {e}")
            return {}

    async def get_air_quality(self, lat: float, lon: float) -> Dict[str, Any]:
        """Fetch current air quality data (with Redis caching)"""
        cache_key = f"air_quality:{round(float(lat), 3)}:{round(float(lon), 3)}"
        try:
            # Check cache
            if self.redis_available:
                cached = await self.redis.get(cache_key)
                if cached:
                    return json.loads(cached)

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                params = {
                    "latitude": lat,
                    "longitude": lon,
                    "current": "european_aqi,no2,so2,pm10,pm2_5",
                    "timezone": "auto"
                }
                logger.debug(f"Fetching air quality data: {self.BASE_URL_AIR_QUALITY} with {params}")
                response = await client.get(self.BASE_URL_AIR_QUALITY, params=params)
                response.raise_for_status()
                data = response.json()
                
                current = data.get("current", {})
                result = {
                    "aqi": current.get("european_aqi", 0),
                    "no2": current.get("no2", 0),
                    "so2": current.get("so2", 0),
                    "pm10": current.get("pm10", 0),
                    "pm2_5": current.get("pm2_5", 0)
                }
                
                if self.redis_available:
                    await self.redis.setex(cache_key, self.cache_expiry, json.dumps(result))
                logger.debug(f"Air quality data processed: {result}")
                return result
        except Exception as e:
            logger.error(f"Error fetching air quality data: {e}")
            return {"aqi": 20, "no2": 0, "so2": 0, "pm10": 0, "pm2_5": 0} # Safe clean-air default


# Singleton instance
open_meteo_provider = OpenMeteoProvider()
