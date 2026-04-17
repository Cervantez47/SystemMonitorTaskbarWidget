# monitors/cpu_monitor.py

import psutil


def get_cpu_percent() -> float:
    """Return overall CPU usage as a percentage (0.0–100.0).

    Uses a non-blocking call; the first call after startup may return 0.0
    which is expected — subsequent calls reflect the real interval delta.
    """
    return psutil.cpu_percent(interval=None)
