from PyQt5.QtWidgets import  QDialog, QComboBox, QPushButton, QRadioButton
from pulse.utils import error
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

class ElementTypeInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/elementTypeInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.index = 0
        self.element_type = 'pipe_1'
        self.flagAll = False
        self.flagEntity = False

        self.comboBox = self.findChild(QComboBox, 'comboBox')
        self.comboBox.currentIndexChanged.connect(self.selectionChange)
        self.index = self.comboBox.currentIndex()

        self.radioButton_all = self.findChild(QRadioButton, 'radioButton_all')
        self.radioButton_entity = self.findChild(QRadioButton, 'radioButton_entity')
        self.radioButton_all.toggled.connect(self.radioButtonEvent)
        self.radioButton_entity.toggled.connect(self.radioButtonEvent)

        self.pushButton_2 = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_2.clicked.connect(self.button_clicked)

        self.exec_()

    def radioButtonEvent(self):
        self.flagAll = self.radioButton_all.isChecked()
        self.flagEntity = self.radioButton_entity.isChecked()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            # self.index = -1
            self.close()

    def selectionChange(self, index):
        self.index = self.comboBox.currentIndex()
        if self.index == 0:
            self.element_type = 'pipe_1'
        elif self.index == 1:
            self.element_type = 'pipe_2'
        elif self.index == 2:
            self.element_type = 'shell'

    def check(self):
        self.close()

    def button_clicked(self):
        self.check()