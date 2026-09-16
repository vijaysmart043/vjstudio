"""
Multiview monitoring component rendering a 2x2 / 3x3 production matrix
for Preview, Program, and all active camera/media sources simultaneously.
"""

from typing import List, Optional
from app.core.logger import logger
from app.media.frame import VideoFrame
from app.production.input_manager import input_manager
from app.production.preview_output import preview_output
from app.production.program_output import program_output

try:
    from PySide6.QtCore import Qt, QTimer
    from PySide6.QtGui import QImage, QPixmap, QPainter, QColor, QFont, QPen
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout,
        QFrame, QSizePolicy
    )
    import cv2
    import numpy as np
    HAS_QT = True
except ImportError:
    HAS_QT = False


class MultiviewCell(QFrame):
    """Single viewport cell in the multiview wall with custom label and tally border."""

    def __init__(self, title: str, tally_color: str = "#3A3F4B", parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.title = title
        self.tally_color = tally_color
        self.setObjectName("MultiviewCell")
        self.setStyleSheet(f"""
            QFrame#MultiviewCell {{
                background-color: #0A0C0E;
                border: 2px solid {self.tally_color};
                border-radius: 4px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(0)

        # Label Header
        self.header = QLabel(title)
        self.header.setStyleSheet(f"""
            background-color: {self.tally_color};
            color: #FFFFFF;
            font-size: 10px;
            font-weight: bold;
            padding: 2px 4px;
        """)
        layout.addWidget(self.header)

        # Display screen
        self.display = QLabel()
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.display.setStyleSheet("background-color: #050607;")
        layout.addWidget(self.display)

    def set_tally(self, color_hex: str, label_text: Optional[str] = None) -> None:
        self.tally_color = color_hex
        if label_text:
            self.header.setText(label_text)
        self.setStyleSheet(f"""
            QFrame#MultiviewCell {{
                background-color: #0A0C0E;
                border: 2px solid {self.tally_color};
                border-radius: 4px;
            }}
        """)
        self.header.setStyleSheet(f"""
            background-color: {self.tally_color};
            color: #FFFFFF;
            font-size: 10px;
            font-weight: bold;
            padding: 2px 4px;
        """)

    def update_frame(self, frame: Optional[VideoFrame]) -> None:
        if frame is None or frame.data is None:
            self.display.clear()
            return

        try:
            h, w, ch = frame.data.shape
            # Fast downscale for multiview tile
            target_w = max(160, self.display.width())
            target_h = max(90, int(target_w * 9 / 16))
            resized = cv2.resize(frame.data, (target_w, target_h), interpolation=cv2.INTER_NEAREST)
            rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            q_img = QImage(rgb.data, target_w, target_h, target_w * 3, QImage.Format.Format_RGB888)
            self.display.setPixmap(QPixmap.fromImage(q_img))
        except Exception:
            pass


class MultiviewWidget(QWidget):
    """Broadcast Multiviewer wall displaying Preview, Program, and inputs in a dense studio grid."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("MultiviewWidget")
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        # 8-channel production multiview matrix
        grid = QGridLayout()
        grid.setSpacing(4)

        # Upper row: Big Preview & Big Program
        self.cell_preview = MultiviewCell("CUE - PREVIEW", tally_color="#00E676")
        grid.addWidget(self.cell_preview, 0, 0, 1, 2)

        self.cell_program = MultiviewCell("LIVE - PROGRAM", tally_color="#FF1744")
        grid.addWidget(self.cell_program, 0, 2, 1, 2)

        # Lower row: 4 Camera/Media inputs
        self.input_cells: List[MultiviewCell] = []
        for i in range(4):
            cell = MultiviewCell(f"INPUT {i+1}", tally_color="#3A3F4B")
            self.input_cells.append(cell)
            grid.addWidget(cell, 1, i)

        layout.addLayout(grid)

    def refresh_multiview(self) -> None:
        """Called on production tick to update all tiles in the multiviewer wall."""
        # 1. Preview
        prev_frame = preview_output.get_frame()
        self.cell_preview.update_frame(prev_frame)

        # 2. Program
        prog_frame = program_output.get_frame()
        self.cell_program.update_frame(prog_frame)

        # 3. Inputs
        sources = input_manager.get_all_sources()
        for idx, cell in enumerate(self.input_cells):
            if idx < len(sources):
                src = sources[idx]
                # Determine tally state
                is_prog = (src.id == program_output.current_source_id)
                is_prev = (src.id == preview_output.current_source_id)
                tally_color = "#FF1744" if is_prog else ("#00E676" if is_prev else "#3A3F4B")
                cell.set_tally(tally_color, f"{src.name} [{src.type.value.upper()}]")
                cell.update_frame(src.get_frame())
            else:
                cell.set_tally("#2A2D34", f"EMPTY {idx+1}")
                cell.update_frame(None)
