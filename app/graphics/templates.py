"""
Virtual Sets & Studio Templates for VJ Studio.
Provides multi-layer virtual environments (News Studio, Sports, Podcast, Tech, Corporate, Weather).
"""

from dataclasses import dataclass, field
from typing import Any, List, Optional
from app.production.scene import Scene, SceneLayer

try:
    import cv2
    import numpy as np
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False


@dataclass
class StudioTemplate:
    """Pre-configured virtual studio layout template."""
    id: str
    name: str
    category: str
    description: str
    bg_gradient_start: tuple = (20, 24, 32)
    bg_gradient_end: tuple = (10, 12, 16)
    has_chroma_key: bool = False
    has_ticker: bool = False
    has_lower_third: bool = False

    def generate_backdrop(self, width: int = 1920, height: int = 1080) -> Optional[Any]:
        """Generates a high-definition synthetic virtual studio backdrop."""
        if not HAS_OPENCV:
            return None

        canvas = np.zeros((height, width, 3), dtype=np.uint8)
        # Vertical gradient
        for y in range(height):
            alpha = y / float(height)
            b = int(self.bg_gradient_start[0] * (1 - alpha) + self.bg_gradient_end[0] * alpha)
            g = int(self.bg_gradient_start[1] * (1 - alpha) + self.bg_gradient_end[1] * alpha)
            r = int(self.bg_gradient_start[2] * (1 - alpha) + self.bg_gradient_end[2] * alpha)
            canvas[y, :] = (b, g, r)

        # Studio architectural lines and lighting rim
        cv2.line(canvas, (0, int(height * 0.7)), (width, int(height * 0.7)), (40, 50, 65), 2)
        cv2.line(canvas, (0, int(height * 0.7) + 8), (width, int(height * 0.7) + 8), (0, 160, 255), 1)

        # Watermark set label
        cv2.putText(
            canvas,
            f"VJ STUDIO SET // {self.name.upper()}",
            (60, int(height * 0.2)),
            cv2.FONT_HERSHEY_DUPLEX,
            0.7,
            (55, 65, 80),
            1,
            cv2.LINE_AA,
        )
        return canvas


# Studio Templates Catalog
BUILTIN_TEMPLATES: List[StudioTemplate] = [
    StudioTemplate(
        id="news_studio",
        name="News Broadcast Studio",
        category="News",
        description="Dual-host newsroom anchor desk with live video wall and breaking news ticker.",
        bg_gradient_start=(35, 25, 18),
        bg_gradient_end=(12, 10, 8),
        has_ticker=True,
        has_lower_third=True,
    ),
    StudioTemplate(
        id="sports_studio",
        name="Sports Arena Desk",
        category="Sports",
        description="High-energy arena backdrop with scorebug and replay feed positions.",
        bg_gradient_start=(20, 36, 20),
        bg_gradient_end=(8, 14, 8),
        has_ticker=True,
    ),
    StudioTemplate(
        id="podcast_studio",
        name="Podcast Studio Lounge",
        category="Podcast",
        description="Warm acoustic studio paneling with dual webcam PiP frames.",
        bg_gradient_start=(18, 22, 38),
        bg_gradient_end=(8, 10, 16),
        has_lower_third=True,
    ),
    StudioTemplate(
        id="tech_studio",
        name="Technology & Dev Studio",
        category="Technology",
        description="Dark obsidian slate design optimized for coding tutorials and keynotes.",
        bg_gradient_start=(28, 24, 20),
        bg_gradient_end=(10, 8, 8),
        has_ticker=False,
    ),
    StudioTemplate(
        id="corporate_studio",
        name="Corporate Keynote Studio",
        category="Corporate",
        description="Clean executive presentation staging with picture-in-picture slides.",
        bg_gradient_start=(30, 30, 30),
        bg_gradient_end=(12, 12, 12),
        has_lower_third=True,
    ),
    StudioTemplate(
        id="weather_studio",
        name="Meteorology Center",
        category="Weather",
        description="Green-screen chroma key stage with satellite radar screen insert.",
        bg_gradient_start=(38, 28, 14),
        bg_gradient_end=(14, 10, 8),
        has_chroma_key=True,
    ),
]


def get_template(template_id: str) -> Optional[StudioTemplate]:
    for t in BUILTIN_TEMPLATES:
        if t.id == template_id:
            return t
    return None
