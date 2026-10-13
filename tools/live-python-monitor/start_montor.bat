@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
    if errorlevel 1 exit /b 1
)

.venv\Scripts\python.exe -c "import serial; import matplotlib" >nul 2>&1
if errorlevel 1 (
    .venv\Scripts\python.exe -m pip install --upgrade pip
    if errorlevel 1 exit /b 1
    .venv\Scripts\python.exe -m pip install pyserial matplotlib
    if errorlevel 1 exit /b 1
)

.venv\Scripts\python.exe monitor.py
pause