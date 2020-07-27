import os
from os.path import basename
import numpy as np
from PyQt5.QtWidgets import QToolButton, QPushButton, QLineEdit, QDialogButtonBox, QFileDialog, QDialog, QMessageBox, QTabWidget, QWidget, QTreeWidgetItem, QTreeWidget, QSpinBox
from pulse.utils import error
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from shutil import copyfile
from pulse.utils import error, remove_bc_from_file

class SpecificImpedanceInput(QDialog):
    def __init__(self, project, list_node_ids, transform_points, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/specificImpedanceInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.userPath = os.path.expanduser('~')
        self.new_load_path_table = ""

        self.project = project
        self.transform_points = transform_points
        self.project_file_path = project.project_file_path
        self.acoustic_bc_info_path = project.file._node_acoustic_path

        self.nodes = project.mesh.nodes
        self.specific_impedance = None
        self.nodes_typed = []
        self.imported_table = False
        self.remove_specific_impedance = False

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')
        self.lineEdit_specific_impedance_real = self.findChild(QLineEdit, 'lineEdit_specific_impedance_real')
        self.lineEdit_specific_impedance_imag = self.findChild(QLineEdit, 'lineEdit_specific_impedance_imag')
        self.lineEdit_load_table_path = self.findChild(QLineEdit, 'line_load_table_path')

        self.tabWidget_specific_impedance = self.findChild(QTabWidget, "tabWidget_specific_impedance")
        self.tab_single_values = self.tabWidget_specific_impedance.findChild(QWidget, "tab_single_values")
        self.tab_table_values = self.tabWidget_specific_impedance.findChild(QWidget, "tab_table_values")

        self.treeWidget_specific_impedance = self.findChild(QTreeWidget, 'treeWidget_specific_impedance')
        self.treeWidget_specific_impedance.setColumnWidth(1, 20)
        self.treeWidget_specific_impedance.setColumnWidth(2, 80)
        self.treeWidget_specific_impedance.itemClicked.connect(self.on_click_item)
        self.treeWidget_specific_impedance.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.toolButton_load_table = self.findChild(QToolButton, 'toolButton_load_table')
        self.toolButton_load_table.clicked.connect(self.load_specific_impedance_table)

        self.pushButton_single_values_confirm = self.findChild(QPushButton, 'pushButton_single_values_confirm')
        self.pushButton_single_values_confirm.clicked.connect(self.check_single_values)

        self.pushButton_table_values_confirm = self.findChild(QPushButton, 'pushButton_table_values_confirm')
        self.pushButton_table_values_confirm.clicked.connect(self.check_table_values)
        self.lineEdit_skiprows = self.findChild(QSpinBox, 'spinBox')

        self.pushButton_remove_bc_confirm = self.findChild(QPushButton, 'pushButton_remove_bc_confirm')
        self.pushButton_remove_bc_confirm.clicked.connect(self.check_remove_bc_from_node)

        self.pushButton_remove_bc_confirm_2 = self.findChild(QPushButton, 'pushButton_remove_bc_confirm_2')
        self.pushButton_remove_bc_confirm_2.clicked.connect(self.check_remove_bc_from_node)
        
        self.writeNodes(list_node_ids)
        self.load_nodes_info()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_specific_impedance.currentIndex()==0:
                self.check_single_values()
            elif self.tabWidget_specific_impedance.currentIndex()==1:
                self.check_table_values()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        self.lineEdit_nodeID.setText(text)

    def check_input_nodes(self):
        try:
            tokens = self.lineEdit_nodeID.text().strip().split(',')
            try:
                tokens.remove('')
            except:     
                pass
            self.nodes_typed = list(map(int, tokens))

            if self.lineEdit_nodeID.text()=="":
                error("Inform a valid Node ID before to confirm the input!", title = "Error Node ID's")
                return

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

    def check_complex_entries(self, lineEdit_real, lineEdit_imag):

        self.stop = False
        if lineEdit_real.text() != "":
            try:
                real_F = float(lineEdit_real.text())
            except Exception:
                error("Wrong input for real part of specific impedance.", title="Error")
                self.stop = True
                return
        else:
            real_F = 0

        if lineEdit_imag.text() != "":
            try:
                imag_F = float(lineEdit_imag.text())
            except Exception:
                error("Wrong input for imaginary part of specific impedance.", title="Error")
                self.stop = True
                return
        else:
            imag_F = 0
        
        if real_F == 0 and imag_F == 0:
            return None
        else:
            return real_F + 1j*imag_F

    def check_single_values(self):

        self.check_input_nodes()
        specific_impedance = self.check_complex_entries(self.lineEdit_specific_impedance_real, self.lineEdit_specific_impedance_imag)
 
        if self.stop:
            return

        if specific_impedance is not None:
            self.specific_impedance = specific_impedance
            self.project.set_specific_impedance_bc_by_node(self.nodes_typed, self.specific_impedance, False)
            self.transform_points(self.nodes_typed)
            self.close()
        else:    
            error("You must to inform at least one nodal load to confirm the input!", title = " ERROR ")
 
    def load_table(self, lineEdit, header):
        
        self.basename = ""
        window_label = 'Choose a table to import the specific impedance'
        self.path_imported_table, _type = QFileDialog.getOpenFileName(None, window_label, self.userPath, 'Files (*.dat; *.csv)')

        if self.path_imported_table == "":
            return "", ""

        self.basename = os.path.basename(self.path_imported_table)
        lineEdit.setText(self.path_imported_table)
        if self.basename != "":
            self.imported_table_name = self.basename
        
        if "\\" in self.project_file_path:
            self.new_load_path_table = "{}\\{}".format(self.project_file_path, self.basename)
        elif "/" in self.project_file_path:
            self.new_load_path_table = "{}/{}".format(self.project_file_path, self.basename)

        try:
            skiprows = int(self.lineEdit_skiprows.text())                
            imported_file = np.loadtxt(self.path_imported_table, delimiter=",", skiprows=skiprows)
        except Exception as e:
            message = [str(e) + " It is recommended to skip the header rows."] 
            error(message[0], title="ERROR WHILE LOADING TABLE")
            return

        if imported_file.shape[1]<2:
            error("The imported table has insufficient number of columns. The spectrum \ndata must have frequencies, real and imaginary columns.")
            return
    
        try:
            self.imported_values = imported_file[:,1] + 1j*imported_file[:,2]
            if imported_file.shape[1]>2:

                self.frequencies = imported_file[:,0]
                self.f_min = self.frequencies[0]
                self.f_max = self.frequencies[-1]
                self.f_step = self.frequencies[1] - self.frequencies[0] 
                self.imported_table = True

                real_values = np.real(self.imported_values)
                imag_values = np.imag(self.imported_values)
                abs_values = np.imag(self.imported_values)
                data = np.array([self.frequencies, real_values, imag_values, abs_values]).T
                np.savetxt(self.new_load_path_table, data, delimiter=",", header=header)

        except Exception as e:
            error(str(e))

        return self.imported_values, self.basename

    def load_specific_impedance_table(self):
        header = "specific impedance || Frequency [Hz], real[Pa], imaginary[Pa], absolute[Pa]"
        self.specific_impedance, self.basename_specific_impedance = self.load_table(self.lineEdit_load_table_path, header)
    
    def check_table_values(self):

        self.check_input_nodes()

        if self.lineEdit_load_table_path != "":
            if self.specific_impedance is not None:
                self.project.set_specific_impedance_bc_by_node(self.nodes_typed, self.specific_impedance, True, table_name=self.basename_specific_impedance)
                self.transform_points(self.nodes_typed)
        self.close()

    def text_label(self, value):
        text = ""
        if isinstance(value, complex):
            value_label = str(value)
        elif isinstance(value, np.ndarray):
            value_label = 'Table'
        text = "{}".format(value_label)
        return text

    def load_nodes_info(self):
        for node in self.project.mesh.nodes_with_specific_impedance:
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(node.specific_impedance))])
            self.treeWidget_specific_impedance.addTopLevelItem(new)

    def on_click_item(self, item):
        self.lineEdit_nodeID.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_nodeID.setText(item.text(0))
        self.check_remove_bc_from_node()

    def check_remove_bc_from_node(self):

        self.check_input_nodes()
        key_strings = ["specific impedance"]
        message = "The specific impedance attributed to the {} node(s) have been removed.".format(self.nodes_typed)
        remove_bc_from_file(self.nodes_typed, self.acoustic_bc_info_path, key_strings, message)
        self.project.mesh.set_specific_impedance_bc_by_node(self.nodes_typed, None)
        self.transform_points(self.nodes_typed)
        self.close()