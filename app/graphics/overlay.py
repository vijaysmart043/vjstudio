"""
Base broadcast overlay and graphics rendering primitives.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Tuple

try:
    import cv2
    import numpy as np
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False


@dataclass
class OverlayPosition:
    x: int = 50
    y: int = 50
    width: int = 400
    height: int = 100
    opacity: float = 1.0
    visible: bool = True


class BaseOverlay(ABC):
    """Abstract graphics overlay layer rendered atop composed program frames."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.pos = OverlayPosition()

    @abstractmethod
    def render(self, canvas: Any) -> None:
        """Draw graphics onto the provided canvas numpy array."""
        pass
