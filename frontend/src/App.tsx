import React from 'react';
import { Routes, Route } from 'react-router-dom';
import styled from 'styled-components';
import MapView from './components/MapView';
import Dashboard from './components/Dashboard';
import RiskAnalysis from './components/RiskAnalysis';
import FinancialMetrics from './components/FinancialMetrics';
import ScenarioComparison from './components/ScenarioComparison';
import Header from './components/Header';
import Login from './components/Login';
import authService from './services/authService';

const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #0a192f;
  color: #e6f1ff;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
`;

const MainContent = styled.main`
  flex: 1;
  display: flex;
  overflow: hidden;
`;

const PrivateRoute = ({ children }: { children: React.ReactNode }) => {
  return authService.isAuthenticated() ? <>{children}</> : <Login />;
};

function App() {
  return (
    <AppContainer>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="*" element={
          <PrivateRoute>
            <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
              <Header />
              <MainContent>
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/map" element={<MapView />} />
                  <Route path="/risk-analysis" element={<RiskAnalysis />} />
                  <Route path="/financial-metrics" element={<FinancialMetrics />} />
                  <Route path="/scenarios" element={<ScenarioComparison />} />
                </Routes>
              </MainContent>
            </div>
          </PrivateRoute>
        } />
      </Routes>
    </AppContainer>
  );
}

export default App;