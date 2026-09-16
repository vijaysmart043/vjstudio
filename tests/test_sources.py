"""
Tests for MediaSource lifecycle, registry, and preview/program cueing.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.constants import SourceType
from app.media.camera import CameraSource
from app.media.screen_capture import ScreenCaptureSource
from app.production.input_manager import input_manager
from app.production.preview_output import preview_output
from app.production.program_output import program_output
from app.production.transition_manager import transition_manager


def test_media_source_creation():
    cam = CameraSource(name="Test Cam", device_index=0)
    assert cam.name == "Test Cam"
    assert cam.type == SourceType.CAMERA
    assert cam.width == 1280
    assert cam.height == 720
    assert cam.visible is True


def test_input_registry_and_transition():
    c1 = CameraSource(name="C1", device_index=0)
    c2 = ScreenCaptureSource(name="S1")

    input_manager.add_source(c1)
    input_manager.add_source(c2)

    # Cue C1 to Preview
    preview_output.select_source(c1.id)
    assert preview_output.current_source_id == c1.id

    # Cue C2 to Program
    program_output.set_source(c2.id)
    assert program_output.current_source_id == c2.id

    # Execute CUT
    transition_manager.cut()

    # C1 should now be on Program, and C2 should now be on Preview
    assert program_output.current_source_id == c1.id
    assert preview_output.current_source_id == c2.id


if __name__ == "__main__":
    test_media_source_creation()
    test_input_registry_and_transition()
    print("test_sources passed!")
