"""
Tests for cross-platform PathManager resolution and user data directories.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.paths import paths


def test_path_manager_directories():
    assert paths.app_dir.exists()
    assert paths.user_data_dir is not None
    assert paths.logs_dir is not None
    assert paths.default_config_file is not None


def test_log_file_resolution():
    log_file = paths.log_file
    assert log_file.name == "vjstudio.log"


if __name__ == "__main__":
    test_path_manager_directories()
    test_log_file_resolution()
    print("test_paths passed!")
