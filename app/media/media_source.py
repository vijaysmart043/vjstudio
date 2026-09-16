"""
Base abstract class for all media inputs in VJ Studio.
"""

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Tuple
from app.core.constants import SourceType
from app.media.frame import VideoFrame


@dataclass
class SourceTransform:
    x: int = 0
    y: int = 0
    width: int = 1920
    height: int = 1080
    scale: float = 1.0
    opacity: float = 1.0
    rotation: float = 0.0


class MediaSource(ABC):
    """Abstract base class representing an active or standby media input."""

    def __init__(
        self,
        name: str,
        source_type: SourceType,
        source_id: Optional[str] = None,
        width: int = 1920,
        height: int = 1080,
    ) -> None:
        self.id = source_id or str(uuid.uuid4())[:8]
        self.name = name
        self.type = source_type
        self.width = width
        self.height = height
        self.transform = SourceTransform(width=width, height=height)
        self.visible = True
        self.enabled = True
        self.audio_enabled = False
        self.is_active = False

    @abstractmethod
    def start(self) -> bool:
        """Initialize and start streaming frames from this source."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Release underlying hardware or file resources cleanly."""
        pass

    @abstractmethod
    def get_frame(self) -> Optional[VideoFrame]:
        """Fetch the latest available frame for composition."""
        pass

    def set_position(self, x: int, y: int) -> None:
        self.transform.x = x
        self.transform.y = y

    def set_size(self, width: int, height: int) -> None:
        self.transform.width = width
        self.transform.height = height

    def set_opacity(self, opacity: float) -> None:
        self.transform.opacity = max(0.0, min(1.0, opacity))

    def set_visibility(self, visible: bool) -> None:
        self.visible = visible

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id='{self.id}' name='{self.name}' type='{self.type.value}'>"
