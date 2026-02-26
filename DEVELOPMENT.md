# ClimateRisk AI - Development Setup

## Quick Start

1. **Install Docker Desktop** (if not already installed)
2. **Run the startup script:**
   ```bash
   start-dev.bat
   ```

## Manual Setup

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app/main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Database Setup
```bash
docker-compose up -d database redis
```

## Development URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432
- **Redis**: localhost:6379

## Environment Variables

Create `.env` file in backend directory:
```
DATABASE_URL=postgresql://climaterisk:climaterisk123@localhost:5432/climaterisk
REDIS_URL=redis://localhost:6379
MAPBOX_ACCESS_TOKEN=your_mapbox_token_here
```

## Testing the API

```bash
# Test risk score calculation
curl -X POST "http://localhost:8000/api/v1/climate-risk/risk-score" \
  -H "Content-Type: application/json" \
  -d '{"latitude": 40.7128, "longitude": -74.0060, "temperature_increase": 2.5, "precipitation_change": 15.0}'

# Test financial loss calculation
curl -X POST "http://localhost:8000/api/v1/climate-risk/financial-loss" \
  -H "Content-Type: application/json" \
  -d '{"property_value": 500000, "property_type": "residential", "latitude": 40.7128, "longitude": -74.0060}'
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
│   └── requirements.txt # Python dependencies
├── frontend/            # React frontend
│   ├── src/             # Source code
│   │   ├── components/  # React components
│   │   ├── services/    # API services
│   │   └── types/       # TypeScript types
│   └── package.json     # Node dependencies
├── infrastructure/      # Docker configs
└── docker-compose.yml   # Container orchestration
```

## Next Steps

1. Set up Mapbox account and get access token
2. Configure climate data sources
3. Add real geospatial data
4. Implement user authentication
5. Add portfolio management features
6. Deploy to cloud environment