"""Creates the QApplication, the private profile and the main window."""
import gc
import sys

from PyQt6.QtCore import QCoreApplication, QEvent
from PyQt6.QtWidgets import QApplication

from artemis.browser.privacy import wipe_private_data
from artemis.browser.profile import build_profile
from artemis.browser.window import BrowserWindow
from artemis.config import APP_NAME


def run():
    wipe_private_data()                 # clean leftovers from a crash
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)

    profile = build_profile()
    window = BrowserWindow(profile)
    window.show()
    code = app.exec()

    # release web objects before the profile, then delete history artifacts
    window.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
    del window
    gc.collect()
    del profile
    wipe_private_data()
    sys.exit(code)
