"""
Project file (.vjstudio) serialization and loading.
"""

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
from app.core.logger import logger


@dataclass
class ProjectMetadata:
    name: str = "Untitled Project"
    version: str = "1.0.0"
    created_at: str = ""
    width: int = 1920
    height: int = 1080
    fps: int = 30


class ProjectRepository:
    """Saves and loads .vjstudio project files."""

    @staticmethod
    def save_project(file_path: Path, project_name: str = "Live Production") -> bool:
        try:
            from app.production.scene_manager import scene_manager
            from app.production.input_manager import input_manager

            scenes_data = [s.to_dict() for s in scene_manager.get_all_scenes()]
            sources_data = [
                {
                    "id": src.id,
                    "name": src.name,
                    "type": src.type.value,
                    "width": src.width,
                    "height": src.height,
                    "visible": src.visible,
                    "audio_enabled": src.audio_enabled,
                }
                for src in input_manager.get_all_sources()
            ]

            payload = {
                "format": "vjstudio_project",
                "version": "1.0.0",
                "project_name": project_name,
                "scenes": scenes_data,
                "sources": sources_data,
            }

            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)

            logger.info(f"Saved project file -> {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save project file: {e}")
            return False

    @staticmethod
    def load_project(file_path: Path) -> Optional[Dict[str, Any]]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.info(f"Loaded project file -> {file_path}")
            return data
        except Exception as e:
            logger.error(f"Failed to load project file: {e}")
            return None
