"""
Tests for Scene creation, layer management, and serialization.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.production.scene import Scene, SceneLayer
from app.production.scene_manager import scene_manager


def test_scene_creation_and_layers():
    scene = Scene(name="Test Scene 1")
    layer1 = scene.add_layer("source_cam_1", 0, 0, 1920, 1080)
    layer2 = scene.add_layer("source_logo_1", 100, 100, 300, 150)

    assert len(scene.layers) == 2
    assert scene.layers[0].source_id == "source_cam_1"
    assert scene.layers[1].source_id == "source_logo_1"

    data = scene.to_dict()
    restored = Scene.from_dict(data)

    assert restored.name == "Test Scene 1"
    assert len(restored.layers) == 2
    assert restored.layers[1].source_id == "source_logo_1"


def test_scene_manager_operations():
    s = Scene(name="Studio Scene B")
    scene_manager.add_scene(s)
    assert scene_manager.get_scene(s.id) is not None

    scene_manager.set_active_scene(s.id)
    assert scene_manager.active_scene.id == s.id


if __name__ == "__main__":
    test_scene_creation_and_layers()
    test_scene_manager_operations()
    print("test_scenes passed!")
