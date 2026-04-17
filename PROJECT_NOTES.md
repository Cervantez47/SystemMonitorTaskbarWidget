# SystemMonitorTaskbarWidget — Project Notes

## Overview

A lightweight Windows 11 taskbar widget displaying real-time system metrics:
- CPU usage (%)
- RAM usage (%)
- HDD/SSD storage usage across all local physical disks (excludes Google Drive / network-mapped drives)
- Network usage (upload/download speeds in KB/s or MB/s)

## Approach

Windows 11 has no native public API for embedding content into the taskbar itself.
The chosen approach is a **frameless, always-on-top floating window** anchored to the
taskbar area at the bottom of the screen. This is the same technique used by popular
tools like TrafficMonitor and similar utilities.

- On launch the widget auto-positions itself just above or overlapping the taskbar
- It is non-interactive by default (click-through optional) but can have a right-click context menu
- It runs in the background as a tray icon with options to show/hide/exit

## Tech Stack

| Layer | Tool | Reason |
|---|---|---|
| Language | Python 3.11+ | Rapid dev, rich ecosystem |
| System Metrics | `psutil` | Cross-platform, covers CPU/RAM/disk/net |
| UI Framework | `PyQt5` | Frameless windows, painters, transparency support |
| Tray Icon | `PyQt5 QSystemTrayIcon` | Native Windows tray integration |
| Packaging | `PyInstaller` | Single `.exe` for distribution |

## Disk Filtering Logic

- Enumerate all partitions via `psutil.disk_partitions()`
- Include only partitions with `fstype` in `['NTFS', 'FAT32', 'exFAT', 'ReFS']`
- Exclude any mount point that is a network/virtual drive (Google Drive maps as a network
  drive letter, e.g. `G:\`, with `opts` containing `remote`)
- Exclude partitions where `psutil.disk_usage()` raises `PermissionError`

---

## Scaffold Structure

```
SystemMonitorTaskbarWidget/
├── PROJECT_NOTES.md          ← this file
├── main.py                   ← entry point; launches QApplication + widget
├── requirements.txt          ← psutil, PyQt5, pyinstaller
├── config.py                 ← user-tunable settings (refresh rate, colors, etc.)
├── monitors/
│   ├── __init__.py
│   ├── cpu_monitor.py        ← CPU % via psutil.cpu_percent()
│   ├── ram_monitor.py        ← RAM % via psutil.virtual_memory()
│   ├── disk_monitor.py       ← Disk usage; filters out Google Drive / network drives
│   └── network_monitor.py    ← Net speed; delta bytes over interval
└── ui/
    ├── __init__.py
    ├── widget.py             ← Main QWidget: frameless, always-on-top, taskbar-anchored
    ├── tray.py               ← QSystemTrayIcon with right-click menu
    └── styles.py             ← Colors, fonts, layout constants
```

---

## Development Log

### 2026-04-17 — Project Initialized

- [x] Created project directory `d:\VS Code\projects\SystemMonitorTaskbarWidget`
- [x] Drafted PROJECT_NOTES.md with overview, approach, tech stack, scaffold structure
- [x] Create directory scaffold (all folders + `__init__.py` files)
- [x] Write `requirements.txt`
- [x] Write `config.py`
- [x] Implement `monitors/cpu_monitor.py`
- [x] Implement `monitors/ram_monitor.py`
- [x] Implement `monitors/disk_monitor.py`
- [x] Implement `monitors/network_monitor.py`
- [x] Implement `ui/styles.py`
- [x] Implement `ui/widget.py`
- [x] Implement `ui/tray.py`
- [x] Implement `main.py`
- [x] Test: metrics accuracy
- [x] Test: Google Drive exclusion — detected via volume label ("Google Drive"); fstype=FAT32/rw,fixed not reliable
- [x] Test: window anchoring / repositioning on resolution change
- [x] Test: tray icon show/hide/exit
- [x] Add corner cycling — Ctrl+Alt+Z cycles bottom-right → bottom-left → top-left → top-right
- [x] Add startup registration — "Start with Windows" toggle in tray menu (HKCU Run key)
- [x] Corner preference persists across restarts (%APPDATA%\SystemMonitorTaskbarWidget\state.json)
- [x] Write README.md
- [x] Write .gitignore
- [x] Write build.bat (PyInstaller packaging script)
- [x] Initialize git repo and push to GitHub (Cervantez47/SystemMonitorTaskbarWidget)
- [ ] Package with PyInstaller → `.exe` (run build.bat)

---

## Key Decisions & Notes

- **Refresh interval:** default 1 second for network/CPU, 5 seconds for disk
- **Network baseline:** delta is calculated between ticks, so first reading shows 0 — expected behavior
- **Multi-monitor:** widget anchors to the primary display's taskbar by default
- **Dark/light mode:** default dark theme to match Windows 11 taskbar aesthetics; configurable in `config.py`
- **Google Drive detection:** Google Drive for Desktop uses WinFSP — appears as `FAT32 rw,fixed` (NOT `remote`). Detected by calling `GetVolumeInformationW` and checking the volume label for "Google".
- **Corner cycling:** `Ctrl+Alt+Z` cycles bottom-right → bottom-left → top-left → top-right. Preference saved to `%APPDATA%\SystemMonitorTaskbarWidget\state.json`.
- **Startup:** "Start with Windows" toggle in tray right-click menu. Writes `pythonw.exe main.py` (or `.exe` path when packaged) to `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`.
- **Hotkey `Ctrl+Alt+M` was taken** (Teams mute) — using `Ctrl+Alt+Z` instead.
