@echo off
REM Quick Start Script for 6G Manufacturing Analytics Platform (Windows)

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║  6G Network Performance Manufacturing Analytics Platform          ║
echo ║  Quick Start Setup Script (Windows)                               ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

REM Check Python installation
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8 or higher
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% found
echo.

REM Create virtual environment
echo [2/5] Setting up virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1
echo ✓ Dependencies installed
echo.

REM Display startup information
echo [5/5] Starting Streamlit application...
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                    STARTUP INFORMATION                           ║
echo ╠════════════════════════════════════════════════════════════════════╣
echo ║ Application:  6G Manufacturing Analytics Dashboard               ║
echo ║ Local URL:    http://localhost:8501                              ║
echo ║ Status:       Ready                                              ║
echo ║                                                                  ║
echo ║ Features:                                                        ║
echo ║  • Network Performance Monitoring                                ║
echo ║  • Efficiency Impact Analysis                                    ║
echo ║  • Quality & Error Diagnostics                                   ║
echo ║  • Custom KPI Dashboard                                          ║
echo ║  • 6G Optimization Insights                                      ║
echo ║                                                                  ║
echo ║ Press Ctrl+C to stop the server                                  ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

REM Run Streamlit
streamlit run app.py --logger.level=info

pause
