"""Optional weather lookup using the free Open-Meteo API (no key needed)."""
import json
import urllib.request

from PyQt6.QtCore import QThread, pyqtSignal

CODES = {0: "Clear", 1: "Mostly clear", 2: "Partly cloudy", 3: "Overcast", 45: "Fog",
         51: "Drizzle", 61: "Rain", 63: "Rain", 65: "Heavy rain", 71: "Snow",
         80: "Showers", 95: "Thunderstorm"}


def fetch_weather(lat: float, lon: float) -> str:
    url = ("https://api.open-meteo.com/v1/forecast"
           f"?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code")
    with urllib.request.urlopen(url, timeout=6) as resp:
        current = json.loads(resp.read().decode())["current"]
    desc = CODES.get(current.get("weather_code"), "")
    return f"{current['temperature_2m']}°C {desc}".strip()


class WeatherWorker(QThread):
    result = pyqtSignal(str)

    def __init__(self, lat, lon):
        super().__init__()
        self.lat, self.lon = lat, lon

    def run(self):
        try:
            self.result.emit(fetch_weather(self.lat, self.lon))
        except Exception:
            self.result.emit("weather unavailable")
