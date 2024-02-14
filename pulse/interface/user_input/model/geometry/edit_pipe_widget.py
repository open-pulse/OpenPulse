from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QCheckBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

from opps import UI_DIR


class EditPipeWidget(QWidget):
    def __init__(self, geometry_widget, parent=None):
        super().__init__(parent)
        uic.loadUi(Path("pulse/interface/ui_files/model/geometry/edit_pipe.ui"), self)
