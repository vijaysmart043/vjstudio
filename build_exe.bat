@echo off
setlocal enabledelayedexpansion

echo =========================================================
echo       VJ STUDIO — WINDOWS 64-BIT EXECUTABLE BUILDER
echo =========================================================

REM 1. Check Python installation
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python 3.12+ was not found in your PATH.
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [1/6] Python environment detected:
python --version

REM 2. Install requirements
echo [2/6] Checking and installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

REM 3. Run environment validation check
echo [3/6] Running environment validator...
python scripts\check_environment.py

REM 4. Clean previous build directories
echo [4/6] Cleaning previous build artifacts...
if exist build rd /s /q build
if exist dist rd /s /q dist

REM 5. Run PyInstaller
echo [5/6] Compiling VJ Studio with PyInstaller...
pyinstaller --clean --noconfirm VJStudio.spec
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] PyInstaller compilation failed!
    pause
    exit /b 1
)

REM 6. Validate output
echo [6/6] Validating standalone executable...
if exist dist\VJStudio\VJStudio.exe (
    copy /y dist\VJStudio\VJStudio.exe dist\VJStudio.exe >nul 2>&1
    echo =========================================================
    echo [SUCCESS] VJStudio.exe built successfully!
    echo Output directory: %CD%\dist\VJStudio\
    echo Executable:       %CD%\dist\VJStudio\VJStudio.exe
    echo Standalone Copy:  %CD%\dist\VJStudio.exe
    echo =========================================================
) else (
    echo [ERROR] VJStudio.exe was not found in dist\VJStudio!
    pause
    exit /b 1
)

echo Done.
pause
