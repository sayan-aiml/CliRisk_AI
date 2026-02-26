# ClimateRisk AI

A hyperlocal climate risk intelligence platform that quantifies long-term environmental exposure and converts it into financial risk metrics for insurers, banks, developers, asset managers, and governments.

## Core Features

- **Hyperlocal Risk Engine**: Street-level flood probability, heat stress, air quality, and infrastructure vulnerability modeling
- **Interactive Geospatial Map**: Real-time risk visualization with multiple overlay layers
- **Financial Intelligence**: Property loss modeling, premium adjustment, and exposure projections
- **Scenario Simulation**: Climate projection modeling (2035, 2050, extreme scenarios)
- **Multi-Hazard Intelligence**: Comprehensive risk assessment across multiple climate hazards
- **Enterprise API**: Production-ready API with authentication and rate limiting

## Technology Stack

- **Backend**: Python FastAPI, PostgreSQL + PostGIS, Redis
- **Frontend**: React + TypeScript, Mapbox GL JS
- **ML/Analytics**: Scikit-learn, XGBoost, Geopandas
- **Infrastructure**: Docker, Docker Compose, Nginx
- **Monitoring**: Prometheus, Grafana

## Quick Start

```bash
# Clone and setup
git clone <repository>
cd climate-risk-ai

# Start development environment
docker-compose up -d

# Install frontend dependencies
cd frontend && npm install

# Install backend dependencies
cd backend && pip install -r requirements.txt

# Run development servers
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Project Structure

```
climate-risk-ai/
├── backend/              # FastAPI backend
│   ├── app/             # Main application
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Core configuration
│   │   ├── models/      # Database models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   └── utils/       # Utilities
│   ├── alembic/         # Database migrations
│   └── tests/           # Test suite
├── frontend/            # React frontend
│   ├── public/          # Static assets
│   ├── src/             # Source code
│   │   ├── components/  # React components
│   │   ├── hooks/       # Custom hooks
│   │   ├── services/    # API services
│   │   ├── store/       # State management
│   │   └── types/       # TypeScript types
│   └── src-tauri/       # Tauri desktop app (optional)
├── data/                # Data processing pipelines
├── notebooks/           # Jupyter notebooks for ML
├── infrastructure/      # Docker, k8s configs
└── docs/               # Documentation
```

## Development Status

- [ ] Phase 1: Foundation & Core Architecture
- [ ] Phase 2: Core Risk Engine  
- [ ] Phase 3: Interactive Map System
- [ ] Phase 4: Financial Intelligence
- [ ] Phase 5: Enterprise Features

## License

Proprietary - ClimateRisk AI