from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from app.core.database import Base

class Property(Base):
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String)
    country = Column(String, default="US")
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    property_value = Column(Float, nullable=False)
    property_type = Column(String)  # residential, commercial, industrial
    year_built = Column(Integer)
    square_footage = Column(Float)
    number_of_units = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="properties")
    risk_assessments = relationship("RiskAssessment", back_populates="property")
    portfolio = relationship("Portfolio", back_populates="properties")
    
    def __repr__(self):
        return f"<Property(id={self.id}, address={self.address})>"