from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime

class ScenarioBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = True
    is_active: bool = True
    temperature_increase: float = 0.0
    precipitation_change: float = 0.0
    sea_level_rise: float = 0.0
    timeframe_years: Optional[int] = None
    custom_parameters: Optional[Dict] = None

class ScenarioCreate(ScenarioBase):
    pass

class ScenarioUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
    is_active: Optional[bool] = None
    temperature_increase: Optional[float] = None
    precipitation_change: Optional[float] = None
    sea_level_rise: Optional[float] = None
    timeframe_years: Optional[int] = None
    custom_parameters: Optional[Dict] = None

class ScenarioInDB(ScenarioBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Scenario(ScenarioInDB):
    pass