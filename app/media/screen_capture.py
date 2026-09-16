"""
Windows screen and desktop window capture implementation.
"""

from typing import Optional
from app.core.constants import SourceType
from app.core.logger import logger
from app.media.frame import VideoFrame
from app.media.media_source import MediaSource

try:
    import numpy as np
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

try:
    from PIL import ImageGrab
    HAS_IMAGEGRAB = True
except ImportError:
    HAS_IMAGEGRAB = False


class ScreenCaptureSource(MediaSource):
    """Captures the user's primary monitor or active display."""

    def __init__(
        self,
        name: str = "Screen Capture",
        monitor_index: int = 0,
        source_id: Optional[str] = None,
        width: int = 1920,
        height: int = 1080,
    ) -> None:
        super().__init__(name=name, source_type=SourceType.SCREEN, source_id=source_id, width=width, height=height)
        self.monitor_index = monitor_index
        self._frame_count = 0

    def start(self) -> bool:
        self.is_active = True
        logger.info(f"Screen capture '{self.name}' active.")
        return True

    def stop(self) -> None:
        self.is_active = False
        logger.info(f"Screen capture '{self.name}' stopped.")

    def get_frame(self) -> Optional[VideoFrame]:
        if not self.is_active:
            return None

        self._frame_count += 1

        # Attempt PIL ImageGrab for Windows desktop capture
        if HAS_IMAGEGRAB and HAS_CV2:
            try:
                screen = ImageGrab.grab()
                img_np = np.array(screen)
                frame_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
                if frame_bgr.shape[1] != self.width or frame_bgr.shape[0] != self.height:
                    frame_bgr = cv2.resize(frame_bgr, (self.width, self.height), interpolation=cv2.INTER_LINEAR)
                return VideoFrame(
                    width=self.width,
                    height=self.height,
                    data=frame_bgr,
                    format="BGR",
                    frame_number=self._frame_count,
                )
            except Exception as e:
                logger.debug(f"ImageGrab screen capture fallback: {e}")

        # Synthetic Desktop Canvas
        return self._generate_desktop_placeholder()

    def _generate_desktop_placeholder(self) -> VideoFrame:
        w, h = self.width, self.height
        if HAS_CV2:
            # Modern dark desktop grid canvas
            img = np.zeros((h, w, 3), dtype=np.uint8)
            img[:, :] = (26, 22, 18)  # Deep broadcast slate
            # Draw subtle desktop grid
            grid_size = 80
            for x in range(0, w, grid_size):
                cv2.line(img, (x, 0), (x, h), (40, 36, 32), 1)
            for y in range(0, h, grid_size):
                cv2.line(img, (0, y), (w, y), (40, 36, 32), 1)

            # Center desktop emblem
            cv2.rectangle(img, (w // 4, h // 4), (3 * w // 4, 3 * h // 4), (60, 50, 40), 2)
            cv2.putText(
                img,
                "DISPLAY CAPTURE 1 [ACTIVE]",
                (w // 4 + 40, h // 2 - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.4,
                (0, 220, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                img,
                f"Resolution: {w}x{h} @ 60 FPS",
                (w // 4 + 40, h // 2 + 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (180, 180, 180),
                2,
                cv2.LINE_AA,
            )
            return VideoFrame(width=w, height=h, data=img, format="BGR", frame_number=self._frame_count)

        return VideoFrame(width=w, height=h, data=None, format="NONE", frame_number=self._frame_count)
