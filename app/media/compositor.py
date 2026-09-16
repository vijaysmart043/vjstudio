"""
Multi-layer real-time video frame compositor.
"""

from typing import List, Optional
from app.core.logger import logger
from app.media.frame import VideoFrame
from app.media.media_source import MediaSource

try:
    import cv2
    import numpy as np
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False


class Compositor:
    """Combines background and multiple media layers into a unified output frame."""

    def __init__(self, width: int = 1920, height: int = 1080) -> None:
        self.width = width
        self.height = height
        self._blank_frame: Optional[np.ndarray] = None
        self._init_blank()

    def _init_blank(self) -> None:
        if HAS_OPENCV:
            self._blank_frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            # Subtle deep studio slate
            self._blank_frame[:, :] = (18, 16, 14)

    def compose(self, sources: List[MediaSource]) -> VideoFrame:
        """Compose all active and visible sources in layer order (bottom to top)."""
        if not HAS_OPENCV:
            return VideoFrame(width=self.width, height=self.height, data=None, format="NONE")

        # Start with fresh background canvas
        canvas = self._blank_frame.copy() if self._blank_frame is not None else np.zeros((self.height, self.width, 3), dtype=np.uint8)

        for source in sources:
            if not source.visible or not source.enabled:
                continue

            frame = source.get_frame()
            if frame is None or frame.data is None:
                continue

            layer_img = frame.data
            lh, lw = layer_img.shape[:2]

            # Scale if source transform requires it
            t = source.transform
            target_w = int(t.width * t.scale)
            target_h = int(t.height * t.scale)

            if target_w <= 0 or target_h <= 0:
                continue

            if lw != target_w or lh != target_h:
                layer_img = cv2.resize(layer_img, (target_w, target_h), interpolation=cv2.INTER_LINEAR)

            # Position offsets
            x, y = t.x, t.y

            # Bound calculations
            x1 = max(0, x)
            y1 = max(0, y)
            x2 = min(self.width, x + target_w)
            y2 = min(self.height, y + target_h)

            if x1 >= x2 or y1 >= y2:
                continue

            src_x1 = x1 - x
            src_y1 = y1 - y
            src_x2 = src_x1 + (x2 - x1)
            src_y2 = src_y1 + (y2 - y1)

            cropped_layer = layer_img[src_y1:src_y2, src_x1:src_x2]

            if t.opacity >= 0.99:
                canvas[y1:y2, x1:x2] = cropped_layer
            else:
                alpha = t.opacity
                canvas[y1:y2, x1:x2] = cv2.addWeighted(
                    canvas[y1:y2, x1:x2], 1.0 - alpha,
                    cropped_layer, alpha,
                    0,
                )

        return VideoFrame(width=self.width, height=self.height, data=canvas, format="BGR")
