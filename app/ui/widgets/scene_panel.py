"""
Production Scene Management Panel with Scene Switching, Layer Controls, and Add/Delete actions.
"""

from typing import Optional
from app.core.events import events, EVENT_SCENE_CHANGED
from app.core.logger import logger
from app.production.scene import Scene
from app.production.scene_manager import scene_manager

try:
    from PySide6.QtCore import Qt, Signal
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QListWidget, QListWidgetItem, QInputDialog, QMessageBox
    )
    HAS_QT = True
except ImportError:
    HAS_QT = False


class ScenePanel(QWidget):
    """Studio control panel for switching scenes, adding layers, and managing layouts."""

    scene_selected = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._init_ui()
        self.refresh_scenes()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)

        # Header
        header = QHBoxLayout()
        title = QLabel("SCENES")
        title.setObjectName("SectionTitle")
        title.setStyleSheet("font-weight: bold; color: #FFFFFF; font-size: 11px;")
        header.addWidget(title)
        header.addStretch()

        # Add Scene button
        self.add_btn = QPushButton("+ SCENE")
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: #FFFFFF;
                font-size: 10px;
                font-weight: bold;
                border-radius: 3px;
                padding: 3px 8px;
            }
            QPushButton:hover { background-color: #0098FF; }
        """)
        self.add_btn.clicked.connect(self._add_scene_dialog)
        header.addWidget(self.add_btn)

        layout.addLayout(header)

        # Scene List
        self.scene_list = QListWidget()
        self.scene_list.setStyleSheet("""
            QListWidget {
                background-color: #12151B;
                border: 1px solid #282C35;
                border-radius: 4px;
                color: #E0E0E0;
            }
            QListWidget::item {
                padding: 8px 10px;
                border-bottom: 1px solid #1A1D24;
            }
            QListWidget::item:selected {
                background-color: #007ACC;
                color: #FFFFFF;
                font-weight: bold;
            }
            QListWidget::item:hover {
                background-color: #1C222D;
            }
        """)
        self.scene_list.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.scene_list)

        # Bottom actions: Duplicate, Remove
        btn_row = QHBoxLayout()
        self.dup_btn = QPushButton("Duplicate")
        self.dup_btn.setStyleSheet("background-color: #232730; color: #CCCCCC; font-size: 10px; border-radius: 3px; padding: 4px;")
        self.dup_btn.clicked.connect(self._duplicate_active_scene)
        btn_row.addWidget(self.dup_btn)

        self.del_btn = QPushButton("Delete")
        self.del_btn.setStyleSheet("background-color: #232730; color: #FF5252; font-size: 10px; border-radius: 3px; padding: 4px;")
        self.del_btn.clicked.connect(self._delete_active_scene)
        btn_row.addWidget(self.del_btn)

        layout.addLayout(btn_row)

    def refresh_scenes(self) -> None:
        self.scene_list.clear()
        for sc in scene_manager.get_all_scenes():
            item = QListWidgetItem(sc.name)
            item.setData(Qt.ItemDataRole.UserRole, sc.id)
            self.scene_list.addItem(item)
            if sc.id == scene_manager._active_scene_id:
                self.scene_list.setCurrentItem(item)

    def _on_item_clicked(self, item: QListWidgetItem) -> None:
        scene_id = item.data(Qt.ItemDataRole.UserRole)
        if scene_id:
            scene_manager.set_active_scene(scene_id)
            self.scene_selected.emit(scene_id)

    def _add_scene_dialog(self) -> None:
        name, ok = QInputDialog.getText(self, "Add Scene", "Scene Name:")
        if ok and name.strip():
            new_scene = Scene(name=name.strip())
            scene_manager.add_scene(new_scene)
            scene_manager.set_active_scene(new_scene.id)
            self.refresh_scenes()

    def _duplicate_active_scene(self) -> None:
        active = scene_manager.active_scene
        if active:
            dup_scene = Scene(name=f"{active.name} (Copy)")
            for l in active.layers:
                dup_scene.add_layer(l.source_id, l.x, l.y, l.width, l.height)
            scene_manager.add_scene(dup_scene)
            scene_manager.set_active_scene(dup_scene.id)
            self.refresh_scenes()

    def _delete_active_scene(self) -> None:
        active = scene_manager.active_scene
        if active:
            if len(scene_manager.get_all_scenes()) <= 1:
                QMessageBox.warning(self, "Action Denied", "Cannot delete the only remaining broadcast scene.")
                return
            scene_manager.remove_scene(active.id)
            self.refresh_scenes()
