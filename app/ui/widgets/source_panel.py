"""
Source management panel displaying registered inputs and quick-add actions.
"""

from typing import Dict, Optional
from app.core.constants import SourceType
from app.media.camera import CameraSource
from app.media.camera_manager import camera_manager
from app.media.image_source import ImageSource
from app.media.media_source import MediaSource
from app.media.ndi_source import NDISource
from app.media.network_stream_source import NetworkStreamSource
from app.media.screen_capture import ScreenCaptureSource
from app.media.video_source import VideoSource
from app.production.input_manager import input_manager
from app.production.preview_output import preview_output
from app.ui.widgets.source_button import SourceButton

try:
    from PySide6.QtCore import Qt, Signal
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QScrollArea, QGridLayout, QMenu, QFileDialog, QMessageBox, QInputDialog
    )
    HAS_QT = True
except ImportError:
    HAS_QT = False


class SourcePanel(QWidget):
    """Container listing all production inputs with live tally sync."""

    source_selected = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._buttons: Dict[str, SourceButton] = {}
        self._init_ui()
        self.populate_default_sources()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)

        # Header Bar
        header = QHBoxLayout()
        title = QLabel("INPUT SOURCES")
        title.setObjectName("SectionTitle")
        header.addWidget(title)
        header.addStretch()

        # Add Input Button with popup menu
        self.add_btn = QPushButton("+ ADD INPUT")
        self.add_btn.setStyleSheet(
            "background-color: #007ACC; color: white; font-weight: bold; border-radius: 4px; padding: 4px 10px;"
        )
        self.add_btn.clicked.connect(self._show_add_menu)
        header.addWidget(self.add_btn)
        layout.addLayout(header)

        # Scroll area for grid of input cards
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background: transparent; border: none;")

        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(8)

        self.scroll.setWidget(self.grid_container)
        layout.addWidget(self.scroll)

    def populate_default_sources(self) -> None:
        """Populate initial production inputs (Cameras, Screen, Video, Image)."""
        c1 = CameraSource(name="CAM 1 (PRIMARY)", device_index=0)
        c2 = CameraSource(name="CAM 2 (GUEST)", device_index=1)
        screen = ScreenCaptureSource(name="SCREEN CAPTURE 1")
        vid = VideoSource(file_path="intro_clip.mp4", name="PROMO VIDEO")
        img = ImageSource(file_path=None, name="STATION LOGO")

        for src in [c1, c2, screen, vid, img]:
            input_manager.add_source(src)
            self.add_source_button(src)

        # Default cue CAM 1 on Preview
        preview_output.select_source(c1.id)

    def add_source_button(self, source: MediaSource) -> None:
        btn = SourceButton(source)
        btn.clicked.connect(self._on_source_clicked)
        self._buttons[source.id] = btn
        self._relayout_grid()

    def _relayout_grid(self) -> None:
        # Clear grid layout
        for i in reversed(range(self.grid_layout.count())):
            item = self.grid_layout.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)

        # Place buttons in 2 columns
        cols = 2
        for idx, btn in enumerate(self._buttons.values()):
            row = idx // cols
            col = idx % cols
            self.grid_layout.addWidget(btn, row, col)

    def _on_source_clicked(self, source_id: str) -> None:
        preview_output.select_source(source_id)
        self.refresh_all_tallies()
        self.source_selected.emit(source_id)

    def refresh_all_tallies(self) -> None:
        for btn in self._buttons.values():
            btn.refresh_tally()

    def _show_add_menu(self) -> None:
        menu = QMenu(self)
        cam_menu = menu.addMenu("Camera")
        for dev in camera_manager.get_devices():
            action = cam_menu.addAction(dev.name)
            action.triggered.connect(lambda checked=False, d=dev: self._add_camera(d.index, d.name))

        screen_action = menu.addAction("Display / Screen Capture")
        screen_action.triggered.connect(self._add_screen)

        video_action = menu.addAction("Video File...")
        video_action.triggered.connect(self._add_video_file)

        image_action = menu.addAction("Image File...")
        image_action.triggered.connect(self._add_image_file)

        ndi_action = menu.addAction("NDI Network Source...")
        ndi_action.triggered.connect(self._add_ndi_source)

        stream_action = menu.addAction("RTMP / SRT Ingest Stream...")
        stream_action.triggered.connect(self._add_stream_source)

        menu.exec(self.add_btn.mapToGlobal(self.add_btn.rect().bottomLeft()))

    def _add_camera(self, index: int, name: str) -> None:
        src = CameraSource(name=name, device_index=index)
        input_manager.add_source(src)
        self.add_source_button(src)

    def _add_screen(self) -> None:
        count = len([s for s in input_manager.get_all_sources() if s.type == SourceType.SCREEN]) + 1
        src = ScreenCaptureSource(name=f"DISPLAY {count}")
        input_manager.add_source(src)
        self.add_source_button(src)

    def _add_video_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.mkv *.mov *.avi)")
        if file_path:
            src = VideoSource(file_path=file_path)
            input_manager.add_source(src)
            self.add_source_button(src)

    def _add_image_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image Graphic", "", "Image Files (*.png *.jpg *.jpeg *.webp)")
        if file_path:
            src = ImageSource(file_path=file_path)
            input_manager.add_source(src)
            self.add_source_button(src)

    def _add_ndi_source(self) -> None:
        name, ok = QInputDialog.getText(self, "Add NDI Source", "NDI Stream Name (e.g. STUDIO-PC (OBS)):")
        if ok and name.strip():
            src = NDISource(name=f"NDI: {name.strip()}", source_name=name.strip())
            input_manager.add_source(src)
            self.add_source_button(src)

    def _add_stream_source(self) -> None:
        url, ok = QInputDialog.getText(self, "Add Stream Source", "Network Stream URL (rtmp://, srt://, or rtsp://):")
        if ok and url.strip():
            src = NetworkStreamSource(name="NET STREAM", stream_url=url.strip())
            input_manager.add_source(src)
            self.add_source_button(src)
