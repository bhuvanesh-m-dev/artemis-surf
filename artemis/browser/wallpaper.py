"""Optional wallpaper painted behind the toolbar. No image = fully transparent window."""
from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QPainterPath, QPixmap


class Wallpaper:
    def __init__(self):
        self._pixmap = None

    def load(self, path: str):
        pixmap = QPixmap(path) if path else QPixmap()
        self._pixmap = None if pixmap.isNull() else pixmap

    @property
    def active(self) -> bool:
        return self._pixmap is not None

    def paint(self, painter, rect, radius=12):
        if not self._pixmap:
            return
        clip = QPainterPath()
        clip.addRoundedRect(QRectF(rect), radius, radius)
        painter.setClipPath(clip)
        scaled = self._pixmap.scaled(rect.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                     Qt.TransformationMode.SmoothTransformation)
        x = (rect.width() - scaled.width()) // 2
        y = (rect.height() - scaled.height()) // 2
        painter.drawPixmap(x, y, scaled)
