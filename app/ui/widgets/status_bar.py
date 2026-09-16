"""
Broadcast Production Status Bar monitoring live telemetry, encoding, and recording.
"""

import time
from typing import Optional
from app.core.constants import StreamState, RecordState
from app.core.events import events, EVENT_STREAM_STATE_CHANGED, EVENT_RECORD_STATE_CHANGED
from app.recording.recorder import recorder
from app.streaming.streamer import streaming_coordinator
from app.ui.theme import COLOR_SURFACE_DARK, COLOR_BORDER, COLOR_PROGRAM_LIVE, COLOR_PREVIEW_CUE

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel
    HAS_QT = True
except ImportError:
    HAS_QT = False


class BroadcastStatusBar(QFrame):
    """System telemetry and transmission status footer."""

    def __init__(self, parent: Optional[QFrame] = None) -> None:
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setStyleSheet(f"background-color: {COLOR_SURFACE_DARK}; border-top: 1px solid {COLOR_BORDER}; padding: 2px 10px;")
        self._init_ui()
        self._subscribe_events()

    def _init_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(20)

        # 1. LIVE Stream Indicator
        self.live_indicator = QLabel("● LIVE: OFF")
        self.live_indicator.setStyleSheet("font-weight: bold; color: #64748B;")
        layout.addWidget(self.live_indicator)

        # 2. RECORD Indicator
        self.record_indicator = QLabel("■ REC: OFF")
        self.record_indicator.setStyleSheet("font-weight: bold; color: #64748B;")
        layout.addWidget(self.record_indicator)

        # 3. FPS
        self.fps_label = QLabel("FPS: 60")
        self.fps_label.setStyleSheet("color: #94A3B8;")
        layout.addWidget(self.fps_label)

        # 4. CPU usage
        self.cpu_label = QLabel("CPU: 0%")
        self.cpu_label.setStyleSheet("color: #94A3B8;")
        layout.addWidget(self.cpu_label)

        # 5. GPU usage
        self.gpu_label = QLabel("GPU: --")
        self.gpu_label.setStyleSheet("color: #94A3B8;")
        layout.addWidget(self.gpu_label)

        # 6. Dropped frames
        self.dropped_label = QLabel("DROPPED: 0")
        self.dropped_label.setStyleSheet("color: #94A3B8;")
        layout.addWidget(self.dropped_label)

        layout.addStretch()

        # Session Timecode Clock
        self.timecode_label = QLabel("00:00:00")
        self.timecode_label.setStyleSheet("font-family: 'Consolas', monospace; font-size: 13px; font-weight: bold; color: #00E676;")
        layout.addWidget(self.timecode_label)

    def _subscribe_events(self) -> None:
        events.subscribe(EVENT_STREAM_STATE_CHANGED, self._on_stream_state)
        events.subscribe(EVENT_RECORD_STATE_CHANGED, self._on_record_state)

    def _on_stream_state(self, state: StreamState) -> None:
        if state == StreamState.LIVE:
            self.live_indicator.setText("● LIVE")
            self.live_indicator.setStyleSheet(f"font-weight: bold; color: {COLOR_PROGRAM_LIVE};")
        else:
            self.live_indicator.setText("● LIVE: OFF")
            self.live_indicator.setStyleSheet("font-weight: bold; color: #64748B;")

    def _on_record_state(self, state: RecordState) -> None:
        if state == RecordState.RECORDING:
            self.record_indicator.setText("■ REC")
            self.record_indicator.setStyleSheet(f"font-weight: bold; color: {COLOR_PROGRAM_LIVE};")
        else:
            self.record_indicator.setText("■ REC: OFF")
            self.record_indicator.setStyleSheet("font-weight: bold; color: #64748B;")

    def update_telemetry(self) -> None:
        """Called periodically by main UI timer."""
        if HAS_PSUTIL:
            try:
                cpu = psutil.cpu_percent()
                self.cpu_label.setText(f"CPU: {int(cpu)}%")
            except Exception:
                pass

        # Timecode
        now_str = time.strftime("%H:%M:%S")
        self.timecode_label.setText(now_str)
