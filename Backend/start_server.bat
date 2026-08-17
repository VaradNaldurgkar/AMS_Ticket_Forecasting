@echo off

cd /d %~dp0

IF NOT EXIST venv (
    echo.
    echo Virtual environment not found.
    echo Please run install_dependencies.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate

uvicorn src.api.main:app --host 127.0.0.1 --port 8000