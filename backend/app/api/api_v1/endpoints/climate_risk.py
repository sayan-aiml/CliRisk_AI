from fastapi import APIRouter, Depends, HTTPException
import logging

from app.schemas.api import (
    RiskScoreRequest, RiskScoreResponse,
    FinancialLossRequest, FinancialLossResponse
)
from app.services.climate_risk_service import climate_risk_service
from app.services.financial_risk_service import financial_risk_service

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post('/risk-score', response_model=RiskScoreResponse)
async def calculate_risk_score(request: RiskScoreRequest):
    try:
        result = await climate_risk_service.calculate_risk_score(request)
        logger.info(f'Risk score calculated for location ({request.latitude}, {request.longitude})')
        return result
    except Exception as e:
        logger.error(f'Error calculating risk score: {str(e)}')
        raise HTTPException(status_code=500, detail=f'Risk calculation failed: {str(e)}')

@router.post('/financial-loss', response_model=FinancialLossResponse)
async def calculate_financial_loss(request: FinancialLossRequest):
    try:
        result = financial_risk_service.calculate_financial_loss(request)
        logger.info(f'Financial loss calculated for property value ${request.property_value}')
        return result
    except Exception as e:
        logger.error(f'Error calculating financial loss: {str(e)}')
        raise HTTPException(status_code=500, detail=f'Financial calculation failed: {str(e)}')

@router.get('/dashboard-stats')
async def get_dashboard_stats():
    # Match frontend keys in Dashboard.tsx
    return {
        "total_properties": 1284,
        "avg_risk_score": 64.5,
        "total_exposure": 52500000,
        "active_scenarios": 8,
        "risk_distribution": [
            {"level": "low", "title": "Low Risk", "percentage": 23},
            {"level": "moderate", "title": "Moderate Risk", "percentage": 35},
            {"level": "high", "title": "High Risk", "percentage": 28},
            {"level": "severe", "title": "Severe Risk", "percentage": 14}
        ]
    }

@router.get('/health')
async def health_check():
    return {
        'status': 'healthy',
        'service': 'ClimateRisk AI - Climate Risk Engine',
        'version': '1.0.0'
    }