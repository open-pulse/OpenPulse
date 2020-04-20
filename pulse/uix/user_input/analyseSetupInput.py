from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QLabel
from os.path import basename
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

class AnalyseSetupInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/analyseSetupInput.ui', self)

        self.currentTab = 0

        self.label_title = self.findChild(QLabel, 'label_title')
        self.label_subtitle = self.findChild(QLabel, 'label_subtitle')

        self.lineEdit_av = self.findChild(QLineEdit, 'lineEdit_av')
        self.lineEdit_bv = self.findChild(QLineEdit, 'lineEdit_bv')
        self.lineEdit_ah = self.findChild(QLineEdit, 'lineEdit_ah')
        self.lineEdit_bh = self.findChild(QLineEdit, 'lineEdit_bh')
        
        self.lineEdit_min = self.findChild(QLineEdit, 'lineEdit_min')
        self.lineEdit_max = self.findChild(QLineEdit, 'lineEdit_max')
        self.lineEdit_step = self.findChild(QLineEdit, 'lineEdit_step')

        self.tabWidget = self.findChild(QTabWidget, 'tabWidget')
        self.tabWidget.currentChanged.connect(self.tabEvent)
        self.currentTab = self.tabWidget.currentIndex()

        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def error(self, msg, title = "Error"):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(msg)
        msg_box.setWindowTitle(title)
        msg_box.exec_()

    def tabEvent(self):
        self.currentTab = self.tabWidget.currentIndex()

    def check(self):
        pass
