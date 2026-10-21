"""Checks dependencies and creates the data folders before the app starts."""
import sys


def ensure_ready():
    try:
        import PyQt6.QtWebEngineWidgets  # noqa: F401
    except ImportError:
        print("Missing dependencies. Install them with:\n"
              "    pip install -r requirements.txt")
        sys.exit(1)

    from artemis.config import CACHE_DIR, DATA_DIR, PROFILE_DIR
    for folder in (DATA_DIR, PROFILE_DIR, CACHE_DIR):
        folder.mkdir(parents=True, exist_ok=True)
