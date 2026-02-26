@echo off
echo Starting ClimateRisk AI Development Environment...
echo.

echo 1. Starting Docker services...
docker-compose up -d database redis

echo.
echo 2. Waiting for services to start...
timeout /t 10 /nobreak >nul

echo.
echo 3. Starting backend development server...
cd backend
start "Backend Server" cmd /k "python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python app/main.py"

echo.
echo 4. Starting frontend development server...
cd ..\frontend
start "Frontend Server" cmd /k "npm install && npm start"

echo.
echo Development environment started!
echo.
echo Backend API: http://localhost:8000
echo Frontend App: http://localhost:3000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause >nul