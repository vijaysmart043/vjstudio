"""
UI panel module aliases providing clean namespace access for the main broadcast workspace.
"""

from app.ui.widgets.preview_widget import PreviewWidget as PreviewPanel
from app.ui.widgets.program_widget import ProgramWidget as ProgramPanel
from app.ui.widgets.source_panel import SourcePanel
from app.ui.widgets.scene_panel import ScenePanel
from app.ui.widgets.transition_controls import TransitionControlsWidget as TransitionPanel
from app.ui.widgets.audio_mixer import AudioMixerWidget as AudioMixerPanel
from app.ui.widgets.stream_dialog import StreamDialog as StreamingPanel
from app.ui.widgets.record_dialog import RecordDialog as RecordingPanel
from app.ui.widgets.status_bar import BroadcastStatusBar
from app.ui.widgets.settings_dialog import SettingsDialog as SettingsWindow
from app.ui.multiview import MultiviewWidget, MultiviewWindow

__all__ = [
    "PreviewPanel",
    "ProgramPanel",
    "SourcePanel",
    "ScenePanel",
    "TransitionPanel",
    "AudioMixerPanel",
    "StreamingPanel",
    "RecordingPanel",
    "BroadcastStatusBar",
    "SettingsWindow",
    "MultiviewWidget",
    "MultiviewWindow",
]
