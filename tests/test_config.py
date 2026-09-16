"""
Tests for configuration parsing, serialization, and default settings.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import AppConfig, GeneralConfig, VideoConfig, StreamingConfig


def test_default_config_creation():
    cfg = AppConfig()
    assert cfg.general.app_name == "VJ Studio"
    assert cfg.video.base_width == 1920
    assert cfg.video.base_height == 1080
    assert cfg.video.fps == 30
    assert cfg.streaming.video_bitrate_kbps == 4500


def test_config_dict_roundtrip():
    cfg = AppConfig()
    cfg.video.fps = 60
    cfg.general.app_name = "Studio Pro"

    data = cfg.to_dict()
    restored = AppConfig.from_dict(data)

    assert restored.video.fps == 60
    assert restored.general.app_name == "Studio Pro"


if __name__ == "__main__":
    test_default_config_creation()
    test_config_dict_roundtrip()
    print("test_config passed!")
