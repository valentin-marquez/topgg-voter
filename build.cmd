@echo off
setlocal

python --version > nul 2>&1
if errorlevel 1 (
    echo Python 3.9 is not installed.
    echo Please install Python 3.9 and add it to your PATH.
    exit /b 1
)

set "VENV_DIR=venv"
set "VENV_ACTIVATE=%VENV_DIR%\Scripts\activate.bat"
set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"
set "VENV_PIP=%VENV_DIR%\Scripts\pip.exe"

if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)

echo patching undetected_chromedriver > __init__.py 
copy assets/patch/__init__.py venv/Lib/site-packages/undetected_chromedriver/__init__.py

echo Activating virtual environment...
call %VENV_ACTIVATE%

echo Installing dependencies...
%VENV_PIP% install -r requirements.txt

echo Building...

call flet pack launcher.py -i "./assets/icons/favicon.png" --add-data "assets;assets" -n "Top.gg Voter" --product-name "Top.gg Voter" --product-version "1.0.0.0" --file-version "1.0.0" --file-description "Top.gg Voter" --copyright "@2023 by Nozz"