import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "ClimateRisk AI API"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "ClimateRisk AI API"

def test_risk_score_calculation():
    test_data = {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "temperature_increase": 2.5,
        "precipitation_change": 15.0
    }
    
    response = client.post("/api/v1/climate-risk/risk-score", json=test_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "composite_risk_score" in data
    assert "flood_risk_score" in data
    assert "risk_category" in data
    assert data["composite_risk_score"] >= 0
    assert data["composite_risk_score"] <= 100

def test_financial_loss_calculation():
    test_data = {
        "property_value": 500000,
        "property_type": "residential",
        "latitude": 40.7128,
        "longitude": -74.0060
    }
    
    response = client.post("/api/v1/climate-risk/financial-loss", json=test_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "expected_annual_loss" in data
    assert "suggested_premium" in data
    assert "loss_ratio" in data
    assert data["property_value"] == 500000

def test_invalid_coordinates():
    test_data = {
        "latitude": 100,  # Invalid latitude
        "longitude": -74.0060,
        "temperature_increase": 2.5,
        "precipitation_change": 15.0
    }
    
    response = client.post("/api/v1/climate-risk/risk-score", json=test_data)
    assert response.status_code == 422  # Validation error

if __name__ == "__main__":
    pytest.main([__file__])