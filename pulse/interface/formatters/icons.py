import os
import numpy as np
from PIL import Image
from pathlib import Path
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap, QImage
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

def change_icon_color(icon: QIcon, color: QColor):
    if icon is None:
        return 

    size = icon.actualSize(QSize(10_000, 10_000))
    invalid_sizes = [-1, 0, 10_000]

    if size.width() in invalid_sizes:
        return
    
    if size.height() in invalid_sizes:
        return

    pixmap: QPixmap = icon.pixmap(size)
    painter = QPainter(pixmap)
    if not painter.isActive():
        return

    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), color)
    painter.end()
    icon.addPixmap(pixmap)

def change_icon_color_for_widgets(widgets: list[QWidget], color: QColor):
    for widget in widgets:
        if not hasattr(widget, "icon") or not callable(widget.icon):
            continue
        
        if not hasattr(widget, "setIcon") or not callable(widget.setIcon):
            continue
        
        icon = widget.icon()
        change_icon_color(icon, color)
        widget.setIcon(icon)
