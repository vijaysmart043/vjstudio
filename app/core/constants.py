"""
Application-wide constants, enumerations, and defaults.
"""

from enum import Enum, auto

APP_NAME = "VJ Studio"
APP_VERSION = "1.0.0"
APP_AUTHOR = "VJ Studio Broadcast Technologies"
ORGANIZATION_NAME = "VJStudio"
ORGANIZATION_DOMAIN = "vjstudio.local"

# Video Resolutions
RESOLUTIONS = {
    "720p (HD)": (1280, 720),
    "1080p (Full HD)": (1920, 1080),
    "1440p (2K)": (2560, 1440),
    "2160p (4K UHD)": (3840, 2160),
}

# Standard Broadcast Frame Rates
FRAME_RATES = [24, 25, 30, 50, 60]

# Audio Defaults
AUDIO_SAMPLE_RATES = [44100, 48000]
DEFAULT_SAMPLE_RATE = 48000
DEFAULT_AUDIO_CHANNELS = 2
DEFAULT_BUFFER_SIZE = 1024


class SourceType(str, Enum):
    CAMERA = "camera"
    SCREEN = "screen"
    VIDEO = "video"
    IMAGE = "image"
    COLOR = "color"
    SCENE = "scene"
    AUDIO = "audio"
    NDI = "ndi"
    STREAM = "stream"  # RTMP / SRT input stream


class TransitionType(str, Enum):
    CUT = "cut"
    FADE = "fade"
    DISSOLVE = "dissolve"
    WIPE = "wipe"
    SLIDE = "slide"


class StreamState(str, Enum):
    STOPPED = "stopped"
    STARTING = "starting"
    LIVE = "live"
    RECONNECTING = "reconnecting"
    STOPPING = "stopping"
    ERROR = "error"


class RecordState(str, Enum):
    STOPPED = "stopped"
    RECORDING = "recording"
    PAUSED = "paused"
    ERROR = "error"


# Supported media file extensions
SUPPORTED_VIDEO_FORMATS = [".mp4", ".mkv", ".mov", ".avi", ".webm", ".ts"]
SUPPORTED_IMAGE_FORMATS = [".png", ".jpg", ".jpeg", ".webp", ".bmp"]
SUPPORTED_AUDIO_FORMATS = [".wav", ".mp3", ".aac", ".ogg", ".flac"]
