"""
Recording setup configuration dialog.
"""

from pathlib import Path
from typing import Optional
from app.core.config import config_manager
from app.core.paths import paths
from app.recording.recorder import recorder
from app.recording.recording_config import RecordingProfile

try:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import (
        QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
        QComboBox, QSpinBox, QPushButton, QFormLayout, QFileDialog
    )
    HAS_QT = True
except ImportError:
    HAS_QT = False


class RecordDialog(QDialog):
    """Local recording output configuration dialog."""

    def __init__(self, parent: Optional[QDialog] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Recording Setup — VJ Studio")
        self.setFixedSize(500, 300)
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        form = QFormLayout()
        form.setSpacing(10)

        cfg = config_manager.config.recording

        # Output folder row
        path_row = QHBoxLayout()
        self.path_edit = QLineEdit(str(paths.default_recordings_dir))
        path_row.addWidget(self.path_edit)

        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self._browse_dir)
        path_row.addWidget(self.browse_btn)
        form.addRow("Output Folder:", path_row)

        self.format_combo = QComboBox()
        self.format_combo.addItems(["mp4", "mkv"])
        self.format_combo.setCurrentText(cfg.format)
        form.addRow("Recording Format:", self.format_combo)

        self.bitrate_spin = QSpinBox()
        self.bitrate_spin.setRange(2000, 50000)
        self.bitrate_spin.setValue(cfg.video_bitrate_kbps)
        self.bitrate_spin.setSuffix(" Kbps")
        form.addRow("Video Bitrate:", self.bitrate_spin)

        layout.addLayout(form)
        layout.addStretch()

        btn_row = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(self.cancel_btn)

        self.start_btn = QPushButton("START RECORDING NOW")
        self.start_btn.setStyleSheet("background-color: #FF2E4D; color: white; font-weight: bold;")
        self.start_btn.clicked.connect(self._start_recording)
        btn_row.addWidget(self.start_btn)

        layout.addLayout(btn_row)

    def _browse_dir(self) -> None:
        dir_path = QFileDialog.getExistingDirectory(self, "Select Recording Folder", self.path_edit.text())
        if dir_path:
            self.path_edit.setText(dir_path)

    def _start_recording(self) -> None:
        prof = RecordingProfile(
            output_dir=Path(self.path_edit.text()),
            format=self.format_combo.currentText(),
            video_bitrate_kbps=self.bitrate_spin.value(),
        )
        recorder.start_recording(prof)
        self.accept()
