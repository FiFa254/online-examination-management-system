@echo off
setlocal
cd /d "%~dp0"
title Build OEMS.exe

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

echo Installing PyQt5 and PyInstaller...
.venv\Scripts\python.exe -m pip install "PyQt5>=5.15" pyinstaller
if errorlevel 1 goto :fail

.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --onefile --windowed --name OEMS --icon oems_icon.ico --paths . src\launcher.py
if errorlevel 1 goto :fail

echo.
echo Done: dist\OEMS.exe
echo Copy it into the folder that has Student.exe and Teacher.exe, then double-click OEMS.exe.
pause
goto :eof

:fail
echo.
echo [!] Build failed. Read the messages above.
pause
exit /b 1
