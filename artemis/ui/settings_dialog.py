"""Settings: home page, opacity, wallpaper, weather."""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QCheckBox, QDialog, QDialogButtonBox, QDoubleSpinBox,
                             QFileDialog, QFormLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QSlider, QWidget)

from artemis.config import DEFAULT_HOME_URL, settings


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ArtemisSurf Settings")
        self.setMinimumWidth(460)

        self.home = QLineEdit(settings.get("home_url"))

        self.opacity = QSlider(Qt.Orientation.Horizontal)
        self.opacity.setRange(40, 100)
        self.opacity.setValue(int(float(settings.get("opacity")) * 100))

        self.wallpaper = QLineEdit(settings.get("wallpaper"))
        self.wallpaper.setPlaceholderText("None (fully transparent)")
        browse = QPushButton("Browse")
        browse.clicked.connect(self.pick_wallpaper)
        clear = QPushButton("Clear")
        clear.clicked.connect(self.wallpaper.clear)
        wall_row = QWidget()
        wall_lay = QHBoxLayout(wall_row)
        wall_lay.setContentsMargins(0, 0, 0, 0)
        for w in (self.wallpaper, browse, clear):
            wall_lay.addWidget(w)

        self.weather = QCheckBox("Show weather in the Home button tooltip")
        self.weather.setChecked(bool(settings.get("weather_enabled")))
        self.lat = QDoubleSpinBox()
        self.lat.setRange(-90, 90)
        self.lat.setDecimals(4)
        self.lat.setValue(float(settings.get("latitude")))
        self.lon = QDoubleSpinBox()
        self.lon.setRange(-180, 180)
        self.lon.setDecimals(4)
        self.lon.setValue(float(settings.get("longitude")))

        reset = QPushButton("Reset home page")
        reset.clicked.connect(lambda: self.home.setText(DEFAULT_HOME_URL))

        form = QFormLayout(self)
        form.addRow("Home page", self.home)
        form.addRow("", reset)
        form.addRow("Window opacity", self.opacity)
        form.addRow("Wallpaper", wall_row)
        form.addRow(self.weather)
        form.addRow("Latitude", self.lat)
        form.addRow("Longitude", self.lon)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save |
                                   QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def pick_wallpaper(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose wallpaper", "",
                                              "Images (*.png *.jpg *.jpeg *.webp *.bmp)")
        if path:
            self.wallpaper.setText(path)

    def save(self):
        home = self.home.text().strip() or DEFAULT_HOME_URL
        if "://" not in home:
            home = "https://" + home
        settings.set("home_url", home)
        settings.set("opacity", self.opacity.value() / 100)
        settings.set("wallpaper", self.wallpaper.text().strip())
        settings.set("weather_enabled", self.weather.isChecked())
        settings.set("latitude", self.lat.value())
        settings.set("longitude", self.lon.value())
        settings.save()
        self.accept()
