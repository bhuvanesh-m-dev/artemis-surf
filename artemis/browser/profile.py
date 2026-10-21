"""Web profile: keeps logins (cookies), never keeps cache or history."""
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings

from artemis.browser.downloads import attach_download_handler
from artemis.config import APP_NAME, CACHE_DIR, PROFILE_DIR, USER_AGENT


def build_profile() -> QWebEngineProfile:
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    profile = QWebEngineProfile(APP_NAME)
    profile.setPersistentStoragePath(str(PROFILE_DIR))
    profile.setCachePath(str(CACHE_DIR))
    profile.setPersistentCookiesPolicy(
        QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)  # stay signed in
    profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.NoCache)      # no cached pages
    profile.setHttpUserAgent(USER_AGENT)

    s = profile.settings()
    s.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
    s.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
    s.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
    s.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)

    attach_download_handler(profile)
    return profile
