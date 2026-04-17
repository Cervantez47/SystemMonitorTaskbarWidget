# monitors/network_monitor.py

import time
import psutil


class NetworkMonitor:
    """Tracks upload and download speeds between polling ticks."""

    def __init__(self):
        counters = psutil.net_io_counters()
        self._last_bytes_sent = counters.bytes_sent
        self._last_bytes_recv = counters.bytes_recv
        self._last_time = time.monotonic()

    def get_speeds(self) -> dict:
        """Return current upload/download speeds.

        Returns:
            dict with keys:
                upload_bps (float): bytes per second sent
                download_bps (float): bytes per second received
        """
        now = time.monotonic()
        counters = psutil.net_io_counters()

        elapsed = now - self._last_time
        if elapsed <= 0:
            return {"upload_bps": 0.0, "download_bps": 0.0}

        upload_bps = (counters.bytes_sent - self._last_bytes_sent) / elapsed
        download_bps = (counters.bytes_recv - self._last_bytes_recv) / elapsed

        self._last_bytes_sent = counters.bytes_sent
        self._last_bytes_recv = counters.bytes_recv
        self._last_time = now

        return {
            "upload_bps": max(upload_bps, 0.0),
            "download_bps": max(download_bps, 0.0),
        }


def format_speed(bps: float, mb_threshold: int) -> str:
    """Format bytes-per-second into a human-readable string."""
    if bps >= mb_threshold:
        return f"{bps / 1_048_576:.1f} MB/s"
    return f"{bps / 1024:.0f} KB/s"
