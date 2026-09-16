"""
Stream setup configuration dialog.
"""

from typing import Optional
from app.commands.command_bus import command_bus
from app.core.config import config_manager
from app.streaming.stream_config import StreamProfile
from app.streaming.streamer import streaming_coordinator

try:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import (
        QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
        QComboBox, QSpinBox, QPushButton, QFormLayout
    )
    HAS_QT = True
except ImportError:
    HAS_QT = False


class StreamDialog(QDialog):
    """Quick Stream Configuration & Broadcast Trigger dialog."""

    def __init__(self, parent: Optional[QDialog] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("RTMP Streaming Setup — VJ Studio")
        self.setFixedSize(480, 320)
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        form = QFormLayout()
        form.setSpacing(10)

        cfg = config_manager.config.streaming

        self.service_combo = QComboBox()
        self.service_combo.addItems(["Custom RTMP", "YouTube Live", "Twitch", "Facebook Live", "Kick"])
        form.addRow("Streaming Service:", self.service_combo)

        self.url_edit = QLineEdit(cfg.server_url)
        form.addRow("Server URL:", self.url_edit)

        self.key_edit = QLineEdit(cfg.stream_key)
        self.key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_edit.setPlaceholderText("Paste stream key here")
        form.addRow("Stream Key:", self.key_edit)

        self.bitrate_spin = QSpinBox()
        self.bitrate_spin.setRange(1000, 20000)
        self.bitrate_spin.setValue(cfg.video_bitrate_kbps)
        self.bitrate_spin.setSuffix(" Kbps")
        form.addRow("Video Bitrate:", self.bitrate_spin)

        layout.addLayout(form)
        layout.addStretch()

        btn_row = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(self.cancel_btn)

        self.save_btn = QPushButton("Save Settings")
        self.save_btn.clicked.connect(self._save_settings)
        btn_row.addWidget(self.save_btn)

        self.start_btn = QPushButton("START STREAM NOW")
        self.start_btn.setStyleSheet("background-color: #00E676; color: black; font-weight: bold;")
        self.start_btn.clicked.connect(self._start_stream)
        btn_row.addWidget(self.start_btn)

        layout.addLayout(btn_row)

    def _save_settings(self) -> None:
        cfg = config_manager.config.streaming
        cfg.server_url = self.url_edit.text()
        cfg.stream_key = self.key_edit.text()
        cfg.video_bitrate_kbps = self.bitrate_spin.value()
        config_manager.save()
        self.accept()

    def _start_stream(self) -> None:
        self._save_settings()
        prof = StreamProfile(
            server_url=self.url_edit.text(),
            stream_key=self.key_edit.text(),
            video_bitrate_kbps=self.bitrate_spin.value(),
        )
        streaming_coordinator.start_stream(prof)
        self.accept()
