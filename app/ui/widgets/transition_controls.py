"""
Broadcast transition bar containing CUT, FADE, DISSOLVE triggers and manual T-Bar.
"""

from typing import Optional
from app.commands.command_bus import command_bus
from app.production.transition_manager import transition_manager
from app.ui.theme import COLOR_PROGRAM_LIVE, COLOR_PRIMARY_ACCENT, COLOR_BORDER

try:
    from PySide6.QtCore import Qt, Signal
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
        QSpinBox, QLabel, QSlider, QFrame
    )
    HAS_QT = True
except ImportError:
    HAS_QT = False


class TransitionControls(QFrame):
    """Production transition switcher panel."""

    transition_executed = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("Panel")
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(10)

        # Header
        title = QLabel("TRANSITIONS")
        title.setObjectName("SectionTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Primary Switch Buttons (CUT, FADE, DISSOLVE)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.cut_btn = QPushButton("CUT")
        self.cut_btn.setObjectName("CutButton")
        self.cut_btn.setMinimumHeight(38)
        self.cut_btn.clicked.connect(self._on_cut)
        btn_layout.addWidget(self.cut_btn)

        self.fade_btn = QPushButton("AUTO FADE")
        self.fade_btn.setObjectName("TransitionButton")
        self.fade_btn.setMinimumHeight(38)
        self.fade_btn.clicked.connect(self._on_fade)
        btn_layout.addWidget(self.fade_btn)

        self.dissolve_btn = QPushButton("DISSOLVE")
        self.dissolve_btn.setObjectName("TransitionButton")
        self.dissolve_btn.setMinimumHeight(38)
        self.dissolve_btn.clicked.connect(self._on_dissolve)
        btn_layout.addWidget(self.dissolve_btn)

        layout.addLayout(btn_layout)

        # Duration setting row
        dur_row = QHBoxLayout()
        dur_label = QLabel("Duration:")
        dur_label.setStyleSheet("color: #94A3B8; font-weight: bold;")
        dur_row.addWidget(dur_label)

        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(100, 3000)
        self.duration_spin.setSingleStep(50)
        self.duration_spin.setValue(500)
        self.duration_spin.setSuffix(" ms")
        self.duration_spin.valueChanged.connect(self._on_duration_changed)
        dur_row.addWidget(self.duration_spin)
        dur_row.addStretch()

        layout.addLayout(dur_row)

        # T-Bar Fader
        tbar_label = QLabel("T-BAR MANUAL FADER")
        tbar_label.setStyleSheet("color: #64748B; font-size: 10px; font-weight: bold;")
        tbar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(tbar_label)

        self.tbar = QSlider(Qt.Orientation.Horizontal)
        self.tbar.setRange(0, 100)
        self.tbar.setValue(0)
        self.tbar.valueChanged.connect(self._on_tbar_moved)
        self.tbar.sliderReleased.connect(self._on_tbar_released)
        layout.addWidget(self.tbar)

    def _on_cut(self) -> None:
        command_bus.execute("cut")
        self.transition_executed.emit()

    def _on_fade(self) -> None:
        dur = self.duration_spin.value()
        command_bus.execute("fade", dur)
        self.transition_executed.emit()

    def _on_dissolve(self) -> None:
        dur = self.duration_spin.value()
        command_bus.execute("dissolve", dur)
        self.transition_executed.emit()

    def _on_duration_changed(self, val: int) -> None:
        transition_manager.duration_ms = val

    def _on_tbar_moved(self, val: int) -> None:
        progress = val / 100.0
        transition_manager.set_t_bar_position(progress)

    def _on_tbar_released(self) -> None:
        if self.tbar.value() > 90:
            self._on_cut()
        self.tbar.setValue(0)
