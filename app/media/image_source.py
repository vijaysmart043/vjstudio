"""
Static image and graphic input source (PNG, JPG, WEBP).
"""

from pathlib import Path
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


class ImageSource(MediaSource):
    """Loads and renders static image graphics and overlays."""

    def __init__(
        self,
        file_path: Optional[Path] = None,
        name: Optional[str] = None,
        source_id: Optional[str] = None,
        width: int = 1920,
        height: int = 1080,
    ) -> None:
        file_path = Path(file_path) if file_path else None
        display_name = name or (file_path.name if file_path else "Image Graphic")
        super().__init__(name=display_name, source_type=SourceType.IMAGE, source_id=source_id, width=width, height=height)
        self.file_path = file_path
        self._cached_frame: Optional[VideoFrame] = None
        self._frame_count = 0

    def start(self) -> bool:
        self.is_active = True
        self._load_image()
        return True

    def stop(self) -> None:
        self.is_active = False
        self._cached_frame = None

    def _load_image(self) -> None:
        if HAS_OPENCV and self.file_path and self.file_path.exists():
            try:
                img = cv2.imread(str(self.file_path), cv2.IMREAD_COLOR)
                if img is not None:
                    if img.shape[1] != self.width or img.shape[0] != self.height:
                        img = cv2.resize(img, (self.width, self.height), interpolation=cv2.INTER_AREA)
                    self._cached_frame = VideoFrame(
                        width=self.width,
                        height=self.height,
                        data=img,
                        format="BGR",
                    )
                    return
            except Exception as e:
                logger.error(f"Failed to load image {self.file_path}: {e}")

        # Fallback card
        self._cached_frame = self._generate_image_card()

    def _generate_image_card(self) -> VideoFrame:
        w, h = self.width, self.height
        if HAS_OPENCV:
            img = np.zeros((h, w, 3), dtype=np.uint8)
            img[:, :] = (30, 30, 20)  # Dark teal
            cv2.putText(
                img,
                f"STILL GRAPHIC: {self.name}",
                (w // 4, h // 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.3,
                (255, 200, 50),
                2,
                cv2.LINE_AA,
            )
            return VideoFrame(width=w, height=h, data=img, format="BGR")
        return VideoFrame(width=w, height=h, data=None, format="NONE")

    def get_frame(self) -> Optional[VideoFrame]:
        if not self.is_active:
            return None
        self._frame_count += 1
        if self._cached_frame is None:
            self._load_image()
        return self._cached_frame
