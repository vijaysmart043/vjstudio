"""
Stream health monitoring: bitrate, frame drops, network jitter, and connection reliability.
"""

from dataclasses import dataclass
from app.core.constants import StreamState


@dataclass
class StreamHealthStats:
    state: StreamState = StreamState.OFFLINE
    bitrate_kbps: int = 0
    fps: float = 60.0
    dropped_frames: int = 0
    total_frames: int = 0
    cpu_usage_pct: float = 0.0
    uptime_seconds: int = 0

    @property
    def drop_rate_pct(self) -> float:
        if self.total_frames <= 0:
            return 0.0
        return (self.dropped_frames / self.total_frames) * 100.0

    @property
    def health_rating(self) -> str:
        if self.state != StreamState.LIVE:
            return "STANDBY"
        if self.drop_rate_pct > 5.0:
            return "POOR"
        if self.drop_rate_pct > 1.0:
            return "FAIR"
        return "EXCELLENT"
