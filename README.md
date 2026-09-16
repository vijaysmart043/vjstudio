# VJ STUDIO — Professional Live Video Production & Broadcast System

**VJ Studio** is an original Windows 10/11 desktop application inspired by the workflow of professional live broadcast systems (such as vMix and OBS Studio). Engineered with Python 3.12+, PySide6, OpenCV, and FFmpeg, it delivers a high-performance, modular production architecture with a premium dark broadcast control room interface.

---

## Architecture & Layout

```
TOP BAR: VJ STUDIO  [File | Project | Inputs | Stream | Record | Settings | Help]
---------------------------------------------------------------------------------
MAIN PRODUCTION MONITORS:
[ PREVIEW (Green Tally) ]  <--->  [ TRANSITIONS: CUT / FADE / T-BAR ]  <--->  [ PROGRAM LIVE (Red Tally) ]
---------------------------------------------------------------------------------
LOWER PRODUCTION DECK:
[ INPUT SOURCES (Cameras, Screen, Video, Image) ]     [ AUDIO MIXER (Mic 1, Mic 2, Sys, Master) ]
---------------------------------------------------------------------------------
BOTTOM TELEMETRY STATUS BAR:
LIVE: OFF  |  REC: OFF  |  FPS: 60  |  CPU: 12%  |  DROPPED: 0  |  TIMECODE: 00:00:00
```

---

## Key Features in Phase 1

1. **Dual-Bus Broadcast Switching**:
   - **Preview Monitor**: 16:9 viewport with real-time green tally border.
   - **Program Monitor**: 16:9 viewport with luminous red "● PROGRAM LIVE" tally framing.
   - **Transition Center**: Instant `CUT`, timed `AUTO FADE` (500ms default, configurable), `DISSOLVE`, and manual interactive **T-Bar fader**.
2. **Media Input Subsystem**:
   - Generic `MediaSource` polymorphic foundation with coordinate transform, scale, and opacity.
   - **Camera Sources**: DirectShow Windows camera discovery with broadcast SMPTE color bar standby generator.
   - **Display / Screen Capture**: Desktop window and monitor grabber with fallback grid canvas.
   - **Video Clip Playback**: Video playback with Play, Pause, Loop, and Seek.
   - **Image Graphics**: Static graphics (PNG, JPG, WEBP) for logos and backgrounds.
3. **Audio Mixer Subsystem**:
   - 4-channel audio console: `MIC 1`, `MIC 2`, `SYSTEM`, `MASTER`.
   - Dual-channel (L/R) stereo LED dB peak meters with dynamic smooth decay.
   - Volume faders (0–100%) and instant Mute buttons.
4. **Broadcast Overlays & Graphics Engine**:
   - Text overlays, Lower-Third banners (with speaker name and title), scrolling News Ticker, and on-screen 24-hour studio clock.
5. **Robust FFmpeg & Hardware Encoder Engine**:
   - Automatic detection across bundled `ffmpeg/bin/`, user custom directory, and system PATH.
   - Diagnostic probes for NVIDIA NVENC (`h264_nvenc`), Intel QuickSync (`h264_qsv`), AMD AMF (`h264_amf`), and software `libx264`.
   - Hardware encoding with automatic software fallback.
6. **Streaming & Recording Architecture**:
   - RTMP broadcast pipeline with stream key masking (never logged or exposed).
   - Local program recording with safe timestamped files (`VJStudio_YYYY-MM-DD_HH-MM-SS.mp4`).
7. **Broadcast Hotkeys**:
   - `C` → Instant Cut
   - `F` → Auto Fade
   - `D` → Dissolve
   - `Space` → Start/Stop Stream
   - `R` → Start/Stop Local Recording
   - `F1`–`F4` → Quick Cue Inputs 1–4 to Preview
   - `F5`–`F6` → Quick Cue Scenes 1–2
8. **Storage & Settings Persistence**:
   - User settings saved to `%APPDATA%\VJStudio\config\settings.json`.
   - Rotating application logs stored in `%APPDATA%\VJStudio\logs\vjstudio.log`.
   - Local SQLite database for session history and project states.
   - `.vjstudio` project file serialization.

---

## Directory Structure

```
VJ-Studio/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/           # Config, paths, logger, constants, exceptions, events, app lifecycle
│   ├── ui/             # PySide6 main window, theme, stylesheets
│   │   └── widgets/    # Preview, Program, Source cards, Mixer, Transitions, Dialogs
│   ├── media/          # Camera, Screen capture, Video, Image, Compositor, Renderer
│   ├── production/     # Scene, SceneManager, InputManager, TransitionManager, Buses
│   ├── audio/          # Mixer, Metering, Channels, Device management
│   ├── streaming/      # RTMP streamer, SRT interface, Stream coordinator
│   ├── recording/      # Program recorder, timestamped file manager
│   ├── ffmpeg/         # FFmpeg binary detector, diagnostics, subprocess manager
│   ├── graphics/       # Overlays, Lower-thirds, Tickers, Clocks
│   ├── storage/        # SQLite database, project repository
│   └── commands/       # Decoupled CommandBus and HotkeyManager
├── config/
│   └── default.json    # Default settings
├── scripts/
│   ├── check_environment.py
│   └── download_ffmpeg.py
├── tests/              # Unit and integration test suite
├── main.py             # Root execution entry point
├── requirements.txt    # Runtime dependencies
├── requirements-dev.txt# Development & packaging dependencies
├── VJStudio.spec       # PyInstaller standalone build recipe
├── build_exe.bat       # One-click Windows executable builder
├── build_installer.bat # Inno Setup installer generator
├── installer.iss       # Inno Setup script
├── PROJECT_STATUS.md   # Roadmap and status tracker
└── README.md
```

---

## Windows Quick Start Guide

### Prerequisites
- Windows 10 or 11 (64-bit)
- Python 3.12+ (ensure **"Add python.exe to PATH"** is checked during installation)

### 1. Installation
Open Command Prompt or PowerShell in the project directory:

```cmd
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 2. Verify Environment
Run the diagnostic check:

```cmd
python scripts\check_environment.py
```

### 3. Run Application
Launch VJ Studio in development mode:

```cmd
python main.py
```

### 4. Build Standalone VJStudio.exe (No Python Required)
Run the Windows PowerShell automated build script:

```powershell
.\build_windows.ps1
```

Or run the batch builder:

```cmd
build_exe.bat
```

Or manually via PyInstaller:

```cmd
pyinstaller --clean --noconfirm VJStudio.spec
```

The resulting standalone executable will be located in:
`dist\VJStudio.exe` and `dist\VJStudio\VJStudio.exe`

### 5. Build Setup Installer (VJStudio-Setup.exe)
With Inno Setup installed:

```cmd
build_installer.bat
```

---

## Running Unit Tests

```cmd
python -m pytest tests/
```

Or run standalone test scripts directly:

```cmd
python tests\test_config.py
python tests\test_paths.py
python tests\test_sources.py
python tests\test_scenes.py
python tests\test_program_pipeline.py
```
