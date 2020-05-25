from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QPushButton
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

class VolumeVelocityInput(QDialog):
    def __init__(self, list_node_ids, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/volumevelocityInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.volume_velocity = None
        self.nodes = []

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')
        self.lineEdit_volume_velocity = self.findChild(QLineEdit, 'lineEdit_volume_velocity')

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check)

        self.writeNodes(list_node_ids)

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

    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        self.lineEdit_nodeID.setText(text)

    def isInteger(self, value):
        try:
            int(value)
            return True
        except:
            return False

    def isFloat(self, value):
        try:
            float(value)
            return True
        except:
            return False

    def check(self):
        try:
            tokens = self.lineEdit_nodeID.text().strip().split(',')
            try:
                tokens.remove('')
            except:
                pass
            self.nodes = list(map(int, tokens))
        except Exception:
            self.error("Wrong input for Node ID's!", "Error Node ID's")
            return

        volume_velocity = None
        if self.lineEdit_volume_velocity.text() != "":
            if self.isFloat(self.lineEdit_volume_velocity.text()):
                volume_velocity = float(self.lineEdit_volume_velocity.text())
            else:
                self.error("Wrong input (volume_velocity)!", "Error")
                return
        
        self.volume_velocity = volume_velocity
        self.close()