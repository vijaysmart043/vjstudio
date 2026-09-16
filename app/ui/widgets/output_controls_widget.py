"""
Dedicated Broadcast Streaming and Recording Control Deck.
Quick-access buttons for Start/Stop Stream, Start/Stop Record, NDI Out, and Virtual Camera.
"""

from typing import Optional
from app.commands.command_bus import command_bus
from app.core.constants import RecordState, StreamState
from app.core.events import events, EVENT_RECORD_STATE_CHANGED, EVENT_STREAM_STATE_CHANGED
from app.production.program_output import program_output
from app.recording.recorder import recorder
from app.streaming.streamer import streaming_coordinator

try:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
    )
    HAS_QT = True
except ImportError:
    HAS_QT = False


class OutputControlsWidget(QWidget):
    """Deck containing master Broadcast Start/Stop controls for Stream, Record, NDI, and Virtual Cam."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._init_ui()
        events.subscribe(EVENT_STREAM_STATE_CHANGED, self._on_stream_state_changed)
        events.subscribe(EVENT_RECORD_STATE_CHANGED, self._on_record_state_changed)

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)

        header = QLabel("MASTER OUTPUT CONTROLS")
        header.setStyleSheet("color: #8E9BAE; font-size: 10px; font-weight: bold; letter-spacing: 1px;")
        layout.addWidget(header)

        # Stream Action Button
        self.stream_btn = QPushButton("START STREAMING")
        self.stream_btn.setFixedHeight(34)
        self.stream_btn.setStyleSheet("""
            QPushButton {
                background-color: #2E7D32;
                color: #FFFFFF;
                font-weight: bold;
                border-radius: 4px;
                border: 1px solid #388E3C;
            }
            QPushButton:hover { background-color: #388E3C; }
        """)
        self.stream_btn.clicked.connect(self._toggle_stream)
        layout.addWidget(self.stream_btn)

        # Record Action Button
        self.record_btn = QPushButton("START RECORDING")
        self.record_btn.setFixedHeight(34)
        self.record_btn.setStyleSheet("""
            QPushButton {
                background-color: #C62828;
                color: #FFFFFF;
                font-weight: bold;
                border-radius: 4px;
                border: 1px solid #D32F2F;
            }
            QPushButton:hover { background-color: #D32F2F; }
        """)
        self.record_btn.clicked.connect(self._toggle_record)
        layout.addWidget(self.record_btn)

        # Secondary Toggles Row (NDI Out, Virtual Cam)
        toggles_layout = QHBoxLayout()
        toggles_layout.setSpacing(4)

        self.ndi_btn = QPushButton("NDI OUT")
        self.ndi_btn.setCheckable(True)
        self.ndi_btn.setFixedHeight(28)
        self.ndi_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E232B;
                color: #8E9BAE;
                font-size: 10px;
                font-weight: bold;
                border-radius: 3px;
                border: 1px solid #2D333F;
            }
            QPushButton:checked {
                background-color: #0084FF;
                color: #FFFFFF;
                border: 1px solid #38A2FF;
            }
        """)
        self.ndi_btn.toggled.connect(self._toggle_ndi)
        toggles_layout.addWidget(self.ndi_btn)

        self.vcam_btn = QPushButton("VIRTUAL CAM")
        self.vcam_btn.setCheckable(True)
        self.vcam_btn.setFixedHeight(28)
        self.vcam_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E232B;
                color: #8E9BAE;
                font-size: 10px;
                font-weight: bold;
                border-radius: 3px;
                border: 1px solid #2D333F;
            }
            QPushButton:checked {
                background-color: #9C27B0;
                color: #FFFFFF;
                border: 1px solid #BA68C8;
            }
        """)
        self.vcam_btn.toggled.connect(self._toggle_vcam)
        toggles_layout.addWidget(self.vcam_btn)

        layout.addLayout(toggles_layout)

    def _toggle_stream(self) -> None:
        if streaming_coordinator.state == StreamState.LIVE:
            command_bus.execute("stop_stream")
        else:
            command_bus.execute("start_stream")

    def _toggle_record(self) -> None:
        if recorder.state == RecordState.RECORDING:
            command_bus.execute("stop_recording")
        else:
            command_bus.execute("start_recording")

    def _toggle_ndi(self, checked: bool) -> None:
        program_output.set_ndi_output_enabled(checked)

    def _toggle_vcam(self, checked: bool) -> None:
        program_output.set_virtual_camera_enabled(checked)

    def _on_stream_state_changed(self, state: StreamState) -> None:
        if state == StreamState.LIVE:
            self.stream_btn.setText("STOP STREAMING")
            self.stream_btn.setStyleSheet("""
                QPushButton {
                    background-color: #D32F2F;
                    color: #FFFFFF;
                    font-weight: bold;
                    border-radius: 4px;
                }
            """)
        else:
            self.stream_btn.setText("START STREAMING")
            self.stream_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2E7D32;
                    color: #FFFFFF;
                    font-weight: bold;
                    border-radius: 4px;
                }
            """)

    def _on_record_state_changed(self, state: RecordState) -> None:
        if state == RecordState.RECORDING:
            self.record_btn.setText("STOP RECORDING")
            self.record_btn.setStyleSheet("""
                QPushButton {
                    background-color: #B71C1C;
                    color: #FFFFFF;
                    font-weight: bold;
                    border-radius: 4px;
                    border: 2px solid #FF5252;
                }
            """)
        else:
            self.record_btn.setText("START RECORDING")
            self.record_btn.setStyleSheet("""
                QPushButton {
                    background-color: #C62828;
                    color: #FFFFFF;
                    font-weight: bold;
                    border-radius: 4px;
                }
            """)
