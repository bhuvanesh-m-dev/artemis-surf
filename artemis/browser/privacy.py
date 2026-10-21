"""Deletes cache and history artifacts. Cookies / local storage are never touched."""
import shutil

from artemis.config import CACHE_DIR, HISTORY_FILES, PROFILE_DIR


def wipe_private_data():
    shutil.rmtree(CACHE_DIR, ignore_errors=True)
    for name in HISTORY_FILES:
        path = PROFILE_DIR / name
        try:
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            elif path.exists():
                path.unlink()
        except OSError:
            pass
