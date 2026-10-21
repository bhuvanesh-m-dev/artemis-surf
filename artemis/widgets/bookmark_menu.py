"""Star button (toggle bookmark) + list button (bookmark drop-down)."""
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QMenu, QWidget

from artemis.ui.icons import icon
from artemis.widgets import tool_button


class BookmarkButtons(QWidget):
    open_url = pyqtSignal(str)
    toggled = pyqtSignal()

    def __init__(self, bookmarks, parent=None):
        super().__init__(parent)
        self.bookmarks = bookmarks
        self.star_btn = tool_button("star", "Bookmark this page (Ctrl+D)", self.toggled.emit)
        self.list_btn = tool_button("menu", "Bookmarks", self.show_menu)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(2)
        lay.addWidget(self.star_btn)
        lay.addWidget(self.list_btn)

    def refresh(self, current_url: str):
        name = "star_filled" if self.bookmarks.has(current_url) else "star"
        self.star_btn.setIcon(icon(name))

    def show_menu(self):
        menu = QMenu(self)
        items = self.bookmarks.items()
        if not items:
            menu.addAction("No bookmarks yet").setEnabled(False)
        for url, title in items:
            label = title if len(title) <= 48 else title[:47] + "…"
            menu.addAction(label, lambda u=url: self.open_url.emit(u))
        menu.exec(self.list_btn.mapToGlobal(self.list_btn.rect().bottomLeft()))
