# VJ STUDIO — PROJECT STATUS
**Target Architecture: Windows 10/11 64-bit Desktop Application (`VJStudio.exe`)**
**Language & Engine: Python 3.12+ / PySide6 / OpenCV / FFmpeg / NDI**

---

## Current Status: PRODUCTION READY ARCHITECTURE (Desktop Live Production & Streaming)

### Status Overview
- **Platform**: Windows 10/11 x64 Desktop / Laptop
- **Build Executable**: `dist/VJStudio.exe` (PyInstaller 64-bit bundle)
- **Mobile/Android Artifacts**: **100% PURGED** (No Android, Kotlin, Gradle, APK, AAB, or mobile SDKs)
- **Automated Tests**: 100% Passing (`test_config`, `test_paths`, `test_sources`, `test_scenes`, `test_program_pipeline`, `test_windows_desktop`)

---

### Implemented Architecture Components

1. **Core Application (`app/core/`)**:
   - `application.py`: `VJStudioApplication` desktop lifecycle, directory initialization, and PySide6 Qt GUI loop
   - `config.py`: Broadcast configuration schema with `%APPDATA%` overrides
   - `constants.py`: Broadcast frame rates, resolutions, `SourceType`, `TransitionType`, `StreamState`, `RecordState`
   - `logger.py`: Thread-safe rotating logger with stream-key credential redaction
   - `events.py`: Decoupled `EventBus` for studio telemetry and state distribution
   - `exceptions.py`: Specific domain exceptions (`DeviceError`, `FFmpegError`, `StreamError`, `RecordingError`, `NDIError`, `VirtualCameraError`)
   - `paths.py`: Windows `%APPDATA%` and PyInstaller `_MEIPASS` dynamic resolution

2. **Desktop Broadcast Workspace (`app/ui/`)**:
   - `main_window.py`: Primary Windows production window with menu bar, dual Preview/Program monitors, transition controls (CUT, AUTO FADE, DISSOLVE, T-Bar), scene deck, input card grid, 4-channel audio mixer, output deck, and status bar
   - `multiview_window.py` & `multiview.py`: Standalone auxiliary monitor window (`View -> Open Multiview Window [F11]`) supporting multi-channel matrices (Preview, Program, cameras, NDI, screen capture)
   - `theme.py`: High-contrast dark broadcast theme (#0E1014 canvas, #1D212A cards, emerald green Preview tally, ruby red Program LIVE tally)

3. **Media Sources & Pipeline (`app/media/`)**:
   - `media_source.py`: Base abstract class with 2D transform, scaling, opacity, and audio hooks
   - `camera.py` & `camera_manager.py`: Windows DirectShow webcam & USB capture card ingestion with SMPTE color bar standby fallback
   - `screen_capture.py`: Windows desktop display and window capture
   - `video_source.py`: Local MP4, MKV, MOV, AVI, WebM media playback with transport controls
   - `image_source.py`: Graphic overlays (PNG, JPG, BMP, WebP) with alpha channel transparency
   - `compositor.py`: Multi-layer compositing engine with Z-indexing

4. **Production Switching (`app/production/`)**:
   - `program_output.py`: Canonical unified ProgramOutput pipeline feeding UI, Recording, RTMP, SRT, NDI, and Virtual Camera
   - `preview_output.py`: Isolated cue bus for Preview monitor
   - `scene.py` & `scene_manager.py`: Multi-layer broadcast scene presets
   - `transition_manager.py` & `transition.py`: CUT, cross-fade, and manual T-Bar blending

5. **Broadcast Audio (`app/audio/`)**:
   - `audio_mixer.py`: 4-channel console (`MIC 1`, `MIC 2`, `SYSTEM`, `MASTER`)
   - `audio_source.py`: Audio channels with volume, gain (-20 to +20 dB), pan, and mute
   - `audio_meter.py`: Dual stereo peak LED dB meters
   - `effects.py`: Live DSP processing architecture (Compressor, Limiter, 3-Band EQ, Noise Gate)

6. **Graphics & Studio Sets (`app/graphics/`)**:
   - `title.py`: Customizable studio title cards
   - `lower_third.py`: Presenter and guest lower-third banners with neon accent bars
   - `ticker.py`: Real-time horizontal scrolling news crawl ticker
   - `templates.py`: Multi-layer virtual studio environments (News, Sports, Podcast, Tech, Corporate, Weather)

7. **NDI Integration (`app/ndi/`)**:
   - `ndi_manager.py`: NDI SDK runtime discovery of network sources
   - `ndi_source.py`: Video and audio network ingest from NDI transmitters
   - `ndi_output.py`: Broadcast transmission of the canonical ProgramOutput stream

8. **Virtual Camera (`app/virtual_camera/`)**:
   - `windows_backend.py`: DirectShow / pyvirtualcam camera emulation driver backend
   - `camera_manager.py`: ProgramOutput pipeline consumer hook making live production visible to Zoom, Teams, OBS, Discord, and Meet

9. **FFmpeg & Hardware Encoders (`app/ffmpeg/`)**:
   - `ffmpeg_manager.py`: Diagnostic detection of local/bundled FFmpeg binaries and GPU encoders (NVENC, QuickSync, AMF, libx264)
   - `ffmpeg_process.py`: Subprocess management with stdin pipe control and clean shutdown

10. **Streaming & Recording (`app/streaming/`, `app/recording/`)**:
    - `streamer.py` & `stream_manager.py`: Multi-destination coordinator for RTMP and low-latency SRT
    - `stream_health.py`: Telemetry tracking bitrate, FPS, and dropped frame percentages
    - `recorder.py` & `recording_manager.py`: Local disk recorder with timestamped filenames (`VJStudio_YYYY-MM-DD_HH-MM-SS.mp4`)

11. **Local Storage (`app/storage/`)**:
    - `database.py`: SQLite storage for session logs and presets
    - `project_repository.py` & `projects.py`: Project file (.vjstudio) serialization and loading

12. **Packaging & Builders**:
    - `build_windows.ps1`: Automated PowerShell workflow (.venv, requirements, test suite, PyInstaller, dist validation)
    - `build_windows.bat` & `build_exe.bat`: One-click Windows CMD builders
    - `VJStudio.spec`: PyInstaller specification building 64-bit Windows executable
