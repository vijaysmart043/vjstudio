"""
NDI Program Output Transmitter.
Broadcasts the canonical Program output stream over the local subnet as an NDI sender.
"""

from typing import Optional
from app.core.logger import logger
from app.media.frame import VideoFrame

try:
    import numpy as np
    import NDIlib as ndi
    HAS_NDI = True
except ImportError:
    HAS_NDI = False


class NDIOutput:
    """Publishes the canonical VJ Studio Program feed to the network via NDI."""

    _instance = None

    def __init__(self, sender_name: str = "VJ Studio - Program") -> None:
        self.sender_name = sender_name
        self._is_broadcasting = False
        self._ndi_send = None

    @classmethod
    def get_instance(cls) -> "NDIOutput":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def start(self) -> bool:
        if self._is_broadcasting:
            return True

        logger.info(f"Starting NDI Program Output: {self.sender_name}")
        if HAS_NDI:
            try:
                send_create_desc = ndi.SendCreate()
                send_create_desc.p_ndi_name = self.sender_name
                self._ndi_send = ndi.send_create(send_create_desc)
            except Exception as e:
                logger.error(f"Failed to create NDI sender: {e}")

        self._is_broadcasting = True
        return True

    def stop(self) -> None:
        if not self._is_broadcasting:
            return
        if HAS_NDI and self._ndi_send:
            try:
                ndi.send_destroy(self._ndi_send)
            except Exception:
                pass
            self._ndi_send = None

        self._is_broadcasting = False
        logger.info("Stopped NDI Program Output.")

    def send_frame(self, frame: VideoFrame) -> None:
        """Called by canonical ProgramOutput consumer."""
        if not self._is_broadcasting or frame.data is None:
            return

        if HAS_NDI and self._ndi_send:
            try:
                video_frame = ndi.VideoFrameV2()
                video_frame.data = frame.data
                video_frame.FourCC = ndi.FOURCC_VIDEO_TYPE_BGRX
                video_frame.xres = frame.width
                video_frame.yres = frame.height
                ndi.send_send_video_v2(self._ndi_send, video_frame)
            except Exception as e:
                logger.debug(f"NDI frame dispatch error: {e}")

    @property
    def is_broadcasting(self) -> bool:
        return self._is_broadcasting


ndi_output = NDIOutput.get_instance()
