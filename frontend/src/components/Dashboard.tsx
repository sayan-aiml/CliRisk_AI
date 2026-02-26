import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FiMapPin, FiDollarSign, FiBarChart2, FiTrendingUp } from 'react-icons/fi';
import climateRiskApi from '../services/climateRiskApi';

const DashboardContainer = styled.div`
  display: flex;
  flex-direction: column;
  padding: 2rem;
  gap: 2rem;
  width: 100%;
  height: 100%;
  overflow-y: auto;
`;

const SectionTitle = styled.h2`
  font-size: 1.8rem;
  font-weight: 600;
  color: var(--text-light);
  margin-bottom: 1rem;
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
`;

const StatCard = styled(motion.div)`
  background: linear-gradient(135deg, var(--secondary-dark) 0%, var(--primary-dark) 100%);
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid var(--glass-border);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-glow);
    border-color: var(--accent-blue);
  }
`;

const CardHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
`;

const CardIcon = styled.div<{ color: string }>`
  width: 50px;
  height: 50px;
  border-radius: 12px;
  background: ${props => props.color};
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-dark);
  font-size: 1.5rem;
`;

const CardTitle = styled.h3`
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-light);
`;

const CardValue = styled.div`
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--accent-blue);
  margin: 0.5rem 0;
`;

const CardDescription = styled.p`
  font-size: 0.9rem;
  color: var(--text-muted);
  line-height: 1.5;
`;

const RiskDistribution = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
`;

const RiskCard = styled.div<{ $riskLevel: string }>`
  background: var(--secondary-dark);
  border-radius: 12px;
  padding: 1.5rem;
  border-left: 4px solid ${props => {
    switch (props.$riskLevel) {
      case 'low': return 'var(--success-green)';
      case 'moderate': return 'var(--warning-orange)';
      case 'high': return 'var(--danger-red)';
      case 'severe': return '#ff0000';
      default: return 'var(--text-muted)';
    }
  }};
  border: 1px solid var(--glass-border);
`;

const RiskHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
`;

const RiskTitle = styled.h4`
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-light);
`;

const RiskPercentage = styled.span<{ $riskLevel: string }>`
  font-size: 1.5rem;
  font-weight: 700;
  color: ${props => {
    switch (props.$riskLevel) {
      case 'low': return 'var(--success-green)';
      case 'moderate': return 'var(--warning-orange)';
      case 'high': return 'var(--danger-red)';
      case 'severe': return '#ff0000';
      default: return 'var(--text-muted)';
    }
  }};
`;

const RiskDescription = styled.p`
  font-size: 0.9rem;
  color: var(--text-muted);
  line-height: 1.5;
`;

function Dashboard() {
  const [stats, setStats] = useState({
    totalProperties: 1247,
    avgRiskScore: 42.3,
    totalExposure: 2850000,
    activeScenarios: 5
  });

  const [riskCategories, setRiskCategories] = useState([
    {
      level: 'low',
      title: 'Low Risk',
      percentage: 23,
      description: 'Properties with minimal climate exposure and low financial risk'
    },
    {
      level: 'moderate',
      title: 'Moderate Risk',
      percentage: 35,
      description: 'Properties with manageable risk requiring standard mitigation'
    },
    {
      level: 'high',
      title: 'High Risk',
      percentage: 28,
      description: 'Properties requiring significant risk management and insurance'
    },
    {
      level: 'severe',
      title: 'Severe Risk',
      percentage: 14,
      description: 'Properties with extreme exposure requiring immediate attention'
    }
  ]);

  const [isLoading, setIsLoading] = useState(true);

  React.useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await climateRiskApi.getDashboardStats();
        setStats({
          totalProperties: data.total_properties,
          avgRiskScore: data.avg_risk_score,
          totalExposure: data.total_exposure,
          activeScenarios: data.active_scenarios
        });

        // Merge descriptions back into the fetched distribution
        const descriptions: Record<string, string> = {
          low: 'Properties with minimal climate exposure and low financial risk',
          moderate: 'Properties with manageable risk requiring standard mitigation',
          high: 'Properties requiring significant risk management and insurance',
          severe: 'Properties with extreme exposure requiring immediate attention'
        };

        setRiskCategories(data.risk_distribution.map((item: any) => ({
          ...item,
          description: descriptions[item.level] || ''
        })));
      } catch (error) {
        console.error("Failed to fetch dashboard stats:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchStats();
  }, []);

  return (
    <DashboardContainer>
      <SectionTitle>Climate Risk Dashboard</SectionTitle>

      <StatsGrid>
        <StatCard
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <CardHeader>
            <CardIcon color="var(--primary-teal)">
              <FiMapPin />
            </CardIcon>
            <CardTitle>Properties Analyzed</CardTitle>
          </CardHeader>
          <CardValue>{stats?.totalProperties?.toLocaleString() || '0'}</CardValue>
          <CardDescription>
            Total properties in portfolio with climate risk assessments
          </CardDescription>
        </StatCard>

        <StatCard
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <CardHeader>
            <CardIcon color="var(--primary-emerald)">
              <FiBarChart2 />
            </CardIcon>
            <CardTitle>Average Risk Score</CardTitle>
          </CardHeader>
          <CardValue>{stats.avgRiskScore}</CardValue>
          <CardDescription>
            Composite risk score across all properties (0-100 scale)
          </CardDescription>
        </StatCard>

        <StatCard
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <CardHeader>
            <CardIcon color="var(--warning-orange)">
              <FiDollarSign />
            </CardIcon>
            <CardTitle>Total Exposure</CardTitle>
          </CardHeader>
          <CardValue>${(stats.totalExposure / 1000000).toFixed(1)}M</CardValue>
          <CardDescription>
            Annual expected loss across entire portfolio
          </CardDescription>
        </StatCard>

        <StatCard
          whileHover={{ scale: 1.02 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <CardHeader>
            <CardIcon color="var(--accent-blue)">
              <FiTrendingUp />
            </CardIcon>
            <CardTitle>Active Scenarios</CardTitle>
          </CardHeader>
          <CardValue>{stats.activeScenarios}</CardValue>
          <CardDescription>
            Climate scenarios currently being modeled
          </CardDescription>
        </StatCard>
      </StatsGrid>

      <SectionTitle>Risk Distribution</SectionTitle>
      <RiskDistribution>
        {riskCategories.map((category) => (
          <RiskCard key={category.level} $riskLevel={category.level}>
            <RiskHeader>
              <RiskTitle>{category.title}</RiskTitle>
              <RiskPercentage $riskLevel={category.level}>
                {category.percentage}%
              </RiskPercentage>
            </RiskHeader>
            <RiskDescription>{category.description}</RiskDescription>
          </RiskCard>
        ))}
      </RiskDistribution>
    </DashboardContainer>
  );
}

export default Dashboard;