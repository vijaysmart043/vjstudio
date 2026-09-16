"""
Titles graphics module for customizable broadcast titles, banners, and typography cards.
"""

from typing import Any, Tuple
from app.graphics.overlay import BaseOverlay

try:
    import cv2
    import numpy as np
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False


class TitleOverlay(BaseOverlay):
    """Broadcast headline title banner with configurable font, size, position, and colors."""

    def __init__(
        self,
        name: str = "Studio Title",
        text: str = "VJ STUDIO BROADCAST",
        font_scale: float = 1.2,
        color: Tuple[int, int, int] = (255, 255, 255),
        thickness: int = 2,
    ) -> None:
        super().__init__(name)
        self.text = text
        self.font_scale = font_scale
        self.color = color
        self.thickness = thickness

    def render(self, canvas: Any) -> None:
        if not self.pos.visible or not HAS_OPENCV or canvas is None:
            return

        cv2.putText(
            canvas,
            self.text,
            (self.pos.x, self.pos.y),
            cv2.FONT_HERSHEY_DUPLEX,
            self.font_scale,
            self.color,
            self.thickness,
            cv2.LINE_AA,
        )
