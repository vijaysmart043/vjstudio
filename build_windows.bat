@echo off
REM ============================================================================
REM VJ Studio - Windows 10/11 64-bit Automated Build Script
REM Compiles standalone VJStudio.exe with PyInstaller
REM ============================================================================
setlocal enabledelayedexpansion

echo =========================================================
echo    VJ STUDIO - WINDOWS DESKTOP BUILD AUTOMATION (x64)    
echo =========================================================

REM 1. Virtual environment
if not exist .venv (
    echo [1/5] Initializing Python virtual environment in .venv...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Python 3.11+ is required in system PATH.
        exit /b 1
    )
)
call .venv\Scripts\activate.bat

REM 2. Install dependencies
echo [2/5] Installing/verifying requirements...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM 3. Run automated tests
echo [3/5] Running automated tests...
python tests/test_config.py
if errorlevel 1 ( echo [FAIL] test_config failed & exit /b 1 )
python tests/test_paths.py
if errorlevel 1 ( echo [FAIL] test_paths failed & exit /b 1 )
python tests/test_sources.py
if errorlevel 1 ( echo [FAIL] test_sources failed & exit /b 1 )
python tests/test_scenes.py
if errorlevel 1 ( echo [FAIL] test_scenes failed & exit /b 1 )
python tests/test_program_pipeline.py
if errorlevel 1 ( echo [FAIL] test_program_pipeline failed & exit /b 1 )
echo [OK] All automated tests passed!

REM 4. Build with PyInstaller
echo [4/5] Building VJStudio.exe with PyInstaller...
pyinstaller --clean --noconfirm VJStudio.spec

REM 5. Validate executable
echo [5/5] Checking generated executable...
if exist dist\VJStudio\VJStudio.exe (
    copy /y dist\VJStudio\VJStudio.exe dist\VJStudio.exe >nul 2>&1
    echo =========================================================
    echo [SUCCESS] dist\VJStudio.exe generated successfully!
    echo Directory: %CD%\dist\VJStudio\
    echo Standalone Copy: %CD%\dist\VJStudio.exe
    echo =========================================================
) else if exist dist\VJStudio.exe (
    echo =========================================================
    echo [SUCCESS] dist\VJStudio.exe generated successfully!
    echo =========================================================
) else (
    echo [ERROR] VJStudio.exe was not created in dist/
    exit /b 1
)

endlocal
