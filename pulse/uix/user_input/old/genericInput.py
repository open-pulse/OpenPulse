from PyQt5.QtWidgets import QLabel, QToolButton, QLineEdit, QDialogButtonBox, QFileDialog, QDialog, QColorDialog, QMessageBox
from os.path import basename
from PyQt5.QtGui import QColor
from PyQt5 import uic
import configparser

class GenericInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/addTemp.ui', self)
        self.exec_()