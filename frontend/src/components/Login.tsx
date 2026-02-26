import React, { useState } from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import { FiLock, FiUser, FiMap } from 'react-icons/fi';
import authService from '../services/authService';

const LoginContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: #0a192f;
  color: #e6f1ff;
  padding: 2rem;
`;

const LoginCard = styled.div`
  background: rgba(17, 34, 64, 0.9);
  backdrop-filter: blur(12px);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  padding: 2.5rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
`;

const Logo = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 2rem;
  color: var(--accent-blue);
  
  span {
    background: linear-gradient(135deg, var(--primary-teal) 0%, var(--primary-emerald) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
`;

const Title = styled.h2`
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
`;

const InputGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const Label = styled.label`
  font-size: 0.9rem;
  color: var(--text-muted);
`;

const InputWrapper = styled.div`
  position: relative;
  display: flex;
  align-items: center;
`;

const InputIcon = styled.div`
  position: absolute;
  left: 1rem;
  color: var(--accent-blue);
`;

const StyledInput = styled.input`
  width: 100%;
  background: var(--primary-dark);
  border: 1px solid var(--glass-border);
  color: var(--text-light);
  padding: 0.75rem 1rem 0.75rem 3rem;
  border-radius: 8px;
  font-size: 1rem;

  &:focus {
    outline: none;
    border-color: var(--accent-blue);
    box-shadow: 0 0 0 2px rgba(100, 255, 218, 0.1);
  }
`;

const LoginButton = styled.button`
  background: linear-gradient(135deg, var(--primary-teal) 0%, var(--primary-emerald) 100%);
  color: var(--primary-dark);
  border: none;
  padding: 0.75rem;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1rem;

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-glow);
  }

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
`;

const ErrorMessage = styled.div`
  color: var(--danger-red);
  font-size: 0.85rem;
  text-align: center;
  margin-top: 1rem;
`;

const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      await authService.login(username, password);
      navigate('/');
    } catch (err: any) {
      setError('Invalid username or password');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <LoginContainer>
      <LoginCard>
        <Logo>
          <FiMap />
          <span>CliRisk AI</span>
        </Logo>
        <Title>Enterprise Access</Title>
        <Form onSubmit={handleLogin}>
          <InputGroup>
            <Label>Username</Label>
            <InputWrapper>
              <InputIcon><FiUser /></InputIcon>
              <StyledInput
                type="text"
                placeholder="Admin"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </InputWrapper>
          </InputGroup>
          <InputGroup>
            <Label>Password</Label>
            <InputWrapper>
              <InputIcon><FiLock /></InputIcon>
              <StyledInput
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </InputWrapper>
          </InputGroup>
          <LoginButton type="submit" disabled={isLoading}>
            {isLoading ? 'Authenticating...' : 'Sign In'}
          </LoginButton>
          {error && <ErrorMessage>{error}</ErrorMessage>}
        </Form>
      </LoginCard>
    </LoginContainer>
  );
};

export default Login;
