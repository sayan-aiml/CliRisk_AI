from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=False)
    
    # Risk scores (0-100)
    composite_risk_score = Column(Float, nullable=False)
    flood_risk_score = Column(Float)
    heat_risk_score = Column(Float)
    air_quality_risk_score = Column(Float)
    water_scarcity_risk_score = Column(Float)
    infrastructure_risk_score = Column(Float)
    
    # Risk categories
    risk_category = Column(String)  # Low, Moderate, High, Severe
    risk_percentile = Column(Float)  # vs city/region
    
    # Financial metrics
    expected_annual_loss = Column(Float)
    property_value = Column(Float)
    loss_ratio = Column(Float)
    suggested_premium = Column(Float)
    
    # Risk drivers breakdown (% contribution)
    risk_drivers = Column(JSON)  # {rainfall: 30, drainage: 25, elevation: 20, ...}
    
    # Model confidence
    confidence_score = Column(Float)
    model_version = Column(String)
    
    # Additional metadata
    assessment_notes = Column(Text)
    raw_data = Column(JSON)  # Store detailed calculation data
    
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    property = relationship("Property", back_populates="risk_assessments")
    scenario = relationship("Scenario", back_populates="risk_assessments")
    
    def __repr__(self):
        return f"<RiskAssessment(id={self.id}, property_id={self.property_id}, score={self.composite_risk_score})>"