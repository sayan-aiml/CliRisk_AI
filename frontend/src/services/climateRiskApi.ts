import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

export interface RiskScoreRequest {
    latitude: number;
    longitude: number;
    temperature_increase?: number;
    precipitation_change?: number;
    infrastructure_age_factor?: number;
}

export interface RiskScoreResponse {
    composite_risk_score: number;
    flood_risk_score: number;
    heat_risk_score: number;
    air_quality_risk_score: number;
    water_scarcity_risk_score: number;
    infrastructure_risk_score: number;
    risk_category: string;
    risk_drivers: Record<string, number>;
    confidence_score: number;
    model_version: string;
    calculation_timestamp: string;
}

export interface FinancialLossRequest {
    property_value: number;
    property_type: string;
    risk_assessment: RiskScoreResponse;
}

export interface FinancialLossResponse {
    property_value: number;
    expected_annual_loss: number;
    loss_ratio: number;
    suggested_premium: number;
    projections: Record<number, any>;
    return_periods: Record<string, number>;
    stress_tests: Record<string, any>;
    threshold_probabilities: Record<string, number>;
    calculation_timestamp: string;
}

const climateRiskApi = {
    getRiskScore: async (request: RiskScoreRequest): Promise<RiskScoreResponse> => {
        const response = await axios.post(`${API_URL}/climate-risk/risk-score`, request);
        return response.data;
    },

    getFinancialLoss: async (request: FinancialLossRequest): Promise<FinancialLossResponse> => {
        const response = await axios.post(`${API_URL}/climate-risk/financial-loss`, request);
        return response.data;
    },

    getDashboardStats: async () => {
        const response = await axios.get(`${API_URL}/climate-risk/dashboard-stats`);
        return response.data;
    },
};

export default climateRiskApi;
