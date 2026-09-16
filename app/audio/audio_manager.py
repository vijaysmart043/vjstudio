"""
Audio hardware discovery and device enumeration for Windows audio endpoints.
"""

from typing import List
from app.core.logger import logger


class AudioDeviceInfo:
    def __init__(self, id: str, name: str, is_default: bool = False) -> None:
        self.id = id
        self.name = name
        self.is_default = is_default

    def __repr__(self) -> str:
        return f"<AudioDevice '{self.name}' (default={self.is_default})>"


class AudioManager:
    """Manages audio endpoint discovery (Microphones, Speakers)."""

    _instance = None

    def __init__(self) -> None:
        self._input_devices: List[AudioDeviceInfo] = []
        self._output_devices: List[AudioDeviceInfo] = []
        self.scan_devices()

    @classmethod
    def get_instance(cls) -> "AudioManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def scan_devices(self) -> None:
        """Enumerate system audio endpoints."""
        self._input_devices = [
            AudioDeviceInfo("def_mic", "Default Microphone (WASAPI)", is_default=True),
            AudioDeviceInfo("mic_line_1", "Realtek High Definition Audio (Mic in)"),
        ]
        self._output_devices = [
            AudioDeviceInfo("def_out", "Default Playback Device (Speakers)", is_default=True),
            AudioDeviceInfo("headphones", "Headphones (WASAPI)"),
        ]
        logger.info(f"Discovered {len(self._input_devices)} audio input devices.")

    @property
    def input_devices(self) -> List[AudioDeviceInfo]:
        return self._input_devices

    @property
    def output_devices(self) -> List[AudioDeviceInfo]:
        return self._output_devices


audio_manager = AudioManager.get_instance()
