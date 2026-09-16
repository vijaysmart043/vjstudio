"""
Windows Virtual Camera integration package for VJ Studio.
Publishes canonical ProgramOutput as a native DirectShow / Media Foundation virtual camera
for Microsoft Teams, Zoom, OBS, Discord, Google Meet, and browsers.
"""

from app.virtual_camera.camera_manager import VirtualCameraManager, virtual_camera_manager

__all__ = ["VirtualCameraManager", "virtual_camera_manager"]
