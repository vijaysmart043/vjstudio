"""
Preview bus output controller.
"""

from typing import Optional
from app.core.events import events, EVENT_INPUT_SELECTED_PREVIEW
from app.core.logger import logger
from app.media.frame import VideoFrame
from app.media.media_source import MediaSource
from app.production.input_manager import input_manager


class PreviewOutput:
    """Manages the source currently cued on the PREVIEW bus (Green Tally)."""

    _instance = None

    def __init__(self) -> None:
        self._current_source_id: Optional[str] = None

    @classmethod
    def get_instance(cls) -> "PreviewOutput":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def select_source(self, source_id: str) -> bool:
        src = input_manager.get_source(source_id)
        if src:
            self._current_source_id = source_id
            logger.info(f"Cued on Preview: {src.name} [{source_id}]")
            events.publish(EVENT_INPUT_SELECTED_PREVIEW, source_id)
            return True
        return False

    @property
    def current_source_id(self) -> Optional[str]:
        return self._current_source_id

    @property
    def current_source(self) -> Optional[MediaSource]:
        if self._current_source_id:
            return input_manager.get_source(self._current_source_id)
        return None

    def get_frame(self) -> Optional[VideoFrame]:
        src = self.current_source
        if src and src.enabled:
            return src.get_frame()
        return None


preview_output = PreviewOutput.get_instance()
