"""
Broadcast Audio Mixer widget featuring multi-channel faders and live dB level meters.
"""

from typing import Dict, List, Optional
from app.audio.audio_mixer import audio_mixer
from app.audio.audio_source import AudioChannel
from app.ui.theme import COLOR_SURFACE_CARD, COLOR_BORDER, COLOR_PROGRAM_LIVE

try:
    from PySide6.QtCore import Qt, QRect
    from PySide6.QtGui import QPainter, QColor, QBrush, QLinearGradient
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider,
        QPushButton, QFrame
    )
    HAS_QT = True
except ImportError:
    HAS_QT = False


class MeterBar(QWidget):
    """Dual-channel (L/R) stereo LED audio peak meter."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setFixedWidth(20)
        self.setMinimumHeight(90)
        self.level_l = 0.0
        self.level_r = 0.0

    def set_levels(self, l: float, r: float) -> None:
        self.level_l = l
        self.level_r = r
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        w = self.width()
        h = self.height()

        # Background track
        painter.fillRect(0, 0, w, h, QColor(16, 18, 22))

        ch_w = (w - 4) // 2

        # Draw left and right channels
        for idx, lvl in enumerate([self.level_l, self.level_r]):
            x = 2 + idx * (ch_w + 1)
            meter_h = int(lvl * h)
            y = h - meter_h

            # Segmented broadcast gradient: Green (-60 to -12 dB), Yellow (-12 to -3 dB), Red (clip)
            gradient = QLinearGradient(x, h, x, 0)
            gradient.setColorAt(0.0, QColor(0, 230, 118))   # Green
            gradient.setColorAt(0.7, QColor(255, 179, 0))   # Yellow / Amber
            gradient.setColorAt(0.9, QColor(255, 46, 77))   # Red Peak
            painter.fillRect(x, y, ch_w, meter_h, QBrush(gradient))


class ChannelStrip(QFrame):
    """Single vertical audio fader strip for an audio source."""

    def __init__(self, channel: AudioChannel, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.channel = channel
        self.setObjectName("Card")
        self.setFixedWidth(80)
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 8, 6, 8)
        layout.setSpacing(6)

        # Label
        self.name_label = QLabel(self.channel.name)
        self.name_label.setStyleSheet("font-size: 10px; font-weight: bold; color: #FFFFFF;")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label)

        # Meter & Fader row
        mid_row = QHBoxLayout()
        mid_row.setContentsMargins(0, 0, 0, 0)
        mid_row.setSpacing(4)

        # Vertical Slider
        self.fader = QSlider(Qt.Orientation.Vertical)
        self.fader.setRange(0, 100)
        self.fader.setValue(int(self.channel.volume * 100))
        self.fader.valueChanged.connect(self._on_volume_changed)
        mid_row.addWidget(self.fader)

        # LED Meter
        self.meter = MeterBar()
        mid_row.addWidget(self.meter)

        layout.addLayout(mid_row)

        # Mute button
        self.mute_btn = QPushButton("MUTE")
        self.mute_btn.setFixedHeight(22)
        self.mute_btn.setStyleSheet(
            "font-size: 9px; font-weight: bold; padding: 2px 4px; border-radius: 3px; background-color: #242933;"
        )
        self.mute_btn.clicked.connect(self._on_mute_toggle)
        layout.addWidget(self.mute_btn)

    def _on_volume_changed(self, val: int) -> None:
        audio_mixer.set_volume(self.channel.id, val / 100.0)

    def _on_mute_toggle(self) -> None:
        is_muted = audio_mixer.toggle_mute(self.channel.id)
        if is_muted:
            self.mute_btn.setStyleSheet(
                "font-size: 9px; font-weight: bold; padding: 2px 4px; border-radius: 3px; "
                "background-color: #FF2E4D; color: white;"
            )
        else:
            self.mute_btn.setStyleSheet(
                "font-size: 9px; font-weight: bold; padding: 2px 4px; border-radius: 3px; "
                "background-color: #242933; color: #F3F5F7;"
            )

    def update_meter(self) -> None:
        self.meter.set_levels(self.channel.peak_level_l, self.channel.peak_level_r)


class AudioMixerWidget(QFrame):
    """Audio mixer panel housing all channel strips."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("Panel")
        self._strips: Dict[str, ChannelStrip] = {}
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)

        # Header
        header = QHBoxLayout()
        title = QLabel("AUDIO MIXER")
        title.setObjectName("SectionTitle")
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)

        # Channel Strips Container
        strips_row = QHBoxLayout()
        strips_row.setContentsMargins(0, 0, 0, 0)
        strips_row.setSpacing(8)

        for ch in audio_mixer.get_channels():
            strip = ChannelStrip(ch)
            self._strips[ch.id] = strip
            strips_row.addWidget(strip)

        layout.addLayout(strips_row)

    def update_meters(self) -> None:
        for strip in self._strips.values():
            strip.update_meter()
