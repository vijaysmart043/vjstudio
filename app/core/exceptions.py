"""
VJ Studio exceptions hierarchy for graceful handling and error recovery.
"""

class VJStudioError(Exception):
    """Base exception for all VJ Studio broadcast subsystem errors."""
    pass


class DeviceError(VJStudioError):
    """Hardware device errors (Camera, Audio capture card, DirectShow)."""
    pass


class FFmpegError(VJStudioError):
    """FFmpeg binary execution or hardware encoder failures."""
    pass


class StreamError(VJStudioError):
    """RTMP / SRT connection, handshake, or socket errors."""
    pass


class RecordingError(VJStudioError):
    """Local storage recording or filesystem write errors."""
    pass


class NDIError(VJStudioError):
    """NDI discovery, packet reception, or transmission failures."""
    pass


class VirtualCameraError(VJStudioError):
    """DirectShow / Media Foundation virtual camera backend errors."""
    pass
