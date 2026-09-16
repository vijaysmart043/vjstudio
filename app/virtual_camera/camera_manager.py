"""
Virtual Camera Manager.
Connects canonical ProgramOutput to the Windows Virtual Camera driver backend.
"""

from typing import Optional
from app.core.logger import logger
from app.media.frame import VideoFrame
from app.virtual_camera.windows_backend import WindowsVirtualCameraBackend


class VirtualCameraManager:
    """Manages the Windows Virtual Camera service lifecycle and Program feed hook."""

    _instance = None

    def __init__(self) -> None:
        self.backend = WindowsVirtualCameraBackend()
        self._is_active = False

    @classmethod
    def get_instance(cls) -> "VirtualCameraManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def start(self) -> bool:
        if self._is_active:
            return True
        ok = self.backend.start()
        if ok:
            self._is_active = True
            logger.info("Virtual Camera broadcast activated.")
        return ok

    def stop(self) -> None:
        if not self._is_active:
            return
        self.backend.stop()
        self._is_active = False
        logger.info("Virtual Camera broadcast deactivated.")

    def on_program_frame(self, frame: VideoFrame) -> None:
        """Consumer callback called by canonical ProgramOutput."""
        if self._is_active:
            self.backend.send_frame(frame)

    @property
    def is_active(self) -> bool:
        return self._is_active


virtual_camera_manager = VirtualCameraManager.get_instance()
