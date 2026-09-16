"""
Transport controls for video clip playback (Play, Pause, Stop, Loop, Seek).
"""

from typing import Optional
from app.media.video_source import VideoSource
from app.production.preview_output import preview_output

try:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QSlider
    HAS_QT = True
except ImportError:
    HAS_QT = False


class TransportControls(QWidget):
    """Media clip transport bar."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.play_btn = QPushButton("▶ PLAY")
        self.play_btn.clicked.connect(self._on_play)
        layout.addWidget(self.play_btn)

        self.pause_btn = QPushButton("⏸ PAUSE")
        self.pause_btn.clicked.connect(self._on_pause)
        layout.addWidget(self.pause_btn)

        self.loop_btn = QPushButton("🔁 LOOP: ON")
        self.loop_btn.clicked.connect(self._on_loop_toggle)
        layout.addWidget(self.loop_btn)

    def _get_active_video(self) -> Optional[VideoSource]:
        src = preview_output.current_source
        if isinstance(src, VideoSource):
            return src
        return None

    def _on_play(self) -> None:
        vid = self._get_active_video()
        if vid:
            vid.play()

    def _on_pause(self) -> None:
        vid = self._get_active_video()
        if vid:
            vid.pause()

    def _on_loop_toggle(self) -> None:
        vid = self._get_active_video()
        if vid:
            vid.loop = not vid.loop
            self.loop_btn.setText(f"🔁 LOOP: {'ON' if vid.loop else 'OFF'}")
