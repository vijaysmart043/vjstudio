"""
Broadcast PREVIEW monitor widget featuring green tally light framing.
"""

from typing import Optional
from app.core.constants import APP_NAME
from app.media.frame import VideoFrame
from app.media.renderer import FrameRenderer
from app.production.preview_output import preview_output
from app.ui.theme import COLOR_PREVIEW_CUE, COLOR_SURFACE_DARK, COLOR_BORDER

try:
    from PySide6.QtCore import Qt, QRect
    from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPixmap
    from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
    HAS_QT = True
except ImportError:
    HAS_QT = False


class PreviewWidget(QWidget):
    """Viewport displaying the source currently cued on PREVIEW."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setMinimumSize(320, 180)
        self._current_pixmap: Optional[QPixmap] = None
        self._source_name: str = "NO SOURCE"

    def update_frame(self, frame: Optional[VideoFrame]) -> None:
        src = preview_output.current_source
        self._source_name = src.name.upper() if src else "PREVIEW [EMPTY]"

        if frame and frame.is_valid:
            self._current_pixmap = FrameRenderer.to_qpixmap(frame)
        else:
            self._current_pixmap = None
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()

        # Canvas background
        painter.fillRect(0, 0, w, h, QColor(14, 16, 20))

        # Maintain 16:9 aspect ratio letterbox/pillarbox
        target_ratio = 16.0 / 9.0
        avail_ratio = w / max(1, h)

        if avail_ratio > target_ratio:
            disp_h = h - 8
            disp_w = int(disp_h * target_ratio)
        else:
            disp_w = w - 8
            disp_h = int(disp_w / target_ratio)

        x = (w - disp_w) // 2
        y = (h - disp_h) // 2
        disp_rect = QRect(x, y, disp_w, disp_h)

        # Draw Video Frame
        if self._current_pixmap and not self._current_pixmap.isNull():
            painter.drawPixmap(disp_rect, self._current_pixmap)
        else:
            painter.fillRect(disp_rect, QColor(22, 25, 32))
            painter.setPen(QColor(100, 110, 130))
            painter.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            painter.drawText(disp_rect, Qt.AlignmentFlag.AlignCenter, "CUE A SOURCE FOR PREVIEW")

        # Green Tally Frame (PREVIEW indicator)
        tally_pen = QPen(QColor(COLOR_PREVIEW_CUE), 2)
        painter.setPen(tally_pen)
        painter.drawRect(disp_rect)

        # Header Badge: PREVIEW
        badge_w, badge_h = 100, 22
        badge_rect = QRect(x + 8, y + 8, badge_w, badge_h)
        painter.fillRect(badge_rect, QColor(0, 230, 118, 200))
        painter.setPen(QColor(0, 0, 0))
        painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Black))
        painter.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, "PREVIEW")

        # Source Name Footer Badge
        name_rect = QRect(x + 8, y + disp_h - 26, disp_w - 16, 20)
        painter.fillRect(name_rect, QColor(10, 12, 16, 210))
        painter.setPen(QColor(220, 230, 240))
        painter.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold))
        painter.drawText(name_rect.adjusted(8, 0, 0, 0), Qt.AlignmentFlag.AlignVCenter, self._source_name)
