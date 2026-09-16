# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller specification for VJ Studio Windows 10/11 64-bit standalone executable.
"""

import sys
import os
from pathlib import Path

block_cipher = None

project_root = Path(SPECPATH).resolve()

# Bundled data files (config, assets, ffmpeg)
datas = [
    (str(project_root / "config"), "config"),
]

# Include assets directory if present
assets_dir = project_root / "assets"
if assets_dir.exists():
    datas.append((str(assets_dir), "assets"))

# Include bundled ffmpeg if present
ffmpeg_bin = project_root / "ffmpeg" / "bin"
if ffmpeg_bin.exists():
    datas.append((str(ffmpeg_bin), "ffmpeg/bin"))

binaries = []

hidden_imports = [
    "PySide6.QtCore",
    "PySide6.QtGui",
    "PySide6.QtWidgets",
    "cv2",
    "numpy",
    "PIL",
    "PIL.ImageGrab",
    "psutil",
    "sqlite3",
    "dataclasses_json",
    "app.audio.audio_mixer",
    "app.commands.command_bus",
    "app.core.constants",
    "app.core.events",
    "app.core.logger",
    "app.core.paths",
    "app.core.settings",
    "app.ffmpeg.ffmpeg_manager",
    "app.ffmpeg.ffmpeg_process",
    "app.media.camera",
    "app.media.camera_manager",
    "app.media.compositor",
    "app.media.frame",
    "app.media.image_source",
    "app.media.media_source",
    "app.media.ndi_source",
    "app.media.network_stream_source",
    "app.media.renderer",
    "app.media.screen_capture",
    "app.media.video_source",
    "app.production.input_manager",
    "app.production.preview_output",
    "app.production.program_output",
    "app.production.scene",
    "app.production.scene_manager",
    "app.production.transition_manager",
    "app.recording.recorder",
    "app.recording.recording_config",
    "app.storage.project_repository",
    "app.storage.sqlite_db",
    "app.streaming.rtmp",
    "app.streaming.srt",
    "app.streaming.stream_config",
    "app.streaming.streamer",
    "app.ui.main_window",
    "app.ui.multiview_window",
    "app.ui.theme",
]

a = Analysis(
    [str(project_root / "main.py")],
    pathex=[str(project_root)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "matplotlib", "scipy"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="VJStudio",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Windows GUI application (no console window)
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="VJStudio",
)
