# SystemMonitorTaskbarWidget

A lightweight Windows 11 system monitor widget that floats near the taskbar, showing real-time CPU, RAM, disk, and network usage at a glance — no bloat, no settings panels.

## Features

- **CPU usage** — updated every second, color-coded by load
- **RAM usage** — updated every second
- **Disk usage** — all local physical drives (C:, D:, etc.); Google Drive and network drives automatically excluded
- **Network speed** — live upload / download in KB/s or MB/s
- **Color coding** — white (normal) → yellow (>70%) → red (>90%)
- **Corner cycling** — press `Ctrl+Alt+Z` to cycle the widget between all four screen corners; position is remembered across restarts
- **System tray** — right-click for Show/Hide, Start with Windows toggle, and Exit
- **Start with Windows** — one-click toggle; no admin rights required

## Why a floating widget and not embedded in the taskbar?

Windows 11 rewrote the taskbar in WinUI 3 with no public API for third-party content injection. A frameless always-on-top window is the standard approach used by tools like TrafficMonitor and HWiNFO.

---

## Requirements

- Windows 10 / 11 (64-bit)
- Python 3.11+ *(only needed to run from source)*
- Dependencies: `psutil`, `PyQt5`

---

## Installation

### Option A — Run from source

```bash
git clone https://github.com/Cervantez47/SystemMonitorTaskbarWidget.git
cd SystemMonitorTaskbarWidget
pip install -r requirements.txt
pythonw main.py
```

### Option B — Build a standalone .exe

```bash
pip install -r requirements.txt
build.bat
# Output: dist\SystemMonitorTaskbarWidget.exe
```

Run the `.exe` directly — no Python installation required.

---

## Usage

- **Launch:** `pythonw main.py` (or double-click the `.exe`)
- **Tray icon:** Green square in the system notification area (bottom-right of taskbar)
  - Double-click → show / hide widget
  - Right-click → full menu

---

## Keyboard Shortcut

| Shortcut | Action |
|---|---|
| `Ctrl+Alt+Z` | Cycle widget to next screen corner |

Corner order: bottom-right → bottom-left → top-left → top-right → (repeat)

Your last position is saved to `%APPDATA%\SystemMonitorTaskbarWidget\state.json` and restored on next launch.

---

## Configuration

Edit [config.py](config.py) to customize:

| Setting | Default | Description |
|---|---|---|
| `REFRESH_INTERVAL_FAST_MS` | `1000` | CPU / RAM / Network update interval (ms) |
| `REFRESH_INTERVAL_SLOW_MS` | `5000` | Disk update interval (ms) |
| `WIDGET_OPACITY` | `0.92` | Widget transparency (0.0–1.0) |
| `THRESHOLD_WARN` | `70` | Yellow color threshold (%) |
| `THRESHOLD_CRITICAL` | `90` | Red color threshold (%) |
| `FONT_FAMILY` | `Segoe UI` | Display font |
| `FONT_SIZE` | `9` | Font size (pt) |
| `DISK_EXCLUDE_MOUNTPOINTS` | `set()` | Extra drive letters to hide |

---

## Project Structure

```
SystemMonitorTaskbarWidget/
├── main.py                   # Entry point
├── config.py                 # All user-tunable settings
├── startup.py                # Windows startup registry helpers
├── build.bat                 # PyInstaller packaging script
├── requirements.txt
├── monitors/
│   ├── cpu_monitor.py
│   ├── ram_monitor.py
│   ├── disk_monitor.py       # Filters Google Drive / network drives by volume label
│   └── network_monitor.py    # Delta-based upload/download speed
└── ui/
    ├── widget.py             # Frameless always-on-top window, corner logic
    ├── tray.py               # System tray icon + context menu
    ├── hotkey.py             # Win32 RegisterHotKey global shortcut
    └── styles.py             # Colors, fonts, threshold-based color coding
```

---

## License

MIT
