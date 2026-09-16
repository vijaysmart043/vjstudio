"""
FFmpeg integration package for process control, binary detection, and hardware encoders.
"""

from app.ffmpeg.ffmpeg_manager import FFmpegManager, ffmpeg_manager
from app.ffmpeg.encoder import DEFAULT_ENCODERS, EncoderCapability
from app.ffmpeg.process import FFmpegProcess

__all__ = ["FFmpegManager", "ffmpeg_manager", "DEFAULT_ENCODERS", "EncoderCapability", "FFmpegProcess"]
