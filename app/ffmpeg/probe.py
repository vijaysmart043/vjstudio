"""
FFprobe wrapper to extract media metadata (resolution, fps, duration, audio channels).
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional
from app.core.logger import logger
from app.ffmpeg.ffmpeg_manager import ffmpeg_manager


def probe_file(file_path: Path) -> Optional[Dict[str, Any]]:
    """Inspects a media file using ffprobe and returns metadata."""
    if not ffmpeg_manager.ffprobe_path or not file_path.exists():
        return None

    try:
        cmd = [
            str(ffmpeg_manager.ffprobe_path),
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(file_path),
        ]
        res = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        return json.loads(res.stdout)
    except Exception as e:
        logger.warning(f"Failed to probe {file_path}: {e}")
        return None
