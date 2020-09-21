from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QPushButton, QLabel, QComboBox, QWidget
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

from pulse.utils import error
from pulse.preprocessing.cross_section import CrossSection

import numpy as np
import matplotlib.pyplot as plt  

class PrintMessageInput(QDialog):
    def __init__(self, text_info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/printMessages.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.Label_message = self.findChild(QLabel, 'Label_message')
        self.Label_title = self.findChild(QLabel, 'Label_title')

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.message_close)

        self.text_info = text_info
        self.Label_title.setText(text_info[0])
        self.Label_message.setText(text_info[1])

        self.exec_()

    def message_close(self):
        self.close()