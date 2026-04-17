# ui/hotkey.py — Global hotkey registration via Win32 RegisterHotKey

import ctypes
import ctypes.wintypes
from PyQt5.QtCore import QAbstractNativeEventFilter

# Ctrl+Alt+Z  — cycle widget corner
MOD_CONTROL   = 0x0002
MOD_ALT       = 0x0001
VK_Z          = 0x5A
HOTKEY_ID     = 1
WM_HOTKEY     = 0x0312


class GlobalHotkeyFilter(QAbstractNativeEventFilter):
    """Installs a Win32 global hotkey and calls `on_corner_cycle` when triggered."""

    def __init__(self, on_corner_cycle):
        super().__init__()
        self._callback = on_corner_cycle
        ok = ctypes.windll.user32.RegisterHotKey(None, HOTKEY_ID, MOD_CONTROL | MOD_ALT, VK_Z)
        if not ok:
            print("[hotkey] WARNING: Could not register Ctrl+Alt+Z — already in use?")

    def nativeEventFilter(self, eventType, message):
        if eventType == b"windows_generic_MSG":
            try:
                msg = ctypes.wintypes.MSG.from_address(int(message))
                if msg.message == WM_HOTKEY and msg.wParam == HOTKEY_ID:
                    self._callback()
                    return True, 0
            except Exception:
                pass
        return False, 0

    def unregister(self):
        ctypes.windll.user32.UnregisterHotKey(None, HOTKEY_ID)
