from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem
from os.path import basename
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

class DOFInput(QDialog):
    def __init__(self, list_node_ids, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/dofInput.ui', self)

        self.dof = None
        self.nodes = []

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')

        self.lineEdit_ux = self.findChild(QLineEdit, 'lineEdit_ux')
        self.lineEdit_uy = self.findChild(QLineEdit, 'lineEdit_uy')
        self.lineEdit_uz = self.findChild(QLineEdit, 'lineEdit_uz')
        self.lineEdit_rx = self.findChild(QLineEdit, 'lineEdit_rx')
        self.lineEdit_ry = self.findChild(QLineEdit, 'lineEdit_ry')
        self.lineEdit_rz = self.findChild(QLineEdit, 'lineEdit_rz')

        self.lineEdit_all = self.findChild(QLineEdit, 'lineEdit_all')

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

        if self.lineEdit_all.text() != "":
            if self.isInteger(self.lineEdit_all.text()):
                dof = int(self.lineEdit_all.text())
                self.dof = [dof, dof, dof, dof, dof, dof]
                self.close()
            else:
                self.error("Wrong input (All Dofs)!", "Error (All Dofs)")
                return
        else:
            ux = uy = uz = None
            if self.lineEdit_ux.text() != "":
                if self.isInteger(self.lineEdit_ux.text()):
                    ux = int(self.lineEdit_ux.text())
                else:
                    self.error("Wrong input (ux)!", "Error")
                    return
            
            if self.lineEdit_uy.text() != "":
                if self.isInteger(self.lineEdit_uy.text()):
                    uy = int(self.lineEdit_uy.text())
                else:
                    self.error("Wrong input (uy)!", "Error")
                    return

            if self.lineEdit_uz.text() != "":
                if self.isInteger(self.lineEdit_uz.text()):
                    uz = int(self.lineEdit_uz.text())
                else:
                    self.error("Wrong input (uz)!", "Error")
                    return

            
            rx = ry = rz = None
            if self.lineEdit_rx.text() != "":
                if self.isInteger(self.lineEdit_rx.text()):
                    rx = int(self.lineEdit_rx.text())
                else:
                    self.error("Wrong input (rx)!", "Error")
                    return
            
            if self.lineEdit_ry.text() != "":
                if self.isInteger(self.lineEdit_ry.text()):
                    ry = int(self.lineEdit_ry.text())
                else:
                    self.error("Wrong input (ry)!", "Error")
                    return

            if self.lineEdit_rz.text() != "":
                if self.isInteger(self.lineEdit_rz.text()):
                    rz = int(self.lineEdit_rz.text())
                else:
                    self.error("Wrong input (rz)!", "Error")
                    return

            self.dof = [ux, uy, uz, rx, ry, rz]
            self.close()