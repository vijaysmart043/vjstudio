"""
Canonical ProgramOutput Pipeline.
Directly supplies the unified broadcast Program feed to:
1. Preview / Program UI Display
2. Local Recording Engine
3. RTMP Live Streaming
4. SRT Low-Latency Streaming
5. NDI Network Output
6. Virtual Camera Feed
"""

from typing import Callable, List, Optional
from app.core.events import events, EVENT_INPUT_SELECTED_PROGRAM
from app.core.logger import logger
from app.media.frame import VideoFrame
from app.media.media_source import MediaSource
from app.production.input_manager import input_manager

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


# Type definition for downstream consumer callbacks
FrameConsumer = Callable[[VideoFrame], None]


class ProgramOutput:
    """
    Unified canonical Program Output Pipeline.
    Single point of truth feeding UI, Streamer, Recorder, NDI, and Virtual Camera.
    """

    _instance = None

    def __init__(self) -> None:
        self._current_source_id: Optional[str] = None
        self._consumers: List[FrameConsumer] = []
        self._ndi_output_enabled: bool = False
        self._virtual_cam_enabled: bool = False
        self._last_frame: Optional[VideoFrame] = None
        self._frame_count: int = 0

    @classmethod
    def get_instance(cls) -> "ProgramOutput":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def set_source(self, source_id: str) -> bool:
        src = input_manager.get_source(source_id)
        if src:
            self._current_source_id = source_id
            logger.info(f"AIRING LIVE on Canonical Program Pipeline: {src.name} [{source_id}]")
            events.publish(EVENT_INPUT_SELECTED_PROGRAM, source_id)
            return True
        return False

    @property
    def current_source_id(self) -> Optional[str]:
        return self._current_source_id

    @property
    def current_source(self) -> Optional[MediaSource]:
        if self._current_source_id:
            return input_manager.get_source(self._current_source_id)
        return None

    def register_consumer(self, consumer: FrameConsumer) -> None:
        """Register downstream outputs (Recorder, RTMP, SRT, NDI, Virtual Camera)."""
        if consumer not in self._consumers:
            self._consumers.append(consumer)

    def unregister_consumer(self, consumer: FrameConsumer) -> None:
        if consumer in self._consumers:
            self._consumers.remove(consumer)

    def get_frame(self) -> Optional[VideoFrame]:
        """Fetch frame from active Program source and broadcast to all registered consumers."""
        src = self.current_source
        frame: Optional[VideoFrame] = None

        if src and src.enabled:
            frame = src.get_frame()

        if frame is not None:
            self._last_frame = frame
            self._frame_count += 1
            # Dispatch to downstream encoders/consumers
            for consumer in self._consumers:
                try:
                    consumer(frame)
                except Exception as e:
                    logger.error(f"Downstream consumer error: {e}")

        return frame

    @property
    def last_frame(self) -> Optional[VideoFrame]:
        return self._last_frame

    # NDI Output control
    def set_ndi_output_enabled(self, enabled: bool) -> None:
        self._ndi_output_enabled = enabled
        try:
            from app.ndi.ndi_output import ndi_output
            if enabled:
                ndi_output.start()
                self.register_consumer(ndi_output.send_frame)
            else:
                self.unregister_consumer(ndi_output.send_frame)
                ndi_output.stop()
        except Exception as e:
            logger.warning(f"NDI Output hook notice: {e}")
        logger.info(f"Program NDI Network Output set to: {'ENABLED' if enabled else 'DISABLED'}")

    @property
    def is_ndi_output_enabled(self) -> bool:
        return self._ndi_output_enabled

    # Virtual Camera control
    def set_virtual_camera_enabled(self, enabled: bool) -> None:
        self._virtual_cam_enabled = enabled
        try:
            from app.virtual_camera.camera_manager import virtual_camera_manager
            if enabled:
                virtual_camera_manager.start()
                self.register_consumer(virtual_camera_manager.on_program_frame)
            else:
                self.unregister_consumer(virtual_camera_manager.on_program_frame)
                virtual_camera_manager.stop()
        except Exception as e:
            logger.warning(f"Virtual Camera hook notice: {e}")
        logger.info(f"Program Virtual Camera Output set to: {'ENABLED' if enabled else 'DISABLED'}")

    @property
    def is_virtual_camera_enabled(self) -> bool:
        return self._virtual_cam_enabled


program_output = ProgramOutput.get_instance()
