#!/bin/bash
# FastReports API Server Startup Script

echo "=========================================="
echo "FastReports API Server"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Set environment variables
export API_HOST=${API_HOST:-"0.0.0.0"}
export API_PORT=${API_PORT:-"8000"}

echo ""
echo "Starting API server on http://${API_HOST}:${API_PORT}"
echo "API Documentation: http://localhost:${API_PORT}/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python api_server.py

# Made with Bob
