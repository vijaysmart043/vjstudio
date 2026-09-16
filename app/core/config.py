"""
Application configuration management with JSON persistence and schema defaults.
"""

import json
import shutil
from dataclasses import dataclass, field, asdict
from typing import Any, Dict
from app.core.paths import paths
from app.core.logger import logger


@dataclass
class GeneralConfig:
    app_name: str = "VJ Studio"
    version: str = "1.0.0"
    theme: str = "dark_broadcast"
    auto_check_updates: bool = False
    save_project_on_exit: bool = True
    confirm_exit_on_stream: bool = True


@dataclass
class VideoConfig:
    base_width: int = 1920
    base_height: int = 1080
    fps: int = 30
    aspect_ratio: str = "16:9"
    color_space: str = "sRGB"
    gpu_acceleration: bool = True


@dataclass
class AudioConfig:
    sample_rate: int = 48000
    channels: int = 2
    buffer_size: int = 1024
    master_volume: float = 0.85


@dataclass
class StreamingConfig:
    service: str = "Custom RTMP"
    server_url: str = "rtmp://live.example.com/app"
    stream_key: str = ""
    video_bitrate_kbps: int = 4500
    audio_bitrate_kbps: int = 160
    keyframe_interval_sec: int = 2
    encoder: str = "auto"


@dataclass
class RecordingConfig:
    output_directory: str = "recordings"
    format: str = "mp4"
    video_bitrate_kbps: int = 8000
    audio_bitrate_kbps: int = 192
    encoder: str = "auto"


@dataclass
class FFmpegConfig:
    custom_bin_path: str = ""
    prefer_hardware_accel: bool = True


@dataclass
class HotkeysConfig:
    cut: str = "C"
    fade: str = "F"
    dissolve: str = "D"
    toggle_stream: str = "Space"
    toggle_record: str = "R"
    input_1: str = "F1"
    input_2: str = "F2"
    input_3: str = "F3"
    input_4: str = "F4"
    scene_1: str = "F5"
    scene_2: str = "F6"


@dataclass
class AppConfig:
    general: GeneralConfig = field(default_factory=GeneralConfig)
    video: VideoConfig = field(default_factory=VideoConfig)
    audio: AudioConfig = field(default_factory=AudioConfig)
    streaming: StreamingConfig = field(default_factory=StreamingConfig)
    recording: RecordingConfig = field(default_factory=RecordingConfig)
    ffmpeg: FFmpegConfig = field(default_factory=FFmpegConfig)
    hotkeys: HotkeysConfig = field(default_factory=HotkeysConfig)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AppConfig":
        return cls(
            general=GeneralConfig(**data.get("general", {})),
            video=VideoConfig(**data.get("video", {})),
            audio=AudioConfig(**data.get("audio", {})),
            streaming=StreamingConfig(**data.get("streaming", {})),
            recording=RecordingConfig(**data.get("recording", {})),
            ffmpeg=FFmpegConfig(**data.get("ffmpeg", {})),
            hotkeys=HotkeysConfig(**data.get("hotkeys", {})),
        )


class ConfigManager:
    """Loads, caches, and persists application configuration."""

    _instance = None

    def __init__(self) -> None:
        self.config = AppConfig()
        self.load()

    @classmethod
    def get_instance(cls) -> "ConfigManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load(self) -> AppConfig:
        """Load configuration from user settings or bundled defaults."""
        data: Dict[str, Any] = {}

        # 1. Load default config if exists
        default_path = paths.default_config_file
        if default_path.exists():
            try:
                with open(default_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                logger.error(f"Failed to read default config: {e}")

        # 2. Merge user config if exists
        user_path = paths.user_config_file
        if user_path.exists():
            try:
                with open(user_path, "r", encoding="utf-8") as f:
                    user_data = json.load(f)
                    # Recursive shallow section update
                    for section, values in user_data.items():
                        if section in data and isinstance(values, dict):
                            data[section].update(values)
                        else:
                            data[section] = values
            except Exception as e:
                logger.warning(f"Could not load user settings: {e}")

        try:
            self.config = AppConfig.from_dict(data)
        except Exception as e:
            logger.error(f"Error parsing configuration data, using defaults: {e}")
            self.config = AppConfig()

        return self.config

    def save(self) -> bool:
        """Persist current settings to the user configuration file."""
        try:
            user_path = paths.user_config_file
            user_path.parent.mkdir(parents=True, exist_ok=True)
            with open(user_path, "w", encoding="utf-8") as f:
                json.dump(self.config.to_dict(), f, indent=2)
            logger.info(f"Saved user configuration to {user_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False


config_manager = ConfigManager.get_instance()
config = config_manager.config
Config = AppConfig
