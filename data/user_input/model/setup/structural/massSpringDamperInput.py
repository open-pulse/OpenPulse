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
        self.lumped_elements_files_folder_path = get_new_path(self.structural_folder_path, "lumped_elements_files")

        self.userPath = os.path.expanduser('~')
        self.new_load_path_table = ""
        self.imported_table_name = ""

        self.nodes = self.preprocessor.nodes
        self.loads = None
        self.nodes_typed = []

        self.lumped_masses = None
        self.lumped_stiffness = None
        self.lumped_dampings = None
        self.list_Nones = [None, None, None, None, None, None]
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

        self.Mx_filename = None
        self.My_filename = None
        self.Mz_filename = None
        self.Jx_filename = None
        self.Jy_filename = None
        self.Jz_filename = None

        self.Mx_basename = None
        self.My_basename = None
        self.Mz_basename = None
        self.Jx_basename = None
        self.Jy_basename = None
        self.Jz_basename = None

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

        self.Kx_filename = None
        self.Ky_filename = None
        self.Kz_filename = None
        self.Krx_filename = None
        self.Kry_filename = None
        self.Krz_filename = None

        self.Kx_basename = None
        self.Ky_basename = None
        self.Kz_basename = None
        self.Krx_basename = None
        self.Kry_basename = None
        self.Krz_basename = None

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

        self.Cx_filename = None
        self.Cy_filename = None
        self.Cz_filename = None
        self.Crx_filename = None
        self.Cry_filename = None
        self.Crz_filename = None

        self.Cx_basename = None
        self.Cy_basename = None
        self.Cz_basename = None
        self.Crx_basename = None
        self.Cry_basename = None
        self.Crz_basename = None

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
            self.remove_masses_table_files()
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
            self.remove_stiffness_table_files()
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
            self.remove_damping_table_files()
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
            message = "You must inform at least one external element\n"
            message += "before confirming the input!"
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

    def load_table(self, lineEdit, _label, direct_load=False):
        window_title = "ERROR"
        title = "Error reached while loading table"
        try:
            if direct_load:
                self.path_imported_table = lineEdit.text()
            else:
                window_label = 'Choose a table to import the {} nodal load'.format(_label)
                self.path_imported_table, _ = QFileDialog.getOpenFileName(None, window_label, self.userPath, 'Files (*.csv; *.dat; *.txt)')

            if self.path_imported_table == "":
                return None, None
            
            self.imported_filename = os.path.basename(self.path_imported_table)
            lineEdit.setText(self.path_imported_table)                       
            imported_file = np.loadtxt(self.path_imported_table, delimiter=",")
        
            if imported_file.shape[1]<2:
                message = "The imported table has insufficient number of columns. The imported \n"
                message += "data must have two columns of values."
                PrintMessageInput([title, message, window_title])
                lineEdit.setFocus()
                return None, None

            if imported_file.shape[1]>=2:
                self.imported_values = imported_file[:,1]
                self.frequencies = imported_file[:,0]
                self.f_min = self.frequencies[0]
                self.f_max = self.frequencies[-1]
                self.f_step = self.frequencies[1] - self.frequencies[0]

                if self.project.change_project_frequency_setup(self.imported_filename, list(self.frequencies)):
                    self.stop = True
                    return None, None
                else:
                    self.project.set_frequencies(self.frequencies, self.f_min, self.f_max, self.f_step)
                    self.stop = False
            
                return self.imported_values, self.imported_filename

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([title, message, window_title])
            lineEdit.setFocus()
            return None, None

    def load_Mx_table(self):
        self.Mx_table, self.Mx_filename = self.load_table(self.lineEdit_path_table_Mx, "Mx")
        if self.stop:
            self.stop = False
            self.Mx_table, self.Mx_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Mx)

    def load_My_table(self):
        self.My_table, self.My_filename = self.load_table(self.lineEdit_path_table_My, "My")
        if self.stop:
            self.stop = False
            self.My_table, self.My_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_My)

    def load_Mz_table(self):
        self.Mz_table, self.Mz_filename = self.load_table(self.lineEdit_path_table_Mz, "Mz")
        if self.stop:
            self.stop = False
            self.Mz_table, self.Mz_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Mz)
    
    def load_Jx_table(self):
        self.Jx_table, self.Jx_filename = self.load_table(self.lineEdit_path_table_Jx, "Jx")
        if self.stop:
            self.stop = False
            self.Jx_table, self.Jx_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Jx)

    def load_Jy_table(self):
        self.Jy_table, self.Jy_filename = self.load_table(self.lineEdit_path_table_Jy, "Jy")
        if self.stop:
            self.stop = False
            self.Jy_table, self.Jy_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Jy)

    def load_Jz_table(self):
        self.Jz_table, self.Jz_filename = self.load_table(self.lineEdit_path_table_Jz, "Jz")
        if self.stop:
            self.stop = False
            self.Jz_table, self.Jz_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Jz)

    def load_Kx_table(self):
        self.Kx_table, self.Kx_filename = self.load_table(self.lineEdit_path_table_Kx, "Kx")
        if self.stop:
            self.stop = False
            self.Kx_table, self.Kx_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Kx)

    def load_Ky_table(self):
        self.Ky_table, self.Ky_filename = self.load_table(self.lineEdit_path_table_Ky, "Ky")
        if self.stop:
            self.stop = False
            self.Ky_table, self.Ky_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Ky)

    def load_Kz_table(self):
        self.Kz_table, self.Kz_filename = self.load_table(self.lineEdit_path_table_Kz, "Kz")
        if self.stop:
            self.stop = False
            self.Kz_table, self.Kz_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Kz)

    def load_Krx_table(self):
        self.Krx_table, self.Krx_filename = self.load_table(self.lineEdit_path_table_Krx, "Krx")
        if self.stop:
            self.stop = False
            self.Krx_table, self.Krx_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Krx)

    def load_Kry_table(self):
        self.Kry_table, self.Kry_filename = self.load_table(self.lineEdit_path_table_Kry, "Kry")
        if self.stop:
            self.stop = False
            self.Kry_table, self.Kry_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Kry)

    def load_Krz_table(self):
        self.Krz_table, self.Krz_filename = self.load_table(self.lineEdit_path_table_Krz, "Krz")
        if self.stop:
            self.stop = False
            self.Krz_table, self.Krz_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Krz)

    def load_Cx_table(self):
        self.Cx_table, self.Cx_filename = self.load_table(self.lineEdit_path_table_Cx, "Cx")
        if self.stop:
            self.stop = False
            self.Cx_table, self.Cx_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Cx)

    def load_Cy_table(self):
        self.Cy_table, self.Cy_filename = self.load_table(self.lineEdit_path_table_Cy, "Cy")
        if self.stop:
            self.stop = False
            self.Cy_table, self.Cy_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Cy)

    def load_Cz_table(self):
        self.Cz_table, self.Cz_filename = self.load_table(self.lineEdit_path_table_Cz, "Cz")
        if self.stop:
            self.stop = False
            self.Cz_table, self.Cz_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Cz)

    def load_Crx_table(self):
        self.Crx_table, self.Crx_filename = self.load_table(self.lineEdit_path_table_Crx, "Crx")
        if self.stop:
            self.stop = False
            self.Crx_table, self.Crx_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Crx)

    def load_Cry_table(self):
        self.Cry_table, self.Cry_filename = self.load_table(self.lineEdit_path_table_Cry, "Cry")
        if self.stop:
            self.stop = False
            self.Cry_table, self.Cry_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Cry)

    def load_Crz_table(self):
        self.Crz_table, self.Crz_filename = self.load_table(self.lineEdit_path_table_Crz, "Crz")
        if self.stop:
            self.stop = False
            self.Crz_table, self.Crz_filename = None, None
            self.lineEdit_reset(self.lineEdit_path_table_Crz)
      
    def lineEdit_reset(self, lineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()

    def save_tables_files(self, node_id, values, filename, _label, unit_label):

        real_values = np.real(values)
        data = np.array([self.frequencies, real_values]).T
        self.project.create_folders_structural("lumped_elements_files")

        if _label in ["Kx", "Ky", "Kz", "Krx", "Kry", "Krz"]:
            header = f"OpenPulse - imported table for {_label} lumped stiffness @ node {node_id}\n "
            lumped_label = "lumped_stiffness"

        if _label in ["Cx", "Cy", "Cz", "Crx", "Cry", "Crz"]:
            header = f"OpenPulse - imported table for {_label} lumped damping @ node {node_id}\n "
            lumped_label = "lumped_damping"

        if _label in ["Mx", "My", "Mz"]:
            header = f"OpenPulse - imported table for {_label} lumped mass @ node {node_id}\n "
            lumped_label = "lumped_mass"

        if _label in ["Jx", "Jy", "Jz"]:
            header = f"OpenPulse - imported table for {_label} lumped moment of inertia @ node {node_id}\n "
            lumped_label = "lumped_moment_of_inertia"

        header += f"\nSource filename: {filename}\n"
        header += f"\nFrequency [Hz], values[{unit_label}]"

        basename = f"{lumped_label}_{_label}_node_{node_id}.dat"
    
        new_path_table = get_new_path(self.lumped_elements_files_folder_path, basename)
        np.savetxt(new_path_table, data, delimiter=",", header=header)

        return values, basename

    def check_table_values_lumped_masses(self):

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stop:
            return
       
        for node_id in self.nodes_typed:
            Mx = My = Mz = None
            if self.lineEdit_path_table_Mx.text() != "":
                if self.Mx_table is None:
                    if self.Mx_filename is None:
                        self.Mx_table, self.Mx_filename = self.load_table(self.lineEdit_path_table_Mx, "Mx", direct_load=True)
                if self.Mx_table is not None:
                    Mx, self.Mx_basename = self.save_tables_files(node_id, self.Mx_table, self.Mx_filename, "Mx", "N")
            
            if self.lineEdit_path_table_My.text() != "":
                if self.My_table is None:
                    if self.My_filename is None:
                        self.My_table, self.My_filename = self.load_table(self.lineEdit_path_table_My, "My", direct_load=True)
                if self.My_table is not None:
                    My, self.My_basename = self.save_tables_files(node_id, self.My_table, self.My_filename, "My", "N")
            
            if self.lineEdit_path_table_Mz.text() != "":
                if self.Mz_table is None:
                    if self.Mz_filename is None:
                        self.Mz_table, self.Mz_filename = self.load_table(self.lineEdit_path_table_Mz, "Mz", direct_load=True)
                if self.Mz_table is not None:
                    Mz, self.Mz_basename = self.save_tables_files(node_id, self.Mz_table, self.Mz_filename, "Mz", "N")
            
            Jx = Jy = Jz = None
            if self.lineEdit_path_table_Jx.text() != "":
                if self.Jx_table is None:
                    if self.Jx_filename is None:
                        self.Jx_table, self.Jx_filename = self.load_table(self.lineEdit_path_table_Jx, "Jx", direct_load=True)
                if self.Jx_table is not None:
                    Jx, self.Jx_basename = self.save_tables_files(node_id, self.Jx_table, self.Jx_filename, "Jx", "kg.m²")
                    
            if self.lineEdit_path_table_Jy.text() != "":
                if self.Jy_table is None:
                    if self.Jy_filename is None:
                        self.Jy_table, self.Jy_filename = self.load_table(self.lineEdit_path_table_Jy, "Jy", direct_load=True)
                if self.Jy_table is not None:
                    Jy, self.Jy_basename = self.save_tables_files(node_id, self.Jy_table, self.Jy_filename, "Jy", "kg.m²")
            
            if self.lineEdit_path_table_Jz.text() != "":
                if self.Jz_table is None:
                    if self.Jz_filename is None:
                        self.Jz_table, self.Jz_filename = self.load_table(self.lineEdit_path_table_Jz, "Jz", direct_load=True)
                if self.Jz_table is not None:
                    Jz, self.Jz_basename = self.save_tables_files(node_id, self.Jz_table, self.Jz_filename, "Jz", "kg.m²")

            lumped_masses = [Mx, My, Mz, Jx, Jy, Jz]

            if sum([0 if bc is None else 1 for bc in lumped_masses]) != 0:

                self.flag_lumped_masses = True
                self.basenames = [  self.Mx_basename, self.My_basename, self.Mz_basename, 
                                    self.Jx_basename, self.Jy_basename, self.Jz_basename  ]

                self.lumped_masses = lumped_masses
                data = [lumped_masses, self.basenames]

                node = self.preprocessor.nodes[node_id]
                if node.loaded_table_for_lumped_masses:
                    if node.lumped_masses_table_names != self.list_Nones:
                        list_table_names = node.lumped_masses_table_names
                        for basename in self.basenames:
                            if basename in list_table_names:
                                list_table_names.remove(basename)
                        self.process_table_file_removal(list_table_names)

                self.project.add_lumped_masses_by_node([node_id], data, True)
                

    def check_table_values_lumped_stiffness(self):

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stop:
            return

        for node_id in self.nodes_typed:
            Kx = Ky = Kz = None
            if self.lineEdit_path_table_Kx.text() != "":
                if self.Kx_table is None:
                    if self.Kx_filename is None:
                        self.Kx_table, self.Kx_filename = self.load_table(self.lineEdit_path_table_Kx, "Kx", direct_load=True)
                if self.Kx_table is not None:
                    Kx, self.Kx_basename = self.save_tables_files(node_id, self.Kx_table, self.Kx_filename, "Kx", "N/m")

            if self.lineEdit_path_table_Ky.text() != "":
                if self.Ky_table is None:
                    if self.Ky_filename is None:
                        self.Ky_table, self.Ky_filename = self.load_table(self.lineEdit_path_table_Ky, "Ky", direct_load=True)
                if self.Ky_table is not None:
                    Ky, self.Ky_basename = self.save_tables_files(node_id, self.Ky_table, self.Ky_filename, "Ky", "N/m")

            if self.lineEdit_path_table_Kz.text() != "":
                if self.Kz_table is None:
                    if self.Kz_filename is None:
                        self.Kz_table, self.Kz_filename = self.load_table(self.lineEdit_path_table_Kz, "Kz", direct_load=True)
                if self.Kz_table is not None:
                    Kz, self.Kz_basename = self.save_tables_files(node_id, self.Kz_table, self.Kz_filename, "Kz", "N/m")

            Krx = Kry = Krz = None
            if self.lineEdit_path_table_Krx.text() != "":
                if self.Krx_table is None:
                    if self.Krx_filename is None:
                        self.Krx_table, self.Krx_filename = self.load_table(self.lineEdit_path_table_Krx, "Krx", direct_load=True)
                if self.Krx_table is not None:
                    Krx, self.Krx_basename = self.save_tables_files(node_id, self.Krx_table, self.Krx_filename, "Krx", "N.m/rad")

            if self.lineEdit_path_table_Kry.text() != "":
                if self.Kry_table is None:
                    if self.Kry_filename is None:
                        self.Kry_table, self.Kry_filename = self.load_table(self.lineEdit_path_table_Kry, "Kry", direct_load=True)
                if self.Kry_table is not None:
                    Kry, self.Kry_basename = self.save_tables_files(node_id, self.Kry_table, self.Kry_filename, "Kry", "N.m/rad")

            if self.lineEdit_path_table_Krz.text() != "":
                if self.Krz_table is None:
                    if self.Krz_filename is None:
                        self.Krz_table, self.Krz_filename = self.load_table(self.lineEdit_path_table_Krz, "Krz", direct_load=True)
                if self.Krz_table is not None:
                    Krz, self.Krz_basename = self.save_tables_files(node_id, self.Krz_table, self.Krz_filename, "Krz", "N.m/rad")
        
            lumped_stiffness = [Kx, Ky, Kz, Krx, Kry, Krz]

            if sum([0 if bc is None else 1 for bc in lumped_stiffness]) != 0:

                self.flag_lumped_stiffness = True
                self.basenames = [  self.Kx_basename, self.Ky_basename, self.Kz_basename, 
                                    self.Krx_basename, self.Kry_basename, self.Krz_basename  ]
                
                self.lumped_stiffness = lumped_stiffness
                data = [lumped_stiffness, self.basenames]

                node = self.preprocessor.nodes[node_id]
                if node.loaded_table_for_lumped_stiffness:
                    if node.lumped_stiffness_table_names != self.list_Nones:
                        list_table_names = node.lumped_stiffness_table_names
                        for basename in self.basenames:
                            if basename in list_table_names:
                                list_table_names.remove(basename)
                        self.process_table_file_removal(list_table_names)

                self.project.add_lumped_stiffness_by_node([node_id], data, True)

    def check_table_values_lumped_dampings(self):

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_nodeID)
        if self.stop:
            return

        for node_id in self.nodes_typed:
            Cx = Cy = Cz = None
            if self.lineEdit_path_table_Cx.text() != "":
                if self.Cx_table is None:
                    if self.Cx_filename is None:
                        self.Cx_table, self.Cx_filename = self.load_table(self.lineEdit_path_table_Cx, "Cx", direct_load=True)
                if self.Cx_table is not None:
                    Cx, self.Cx_basename = self.save_tables_files(node_id, self.Cx_table, self.Cx_filename, "Cx", "N.s/m")

            if self.lineEdit_path_table_Cy.text() != "":
                if self.Cy_table is None:
                    if self.Cy_filename is None:
                        self.Cy_table, self.Cy_filename = self.load_table(self.lineEdit_path_table_Cy, "Cy", direct_load=True)
                if self.Cy_table is not None:
                    Cy, self.Cy_basename = self.save_tables_files(node_id, self.Cy_table, self.Cy_filename, "Cy", "N.s/m")

            if self.lineEdit_path_table_Cz.text() != "":
                if self.Cz_table is None:
                    if self.Cz_filename is None:
                        self.Cz_table, self.Cz_filename = self.load_table(self.lineEdit_path_table_Cz, "Cz", direct_load=True)
                if self.Cz_table is not None:
                    Cz, self.Cz_basename = self.save_tables_files(node_id, self.Cz_table, self.Cz_filename, "Cz", "N.s/m")

            Crx = Cry = Crz = None
            if self.lineEdit_path_table_Crx.text() != "":
                if self.Crx_table is None:
                    if self.Crx_filename is None:
                        self.Crx_table, self.Crx_filename = self.load_table(self.lineEdit_path_table_Crx, "Crx", direct_load=True)
                if self.Crx_table is not None:
                    Crx, self.Crx_basename = self.save_tables_files(node_id, self.Crx_table, self.Crx_filename, "Crx", "N.m/rad/s")

            if self.lineEdit_path_table_Cry.text() != "":
                if self.Cry_table is None:
                    if self.Cry_filename is None:
                        self.Cry_table, self.Cry_filename = self.load_table(self.lineEdit_path_table_Cry, "Cry", direct_load=True)
                if self.Cry_table is not None:
                    Cry, self.Cry_basename = self.save_tables_files(node_id, self.Cry_table, self.Cry_filename, "Cry", "N.m/rad/s")

            if self.lineEdit_path_table_Crz.text() != "":
                if self.Crz_table is None:
                    if self.Crz_filename is None:
                        self.Crz_table, self.Crz_filename = self.load_table(self.lineEdit_path_table_Crz, "Crz", direct_load=True)
                if self.Crz_table is not None:
                    Crz, self.Crz_basename = self.save_tables_files(node_id, self.Crz_table, self.Crz_filename, "Crz", "N.m/rad/s")
            
            lumped_dampings = [Cx, Cy, Cz, Crx, Cry, Crz]

            if sum([0 if bc is None else 1 for bc in lumped_dampings]) != 0:
                
                self.flag_lumped_dampings = True
                self.basenames = [  self.Cx_basename, self.Cy_basename, self.Cz_basename, 
                                    self.Crx_basename, self.Cry_basename, self.Crz_basename  ]
                
                self.lumped_dampings = lumped_dampings
                data = [lumped_dampings, self.basenames]

                node = self.preprocessor.nodes[node_id]
                if node.loaded_table_for_lumped_dampings:
                    if node.lumped_dampings_table_names != self.list_Nones:
                        list_table_names = node.lumped_dampings_table_names
                        for basename in self.basenames:
                            if basename in list_table_names:
                                list_table_names.remove(basename)
                        self.process_table_file_removal(list_table_names)

                self.project.add_lumped_dampings_by_node([node_id], data, True)

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
            message = "You must inform at least one external element\n" 
            message += "table path before confirming the input!"
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

    def process_table_file_removal(self, list_table_names):
        for table_name in list_table_names:
            self.project.remove_structural_table_files_from_folder(table_name, folder_name="lumped_elements_files")

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
            message = "The masses and moments of inertia attributed to the \n\n"
            message += f"{self.nodes_typed}\n\n node(s) have been removed."
            remove_bc_from_file(self.nodes_typed, self.structural_bc_info_path, key_strings, message, equals_keys=True)
            self.remove_masses_table_files()
            self.preprocessor.add_mass_to_node(self.nodes_typed, data)
   
        if (self.remove_spring and self.tabWidget_remove.currentIndex()==0) or self.tabWidget_remove.currentIndex()==1:   
            key_strings = ["spring stiffness", "torsional spring stiffness"]
            message = "The stiffness (translational and tosional) attributed to the \n\n"
            message += f"{self.nodes_typed}\n\n node(s) have been removed."
            remove_bc_from_file(self.nodes_typed, self.structural_bc_info_path, key_strings, message, equals_keys=True)
            self.remove_stiffness_table_files()
            self.preprocessor.add_spring_to_node(self.nodes_typed, data)
            
        if (self.remove_damper and self.tabWidget_remove.currentIndex()==0) or self.tabWidget_remove.currentIndex()==3: 
            key_strings = ["damping coefficients", "torsional damping coefficients"]
            message = "The dampings (translational and tosional) attributed to the \n\n"
            message += f"{self.nodes_typed}\n\n node(s) have been removed."
            remove_bc_from_file(self.nodes_typed, self.structural_bc_info_path, key_strings, message, equals_keys=True)
            self.remove_damping_table_files()
            self.preprocessor.add_damper_to_node(self.nodes_typed, data)

        self.load_nodes_info()
        self.transform_points(self.nodes_typed)
        # self.close()
    
    def remove_masses_table_files(self):
        for node_typed in self.nodes_typed:
            node = self.preprocessor.nodes[node_typed]
            if node.loaded_table_for_lumped_masses:
                list_table_names = node.lumped_masses_table_names
                self.process_table_file_removal(list_table_names)

    def remove_stiffness_table_files(self):
        for node_typed in self.nodes_typed:
            node = self.preprocessor.nodes[node_typed]
            if node.loaded_table_for_lumped_stiffness:
                list_table_names = node.lumped_stiffness_table_names
                self.process_table_file_removal(list_table_names)
    
    def remove_damping_table_files(self):
        for node_typed in self.nodes_typed:
            node = self.preprocessor.nodes[node_typed]
            if node.loaded_table_for_lumped_dampings:
                list_table_names = node.lumped_dampings_table_names
                self.process_table_file_removal(list_table_names)    

    def process_table_file_removal(self, list_table_names):
        _list_table_names = []
        for table_name in list_table_names:
            if table_name is not None:
                if table_name not in _list_table_names:
                    _list_table_names.append(table_name)

        for _table_name in _list_table_names:
            self.project.remove_structural_table_files_from_folder(_table_name, folder_name="lumped_elements_files")

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
        for node in self.preprocessor.nodes_connected_to_springs:
            lumped_stiffness_mask = [False if bc is None else True for bc in node.lumped_stiffness]
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(lumped_stiffness_mask, load_labels))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_springs.addTopLevelItem(new)

        self.treeWidget_dampers.clear()
        load_labels = np.array(['c_x','c_y','c_z','c_rx','c_ry','c_rz'])
        for node in self.preprocessor.nodes_connected_to_dampers:
            lumped_dampings_mask = [False if bc is None else True for bc in node.lumped_dampings]
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(lumped_dampings_mask, load_labels))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_dampers.addTopLevelItem(new)

        self.treeWidget_masses.clear()
        load_labels = np.array(['m_x','m_y','m_z','Jx','Jy','Jz'])
        for node in self.preprocessor.nodes_with_masses:
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
                            table_name = get_new_path(self.lumped_elements_files_folder_path, table_names[index])
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
                            table_name = get_new_path(self.lumped_elements_files_folder_path, table_names[index])
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
                            table_name = get_new_path(self.lumped_elements_files_folder_path, table_names[index])
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
            