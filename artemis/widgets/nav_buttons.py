"""Back / Forward / Refresh / Home button group."""
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QWidget

from artemis.widgets import tool_button


class NavButtons(QWidget):
    back = pyqtSignal()
    forward = pyqtSignal()
    reload = pyqtSignal()
    home = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.back_btn = tool_button("back", "Back (Alt+Left)", self.back.emit)
        self.forward_btn = tool_button("forward", "Forward (Alt+Right)", self.forward.emit)
        self.reload_btn = tool_button("refresh", "Refresh (F5)", self.reload.emit)
        self.home_btn = tool_button("home", "Home", self.home.emit)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(2)
        for b in (self.back_btn, self.forward_btn, self.reload_btn, self.home_btn):
            lay.addWidget(b)
        self.update_state(False, False)

    def update_state(self, can_back: bool, can_forward: bool):
        self.back_btn.setEnabled(can_back)
        self.forward_btn.setEnabled(can_forward)
