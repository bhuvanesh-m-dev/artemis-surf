"""Minimal centered address bar whose width follows the URL length."""
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QLineEdit


class UrlBar(QLineEdit):
    submitted = pyqtSignal(str)
    MIN_WIDTH = 240

    def __init__(self, parent=None):
        super().__init__(parent)
        self._max_width = 800
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setPlaceholderText("Search or enter address")
        self.returnPressed.connect(lambda: self.submitted.emit(self.text()))
        self.textChanged.connect(lambda _text: self.refit())
        self.refit()

    def set_max_width(self, width: int):
        self._max_width = max(self.MIN_WIDTH, width)
        self.refit()

    def refit(self):
        text = self.text() or self.placeholderText()
        wanted = self.fontMetrics().horizontalAdvance(text) + 70
        self.setFixedWidth(max(self.MIN_WIDTH, min(wanted, self._max_width)))

    def show_url(self, url: str):
        if not self.hasFocus():
            self.setText(url)
            self.setCursorPosition(0)

    def focus_all(self):
        self.setFocus()
        self.selectAll()
