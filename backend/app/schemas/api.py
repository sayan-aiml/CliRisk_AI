from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

class PropertyType(str, Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"

# Risk Score Calculation
class RiskScoreRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    temperature_increase: float = Field(0.0, ge=0, le=10, description="Temperature increase in °C")
    precipitation_change: float = Field(0.0, ge=-50, le=50, description="Precipitation change in %")
    infrastructure_age_factor: Optional[float] = Field(1.0, ge=0.1, le=3.0)

class RiskScoreResponse(BaseModel):
    composite_risk_score: float = Field(..., ge=0, le=100)
    flood_risk_score: float = Field(..., ge=0, le=100)
    heat_risk_score: float = Field(..., ge=0, le=100)
    air_quality_risk_score: float = Field(..., ge=0, le=100)
    water_scarcity_risk_score: float = Field(..., ge=0, le=100)
    infrastructure_risk_score: float = Field(..., ge=0, le=100)
    risk_category: str = Field(..., pattern="^(Low|Moderate|High|Severe)$")
    risk_drivers: Dict[str, float]  # percentage breakdown
    confidence_score: float = Field(..., ge=0, le=100)
    model_version: str
    calculation_timestamp: datetime

# Financial Loss Calculation
class FinancialLossRequest(BaseModel):
    property_value: float = Field(..., gt=0)
    property_type: PropertyType = PropertyType.RESIDENTIAL
    risk_assessment: RiskScoreResponse

class ProjectionData(BaseModel):
    annual_loss: float
    cumulative_loss: float
    present_value: float
    loss_ratio: float

class StressTestResult(BaseModel):
    expected_annual_loss: float
    change_percentage: float
    severity: str

class FinancialLossResponse(BaseModel):
    property_value: float
    expected_annual_loss: float
    loss_ratio: float
    suggested_premium: float
    projections: Dict[int, ProjectionData]
    return_periods: Dict[str, float]
    stress_tests: Dict[str, StressTestResult]
    threshold_probabilities: Dict[float, float]
    calculation_timestamp: datetime

# Multi-Hazard Assessment
class MultiHazardRequest(BaseModel):
    latitude: float
    longitude: float
    property_value: float
    property_type: PropertyType = PropertyType.RESIDENTIAL
    scenarios: List[str] = ["Current Climate", "2050 Projection"]

class HazardDetail(BaseModel):
    hazard_type: str
    risk_score: float
    financial_impact: float
    probability: float
    description: str

class MultiHazardResponse(BaseModel):
    location: Dict[str, float]  # lat, lon
    property_value: float
    total_risk_score: float
    hazard_breakdown: List[HazardDetail]
    overall_risk_category: str
    recommendations: List[str]
    calculation_timestamp: datetime

# Scenario Simulation
class ScenarioSimulationRequest(BaseModel):
    latitude: float
    longitude: float
    property_value: float
    property_type: PropertyType = PropertyType.RESIDENTIAL
    scenario_ids: List[int] = Field(default_factory=lambda: [1, 2, 3])  # Current, 2035, 2050

class ScenarioResult(BaseModel):
    scenario_name: str
    composite_risk_score: float
    expected_annual_loss: float
    suggested_premium: float
    risk_category: str
    confidence_score: float

class ScenarioSimulationResponse(BaseModel):
    location: Dict[str, float]
    property_value: float
    scenario_results: List[ScenarioResult]
    comparison: Dict[str, float]  # percentage changes between scenarios
    calculation_timestamp: datetime