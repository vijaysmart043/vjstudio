"""
Broadcast PROGRAM monitor widget featuring glowing red LIVE tally framing.
"""

from typing import Optional
from app.media.frame import VideoFrame
from app.media.renderer import FrameRenderer
from app.production.program_output import program_output
from app.ui.theme import COLOR_PROGRAM_LIVE, COLOR_BORDER

try:
    from PySide6.QtCore import Qt, QRect
    from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPixmap
    from PySide6.QtWidgets import QWidget
    HAS_QT = True
except ImportError:
    HAS_QT = False


class ProgramWidget(QWidget):
    """Viewport displaying the live broadcast airing on PROGRAM."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setMinimumSize(320, 180)
        self._current_pixmap: Optional[QPixmap] = None
        self._source_name: str = "PROGRAM LIVE"

    def update_frame(self, frame: Optional[VideoFrame]) -> None:
        src = program_output.current_source
        self._source_name = src.name.upper() if src else "BLACK"

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

        # 16:9 Aspect ratio
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
            painter.fillRect(disp_rect, QColor(12, 10, 14))
            painter.setPen(QColor(120, 50, 60))
            painter.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            painter.drawText(disp_rect, Qt.AlignmentFlag.AlignCenter, "PROGRAM OUTPUT [BLACK]")

        # Red Tally Frame (PROGRAM LIVE indicator)
        tally_pen = QPen(QColor(COLOR_PROGRAM_LIVE), 3)
        painter.setPen(tally_pen)
        painter.drawRect(disp_rect)

        # Header Badge: PROGRAM LIVE
        badge_w, badge_h = 130, 22
        badge_rect = QRect(x + 8, y + 8, badge_w, badge_h)
        painter.fillRect(badge_rect, QColor(255, 46, 77, 230))
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Black))
        painter.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, "● PROGRAM LIVE")

        # Source Name Footer Badge
        name_rect = QRect(x + 8, y + disp_h - 26, disp_w - 16, 20)
        painter.fillRect(name_rect, QColor(10, 12, 16, 210))
        painter.setPen(QColor(255, 230, 230))
        painter.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold))
        painter.drawText(name_rect.adjusted(8, 0, 0, 0), Qt.AlignmentFlag.AlignVCenter, f"LIVE FEED: {self._source_name}")
