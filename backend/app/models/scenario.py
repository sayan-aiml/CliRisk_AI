from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Scenario(Base):
    __tablename__ = "scenarios"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    is_public = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    
    # Climate parameters
    temperature_increase = Column(Float, default=0.0)  # degrees Celsius
    precipitation_change = Column(Float, default=0.0)  # percentage change
    sea_level_rise = Column(Float, default=0.0)  # meters
    timeframe_years = Column(Integer)  # projection year (e.g., 2035, 2050)
    
    # Custom parameters
    custom_parameters = Column(JSON)  # additional scenario parameters
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    risk_assessments = relationship("RiskAssessment", back_populates="scenario")
    
    def __repr__(self):
        return f"<Scenario(id={self.id}, name={self.name})>"

# Predefined scenarios
PREDEFINED_SCENARIOS = [
    {
        "name": "Current Climate",
        "description": "Baseline risk assessment using current climate conditions",
        "temperature_increase": 0.0,
        "precipitation_change": 0.0,
        "sea_level_rise": 0.0,
        "timeframe_years": 2024
    },
    {
        "name": "2035 Projection",
        "description": "Climate projection for 2035 under moderate emissions scenario",
        "temperature_increase": 1.2,
        "precipitation_change": 8.0,
        "sea_level_rise": 0.15,
        "timeframe_years": 2035
    },
    {
        "name": "2050 Projection",
        "description": "Climate projection for 2050 under high emissions scenario",
        "temperature_increase": 2.5,
        "precipitation_change": 15.0,
        "sea_level_rise": 0.35,
        "timeframe_years": 2050
    },
    {
        "name": "Extreme Climate",
        "description": "Worst-case climate scenario with maximum projected changes",
        "temperature_increase": 4.0,
        "precipitation_change": 25.0,
        "sea_level_rise": 0.8,
        "timeframe_years": 2080
    }
]