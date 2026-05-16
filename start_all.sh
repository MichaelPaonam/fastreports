#!/bin/bash
# FastReports - Start Both API Server and Dashboard

echo "=========================================="
echo "FastReports - Full Stack Startup"
echo "=========================================="
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down services..."
    kill $API_PID 2>/dev/null
    kill $DASHBOARD_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating Python virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Start API server in background
echo ""
echo "Starting API server on http://localhost:8000..."
python api_server.py > output/logs/api_server.log 2>&1 &
API_PID=$!
echo "API server started (PID: $API_PID)"
echo "API logs: output/logs/api_server.log"

# Wait for API server to start
sleep 3

# Check if API server is running
if ! kill -0 $API_PID 2>/dev/null; then
    echo "ERROR: API server failed to start. Check logs at output/logs/api_server.log"
    exit 1
fi

# Install dashboard dependencies if needed
if [ ! -d "dashboard/node_modules" ]; then
    echo ""
    echo "Installing dashboard dependencies..."
    cd dashboard
    npm install
    cd ..
fi

# Start dashboard
echo ""
echo "Starting dashboard on http://localhost:3000..."
cd dashboard
npm run dev > ../output/logs/dashboard.log 2>&1 &
DASHBOARD_PID=$!
cd ..
echo "Dashboard started (PID: $DASHBOARD_PID)"
echo "Dashboard logs: output/logs/dashboard.log"

echo ""
echo "=========================================="
echo "Services Running:"
echo "  - API Server: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Dashboard: http://localhost:3000"
echo "=========================================="
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for both processes
wait $API_PID $DASHBOARD_PID

# Made with Bob
