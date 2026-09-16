"""
Unified command dispatcher decoupling UI, hotkeys, and future AI automation.
"""

from typing import Any, Callable, Dict, Optional
from app.audio.audio_mixer import audio_mixer
from app.core.logger import logger
from app.production.preview_output import preview_output
from app.production.program_output import program_output
from app.production.transition_manager import transition_manager
from app.recording.recorder import recorder
from app.recording.recording_config import RecordingProfile
from app.streaming.streamer import streaming_coordinator
from app.streaming.stream_config import StreamProfile
from app.core.paths import paths


class CommandBus:
    """Dispatches core production actions callable by GUI, hotkeys, or future AI assistant."""

    _instance = None

    def __init__(self) -> None:
        self._handlers: Dict[str, Callable[..., Any]] = {}
        self._register_default_handlers()

    @classmethod
    def get_instance(cls) -> "CommandBus":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def register(self, command_name: str, handler: Callable[..., Any]) -> None:
        self._handlers[command_name] = handler

    def execute(self, command_name: str, *args: Any, **kwargs: Any) -> Any:
        if command_name in self._handlers:
            try:
                logger.info(f"Executing command: '{command_name}'")
                return self._handlers[command_name](*args, **kwargs)
            except Exception as e:
                logger.error(f"Error executing command '{command_name}': {e}", exc_info=True)
                return False
        else:
            logger.warning(f"Unrecognized command: '{command_name}'")
            return False

    def _register_default_handlers(self) -> None:
        # Switching
        self.register("cut", lambda: transition_manager.cut())
        self.register("fade", lambda duration=500: transition_manager.fade(duration))
        self.register("dissolve", lambda duration=500: transition_manager.dissolve(duration))
        self.register("select_preview", lambda source_id: preview_output.select_source(source_id))
        self.register("take_program", lambda source_id: program_output.set_source(source_id))

        # Audio
        self.register("mute_audio", lambda channel_id: audio_mixer.set_mute(channel_id, True))
        self.register("unmute_audio", lambda channel_id: audio_mixer.set_mute(channel_id, False))
        self.register("toggle_mute", lambda channel_id: audio_mixer.toggle_mute(channel_id))
        self.register("set_volume", lambda channel_id, vol: audio_mixer.set_volume(channel_id, vol))

        # Stream / Record
        self.register("start_stream", lambda: streaming_coordinator.start_stream(StreamProfile()))
        self.register("stop_stream", lambda: streaming_coordinator.stop_stream())
        self.register("start_recording", lambda: recorder.start_recording(RecordingProfile(output_dir=paths.default_recordings_dir)))
        self.register("stop_recording", lambda: recorder.stop_recording())


command_bus = CommandBus.get_instance()
