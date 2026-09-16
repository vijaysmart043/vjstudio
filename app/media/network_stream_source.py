"""
Network streaming input source (RTMP / SRT / RTSP playback).
Pulls a live network stream into the VJ Studio media pipeline using OpenCV / FFmpeg.
"""

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


class NetworkStreamSource(MediaSource):
    """Ingests RTMP, SRT, or RTSP incoming feeds into the production pipeline."""

    def __init__(self, name: str, stream_url: str) -> None:
        super().__init__(name=name, source_type=SourceType.STREAM, width=1920, height=1080)
        self.stream_url = stream_url
        self._cap = None
        self._standby_frame: Optional[np.ndarray] = None

    def start(self) -> bool:
        if self.is_active:
            return True

        logger.info(f"Connecting to network stream: {self.stream_url}")
        if HAS_OPENCV:
            try:
                self._cap = cv2.VideoCapture(self.stream_url)
                if self._cap.isOpened():
                    logger.info(f"Successfully opened stream: {self.name}")
            except Exception as e:
                logger.warning(f"Unable to open stream immediately: {e}. Will retry in background.")

        self.is_active = True
        return True

    def stop(self) -> None:
        if not self.is_active:
            return
        if self._cap:
            try:
                self._cap.release()
            except Exception:
                pass
            self._cap = None
        self.is_active = False
        logger.info(f"Stopped network stream: {self.name}")

    def get_frame(self) -> Optional[VideoFrame]:
        if not self.is_active or not self.visible:
            return None

        if HAS_OPENCV:
            if self._cap and self._cap.isOpened():
                ret, frame = self._cap.read()
                if ret and frame is not None:
                    h, w = frame.shape[:2]
                    if w != self.width or h != self.height:
                        frame = cv2.resize(frame, (self.width, self.height))
                    return VideoFrame(width=self.width, height=self.height, data=frame, format="BGR")

            # Fallback standby feed with stream URL information
            if self._standby_frame is None:
                self._standby_frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                self._standby_frame[:, :] = (24, 18, 22)

            f = self._standby_frame.copy()
            cv2.putText(
                f,
                f"STREAM INGEST | {self.name}",
                (40, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 128),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                f,
                f"URL: {self.stream_url}",
                (40, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (180, 180, 180),
                1,
                cv2.LINE_AA,
            )
            return VideoFrame(width=self.width, height=self.height, data=f, format="BGR")

        return VideoFrame(width=self.width, height=self.height, data=None, format="NONE")
