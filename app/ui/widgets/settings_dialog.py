"""
Application settings dialog with tabbed configuration panels.
"""

from typing import Optional
from app.core.config import config_manager
from app.ffmpeg.ffmpeg_manager import ffmpeg_manager

try:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import (
        QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
        QComboBox, QSpinBox, QPushButton, QFormLayout, QTabWidget,
        QWidget, QTextEdit, QCheckBox
    )
    HAS_QT = True
except ImportError:
    HAS_QT = False


class SettingsDialog(QDialog):
    """Broadcast studio settings dialog."""

    def __init__(self, parent: Optional[QDialog] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Preferences & System Settings — VJ Studio")
        self.resize(600, 440)
        self._init_ui()

    def _init_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        self.tabs = QTabWidget()

        # Tab 1: Video
        video_tab = QWidget()
        v_form = QFormLayout(video_tab)
        self.res_combo = QComboBox()
        self.res_combo.addItems(["1920x1080 (1080p)", "1280x720 (720p)", "3840x2160 (4K UHD)"])
        v_form.addRow("Base Canvas Resolution:", self.res_combo)

        self.fps_combo = QComboBox()
        self.fps_combo.addItems(["60", "50", "30", "25", "24"])
        self.fps_combo.setCurrentText(str(config_manager.config.video.fps))
        v_form.addRow("Broadcast Output FPS:", self.fps_combo)

        self.gpu_check = QCheckBox("Enable GPU Hardware Acceleration")
        self.gpu_check.setChecked(config_manager.config.video.gpu_acceleration)
        v_form.addRow("", self.gpu_check)
        self.tabs.addTab(video_tab, "Video")

        # Tab 2: Audio
        audio_tab = QWidget()
        a_form = QFormLayout(audio_tab)
        self.sr_combo = QComboBox()
        self.sr_combo.addItems(["48000 Hz (Broadcast standard)", "44100 Hz (CD audio)"])
        a_form.addRow("Audio Sample Rate:", self.sr_combo)
        self.tabs.addTab(audio_tab, "Audio")

        # Tab 3: FFmpeg & Hardware Encoders
        ff_tab = QWidget()
        ff_layout = QVBoxLayout(ff_tab)
        ff_desc = QLabel("FFMPEG SYSTEM DIAGNOSTICS & ENCODER PROBE:")
        ff_desc.setStyleSheet("font-weight: bold; color: #70B8FF;")
        ff_layout.addWidget(ff_desc)

        diag_text = QTextEdit()
        diag_text.setReadOnly(True)
        diag = ffmpeg_manager.get_diagnostics()
        diag_lines = [f"• {k}: {v}" for k, v in diag.items()]
        diag_text.setText("\n".join(diag_lines))
        ff_layout.addWidget(diag_text)
        self.tabs.addTab(ff_tab, "FFmpeg Diagnostics")

        # Tab 4: Hotkeys
        hk_tab = QWidget()
        hk_form = QFormLayout(hk_tab)
        hk_form.addRow("Instant Cut:", QLabel("C"))
        hk_form.addRow("Auto Fade:", QLabel("F"))
        hk_form.addRow("Dissolve:", QLabel("D"))
        hk_form.addRow("Toggle Live Stream:", QLabel("Space"))
        hk_form.addRow("Toggle Recording:", QLabel("R"))
        hk_form.addRow("Cue Inputs 1-4:", QLabel("F1, F2, F3, F4"))
        hk_form.addRow("Cue Scenes 1-2:", QLabel("F5, F6"))
        self.tabs.addTab(hk_tab, "Hotkeys")

        main_layout.addWidget(self.tabs)

        # Action buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.close_btn = QPushButton("Done")
        self.close_btn.clicked.connect(self.accept)
        btn_row.addWidget(self.close_btn)

        main_layout.addLayout(btn_row)
