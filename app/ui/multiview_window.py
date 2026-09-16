"""
Standalone Multiview Production Window.
Allows positioning the Multiview grid on a second monitor / auxiliary display.
"""

from typing import Optional
from app.core.constants import APP_NAME
from app.ui.theme import DARK_BROADCAST_STYLESHEET
from app.ui.widgets.multiview_widget import MultiviewWidget

try:
    from PySide6.QtCore import Qt, QTimer
    from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
    HAS_QT = True
except ImportError:
    HAS_QT = False


class MultiviewWindow(QMainWindow):
    """Separate auxiliary monitor window for Studio Multiview output."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(f"{APP_NAME} — Multiview Production Monitor")
        self.resize(1280, 720)
        self.setMinimumSize(800, 480)
        self.setStyleSheet(DARK_BROADCAST_STYLESHEET)

        central = QWidget(self)
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(4, 4, 4, 4)

        self.multiview = MultiviewWidget(self)
        layout.addWidget(self.multiview)

        # 30 FPS refresh timer
        self.timer = QTimer(self)
        self.timer.setInterval(33)
        self.timer.timeout.connect(self.multiview.refresh_multiview)
        self.timer.start()
