"""
Core package exports: Application lifecycle, configuration, logging, events, exceptions, and paths.
"""

from app.core.application import VJStudioApplication
from app.core.config import Config, config
from app.core.constants import APP_NAME, APP_VERSION, SourceType, TransitionType, StreamState, RecordState
from app.core.events import EventBus, events
from app.core.exceptions import VJStudioError, DeviceError, FFmpegError, StreamError, RecordingError, NDIError, VirtualCameraError
from app.core.logger import logger
from app.core.paths import PathManager, paths

__all__ = [
    "VJStudioApplication",
    "Config",
    "config",
    "APP_NAME",
    "APP_VERSION",
    "SourceType",
    "TransitionType",
    "StreamState",
    "RecordState",
    "EventBus",
    "events",
    "VJStudioError",
    "DeviceError",
    "FFmpegError",
    "StreamError",
    "RecordingError",
    "NDIError",
    "VirtualCameraError",
    "logger",
    "PathManager",
    "paths",
]
