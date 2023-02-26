@REM activate the virtual environment and run the src/main.py script
@REM with the arguments passed to this script

@echo off
setlocal

@REM check if python 3.9 is installed
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


echo Activating virtual environment...
call %VENV_ACTIVATE%

echo Installing dependencies...
%VENV_PIP% install -r requirements.txt

@REM pass all arguments to the python script
echo Building...

call flet pack launcher.py -i "./assets/icons/favicon.png" --add-data "assets;assets" -n "Top.gg Voter" --product-name "Top.gg Voter" --product-version "1.0"