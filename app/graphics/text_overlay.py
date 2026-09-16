"""
Broadcast text overlays, lower-thirds, tickers, clocks, and graphic badges.
"""

import datetime
from typing import Any
from app.graphics.overlay import BaseOverlay

try:
    import cv2
    import numpy as np
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False


class TextOverlay(BaseOverlay):
    """Customizable on-screen text banner."""

    def __init__(self, name: str = "Text Overlay", text: str = "VJ STUDIO LIVE") -> None:
        super().__init__(name)
        self.text = text
        self.font_scale = 1.0
        self.color = (255, 255, 255)
        self.thickness = 2

    def render(self, canvas: Any) -> None:
        if not self.pos.visible or not HAS_OPENCV or canvas is None:
            return
        cv2.putText(
            canvas,
            self.text,
            (self.pos.x, self.pos.y),
            cv2.FONT_HERSHEY_SIMPLEX,
            self.font_scale,
            self.color,
            self.thickness,
            cv2.LINE_AA,
        )


class LowerThirdOverlay(BaseOverlay):
    """Professional lower-third graphic banner displaying speaker name and title."""

    def __init__(self, name: str = "Lower Third", title: str = "ALEX CARTER", subtitle: str = "Lead Broadcast Engineer") -> None:
        super().__init__(name)
        self.title = title
        self.subtitle = subtitle
        self.accent_color = (0, 160, 255)  # Amber / Blue broadcast accent

    def render(self, canvas: Any) -> None:
        if not self.pos.visible or not HAS_OPENCV or canvas is None:
            return

        h, w = canvas.shape[:2]
        x1, y1 = 80, h - 140
        x2, y2 = 640, h - 60

        # Semi-transparent dark background card
        sub = canvas[y1:y2, x1:x2]
        bg = np.zeros_like(sub)
        bg[:, :] = (20, 20, 24)
        cv2.addWeighted(sub, 0.2, bg, 0.8, 0, sub)
        canvas[y1:y2, x1:x2] = sub

        # Neon accent bar on left
        cv2.rectangle(canvas, (x1, y1), (x1 + 6, y2), self.accent_color, -1)

        # Title and subtitle text
        cv2.putText(canvas, self.title, (x1 + 24, y1 + 34), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(canvas, self.subtitle, (x1 + 24, y1 + 62), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1, cv2.LINE_AA)


class TickerOverlay(BaseOverlay):
    """Horizontal scrolling news/info ticker."""

    def __init__(self, name: str = "Ticker", text: str = "BREAKING NEWS: LIVE BROADCAST PRODUCTION POWERED BY VJ STUDIO") -> None:
        super().__init__(name)
        self.text = text
        self.offset = 0
        self.speed = 3

    def render(self, canvas: Any) -> None:
        if not self.pos.visible or not HAS_OPENCV or canvas is None:
            return
        h, w = canvas.shape[:2]
        bar_h = 36
        y1 = h - bar_h

        # Banner strip
        cv2.rectangle(canvas, (0, y1), (w, h), (16, 16, 20), -1)
        cv2.rectangle(canvas, (0, y1), (100, h), (0, 50, 200), -1)
        cv2.putText(canvas, "NEWS", (15, y1 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2, cv2.LINE_AA)

        # Scrolling text
        self.offset = (self.offset + self.speed) % (w + 1200)
        draw_x = w - self.offset
        cv2.putText(canvas, self.text, (draw_x, y1 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (220, 220, 220), 1, cv2.LINE_AA)


class ClockOverlay(BaseOverlay):
    """On-screen broadcast clock."""

    def __init__(self, name: str = "Clock", is_24hr: bool = True) -> None:
        super().__init__(name)
        self.is_24hr = is_24hr

    def render(self, canvas: Any) -> None:
        if not self.pos.visible or not HAS_OPENCV or canvas is None:
            return

        fmt = "%H:%M:%S" if self.is_24hr else "%I:%M:%S %p"
        time_str = datetime.datetime.now().strftime(fmt)

        h, w = canvas.shape[:2]
        x = w - 180
        y = 50

        # Background badge
        cv2.rectangle(canvas, (x - 10, y - 30), (x + 160, y + 10), (20, 20, 24), -1)
        cv2.putText(canvas, time_str, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 230, 118), 2, cv2.LINE_AA)
