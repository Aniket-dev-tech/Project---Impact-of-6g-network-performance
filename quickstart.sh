#!/bin/bash
# Quick Start Script for 6G Manufacturing Analytics Platform
# This script sets up and runs the application

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║  6G Network Performance Manufacturing Analytics Platform          ║"
echo "║  Quick Start Setup Script                                         ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python installation
echo -e "${BLUE}[1/5]${NC} Checking Python installation..."
if ! command -v python &> /dev/null; then
    echo -e "${RED}✗ Python not found. Please install Python 3.8+${NC}"
    exit 1
fi
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"
echo ""

# Create virtual environment
echo -e "${BLUE}[2/5]${NC} Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}[3/5]${NC} Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Install dependencies
echo -e "${BLUE}[4/5]${NC} Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Display startup information
echo -e "${BLUE}[5/5]${NC} Starting Streamlit application..."
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    STARTUP INFORMATION                           ║${NC}"
echo -e "${GREEN}╠════════════════════════════════════════════════════════════════════╣${NC}"
echo -e "${GREEN}║ Application:  6G Manufacturing Analytics Dashboard               ║${NC}"
echo -e "${GREEN}║ Local URL:    ${BLUE}http://localhost:8501${GREEN}                             ║${NC}"
echo -e "${GREEN}║ Status:       Ready                                              ║${NC}"
echo -e "${GREEN}║                                                                  ║${NC}"
echo -e "${GREEN}║ Features:                                                        ║${NC}"
echo -e "${GREEN}║  • Network Performance Monitoring                                ║${NC}"
echo -e "${GREEN}║  • Efficiency Impact Analysis                                    ║${NC}"
echo -e "${GREEN}║  • Quality & Error Diagnostics                                   ║${NC}"
echo -e "${GREEN}║  • Custom KPI Dashboard                                          ║${NC}"
echo -e "${GREEN}║  • 6G Optimization Insights                                      ║${NC}"
echo -e "${GREEN}║                                                                  ║${NC}"
echo -e "${GREEN}║ Press Ctrl+C to stop the server                                  ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Run Streamlit
streamlit run app.py --logger.level=info
