"""Central configuration: constants plus user settings saved to settings.json."""
import json
from pathlib import Path

APP_NAME = "ArtemisSurf"
DEFAULT_HOME_URL = "https://bhuvanesh-m-dev.github.io/artemis-surf/home-page"
SEARCH_URL = "https://www.google.com/search?q="

DATA_DIR = Path.home() / ".artemissurf"
PROFILE_DIR = DATA_DIR / "profile"        # cookies + local storage (kept = stay signed in)
CACHE_DIR = DATA_DIR / "cache"            # wiped on every start and exit
BOOKMARKS_FILE = DATA_DIR / "bookmarks.json"
SETTINGS_FILE = DATA_DIR / "settings.json"

# A normal Chrome user agent helps Google / YouTube accept sign-in
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

# Files that would reveal browsing history; deleted on start and exit
HISTORY_FILES = ["Visited Links", "History", "History-journal", "Top Sites",
                 "Favicons", "Network Action Predictor"]

SIDE_WIDTH = 200   # equal left/right toolbar groups keep the address bar centered


class Settings:
    DEFAULTS = {
        "home_url": DEFAULT_HOME_URL,
        "opacity": 0.94,            # 1.0 = opaque, lower = more transparent
        "wallpaper": "",            # path to an image, empty = fully transparent
        "weather_enabled": False,
        "latitude": 0.0,
        "longitude": 0.0,
    }

    def __init__(self):
        self.data = dict(self.DEFAULTS)
        self.load()

    def load(self):
        try:
            saved = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
            self.data.update({k: v for k, v in saved.items() if k in self.DEFAULTS})
        except (OSError, ValueError):
            pass

    def save(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        SETTINGS_FILE.write_text(json.dumps(self.data, indent=2), encoding="utf-8")

    def get(self, key):
        return self.data.get(key, self.DEFAULTS[key])

    def set(self, key, value):
        self.data[key] = value


settings = Settings()
