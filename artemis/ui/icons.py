"""Vector icons drawn with QPainter, so no image files are needed."""
import math
from functools import lru_cache

from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import QBrush, QColor, QIcon, QPainter, QPen, QPixmap, QPolygonF

COLOR = QColor("#f1f1f5")
STAR = QColor("#ffd166")
SIZE = 48


def _pen(color=COLOR, width=3.6):
    return QPen(color, width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                Qt.PenJoinStyle.RoundJoin)


def _poly(p, points):
    p.drawPolyline(QPolygonF([QPointF(x, y) for x, y in points]))


def _back(p):
    p.drawLine(36, 24, 12, 24)
    _poly(p, [(22, 14), (12, 24), (22, 34)])


def _forward(p):
    p.drawLine(12, 24, 36, 24)
    _poly(p, [(26, 14), (36, 24), (26, 34)])


def _refresh(p):
    p.drawArc(QRectF(12, 12, 24, 24), 50 * 16, 280 * 16)
    _poly(p, [(38, 9), (32, 15), (39, 19)])


def _home(p):
    _poly(p, [(9, 24), (24, 11), (39, 24)])
    _poly(p, [(14, 22), (14, 37), (34, 37), (34, 22)])


def _star(p, filled):
    points = []
    for i in range(10):
        r = 17 if i % 2 == 0 else 7.5
        a = -math.pi / 2 + i * math.pi / 5
        points.append(QPointF(24 + r * math.cos(a), 25 + r * math.sin(a)))
    if filled:
        p.setBrush(QBrush(STAR))
        p.setPen(_pen(STAR, 2.5))
    p.drawPolygon(QPolygonF(points))


def _menu(p):
    for y in (15, 24, 33):
        p.drawLine(13, y, 35, y)


def _minimize(p):
    p.drawLine(14, 33, 34, 33)


def _maximize(p):
    p.drawRoundedRect(QRectF(14, 14, 20, 20), 3, 3)


def _close(p):
    p.drawLine(14, 14, 34, 34)
    p.drawLine(34, 14, 14, 34)


def _settings(p):
    p.drawEllipse(QPointF(24, 24), 8, 8)
    for i in range(8):
        a = i * math.pi / 4
        p.drawLine(QPointF(24 + 12 * math.cos(a), 24 + 12 * math.sin(a)),
                   QPointF(24 + 17 * math.cos(a), 24 + 17 * math.sin(a)))


_DRAWERS = {
    "back": _back, "forward": _forward, "refresh": _refresh, "home": _home,
    "star": lambda p: _star(p, False), "star_filled": lambda p: _star(p, True),
    "menu": _menu, "minimize": _minimize, "maximize": _maximize,
    "close": _close, "settings": _settings,
}


@lru_cache(maxsize=None)
def icon(name: str) -> QIcon:
    pixmap = QPixmap(SIZE, SIZE)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(_pen())
    _DRAWERS[name](painter)
    painter.end()
    return QIcon(pixmap)
