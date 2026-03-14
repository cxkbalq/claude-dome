#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting local Ubuntu setup for Computer Use Demo..."

# 1. Install System Dependencies
echo "📦 Checking and installing system dependencies..."
sudo apt-get update

# Ubuntu 20.04 compatibility check
UBUNTU_VERSION=$(lsb_release -rs 2>/dev/null || echo "22.04")
FIREFOX_PKG="firefox-esr"
PDF_PKG="xpdf"
if [ "$UBUNTU_VERSION" = "20.04" ]; then
    FIREFOX_PKG="firefox"
    # xpdf is not available in Ubuntu 20.04 repositories, use evince as a modern alternative
    PDF_PKG="evince"
fi

sudo apt-get install -y \
    xvfb xterm xdotool scrot imagemagick mutter x11vnc \
    build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev curl git libncursesw5-dev \
    xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
    net-tools netcat software-properties-common \
    libreoffice $FIREFOX_PKG x11-apps $PDF_PKG gedit xpaint \
    tint2 galculator pcmanfm unzip

# 2. Setup Python Environment
echo "🐍 Activating Python environment (Conda: py311)..."

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Conda not found. Please ensure Conda is installed and in your PATH."
    exit 1
fi

# Activate the existing conda environment
CONDA_PATH=$(conda info --base)
source "$CONDA_PATH/etc/profile.d/conda.sh"
conda activate py311

pip install --upgrade pip
pip install -r computer_use_demo/requirements.txt

# 3. Setup noVNC
echo "🌐 Setting up noVNC..."
if [ ! -d "noVNC" ]; then
    git clone --branch v1.5.0 https://github.com/novnc/noVNC.git noVNC
    git clone --branch v0.12.0 https://github.com/novnc/websockify noVNC/utils/websockify
    ln -sf vnc.html noVNC/index.html
fi

# 4. Environment Variables
export DISPLAY_NUM=1
export HEIGHT=768
export WIDTH=1024
export DISPLAY=:${DISPLAY_NUM}
export HOME=$(pwd)
export ANTHROPIC_BASE_URL="https://www.packyapi.com"

# Ensure config directory exists where tint2 expects it
mkdir -p $HOME/.config
cp -r image/.config/* $HOME/.config/ 2>/dev/null || true

# 5. Launch Services
echo "🎬 Launching services..."

# Ensure we have the right permissions for startup scripts
chmod +x ./image/*.sh

# Start Xvfb
./image/xvfb_startup.sh

# Start Window Manager and other desktop components
cd image
./tint2_startup.sh
./mutter_startup.sh
./x11vnc_startup.sh
cd ..

# Start noVNC
echo "starting noVNC"
./noVNC/utils/novnc_proxy \
    --vnc localhost:5900 \
    --listen 6080 \
    --web ./noVNC \
    > /tmp/novnc.log 2>&1 &

# Wait for noVNC to start
timeout=10
while [ $timeout -gt 0 ]; do
    if netstat -tuln | grep -q ":6080 "; then
        break
    fi
    sleep 1
    ((timeout--))
done
echo "noVNC started successfully"

# 6. Start Streamlit App
echo "✨ Starting Streamlit app..."

# Start the auxiliary http server (needed for some local file serving)
cd image
python3 http_server.py > /tmp/server_logs.txt 2>&1 &
cd ..

# Start Streamlit with explicit environment variables
WIDTH=$WIDTH HEIGHT=$HEIGHT DISPLAY_NUM=$DISPLAY_NUM ANTHROPIC_BASE_URL=$ANTHROPIC_BASE_URL \
STREAMLIT_SERVER_PORT=8501 python -m streamlit run computer_use_demo/streamlit.py &

echo "✨ Computer Use Demo is ready!"
echo "➡️  Open http://localhost:6080 in your browser to begin the VNC session"
echo "➡️  The Streamlit app is running at http://localhost:8501"

# Wait for all background processes
wait
