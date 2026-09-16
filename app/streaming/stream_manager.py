"""
Stream manager module forwarding to streaming coordinator and stream health.
"""

from app.streaming.streamer import StreamingCoordinator, streaming_coordinator as stream_manager
from app.streaming.stream_health import StreamHealthStats
from app.streaming.rtmp import RTMPStreamer
from app.streaming.srt import SRTStreamer
from app.streaming.stream_config import StreamProfile

__all__ = [
    "StreamingCoordinator",
    "stream_manager",
    "StreamHealthStats",
    "RTMPStreamer",
    "SRTStreamer",
    "StreamProfile",
]
