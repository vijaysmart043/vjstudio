"""
Ticker graphics module with high-speed looping crawl ticker.
"""

from typing import Any
from app.graphics.overlay import BaseOverlay

try:
    import cv2
    import numpy as np
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False


class Ticker(BaseOverlay):
    """Dynamic scrolling horizontal news and telemetry crawler."""

    def __init__(
        self,
        name: str = "Broadcast Ticker",
        badge: str = "BREAKING",
        text: str = "LIVE PRODUCTION POWERED BY VJ STUDIO — PROFESSIONAL WINDOWS BROADCAST PLATFORM",
        speed: int = 4,
    ) -> None:
        super().__init__(name)
        self.badge = badge
        self.text = text
        self.speed = speed
        self._offset = 0

    def render(self, canvas: Any) -> None:
        if not self.pos.visible or not HAS_OPENCV or canvas is None:
            return

        h, w = canvas.shape[:2]
        bar_h = 36
        y1 = h - bar_h

        # Crawler background strip
        cv2.rectangle(canvas, (0, y1), (w, h), (14, 16, 22), -1)
        # Category indicator badge
        badge_w = 110
        cv2.rectangle(canvas, (0, y1), (badge_w, h), (0, 36, 196), -1)
        cv2.putText(canvas, self.badge, (12, y1 + 24), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

        # Scrolling text
        self._offset = (self._offset + self.speed) % (w + 1400)
        draw_x = w - self._offset
        cv2.putText(canvas, self.text, (draw_x, y1 + 24), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (230, 230, 230), 1, cv2.LINE_AA)
