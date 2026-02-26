from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime

class RiskAssessmentBase(BaseModel):
    property_id: int
    scenario_id: int
    composite_risk_score: float
    flood_risk_score: Optional[float] = None
    heat_risk_score: Optional[float] = None
    air_quality_risk_score: Optional[float] = None
    water_scarcity_risk_score: Optional[float] = None
    infrastructure_risk_score: Optional[float] = None
    risk_category: str
    risk_percentile: Optional[float] = None
    expected_annual_loss: Optional[float] = None
    property_value: Optional[float] = None
    loss_ratio: Optional[float] = None
    suggested_premium: Optional[float] = None
    risk_drivers: Optional[Dict] = None
    confidence_score: Optional[float] = None
    model_version: Optional[str] = None
    assessment_notes: Optional[str] = None
    raw_data: Optional[Dict] = None

class RiskAssessmentCreate(RiskAssessmentBase):
    pass

class RiskAssessmentUpdate(BaseModel):
    composite_risk_score: Optional[float] = None
    flood_risk_score: Optional[float] = None
    heat_risk_score: Optional[float] = None
    air_quality_risk_score: Optional[float] = None
    water_scarcity_risk_score: Optional[float] = None
    infrastructure_risk_score: Optional[float] = None
    risk_category: Optional[str] = None
    risk_percentile: Optional[float] = None
    expected_annual_loss: Optional[float] = None
    property_value: Optional[float] = None
    loss_ratio: Optional[float] = None
    suggested_premium: Optional[float] = None
    risk_drivers: Optional[Dict] = None
    confidence_score: Optional[float] = None
    model_version: Optional[str] = None
    assessment_notes: Optional[str] = None
    raw_data: Optional[Dict] = None

class RiskAssessmentInDB(RiskAssessmentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class RiskAssessment(RiskAssessmentInDB):
    pass