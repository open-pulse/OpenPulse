import os
from os.path import basename
import numpy as np
from PyQt5.QtWidgets import QToolButton, QPushButton, QLineEdit, QDialogButtonBox, QFileDialog, QDialog, QMessageBox, QTabWidget
from pulse.utils import error
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from shutil import copyfile
from pulse.utils import error

class SpecificImpedanceInput(QDialog):
    def __init__(self, nodes, list_node_ids, project_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/specificimpedanceInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.userPath = os.path.expanduser('~')
        self.project_path = project_path
        self.new_load_path_table = ""

        self.nodes = nodes
        self.specific_impedance = None
        self.nodes_typed = []
        self.remove_specific_impedance = False
        self.flag_real = False
        self.flag_imag = False

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')
        self.lineEdit_specific_impedance_real = self.findChild(QLineEdit, 'lineEdit_specific_impedance_real')
        self.lineEdit_specific_impedance_imag = self.findChild(QLineEdit, 'lineEdit_specific_impedance_imag')
        self.lineEdit_load_table_path = self.findChild(QLineEdit, 'line_load_table_path')

        self.toolButton_load_table = self.findChild(QToolButton, 'toolButton_load_table')
        self.toolButton_load_table.clicked.connect(self.load_table)

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check)

        self.writeNodes(list_node_ids)
        self.exec_()

    def load_table(self):
        
        self.path_imported_table, _type = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'Dat Files (*.dat)')

        if self.path_imported_table == "":
            return

        self.specific_impedance_table_name = os.path.basename(self.path_imported_table)
        self.lineEdit_load_table_path.setText(self.path_imported_table)
        
        if "\\" in self.project_path:
            self.new_load_path_table = "{}\\{}".format(self.project_path, self.specific_impedance_table_name)
        elif "/" in self.project_path:
            self.new_load_path_table = "{}/{}".format(self.project_path, self.specific_impedance_table_name)

        copyfile(self.path_imported_table, self.new_load_path_table)
        loaded_file = np.loadtxt(self.new_load_path_table, delimiter=",")

        self.specific_impedance = loaded_file[:,1] + 1j*loaded_file[:,2]
        if loaded_file.shape[1]>2:
            self.frequencies = loaded_file[:,0]
            self.f_min = self.frequencies[0]
            self.f_max = self.frequencies[-1]
            self.df = self.frequencies[1] - self.frequencies[0] 
    
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

            if self.lineEdit_nodeID.text()=="":
                error("Inform a valid Node ID before confirm th input!", title = "Error Node ID's")
                return
                
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
        
        if self.specific_impedance is not None:
            try:
                isinstance(self.specific_impedance, np.ndarray)
            except Exception:
                error("Invalid Specific Impedance table!")
                return
        else:

            specific_impedance = None
            specific_impedance_real = 0
            specific_impedance_imag = 0
            
            if self.lineEdit_specific_impedance_real.text() != "":
                try:
                    specific_impedance_real = float(self.lineEdit_specific_impedance_real.text())
                    self.flag_real = True
                except Exception:
                    error("Wrong input for the Specific Impedance!", title = " ERROR ")
                    return

            if self.lineEdit_specific_impedance_imag.text() != "":
                try:
                    specific_impedance_imag = float(self.lineEdit_specific_impedance_imag.text())
                    self.flag_imag = True
                except Exception:
                    error("Wrong input for the Specific Impedance!", title = " ERROR ")
                    return

            if self.flag_real or self.flag_imag:
                specific_impedance = specific_impedance_real + 1j*specific_impedance_imag
            
            if self.lineEdit_specific_impedance_real.text() == "" and self.lineEdit_specific_impedance_imag.text() == "":
                Qclose = QMessageBox.question(
                    self,
                    "WARNING",
                    ("Are you want to delete any Specific Impedance \nassigned to the Node {} ?").format(str(self.nodes_typed)[1:-1]),
                    QMessageBox.Cancel | QMessageBox.Yes, QMessageBox.Yes)
                if Qclose == QMessageBox.Yes:
                    self.remove_specific_impedance = True 
                else:
                    self.remove_specific_impedance = False
                    return          
                # error(("The pressure(s) assigned to the Node(s): {} has been deleted.").format(str(self.nodes_typed)[1:-1]), title = " WARNING ")

            self.specific_impedance = specific_impedance
        self.close()