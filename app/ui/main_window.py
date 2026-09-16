"""
VJ Studio primary broadcast production window.
"""

from typing import Optional
from app.audio.audio_mixer import audio_mixer
from app.commands.command_bus import command_bus
from app.commands.hotkeys import HotkeyManager
from app.core.constants import APP_NAME, APP_VERSION
from app.core.logger import logger
from app.core.paths import paths
from app.production.preview_output import preview_output
from app.production.program_output import program_output
from app.storage.project_repository import ProjectRepository
from app.ui.multiview_window import MultiviewWindow
from app.ui.theme import DARK_BROADCAST_STYLESHEET
from app.ui.widgets.audio_mixer import AudioMixerWidget
from app.ui.widgets.multiview_widget import MultiviewWidget
from app.ui.widgets.output_controls_widget import OutputControlsWidget
from app.ui.widgets.preview_widget import PreviewWidget
from app.ui.widgets.program_widget import ProgramWidget
from app.ui.widgets.record_dialog import RecordDialog
from app.ui.widgets.scene_panel import ScenePanel
from app.ui.widgets.settings_dialog import SettingsDialog
from app.ui.widgets.source_panel import SourcePanel
from app.ui.widgets.status_bar import BroadcastStatusBar
from app.ui.widgets.stream_dialog import StreamDialog
from app.ui.widgets.transition_controls import TransitionControls

try:
    from PySide6.QtCore import Qt, QTimer
    from PySide6.QtGui import QAction, QIcon, QKeySequence
    from PySide6.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QSplitter, QMenuBar, QMenu, QFileDialog, QMessageBox
    )
    HAS_QT = True
except ImportError:
    HAS_QT = False


class VJStudioMainWindow(QMainWindow):
    """Main broadcast control room interface for VJ Studio."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} — Live Video Production & Broadcast Studio v{APP_VERSION}")
        self.resize(1366, 820)
        self.setMinimumSize(1024, 640)
        self.setStyleSheet(DARK_BROADCAST_STYLESHEET)

        self.hotkey_mgr = HotkeyManager()
        self._multiview_window: Optional[MultiviewWindow] = None

        self._init_menu_bar()
        self._init_ui()
        self._init_production_timer()

    def _init_menu_bar(self) -> None:
        menubar = self.menuBar()

        # 1. File Menu
        file_menu = menubar.addMenu("File")
        new_act = file_menu.addAction("New Project")
        new_act.setShortcut(QKeySequence.StandardKey.New)
        new_act.triggered.connect(self._new_project)

        open_act = file_menu.addAction("Open Project...")
        open_act.setShortcut(QKeySequence.StandardKey.Open)
        open_act.triggered.connect(self._open_project)

        save_act = file_menu.addAction("Save Project")
        save_act.setShortcut(QKeySequence.StandardKey.Save)
        save_act.triggered.connect(self._save_project)

        file_menu.addSeparator()
        exit_act = file_menu.addAction("Exit VJ Studio")
        exit_act.setShortcut(QKeySequence("Alt+F4"))
        exit_act.triggered.connect(self.close)

        # 2. Inputs Menu
        inputs_menu = menubar.addMenu("Inputs")
        add_cam = inputs_menu.addAction("Add Camera Input")
        add_cam.triggered.connect(lambda: self.source_panel._show_add_menu())
        add_scr = inputs_menu.addAction("Add Screen Capture")
        add_scr.triggered.connect(self.source_panel._add_screen)
        add_vid = inputs_menu.addAction("Add Video Clip...")
        add_vid.triggered.connect(self.source_panel._add_video_file)

        # 3. Stream Menu
        stream_menu = menubar.addMenu("Stream")
        stream_cfg_act = stream_menu.addAction("RTMP Stream Settings...")
        stream_cfg_act.triggered.connect(self._open_stream_dialog)
        start_stream_act = stream_menu.addAction("Start Streaming (Space)")
        start_stream_act.triggered.connect(lambda: command_bus.execute("start_stream"))
        stop_stream_act = stream_menu.addAction("Stop Streaming")
        stop_stream_act.triggered.connect(lambda: command_bus.execute("stop_stream"))

        # 4. Record Menu
        rec_menu = menubar.addMenu("Record")
        rec_cfg_act = rec_menu.addAction("Recording Settings...")
        rec_cfg_act.triggered.connect(self._open_record_dialog)
        start_rec_act = rec_menu.addAction("Start Recording (R)")
        start_rec_act.triggered.connect(lambda: command_bus.execute("start_recording"))
        stop_rec_act = rec_menu.addAction("Stop Recording")
        stop_rec_act.triggered.connect(lambda: command_bus.execute("stop_recording"))

        # 5. View Menu (Multiview / Monitors)
        view_menu = menubar.addMenu("View")
        mv_act = view_menu.addAction("Open Multiview Window (F11)")
        mv_act.setShortcut(QKeySequence("F11"))
        mv_act.triggered.connect(self._toggle_multiview_window)

        # 6. Settings Menu
        settings_menu = menubar.addMenu("Settings")
        pref_act = settings_menu.addAction("Preferences...")
        pref_act.triggered.connect(self._open_settings_dialog)

        # 7. Help Menu
        help_menu = menubar.addMenu("Help")
        diag_act = help_menu.addAction("Diagnostics & FFmpeg Check")
        diag_act.triggered.connect(self._open_settings_dialog)
        about_act = help_menu.addAction(f"About {APP_NAME}")
        about_act.triggered.connect(self._show_about)

    def _init_ui(self) -> None:
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(6, 6, 6, 6)
        root_layout.setSpacing(6)

        # Vertical splitter dividing Upper Monitors & Transition and Lower Mixer & Inputs
        main_splitter = QSplitter(Qt.Orientation.Vertical)

        # ==========================================
        # UPPER PRODUCTION AREA: PREVIEW | TRANSITION | PROGRAM
        # ==========================================
        upper_container = QWidget()
        upper_layout = QHBoxLayout(upper_container)
        upper_layout.setContentsMargins(0, 0, 0, 0)
        upper_layout.setSpacing(8)

        # 1. Preview Monitor
        self.preview_widget = PreviewWidget()
        upper_layout.addWidget(self.preview_widget, stretch=4)

        # 2. Transition Center Controls
        self.transition_controls = TransitionControls()
        self.transition_controls.setFixedWidth(240)
        self.transition_controls.transition_executed.connect(self._on_transition)
        upper_layout.addWidget(self.transition_controls, stretch=0)

        # 3. Program Live Monitor
        self.program_widget = ProgramWidget()
        upper_layout.addWidget(self.program_widget, stretch=4)

        main_splitter.addWidget(upper_container)

        # ==========================================
        # LOWER PRODUCTION AREA: SCENES | INPUT GRID | AUDIO MIXER | OUTPUTS
        # ==========================================
        lower_container = QWidget()
        lower_layout = QHBoxLayout(lower_container)
        lower_layout.setContentsMargins(0, 0, 0, 0)
        lower_layout.setSpacing(8)

        # 1. Production Scene Panel
        self.scene_panel = ScenePanel()
        self.scene_panel.setFixedWidth(200)
        lower_layout.addWidget(self.scene_panel, stretch=0)

        # 2. Source / Input Panel
        self.source_panel = SourcePanel()
        self.source_panel.source_selected.connect(self._on_source_selected)
        lower_layout.addWidget(self.source_panel, stretch=5)

        # 3. Audio Mixer Panel
        self.audio_mixer_widget = AudioMixerWidget()
        lower_layout.addWidget(self.audio_mixer_widget, stretch=3)

        # 4. Master Output Controls Deck (Stream, Record, NDI, Virtual Cam)
        self.output_controls_widget = OutputControlsWidget()
        self.output_controls_widget.setFixedWidth(190)
        lower_layout.addWidget(self.output_controls_widget, stretch=0)

        main_splitter.addWidget(lower_container)

        root_layout.addWidget(main_splitter)

        # ==========================================
        # BOTTOM STATUS TELEMETRY BAR
        # ==========================================
        self.status_bar = BroadcastStatusBar()
        root_layout.addWidget(self.status_bar)

    def _init_production_timer(self) -> None:
        """High-precision 30 FPS production loop for monitor redraws and meters."""
        self.timer = QTimer(self)
        self.timer.setInterval(33)  # ~30 fps
        self.timer.timeout.connect(self._on_production_tick)
        self.timer.start()

    def _on_production_tick(self) -> None:
        # 1. Refresh Preview monitor frame
        prev_frame = preview_output.get_frame()
        self.preview_widget.update_frame(prev_frame)

        # 2. Refresh Program monitor frame
        prog_frame = program_output.get_frame()
        self.program_widget.update_frame(prog_frame)

        # 3. Refresh audio levels and UI strips
        audio_mixer.update_levels()
        self.audio_mixer_widget.update_meters()

        # 4. Refresh status telemetry
        self.status_bar.update_telemetry()

    def _on_source_selected(self, source_id: str) -> None:
        # Automatically update UI badges
        self.source_panel.refresh_all_tallies()

    def _on_transition(self) -> None:
        self.source_panel.refresh_all_tallies()

    def keyPressEvent(self, event) -> None:
        """Intercept broadcast hotkeys."""
        key = event.key()
        if key == Qt.Key.Key_Space:
            self.hotkey_mgr.handle_key_press("Space")
            event.accept()
        elif key == Qt.Key.Key_C:
            self.hotkey_mgr.handle_key_press("C")
            self._on_transition()
            event.accept()
        elif key == Qt.Key.Key_F:
            self.hotkey_mgr.handle_key_press("F")
            self._on_transition()
            event.accept()
        elif key == Qt.Key.Key_D:
            self.hotkey_mgr.handle_key_press("D")
            self._on_transition()
            event.accept()
        elif key == Qt.Key.Key_R:
            self.hotkey_mgr.handle_key_press("R")
            event.accept()
        elif Qt.Key.Key_F1 <= key <= Qt.Key.Key_F12:
            f_num = key - Qt.Key.Key_F1 + 1
            self.hotkey_mgr.handle_key_press(f"F{f_num}")
            self.source_panel.refresh_all_tallies()
            event.accept()
        else:
            super().keyPressEvent(event)

    def _open_stream_dialog(self) -> None:
        dlg = StreamDialog(self)
        dlg.exec()

    def _open_record_dialog(self) -> None:
        dlg = RecordDialog(self)
        dlg.exec()

    def _open_settings_dialog(self) -> None:
        dlg = SettingsDialog(self)
        dlg.exec()

    def _toggle_multiview_window(self) -> None:
        if self._multiview_window is None:
            self._multiview_window = MultiviewWindow(self)
        if self._multiview_window.isVisible():
            self._multiview_window.hide()
        else:
            self._multiview_window.show()
            self._multiview_window.raise_()
            self._multiview_window.activateWindow()

    def _new_project(self) -> None:
        QMessageBox.information(self, "New Project", "New broadcast production initialized.")

    def _save_project(self) -> None:
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save VJ Studio Project", str(paths.default_projects_dir / "project.vjstudio"), "VJ Studio Projects (*.vjstudio)"
        )
        if file_path:
            ProjectRepository.save_project(file_path)
            QMessageBox.information(self, "Project Saved", f"Project saved successfully:\n{file_path}")

    def _open_project(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open VJ Studio Project", str(paths.default_projects_dir), "VJ Studio Projects (*.vjstudio)"
        )
        if file_path:
            ProjectRepository.load_project(file_path)
            QMessageBox.information(self, "Project Loaded", f"Loaded project:\n{file_path}")

    def _show_about(self) -> None:
        QMessageBox.about(
            self,
            f"About {APP_NAME}",
            f"<b>{APP_NAME} v{APP_VERSION}</b><br><br>"
            "Professional Live Video Production, Mixing, and Streaming System.<br>"
            "Engineered for Windows 10/11 64-bit.<br><br>"
            "Designed for low-latency broadcast switching, RTMP/SRT distribution, and live multi-camera mixing."
        )

    def closeEvent(self, event) -> None:
        logger.info("VJ Studio shutting down cleanly.")
        input_manager.stop_all()
        command_bus.execute("stop_stream")
        command_bus.execute("stop_recording")
        event.accept()
