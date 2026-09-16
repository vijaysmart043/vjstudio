"""
Utility script to assist with acquiring FFmpeg binaries for Windows distribution.
"""

import sys
from pathlib import Path

FFMPEG_DIR = Path(__file__).resolve().parent.parent / "ffmpeg" / "bin"


def main():
    print("=== FFmpeg Setup Helper for VJ Studio ===")
    print(f"Target bundled binary directory: {FFMPEG_DIR}")
    FFMPEG_DIR.mkdir(parents=True, exist_ok=True)
    print("\nTo bundle FFmpeg with VJ Studio:")
    print("1. Download FFmpeg Essentials build for Windows from: https://www.gyan.dev/ffmpeg/builds/")
    print(f"2. Extract 'ffmpeg.exe' and 'ffprobe.exe' into:\n   {FFMPEG_DIR}")
    print("3. VJ Studio and PyInstaller will automatically detect and bundle these binaries!")


if __name__ == "__main__":
    main()
