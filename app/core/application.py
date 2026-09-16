"""
Core desktop application lifecycle, crash reporting, and runtime orchestration.
"""

import sys
from typing import Any, Optional
from app.core.constants import APP_NAME, APP_VERSION
from app.core.logger import logger
from app.core.paths import paths
from app.core.config import config
from app.storage.database import Database
from app.ffmpeg.ffmpeg_manager import ffmpeg_manager
from app.ndi.ndi_manager import ndi_manager

try:
    from PySide6.QtWidgets import QApplication
    HAS_QT = True
except ImportError:
    HAS_QT = False
    QApplication = Any  # type: ignore


class VJStudioApplication:
    """Orchestrates system startup, desktop services, database migrations, and clean exit."""

    def __init__(self, sys_argv: list) -> None:
        self.sys_argv = sys_argv
        self.qt_app: Optional[QApplication] = None
        self._is_initialized = False

    def initialize(self) -> bool:
        """Initializes logging, directories, database, and hardware engines."""
        logger.info(f"Starting {APP_NAME} v{APP_VERSION} on Windows desktop...")

        # 1. Verify directory paths
        paths.user_data_dir.mkdir(parents=True, exist_ok=True)
        paths.logs_dir.mkdir(parents=True, exist_ok=True)
        paths.recordings_dir.mkdir(parents=True, exist_ok=True)

        # 2. Initialize SQLite storage
        Database.get_instance()

        # 3. Detect FFmpeg and hardware encoders
        ffmpeg_manager.detect()
        if ffmpeg_manager.is_available:
            logger.info(f"FFmpeg ready: {ffmpeg_manager.ffmpeg_path} ({ffmpeg_manager.version_info})")
        else:
            logger.warning("FFmpeg not found on PATH or bundle; software render fallback active.")

        # 4. Initialize NDI runtime
        ndi_manager.discover_sources()

        self._is_initialized = True
        return True

    def create_gui(self) -> Optional[QApplication]:
        if not HAS_QT:
            logger.error("PySide6 is not installed. GUI mode unavailable.")
            return None

        self.qt_app = QApplication(self.sys_argv)
        self.qt_app.setApplicationName(APP_NAME)
        self.qt_app.setApplicationVersion(APP_VERSION)
        return self.qt_app

    def run(self) -> int:
        self.initialize()
        if not HAS_QT:
            logger.info("Running in headless console mode.")
            return 0

        app = self.create_gui()
        if not app:
            return 1

        from app.ui.main_window import MainWindow
        window = MainWindow()
        window.show()
        return app.exec()
