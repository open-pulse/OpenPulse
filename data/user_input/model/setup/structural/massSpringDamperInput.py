import os
from os.path import basename
import numpy as np
from PyQt5.QtWidgets import QToolButton, QFileDialog, QLineEdit, QDialog, QTreeWidget, QRadioButton, QTreeWidgetItem, QPushButton, QTabWidget, QWidget, QMessageBox, QCheckBox, QTreeWidget
from pulse.utils import remove_bc_from_file, get_new_path, create_new_folder
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from shutil import copyfile

from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput

class MassSpringDamperInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Model/Setup/Structural/addMassSpringDamperInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)
        self.transform_points = self.opv.transformPoints

        self.project = project
        self.preprocessor = project.preprocessor
        self.before_run = project.get_model_checks()
        
        self.structural_bc_info_path = project.file._node_structural_path
        self.structural_folder_path = self.project.file._structural_imported_data_folder_path
        self.lumped_elements_tables_folder_path = get_new_path(self.structural_folder_path, "lumped_elements_tables")

        self.userPath = os.path.expanduser('~')
        self.new_load_path_table = ""
        self.imported_table_name = ""

        self.nodes = self.preprocessor.nodes
        self.loads = None
        self.nodes_typed = []
        self.imported_table = False

        self.lumped_masses = None
        self.lumped_stiffness = None
        self.lumped_dampings = None
        self.lumped_masses_inputs_from_node = False
        self.lumped_stiffness_inputs_from_node = False
        self.lumped_dampings_inputs_from_node = False
        self.stop = False

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')

        self.lineEdit_Mx = self.findChild(QLineEdit, 'lineEdit_Mx')
        self.lineEdit_My = self.findChild(QLineEdit, 'lineEdit_My')
        self.lineEdit_Mz = self.findChild(QLineEdit, 'lineEdit_Mz')
        self.lineEdit_Jx = self.findChild(QLineEdit, 'lineEdit_Jx')
        self.lineEdit_Jy = self.findChild(QLineEdit, 'lineEdit_Jy')
        self.lineEdit_Jz = self.findChild(QLineEdit, 'lineEdit_Jz')

        self.list_lineEdit_constant_values_lumped_masses = [self.lineEdit_Mx,
                                                            self.lineEdit_My,
                                                            self.lineEdit_Mz,
                                                            self.lineEdit_Jx,
                                                            self.lineEdit_Jy,
                                                            self.lineEdit_Jz]

        self.lineEdit_Kx = self.findChild(QLineEdit, 'lineEdit_Kx')
        self.lineEdit_Ky = self.findChild(QLineEdit, 'lineEdit_Ky')
        self.lineEdit_Kz = self.findChild(QLineEdit, 'lineEdit_Kz')
        self.lineEdit_Krx = self.findChild(QLineEdit, 'lineEdit_Krx')
        self.lineEdit_Kry = self.findChild(QLineEdit, 'lineEdit_Kry')
        self.lineEdit_Krz = self.findChild(QLineEdit, 'lineEdit_Krz')

        self.list_lineEdit_constant_values_lumped_stiffness = [ self.lineEdit_Kx,
                                                                self.lineEdit_Ky,
                                                                self.lineEdit_Kz,
                                                                self.lineEdit_Krx,
                                                                self.lineEdit_Kry,
                                                                self.lineEdit_Krz ]

        self.lineEdit_Cx = self.findChild(QLineEdit, 'lineEdit_Cx')
        self.lineEdit_Cy = self.findChild(QLineEdit, 'lineEdit_Cy')
        self.lineEdit_Cz = self.findChild(QLineEdit, 'lineEdit_Cz')
        self.lineEdit_Crx = self.findChild(QLineEdit, 'lineEdit_Crx')
        self.lineEdit_Cry = self.findChild(QLineEdit, 'lineEdit_Cry')
        self.lineEdit_Crz = self.findChild(QLineEdit, 'lineEdit_Crz')

        self.list_lineEdit_constant_values_lumped_dampings = [  self.lineEdit_Cx,
                                                                self.lineEdit_Cy,
                                                                self.lineEdit_Cz,
                                                                self.lineEdit_Crx,
                                                                self.lineEdit_Cry,
                                                                self.lineEdit_Crz  ]

        self.lineEdit_path_table_Mx = self.findChild(QLineEdit, 'lineEdit_path_table_Mx')
        self.lineEdit_path_table_My = self.findChild(QLineEdit, 'lineEdit_path_table_My')
        self.lineEdit_path_table_Mz = self.findChild(QLineEdit, 'lineEdit_path_table_Mz')
        self.lineEdit_path_table_Jx = self.findChild(QLineEdit, 'lineEdit_path_table_Jx')
        self.lineEdit_path_table_Jy = self.findChild(QLineEdit, 'lineEdit_path_table_Jy')
        self.lineEdit_path_table_Jz = self.findChild(QLineEdit, 'lineEdit_path_table_Jz')

        self.list_lineEdit_table_values_lumped_masses = [   self.lineEdit_path_table_Mx,
                                                            self.lineEdit_path_table_My,
                                                            self.lineEdit_path_table_Mz,
                                                            self.lineEdit_path_table_Jx,
                                                            self.lineEdit_path_table_Jy,
                                                            self.lineEdit_path_table_Jz  ]

        self.toolButton_load_Mx_table = self.findChild(QToolButton, 'toolButton_load_Mx_table')
        self.toolButton_load_My_table = self.findChild(QToolButton, 'toolButton_load_My_table')
        self.toolButton_load_Mz_table = self.findChild(QToolButton, 'toolButton_load_Mz_table')
        self.toolButton_load_Jx_table = self.findChild(QToolButton, 'toolButton_load_Jx_table')
        self.toolButton_load_Jy_table = self.findChild(QToolButton, 'toolButton_load_Jy_table')
        self.toolButton_load_Jz_table = self.findChild(QToolButton, 'toolButton_load_Jz_table') 

        self.toolButton_load_Mx_table.clicked.connect(self.load_Mx_table)
        self.toolButton_load_My_table.clicked.connect(self.load_My_table)
        self.toolButton_load_Mz_table.clicked.connect(self.load_Mz_table)
        self.toolButton_load_Jx_table.clicked.connect(self.load_Jx_table)
        self.toolButton_load_Jy_table.clicked.connect(self.load_Jy_table)
        self.toolButton_load_Jz_table.clicked.connect(self.load_Jz_table)

        self.Mx_table = None
        self.My_table = None
        self.Mz_table = None
        self.Jx_table = None
        self.Jy_table = None
        self.Jz_table = None

        self.basename_Mx = None
        self.basename_My = None
        self.basename_Mz = None
        self.basename_Jx = None
        self.basename_Jy = None
        self.basename_Jz = None

        self.lineEdit_path_table_Kx = self.findChild(QLineEdit, 'lineEdit_path_table_Kx')
        self.lineEdit_path_table_Ky = self.findChild(QLineEdit, 'lineEdit_path_table_Ky')
        self.lineEdit_path_table_Kz = self.findChild(QLineEdit, 'lineEdit_path_table_Kz')
        self.lineEdit_path_table_Krx = self.findChild(QLineEdit, 'lineEdit_path_table_Krx')
        self.lineEdit_path_table_Kry = self.findChild(QLineEdit, 'lineEdit_path_table_Kry')
        self.lineEdit_path_table_Krz = self.findChild(QLineEdit, 'lineEdit_path_table_Krz')

        self.list_lineEdit_table_values_lumped_stiffness = [self.lineEdit_path_table_Kx,
                                                            self.lineEdit_path_table_Ky,
                                                            self.lineEdit_path_table_Kz,
                                                            self.lineEdit_path_table_Krx,
                                                            self.lineEdit_path_table_Kry,
                                                            self.lineEdit_path_table_Krz]

        self.toolButton_load_Kx_table = self.findChild(QToolButton, 'toolButton_load_Kx_table')
        self.toolButton_load_Ky_table = self.findChild(QToolButton, 'toolButton_load_Ky_table')
        self.toolButton_load_Kz_table = self.findChild(QToolButton, 'toolButton_load_Kz_table')
        self.toolButton_load_Krx_table = self.findChild(QToolButton, 'toolButton_load_Krx_table')
        self.toolButton_load_Kry_table = self.findChild(QToolButton, 'toolButton_load_Kry_table')
        self.toolButton_load_Krz_table = self.findChild(QToolButton, 'toolButton_load_Krz_table') 

        self.toolButton_load_Kx_table.clicked.connect(self.load_Kx_table)
        self.toolButton_load_Ky_table.clicked.connect(self.load_Ky_table)
        self.toolButton_load_Kz_table.clicked.connect(self.load_Kz_table)
        self.toolButton_load_Krx_table.clicked.connect(self.load_Krx_table)
        self.toolButton_load_Kry_table.clicked.connect(self.load_Kry_table)
        self.toolButton_load_Krz_table.clicked.connect(self.load_Krz_table)

        self.Kx_table = None
        self.Ky_table = None
        self.Kz_table = None
        self.Krx_table = None
        self.Kry_table = None
        self.Krz_table = None

        self.basename_Kx = None
        self.basename_Ky = None
        self.basename_Kz = None
        self.basename_Krx = None
        self.basename_Kry = None
        self.basename_Krz = None

        self.lineEdit_path_table_Cx = self.findChild(QLineEdit, 'lineEdit_path_table_Cx')
        self.lineEdit_path_table_Cy = self.findChild(QLineEdit, 'lineEdit_path_table_Cy')
        self.lineEdit_path_table_Cz = self.findChild(QLineEdit, 'lineEdit_path_table_Cz')
        self.lineEdit_path_table_Crx = self.findChild(QLineEdit, 'lineEdit_path_table_Crx')
        self.lineEdit_path_table_Cry = self.findChild(QLineEdit, 'lineEdit_path_table_Cry')
        self.lineEdit_path_table_Crz = self.findChild(QLineEdit, 'lineEdit_path_table_Crz')

        self.list_lineEdit_table_values_lumped_dampings = [ self.lineEdit_path_table_Cx,
                                                            self.lineEdit_path_table_Cy,
                                                            self.lineEdit_path_table_Cz,
                                                            self.lineEdit_path_table_Crx,
                                                            self.lineEdit_path_table_Cry,
                                                            self.lineEdit_path_table_Crz ]

        self.toolButton_load_Cx_table = self.findChild(QToolButton, 'toolButton_load_Cx_table')
        self.toolButton_load_Cy_table = self.findChild(QToolButton, 'toolButton_load_Cy_table')
        self.toolButton_load_Cz_table = self.findChild(QToolButton, 'toolButton_load_Cz_table')
        self.toolButton_load_Crx_table = self.findChild(QToolButton, 'toolButton_load_Crx_table')
        self.toolButton_load_Cry_table = self.findChild(QToolButton, 'toolButton_load_Cry_table')
        self.toolButton_load_Crz_table = self.findChild(QToolButton, 'toolButton_load_Crz_table') 

        self.toolButton_load_Cx_table.clicked.connect(self.load_Cx_table)
        self.toolButton_load_Cy_table.clicked.connect(self.load_Cy_table)
        self.toolButton_load_Cz_table.clicked.connect(self.load_Cz_table)
        self.toolButton_load_Crx_table.clicked.connect(self.load_Crx_table)
        self.toolButton_load_Cry_table.clicked.connect(self.load_Cry_table)
        self.toolButton_load_Crz_table.clicked.connect(self.load_Crz_table)

        self.Cx_table = None
        self.Cy_table = None
        self.Cz_table = None
        self.Crx_table = None
        self.Cry_table = None
        self.Crz_table = None

        self.basename_Cx = None
        self.basename_Cy = None
        self.basename_Cz = None
        self.basename_Crx = None
        self.basename_Cry = None
        self.basename_Crz = None

        self.flag_lumped_masses = False
        self.flag_lumped_stiffness = False
        self.flag_lumped_dampings = False

        self.checkBox_remove_mass = self.findChild(QCheckBox, 'checkBox_remove_mass')
        self.checkBox_remove_spring = self.findChild(QCheckBox, 'checkBox_remove_spring')
        self.checkBox_remove_damper = self.findChild(QCheckBox, 'checkBox_remove_damper')

        self.tabWidget_external_elements = self.findChild(QTabWidget, "tabWidget_external_elements")
        self.tab_constant_values = self.tabWidget_external_elements.findChild(QWidget, "tab_constant_values")
        self.tab_table_values = self.tabWidget_external_elements.findChild(QWidget, "tab_table_values")

        self.tabWidget_constant_values = self.findChild(QTabWidget, "tabWidget_constant_values")
        self.tab_mass = self.tabWidget_constant_values.findChild(QWidget, "tab_mass")
        self.tab_spring = self.tabWidget_constant_values.findChild(QWidget, "tab_spring")
        self.tab_damper = self.tabWidget_constant_values.findChild(QWidget, "tab_damper")

        self.tabWidget_table_values = self.findChild(QTabWidget, "tabWidget_table_values")
        self.tab_mass_table = self.tabWidget_table_values.findChild(QWidget, "tab_mass_table")
        self.tab_spring_table = self.tabWidget_table_values.findChild(QWidget, "tab_spring_table")
        self.tab_damper_table = self.tabWidget_table_values.findChild(QWidget, "tab_damper_table")   

        self.tabWidget_remove = self.findChild(QTabWidget, "tabWidget_remove")
        self.tab_multiple_remove = self.tabWidget_remove.findChild(QWidget, "tab_multiple_remove")
        self.tab_spring_remove = self.tabWidget_remove.findChild(QWidget, "tab_spring_remove")
        self.tab_mass_remove = self.tabWidget_remove.findChild(QWidget, "tab_mass_remove")
        self.tab_damper_remove = self.tabWidget_remove.findChild(QWidget, "tab_damper_remove")

        self.treeWidget_springs = self.findChild(QTreeWidget, 'treeWidget_springs')
        self.treeWidget_springs.setColumnWidth(0, 70)
        # self.treeWidget_springs.setColumnWidth(1, 80)
        self.treeWidget_springs.itemClicked.connect(self.on_click_item)
        self.treeWidget_springs.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.treeWidget_dampers = self.findChild(QTreeWidget, 'treeWidget_dampers')
        self.treeWidget_dampers.setColumnWidth(0, 70)
        # self.treeWidget_dampers.setColumnWidth(1, 80)
        self.treeWidget_dampers.itemClicked.connect(self.on_click_item)
        self.treeWidget_dampers.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.treeWidget_masses = self.findChild(QTreeWidget, 'treeWidget_masses')
        self.treeWidget_masses.setColumnWidth(0, 70)
        # self.treeWidget_masses.setColumnWidth(1, 80)
        self.treeWidget_masses.itemClicked.connect(self.on_click_item)
        self.treeWidget_masses.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.pushButton_constant_value_confirm = self.findChild(QPushButton, 'pushButton_constant_value_confirm')
        self.pushButton_constant_value_confirm.clicked.connect(self.check_all_constant_values_inputs)

        self.pushButton_table_values_confirm = self.findChild(QPushButton, 'pushButton_table_values_confirm')
        self.pushButton_table_values_confirm.clicked.connect(self.check_all_table_values_inputs)

        self.pushButton_remove_bc_confirm = self.findChild(QPushButton, 'pushButton_remove_bc_confirm')
        self.pushButton_remove_bc_confirm.clicked.connect(self.check_remove_bc_from_node)

        self.pushButton_remove_spring_confirm = self.findChild(QPushButton, 'pushButton_remove_spring_confirm')
        self.pushButton_remove_spring_confirm.clicked.connect(self.check_remove_bc_from_node)

        self.pushButton_remove_mass_confirm = self.findChild(QPushButton, 'pushButton_remove_mass_confirm')
        self.pushButton_remove_mass_confirm.clicked.connect(self.check_remove_bc_from_node)

        self.pushButton_remove_damper_confirm = self.findChild(QPushButton, 'pushButton_remove_damper_confirm')
        self.pushButton_remove_damper_confirm.clicked.connect(self.check_remove_bc_from_node)

        self.update()
        self.load_nodes_info()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_external_elements.currentIndex()==0:
                self.check_all_constant_values_inputs()
            elif self.tabWidget_external_elements.currentIndex()==1:
                self.check_all_table_values_inputs()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        self.lineEdit_nodeID.setText(text[:-2])

    def check_entries(self, lineEdit, label):

        self.stop = False
        if lineEdit.text() != "":
            try:
                value = float(lineEdit.text())
            except Exception:
                window_title ="ERROR"
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for real part of {label}."
                PrintMessageInput([title, message, window_title])
                self.stop = True
                return
        else:
            value = 0

        if value == 0:
            return None
        else:
            return value

    def check_constant_values_lumped_masses(self):
        
        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stopstop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stopstop:
            return

        Mx = self.check_entries(self.lineEdit_Mx, "Mx")
        if self.stop:
            return
        My = self.check_entries(self.lineEdit_My, "My")
        if self.stop:
            return        
        Mz = self.check_entries(self.lineEdit_Mz, "Mz")
        if self.stop:
            return        
        Jx = self.check_entries(self.lineEdit_Jx, "Jx")
        if self.stop:
            return        
        Jy = self.check_entries(self.lineEdit_Jy, "Jy")
        if self.stop:
            return        
        Jz = self.check_entries(self.lineEdit_Jz, "Jz")
        if self.stop:
            return

        lumped_masses = [Mx, My, Mz, Jx, Jy, Jz]
        
        if lumped_masses.count(None) != 6:
            self.flag_lumped_masses = True
            self.lumped_masses = lumped_masses
            table_names = [None, None, None, None, None, None]
            data = [lumped_masses, table_names]
            self.project.add_lumped_masses_by_node(self.nodes_typed, data, False)
        
    def check_constant_values_lumped_stiffness(self):

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stopstop:
            return

        Kx = self.check_entries(self.lineEdit_Kx, "Kx")
        if self.stop:
            return
        Ky = self.check_entries(self.lineEdit_Ky, "Ky")
        if self.stop:
            return        
        Kz = self.check_entries(self.lineEdit_Kz, "Kz")
        if self.stop:
            return        
        Krx = self.check_entries(self.lineEdit_Krx, "Krx")
        if self.stop:
            return        
        Kry = self.check_entries(self.lineEdit_Kry, "Kry")
        if self.stop:
            return        
        Krz = self.check_entries(self.lineEdit_Krz, "Krz")
        if self.stop:
            return

        lumped_stiffness = [Kx, Ky, Kz, Krx, Kry, Krz]
        
        if lumped_stiffness.count(None) != 6:
            self.flag_lumped_stiffness = True
            self.lumped_stiffness = lumped_stiffness
            table_names = [None, None, None, None, None, None]
            data = [lumped_stiffness, table_names]
            self.project.add_lumped_stiffness_by_node(self.nodes_typed, data, False)
 
    def check_constant_values_lumped_dampings(self):

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stopstop:
            return

        Cx = self.check_entries(self.lineEdit_Cx, "Cx")
        if self.stop:
            return
        Cy = self.check_entries(self.lineEdit_Cy, "Cy")
        if self.stop:
            return        
        Cz = self.check_entries(self.lineEdit_Cz, "Cz")
        if self.stop:
            return        
        Crx = self.check_entries(self.lineEdit_Crx, "Crx")
        if self.stop:
            return        
        Cry = self.check_entries(self.lineEdit_Cry, "Cry")
        if self.stop:
            return        
        Crz = self.check_entries(self.lineEdit_Crz, "Crz")
        if self.stop:
            return

        lumped_dampings = [Cx, Cy, Cz, Crx, Cry, Crz]
         
        if lumped_dampings.count(None) != 6:
            self.flag_lumped_dampings = True
            self.lumped_dampings = lumped_dampings
            table_names = [None, None, None, None, None, None]
            data = [lumped_dampings, table_names]
            self.project.add_lumped_dampings_by_node(self.nodes_typed, data, False)

    def check_all_constant_values_inputs(self):

        self.check_constant_values_lumped_masses()
        if self.stop:
            return

        self.check_constant_values_lumped_stiffness()
        if self.stop:
            return

        self.check_constant_values_lumped_dampings()
        if self.stop:
            return

        if not (self.flag_lumped_masses or self.flag_lumped_stiffness or self.flag_lumped_dampings):
            window_title ="ERROR"
            title = "Additional inputs required"
            message = "You must to inform at least one external element to confirm the input!"
            PrintMessageInput([title, message, window_title]) 
            return
        
        if self.lumped_masses is not None:
            print("[Set Mass] - defined at node(s) {}".format(self.nodes_typed))
        if self.lumped_stiffness is not None:
            print("[Set Spring] - defined at node(s) {}".format(self.nodes_typed))
        if self.lumped_dampings is not None:
            print("[Set Damper] - defined at node(s) {}".format(self.nodes_typed))
        
        self.transform_points(self.nodes_typed)
        self.close()

    def load_table(self, lineEdit, text, header, direct_load=False):
        
        self.project.file.temp_table_name = None
        
        if direct_load:
            self.path_imported_table = lineEdit.text()
        else:
            self.basename = ""
            window_label = 'Choose a table to import the {} nodal load'.format(text)
            self.path_imported_table, _type = QFileDialog.getOpenFileName(None, window_label, self.userPath, 'Files (*.csv; *.dat; *.txt)')
            lineEdit.setText(self.path_imported_table)

        if self.path_imported_table == "":
            return "", ""
        
        self.basename = os.path.basename(self.path_imported_table)
        if self.basename != "":
            self.imported_table_name = self.basename

        self.project.create_folders_structural("lumped_elements_tables")
        self.new_load_path_table = get_new_path(self.lumped_elements_tables_folder_path, self.basename)

        try:                
            imported_file = np.loadtxt(self.path_imported_table, delimiter=",")
        except Exception as log_error:
            window_title ="ERROR"
            title = "Error reached while loading table"
            message = f" {str(log_error)} \n\nIt is recommended to skip the header rows."
            PrintMessageInput([title, message, window_title])
            return

        if imported_file.shape[1]<2:
            window_title ="ERROR"
            title = "Error reached while loading table"
            message = "The imported table has insufficient number of columns. The spectrum \n"
            message += "data must have frequencies, real and imaginary columns."
            PrintMessageInput([title, message, window_title])
            return
    
        try:
            self.imported_values = imported_file[:,1]
            if imported_file.shape[1]>=2:

                self.frequencies = imported_file[:,0]
                self.f_min = self.frequencies[0]
                self.f_max = self.frequencies[-1]
                self.f_step = self.frequencies[1] - self.frequencies[0] 
                self.imported_table = True
               
                _values = self.imported_values
                data = np.array([self.frequencies, _values, np.zeros_like(self.frequencies)]).T
                np.savetxt(self.new_load_path_table, data, delimiter=",", header=header)

        except Exception as log_error:
            window_title ="ERROR"
            title = "Error reached while loading table"
            message = f" {str(log_error)} \n\nIt is recommended to skip the header rows."
            PrintMessageInput([title, message, window_title])

        return self.imported_values, self.basename

    def load_Mx_table(self):
        header = "Mx || Frequency [Hz], value[kg]"
        self.Mx_table, self.basename_Mx = self.load_table(self.lineEdit_path_table_Mx, "Mx", header)

    def load_My_table(self):
        header = "My || Frequency [Hz], value[kg]"
        self.My_table, self.basename_My = self.load_table(self.lineEdit_path_table_My, "My", header)

    def load_Mz_table(self):
        header = "Mz || Frequency [Hz], value[kg]"
        self.Mz_table, self.basename_Mz = self.load_table(self.lineEdit_path_table_Mz, "Mz", header)
    
    def load_Jx_table(self):
        header = "Jx || Frequency [Hz], value[kg.m²]"
        self.Jx_table, self.basename_Jx = self.load_table(self.lineEdit_path_table_Jx, "Fx", header)
    
    def load_Jy_table(self):
        header = "Jy || Frequency [Hz], value[kg.m²]"
        self.Jy_table, self.basename_Jy = self.load_table(self.lineEdit_path_table_Jy, "Jy", header)

    def load_Jz_table(self):
        header = "Jz || Frequency [Hz], value[kg.m²]"
        self.Jz_table, self.basename_Jz = self.load_table(self.lineEdit_path_table_Jz, "Jz", header)

    def load_Kx_table(self):
        header = "Kx || Frequency [Hz], value[N/m]"
        self.Kx_table, self.basename_Kx = self.load_table(self.lineEdit_path_table_Kx, "Kx", header)

    def load_Ky_table(self):
        header = "Ky || Frequency [Hz], value[N/m]"
        self.Ky_table, self.basename_Ky = self.load_table(self.lineEdit_path_table_Ky, "Ky", header)

    def load_Kz_table(self):
        header = "Kz || Frequency [Hz], value[N/m]"
        self.Kz_table, self.basename_Kz = self.load_table(self.lineEdit_path_table_Kz, "Kz", header)

    def load_Krx_table(self):
        header = "Krx || Frequency [Hz], value[N.m/rad]"
        self.Krx_table, self.basename_Krx = self.load_table(self.lineEdit_path_table_Krx, "Krx", header)

    def load_Kry_table(self):
        header = "Kry || Frequency [Hz], value[N.m/rad]"
        self.Kry_table, self.basename_Kry = self.load_table(self.lineEdit_path_table_Kry, "Kry", header)

    def load_Krz_table(self):
        header = "Krz || Frequency [Hz], value[N.m/rad]"
        self.Krz_table, self.basename_Krz = self.load_table(self.lineEdit_path_table_Krz, "Krz", header)

    def load_Cx_table(self):
        header = "Cx || Frequency [Hz], value[N.s/m]"
        self.Cx_table, self.basename_Cx = self.load_table(self.lineEdit_path_table_Cx, "Cx", header)

    def load_Cy_table(self):
        header = "Cy || Frequency [Hz], value[N.s/m]"
        self.Cy_table, self.basename_Cy = self.load_table(self.lineEdit_path_table_Cy, "Cy", header)

    def load_Cz_table(self):
        header = "Cz || Frequency [Hz], value[N.s/m]"
        self.Cz_table, self.basename_Cz = self.load_table(self.lineEdit_path_table_Cz, "Cz", header)

    def load_Crx_table(self):
        header = "Crx || Frequency [Hz], value[N.m/rad/s]"
        self.Crx_table, self.basename_Crx = self.load_table(self.lineEdit_path_table_Crx, "Crx", header)

    def load_Cry_table(self):
        header = "Cry || Frequency [Hz], value[N.m/rad/s]"
        self.Cry_table, self.basename_Cry = self.load_table(self.lineEdit_path_table_Cry, "Cry", header)

    def load_Crz_table(self):
        header = "Crz || Frequency [Hz], value[N.m/rad/s]"
        self.Crz_table, self.basename_Crz = self.load_table(self.lineEdit_path_table_Crz, "Crz", header)
      
    def check_table_values_lumped_masses(self):

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stop:
            return

        Mx = My = Mz = None
        if self.lineEdit_path_table_Mx.text() != "":
            if self.Mx_table is None:
                header = "Mx || Frequency [Hz], value[kg]"
                Mx, self.basename_Mx = self.load_table(self.lineEdit_path_table_Mx, "Mx", header, direct_load=True)
            else:
                Mx = self.Mx_table
        if self.lineEdit_path_table_My.text() != "":
            if self.My_table is None:
                header = "My || Frequency [Hz], value[kg]"
                My, self.basename_My = self.load_table(self.lineEdit_path_table_My, "My", header, direct_load=True)
            else:
                My = self.My_table
        if self.lineEdit_path_table_Mz.text() != "":
            if self.Mz_table is None:
                header = "Mz || Frequency [Hz], value[kg]"
                Mz, self.basename_Mz = self.load_table(self.lineEdit_path_table_Mz, "Mz", header, direct_load=True)
            else:
                Mz = self.Mz_table

        Jx = Jy = Jz = None
        if self.lineEdit_path_table_Jx.text() != "":
            if self.Jx_table is None:
                header = "Jx || Frequency [Hz], value[kg.m²]"
                Jx, self.basename_Jx = self.load_table(self.lineEdit_path_table_Jx, "Jx", header, direct_load=True)
            else:
                Jx = self.Jx_table
        if self.lineEdit_path_table_Jy.text() != "":
            if self.Jy_table is None:
                header = "Jy || Frequency [Hz], value[kg.m²]"
                Jy, self.basename_Jy = self.load_table(self.lineEdit_path_table_Jy, "Jy", header, direct_load=True)
            else:
                Jy = self.Jy_table
        if self.lineEdit_path_table_Jz.text() != "":
            if self.Jz_table is None:
                header = "Jz || Frequency [Hz], value[kg.m²]"
                Jz, self.basename_Jz = self.load_table(self.lineEdit_path_table_Jz, "Jz", header, direct_load=True)
            else:
                Jz = self.Jz_table
        
        lumped_masses = [Mx, My, Mz, Jx, Jy, Jz]

        if sum([1 if bc is not None else 0 for bc in lumped_masses]) != 0:
            self.flag_lumped_masses = True
            self.basenames = [self.basename_Mx, self.basename_My, self.basename_Mz, self.basename_Jx, self.basename_Jy, self.basename_Jz]
            self.lumped_masses = lumped_masses
            data = [lumped_masses, self.basenames]
            self.project.add_lumped_masses_by_node(self.nodes_typed, data, True)

    def check_table_values_lumped_stiffness(self):

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stop:
            return

        Kx = Ky = Kz = None
        if self.lineEdit_path_table_Kx.text() != "":
            if self.Kx_table is None:
                header = "Kx || Frequency [Hz], value[N/m]"
                Kx, self.basename_Kx = self.load_table(self.lineEdit_path_table_Kx, "Kx", header, direct_load=True)
            else:
                Kx = self.Kx_table
        if self.lineEdit_path_table_Ky.text() != "":
            if self.Ky_table is None:
                header = "Ky || Frequency [Hz], value[N/m]"
                Ky, self.basename_Ky = self.load_table(self.lineEdit_path_table_Ky, "Ky", header, direct_load=True)
            else:
                Ky = self.Ky_table
        if self.lineEdit_path_table_Kz.text() != "":
            if self.Kz_table is None:
                header = "Kz || Frequency [Hz], value[N/m]"
                Kz, self.basename_Kz = self.load_table(self.lineEdit_path_table_Kz, "Kz", header, direct_load=True)
            else:
                Kz = self.Kz_table

        Krx = Kry = Krz = None
        if self.lineEdit_path_table_Krx.text() != "":
            if self.Krx_table is None:
                header = "Krx || Frequency [Hz], value[N.m/rad]"
                Krx, self.basename_Krx = self.load_table(self.lineEdit_path_table_Krx, "Krx", header, direct_load=True)
            else:
                Krx = self.Krx_table
        if self.lineEdit_path_table_Kry.text() != "":
            if self.Kry_table is None:
                header = "Kry || Frequency [Hz], value[N.m/rad]"
                Kry, self.basename_Kry = self.load_table(self.lineEdit_path_table_Kry, "Kry", header, direct_load=True)
            else:
                Kry = self.Kry_table
        if self.lineEdit_path_table_Krz.text() != "":
            if self.Krz_table is None:
                header = "Krz || Frequency [Hz], value[N.m/rad]"
                Krz, self.basename_Krz = self.load_table(self.lineEdit_path_table_Krz, "Krz", header, direct_load=True)
            else:
                Krz = self.Krz_table
        
        lumped_stiffness = [Kx, Ky, Kz, Krx, Kry, Krz]

        if sum([1 if bc is not None else 0 for bc in lumped_stiffness]) != 0:
            self.flag_lumped_stiffness = True
            self.basenames = [self.basename_Kx, self.basename_Ky, self.basename_Kz, self.basename_Krx, self.basename_Kry, self.basename_Krz]
            self.lumped_stiffness = lumped_stiffness
            data = [lumped_stiffness, self.basenames]
            self.project.add_lumped_stiffness_by_node(self.nodes_typed, data, True)

    def check_table_values_lumped_dampings(self):

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stop:
            return

        Cx = Cy = Cz = None
        if self.lineEdit_path_table_Cx.text() != "":
            if self.Cx_table is None:
                header = "Cx || Frequency [Hz], value[N.s/m]"
                Cx, self.basename_Cx = self.load_table(self.lineEdit_path_table_Cx, "Cx", header, direct_load=True)
            else:
                Cx = self.Cx_table
        if self.lineEdit_path_table_Cy.text() != "":
            if self.Cy_table is None:
                header = "Cy || Frequency [Hz], value[N.s/m]"
                Cy, self.basename_Cy = self.load_table(self.lineEdit_path_table_Cy, "Cy", header, direct_load=True)
            else:
                Cy = self.Cy_table
        if self.lineEdit_path_table_Cz.text() != "":
            if self.Cz_table is None:
                header = "Cz || Frequency [Hz], value[N.s/m]"
                Cz, self.basename_Cz = self.load_table(self.lineEdit_path_table_Cz, "Cz", header, direct_load=True)
            else:
                Cz = self.Cz_table

        Crx = Cry = Crz = None
        if self.lineEdit_path_table_Crx.text() != "":
            if self.Crx_table is None:
                header = "Crx || Frequency [Hz], value[N.m/rad/s]"
                Crx, self.basename_Crx = self.load_table(self.lineEdit_path_table_Crx, "Crx", header, direct_load=True)
            else:
                Crx = self.Crx_table
        if self.lineEdit_path_table_Cry.text() != "":
            if self.Cry_table is None:
                header = "Cry || Frequency [Hz], value[N.m/rad/s]"
                Cry, self.basename_Cry = self.load_table(self.lineEdit_path_table_Cry, "Cry", header, direct_load=True)
            else:
                Cry = self.Cry_table
        if self.lineEdit_path_table_Crz.text() != "":
            if self.Crz_table is None:
                header = "Crz || Frequency [Hz], value[N.m/rad/s]"
                Crz, self.basename_Crz = self.load_table(self.lineEdit_path_table_Crz, "Crz", header, direct_load=True)
            else:
                Crz = self.Crz_table
            
        lumped_dampings = [Cx, Cy, Cz, Crx, Cry, Crz]

        if sum([1 if bc is not None else 0 for bc in lumped_dampings]) != 0:
            self.flag_lumped_dampings = True
            self.basenames = [self.basename_Cx, self.basename_Cy, self.basename_Cz, self.basename_Crx, self.basename_Cry, self.basename_Crz]
            self.lumped_dampings = lumped_dampings
            data = [lumped_dampings, self.basenames]
            self.project.add_lumped_dampings_by_node(self.nodes_typed, data, True)

    def check_all_table_values_inputs(self):

        self.check_table_values_lumped_masses()
        if self.stop:
            return

        self.check_table_values_lumped_stiffness()
        if self.stop:
            return

        self.check_table_values_lumped_dampings()
        if self.stop:
            return

        if not (self.flag_lumped_masses or self.flag_lumped_stiffness or self.flag_lumped_dampings):
            window_title ="ERROR"
            title = "Additional inputs required"
            message = "You must to inform at least one external element to confirm the input!"
            PrintMessageInput([title, message, window_title]) 
            return

        if self.lumped_masses is not None:
            print("[Set Mass] - defined at node(s) {}".format(self.nodes_typed))
        if self.lumped_stiffness is not None:
            print("[Set Spring] - defined at node(s) {}".format(self.nodes_typed))
        if self.lumped_dampings is not None:
            print("[Set Damper] - defined at node(s) {}".format(self.nodes_typed))

        self.transform_points(self.nodes_typed)
        self.close()      

    def check_remove_bc_from_node(self):

        list_reset = [None, None, None, None, None, None]
        data = [list_reset, list_reset]

        self.remove_mass = self.checkBox_remove_mass.isChecked()
        self.remove_spring = self.checkBox_remove_spring.isChecked()
        self.remove_damper = self.checkBox_remove_damper.isChecked()

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stop:
            return

        if (self.remove_mass and self.tabWidget_remove.currentIndex()==0) or self.tabWidget_remove.currentIndex()==2:    
            key_strings = ["masses", "moments of inertia"]
            message = "The masses and moments of inertia attributed to the \n\n{}\n\n node(s) have been removed.".format(self.nodes_typed)
            remove_bc_from_file(self.nodes_typed, self.structural_bc_info_path, key_strings, message)
            self.remove_masses_table_files()
            self.project.preprocessor.add_mass_to_node(self.nodes_typed, data)
   
        if (self.remove_spring and self.tabWidget_remove.currentIndex()==0) or self.tabWidget_remove.currentIndex()==1:   
            key_strings = ["spring stiffness", "torsional spring stiffness"]
            message = "The stiffness (translational and tosional) attributed to the \n\n{}\n\n node(s) have been removed.".format(self.nodes_typed)
            remove_bc_from_file(self.nodes_typed, self.structural_bc_info_path, key_strings, message)
            self.remove_stiffness_table_files()
            self.project.preprocessor.add_spring_to_node(self.nodes_typed, data)
            
        if (self.remove_damper and self.tabWidget_remove.currentIndex()==0) or self.tabWidget_remove.currentIndex()==3: 
            key_strings = ["damping coefficients", "torsional damping coefficients"]
            message = "The dampings (translational and tosional) attributed to the \n\n{}\n\n node(s) have been removed.".format(self.nodes_typed)
            remove_bc_from_file(self.nodes_typed, self.structural_bc_info_path, key_strings, message)
            self.remove_damping_table_files()
            self.project.preprocessor.add_damper_to_node(self.nodes_typed, data)

        self.load_nodes_info()
        self.transform_points(self.nodes_typed)
        # self.close()
    
    def remove_masses_table_files(self):
        for node_typed in self.nodes_typed:
            node = self.preprocessor.nodes[node_typed]
            if node.loaded_table_for_lumped_masses:
                list_table_names = node.lumped_masses_table_names
                self.confirm_table_file_removal(list_table_names, "Spring stiffness")

    def remove_stiffness_table_files(self):
        for node_typed in self.nodes_typed:
            node = self.preprocessor.nodes[node_typed]
            if node.loaded_table_for_lumped_stiffness:
                list_table_names = node.lumped_stiffness_table_names
                self.confirm_table_file_removal(list_table_names, "Masses/Moments of inertia")
    
    def remove_damping_table_files(self):
        for node_typed in self.nodes_typed:
            node = self.preprocessor.nodes[node_typed]
            if node.loaded_table_for_lumped_dampings:
                list_table_names = node.lumped_dampings_table_names
                self.confirm_table_file_removal(list_table_names, "Damping coefficients")    

    def confirm_table_file_removal(self, list_table_names, label):
        _list_table_names = []
        for table_name in list_table_names:
            if table_name is not None:
                if table_name not in _list_table_names:
                    _list_table_names.append(table_name)

        title = f"{label} - removal of imported table files"
        message = "Do you want to remove the following unused imported table \nfrom the project folder?\n\n"
        for _table_name in _list_table_names:
            message += f"{_table_name}\n"
        message += "\n\nPress the Continue button to proceed with removal or press Cancel or \nClose buttons to abort the current operation."
        read = CallDoubleConfirmationInput(title, message)

        if read._doNotRun:
            return

        if read._continue:
            for _table_name in _list_table_names:
                self.project.remove_structural_table_files_from_folder(_table_name, folder_name="lumped_elements_tables")
            # self.project.remove_structural_empty_folders(folder_name="lumped_elements_tables")   


    def text_label(self, mask, load_labels):
        
        text = ""
        temp = load_labels[mask]

        if list(mask).count(True) == 6:
            text = "[{}, {}, {}, {}, {}, {}]".format(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5])
        elif list(mask).count(True) == 5:
            text = "[{}, {}, {}, {}, {}]".format(temp[0], temp[1], temp[2], temp[3], temp[4])
        elif list(mask).count(True) == 4:
            text = "[{}, {}, {}, {}]".format(temp[0], temp[1], temp[2], temp[3])
        elif list(mask).count(True) == 3:
            text = "[{}, {}, {}]".format(temp[0], temp[1], temp[2])
        elif list(mask).count(True) == 2:
            text = "[{}, {}]".format(temp[0], temp[1])
        elif list(mask).count(True) == 1:
            text = "[{}]".format(temp[0])
        return text

    def load_nodes_info(self):

        self.treeWidget_springs.clear()
        load_labels = np.array(['k_x','k_y','k_z','k_rx','k_ry','k_rz'])        
        for node in self.project.preprocessor.nodes_connected_to_springs:
            lumped_stiffness_mask = [False if bc is None else True for bc in node.lumped_stiffness]
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(lumped_stiffness_mask, load_labels))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_springs.addTopLevelItem(new)

        self.treeWidget_dampers.clear()
        load_labels = np.array(['c_x','c_y','c_z','c_rx','c_ry','c_rz'])
        for node in self.project.preprocessor.nodes_connected_to_dampers:
            lumped_dampings_mask = [False if bc is None else True for bc in node.lumped_dampings]
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(lumped_dampings_mask, load_labels))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_dampers.addTopLevelItem(new)

        self.treeWidget_masses.clear()
        load_labels = np.array(['m_x','m_y','m_z','Jx','Jy','Jz'])
        for node in self.project.preprocessor.nodes_with_masses:
            lumped_masses_mask = [False if bc is None else True for bc in node.lumped_masses]
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(lumped_masses_mask, load_labels))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_masses.addTopLevelItem(new)

    def on_click_item(self, item):
        self.lineEdit_nodeID.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_nodeID.setText(item.text(0))
        self.check_remove_bc_from_node()

    def reset_input_fields_masses(self, force_reset=False):
        if self.lumped_masses_inputs_from_node or force_reset:
            for lineEdit_constant_masses in self.list_lineEdit_constant_values_lumped_masses:    
                lineEdit_constant_masses.setText("")
            for lineEdit_table_masses in self.list_lineEdit_table_values_lumped_masses:
                lineEdit_table_masses.setText("")
            self.lumped_masses_inputs_from_node = False

    def reset_input_fields_stiffness(self, force_reset=False):
        if self.lumped_stiffness_inputs_from_node or force_reset:
            for lineEdit_constant_stiffness in self.list_lineEdit_constant_values_lumped_stiffness:    
                lineEdit_constant_stiffness.setText("")
            for lineEdit_table_stiffness in self.list_lineEdit_table_values_lumped_stiffness:
                lineEdit_table_stiffness.setText("")
            self.lumped_stiffness_inputs_from_node = False

    def reset_input_fields_dampings(self, force_reset=False):
        if self.lumped_dampings_inputs_from_node or force_reset:
            for lineEdit_constant_dampings in self.list_lineEdit_constant_values_lumped_dampings:    
                lineEdit_constant_dampings.setText("")
            for lineEdit_table_dampings in self.list_lineEdit_table_values_lumped_dampings:
                lineEdit_table_dampings.setText("")
            self.lumped_dampings_inputs_from_node = False

    def update(self):
        list_picked_nodes = self.opv.getListPickedPoints()
        if list_picked_nodes != []:
            picked_node = list_picked_nodes[0]
            node = self.preprocessor.nodes[picked_node]
            self.writeNodes(self.opv.getListPickedPoints())

            #Lumped masses/inertia
            if node.there_are_lumped_masses:
                self.reset_input_fields_masses(force_reset=True)
                if node.loaded_table_for_lumped_masses:
                    table_names = node.lumped_masses_table_names
                    self.tabWidget_external_elements.setCurrentWidget(self.tab_table_values)
                    self.tabWidget_table_values.setCurrentWidget(self.tab_mass_table)
                    for index, lineEdit_table in enumerate(self.list_lineEdit_table_values_lumped_masses):
                        if table_names[index] is not None:
                            table_name = get_new_path(self.lumped_elements_tables_folder_path, table_names[index])
                            lineEdit_table.setText(table_name)
                else:
                    lumped_masses = node.lumped_masses
                    self.tabWidget_external_elements.setCurrentWidget(self.tab_constant_values)
                    self.tabWidget_constant_values.setCurrentWidget(self.tab_mass)
                    for index, lineEdit_constant in enumerate(self.list_lineEdit_constant_values_lumped_masses):
                        if lumped_masses[index] is not None:
                            lineEdit_constant.setText(str(lumped_masses[index]))
                self.lumped_masses_inputs_from_node = True
            else:
                self.reset_input_fields_masses()

            #Lumped stiffness
            if node.there_are_lumped_stiffness:
                self.reset_input_fields_stiffness(force_reset=True)
                if node.loaded_table_for_lumped_stiffness:
                    table_names = node.lumped_stiffness_table_names
                    self.tabWidget_external_elements.setCurrentWidget(self.tab_table_values)
                    self.tabWidget_table_values.setCurrentWidget(self.tab_spring_table)
                    for index, lineEdit_table in enumerate(self.list_lineEdit_table_values_lumped_stiffness):
                        if table_names[index] is not None:
                            table_name = get_new_path(self.lumped_elements_tables_folder_path, table_names[index])
                            lineEdit_table.setText(table_name)
                else:
                    lumped_stiffness = node.lumped_stiffness
                    self.tabWidget_external_elements.setCurrentWidget(self.tab_constant_values)
                    self.tabWidget_constant_values.setCurrentWidget(self.tab_spring)
                    for index, lineEdit_constant in enumerate(self.list_lineEdit_constant_values_lumped_stiffness):
                        if lumped_stiffness[index] is not None:
                            lineEdit_constant.setText(str(lumped_stiffness[index]))
                self.lumped_stiffness_inputs_from_node = True
            else:
                self.reset_input_fields_stiffness()

            #Lumped dampings
            if node.there_are_lumped_dampings:
                self.reset_input_fields_dampings(force_reset=True)
                if node.loaded_table_for_lumped_dampings:
                    table_names = node.lumped_dampings_table_names
                    self.tabWidget_external_elements.setCurrentWidget(self.tab_table_values)
                    self.tabWidget_table_values.setCurrentWidget(self.tab_damper_table)
                    for index, lineEdit_table in enumerate(self.list_lineEdit_table_values_lumped_dampings):
                        if table_names[index] is not None:
                            table_name = get_new_path(self.lumped_elements_tables_folder_path, table_names[index])
                            lineEdit_table.setText(table_name)
                else:
                    lumped_dampings = node.lumped_dampings
                    self.tabWidget_external_elements.setCurrentWidget(self.tab_constant_values)
                    self.tabWidget_constant_values.setCurrentWidget(self.tab_damper)
                    for index, lineEdit_constant in enumerate(self.list_lineEdit_constant_values_lumped_dampings):
                        if lumped_dampings[index] is not None:
                            lineEdit_constant.setText(str(lumped_dampings[index]))
                self.lumped_dampings_inputs_from_node = True
            else:
                self.reset_input_fields_dampings()
            