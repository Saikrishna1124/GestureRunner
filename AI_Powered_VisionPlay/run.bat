@echo off
setlocal
cd /d "%~dp0"
echo Starting AI Subway Surfer Controller...
if not exist .venv (
    echo Error: Virtual environment [.venv] not found.
    pause
    exit /b
)
call .venv\Scripts\activate.bat
python src\controller.py
pause
endlocal
