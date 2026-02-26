import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from geopy.distance import geodesic
import logging

from app.core.config import settings
from app.schemas.api import RiskScoreRequest, RiskScoreResponse
from app.services.data_providers.open_meteo import open_meteo_provider

logger = logging.getLogger(__name__)

class ClimateRiskService:
    """Core climate risk calculation service"""
    
    def __init__(self):
        self.model_version = settings.MODEL_VERSION
        self.confidence_threshold = settings.CONFIDENCE_THRESHOLD
        
    async def calculate_risk_score(self, request: RiskScoreRequest) -> RiskScoreResponse:
        """
        Calculate comprehensive climate risk score for a location using real-world data
        """
        try:
            # Fetch real data from Open-Meteo
            elevation = await open_meteo_provider.get_elevation(request.latitude, request.longitude)
            if elevation is None: elevation = 50.0 # Default fallback
            
            historical = await open_meteo_provider.get_historical_averages(request.latitude, request.longitude)
            projections = await open_meteo_provider.get_climate_projections(request.latitude, request.longitude)
            air_quality_data = await open_meteo_provider.get_air_quality(request.latitude, request.longitude)
            
            # Determine urban density dynamically using NO2 as a proxy
            # NO2 > 20 is typically urban combustion.
            no2_val = air_quality_data.get("no2", 0)
            if no2_val > 40: urban_density = 0.9      # Major City
            elif no2_val > 20: urban_density = 0.65   # Urban/Suburban
            elif no2_val > 10: urban_density = 0.4    # Developing/Rural
            else: urban_density = 0.15                # Remote/Pristine
            
            historical_floods = 1 # Baseline risk
            
            # Calculate individual risk components based on REAL data + USER SCENARIO inputs
            # Model Delta = (Future Projection - Historical Baseline)
            model_precip_delta = projections.get("projected_annual_precip", 0) - historical.get("total_annual_precip", 0)
            model_temp_delta = projections.get("projected_avg_temp", 0) - historical.get("avg_max_temp", 0)
            
            # Combine Model Delta with User Input Scenario (e.g. "What if it rains 20% more than the model predicts?")
            final_precip_change = model_precip_delta + (request.precipitation_change or 0)
            final_temp_increase = model_temp_delta + (request.temperature_increase or 0)

            # Determine coastal proximity (Simplified proximity to Lat/Lon bounds for major oceans)
            # In production, this would use a spatial distance-to-coast API
            is_coastal = self._check_coastal_proximity(request.latitude, request.longitude)
            
            flood_risk = self._calculate_flood_risk(
                elevation=elevation,
                drainage_distance=1500.0,
                historical_floods=historical_floods,
                precipitation_change=final_precip_change,
                historical_baseline_precip=historical.get("total_annual_precip", 800.0),
                is_coastal=is_coastal
            )
            
            heat_risk = await self._calculate_heat_risk(
                latitude=request.latitude,
                longitude=request.longitude,
                temperature_increase=final_temp_increase,
                urban_density=urban_density
            )
            
            air_quality_risk = self._calculate_air_quality_risk(
                aqi_value=air_quality_data.get("aqi", 20),
                urban_density=urban_density,
                is_remote=(urban_density < 0.3)
            )
            
            water_scarcity_risk = self._calculate_water_scarcity_risk(
                latitude=request.latitude,
                longitude=request.longitude,
                precipitation_change=final_precip_change,
                historical_baseline_precip=historical.get("total_annual_precip", 800.0)
            )
            
            infrastructure_risk = self._calculate_infrastructure_risk(
                urban_density=urban_density,
                age_factor=request.infrastructure_age_factor or 1.0
            )
            
            # Calculate composite risk score
            composite_score = self._calculate_composite_risk(
                flood_risk=flood_risk,
                heat_risk=heat_risk,
                air_quality_risk=air_quality_risk,
                water_scarcity_risk=water_scarcity_risk,
                infrastructure_risk=infrastructure_risk
            )
            
            risk_drivers = self._calculate_risk_drivers(
                flood_risk=flood_risk,
                heat_risk=heat_risk,
                air_quality_risk=air_quality_risk,
                water_scarcity_risk=water_scarcity_risk,
                infrastructure_risk=infrastructure_risk,
                composite_score=composite_score
            )
            
            risk_category = self._determine_risk_category(composite_score)
            
            confidence_score = self._calculate_confidence_score(
                data_completeness=self._assess_data_completeness(request),
                model_reliability=historical.get("data_points", 0) / 3650.0 # Proportional to baseline data length
            )
            
            return RiskScoreResponse(
                composite_risk_score=composite_score,
                flood_risk_score=flood_risk,
                heat_risk_score=heat_risk,
                air_quality_risk_score=air_quality_risk,
                water_scarcity_risk_score=water_scarcity_risk,
                infrastructure_risk_score=infrastructure_risk,
                risk_category=risk_category,
                risk_drivers=risk_drivers,
                confidence_score=confidence_score,
                model_version=f"{self.model_version}-om", # Open-Meteo integrated
                calculation_timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error calculating risk score: {str(e)}")
            raise
    
    def _calculate_flood_risk(self, elevation: float, drainage_distance: float, 
                            historical_floods: int, precipitation_change: float,
                            historical_baseline_precip: float, is_coastal: bool) -> float:
        """Calculate flood risk score (0-100)"""
        # Desert Gate: If historical rainfall < 200mm, flood risk is near-zero 
        # unless it's a massive anomaly (>50% increase)
        if historical_baseline_precip < 200 and precipitation_change < 50:
            return 5.0 # Baseline residual risk
            
        # Base risk factors
        elevation_risk = max(0, (15 - elevation) / 15 * 100)  # Lower elevation = higher risk
        historical_risk = min(100, historical_floods * 25)
        
        # Precip risk scales with the baseline (ratio-based)
        precip_intensity = (precipitation_change / max(1, historical_baseline_precip)) * 500
        precip_risk = min(100, max(0, precip_intensity))
        
        # Coastal surge factor
        coastal_factor = 30 if (is_coastal and elevation < 5) else 0
        
        # Weighted combination
        flood_score = (
            elevation_risk * 0.35 +
            historical_risk * 0.20 +
            precip_risk * 0.30 +
            coastal_factor * 0.15
        )
        
        return min(100, flood_score)
    
    async def _calculate_heat_risk(self, latitude: float, longitude: float, 
                           temperature_increase: float, urban_density: float) -> float:
        """Calculate heat risk score (0-100)"""
        # Base temperature risk: Exponentially higher in tropics
        # lat 0 (Equator) -> 90 risk, lat 30 (Dubai) -> 75 risk, lat 50 (London) -> 30 risk
        lat_factor = abs(latitude)
        base_temp_risk = max(0, 90 - (lat_factor * 1.2))
        
        # Urban heat island effect (highly significant for commercial centers)
        urban_heat_effect = urban_density * 60
        
        # Climate change amplification (Open-Meteo model delta)
        climate_amplification = temperature_increase * 20
        
        heat_score = min(100, (base_temp_risk * 0.4) + (urban_heat_effect * 0.3) + (climate_amplification * 0.3))
        return heat_score
    
    def _calculate_air_quality_risk(self, aqi_value: float, urban_density: float, is_remote: bool = False) -> float:
        """Calculate air quality risk score (0-100)"""
        # Remote Region Discount: If remote (low urban density), 
        # high AQI is likely natural (sea salt/dust), not anthropogenic smog.
        effective_aqi = aqi_value
        if is_remote and aqi_value > 40:
            effective_aqi = 30 + (aqi_value - 40) * 0.3 # Dampen the tail
            
        # Normalize to 0-100 risk score
        aqi_risk = min(100, (effective_aqi / 80) * 100)
        
        # Combine with urbanization as a secondary factor
        final_aq_score = (aqi_risk * 0.8) + (urban_density * 20)
        return min(100, final_aq_score)
    
    def _calculate_water_scarcity_risk(self, latitude: float, longitude: float, 
                                     precipitation_change: float,
                                     historical_baseline_precip: float) -> float:
        """Calculate water scarcity risk score (0-100)"""
        # Aridity Scaling: Lower baseline precipitation increases base vulnerability
        # < 400mm = Arid/Semi-Arid transition
        base_vulnerability = max(0, (500 - historical_baseline_precip) / 5) 
        
        # Sensitivity to decrease
        scarcity_risk = max(0, -precipitation_change * 3)
        
        return min(100, base_vulnerability + scarcity_risk)
    
    def _calculate_infrastructure_risk(self, urban_density: float, age_factor: float) -> float:
        """Calculate infrastructure vulnerability score (0-100)"""
        # Older infrastructure in dense areas is more vulnerable
        infrastructure_score = min(100, urban_density * 50 + age_factor * 30 + 20)
        return infrastructure_score
    
    def _calculate_composite_risk(self, flood_risk: float, heat_risk: float,
                                air_quality_risk: float, water_scarcity_risk: float,
                                infrastructure_risk: float) -> float:
        """Calculate weighted composite risk score"""
        composite_score = (
            flood_risk * 0.3 +
            heat_risk * 0.25 +
            air_quality_risk * 0.2 +
            water_scarcity_risk * 0.15 +
            infrastructure_risk * 0.1
        )
        return composite_score
    
    def _calculate_risk_drivers(self, flood_risk: float, heat_risk: float,
                              air_quality_risk: float, water_scarcity_risk: float,
                              infrastructure_risk: float, composite_score: float) -> Dict[str, float]:
        """Calculate percentage contribution of each risk driver"""
        if composite_score == 0:
            return {
                "flood": 0,
                "heat": 0,
                "air_quality": 0,
                "water_scarcity": 0,
                "infrastructure": 0
            }
        
        total_weighted = (
            flood_risk * 0.3 +
            heat_risk * 0.25 +
            air_quality_risk * 0.2 +
            water_scarcity_risk * 0.15 +
            infrastructure_risk * 0.1
        )
        
        return {
            "flood": round((flood_risk * 0.3 / total_weighted) * 100, 1),
            "heat": round((heat_risk * 0.25 / total_weighted) * 100, 1),
            "air_quality": round((air_quality_risk * 0.2 / total_weighted) * 100, 1),
            "water_scarcity": round((water_scarcity_risk * 0.15 / total_weighted) * 100, 1),
            "infrastructure": round((infrastructure_risk * 0.1 / total_weighted) * 100, 1)
        }
    
    def _determine_risk_category(self, composite_score: float) -> str:
        """Determine risk category based on composite score"""
        if composite_score < 25:
            return "Low"
        elif composite_score < 50:
            return "Moderate"
        elif composite_score < 75:
            return "High"
        else:
            return "Severe"
    
    def _calculate_confidence_score(self, data_completeness: float, model_reliability: float) -> float:
        """Calculate overall confidence score (0-100)"""
        return (data_completeness * 0.6 + model_reliability * 0.4)

    def _check_coastal_proximity(self, lat: float, lon: float) -> bool:
        """Generalized heuristic for coastal proximity (Global Major Coastlines & Islands)"""
        # We use a broad range of coordinate boxes for global oceans
        # In a full system, this would be a true GeoJSON intersection or distance API
        
        is_near_water = False
        
        # Indian Ocean & Archipelagos (Andaman, etc)
        if (5 <= lat <= 25) and (65 <= lon <= 100): is_near_water = True
        # Pacific Rim (East Asia, Japan)
        elif (0 <= lat <= 45) and (120 <= lon <= 150): is_near_water = True
        # Atlantic (US East Coast, Europe West Coast)
        elif (30 <= lat <= 60) and (-80 <= lon <= -10): is_near_water = True
        # Mediterranean
        elif (30 <= lat <= 45) and (-5 <= lon <= 35): is_near_water = True
        # Gulf / Middle East
        elif (20 <= lat <= 30) and (45 <= lon <= 65): is_near_water = True
        
        return is_near_water
    
    def _assess_data_completeness(self, request: RiskScoreRequest) -> float:
        """Assess completeness of input data (0-1)"""
        count = 0
        if request.latitude is not None: count += 1
        if request.longitude is not None: count += 1
        if request.precipitation_change is not None: count += 1
        if request.temperature_increase is not None: count += 1
        return count / 4.0

# Singleton instance
climate_risk_service = ClimateRiskService()