"""
Secure Reliable Transport (SRT) streaming service interface.
"""

from typing import Optional
from app.core.constants import StreamState
from app.core.logger import logger


class SRTStreamer:
    """SRT transmission interface with safe dependency validation."""

    def __init__(self) -> None:
        self.state: StreamState = StreamState.STOPPED

    def is_supported(self) -> bool:
        """Returns True if libsrt is compiled into FFmpeg."""
        # Clean service query
        return False

    def start(self, srt_url: str, passphrase: Optional[str] = None) -> bool:
        logger.info(f"SRT Service Interface invoked for: {srt_url} (Phase 1 Stub)")
        return False

    def stop(self) -> None:
        self.state = StreamState.STOPPED
