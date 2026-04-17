# ui/tray.py — System tray icon with right-click context menu

import startup
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPainter
from PyQt5.QtCore import Qt


def _make_icon() -> QIcon:
    """Generate a simple colored square icon (no external image file needed)."""
    pixmap = QPixmap(16, 16)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(QColor(80, 200, 120))
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(0, 0, 16, 16, 3, 3)
    painter.end()
    return QIcon(pixmap)


class TrayIcon(QSystemTrayIcon):
    def __init__(self, widget, parent=None):
        super().__init__(_make_icon(), parent)
        self._widget = widget
        self.setToolTip("System Monitor  |  Ctrl+Alt+Z → cycle corner")
        self._build_menu()
        self.activated.connect(self._on_activated)

    def _build_menu(self):
        menu = QMenu()

        show_action = QAction("Show / Hide", menu)
        show_action.triggered.connect(self._toggle_visibility)
        menu.addAction(show_action)

        menu.addSeparator()

        # Startup toggle — reflects current registry state
        self._startup_action = QAction("Start with Windows", menu)
        self._startup_action.setCheckable(True)
        self._startup_action.setChecked(startup.is_enabled())
        self._startup_action.triggered.connect(self._toggle_startup)
        menu.addAction(self._startup_action)

        menu.addSeparator()

        quit_action = QAction("Exit", menu)
        quit_action.triggered.connect(QApplication.quit)
        menu.addAction(quit_action)

        self.setContextMenu(menu)

    def _toggle_visibility(self):
        if self._widget.isVisible():
            self._widget.hide()
        else:
            self._widget.show()

    def _toggle_startup(self, checked: bool):
        if checked:
            startup.enable()
        else:
            startup.disable()
        # Re-read actual registry state in case of error
        self._startup_action.setChecked(startup.is_enabled())

    def _on_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self._toggle_visibility()
