"""
Master audio mixing engine managing input channels and master bus.
"""

import random
from typing import Dict, List, Optional
from app.audio.audio_meter import AudioMeter
from app.audio.audio_source import AudioChannel
from app.core.events import events, EVENT_AUDIO_LEVELS_UPDATED
from app.core.logger import logger


class AudioMixer:
    """Manages audio channels (Mic 1, Mic 2, System, Master) and simulated/real metering."""

    _instance = None

    def __init__(self) -> None:
        self._channels: Dict[str, AudioChannel] = {}
        self._init_default_channels()

    @classmethod
    def get_instance(cls) -> "AudioMixer":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _init_default_channels(self) -> None:
        channels = [
            AudioChannel("mic_1", "MIC 1", volume=0.85),
            AudioChannel("mic_2", "MIC 2", volume=0.75),
            AudioChannel("system", "SYSTEM", volume=0.80),
            AudioChannel("master", "MASTER", volume=0.90),
        ]
        for ch in channels:
            self._channels[ch.id] = ch

    def get_channels(self) -> List[AudioChannel]:
        return list(self._channels.values())

    def get_channel(self, channel_id: str) -> Optional[AudioChannel]:
        return self._channels.get(channel_id)

    def set_volume(self, channel_id: str, volume: float) -> None:
        ch = self.get_channel(channel_id)
        if ch:
            ch.volume = max(0.0, min(1.0, volume))

    def set_mute(self, channel_id: str, muted: bool) -> None:
        ch = self.get_channel(channel_id)
        if ch:
            ch.muted = muted

    def toggle_mute(self, channel_id: str) -> bool:
        ch = self.get_channel(channel_id)
        if ch:
            ch.muted = not ch.muted
            return ch.muted
        return False

    def update_levels(self) -> None:
        """Called periodically by production timer to refresh meters smoothly."""
        for ch in self._channels.values():
            if ch.muted or ch.volume <= 0.01:
                target_l, target_r = 0.0, 0.0
            else:
                # Dynamic broadcast vocal/music level simulation based on channel volume
                base = ch.volume * 0.75
                jitter = (random.random() - 0.5) * 0.25
                target_l = max(0.0, min(0.98, base + jitter))
                target_r = max(0.0, min(0.98, base + jitter * 0.9))

            ch.peak_level_l = AudioMeter.smooth_decay(ch.peak_level_l, target_l, 0.08)
            ch.peak_level_r = AudioMeter.smooth_decay(ch.peak_level_r, target_r, 0.08)

        events.publish(EVENT_AUDIO_LEVELS_UPDATED, self._channels)


audio_mixer = AudioMixer.get_instance()
