"""
Hardware camera discovery and device enumeration for Windows.
"""

from typing import Dict, List
from app.core.logger import logger

try:
    import cv2
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False


class CameraInfo:
    def __init__(self, index: int, name: str, is_available: bool = True) -> None:
        self.index = index
        self.name = name
        self.is_available = is_available

    def __repr__(self) -> str:
        return f"<CameraInfo {self.index}: '{self.name}'>"


class CameraManager:
    """Discovers and caches available video input devices."""

    _instance = None

    def __init__(self) -> None:
        self._cached_devices: List[CameraInfo] = []

    @classmethod
    def get_instance(cls) -> "CameraManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def scan_devices(self, max_devices_to_check: int = 4) -> List[CameraInfo]:
        """Scan system for available camera indices."""
        devices: List[CameraInfo] = []
        if not HAS_OPENCV:
            devices.append(CameraInfo(0, "Integrated Camera (Virtual)"))
            self._cached_devices = devices
            return devices

        for idx in range(max_devices_to_check):
            try:
                cap = cv2.VideoCapture(idx)
                if cap.isOpened():
                    devices.append(CameraInfo(idx, f"Camera {idx + 1} (DirectShow)"))
                    cap.release()
            except Exception as e:
                logger.debug(f"Camera index {idx} scan error: {e}")

        # If no physical camera detected, provide a reliable virtual camera option
        if not devices:
            devices.append(CameraInfo(0, "Camera 1 (Virtual Test Source)"))

        self._cached_devices = devices
        logger.info(f"Discovered cameras: {devices}")
        return devices

    def get_devices(self) -> List[CameraInfo]:
        if not self._cached_devices:
            return self.scan_devices()
        return self._cached_devices

    def get_available_cameras(self) -> List[CameraInfo]:
        return self.get_devices()


camera_manager = CameraManager.get_instance()
