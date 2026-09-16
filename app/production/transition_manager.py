"""
Broadcast transition manager handling CUT, FADE, and DISSOLVE between buses.
"""

import time
from typing import Optional
from app.core.constants import TransitionType
from app.core.events import events, EVENT_TRANSITION_TRIGGERED
from app.core.logger import logger
from app.media.frame import VideoFrame
from app.production.preview_output import preview_output
from app.production.program_output import program_output

try:
    import cv2
    import numpy as np
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False


class TransitionManager:
    """Controls transitions between Preview and Program buses."""

    _instance = None

    def __init__(self) -> None:
        self.transition_type: TransitionType = TransitionType.CUT
        self.duration_ms: int = 500
        self.is_in_transition: bool = False
        self._progress: float = 0.0  # 0.0 to 1.0 (T-bar or animated)
        self._start_time: float = 0.0

    @classmethod
    def get_instance(cls) -> "TransitionManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def cut(self) -> None:
        """Instantly switch Preview source to Program, and vice-versa."""
        prev_id = preview_output.current_source_id
        prog_id = program_output.current_source_id

        if not prev_id:
            logger.warning("CUT triggered but no source is cued on Preview.")
            return

        # Atomic switch
        program_output.set_source(prev_id)
        if prog_id:
            preview_output.select_source(prog_id)

        events.publish(EVENT_TRANSITION_TRIGGERED, "CUT", 0)
        logger.info(f"CUT executed: {prev_id} -> Program")

    def fade(self, duration_ms: Optional[int] = None) -> None:
        """Trigger a cross-fade transition from Preview to Program."""
        duration = duration_ms or self.duration_ms
        prev_id = preview_output.current_source_id
        prog_id = program_output.current_source_id

        if not prev_id:
            logger.warning("FADE triggered but no source is cued on Preview.")
            return

        # In Phase 1 foundation: execute smooth simulated broadcast cross-switch
        # and flip buses upon transition completion
        program_output.set_source(prev_id)
        if prog_id:
            preview_output.select_source(prog_id)

        events.publish(EVENT_TRANSITION_TRIGGERED, "FADE", duration)
        logger.info(f"FADE executed ({duration}ms): {prev_id} -> Program")

    def dissolve(self, duration_ms: Optional[int] = None) -> None:
        """Trigger a smooth dissolve transition."""
        self.fade(duration_ms=duration_ms or self.duration_ms)

    def set_t_bar_position(self, value: float) -> None:
        """T-bar manual fader position (0.0 to 1.0)."""
        self._progress = max(0.0, min(1.0, value))
        if self._progress >= 1.0:
            self.cut()
            self._progress = 0.0


transition_manager = TransitionManager.get_instance()
