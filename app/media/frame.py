"""
VideoFrame encapsulation for consistent inter-subsystem data flow.
"""

import time
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class VideoFrame:
    """Represents a single video frame with timestamp and dimension metadata."""
    width: int
    height: int
    data: Any  # numpy.ndarray (RGB/BGR/RGBA) or QImage
    format: str = "BGR"  # BGR, RGB, RGBA
    timestamp: float = field(default_factory=time.time)
    frame_number: int = 0

    @property
    def is_valid(self) -> bool:
        return self.data is not None and self.width > 0 and self.height > 0
