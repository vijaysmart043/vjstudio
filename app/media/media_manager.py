"""
Media manager coordinating all active media inputs, hardware devices, and playback decoders.
"""

from app.media.camera import CameraSource
from app.media.camera_manager import CameraManager, camera_manager
from app.media.image_source import ImageSource
from app.media.media_source import MediaSource, SourceTransform
from app.media.screen_capture import ScreenCaptureSource
from app.media.video_source import VideoSource
from app.production.input_manager import InputManager, input_manager as media_manager

__all__ = [
    "CameraSource",
    "CameraManager",
    "camera_manager",
    "ImageSource",
    "MediaSource",
    "SourceTransform",
    "ScreenCaptureSource",
    "VideoSource",
    "media_manager",
    "InputManager",
]
