"""
Video file playback source with playback controls and loop support.
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


class VideoSource(MediaSource):
    """Plays back pre-recorded video media clips."""

    def __init__(
        self,
        file_path: Path,
        name: Optional[str] = None,
        source_id: Optional[str] = None,
        loop: bool = True,
        width: int = 1920,
        height: int = 1080,
    ) -> None:
        file_path = Path(file_path)
        display_name = name or file_path.name
        super().__init__(name=display_name, source_type=SourceType.VIDEO, source_id=source_id, width=width, height=height)
        self.file_path = file_path
        self.loop = loop
        self.is_playing = True
        self.volume = 1.0
        self.audio_enabled = True
        self._capture = None
        self._frame_count = 0

    def start(self) -> bool:
        if self.is_active:
            return True

        if HAS_OPENCV and self.file_path.exists():
            try:
                self._capture = cv2.VideoCapture(str(self.file_path))
                if self._capture.isOpened():
                    self.is_active = True
                    self.is_playing = True
                    logger.info(f"Video '{self.name}' opened: {self.file_path}")
                    return True
            except Exception as e:
                logger.error(f"Failed to open video file {self.file_path}: {e}")

        # Active placeholder
        self.is_active = True
        return True

    def stop(self) -> None:
        self.is_active = False
        self.is_playing = False
        if self._capture is not None:
            self._capture.release()
            self._capture = None
        logger.info(f"Video '{self.name}' stopped.")

    def play(self) -> None:
        self.is_playing = True

    def pause(self) -> None:
        self.is_playing = False

    def toggle_play_pause(self) -> None:
        self.is_playing = not self.is_playing

    def seek(self, frame_number: int) -> None:
        if self._capture is not None and self._capture.isOpened():
            self._capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    def get_frame(self) -> Optional[VideoFrame]:
        if not self.is_active:
            return None

        self._frame_count += 1

        if self._capture is not None and self._capture.isOpened() and self.is_playing:
            ret, frame = self._capture.read()
            if not ret:
                if self.loop:
                    self._capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, frame = self._capture.read()
                else:
                    self.is_playing = False
                    return None

            if ret and frame is not None:
                if frame.shape[1] != self.width or frame.shape[0] != self.height:
                    frame = cv2.resize(frame, (self.width, self.height), interpolation=cv2.INTER_LINEAR)
                return VideoFrame(width=self.width, height=self.height, data=frame, format="BGR", frame_number=self._frame_count)

        # Broadcast Video Media Canvas
        return self._generate_video_card()

    def _generate_video_card(self) -> VideoFrame:
        w, h = self.width, self.height
        if HAS_OPENCV:
            img = np.zeros((h, w, 3), dtype=np.uint8)
            img[:, :] = (35, 20, 20)  # Deep broadcast burgundy
            status = "PLAYING" if self.is_playing else "PAUSED"
            cv2.putText(
                img,
                f"MEDIA CLIP: {self.name}",
                (w // 4, h // 2 - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.3,
                (0, 255, 200),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                img,
                f"Status: {status} | Loop: {self.loop}",
                (w // 4, h // 2 + 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (200, 200, 200),
                2,
                cv2.LINE_AA,
            )
            return VideoFrame(width=w, height=h, data=img, format="BGR", frame_number=self._frame_count)
        return VideoFrame(width=w, height=h, data=None, format="NONE", frame_number=self._frame_count)
