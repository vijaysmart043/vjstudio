"""
Peak meter mathematics with decay smoothing and clip protection.
"""

import math
from typing import Tuple


class AudioMeter:
    """Calculates RMS and Peak levels in decibels and normalized linear scales."""

    @staticmethod
    def linear_to_db(linear: float) -> float:
        if linear <= 0.00001:
            return -60.0
        return max(-60.0, 20.0 * math.log10(linear))

    @staticmethod
    def db_to_linear(db: float) -> float:
        if db <= -60.0:
            return 0.0
        return math.pow(10.0, db / 20.0)

    @staticmethod
    def smooth_decay(current: float, target: float, decay_rate: float = 0.15) -> float:
        if target > current:
            return target
        return max(0.0, current - decay_rate)
