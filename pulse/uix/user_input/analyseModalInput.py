from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QComboBox, QPushButton
from os.path import basename
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

class AnalyseModalInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/analyseModalStructuralInput.ui', self)

        self.modes = 0

        self.lineEdit = self.findChild(QLineEdit, 'lineEdit')

        self.pushButton_2 = self.findChild(QPushButton, 'pushButton_2')
        self.pushButton_2.clicked.connect(self.button_clicked)

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

    def isInteger(self, value):
        try:
            int(value)
            return True
        except:
            return False

    def check(self):
        if self.lineEdit.text() == "":
            self.error("Insert a value")
            return
        else:
            if self.isInteger(self.lineEdit.text()):
                self.modes = int(self.lineEdit.text())
            else:
                self.error("Value error")
                return
        self.close()

    def button_clicked(self):
        self.check()