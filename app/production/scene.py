"""
Production Scene representation containing multi-source layers and layout settings.
"""

import uuid
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class SceneLayer:
    source_id: str
    layer_order: int
    x: int = 0
    y: int = 0
    width: int = 1920
    height: int = 1080
    scale: float = 1.0
    opacity: float = 1.0
    visible: bool = True


@dataclass
class Scene:
    """A broadcast scene comprising an ordered stack of media source layers."""
    name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    layers: List[SceneLayer] = field(default_factory=list)
    transition_type: str = "fade"
    transition_duration_ms: int = 500

    def add_layer(self, source_id: str, x: int = 0, y: int = 0, width: int = 1920, height: int = 1080) -> SceneLayer:
        layer = SceneLayer(
            source_id=source_id,
            layer_order=len(self.layers),
            x=x,
            y=y,
            width=width,
            height=height,
        )
        self.layers.append(layer)
        return layer

    def remove_layer(self, source_id: str) -> bool:
        initial_len = len(self.layers)
        self.layers = [l for l in self.layers if l.source_id != source_id]
        return len(self.layers) < initial_len

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Scene":
        layers_data = data.get("layers", [])
        layers = [SceneLayer(**l) for l in layers_data]
        return cls(
            name=data["name"],
            id=data.get("id", str(uuid.uuid4())[:8]),
            layers=layers,
            transition_type=data.get("transition_type", "fade"),
            transition_duration_ms=data.get("transition_duration_ms", 500),
        )
