"""
Broadcast Input Card button showing live thumbnail, type badge, and active tally status.
"""

from typing import Optional
from app.core.constants import SourceType
from app.media.media_source import MediaSource
from app.production.preview_output import preview_output
from app.production.program_output import program_output
from app.ui.theme import COLOR_PREVIEW_CUE, COLOR_PROGRAM_LIVE, COLOR_SURFACE_CARD, COLOR_BORDER

try:
    from PySide6.QtCore import Qt, Signal
    from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
    HAS_QT = True
except ImportError:
    HAS_QT = False


class SourceButton(QFrame):
    """Interactive input card widget representing a media source."""

    clicked = Signal(str)  # Emits source_id when clicked

    def __init__(self, source: MediaSource, parent: Optional[QFrame] = None) -> None:
        super().__init__(parent)
        self.source = source
        self.setObjectName("Card")
        self.setFixedHeight(84)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._init_ui()
        self.refresh_tally()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)

        # Top row: Type badge and ID tag
        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)

        self.type_badge = QLabel(self.source.type.value.upper())
        self.type_badge.setStyleSheet(
            "background-color: #262D3D; color: #70B8FF; font-size: 9px; font-weight: bold; "
            "padding: 2px 6px; border-radius: 3px;"
        )
        top_row.addWidget(self.type_badge)
        top_row.addStretch()

        self.tally_badge = QLabel("")
        self.tally_badge.setStyleSheet("font-size: 9px; font-weight: 800; padding: 2px 6px; border-radius: 3px;")
        self.tally_badge.setVisible(False)
        top_row.addWidget(self.tally_badge)

        layout.addLayout(top_row)

        # Main source name label
        self.name_label = QLabel(self.source.name)
        self.name_label.setStyleSheet("font-size: 13px; font-weight: 700; color: #FFFFFF;")
        layout.addWidget(self.name_label)

        # Bottom info row: resolution and audio state
        audio_text = "🔊 AUDIO" if self.source.audio_enabled else "🔇 MUTE"
        info_label = QLabel(f"{self.source.width}x{self.source.height} • {audio_text}")
        info_label.setStyleSheet("font-size: 10px; color: #7F8B9E;")
        layout.addWidget(info_label)

    def refresh_tally(self) -> None:
        """Update visual border and badge based on Preview / Program state."""
        sid = self.source.id
        is_program = (program_output.current_source_id == sid)
        is_preview = (preview_output.current_source_id == sid)

        if is_program:
            self.setStyleSheet(f"QFrame#Card {{ background-color: #2D1418; border: 2px solid {COLOR_PROGRAM_LIVE}; border-radius: 6px; }}")
            self.tally_badge.setText("LIVE")
            self.tally_badge.setStyleSheet("background-color: #FF2E4D; color: #FFFFFF; font-size: 9px; font-weight: 800; border-radius: 3px;")
            self.tally_badge.setVisible(True)
        elif is_preview:
            self.setStyleSheet(f"QFrame#Card {{ background-color: #12281E; border: 2px solid {COLOR_PREVIEW_CUE}; border-radius: 6px; }}")
            self.tally_badge.setText("PREVIEW")
            self.tally_badge.setStyleSheet("background-color: #00E676; color: #000000; font-size: 9px; font-weight: 800; border-radius: 3px;")
            self.tally_badge.setVisible(True)
        else:
            self.setStyleSheet("QFrame#Card { background-color: #1D212A; border: 1px solid #2B3240; border-radius: 6px; }")
            self.tally_badge.setVisible(False)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.source.id)
        super().mousePressEvent(event)
