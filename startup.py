# startup.py — Windows startup registry helpers

import os
import sys
import winreg

_REG_KEY  = r"Software\Microsoft\Windows\CurrentVersion\Run"
_APP_NAME = "SystemMonitorTaskbarWidget"


def _launch_command() -> str:
    """Return the command to add to the registry Run key."""
    if getattr(sys, "frozen", False):
        # Running as a PyInstaller .exe
        return f'"{sys.executable}"'
    # Running as a plain Python script
    pythonw = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    script  = os.path.abspath(os.path.join(os.path.dirname(__file__), "main.py"))
    return f'"{pythonw}" "{script}"'


def is_enabled() -> bool:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, _REG_KEY, 0, winreg.KEY_READ)
        winreg.QueryValueEx(key, _APP_NAME)
        winreg.CloseKey(key)
        return True
    except (FileNotFoundError, OSError):
        return False


def enable():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, _REG_KEY, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, _APP_NAME, 0, winreg.REG_SZ, _launch_command())
    winreg.CloseKey(key)


def disable():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, _REG_KEY, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, _APP_NAME)
        winreg.CloseKey(key)
    except (FileNotFoundError, OSError):
        pass
