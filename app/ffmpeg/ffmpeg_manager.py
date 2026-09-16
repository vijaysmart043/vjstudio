"""
FFmpeg discovery, diagnostic probing, and encoder capability reporting.
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from app.core.paths import paths
from app.core.logger import logger
from app.ffmpeg.encoder import DEFAULT_ENCODERS, EncoderCapability


class FFmpegManager:
    """Detects and validates local and bundled FFmpeg and ffprobe binaries."""

    _instance: Optional["FFmpegManager"] = None

    def __init__(self) -> None:
        self.ffmpeg_path: Optional[Path] = None
        self.ffprobe_path: Optional[Path] = None
        self.version_info: str = "Unknown"
        self.available_encoders: Dict[str, bool] = {}
        self.initialized = False
        self.detect()

    @classmethod
    def get_instance(cls) -> "FFmpegManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def detect(self, custom_path: Optional[str] = None) -> bool:
        """Search for ffmpeg binaries across bundle, custom path, and system PATH."""
        search_locations: List[Path] = []

        # 1. User custom path if provided
        if custom_path and os.path.isdir(custom_path):
            search_locations.append(Path(custom_path))

        # 2. Bundled FFmpeg directory
        search_locations.append(paths.bundled_ffmpeg_bin)
        search_locations.append(paths.app_dir / "ffmpeg" / "bin")
        search_locations.append(paths.app_dir / "bin")

        # Check search locations for ffmpeg.exe (Windows) or ffmpeg (POSIX)
        exe_ext = ".exe" if os.name == "nt" else ""
        for loc in search_locations:
            candidate_ffmpeg = loc / f"ffmpeg{exe_ext}"
            candidate_ffprobe = loc / f"ffprobe{exe_ext}"
            if candidate_ffmpeg.exists():
                self.ffmpeg_path = candidate_ffmpeg
                if candidate_ffprobe.exists():
                    self.ffprobe_path = candidate_ffprobe
                break

        # 3. Fall back to system PATH
        if not self.ffmpeg_path:
            system_ffmpeg = shutil.which("ffmpeg")
            if system_ffmpeg:
                self.ffmpeg_path = Path(system_ffmpeg)
            system_ffprobe = shutil.which("ffprobe")
            if system_ffprobe:
                self.ffprobe_path = Path(system_ffprobe)

        if self.ffmpeg_path:
            self._probe_version_and_encoders()
            self.initialized = True
            logger.info(f"FFmpeg located at: {self.ffmpeg_path} (Version: {self.version_info})")
            return True
        else:
            logger.warning("FFmpeg binary not detected on system or in bundle.")
            self.initialized = False
            return False

    def _probe_version_and_encoders(self) -> None:
        """Query FFmpeg for version and compiled encoder support."""
        if not self.ffmpeg_path:
            return

        # 1. Probe version
        try:
            cmd = [str(self.ffmpeg_path), "-version"]
            res = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )
            first_line = res.stdout.splitlines()[0] if res.stdout else "Unknown"
            self.version_info = first_line.replace("ffmpeg version", "").strip()
        except Exception as e:
            logger.warning(f"Failed to query FFmpeg version: {e}")
            self.version_info = "Detected (Unversioned)"

        # 2. Probe encoders
        try:
            cmd = [str(self.ffmpeg_path), "-encoders"]
            res = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )
            output = res.stdout
            self.available_encoders["libx264"] = "libx264" in output
            self.available_encoders["h264_nvenc"] = "h264_nvenc" in output
            self.available_encoders["h264_qsv"] = "h264_qsv" in output
            self.available_encoders["h264_amf"] = "h264_amf" in output
            self.available_encoders["aac"] = "aac" in output
        except Exception as e:
            logger.warning(f"Failed to query FFmpeg encoders: {e}")
            # Fallback assumption
            self.available_encoders["libx264"] = True

    @property
    def is_available(self) -> bool:
        return self.ffmpeg_path is not None

    def get_diagnostics(self) -> Dict[str, str]:
        """Produce human-readable broadcast diagnostics."""
        diag = {
            "FFmpeg Status": "Available" if self.ffmpeg_path else "Not Found",
            "FFmpeg Path": str(self.ffmpeg_path) if self.ffmpeg_path else "N/A",
            "FFprobe Status": "Available" if self.ffprobe_path else "Not Found",
            "Version": self.version_info,
            "H.264 (libx264)": "Available" if self.available_encoders.get("libx264") else "Unavailable",
            "NVIDIA NVENC": "Available" if self.available_encoders.get("h264_nvenc") else "Unavailable",
            "Intel QuickSync": "Available" if self.available_encoders.get("h264_qsv") else "Unavailable",
            "AMD AMF": "Available" if self.available_encoders.get("h264_amf") else "Unavailable",
        }
        return diag

    def get_best_h264_encoder(self) -> str:
        """Select highest performance hardware encoder, falling back to libx264."""
        if self.available_encoders.get("h264_nvenc"):
            return "h264_nvenc"
        if self.available_encoders.get("h264_qsv"):
            return "h264_qsv"
        if self.available_encoders.get("h264_amf"):
            return "h264_amf"
        return "libx264"


ffmpeg_manager = FFmpegManager.get_instance()
