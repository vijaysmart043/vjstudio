"""
Global keyboard shortcuts manager for live broadcast switching.
"""

from typing import Dict
from app.commands.command_bus import command_bus
from app.core.logger import logger
from app.production.input_manager import input_manager


class HotkeyManager:
    """Translates keyboard events into Production commands."""

    def __init__(self) -> None:
        self.enabled = True

    def handle_key_press(self, key_text: str) -> bool:
        """Evaluate keypress and execute corresponding action."""
        if not self.enabled:
            return False

        key = key_text.upper()

        if key == "C":
            command_bus.execute("cut")
            return True
        elif key == "F":
            command_bus.execute("fade", 500)
            return True
        elif key == "D":
            command_bus.execute("dissolve", 500)
            return True
        elif key == "SPACE":
            # Toggle stream
            from app.streaming.streamer import streaming_coordinator
            from app.core.constants import StreamState
            if streaming_coordinator.state == StreamState.LIVE:
                command_bus.execute("stop_stream")
            else:
                command_bus.execute("start_stream")
            return True
        elif key == "R":
            from app.recording.recorder import recorder
            from app.core.constants import RecordState
            if recorder.state == RecordState.RECORDING:
                command_bus.execute("stop_recording")
            else:
                command_bus.execute("start_recording")
            return True
        elif key.startswith("F") and key[1:].isdigit():
            idx = int(key[1:]) - 1
            sources = input_manager.get_all_sources()
            if 0 <= idx < len(sources):
                command_bus.execute("select_preview", sources[idx].id)
                return True

        return False
