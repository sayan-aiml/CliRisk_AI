import React from 'react';
import styled from 'styled-components';
import { FiBarChart2, FiPieChart, FiTrendingUp } from 'react-icons/fi';

const RiskAnalysisContainer = styled.div`
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

const AnalysisGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
`;

const AnalysisCard = styled.div`
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

const RiskBreakdown = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const RiskItem = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: rgba(17, 34, 64, 0.5);
  border-radius: 8px;
  border: 1px solid var(--glass-border);
`;

const RiskLabel = styled.span`
  font-weight: 500;
  color: var(--text-light);
`;

const RiskScore = styled.span<{ level: string }>`
  font-weight: 700;
  color: ${props => {
    switch (props.level) {
      case 'low': return 'var(--success-green)';
      case 'moderate': return 'var(--warning-orange)';
      case 'high': return 'var(--danger-red)';
      case 'severe': return '#ff0000';
      default: return 'var(--text-muted)';
    }
  }};
`;

function RiskAnalysis() {
  const [assessment, setAssessment] = React.useState<any>(null);

  React.useEffect(() => {
    const saved = localStorage.getItem('lastAssessment');
    if (saved) {
      setAssessment(JSON.parse(saved));
    }
  }, []);

  const getRiskData = () => {
    if (!assessment) return [];
    return [
      { hazard: 'Flood Risk', score: assessment.floodRisk, level: determineLevel(assessment.floodRisk) },
      { hazard: 'Heat Stress', score: assessment.heatRisk, level: determineLevel(assessment.heatRisk) },
      { hazard: 'Air Quality', score: assessment.airQualityRisk, level: determineLevel(assessment.airQualityRisk) },
      { hazard: 'Water Scarcity', score: 32, level: 'low' }, // Placeholder for now
      { hazard: 'Infrastructure', score: 65, level: 'moderate' } // Placeholder for now
    ];
  };

  const determineLevel = (score: number) => {
    if (score < 25) return 'low';
    if (score < 50) return 'moderate';
    if (score < 75) return 'high';
    return 'severe';
  };

  const getDrivers = () => {
    if (!assessment || !assessment.risk_drivers) {
      // Fallback or derived from the riskData mapping
      return [
        { factor: 'Elevation', contribution: 25 },
        { factor: 'Drainage Distance', contribution: 20 },
        { factor: 'Urban Density', contribution: 15 }
      ];
    }
    // Map from backend risk_drivers Dict[str, float]
    const labels: Record<string, string> = {
      flood: 'Flood Contribution',
      heat: 'Heat Contribution',
      air_quality: 'Air Quality Impact',
      water_scarcity: 'Water Stress',
      infrastructure: 'Infrastructure Fragility'
    };

    return Object.entries(assessment.risk_drivers || {}).map(([key, value]) => ({
      factor: labels[key] || key,
      contribution: value as number
    }));
  };

  const riskData = getRiskData();
  const drivers = getDrivers();

  return (
    <RiskAnalysisContainer>
      <SectionTitle>Risk Analysis</SectionTitle>

      {!assessment && (
        <AnalysisCard style={{ marginBottom: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
          Please select a location on the Map first to see detailed risk analysis.
        </AnalysisCard>
      )}

      <AnalysisGrid>
        <AnalysisCard>
          <CardHeader>
            <FiBarChart2 />
            <CardTitle>Hazard Breakdown</CardTitle>
          </CardHeader>
          <RiskBreakdown>
            {riskData.map((item) => (
              <RiskItem key={item.hazard}>
                <RiskLabel>{item.hazard}</RiskLabel>
                <RiskScore level={item.level}>
                  {item.score}/100
                </RiskScore>
              </RiskItem>
            ))}
          </RiskBreakdown>
        </AnalysisCard>

        <AnalysisCard>
          <CardHeader>
            <FiPieChart />
            <CardTitle>Risk Drivers</CardTitle>
          </CardHeader>
          <RiskBreakdown>
            {drivers.map((driver) => (
              <RiskItem key={driver.factor}>
                <RiskLabel>{driver.factor}</RiskLabel>
                <RiskScore level="moderate">
                  {driver.contribution}%
                </RiskScore>
              </RiskItem>
            ))}
          </RiskBreakdown>
        </AnalysisCard>
      </AnalysisGrid>

      <AnalysisCard>
        <CardHeader>
          <FiTrendingUp />
          <CardTitle>Risk Trends</CardTitle>
        </CardHeader>
        <div style={{
          height: '300px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'var(--text-muted)'
        }}>
          Risk trend visualization will be displayed here
        </div>
      </AnalysisCard>
    </RiskAnalysisContainer>
  );
}

export default RiskAnalysis;