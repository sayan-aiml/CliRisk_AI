from pydantic_settings import BaseSettings
from typing import List, Optional
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "ClimateRisk AI"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ENVIRONMENT: str = "development"
    
    # Server settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:8000",
    ]
    
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # Database settings
    DATABASE_URL: str = "postgresql://climaterisk:climaterisk123@localhost:5432/climaterisk"
    
    # Redis settings
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_CACHE_EXPIRE: int = 3600  # 1 hour
    
    # Authentication settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    JWT_ALGORITHM: str = "HS256"
    
    # API settings
    API_RATE_LIMIT: str = "100/minute"
    
    # Geospatial settings
    MAPBOX_ACCESS_TOKEN: Optional[str] = None
    DEFAULT_LOCATION: List[float] = [40.7128, -74.0060]  # NYC
    DEFAULT_ZOOM: int = 12
    
    # Climate data settings
    CLIMATE_DATA_DIR: str = "/app/data/climate"
    GEOSPATIAL_DATA_DIR: str = "/app/data/geospatial"
    
    # Model settings
    MODEL_VERSION: str = "1.0.0"
    CONFIDENCE_THRESHOLD: float = 0.7
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()