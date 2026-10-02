@echo off
rem Double-click to run OEMS smoke checks: compile the source, load the modules, and connect to the database
setlocal
cd /d "%~dp0"
title OEMS - checks

if not exist .venv\Scripts\python.exe (
    echo [!] Run start.bat once first to create the virtual environment and install packages.
    pause
    exit /b 1
)
if not exist .env (
    echo [!] Run start.bat once first to create .env with the SQL Server connection.
    pause
    exit /b 1
)

echo Compiling source...
.venv\Scripts\python.exe -m compileall -q src
if errorlevel 1 goto :fail

echo Loading modules...
.venv\Scripts\python.exe -c "import src.config, src.db, src.link_service, src.student_app"
if errorlevel 1 goto :fail

echo Connecting to the database...
.venv\Scripts\python.exe -c "from src import db; db.fetch_one('SELECT 1')"
if errorlevel 1 goto :fail

echo.
echo All checks passed.
pause
goto :eof

:fail
echo.
echo [!] Some checks failed. Read the messages above.
pause
exit /b 1
