# monitors/ram_monitor.py

import psutil


def get_ram_percent() -> float:
    """Return RAM usage as a percentage (0.0–100.0)."""
    return psutil.virtual_memory().percent
