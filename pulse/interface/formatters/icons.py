from pathlib import Path
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap
from PySide6.QtCore import QSize
from pulse import ICON_DIR

def get_icons_path(filename):
    path = ICON_DIR / filename
    if path.exists():
        return str(path)

def get_formatted_icon(path: Path | str, color: QColor):
    pixmap = QPixmap(str(path))
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), color)
    painter.end()
    return QIcon(pixmap)

def get_openpulse_icon(color=QColor("#0055DD")):

    icon_path =  str(ICON_DIR / 'pulse/pulse_icon.png')
    # return get_formatted_icon(icon_path, color)
    return QIcon(icon_path)

def get_warning_icon(color=None):
    if color is None:
        icon_path =  str(ICON_DIR / 'warnings/warning_2.png')
        return QIcon(icon_path)
    else:
        icon_path = str(ICON_DIR / 'warnings/transparent_warning.png')
        return get_formatted_icon(icon_path, color)

def get_error_icon(color=None):
    if color is None:
        icon_path = str(ICON_DIR / 'warnings/warning_2.png')
        return QIcon(icon_path)
    else:
        icon_path = str(ICON_DIR / 'warnings/transparent_warning.png')
        return get_formatted_icon(icon_path, color)

def change_icon_color(icon: QIcon, size: QSize, color: QColor):
    if icon is None or icon.isNull():
        return None

    pixmap = icon.pixmap(size)
    if pixmap.isNull():
        return None

    painter = QPainter(pixmap)
    if not painter.isActive():
        return None

    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), color)
    painter.end()
    return QIcon(pixmap)

def change_icon_color_for_widgets(widgets, color: QColor):
    for widget in widgets:
        if not hasattr(widget, "icon") or not callable(widget.icon):
            continue

        if not hasattr(widget, "setIcon") or not callable(widget.setIcon):
            continue

        if hasattr(widget, "should_paint") and not widget.should_paint:
            continue

        icon = widget.icon()
        size = widget.iconSize() if hasattr(widget, "iconSize") else icon.actualSize(QSize(256, 256))
        new_icon = change_icon_color(icon, size, color)
        if new_icon is not None:
            widget.setIcon(new_icon)
