"""
NDI Media Source.
Ingests live video and audio packets from an NDI network transmitter.
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
    import NDIlib as ndi
    HAS_NDI = True
except ImportError:
    HAS_NDI = False


class NDISource(MediaSource):
    """Ingests NDI video and audio stream into the production switcher."""

    def __init__(self, name: str, source_name: Optional[str] = None) -> None:
        super().__init__(name=name, source_type=SourceType.NDI, width=1920, height=1080)
        self.source_name = source_name or name
        self._ndi_recv = None
        self._connected = False
        self._standby_frame: Optional[np.ndarray] = None
        self._frame_count = 0

    def start(self) -> bool:
        if self.is_active:
            return True

        logger.info(f"Connecting to NDI transmitter: {self.source_name}")
        if HAS_NDI:
            try:
                recv_create_desc = ndi.RecvCreateV3()
                recv_create_desc.color_format = ndi.RECV_COLOR_FORMAT_BGRX_BGRA
                self._ndi_recv = ndi.recv_create_v3(recv_create_desc)
                # Connect to specific source
                src = ndi.Source()
                src.ndi_name = self.source_name
                ndi.recv_connect(self._ndi_recv, src)
                self._connected = True
            except Exception as e:
                logger.warning(f"NDI receiver error: {e}")
        else:
            self._connected = True

        self.is_active = True
        return True

    def stop(self) -> None:
        if not self.is_active:
            return
        if HAS_NDI and self._ndi_recv:
            try:
                ndi.recv_destroy(self._ndi_recv)
            except Exception:
                pass
            self._ndi_recv = None

        self._connected = False
        self.is_active = False
        logger.info(f"Disconnected from NDI transmitter: {self.name}")

    def get_frame(self) -> Optional[VideoFrame]:
        if not self.is_active or not self.visible:
            return None

        self._frame_count += 1

        if HAS_NDI and self._ndi_recv:
            try:
                t, v, a, _ = ndi.recv_capture_v2(self._ndi_recv, 10)
                if t == ndi.FRAME_TYPE_VIDEO and v.data is not None:
                    frame = np.copy(v.data)
                    ndi.recv_free_video_v2(self._ndi_recv, v)
                    return VideoFrame(width=v.xres, height=v.yres, data=frame, format="BGR")
            except Exception as e:
                logger.error(f"Error receiving NDI frame: {e}")

        # Software standby slate with NDI telemetry
        if HAS_CV2:
            if self._standby_frame is None:
                self._standby_frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                self._standby_frame[:, :] = (34, 26, 18)  # Deep NDI cyan-slate

            frame = self._standby_frame.copy()
            cv2.putText(
                frame,
                f"NDI INGEST | {self.source_name}",
                (50, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.1,
                (0, 230, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                frame,
                f"STATUS: {'CONNECTED' if self._connected else 'CONNECTING'} | 1080p 59.94 NDI|HX",
                (50, 130),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (180, 190, 205),
                1,
                cv2.LINE_AA,
            )
            return VideoFrame(width=self.width, height=self.height, data=frame, format="BGR")

        return VideoFrame(width=self.width, height=self.height, data=None, format="NONE")
