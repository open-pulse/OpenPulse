from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QPushButton
from pulse.utils import error
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

class DOFInput(QDialog):
    def __init__(self, nodes, list_node_ids, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/dofInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.nodes = nodes
        self.dof = [None, None, None, None, None, None]
        self.nodes_typed = []
        self.remove_prescribed_dofs = False

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')

        self.lineEdit_ux = self.findChild(QLineEdit, 'lineEdit_ux')
        self.lineEdit_uy = self.findChild(QLineEdit, 'lineEdit_uy')
        self.lineEdit_uz = self.findChild(QLineEdit, 'lineEdit_uz')
        self.lineEdit_rx = self.findChild(QLineEdit, 'lineEdit_rx')
        self.lineEdit_ry = self.findChild(QLineEdit, 'lineEdit_ry')
        self.lineEdit_rz = self.findChild(QLineEdit, 'lineEdit_rz')

        self.lineEdit_all = self.findChild(QLineEdit, 'lineEdit_all')

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
            error("Wrong input for Node ID's!", title = "Error Node ID's")
            return
            
        try:
            for node in self.nodes_typed:
                self.nodes[node].external_index
        except:
            message = [" The Node ID input values must be\n major than 1 and less than {}.".format(len(self.nodes))]
            error(message[0], title = " INCORRECT NODE ID INPUT! ")
            return

        if self.lineEdit_all.text() != "":
            try:
                value_dof = float(self.lineEdit_all.text())
                self.dof = [value_dof, value_dof, value_dof, value_dof, value_dof, value_dof]
                self.close()
            except Exception:
                error("Wrong input (All Dofs)!", title = "Error (All Dofs)")
                return
 
        else:
            ux = uy = uz = None
            if self.lineEdit_ux.text() != "":
                try:
                    ux = float(self.lineEdit_ux.text())
                except Exception:
                    error("Wrong input (ux)!", title = "Error")
                    return
            
            if self.lineEdit_uy.text() != "":
                try:
                    uy = float(self.lineEdit_uy.text())
                except Exception:
                    error("Wrong input (uy)!", title = "Error")
                    return

            if self.lineEdit_uz.text() != "":
                try:
                    uz = float(self.lineEdit_uz.text())
                except Exception:
                    error("Wrong input (uz)!", title = "Error")
                    return

            rx = ry = rz = None
            if self.lineEdit_rx.text() != "":
                try:
                    rx = float(self.lineEdit_rx.text())
                except Exception:
                    error("Wrong input (rx)!", title = "Error")
                    return
            
            if self.lineEdit_ry.text() != "":
                try:
                    ry = float(self.lineEdit_ry.text())
                except Exception:
                    error("Wrong input (ry)!", title = "Error")
                    return

            if self.lineEdit_rz.text() != "":
                try:
                    rz = float(self.lineEdit_rz.text())
                except Exception:
                    error("Wrong input (rz)!", title = "Error")
                    return
            
            dofs_inputs = [ux, uy, uz, rx, ry, rz]
                
            if dofs_inputs.count(None) == 6:
                Qclose = QMessageBox.question(
                    self,
                    "WARNING",
                    ("Are you want to delete any prescribed DOF \nassigned to the Node {} ?").format(str(self.nodes_typed)[1:-1]),
                    QMessageBox.Cancel | QMessageBox.Yes, QMessageBox.Yes)
                if Qclose == QMessageBox.Yes:
                    self.remove_prescribed_dofs = True 
                else:
                    self.remove_prescribed_dofs = False
                    return  
                # error(("The values assigned to the DOFs of the Node(s) [{}] have been deleted.").format(str(self.nodes_typed)[1:-1]), title = " WARNING ")
                
            self.dof = dofs_inputs
            self.close()