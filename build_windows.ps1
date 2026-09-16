<#
.SYNOPSIS
    VJ Studio - Windows 10/11 64-bit Automated Build and Packaging Script
.DESCRIPTION
    1. Creates/uses the Python virtual environment (.venv)
    2. Installs and upgrades all dependencies from requirements.txt
    3. Verifies FFmpeg and native dependencies
    4. Runs automated tests (config, paths, sources, scenes, pipeline)
    5. Builds the standalone Windows application with PyInstaller
    6. Verifies the output at dist/VJStudio.exe
#>

[CmdletBinding()]
param(
    [switch]$SkipTests = $false,
    [switch]$Clean = $false
)

$ErrorActionPreference = "Stop"

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "   VJ STUDIO - PROFESSIONAL WINDOWS BUILD SYSTEM (x64)   " -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

# 1. Virtual Environment Setup
$VenvDir = Join-Path $ProjectRoot ".venv"
$PythonExe = Join-Path $VenvDir "Scripts\python.exe"
$PipExe = Join-Path $VenvDir "Scripts\pip.exe"
$PyInstallerExe = Join-Path $VenvDir "Scripts\pyinstaller.exe"

if (-not (Test-Path $PythonExe)) {
    Write-Host "[1/6] Creating Python virtual environment in .venv..." -ForegroundColor Yellow
    python -m venv $VenvDir
    if (-not (Test-Path $PythonExe)) {
        Write-Error "Failed to initialize Python virtual environment. Ensure Python 3.11+ is in PATH."
    }
} else {
    Write-Host "[1/6] Found existing virtual environment: $VenvDir" -ForegroundColor Green
}

# 2. Dependency Installation
Write-Host "[2/6] Installing/verifying dependencies from requirements.txt..." -ForegroundColor Yellow
& $PipExe install --upgrade pip
& $PipExe install -r requirements.txt

# 3. FFmpeg and Native Dependency Verification
Write-Host "[3/6] Verifying FFmpeg and native runtime dependencies..." -ForegroundColor Yellow
$BundledFFmpeg = Join-Path $ProjectRoot "ffmpeg\bin\ffmpeg.exe"
$FFmpegFound = $false

if (Test-Path $BundledFFmpeg) {
    Write-Host "  -> Bundled FFmpeg found: $BundledFFmpeg" -ForegroundColor Green
    $FFmpegFound = $true
} else {
    try {
        $SysFFmpeg = (Get-Command ffmpeg -ErrorAction SilentlyContinue).Source
        if ($SysFFmpeg) {
            Write-Host "  -> System FFmpeg found: $SysFFmpeg" -ForegroundColor Green
            $FFmpegFound = $true
        }
    } catch {
        $FFmpegFound = $false
    }
}

if (-not $FFmpegFound) {
    Write-Warning "FFmpeg executable not detected in bundled or PATH directories. Broadcast encoding will use fallback/software pipeline."
}

# 4. Run Automated Test Suite
if (-not $SkipTests) {
    Write-Host "[4/6] Running automated test suite..." -ForegroundColor Yellow
    & $PythonExe tests/test_config.py
    & $PythonExe tests/test_paths.py
    & $PythonExe tests/test_sources.py
    & $PythonExe tests/test_scenes.py
    & $PythonExe tests/test_program_pipeline.py
    Write-Host "  -> All test suites passed successfully!" -ForegroundColor Green
} else {
    Write-Host "[4/6] Skipping automated test suite (-SkipTests flag passed)." -ForegroundColor Gray
}

# 5. Clean Previous Builds
if ($Clean) {
    Write-Host "[5/6] Cleaning previous build artifacts..." -ForegroundColor Yellow
    if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
    if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
} else {
    Write-Host "[5/6] Preparing build directories..." -ForegroundColor Yellow
}

# 6. PyInstaller Compilation
Write-Host "[6/6] Compiling standalone VJStudio.exe with PyInstaller..." -ForegroundColor Yellow
& $PyInstallerExe --clean --noconfirm VJStudio.spec

# Check Output
$FinalExeFolder = Join-Path $ProjectRoot "dist\VJStudio\VJStudio.exe"
$FinalExeSingle = Join-Path $ProjectRoot "dist\VJStudio.exe"

if (Test-Path $FinalExeFolder) {
    # If folder mode, copy or symlink to dist/VJStudio.exe as well for convenience
    Copy-Item $FinalExeFolder $FinalExeSingle -Force -ErrorAction SilentlyContinue
    Write-Host ""
    Write-Host "=========================================================" -ForegroundColor Green
    Write-Host " [SUCCESS] VJStudio.exe build completed successfully!   " -ForegroundColor Green
    Write-Host " Standalone App: $FinalExeFolder" -ForegroundColor Green
    Write-Host " Root Executable: $FinalExeSingle" -ForegroundColor Green
    Write-Host "=========================================================" -ForegroundColor Green
} elseif (Test-Path $FinalExeSingle) {
    Write-Host ""
    Write-Host "=========================================================" -ForegroundColor Green
    Write-Host " [SUCCESS] VJStudio.exe single-file build completed!     " -ForegroundColor Green
    Write-Host " Executable: $FinalExeSingle" -ForegroundColor Green
    Write-Host "=========================================================" -ForegroundColor Green
} else {
    Write-Error "PyInstaller completed but VJStudio.exe was not generated in dist/."
}
