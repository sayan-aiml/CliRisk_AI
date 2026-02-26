import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
import logging

from app.schemas.api import FinancialLossRequest, FinancialLossResponse

logger = logging.getLogger(__name__)

class FinancialRiskService:
    """Financial risk calculation service"""
    
    def __init__(self):
        self.loss_curve_exponent = 1.5  # Shape parameter for loss curve
        self.discount_rate = 0.03  # 3% discount rate for present value calculations
        
    def calculate_financial_loss(self, request: FinancialLossRequest) -> FinancialLossResponse:
        """
        Calculate financial risk metrics for property
        """
        try:
            # Get risk assessment
            risk_score = request.risk_assessment
            
            # Calculate expected annual loss (EAL)
            eal = self._calculate_expected_annual_loss(
                property_value=request.property_value,
                composite_risk_score=risk_score.composite_risk_score,
                confidence_score=risk_score.confidence_score
            )
            
            # Calculate loss ratios
            loss_ratio = self._calculate_loss_ratio(eal, request.property_value)
            
            # Calculate premium suggestions
            suggested_premium = self._calculate_suggested_premium(
                eal=eal,
                risk_category=risk_score.risk_category,
                property_type=request.property_type
            )
            
            # Calculate multi-year projections
            projections = self._calculate_projections(
                eal=eal,
                property_value=request.property_value,
                years=[1, 5, 10, 20]
            )
            
            # Calculate return periods
            return_periods = self._calculate_return_periods(eal)
            
            # Calculate stress test scenarios
            stress_tests = self._calculate_stress_tests(
                base_eal=eal,
                risk_score=risk_score
            )
            
            # Calculate probability of exceeding thresholds
            threshold_probabilities = self._calculate_threshold_probabilities(
                eal=eal,
                thresholds=[5000, 10000, 25000, 50000]
            )
            
            return FinancialLossResponse(
                property_value=request.property_value,
                expected_annual_loss=eal,
                loss_ratio=loss_ratio,
                suggested_premium=suggested_premium,
                projections=projections,
                return_periods=return_periods,
                stress_tests=stress_tests,
                threshold_probabilities=threshold_probabilities,
                calculation_timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error calculating financial loss: {str(e)}")
            raise
    
    def _calculate_expected_annual_loss(self, property_value: float, 
                                      composite_risk_score: float,
                                      confidence_score: float) -> float:
        """Calculate Expected Annual Loss (EAL)"""
        # Base loss rate based on risk score
        base_loss_rate = (composite_risk_score / 100) * 0.03  # 0-3% of property value
        
        # Adjust for confidence
        confidence_multiplier = 0.5 + (confidence_score / 100) * 0.5  # 0.5-1.0
        
        # Calculate EAL
        eal = property_value * base_loss_rate * confidence_multiplier
        return max(0, eal)
    
    def _calculate_loss_ratio(self, eal: float, property_value: float) -> float:
        """Calculate loss ratio (EAL / Property Value)"""
        if property_value <= 0:
            return 0
        return (eal / property_value) * 100
    
    def _calculate_suggested_premium(self, eal: float, risk_category: str, 
                                   property_type: str) -> float:
        """Calculate suggested insurance premium"""
        # Base premium = EAL + loading
        loading_factor = self._get_loading_factor(risk_category, property_type)
        premium = eal * (1 + loading_factor)
        
        # Add minimum premium
        minimum_premium = 250  # $250 minimum
        return max(minimum_premium, premium)
    
    def _get_loading_factor(self, risk_category: str, property_type: str) -> float:
        """Get loading factor based on risk category and property type"""
        # Base loading by risk category
        category_loading = {
            "Low": 0.2,
            "Moderate": 0.4,
            "High": 0.7,
            "Severe": 1.2
        }
        
        # Property type adjustment
        type_adjustment = {
            "residential": 0.0,
            "commercial": 0.3,
            "industrial": 0.5
        }
        
        base_loading = category_loading.get(risk_category, 0.4)
        type_adj = type_adjustment.get(property_type, 0.0)
        
        return base_loading + type_adj
    
    def _calculate_projections(self, eal: float, property_value: float, 
                             years: List[int]) -> Dict[int, Dict[str, float]]:
        """Calculate loss projections over multiple years"""
        projections = {}
        
        for year in years:
            # Compound annual growth (assuming risk increases over time)
            growth_factor = (1 + 0.02) ** year  # 2% annual increase
            projected_eal = eal * growth_factor
            
            # Calculate cumulative loss
            cumulative_loss = projected_eal * year
            
            # Calculate present value of cumulative loss
            present_value = self._calculate_present_value(cumulative_loss, year)
            
            projections[year] = {
                "annual_loss": projected_eal,
                "cumulative_loss": cumulative_loss,
                "present_value": present_value,
                "loss_ratio": (projected_eal / property_value) * 100
            }
        
        return projections
    
    def _calculate_present_value(self, future_value: float, years: int) -> float:
        """Calculate present value of future loss"""
        return future_value / ((1 + self.discount_rate) ** years)
    
    def _calculate_return_periods(self, eal: float) -> Dict[str, float]:
        """Calculate return periods for different loss events"""
        # Return periods based on EAL (assuming exponential distribution)
        return_periods = {}
        
        # Common return periods in insurance
        events = {
            "1_in_10": 0.1,    # 10% annual probability
            "1_in_25": 0.04,   # 4% annual probability
            "1_in_50": 0.02,   # 2% annual probability
            "1_in_100": 0.01,  # 1% annual probability
            "1_in_250": 0.004, # 0.4% annual probability
            "1_in_500": 0.002  # 0.2% annual probability
        }
        
        for event_name, probability in events.items():
            # Loss amount for given return period
            loss_amount = eal / probability
            return_periods[event_name] = loss_amount
        
        return return_periods
    
    def _calculate_stress_tests(self, base_eal: float, 
                              risk_score) -> Dict[str, Dict[str, float]]:
        """Calculate stress test scenarios"""
        stress_tests = {}
        
        # Scenario multipliers
        scenarios = {
            "Moderate_Climate_Change": 1.2,
            "Severe_Climate_Change": 1.8,
            "Economic_Downturn": 0.8,
            "Regulatory_Changes": 1.3
        }
        
        for scenario_name, multiplier in scenarios.items():
            stressed_eal = base_eal * multiplier
            stress_tests[scenario_name] = {
                "expected_annual_loss": stressed_eal,
                "change_percentage": (multiplier - 1) * 100,
                "severity": "High" if multiplier > 1.5 else "Medium" if multiplier > 1.0 else "Low"
            }
        
        return stress_tests
    
    def _calculate_threshold_probabilities(self, eal: float, 
                                         thresholds: List[float]) -> Dict[float, float]:
        """Calculate probability of exceeding loss thresholds"""
        probabilities = {}
        
        # Assuming log-normal distribution for losses
        # Probability = P(X > T) where X is the loss and T is the threshold
        for threshold in thresholds:
            if eal <= 0:
                probabilities[threshold] = 0.0
            else:
                # Simplified but more realistic probability calculation
                # Higher EAL means higher probability of exceeding any threshold
                # Using a basic sigmoid-like approach for MVP
                val = (eal / threshold) * 0.5
                probability = min(0.99, max(0.01, val / (1 + val)))
                probabilities[threshold] = round(probability, 4)
        
        return probabilities

# Singleton instance
financial_risk_service = FinancialRiskService()