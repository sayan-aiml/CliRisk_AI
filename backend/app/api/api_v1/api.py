from fastapi import APIRouter

from app.api.api_v1.endpoints import climate_risk, auth

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(climate_risk.router, prefix="/climate-risk", tags=["climate-risk"])
