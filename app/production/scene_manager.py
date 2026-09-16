"""
Scene collection manager with creation, cloning, deletion, and serialization.
"""

from typing import Dict, List, Optional
from app.core.events import events, EVENT_SCENE_CHANGED
from app.core.logger import logger
from app.production.scene import Scene


class SceneManager:
    """Manages scene lists, active scene, and scene transitions."""

    _instance = None

    def __init__(self) -> None:
        self._scenes: Dict[str, Scene] = {}
        self._scene_order: List[str] = []
        self._active_scene_id: Optional[str] = None
        self._init_default_scenes()

    @classmethod
    def get_instance(cls) -> "SceneManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _init_default_scenes(self) -> None:
        s1 = Scene(name="SCENE 1 (MAIN)")
        s2 = Scene(name="SCENE 2 (PRESENTATION)")
        self.add_scene(s1)
        self.add_scene(s2)
        self._active_scene_id = s1.id

    def add_scene(self, scene: Scene) -> str:
        self._scenes[scene.id] = scene
        if scene.id not in self._scene_order:
            self._scene_order.append(scene.id)
        return scene.id

    def remove_scene(self, scene_id: str) -> bool:
        if len(self._scenes) <= 1:
            logger.warning("Cannot delete the only remaining scene.")
            return False
        if scene_id in self._scenes:
            del self._scenes[scene_id]
            self._scene_order.remove(scene_id)
            if self._active_scene_id == scene_id:
                self._active_scene_id = self._scene_order[0]
            return True
        return False

    def get_scene(self, scene_id: str) -> Optional[Scene]:
        return self._scenes.get(scene_id)

    def get_all_scenes(self) -> List[Scene]:
        return [self._scenes[sid] for sid in self._scene_order if sid in self._scenes]

    def set_active_scene(self, scene_id: str) -> bool:
        if scene_id in self._scenes:
            self._active_scene_id = scene_id
            events.publish(EVENT_SCENE_CHANGED, self._scenes[scene_id])
            logger.info(f"Active scene changed to: {self._scenes[scene_id].name}")
            return True
        return False

    @property
    def active_scene(self) -> Optional[Scene]:
        if self._active_scene_id:
            return self._scenes.get(self._active_scene_id)
        return None


scene_manager = SceneManager.get_instance()
