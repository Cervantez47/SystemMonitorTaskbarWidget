# ui/styles.py — Layout constants and color helpers

from config import (
    COLOR_BACKGROUND,
    COLOR_LABEL,
    COLOR_VALUE_NORMAL,
    COLOR_VALUE_WARN,
    COLOR_VALUE_CRITICAL,
    THRESHOLD_WARN,
    THRESHOLD_CRITICAL,
    FONT_FAMILY,
    FONT_SIZE,
)
from PyQt5.QtGui import QColor, QFont


def bg_color() -> QColor:
    return QColor(*COLOR_BACKGROUND)


def label_color() -> QColor:
    return QColor(*COLOR_LABEL)


def value_color(percent: float) -> QColor:
    if percent >= THRESHOLD_CRITICAL:
        return QColor(*COLOR_VALUE_CRITICAL)
    if percent >= THRESHOLD_WARN:
        return QColor(*COLOR_VALUE_WARN)
    return QColor(*COLOR_VALUE_NORMAL)


def default_font() -> QFont:
    f = QFont(FONT_FAMILY, FONT_SIZE)
    return f


def bold_font() -> QFont:
    f = QFont(FONT_FAMILY, FONT_SIZE)
    f.setBold(True)
    return f
