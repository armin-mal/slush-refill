@echo off
setlocal

if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
    .venv\Scripts\python -m pip install --upgrade pip
    .venv\Scripts\pip install -r requirements.txt
)

.venv\Scripts\python monitor.py
exit