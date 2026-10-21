"""Bookmarks stored as {url: title} in bookmarks.json."""
import json

from artemis.config import BOOKMARKS_FILE, DATA_DIR


class Bookmarks:
    def __init__(self):
        self._items = {}
        self.load()

    def load(self):
        try:
            self._items = json.loads(BOOKMARKS_FILE.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            self._items = {}

    def save(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        BOOKMARKS_FILE.write_text(json.dumps(self._items, indent=2), encoding="utf-8")

    def has(self, url: str) -> bool:
        return url in self._items

    def toggle(self, url: str, title: str = ""):
        if not url:
            return
        if url in self._items:
            del self._items[url]
        else:
            self._items[url] = title or url
        self.save()

    def items(self):
        return list(self._items.items())
