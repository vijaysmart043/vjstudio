"""
Application event signals and observer bus.
"""

from typing import Any, Callable, Dict, List
from app.core.constants import StreamState, RecordState, TransitionType
from app.core.logger import logger


class EventBus:
    """Thread-safe generic event dispatcher for VJ Studio."""

    _instance = None

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable[..., Any]]] = {}

    @classmethod
    def get_instance(cls) -> "EventBus":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def subscribe(self, event_name: str, callback: Callable[..., Any]) -> None:
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        if callback not in self._subscribers[event_name]:
            self._subscribers[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable[..., Any]) -> None:
        if event_name in self._subscribers and callback in self._subscribers[event_name]:
            self._subscribers[event_name].remove(callback)

    def publish(self, event_name: str, *args: Any, **kwargs: Any) -> None:
        if event_name in self._subscribers:
            for cb in list(self._subscribers[event_name]):
                try:
                    cb(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error handling event '{event_name}': {e}", exc_info=True)


events = EventBus.get_instance()

# Standard Event Name Constants
EVENT_INPUT_SELECTED_PREVIEW = "input.selected.preview"
EVENT_INPUT_SELECTED_PROGRAM = "input.selected.program"
EVENT_INPUT_ADDED = "input.added"
EVENT_INPUT_REMOVED = "input.removed"
EVENT_SCENE_CHANGED = "scene.changed"
EVENT_TRANSITION_TRIGGERED = "transition.triggered"
EVENT_STREAM_STATE_CHANGED = "stream.state_changed"
EVENT_RECORD_STATE_CHANGED = "record.state_changed"
EVENT_AUDIO_LEVELS_UPDATED = "audio.levels_updated"
EVENT_PERFORMANCE_METRICS_UPDATED = "metrics.updated"
