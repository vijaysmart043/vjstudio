@echo off
setlocal

echo =========================================================
echo       VJ STUDIO — INNO SETUP INSTALLER BUILDER
echo =========================================================

REM Check if standalone build exists
if not exist dist\VJStudio\VJStudio.exe (
    echo [ERROR] dist\VJStudio\VJStudio.exe not found!
    echo Please run build_exe.bat first to build the executable.
    pause
    exit /b 1
)

REM Check if Inno Setup Compiler (ISCC) is available
where iscc >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Inno Setup compiler (iscc.exe) not found in PATH.
    echo Default installation path is typically:
    echo "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    echo.
    echo Please compile 'installer.iss' manually using Inno Setup GUI,
    echo or add Inno Setup to your system PATH.
    pause
    exit /b 0
)

echo Compiling VJStudio-Setup.exe using Inno Setup...
iscc installer.iss
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Installer generated in Output\VJStudio-Setup.exe
) else (
    echo [ERROR] Inno Setup compilation failed.
)

pause
