@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
    if errorlevel 1 exit /b 1
)

".venv\Scripts\python.exe" -m pip install minimalmodbus pyserial
if errorlevel 1 exit /b 1

".venv\Scripts\python.exe" gui.py

pause
exit