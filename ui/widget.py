# ui/widget.py — Frameless always-on-top taskbar widget with corner cycling

import json
import os

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QApplication
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor

from config import (
    REFRESH_INTERVAL_FAST_MS,
    REFRESH_INTERVAL_SLOW_MS,
    WIDGET_OPACITY,
    WIDGET_HEIGHT,
    WIDGET_PADDING_RIGHT,
    NETWORK_MB_THRESHOLD,
)
from monitors.cpu_monitor import get_cpu_percent
from monitors.ram_monitor import get_ram_percent
from monitors.disk_monitor import get_disk_usages
from monitors.network_monitor import NetworkMonitor, format_speed
from ui.styles import bg_color, label_color, value_color, default_font

# Corner constants (cycle order on each hotkey press)
CORNERS = ["bottom-right", "bottom-left", "top-left", "top-right"]

_STATE_FILE = os.path.join(
    os.environ.get("APPDATA", os.path.dirname(os.path.abspath(__file__))),
    "SystemMonitorTaskbarWidget", "state.json"
)


def _load_corner() -> str:
    try:
        with open(_STATE_FILE) as f:
            return json.load(f).get("corner", "bottom-right")
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return "bottom-right"


def _save_corner(corner: str):
    os.makedirs(os.path.dirname(_STATE_FILE), exist_ok=True)
    try:
        with open(_STATE_FILE, "w") as f:
            json.dump({"corner": corner}, f)
    except OSError:
        pass


class MonitorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._net = NetworkMonitor()
        self._disk_data = []
        self._corner = _load_corner()

        self._setup_window()
        self._setup_labels()

        # Fast timer: CPU, RAM, Network
        self._fast_timer = QTimer(self)
        self._fast_timer.timeout.connect(self._update_fast)
        self._fast_timer.start(REFRESH_INTERVAL_FAST_MS)

        # Slow timer: Disk
        self._slow_timer = QTimer(self)
        self._slow_timer.timeout.connect(self._update_disk)
        self._slow_timer.start(REFRESH_INTERVAL_SLOW_MS)

        # Seed first reads
        get_cpu_percent()   # baseline — first call always 0.0
        self._update_fast()
        self._update_disk()

    # ------------------------------------------------------------------
    # Window setup
    # ------------------------------------------------------------------

    def _setup_window(self):
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(WIDGET_OPACITY)
        self.setFixedHeight(WIDGET_HEIGHT)

    def _setup_labels(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(14)

        font = default_font()

        def make_pair(tag: str) -> tuple:
            lbl = QLabel(tag)
            lbl.setFont(font)
            lbl.setStyleSheet(f"color: rgb(160,160,160);")

            val = QLabel("—")
            val.setFont(font)
            val.setStyleSheet("color: rgb(220,220,220);")

            layout.addWidget(lbl)
            layout.addWidget(val)
            return lbl, val

        _, self._cpu_val = make_pair("CPU")
        _, self._ram_val = make_pair("RAM")

        self._disk_labels: list = []
        self._disk_layout = layout

        _, self._net_up_val  = make_pair("↑")
        _, self._net_dn_val  = make_pair("↓")

    # ------------------------------------------------------------------
    # Corner positioning
    # ------------------------------------------------------------------

    def _reposition(self):
        """Move widget to the current corner of the primary screen."""
        screen    = QApplication.primaryScreen().geometry()
        available = QApplication.primaryScreen().availableGeometry()
        w   = self.width()
        h   = WIDGET_HEIGHT
        pad = WIDGET_PADDING_RIGHT

        if self._corner == "bottom-right":
            x = screen.right()  - w - pad
            y = available.bottom() - h
        elif self._corner == "bottom-left":
            x = screen.left()   + pad
            y = available.bottom() - h
        elif self._corner == "top-left":
            x = screen.left()   + pad
            y = screen.top()    + pad
        elif self._corner == "top-right":
            x = screen.right()  - w - pad
            y = screen.top()    + pad
        else:
            x = screen.right()  - w - pad
            y = available.bottom() - h

        self.move(x, y)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._reposition()

    def cycle_corner(self):
        """Advance to the next corner and persist the choice."""
        idx = CORNERS.index(self._corner) if self._corner in CORNERS else 0
        self._corner = CORNERS[(idx + 1) % len(CORNERS)]
        _save_corner(self._corner)
        self._reposition()

    # ------------------------------------------------------------------
    # Custom painting
    # ------------------------------------------------------------------

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = bg_color()
        color.setAlpha(230)
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 4, 4)

    # ------------------------------------------------------------------
    # Update slots
    # ------------------------------------------------------------------

    def _update_fast(self):
        cpu = get_cpu_percent()
        self._cpu_val.setText(f"{cpu:.0f}%")
        self._cpu_val.setStyleSheet(f"color: {value_color(cpu).name()};")

        ram = get_ram_percent()
        self._ram_val.setText(f"{ram:.0f}%")
        self._ram_val.setStyleSheet(f"color: {value_color(ram).name()};")

        speeds = self._net.get_speeds()
        self._net_up_val.setText(format_speed(speeds["upload_bps"],   NETWORK_MB_THRESHOLD))
        self._net_dn_val.setText(format_speed(speeds["download_bps"], NETWORK_MB_THRESHOLD))

        self.adjustSize()
        self._reposition()

    def _update_disk(self):
        self._disk_data = get_disk_usages()

        for lbl, val in self._disk_labels:
            lbl.hide(); lbl.deleteLater()
            val.hide(); val.deleteLater()
        self._disk_labels.clear()

        insert_index = 4
        font = default_font()
        for disk in self._disk_data:
            drive = disk["mountpoint"].rstrip("\\").rstrip(":")
            tag = QLabel(f"[{drive}]")
            tag.setFont(font)
            tag.setStyleSheet("color: rgb(160,160,160);")

            pct = disk["percent"]
            val = QLabel(f"{pct:.0f}%")
            val.setFont(font)
            val.setStyleSheet(f"color: {value_color(pct).name()};")

            self._disk_layout.insertWidget(insert_index,     tag)
            self._disk_layout.insertWidget(insert_index + 1, val)
            insert_index += 2
            self._disk_labels.append((tag, val))

        self.adjustSize()
        self._reposition()
