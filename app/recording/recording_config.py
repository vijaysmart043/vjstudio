"""
Recording configuration and output format presets.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class RecordingProfile:
    output_dir: Path
    format: str = "mp4"  # mp4 or mkv
    video_bitrate_kbps: int = 8000
    audio_bitrate_kbps: int = 192
    fps: int = 30
    width: int = 1920
    height: int = 1080
    encoder: str = "auto"
