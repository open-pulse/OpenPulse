import os
from pathlib import Path
from PyQt5.QtGui import QColor, QIcon, QPainter, QPixmap
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