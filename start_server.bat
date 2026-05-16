@echo off
REM FastReports API Server Startup Script (Windows)

echo ==========================================
echo FastReports API Server
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Set environment variables
if not defined API_HOST set API_HOST=0.0.0.0
if not defined API_PORT set API_PORT=8000

echo.
echo Starting API server on http://%API_HOST%:%API_PORT%
echo API Documentation: http://localhost:%API_PORT%/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python api_server.py

@REM Made with Bob
