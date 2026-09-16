"""
Comprehensive verification test suite for Windows desktop architecture,
package structure, absence of mobile/Android artifacts, and canonical engine readiness.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.application import VJStudioApplication
from app.core.constants import APP_NAME, SourceType, TransitionType
from app.core.exceptions import VJStudioError
from app.ffmpeg.ffmpeg_manager import ffmpeg_manager
from app.media.camera_manager import camera_manager
from app.media.media_manager import media_manager
from app.production.program_output import program_output
from app.production.preview_output import preview_output
from app.production.transition import transition_manager
from app.audio.audio_mixer import audio_mixer
from app.ndi.ndi_manager import ndi_manager
from app.ndi.ndi_output import ndi_output
from app.virtual_camera.camera_manager import virtual_camera_manager
from app.graphics.templates import BUILTIN_TEMPLATES, get_template
from app.storage.database import Database


def test_windows_desktop_architecture():
    # 1. Verify desktop application initialization
    app = VJStudioApplication(["--headless"])
    assert app.initialize() is True

    # 2. Verify no Android / mobile files exist in the tree
    project_root = Path(__file__).resolve().parent.parent
    forbidden_patterns = [
        "**/*.kt",
        "**/*.kts",
        "**/AndroidManifest.xml",
        "**/*gradle*",
    ]
    for pattern in forbidden_patterns:
        matches = list(project_root.glob(pattern))
        assert len(matches) == 0, f"Found forbidden mobile/Android files: {matches}"

    # 3. Verify media sources & production switching
    cams = camera_manager.get_available_cameras()
    assert isinstance(cams, list)

    # 4. Verify canonical Program Output and consumers
    assert program_output is not None
    program_output.set_ndi_output_enabled(True)
    assert program_output.is_ndi_output_enabled is True
    assert ndi_output.is_broadcasting is True

    program_output.set_virtual_camera_enabled(True)
    assert program_output.is_virtual_camera_enabled is True
    assert virtual_camera_manager.is_active is True

    # Reset output toggles
    program_output.set_ndi_output_enabled(False)
    program_output.set_virtual_camera_enabled(False)

    # 5. Verify Audio Mixer
    channels = audio_mixer.get_channels()
    assert len(channels) >= 4
    ch_ids = [c.id for c in channels]
    assert "mic_1" in ch_ids
    assert "master" in ch_ids

    # 6. Verify Virtual Sets
    assert len(BUILTIN_TEMPLATES) >= 6
    news = get_template("news_studio")
    assert news is not None
    assert news.category == "News"

    # 7. Verify Database
    db = Database.get_instance()
    assert db is not None


if __name__ == "__main__":
    test_windows_desktop_architecture()
    print("test_windows_desktop passed!")
