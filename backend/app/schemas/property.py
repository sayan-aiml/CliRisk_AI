from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PropertyBase(BaseModel):
    address: str
    city: str
    state: str
    zip_code: Optional[str] = None
    country: str = "US"
    latitude: float
    longitude: float
    property_value: float
    property_type: str
    year_built: Optional[int] = None
    square_footage: Optional[float] = None
    number_of_units: Optional[int] = None

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(BaseModel):
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    property_value: Optional[float] = None
    property_type: Optional[str] = None
    year_built: Optional[int] = None
    square_footage: Optional[float] = None
    number_of_units: Optional[int] = None

class PropertyInDB(PropertyBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Property(PropertyInDB):
    pass