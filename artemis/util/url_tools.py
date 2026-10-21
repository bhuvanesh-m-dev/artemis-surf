"""Decides whether address-bar text is a URL or a search."""
from typing import Optional
from urllib.parse import quote_plus

from PyQt6.QtCore import QUrl

from artemis.config import SEARCH_URL


def resolve(text: str) -> Optional[QUrl]:
    text = text.strip()
    if not text:
        return None
    has_scheme = "://" in text or text.startswith(("about:", "file:", "data:"))
    looks_like_url = (has_scheme or "." in text or text.startswith("localhost")) and " " not in text
    if looks_like_url:
        return QUrl.fromUserInput(text)
    return QUrl(SEARCH_URL + quote_plus(text))
