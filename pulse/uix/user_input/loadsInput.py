from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QTreeWidgetItem, QPushButton
from pulse.utils import error
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

class LoadsInput(QDialog):
    def __init__(self, nodes, list_node_ids, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/loadsInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.nodes = nodes
        self.loads = None
        self.nodes_typed = []

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')

        self.lineEdit_fx = self.findChild(QLineEdit, 'lineEdit_fx')
        self.lineEdit_fy = self.findChild(QLineEdit, 'lineEdit_fy')
        self.lineEdit_fz = self.findChild(QLineEdit, 'lineEdit_fz')
        self.lineEdit_mx = self.findChild(QLineEdit, 'lineEdit_mx')
        self.lineEdit_my = self.findChild(QLineEdit, 'lineEdit_my')
        self.lineEdit_mz = self.findChild(QLineEdit, 'lineEdit_mz')

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check)

        self.writeNodes(list_node_ids)

        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        self.lineEdit_nodeID.setText(text)

    def check(self):
        try:
            tokens = self.lineEdit_nodeID.text().strip().split(',')
            try:
                tokens.remove('')
            except:     
                pass
            self.nodes_typed = list(map(int, tokens))
        except Exception:
            error("Wrong input for Node ID's!", "Error Node ID's")
            return

        try:
            for node in self.nodes_typed:
                self.nodes[node].external_index
        except:
            message = [" The Node ID input values must be\n major than 1 and less than {}.".format(len(self.nodes))]
            error(message[0], title = " INCORRECT NODE ID INPUT! ")
            return

        fx = fy = fz = None
        if self.lineEdit_fx.text() != "":
            try:
                fx = float(self.lineEdit_fx.text())
            except Exception:
                error("Wrong input (fx)!", "Error")
                return
        
        if self.lineEdit_fy.text() != "":
            try:
                fy = float(self.lineEdit_fy.text())
            except Exception:
                error("Wrong input (fy)!", "Error")
                return

        if self.lineEdit_fz.text() != "":
            try:
                fz = float(self.lineEdit_fz.text())
            except Exception:
                error("Wrong input (fz)!", "Error")
                return
        
        mx = my = mz = None
        if self.lineEdit_mx.text() != "":
            try:
                mx = float(self.lineEdit_mx.text())
            except Exception:
                error("Wrong input (mx)!", "Error")
                return
        
        if self.lineEdit_my.text() != "":
            try:
                my = float(self.lineEdit_my.text())
            except Exception:
                error("Wrong input (my)!", "Error")
                return

        if self.lineEdit_mz.text() != "":
            try:
                mz = float(self.lineEdit_mz.text())
            except Exception:
                error("Wrong input (mz)!", "Error")
                return

        loads_inputs = [fx, fy, fz, mx, my, mz]
        
        if loads_inputs.count(None) == 6:
            error("You must to inform at least one nodal load to confirm the input!", title = " ERROR ")
            return
            
        for index, value in enumerate(loads_inputs):
            if value == None:
                loads_inputs[index] = 0.0

        self.loads = loads_inputs
        self.close()