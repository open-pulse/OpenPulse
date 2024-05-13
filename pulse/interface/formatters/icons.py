import os
import numpy as np
from PIL import Image
from pathlib import Path
from PyQt5.QtGui import QColor, QIcon, QPainter, QPixmap, QImage
from PyQt5.QtCore import QSize
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
    size = icon.actualSize(QSize(10_000, 10_000))
    if size.width() == 10_000:
        return

    pixmap: QPixmap = icon.pixmap(size)
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), color)
    painter.end()
    icon.addPixmap(pixmap)

# FIXIT
# def add_border_to_icon(icon: QIcon, thickness=3, color=(255, 255, 255, 255)):
#     # Extract pixmap from icon
#     size = icon.actualSize(QSize(10_000, 10_000))
#     if size.width() == 10_000:
#         return
#     pixmap: QPixmap = icon.pixmap(size)

#     # Transform pixmap into numpy ndarray
#     channels = 4  # rgba
#     image = pixmap.toImage().rgbSwapped()
#     bits = image.bits()
#     if bits is None:
#         return
#     bits.setsize(size.height() * size.width() * channels)
#     array: np.ndarray = np.frombuffer(bits, np.uint8).reshape((size.height(), size.width(), channels))
#     # TODO: Resize the array to fit the icon + borders inside it

#     # Extract an outline by doing a XOR between
#     # the trasnparency channel and its dilation
#     # kernel = disk(thickness)
#     kernel = disk(thickness)
#     mask = array[:, :, 3].astype(bool)
#     outline = mask ^ binary_dilation(mask, kernel)

#     # Paint all pixels that belong to the border as white
#     for i in range(size.height()):
#         for j in range(size.width()):
#             if outline[i, j]:
#                 array[i, j] = color

#     # import matplotlib.pyplot as plt
#     # plt.imshow(array)
#     # plt.show()
#     # exit()

#     qimage = QImage(array, array.shape[1], array.shape[0], QImage.Format_RGBA8888)
#     pixmap = QPixmap.fromImage(qimage)
#     icon.addPixmap(pixmap)