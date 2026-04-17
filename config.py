# config.py — User-tunable settings for SystemMonitorTaskbarWidget

# Refresh intervals (milliseconds)
REFRESH_INTERVAL_FAST_MS = 1000   # CPU, RAM, Network
REFRESH_INTERVAL_SLOW_MS = 5000   # Disk (expensive to poll frequently)

# Widget appearance
WIDGET_OPACITY = 0.92             # 0.0 (invisible) to 1.0 (opaque)
WIDGET_HEIGHT = 28                # pixels; matches default Win11 taskbar height
WIDGET_PADDING_RIGHT = 8         # pixels from right edge of screen

# Colors (R, G, B)
COLOR_BACKGROUND = (20, 20, 20)
COLOR_LABEL = (160, 160, 160)
COLOR_VALUE_NORMAL = (220, 220, 220)
COLOR_VALUE_WARN = (255, 200, 60)    # > WARN threshold
COLOR_VALUE_CRITICAL = (255, 80, 80) # > CRITICAL threshold

# Thresholds (%) for color change
THRESHOLD_WARN = 70
THRESHOLD_CRITICAL = 90

# Font
FONT_FAMILY = "Segoe UI"
FONT_SIZE = 9

# Network display unit auto-scaling
# Shows KB/s below this bytes/s value, MB/s above
NETWORK_MB_THRESHOLD = 1_000_000  # 1 MB/s

# Disk filtering
# Partition fstypes to include (local physical drives only)
DISK_INCLUDE_FSTYPES = {"NTFS", "FAT32", "exFAT", "ReFS"}
# Drive letters/paths to always exclude (e.g. Google Drive, OneDrive virtual mounts)
# Add mount points here if auto-detection misses them
DISK_EXCLUDE_MOUNTPOINTS = set()
