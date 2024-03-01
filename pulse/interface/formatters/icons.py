from pathlib import Path
from PyQt5.QtGui import QColor, QIcon, QPainter, QPixmap

def get_formatted_icon(path: Path | str, color: QColor):
    pixmap = QPixmap(str(path))
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), color)
    painter.end()
    return QIcon(pixmap)

def get_openpulse_icon(color: QColor):
    icon_path = str(Path('data/icons/pulse.png'))
    return get_formatted_icon(icon_path, color)