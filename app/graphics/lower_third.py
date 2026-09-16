"""
Lower Third graphics module with professional animated/static presenter badges.
"""

from typing import Any, Tuple
from app.graphics.overlay import BaseOverlay

try:
    import cv2
    import numpy as np
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False


class LowerThird(BaseOverlay):
    """Lower-third graphic card for guest and presenter identification."""

    def __init__(
        self,
        name: str = "Lower Third",
        title: str = "ALEX CARTER",
        role: str = "Broadcast Technical Director",
        accent_color: Tuple[int, int, int] = (0, 165, 255),
    ) -> None:
        super().__init__(name)
        self.title = title
        self.role = role
        self.accent_color = accent_color

    def render(self, canvas: Any) -> None:
        if not self.pos.visible or not HAS_OPENCV or canvas is None:
            return

        h, w = canvas.shape[:2]
        x1, y1 = 70, h - 130
        x2, y2 = min(w - 70, 680), h - 50

        # Card backdrop with soft alpha tint
        sub = canvas[y1:y2, x1:x2]
        bg = np.zeros_like(sub)
        bg[:, :] = (18, 20, 26)
        cv2.addWeighted(sub, 0.15, bg, 0.85, 0, sub)
        canvas[y1:y2, x1:x2] = sub

        # Left neon accent bar
        cv2.rectangle(canvas, (x1, y1), (x1 + 6, y2), self.accent_color, -1)

        # Typography
        cv2.putText(canvas, self.title, (x1 + 20, y1 + 32), cv2.FONT_HERSHEY_DUPLEX, 0.85, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(canvas, self.role, (x1 + 20, y1 + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (190, 195, 205), 1, cv2.LINE_AA)
