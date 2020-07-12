import os
from os.path import basename
import numpy as np
from PyQt5.QtWidgets import QToolButton, QFileDialog, QLineEdit, QDialog, QTreeWidget, QRadioButton, QTreeWidgetItem, QPushButton, QTabWidget, QWidget, QMessageBox
from pulse.utils import error, info_messages, remove_bc_from_file, write_file_inside_project_folder
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from shutil import copyfile

class LoadsInput(QDialog):
    def __init__(self, project, list_node_ids, transform_points, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/loadsInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.project = project
        self.transform_points = transform_points
        self.project_file_path = project.project_file_path
        self.structural_bc_info_path = project.file._nodeStructuralPath

        self.userPath = os.path.expanduser('~')
        self.new_load_path_table = ""
        self.imported_table_name = ""

        self.nodes = project.mesh.nodes
        self.loads = None
        self.nodes_typed = []
        self.imported_table = False

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')

        self.lineEdit_real_Fx = self.findChild(QLineEdit, 'lineEdit_real_Fx')
        self.lineEdit_real_Fy = self.findChild(QLineEdit, 'lineEdit_real_Fy')
        self.lineEdit_real_Fz = self.findChild(QLineEdit, 'lineEdit_real_Fz')
        self.lineEdit_real_Mx = self.findChild(QLineEdit, 'lineEdit_real_Mx')
        self.lineEdit_real_My = self.findChild(QLineEdit, 'lineEdit_real_My')
        self.lineEdit_real_Mz = self.findChild(QLineEdit, 'lineEdit_real_Mz')

        self.lineEdit_imag_Fx = self.findChild(QLineEdit, 'lineEdit_imag_Fx')
        self.lineEdit_imag_Fy = self.findChild(QLineEdit, 'lineEdit_imag_Fy')
        self.lineEdit_imag_Fz = self.findChild(QLineEdit, 'lineEdit_imag_Fz')
        self.lineEdit_imag_Mx = self.findChild(QLineEdit, 'lineEdit_imag_Mx')
        self.lineEdit_imag_My = self.findChild(QLineEdit, 'lineEdit_imag_My')
        self.lineEdit_imag_Mz = self.findChild(QLineEdit, 'lineEdit_imag_Mz')

        self.lineEdit_path_table_Fx = self.findChild(QLineEdit, 'lineEdit_path_table_Fx')
        self.lineEdit_path_table_Fy = self.findChild(QLineEdit, 'lineEdit_path_table_Fy')
        self.lineEdit_path_table_Fz = self.findChild(QLineEdit, 'lineEdit_path_table_Fz')
        self.lineEdit_path_table_Mx = self.findChild(QLineEdit, 'lineEdit_path_table_Mx')
        self.lineEdit_path_table_My = self.findChild(QLineEdit, 'lineEdit_path_table_My')
        self.lineEdit_path_table_Mz = self.findChild(QLineEdit, 'lineEdit_path_table_Mz')

        self.toolButton_load_Fx_table = self.findChild(QToolButton, 'toolButton_load_Fx_table')
        self.toolButton_load_Fy_table = self.findChild(QToolButton, 'toolButton_load_Fy_table')
        self.toolButton_load_Fz_table = self.findChild(QToolButton, 'toolButton_load_Fz_table')
        self.toolButton_load_Mx_table = self.findChild(QToolButton, 'toolButton_load_Mx_table')
        self.toolButton_load_My_table = self.findChild(QToolButton, 'toolButton_load_My_table')
        self.toolButton_load_Mz_table = self.findChild(QToolButton, 'toolButton_load_Mz_table') 

        self.toolButton_load_Fx_table.clicked.connect(self.load_Fx_table)
        self.toolButton_load_Fy_table.clicked.connect(self.load_Fy_table)
        self.toolButton_load_Fz_table.clicked.connect(self.load_Fz_table)
        self.toolButton_load_Mx_table.clicked.connect(self.load_Mx_table)
        self.toolButton_load_My_table.clicked.connect(self.load_My_table)
        self.toolButton_load_Mz_table.clicked.connect(self.load_Mz_table)

        self.Fx_table = None
        self.Fy_table = None
        self.Fz_table = None
        self.Mx_table = None
        self.My_table = None
        self.Mz_table = None

        self.basename_Fx = None
        self.basename_Fy = None
        self.basename_Fz = None
        self.basename_Mx = None
        self.basename_My = None
        self.basename_Mz = None

        self.tabWidget_nodal_loads = self.findChild(QTabWidget, "tabWidget_nodal_loads")
        self.tab_single_values = self.tabWidget_nodal_loads.findChild(QWidget, "tab_single_values")
        self.tab_table = self.tabWidget_nodal_loads.findChild(QWidget, "tab_table")

        self.pushButton_single_value_confirm = self.findChild(QPushButton, 'pushButton_single_value_confirm')
        self.pushButton_single_value_confirm.clicked.connect(self.check_single_values)

        self.pushButton_table_values_confirm = self.findChild(QPushButton, 'pushButton_table_values_confirm')
        self.pushButton_table_values_confirm.clicked.connect(self.check_table_values)

        self.pushButton_remove_bc_confirm = self.findChild(QPushButton, 'pushButton_remove_bc_confirm')
        self.pushButton_remove_bc_confirm.clicked.connect(self.check_remove_bc_from_node)

        self.writeNodes(list_node_ids)
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_nodal_loads.currentIndex()==0:
                self.check_single_values()
            elif self.tabWidget_nodal_loads.currentIndex()==1:
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

    def check_complex_entries(self, lineEdit_real, lineEdit_imag, label):

        self.stop = False
        if lineEdit_real.text() != "":
            try:
                real_F = float(lineEdit_real.text())
            except Exception:
                error("Wrong input for real part of {}!".format(label), "Error")
                self.stop = True
                return
        else:
            real_F = 0

        if lineEdit_imag.text() != "":
            try:
                imag_F = float(lineEdit_imag.text())
            except Exception:
                error("Wrong input for imaginary part of {}!".format(label), "Error")
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

        Fx = self.check_complex_entries(self.lineEdit_real_Fx, self.lineEdit_imag_Fx, "Fx")
        if self.stop:
            return
        Fy = self.check_complex_entries(self.lineEdit_real_Fy, self.lineEdit_imag_Fy, "Fy")
        if self.stop:
            return        
        Fz = self.check_complex_entries(self.lineEdit_real_Fz, self.lineEdit_imag_Fz, "Fz")
        if self.stop:
            return        
        Mx = self.check_complex_entries(self.lineEdit_real_Mx, self.lineEdit_imag_Mx, "Mx")
        if self.stop:
            return        
        My = self.check_complex_entries(self.lineEdit_real_My, self.lineEdit_imag_My, "My")
        if self.stop:
            return        
        Mz = self.check_complex_entries(self.lineEdit_real_Mz, self.lineEdit_imag_Mz, "Mz")
        if self.stop:
            return

        loads = [Fx, Fy, Fz, Mx, My, Mz]
        
        if loads.count(None) != 6:
            self.loads = loads
            self.project.set_loads_by_node(self.nodes_typed, self.loads, False)
            self.transform_points(self.nodes_typed)
            self.close()
        else:    
            error("You must to inform at least one nodal load to confirm the input!", title = " ERROR ")
        
    def load_table(self, lineEdit, text, header):
        
        self.basename = ""
        window_label = 'Choose a table to import the {} nodal load'.format(text)
        self.path_imported_table, _type = QFileDialog.getOpenFileName(None, window_label, self.userPath, 'Dat Files (*.dat)')

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
            imported_file = np.loadtxt(self.path_imported_table, delimiter=",")
        except Exception as e:
            error(str(e))

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

    def load_Fx_table(self):
        header = "Fx || Frequency [Hz], real[N], imaginary[N], absolute[N]"
        self.Fx_table, self.basename_Fx = self.load_table(self.lineEdit_path_table_Fx, "Fx", header)

    def load_Fy_table(self):
        header = "Fy || Frequency [Hz], real[N], imaginary[N], absolute[N]"
        self.Fy_table, self.basename_Fy = self.load_table(self.lineEdit_path_table_Fy, "Fy", header)

    def load_Fz_table(self):
        header = "Fz || Frequency [Hz], real[N], imaginary[N], absolute[N]"
        self.Fz_table, self.basename_Fz = self.load_table(self.lineEdit_path_table_Fz, "Fz", header)

    def load_Mx_table(self):
        header = "Mx || Frequency [Hz], real[N.m], imaginary[N.m], absolute[N.m]"
        self.Mx_table, self.basename_Mx = self.load_table(self.lineEdit_path_table_Mx, "Mx", header)

    def load_My_table(self):
        header = "My || Frequency [Hz], real[N.m], imaginary[N.m], absolute[N.m]"
        self.My_table, self.basename_My = self.load_table(self.lineEdit_path_table_My, "My", header)

    def load_Mz_table(self):
        header = "Mz || Frequency [Hz], real[N.m], imaginary[N.m], absolute[N.m]"
        self.Mz_table, self.basename_Mz = self.load_table(self.lineEdit_path_table_Mz, "Mz", header)

    def check_table_values(self):

        self.check_input_nodes()

        Fx = Fy = Fz = None
        if self.lineEdit_path_table_Fx != "":
            if self.Fx_table is not None:
                Fx = self.Fx_table
        if self.lineEdit_path_table_Fy != "":
            if self.Fy_table is not None:
                Fy = self.Fy_table
        if self.lineEdit_path_table_Fz != "":
            if self.Fz_table is not None:
                Fz = self.Fz_table

        Mx = My = Mz = None
        if self.lineEdit_path_table_Mx != "":
            if self.Mx_table is not None:
                Mx = self.Mx_table
        if self.lineEdit_path_table_My != "":
            if self.My_table is not None:
                My = self.My_table
        if self.lineEdit_path_table_Mz != "":
            if self.Mz_table is not None:
                Mz = self.Mz_table

        self.basenames = [self.basename_Fx, self.basename_Fy, self.basename_Fz, self.basename_Mx, self.basename_My, self.basename_Mz]
        self.loads = [Fx, Fy, Fz, Mx, My, Mz]
        self.project.set_loads_by_node(self.nodes_typed, self.loads, True, table_name=self.basenames)
        self.transform_points(self.nodes_typed)
        self.close()

    def check_remove_bc_from_node(self):

        self.check_input_nodes()
        key_strings = ["forces", "moments"]
        message = "The nodal loads attributed to the {} node(s) have been removed.".format(self.nodes_typed)
        remove_bc_from_file(self.nodes_typed, self.structural_bc_info_path, key_strings, message)
        self.project.mesh.set_structural_load_bc_by_node(self.nodes_typed, [None, None, None, None, None, None])
        self.transform_points(self.nodes_typed)
        self.close()