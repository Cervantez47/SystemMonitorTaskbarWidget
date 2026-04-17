# main.py — Entry point for SystemMonitorTaskbarWidget

import sys
import psutil  # noqa: F401 — validate install at startup

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from ui.widget import MonitorWidget
from ui.tray import TrayIcon
from ui.hotkey import GlobalHotkeyFilter


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    widget = MonitorWidget()
    widget.show()

    tray = TrayIcon(widget)
    tray.show()

    # Register Ctrl+Alt+Z global hotkey → cycle widget corner
    hotkey_filter = GlobalHotkeyFilter(widget.cycle_corner)
    app.installNativeEventFilter(hotkey_filter)

    ret = app.exec_()
    hotkey_filter.unregister()
    sys.exit(ret)


if __name__ == "__main__":
    main()
