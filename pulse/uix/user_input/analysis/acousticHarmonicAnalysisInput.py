from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QTreeWidgetItem, QTabWidget, QComboBox, QPushButton
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

class AcousticHarmonicAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/Analysis/Acoustic/acousticHarmonicAnalysisInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.index = 0

        self.comboBox = self.findChild(QComboBox, 'comboBox')
        self.comboBox.currentIndexChanged.connect(self.selectionChange)
        self.index = self.comboBox.currentIndex()

        self.pushButton_2 = self.findChild(QPushButton, 'pushButton_2')
        self.pushButton_2.clicked.connect(self.button_clicked)

        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def selectionChange(self, index):
        self.index = self.comboBox.currentIndex()

    def check(self):
        self.close()

    def button_clicked(self):
        self.check()