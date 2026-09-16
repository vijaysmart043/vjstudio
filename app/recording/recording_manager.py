"""
Recording manager providing high-level recording controls, disk capacity checks, and file rotation.
"""

from app.recording.recorder import Recorder, recorder
from app.recording.recording_config import RecordingProfile

__all__ = ["Recorder", "recorder", "RecordingProfile"]
