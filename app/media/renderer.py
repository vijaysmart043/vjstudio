"""
Renderer utility converting raw video frames into Qt displayable pixmaps.
"""

from typing import Optional
from app.media.frame import VideoFrame

try:
    from PySide6.QtGui import QImage, QPixmap
    HAS_QT = True
except ImportError:
    HAS_QT = False

try:
    import cv2
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False


class FrameRenderer:
    """Converts VideoFrame numpy arrays to QPixmap for high-performance rendering."""

    @staticmethod
    def to_qimage(frame: VideoFrame) -> Optional["QImage"]:
        if not HAS_QT or frame is None or frame.data is None:
            return None

        data = frame.data
        h, w = data.shape[:2]

        if frame.format == "BGR" and HAS_OPENCV:
            rgb_data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
            bytes_per_line = 3 * w
            return QImage(rgb_data.data, w, h, bytes_per_line, QImage.Format.Format_RGB888).copy()
        elif frame.format == "RGB":
            bytes_per_line = 3 * w
            return QImage(data.data, w, h, bytes_per_line, QImage.Format.Format_RGB888).copy()

        return None

    @staticmethod
    def to_qpixmap(frame: VideoFrame) -> Optional["QPixmap"]:
        qimg = FrameRenderer.to_qimage(frame)
        if qimg is not None:
            return QPixmap.fromImage(qimg)
        return None
