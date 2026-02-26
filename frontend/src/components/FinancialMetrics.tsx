import React, { useState } from 'react';
import styled from 'styled-components';
import { FiDollarSign, FiSettings, FiTrendingUp, FiAlertCircle } from 'react-icons/fi';
import climateRiskApi from '../services/climateRiskApi';

const FinancialMetricsContainer = styled.div`
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
`;

const SectionTitle = styled.h2`
  font-size: 1.8rem;
  font-weight: 600;
  color: var(--text-light);
  margin-bottom: 1.5rem;
`;

const MetricsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
`;

const MetricCard = styled.div`
  background: linear-gradient(135deg, var(--secondary-dark) 0%, var(--primary-dark) 100%);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid var(--glass-border);
`;

const CardHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  color: var(--accent-blue);
`;

const CardTitle = styled.h3`
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-light);
`;

const MetricValue = styled.div`
  font-size: 2rem;
  font-weight: 700;
  color: var(--accent-blue);
  margin: 0.5rem 0;
`;

const MetricDescription = styled.p`
  font-size: 0.9rem;
  color: var(--text-muted);
  line-height: 1.5;
`;

const InputSection = styled.div`
  background: var(--secondary-dark);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid var(--glass-border);
  margin-bottom: 2rem;
`;

const InputGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
`;

const InputGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const Label = styled.label`
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-light);
`;

const StyledSelect = styled.select`
  background: var(--primary-dark);
  border: 1px solid var(--glass-border);
  color: var(--text-light);
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 1rem;
  width: 100%;

  &:focus {
    outline: none;
    border-color: var(--accent-blue);
  }
`;

const Input = styled.input`
  background: var(--primary-dark);
  border: 1px solid var(--glass-border);
  color: var(--text-light);
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 1rem;

  &:focus {
    outline: none;
    border-color: var(--accent-blue);
  }
`;

const CalculateButton = styled.button`
  background: linear-gradient(135deg, var(--primary-teal) 0%, var(--primary-emerald) 100%);
  color: var(--primary-dark);
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 1rem;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-glow);
  }

  &:disabled {
    opacity: 0.7;
    cursor: default;
  }
`;

function FinancialMetrics() {
  const [propertyValue, setPropertyValue] = useState('500000');
  const [propertyType, setPropertyType] = useState('residential');
  const [calculatedMetrics, setCalculatedMetrics] = useState<any>(null);
  const [assessment, setAssessment] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  React.useEffect(() => {
    const saved = localStorage.getItem('lastAssessment');
    if (saved) {
      const parsed = JSON.parse(saved);
      setAssessment(parsed);
      if (parsed.financialData) {
        setCalculatedMetrics({
          expectedAnnualLoss: parsed.financialData.expected_annual_loss,
          lossRatio: parsed.financialData.loss_ratio,
          suggestedPremium: parsed.financialData.suggested_premium,
          projections: parsed.financialData.projections,
          returnPeriods: parsed.financialData.return_periods
        });
        setPropertyValue(parsed.financialData.property_value.toString());
        setPropertyType(parsed.property_type || 'residential');
      }
    }
  }, []);

  const calculateMetrics = async () => {
    if (!assessment) {
      setError("Please select a location on the map first.");
      return;
    }

    const value = parseFloat(propertyValue) || 0;
    if (value <= 0) {
      setError("Please enter a valid property value.");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const financialData = await climateRiskApi.getFinancialLoss({
        property_value: value,
        property_type: propertyType,
        risk_assessment: {
          composite_risk_score: assessment.compositeScore,
          flood_risk_score: assessment.floodRisk,
          heat_risk_score: assessment.heatRisk,
          air_quality_risk_score: assessment.airQualityRisk,
          water_scarcity_risk_score: 0,
          infrastructure_risk_score: 0,
          risk_category: assessment.riskCategory,
          risk_drivers: assessment.risk_drivers || {},
          confidence_score: assessment.confidence,
          model_version: '1.0.0',
          calculation_timestamp: new Date().toISOString()
        } as any
      });

      setCalculatedMetrics({
        expectedAnnualLoss: financialData.expected_annual_loss,
        lossRatio: financialData.loss_ratio,
        suggestedPremium: financialData.suggested_premium,
        projections: financialData.projections,
        returnPeriods: financialData.return_periods
      });

      const updatedAssessment = {
        ...assessment,
        financialData,
        property_type: propertyType
      };
      localStorage.setItem('lastAssessment', JSON.stringify(updatedAssessment));

    } catch (err) {
      console.error("Failed to calculate metrics:", err);
      setError("Financial calculation failed. Please check connection.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <FinancialMetricsContainer>
      <SectionTitle>Financial Risk Metrics</SectionTitle>

      <InputSection>
        <CardHeader>
          <FiSettings />
          <CardTitle>Property Information</CardTitle>
        </CardHeader>

        <InputGrid>
          <InputGroup>
            <Label>Property Value ($)</Label>
            <Input
              type="number"
              value={propertyValue}
              onChange={(e) => setPropertyValue(e.target.value)}
              placeholder="Enter property value"
            />
          </InputGroup>

          <InputGroup>
            <Label>Property Type</Label>
            <StyledSelect
              value={propertyType}
              onChange={(e) => setPropertyType(e.target.value)}
            >
              <option value="residential">Residential</option>
              <option value="commercial">Commercial</option>
              <option value="industrial">Industrial</option>
            </StyledSelect>
          </InputGroup>
        </InputGrid>

        <CalculateButton onClick={calculateMetrics} disabled={isLoading}>
          {isLoading ? 'Calculating...' : 'Calculate Financial Risk'}
        </CalculateButton>

        {error && (
          <div style={{ color: 'var(--danger-red)', marginTop: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <FiAlertCircle /> {error}
          </div>
        )}
      </InputSection>

      {calculatedMetrics && (
        <MetricsGrid>
          <MetricCard>
            <CardHeader>
              <FiDollarSign />
              <CardTitle>Expected Annual Loss</CardTitle>
            </CardHeader>
            <MetricValue>${calculatedMetrics.expectedAnnualLoss.toLocaleString()}</MetricValue>
            <MetricDescription>
              Average annual loss expected from climate-related events
            </MetricDescription>
          </MetricCard>

          <MetricCard>
            <CardHeader>
              <FiTrendingUp />
              <CardTitle>Loss Ratio</CardTitle>
            </CardHeader>
            <MetricValue>{calculatedMetrics.lossRatio.toFixed(1)}%</MetricValue>
            <MetricDescription>
              Annual loss as percentage of property value
            </MetricDescription>
          </MetricCard>

          <MetricCard>
            <CardHeader>
              <FiDollarSign />
              <CardTitle>Suggested Premium</CardTitle>
            </CardHeader>
            <MetricValue>${calculatedMetrics.suggestedPremium.toLocaleString()}</MetricValue>
            <MetricDescription>
              Recommended annual insurance premium
            </MetricDescription>
          </MetricCard>

          <MetricCard>
            <CardHeader>
              <FiTrendingUp />
              <CardTitle>5-Year Projection</CardTitle>
            </CardHeader>
            <MetricValue>${(calculatedMetrics.projections[5]?.cumulative_loss || 0).toLocaleString()}</MetricValue>
            <MetricDescription>
              Cumulative expected loss over 5 years
            </MetricDescription>
          </MetricCard>

          <MetricCard>
            <CardHeader>
              <FiTrendingUp />
              <CardTitle>10-Year Projection</CardTitle>
            </CardHeader>
            <MetricValue>${(calculatedMetrics.projections[10]?.cumulative_loss || 0).toLocaleString()}</MetricValue>
            <MetricDescription>
              Cumulative expected loss over 10 years
            </MetricDescription>
          </MetricCard>
        </MetricsGrid>
      )}
    </FinancialMetricsContainer>
  );
}

export default FinancialMetrics;