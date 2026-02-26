import React, { useState } from 'react';
import styled from 'styled-components';
import { FiLayers, FiTrendingUp, FiBarChart2 } from 'react-icons/fi';
import climateRiskApi from '../services/climateRiskApi';

const ScenarioComparisonContainer = styled.div`
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

const ScenarioSelector = styled.div`
  background: var(--secondary-dark);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid var(--glass-border);
  margin-bottom: 2rem;
`;

const SelectorHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  color: var(--accent-blue);
`;

const SelectorTitle = styled.h3`
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-light);
`;

const ScenarioGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
`;

const ScenarioOption = styled.div<{ selected: boolean }>`
  background: ${props => props.selected ? 'var(--primary-teal)' : 'var(--primary-dark)'};
  border: 2px solid ${props => props.selected ? 'var(--accent-blue)' : 'var(--glass-border)'};
  border-radius: 8px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  
  &:hover {
    border-color: var(--accent-blue);
    transform: translateY(-2px);
  }
`;

const ScenarioName = styled.div`
  font-weight: 600;
  color: var(--text-light);
  margin-bottom: 0.5rem;
`;

const ScenarioDescription = styled.div`
  font-size: 0.8rem;
  color: var(--text-muted);
`;

const ComparisonGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
`;

const ComparisonCard = styled.div`
  background: var(--secondary-dark);
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

const MetricRow = styled.div`
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--glass-border);
  
  &:last-child {
    border-bottom: none;
  }
`;

const MetricLabel = styled.span`
  color: var(--text-muted);
`;

const MetricValue = styled.span<{ change?: number }>`
  font-weight: 600;
  color: ${props => {
    if (props.change === undefined) return 'var(--text-light)';
    return props.change > 0 ? 'var(--danger-red)' :
      props.change < 0 ? 'var(--success-green)' : 'var(--text-muted)';
  }};
`;

function ScenarioComparison() {
  const [selectedScenarios, setSelectedScenarios] = useState([1, 2, 3]); // Baseline, 2035, 2050
  const [scenarioResults, setScenarioResults] = useState<Record<number, any>>({});
  // const [assessment, setAssessment] = useState<any>(null);
  // const [isLoading, setIsLoading] = useState(false);

  React.useEffect(() => {
    const saved = localStorage.getItem('lastAssessment');
    if (saved) {
      const parsed = JSON.parse(saved);
      // setAssessment(parsed);
      fetchAllScenarios(parsed);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchAllScenarios = async (baseAssessment: any) => {
    // setIsLoading(true);
    const results: Record<number, any> = {};

    try {
      for (const scenario of scenarios) {
        const riskData = await climateRiskApi.getRiskScore({
          latitude: baseAssessment.latitude,
          longitude: baseAssessment.longitude,
          temperature_increase: scenario.tempChange,
          precipitation_change: scenario.precipChange
        });

        const financialData = await climateRiskApi.getFinancialLoss({
          property_value: baseAssessment.financialData?.property_value || 500000,
          property_type: baseAssessment.property_type || 'residential',
          risk_assessment: riskData
        });

        results[scenario.id] = {
          riskScore: riskData.composite_risk_score,
          annualLoss: financialData.expected_annual_loss,
          premium: financialData.suggested_premium
        };
      }
      setScenarioResults(results);
    } catch (err) {
      console.error("Failed to fetch scenario data:", err);
    } finally {
      // setIsLoading(false);
    }
  };

  const scenarios = [
    {
      id: 1,
      name: 'Current Climate',
      description: 'Baseline conditions',
      tempChange: 0,
      precipChange: 0
    },
    {
      id: 2,
      name: '2035 Projection',
      description: 'Moderate climate change',
      tempChange: 1.2,
      precipChange: 8
    },
    {
      id: 3,
      name: '2050 Projection',
      description: 'High emissions scenario',
      tempChange: 2.5,
      precipChange: 15
    },
    {
      id: 4,
      name: 'Extreme Climate',
      description: 'Worst-case scenario',
      tempChange: 4.0,
      precipChange: 25
    }
  ];

  const toggleScenario = (id: number) => {
    setSelectedScenarios(prev =>
      prev.includes(id)
        ? prev.filter(scenarioId => scenarioId !== id)
        : [...prev, id]
    );
  };

  const calculateChange = (current: number, baseline: number) => {
    return ((current - baseline) / baseline) * 100;
  };

  const baselineScenario = scenarioResults[1];

  return (
    <ScenarioComparisonContainer>
      <SectionTitle>Scenario Comparison</SectionTitle>

      <ScenarioSelector>
        <SelectorHeader>
          <FiLayers />
          <SelectorTitle>Select Scenarios</SelectorTitle>
        </SelectorHeader>

        <ScenarioGrid>
          {scenarios.map(scenario => (
            <ScenarioOption
              key={scenario.id}
              selected={selectedScenarios.includes(scenario.id)}
              onClick={() => toggleScenario(scenario.id)}
            >
              <ScenarioName>{scenario.name}</ScenarioName>
              <ScenarioDescription>
                {scenario.description}
                <br />
                Temp: +{scenario.tempChange}°C
                <br />
                Precip: +{scenario.precipChange}%
              </ScenarioDescription>
            </ScenarioOption>
          ))}
        </ScenarioGrid>
      </ScenarioSelector>

      <ComparisonGrid>
        <ComparisonCard>
          <CardHeader>
            <FiBarChart2 />
            <CardTitle>Risk Score Comparison</CardTitle>
          </CardHeader>
          {selectedScenarios.map(scenarioId => {
            const scenario = scenarios.find(s => s.id === scenarioId);
            const metrics = scenarioResults[scenarioId];
            if (!metrics || !baselineScenario) return null;
            const change = scenarioId === 1 ? 0 : calculateChange(metrics.riskScore, baselineScenario.riskScore);

            return (
              <MetricRow key={scenarioId}>
                <MetricLabel>{scenario?.name}</MetricLabel>
                <MetricValue change={change}>
                  {metrics.riskScore.toFixed(1)}/100
                  {scenarioId !== 1 && ` (${change > 0 ? '+' : ''}${change.toFixed(1)}%)`}
                </MetricValue>
              </MetricRow>
            );
          })}
        </ComparisonCard>

        <ComparisonCard>
          <CardHeader>
            <FiTrendingUp />
            <CardTitle>Annual Loss Comparison</CardTitle>
          </CardHeader>
          {selectedScenarios.map(scenarioId => {
            const scenario = scenarios.find(s => s.id === scenarioId);
            const metrics = scenarioResults[scenarioId];
            if (!metrics || !baselineScenario) return null;
            const change = scenarioId === 1 ? 0 : calculateChange(metrics.annualLoss, baselineScenario.annualLoss);

            return (
              <MetricRow key={scenarioId}>
                <MetricLabel>{scenario?.name}</MetricLabel>
                <MetricValue change={change}>
                  ${metrics.annualLoss.toLocaleString()}
                  {scenarioId !== 1 && ` (${change > 0 ? '+' : ''}${change.toFixed(1)}%)`}
                </MetricValue>
              </MetricRow>
            );
          })}
        </ComparisonCard>

        <ComparisonCard>
          <CardHeader>
            <FiTrendingUp />
            <CardTitle>Suggested Premium</CardTitle>
          </CardHeader>
          {selectedScenarios.map(scenarioId => {
            const scenario = scenarios.find(s => s.id === scenarioId);
            const metrics = scenarioResults[scenarioId];
            if (!metrics || !baselineScenario) return null;
            const change = scenarioId === 1 ? 0 : calculateChange(metrics.premium, baselineScenario.premium);

            return (
              <MetricRow key={scenarioId}>
                <MetricLabel>{scenario?.name}</MetricLabel>
                <MetricValue change={change}>
                  ${metrics.premium.toLocaleString()}
                  {scenarioId !== 1 && ` (${change > 0 ? '+' : ''}${change.toFixed(1)}%)`}
                </MetricValue>
              </MetricRow>
            );
          })}
        </ComparisonCard>
      </ComparisonGrid>
    </ScenarioComparisonContainer>
  );
}

export default ScenarioComparison;