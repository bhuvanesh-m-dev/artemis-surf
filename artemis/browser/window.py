"""Frameless, transparent main window that assembles the whole browser."""
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QKeySequence, QPainter, QShortcut
from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QSizeGrip, QVBoxLayout, QWidget

from artemis.browser.bookmarks import Bookmarks
from artemis.browser.tab import Tab
from artemis.browser.urlbar import UrlBar
from artemis.browser.wallpaper import Wallpaper
from artemis.config import APP_NAME, SIDE_WIDTH, settings
from artemis.ui.settings_dialog import SettingsDialog
from artemis.ui.styles import STYLE
from artemis.util.url_tools import resolve
from artemis.util.weather import WeatherWorker
from artemis.widgets import tool_button
from artemis.widgets.bookmark_menu import BookmarkButtons
from artemis.widgets.nav_buttons import NavButtons
from artemis.widgets.window_controls import WindowControls


class DragBar(QWidget):
    """Toolbar that drags the frameless window; double-click maximizes."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("bar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.window().windowHandle().startSystemMove()

    def mouseDoubleClickEvent(self, _event):
        self.window().toggle_max()


class BrowserWindow(QMainWindow):
    def __init__(self, profile):
        super().__init__()
        self.profile = profile
        self.bookmarks = Bookmarks()
        self.wallpaper = Wallpaper()
        self._weather = None

        self.setWindowTitle(APP_NAME)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet(STYLE)
        self.setMinimumSize(740, 420)
        self.resize(1200, 780)

        # ---- content
        self.tab = Tab(profile)

        # ---- toolbar
        self.bar = DragBar()
        self.bar.setFixedHeight(46)
        self.nav = NavButtons()
        self.urlbar = UrlBar()
        self.marks = BookmarkButtons(self.bookmarks)
        self.settings_btn = tool_button("settings", "Settings", self.open_settings)
        self.controls = WindowControls()

        row = QHBoxLayout(self.bar)
        row.setContentsMargins(10, 6, 10, 6)
        row.addWidget(self._side([self.nav], align_right=False))
        row.addStretch(1)
        row.addWidget(self.urlbar)
        row.addStretch(1)
        row.addWidget(self._side([self.marks, self.settings_btn, self.controls], align_right=True))

        root = QWidget()
        column = QVBoxLayout(root)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(0)
        column.addWidget(self.bar)
        column.addWidget(self.tab, 1)
        self.setCentralWidget(root)

        self.grip = QSizeGrip(self)
        self.grip.setFixedSize(16, 16)

        self._connect()
        self.apply_settings()
        self.go_home()

    # ---------------------------------------------------------- layout helpers
    @staticmethod
    def _side(widgets, align_right):
        box = QWidget()
        box.setFixedWidth(SIDE_WIDTH)
        lay = QHBoxLayout(box)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(2)
        if align_right:
            lay.addStretch(1)
        for w in widgets:
            lay.addWidget(w)
        if not align_right:
            lay.addStretch(1)
        return box

    def _connect(self):
        self.nav.back.connect(self.tab.back)
        self.nav.forward.connect(self.tab.forward)
        self.nav.reload.connect(self.tab.reload)
        self.nav.home.connect(self.go_home)

        self.urlbar.submitted.connect(self.navigate)
        self.marks.open_url.connect(lambda u: self.tab.setUrl(QUrl(u)))
        self.marks.toggled.connect(self.toggle_bookmark)

        self.controls.minimize.connect(self.showMinimized)
        self.controls.toggle_max.connect(self.toggle_max)
        self.controls.close.connect(self.close)

        self.tab.urlChanged.connect(self.on_url_changed)
        self.tab.loadFinished.connect(lambda _ok: self.update_state())
        self.tab.titleChanged.connect(
            lambda t: self.setWindowTitle(f"{t} - {APP_NAME}" if t else APP_NAME))
        self.tab.fullscreen_changed.connect(self.on_fullscreen)

        for seq, fn in [("Alt+Left", self.tab.back), ("Alt+Right", self.tab.forward),
                        ("F5", self.tab.reload), ("Ctrl+R", self.tab.reload),
                        ("Ctrl+L", self.urlbar.focus_all), ("Ctrl+D", self.toggle_bookmark),
                        ("Alt+Home", self.go_home)]:
            QShortcut(QKeySequence(seq), self, activated=fn)

    # ---------------------------------------------------------- navigation
    def go_home(self):
        self.tab.setUrl(QUrl(settings.get("home_url")))

    def navigate(self, text):
        url = resolve(text)
        if url is not None:
            self.tab.setUrl(url)
            self.tab.setFocus()

    def on_url_changed(self, url):
        self.urlbar.show_url(url.toString())
        self.update_state()

    def update_state(self):
        history = self.tab.history()
        self.nav.update_state(history.canGoBack(), history.canGoForward())
        self.marks.refresh(self.tab.url().toString())

    def toggle_bookmark(self):
        url = self.tab.url().toString()
        self.bookmarks.toggle(url, self.tab.title())
        self.marks.refresh(url)

    # ---------------------------------------------------------- settings
    def open_settings(self):
        if SettingsDialog(self).exec():
            self.apply_settings()

    def apply_settings(self):
        self.setWindowOpacity(float(settings.get("opacity")))
        self.wallpaper.load(settings.get("wallpaper"))
        self.update()
        self.refresh_weather()

    def refresh_weather(self):
        self.nav.home_btn.setToolTip("Home")
        if not settings.get("weather_enabled"):
            return
        self._weather = WeatherWorker(settings.get("latitude"), settings.get("longitude"))
        self._weather.result.connect(lambda text: self.nav.home_btn.setToolTip(f"Home  |  {text}"))
        self._weather.start()

    # ---------------------------------------------------------- window behaviour
    def toggle_max(self):
        self.showNormal() if self.isMaximized() else self.showMaximized()

    def on_fullscreen(self, on):
        self.bar.setVisible(not on)
        self.grip.setVisible(not on)
        self.showFullScreen() if on else self.showNormal()

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.wallpaper.paint(painter, self.rect())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.urlbar.set_max_width(min(int(self.width() * 0.6),
                                      self.width() - 2 * SIDE_WIDTH - 60))
        self.grip.move(self.width() - 16, self.height() - 16)
        self.grip.raise_()

    def closeEvent(self, event):
        self.profile.clearAllVisitedLinks()
        Tab.close_popups()
        super().closeEvent(event)
