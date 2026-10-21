"""Reusable toolbar widgets."""
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QToolButton

from artemis.ui.icons import icon


def tool_button(icon_name, tooltip, slot=None):
    button = QToolButton()
    button.setIcon(icon(icon_name))
    button.setIconSize(QSize(18, 18))
    button.setFixedSize(30, 30)
    button.setToolTip(tooltip)
    button.setCursor(Qt.CursorShape.PointingHandCursor)
    if slot:
        button.clicked.connect(slot)
    return button
