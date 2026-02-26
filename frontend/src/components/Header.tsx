import React from 'react';
import styled from 'styled-components';
import { FiMap, FiBarChart2, FiDollarSign, FiLayers, FiHome, FiLogOut } from 'react-icons/fi';
import { useLocation, useNavigate } from 'react-router-dom';
import authService from '../services/authService';

const HeaderContainer = styled.header`
  background: rgba(17, 34, 64, 0.9);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(100, 255, 218, 0.1);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Logo = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--accent-blue);
  
  span {
    background: linear-gradient(135deg, var(--primary-teal) 0%, var(--primary-emerald) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
`;

const Nav = styled.nav`
  display: flex;
  gap: 2rem;
  align-items: center;
`;

const NavItem = styled.button<{ $active?: boolean }>`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  color: ${props => props.$active ? 'var(--accent-blue)' : 'var(--text-muted)'};
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  
  &:hover {
    color: var(--text-light);
    background: rgba(100, 255, 218, 0.1);
  }
  
  svg {
    font-size: 1.2rem;
  }
`;

const UserSection = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
`;

const UserAvatar = styled.div`
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-teal) 0%, var(--primary-emerald) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: var(--primary-dark);
`;

function Header() {
  const location = useLocation();
  const navigate = useNavigate();

  const navItems = [
    { path: '/', label: 'Dashboard', icon: <FiHome /> },
    { path: '/map', label: 'Map View', icon: <FiMap /> },
    { path: '/risk-analysis', label: 'Risk Analysis', icon: <FiBarChart2 /> },
    { path: '/financial-metrics', label: 'Financial Metrics', icon: <FiDollarSign /> },
    { path: '/scenarios', label: 'Scenarios', icon: <FiLayers /> },
  ];

  return (
    <HeaderContainer>
      <Logo>
        <FiMap />
        <span>ClimateRisk AI</span>
      </Logo>

      <Nav>
        {navItems.map((item) => (
          <NavItem
            key={item.path}
            $active={location.pathname === item.path}
            onClick={() => navigate(item.path)}
          >
            {item.icon}
            {item.label}
          </NavItem>
        ))}
      </Nav>

      <UserSection>
        <UserAvatar>AD</UserAvatar>
        <NavItem onClick={() => { authService.logout(); navigate('/login'); }} style={{ color: 'var(--danger-red)' }}>
          <FiLogOut />
          Logout
        </NavItem>
      </UserSection>
    </HeaderContainer>
  );
}

export default Header;