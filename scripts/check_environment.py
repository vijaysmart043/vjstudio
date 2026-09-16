"""
Environment verification script checking Python version, required modules, and FFmpeg.
"""

import sys
import os
import shutil

print("=== VJ STUDIO ENVIRONMENT CHECK ===")
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

REQUIRED_MODULES = [
    ("PySide6", "Qt GUI Framework"),
    ("cv2", "OpenCV Video Processing"),
    ("numpy", "Numerical Array Processing"),
    ("PIL", "Pillow Image Processing"),
    ("psutil", "System Performance Telemetry"),
]

all_passed = True
for mod_name, desc in REQUIRED_MODULES:
    try:
        __import__(mod_name)
        print(f"  [OK] {mod_name:12} — {desc}")
    except ImportError:
        print(f"  [MISSING] {mod_name:12} — {desc}")
        all_passed = False

# FFmpeg check
ffmpeg_path = shutil.which("ffmpeg")
if ffmpeg_path:
    print(f"  [OK] FFmpeg found in PATH: {ffmpeg_path}")
else:
    print("  [INFO] FFmpeg not found in system PATH (You can place binaries in ffmpeg/bin/)")

if all_passed:
    print("\nEnvironment is READY for VJ Studio!")
else:
    print("\nPlease install missing requirements: pip install -r requirements.txt")
