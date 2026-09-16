"""
Cross-platform path resolution with special handling for Windows and PyInstaller.
"""

import os
import sys
from pathlib import Path
from typing import Optional


class PathManager:
    """Manages application directories and resource paths."""

    _instance: Optional["PathManager"] = None

    def __init__(self) -> None:
        # Determine if running in a PyInstaller frozen bundle
        self.is_frozen = getattr(sys, "frozen", False)

        if self.is_frozen:
            # PyInstaller temp folder
            self._bundle_dir = Path(getattr(sys, "_MEIPASS", sys.executable)).resolve()
            # Directory where the .exe lives
            self._app_dir = Path(sys.executable).parent.resolve()
        else:
            # Running from source code (e.g. repo root)
            self._app_dir = Path(__file__).resolve().parent.parent.parent
            self._bundle_dir = self._app_dir

        # Windows User Data Directory (%APPDATA%/VJStudio or ~/.vjstudio)
        appdata = os.getenv("APPDATA")
        if appdata:
            self._user_data_dir = Path(appdata) / "VJStudio"
        else:
            self._user_data_dir = Path.home() / ".vjstudio"

        self._logs_dir = self._user_data_dir / "logs"
        self._config_dir = self._user_data_dir / "config"
        self._recordings_dir = Path.home() / "Videos" / "VJStudio"
        self._projects_dir = Path.home() / "Documents" / "VJStudio" / "Projects"

        self._ensure_directories()

    @classmethod
    def get_instance(cls) -> "PathManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _ensure_directories(self) -> None:
        """Create user writable directories if they do not exist."""
        for path in [
            self._user_data_dir,
            self._logs_dir,
            self._config_dir,
            self._recordings_dir,
            self._projects_dir,
        ]:
            try:
                path.mkdir(parents=True, exist_ok=True)
            except OSError:
                pass

    @property
    def app_dir(self) -> Path:
        """Root application or executable directory."""
        return self._app_dir

    @property
    def bundle_dir(self) -> Path:
        """PyInstaller unpack bundle directory or source root."""
        return self._bundle_dir

    @property
    def user_data_dir(self) -> Path:
        """Persistent user data directory."""
        return self._user_data_dir

    @property
    def logs_dir(self) -> Path:
        """Directory for rotating logs."""
        return self._logs_dir

    @property
    def log_file(self) -> Path:
        """Primary log file path."""
        return self._logs_dir / "vjstudio.log"

    @property
    def config_dir(self) -> Path:
        """User configuration directory."""
        return self._config_dir

    @property
    def user_config_file(self) -> Path:
        """Active user config json."""
        return self._config_dir / "settings.json"

    @property
    def default_config_file(self) -> Path:
        """Default bundled config file."""
        return self._bundle_dir / "config" / "default.json"

    @property
    def assets_dir(self) -> Path:
        """Static assets directory (icons, fonts, images)."""
        return self._bundle_dir / "assets"

    @property
    def bundled_ffmpeg_bin(self) -> Path:
        """Path to bundled FFmpeg binaries."""
        # Check inside bundle dir first, then app dir
        bundle_path = self._bundle_dir / "ffmpeg" / "bin"
        if bundle_path.exists():
            return bundle_path
        return self._app_dir / "ffmpeg" / "bin"

    @property
    def default_recordings_dir(self) -> Path:
        return self._recordings_dir

    @property
    def recordings_dir(self) -> Path:
        return self._recordings_dir

    @property
    def default_projects_dir(self) -> Path:
        return self._projects_dir

    @property
    def projects_dir(self) -> Path:
        return self._projects_dir


# Global singleton access
paths = PathManager.get_instance()
