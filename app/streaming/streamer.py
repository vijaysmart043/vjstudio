"""
High-level stream coordinator managing RTMP and SRT broadcast engines.
"""

from typing import Optional
from app.core.constants import StreamState
from app.core.logger import logger
from app.streaming.rtmp import RTMPStreamer
from app.streaming.srt import SRTStreamer
from app.streaming.stream_config import StreamProfile


class StreamingCoordinator:
    """Singleton coordinating all outbound streaming destinations."""

    _instance = None

    def __init__(self) -> None:
        self.rtmp = RTMPStreamer()
        self.srt = SRTStreamer()
        self.dropped_frames: int = 0
        self.bitrate_kbps: int = 0

    @classmethod
    def get_instance(cls) -> "StreamingCoordinator":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def state(self) -> StreamState:
        return self.rtmp.state

    def start_stream(self, profile: StreamProfile) -> bool:
        self.dropped_frames = 0
        self.bitrate_kbps = profile.video_bitrate_kbps
        return self.rtmp.start(profile)

    def stop_stream(self) -> None:
        self.rtmp.stop()
        self.bitrate_kbps = 0


streaming_coordinator = StreamingCoordinator.get_instance()
