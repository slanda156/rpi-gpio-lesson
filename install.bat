@echo off
setlocal

REM Check for override argument
set FORCE=0
if "%1"=="--force" set FORCE=1

REM Check if .venv exists
if exist ".venv" (
    if %FORCE%==0 (
        echo .venv already exists. Skipping creation.
        goto install
    )
)

echo Creating virtual environment...
python -m virtualenv .venv

:install
call .venv\Scripts\activate.bat

pip install pip-tools
pip-compile
pip-sync
