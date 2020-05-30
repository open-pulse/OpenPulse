from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QLabel, QPushButton
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

class PlotStructuralModeShapeInput(QDialog):
    def __init__(self, frequencies, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/plotStructuralModeShapeInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)


        self.frequencies = frequencies
        self.mode_index = None

        self.lineEdit = self.findChild(QLineEdit, 'lineEdit')
        self.treeWidget = self.findChild(QTreeWidget, 'treeWidget')
        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.pushButton.clicked.connect(self.button)

        self.treeWidget.itemClicked.connect(self.on_click_item)
        self.treeWidget.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.load()

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

    def isFloat(self, value):
        try:
            float(value)
            return True
        except:
            return False

    def isInt(self, value):
        try:
            int(value)
            return True
        except:
            return False

    def check(self):
        if self.lineEdit.text() == "":
            self.error("Select a frequency or enter a valid mode number.")
            return
        else:
            if float(self.lineEdit.text()) in self.frequencies:
                frequency = float(self.lineEdit.text())
                self.mode_index = self.frequencies.index(frequency)
            elif not self.isInt(self.lineEdit.text()):
                self.error("Please, enter a valid mode number or natural frequency!")
                return
            elif int(self.lineEdit.text())>0 and int(self.lineEdit.text())<=len(self.frequencies):
                    self.mode_index = int(self.lineEdit.text())-1
            else:
                self.error("Please, enter a valid mode number or natural frequency!")
                return

        self.close()

    def load(self):
        for frequency in self.frequencies:
            new = QTreeWidgetItem([str(frequency)])
            self.treeWidget.addTopLevelItem(new)

    def on_click_item(self, item):
        self.lineEdit.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit.setText(item.text(0))
        self.check()

    def button(self):
        self.check()