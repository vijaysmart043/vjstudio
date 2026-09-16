"""
Camera capture implementation with hardware safety and test pattern fallbacks.
"""

import math
import time
from typing import Optional
from app.core.constants import SourceType
from app.core.logger import logger
from app.media.frame import VideoFrame
from app.media.media_source import MediaSource

try:
    import cv2
    import numpy as np
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False


class CameraSource(MediaSource):
    """Hardware camera capture source using OpenCV VideoCapture."""

    def __init__(
        self,
        name: str = "Camera",
        device_index: int = 0,
        source_id: Optional[str] = None,
        width: int = 1280,
        height: int = 720,
        fps: int = 30,
    ) -> None:
        super().__init__(name=name, source_type=SourceType.CAMERA, source_id=source_id, width=width, height=height)
        self.device_index = device_index
        self.fps = fps
        self._capture = None
        self._last_frame: Optional[VideoFrame] = None
        self._frame_count = 0
        self.audio_enabled = True

    def start(self) -> bool:
        if self.is_active:
            return True

        if HAS_OPENCV:
            try:
                # DirectShow backend on Windows (cv2.CAP_DSHOW) provides fast startup
                backend = cv2.CAP_DSHOW if hasattr(cv2, "CAP_DSHOW") else cv2.CAP_ANY
                self._capture = cv2.VideoCapture(self.device_index, backend)
                if self._capture.isOpened():
                    self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                    self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                    self._capture.set(cv2.CAP_PROP_FPS, self.fps)
                    self.is_active = True
                    logger.info(f"Camera '{self.name}' (index {self.device_index}) started.")
                    return True
                else:
                    logger.warning(f"Camera index {self.device_index} could not be opened, using broadcast test pattern.")
            except Exception as e:
                logger.error(f"Error initializing camera {self.device_index}: {e}")

        # Fallback to test pattern mode (safe broadcast standby)
        self.is_active = True
        return True

    def stop(self) -> None:
        self.is_active = False
        if self._capture is not None:
            try:
                self._capture.release()
            except Exception as e:
                logger.warning(f"Error releasing camera: {e}")
            self._capture = None
        logger.info(f"Camera '{self.name}' stopped.")

    def get_frame(self) -> Optional[VideoFrame]:
        if not self.is_active:
            return None

        self._frame_count += 1

        # Real OpenCV capture if open
        if self._capture is not None and self._capture.isOpened():
            ret, frame = self._capture.read()
            if ret and frame is not None:
                self._last_frame = VideoFrame(
                    width=frame.shape[1],
                    height=frame.shape[0],
                    data=frame,
                    format="BGR",
                    frame_number=self._frame_count,
                )
                return self._last_frame

        # Standby test generator (SMPTE color bars with moving sync indicator)
        return self._generate_test_pattern()

    def _generate_test_pattern(self) -> VideoFrame:
        """Generates broadcast test pattern when camera is unavailable or disconnected."""
        w, h = self.width, self.height
        if HAS_OPENCV:
            # Generate 7-bar SMPTE pattern
            colors = [
                (180, 180, 180),  # Gray
                (0, 200, 200),    # Yellow
                (200, 200, 0),    # Cyan
                (0, 200, 0),      # Green
                (200, 0, 200),    # Magenta
                (0, 0, 200),      # Red
                (200, 0, 0),      # Blue
            ]
            bar_w = w // len(colors)
            img = np.zeros((h, w, 3), dtype=np.uint8)
            for i, col in enumerate(colors):
                x1 = i * bar_w
                x2 = w if i == len(colors) - 1 else (i + 1) * bar_w
                img[:, x1:x2] = col

            # Moving sync line
            pos = int((math.sin(self._frame_count * 0.05) + 1.0) * 0.5 * (w - 40)) + 20
            cv2.line(img, (pos, 0), (pos, h), (255, 255, 255), 4)

            # Overlay Label
            cv2.putText(
                img,
                f"{self.name} [STANDBY]",
                (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            return VideoFrame(width=w, height=h, data=img, format="BGR", frame_number=self._frame_count)

        return VideoFrame(width=w, height=h, data=None, format="NONE", frame_number=self._frame_count)
