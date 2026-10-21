"""A browser tab: web view + page. Popups (e.g. 'Sign in with Google') open in a small window."""
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QMainWindow


class Page(QWebEnginePage):
    popups = []     # keep references so popup windows are not garbage collected

    def createWindow(self, _window_type):
        win = QMainWindow()
        win.resize(520, 700)
        view = QWebEngineView(win)
        page = Page(self.profile(), view)
        view.setPage(page)
        win.setCentralWidget(view)
        win.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        page.windowCloseRequested.connect(win.close)
        win.destroyed.connect(lambda *_: Page.popups.remove(win) if win in Page.popups else None)
        Page.popups.append(win)
        win.show()
        return page


class Tab(QWebEngineView):
    fullscreen_changed = pyqtSignal(bool)

    def __init__(self, profile, parent=None):
        super().__init__(parent)
        self._page = Page(profile, self)
        self._page.setBackgroundColor(QColor(0, 0, 0, 0))
        self._page.fullScreenRequested.connect(self._on_fullscreen)
        self.setPage(self._page)

    def _on_fullscreen(self, request):
        request.accept()
        self.fullscreen_changed.emit(request.toggleOn())

    @staticmethod
    def close_popups():
        for win in list(Page.popups):
            win.close()
