"""
Central registry and lifecycle manager for all project inputs and media sources.
"""

from typing import Dict, List, Optional
from app.core.constants import SourceType
from app.core.events import events, EVENT_INPUT_ADDED, EVENT_INPUT_REMOVED
from app.core.logger import logger
from app.media.media_source import MediaSource
from app.media.camera import CameraSource
from app.media.screen_capture import ScreenCaptureSource


class InputManager:
    """Stores, discovers, and tracks all media inputs available for production."""

    _instance = None

    def __init__(self) -> None:
        self._sources: Dict[str, MediaSource] = {}
        self._source_order: List[str] = []

    @classmethod
    def get_instance(cls) -> "InputManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def add_source(self, source: MediaSource) -> str:
        """Register a new media source and start its frame ingestion."""
        self._sources[source.id] = source
        if source.id not in self._source_order:
            self._source_order.append(source.id)

        source.start()
        logger.info(f"Registered input: {source.name} (id={source.id}, type={source.type.value})")
        events.publish(EVENT_INPUT_ADDED, source)
        return source.id

    def remove_source(self, source_id: str) -> bool:
        if source_id in self._sources:
            src = self._sources.pop(source_id)
            if source_id in self._source_order:
                self._source_order.remove(source_id)
            src.stop()
            logger.info(f"Removed input: {src.name} (id={source_id})")
            events.publish(EVENT_INPUT_REMOVED, source_id)
            return True
        return False

    def get_source(self, source_id: str) -> Optional[MediaSource]:
        return self._sources.get(source_id)

    def get_all_sources(self) -> List[MediaSource]:
        return [self._sources[sid] for sid in self._source_order if sid in self._sources]

    def stop_all(self) -> None:
        for src in self._sources.values():
            src.stop()


input_manager = InputManager.get_instance()
