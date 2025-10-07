#!/bin/bash

# MLR-Bench Installation Script
# Educational implementation for teaching multi-agent orchestration

set -e

echo "=========================================="
echo "MLR-Bench Installation"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -e .

# Install additional packages
echo ""
echo "Installing Google ADK..."
pip install google-adk

echo ""
echo "Installing Flask and SocketIO..."
pip install flask flask-socketio aiohttp

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source .venv/bin/activate"
echo ""
echo "2. Configure your environment:"
echo "   cp .env.example .env"
echo "   # Edit .env and add your GOOGLE_API_KEY"
echo ""
echo "3. Run the visualization server:"
echo "   python -m mlr_bench.cli.ui_server"
echo ""
echo "4. In another terminal, run MLR-Bench:"
echo "   mlr-bench --task-id iclr2025_bi_align"
echo ""
echo "5. Open your browser at:"
echo "   http://localhost:5000"
echo ""
echo "=========================================="
