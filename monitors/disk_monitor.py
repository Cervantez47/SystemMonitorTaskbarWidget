# monitors/disk_monitor.py

import ctypes
import psutil
from config import DISK_INCLUDE_FSTYPES, DISK_EXCLUDE_MOUNTPOINTS


def _get_volume_label(mountpoint: str) -> str:
    """Return the volume label for the given mount point (e.g. 'C:\\')."""
    buf = ctypes.create_unicode_buffer(256)
    try:
        ctypes.windll.kernel32.GetVolumeInformationW(
            mountpoint, buf, 256, None, None, None, None, 0
        )
    except OSError:
        return ""
    return buf.value


def _is_local_physical(partition) -> bool:
    """Return True if the partition is a local physical drive we want to display."""
    # Must be a known local filesystem type
    if partition.fstype.upper() not in DISK_INCLUDE_FSTYPES:
        return False

    # Skip any drive flagged as remote (covers traditional mapped network drives)
    opts = partition.opts.lower()
    if "remote" in opts:
        return False

    # Google Drive for Desktop mounts via WinFSP — appears as FAT32 rw,fixed but
    # its volume label contains "Google Drive". Exclude it by label.
    label = _get_volume_label(partition.mountpoint).lower()
    if "google" in label:
        return False

    # Skip any mount points the user has explicitly excluded in config
    if partition.mountpoint in DISK_EXCLUDE_MOUNTPOINTS:
        return False

    return True


def get_disk_usages() -> list[dict]:
    """Return a list of dicts for each qualifying local disk.

    Each dict contains:
        mountpoint (str): e.g. "C:\\"
        total_gb (float): total capacity in GB
        used_gb (float): used space in GB
        percent (float): used percentage (0.0–100.0)
    """
    results = []
    for partition in psutil.disk_partitions(all=False):
        if not _is_local_physical(partition):
            continue
        try:
            usage = psutil.disk_usage(partition.mountpoint)
        except (PermissionError, OSError):
            continue

        results.append({
            "mountpoint": partition.mountpoint,
            "total_gb": usage.total / 1_073_741_824,
            "used_gb": usage.used / 1_073_741_824,
            "percent": usage.percent,
        })

    return results
