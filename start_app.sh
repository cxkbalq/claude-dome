#!/bin/bash

# Exit on error
set -e

echo "=========================================="
echo "Computer Use Demo - Full Stack Startup"
echo "=========================================="

# Activate conda environment
echo "Activating conda environment py311..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate py311

# Set environment variables
export PYTHONPATH=$PYTHONPATH:$(pwd)
export DISPLAY_NUM=1
export HEIGHT=768
export WIDTH=1024
export DISPLAY=:${DISPLAY_NUM}

# Install backend dependencies
echo ""
echo "Installing backend dependencies..."
pip install -q -r api/requirements.txt

# Initialize database
echo ""
echo "Initializing database..."
python api/init_db.py

# Install frontend dependencies if needed
if [ ! -d "vue-dome/node_modules" ]; then
    echo ""
    echo "Installing frontend dependencies..."
    cd vue-dome
    npm install
    cd ..
fi

# Start the FastAPI backend in background
echo ""
echo "Starting FastAPI backend on port 8000..."
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Start the Vue frontend
echo ""
echo "Starting Vue frontend on port 5173..."
cd vue-dome
npm run dev -- --host 0.0.0.0 --port 5173 &
FRONTEND_PID=$!
cd ..

echo ""
echo "=========================================="
echo "✅ Services started successfully!"
echo "=========================================="
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🌐 Vue Application:   http://localhost:5173"
echo "💾 Database:          ./fastapi_app.db"
echo ""
echo "Press Ctrl+C to stop all services"
echo "=========================================="

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping services..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo "Services stopped."
    exit 0
}

# Trap Ctrl+C and call cleanup
trap cleanup INT TERM

# Keep the script running
wait $BACKEND_PID $FRONTEND_PID
