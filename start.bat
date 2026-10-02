@echo off
rem Double-click to run OEMS from source (Teacher or Student app) with Python
setlocal
cd /d "%~dp0"
title OEMS

where python >nul 2>nul
if errorlevel 1 (
    echo [!] Python 3 is not installed. Download it from https://www.python.org and tick "Add python.exe to PATH".
    pause
    exit /b 1
)

if not exist .venv\Scripts\python.exe (
    echo Creating a virtual environment ^(first run only^)...
    python -m venv .venv
    if errorlevel 1 goto :fail
)

if not exist .venv\requirements.installed (
    echo Installing packages ^(first run only^)...
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    if errorlevel 1 goto :fail
    copy /y requirements.txt .venv\requirements.installed >nul
)

if not exist .env (
    copy .env.example .env >nul
    echo [!] Created .env - set the SQL Server connection, save, and close Notepad.
    start /wait notepad .env
)

echo.
echo   1 - Teacher app
echo   2 - Student app ^(needs credentials.json for Google Classroom^)
echo.
choice /c 12 /n /m "Choose 1 or 2: "
if errorlevel 2 (
    set "APP=src.student_app"
) else (
    set "APP=src.teacher_app"
)

.venv\Scripts\python.exe -m %APP%
if errorlevel 1 goto :fail
goto :eof

:fail
echo.
echo [!] Something went wrong. Read the messages above.
pause
exit /b 1
