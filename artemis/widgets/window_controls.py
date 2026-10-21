"""Minimize / Maximize / Close buttons for the frameless window."""
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QWidget

from artemis.widgets import tool_button


class WindowControls(QWidget):
    minimize = pyqtSignal()
    toggle_max = pyqtSignal()
    close = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(2)
        lay.addWidget(tool_button("minimize", "Minimize", self.minimize.emit))
        lay.addWidget(tool_button("maximize", "Maximize", self.toggle_max.emit))
        close_btn = tool_button("close", "Close", self.close.emit)
        close_btn.setObjectName("close")
        lay.addWidget(close_btn)
