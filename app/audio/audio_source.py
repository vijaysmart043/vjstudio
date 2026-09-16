"""
Audio channel representation with volume, mute, gain, and stereo balance.
"""

from dataclasses import dataclass, field


@dataclass
class AudioChannel:
    id: str
    name: str
    volume: float = 0.8  # 0.0 to 1.0
    muted: bool = False
    gain_db: float = 0.0  # -20 dB to +20 dB
    pan: float = 0.0  # -1.0 (Left) to +1.0 (Right)
    peak_level_l: float = 0.0  # 0.0 to 1.0 (meter reading)
    peak_level_r: float = 0.0
