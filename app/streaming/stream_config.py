"""
Streaming connection parameters and encoder settings.
"""

from dataclasses import dataclass


@dataclass
class StreamProfile:
    server_url: str = "rtmp://live.example.com/app"
    stream_key: str = ""
    video_bitrate_kbps: int = 4500
    audio_bitrate_kbps: int = 160
    fps: int = 30
    width: int = 1920
    height: int = 1080
    keyframe_interval: int = 2
    encoder: str = "auto"
