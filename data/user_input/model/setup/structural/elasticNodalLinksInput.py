from PyQt5.QtWidgets import QLineEdit, QDialog, QFileDialog, QTreeWidget, QTreeWidgetItem, QTabWidget, QPushButton, QLabel, QComboBox, QWidget, QToolButton, QMessageBox
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from collections import defaultdict
import os
import numpy as np
import matplotlib.pyplot as plt  

from pulse.utils import get_new_path, remove_bc_from_file
from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput

window_title_1 = "ERROR MESSAGE"
window_title_2 = "WARNING MESSAGE"

class ElasticNodalLinksInput(QDialog):
    def __init__(self, project,  opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Model/Setup/Structural/elasticNodalLinksInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)
        # self.node_id = self.opv.getListPickedPoints()

        self.project = project
        self.preprocessor = project.preprocessor
        self.before_run = project.get_model_checks()
        self.nodes = self.preprocessor.nodes

        self.structural_bc_info_path = project.file._node_structural_path
        # self.imported_data_path = project.file._imported_data_folder_path 
        self.structural_folder_path = self.project.file._structural_imported_data_folder_path
        self.elastic_links_files_folder_path = get_new_path(self.structural_folder_path, "elastic_links_files")
        
        self.userPath = os.path.expanduser('~')       
        self.stop = False
        self.complete = False
        self.aquisition_parameters_processed = False
        self.node_ID_remove = None
        self.ext_key = None
        self.nodeID_1 = None
        self.nodeID_2 = None

        self.elastic_link_stiffness_inputs_from_node = False
        self.elastic_link_dampings_inputs_from_node = False
        
        self.lineEdit_selected_node_ID = self.findChild(QLineEdit, 'lineEdit_selected_node_ID')
        self.lineEdit_first_node_ID = self.findChild(QLineEdit, 'lineEdit_first_node_ID')
        self.lineEdit_last_node_ID = self.findChild(QLineEdit, 'lineEdit_last_node_ID')

        self.lineEdit_Kx = self.findChild(QLineEdit, 'lineEdit_Kx')
        self.lineEdit_Ky = self.findChild(QLineEdit, 'lineEdit_Ky')
        self.lineEdit_Kz = self.findChild(QLineEdit, 'lineEdit_Kz')
        self.lineEdit_Krx = self.findChild(QLineEdit, 'lineEdit_Krx')
        self.lineEdit_Kry = self.findChild(QLineEdit, 'lineEdit_Kry')
        self.lineEdit_Krz = self.findChild(QLineEdit, 'lineEdit_Krz')

        self.list_lineEdit_constant_values_elastic_link_stiffness = [   self.lineEdit_Kx,
                                                                        self.lineEdit_Ky,
                                                                        self.lineEdit_Kz,
                                                                        self.lineEdit_Krx,
                                                                        self.lineEdit_Kry,
                                                                        self.lineEdit_Krz   ]

        self.lineEdit_Cx = self.findChild(QLineEdit, 'lineEdit_Cx')
        self.lineEdit_Cy = self.findChild(QLineEdit, 'lineEdit_Cy')
        self.lineEdit_Cz = self.findChild(QLineEdit, 'lineEdit_Cz')
        self.lineEdit_Crx = self.findChild(QLineEdit, 'lineEdit_Crx')
        self.lineEdit_Cry = self.findChild(QLineEdit, 'lineEdit_Cry')
        self.lineEdit_Crz = self.findChild(QLineEdit, 'lineEdit_Crz')

        self.list_lineEdit_constant_values_elastic_link_dampings = [self.lineEdit_Cx,
                                                                    self.lineEdit_Cy,
                                                                    self.lineEdit_Cz,
                                                                    self.lineEdit_Crx,
                                                                    self.lineEdit_Cry,
                                                                    self.lineEdit_Crz]

        self.lineEdit_path_table_Kx = self.findChild(QLineEdit, 'lineEdit_path_table_Kx')
        self.lineEdit_path_table_Ky = self.findChild(QLineEdit, 'lineEdit_path_table_Ky')
        self.lineEdit_path_table_Kz = self.findChild(QLineEdit, 'lineEdit_path_table_Kz')
        self.lineEdit_path_table_Krx = self.findChild(QLineEdit, 'lineEdit_path_table_Krx')
        self.lineEdit_path_table_Kry = self.findChild(QLineEdit, 'lineEdit_path_table_Kry')
        self.lineEdit_path_table_Krz = self.findChild(QLineEdit, 'lineEdit_path_table_Krz')

        self.list_lineEdit_table_values_elastic_link_stiffness = [  self.lineEdit_path_table_Kx,
                                                                    self.lineEdit_path_table_Ky,
                                                                    self.lineEdit_path_table_Kz,
                                                                    self.lineEdit_path_table_Krx,
                                                                    self.lineEdit_path_table_Kry,
                                                                    self.lineEdit_path_table_Krz  ]

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

        self.list_lineEdit_table_values_elastic_link_dampings = [   self.lineEdit_path_table_Cx,
                                                                    self.lineEdit_path_table_Cy,
                                                                    self.lineEdit_path_table_Cz,
                                                                    self.lineEdit_path_table_Crx,
                                                                    self.lineEdit_path_table_Cry,
                                                                    self.lineEdit_path_table_Crz   ]

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

        self.flag_stiffness_parameters = False
        self.flag_damping_parameters = False
                
        self.pushButton_constant_input_confirm = self.findChild(QPushButton, 'pushButton_constant_input_confirm')
        self.pushButton_constant_input_confirm.clicked.connect(self.constant_input_confirm)

        self.pushButton_table_input_confirm = self.findChild(QPushButton, 'pushButton_table_input_confirm')
        self.pushButton_table_input_confirm.clicked.connect(self.table_input_confirm)

        self.pushButton_remove_link_stiffness = self.findChild(QPushButton, 'pushButton_remove_link_stiffness')
        self.pushButton_remove_link_stiffness.clicked.connect(self.remove_selected_link_stiffness)

        self.pushButton_remove_link_damping = self.findChild(QPushButton, 'pushButton_remove_link_damping')
        self.pushButton_remove_link_damping.clicked.connect(self.remove_selected_link_damping)

        self.pushButton_see_details_selected_link = self.findChild(QPushButton, 'pushButton_see_details_selected_link')
        self.pushButton_see_details_selected_link.clicked.connect(self.get_information)

        self.pushButton_reset_all = self.findChild(QPushButton, 'pushButton_reset_all')
        self.pushButton_reset_all.clicked.connect(self.reset_all)

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.force_to_close)

        self.tabWidget_general = self.findChild(QTabWidget, 'tabWidget_general')
        self.tab_setup = self.tabWidget_general.findChild(QWidget, "tab_setup")
        self.tab_remove = self.tabWidget_general.findChild(QWidget, "tab_remove")

        self.tabWidget_inputs = self.findChild(QTabWidget, 'tabWidget_inputs')
        # self.tabWidget_inputs.currentChanged.connect(self.tabEvent)
        self.tab_constant_values = self.tabWidget_inputs.findChild(QWidget, "tab_constant_values")
        self.tab_table_values = self.tabWidget_inputs.findChild(QWidget, "tab_table_values")

        self.tabWidget_constant_values = self.findChild(QTabWidget, 'tabWidget_single_values')   
        self.tab_spring = self.tabWidget_constant_values.findChild(QWidget, 'tab_spring')
        self.tab_damper = self.tabWidget_constant_values.findChild(QWidget, 'tab_damper')

        self.tabWidget_table_values = self.findChild(QTabWidget, 'tabWidget_table_values')
        self.tab_spring_table = self.tabWidget_table_values.findChild(QWidget, 'tab_spring_table')
        self.tab_damper_table = self.tabWidget_table_values.findChild(QWidget, 'tab_damper_table')

        self.lineEdit_node_ID_info = self.findChild(QLineEdit, 'lineEdit_node_ID_info')
        # self.lineEdit_parameters_info = self.findChild(QLineEdit, 'lineEdit_parameters_info')

        self.treeWidget_nodal_links_stiffness = self.findChild(QTreeWidget, 'treeWidget_nodal_links_stiffness')
        self.treeWidget_nodal_links_stiffness.setColumnWidth(0, 120)
        self.treeWidget_nodal_links_stiffness.itemClicked.connect(self.on_click_item)
        self.treeWidget_nodal_links_stiffness.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_nodal_links_stiffness.headerItem().setTextAlignment(1, Qt.AlignCenter)

        self.treeWidget_nodal_links_damping = self.findChild(QTreeWidget, 'treeWidget_nodal_links_damping')
        self.treeWidget_nodal_links_damping.setColumnWidth(0, 120)
        self.treeWidget_nodal_links_damping.itemClicked.connect(self.on_click_item)
        self.treeWidget_nodal_links_damping.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_nodal_links_damping.headerItem().setTextAlignment(1, Qt.AlignCenter)

        self.update()
        self.load_elastic_links_stiffness_info()
        self.load_elastic_links_damping_info()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_inputs.currentIndex() == 0:
                self.constant_input_confirm()
            elif self.tabWidget_inputs.currentIndex() == 1: 
                self.table_input_confirm() 
        if event.key() == Qt.Key_Escape:
            self.close()

    # def radioButtonEvent_(self):
    #     self.current_tab_index = self.tabWidget_compressor.currentIndex()
    #     if self.current_tab_index == 3:
    #         self.pushButton_confirm.setDisabled(True)
    #     else:
    #         self.pushButton_confirm.setDisabled(False)

    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        self.lineEdit_selected_node_ID.setText(text[:-2])
        if len(list_node_ids) == 2:
            self.lineEdit_first_node_ID.setText(str(min(list_node_ids[-2:])))
            self.lineEdit_last_node_ID.setText(str(max(list_node_ids[-2:])))
        elif len(list_node_ids) == 1:
            self.lineEdit_first_node_ID.setText(str(list_node_ids[-1]))
            self.lineEdit_last_node_ID.setText("")
            
    def check_all_nodes(self):
        
        lineEdit_nodeID = self.lineEdit_first_node_ID.text()
        self.stop, self.nodeID = self.before_run.check_input_NodeID(lineEdit_nodeID, single_ID=True)
        if self.stop:
            return True
        temp_nodeID_1 = self.nodeID
        
        lineEdit_nodeID = self.lineEdit_last_node_ID.text()
        self.stop, self.nodeID = self.before_run.check_input_NodeID(lineEdit_nodeID, single_ID=True)
        if self.stop:
            return True           
        temp_nodeID_2 = self.nodeID

        if temp_nodeID_1 == temp_nodeID_2:
            title = "ERROR IN NODES SELECTION"
            message = "The selected nodes must differ. Try to choose another pair of nodes."
            PrintMessageInput([title, message, window_title_1])
            return True

        if temp_nodeID_2 > temp_nodeID_1:
            self.nodeID_1 = temp_nodeID_1
            self.nodeID_2 = temp_nodeID_2
        else:
            self.nodeID_2 = temp_nodeID_1
            self.nodeID_1 = temp_nodeID_2

        return False
        
    def check_input_parameters(self, lineEdit, label, _float=True):
        title = "INPUT ERROR"
        value_string = lineEdit.text()
        if value_string != "":
            try:
                if _float:
                    value = float(value_string)
                else:
                    value = int(value_string) 
                if value < 0:
                    message = "You cannot input a negative value to the {}.".format(label)
                    PrintMessageInput([title, message, window_title_1])
                    return True
                else:
                    self.value = value
            except Exception:
                message = "You have typed an invalid value to the {}.".format(label)
                PrintMessageInput([title, message, window_title_1])
                return True
        else:
            self.value = None
        return False
    
    def check_all_inputs(self):
        self.parameters_K = None
        self.parameters_C = None
        if self.check_all_nodes():
            return True

        if self.check_input_parameters(self.lineEdit_Kx, 'Kx'):
            return True
        else:
            Kx = self.value

        if self.check_input_parameters(self.lineEdit_Ky, 'Ky'):
            return True
        else:
            Ky = self.value

        if self.check_input_parameters(self.lineEdit_Kz, 'Kz'):
            return True
        else:
            Kz = self.value

        if self.check_input_parameters(self.lineEdit_Krx, 'Krx'):
            return True
        else:
            Krx = self.value

        if self.check_input_parameters(self.lineEdit_Kry, 'Kry'):
            return True
        else:
            Kry = self.value

        if self.check_input_parameters(self.lineEdit_Krz, 'Krz'):
            return True
        else:
            Krz = self.value
        
        if self.check_input_parameters(self.lineEdit_Cx, 'Cx'):
            return True
        else:
            Cx = self.value

        if self.check_input_parameters(self.lineEdit_Cy, 'Cy'):
            return True
        else:
            Cy = self.value

        if self.check_input_parameters(self.lineEdit_Cz, 'Cz'):
            return True
        else:
            Cz = self.value

        if self.check_input_parameters(self.lineEdit_Crx, 'Crx'):
            return True
        else:
            Crx = self.value

        if self.check_input_parameters(self.lineEdit_Cry, 'Cry'):
            return True
        else:
            Cry = self.value

        if self.check_input_parameters(self.lineEdit_Crz, 'Crz'):
            return True
        else:
            Crz = self.value

        list_K = [Kx, Ky, Kz, Krx, Kry, Krz]
        list_C = [Cx, Cy, Cz, Crx, Cry, Crz] 
                
        if list_K.count(None) != 6:
            self.parameters_K = list_K
        if list_C.count(None) != 6:
            self.parameters_C = list_C
        
        if list_K.count(None) == 6 and list_C.count(None) == 6:
            title = 'EMPTY INPUTS FOR STIFFNESS AND DAMPING'
            message = 'Please insert at least a stiffness or damping value before confirming the attribution.'
            PrintMessageInput([title, message, window_title_1])

    def constant_input_confirm(self):
        if self.check_all_inputs():
            return
        table_names = [None, None, None, None, None, None]
        if self.parameters_K is not None:
            self.remove_elastic_link_stiffness_table_files()
            data = [self.parameters_K, table_names]
            self.project.add_elastic_nodal_link_stiffness(self.nodeID_1, self.nodeID_2, data, False)
        if self.parameters_C is not None:
            self.remove_elastic_link_damping_table_files()
            data = [self.parameters_C, table_names]
            self.project.add_elastic_nodal_link_damping(self.nodeID_1, self.nodeID_2, data, False)
        if (self.parameters_K or self.parameters_C) is not None:
            self.opv.updateRendererMesh()
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
            
            # for ext_format in [".csv", ".dat", ".txt"]:
            #     if ext_format in self.basename:
            #         prefix_string = self.basename.split(ext_format)[0]
            #         self.imported_filename = prefix_string.split(f"_{_label}_node_")[0]
                        
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

                if self.project.change_project_frequency_setup(_label, list(self.frequencies)):
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

    def save_tables_files(self, values, filename, _label, unit_label):

        real_values = np.real(values)
        data = np.array([self.frequencies, real_values]).T
        self.project.create_folders_structural("elastic_links_files")

        if _label in ["Kx", "Ky", "Kz", "Krx", "Kry", "Krz"]:
            header = f"OpenPulse - stiffness elastic link - imported table for {_label}  @ "
            basename = f"elastic_link_stiffness_{_label}_linked_nodes_{self.nodeID_1}_{self.nodeID_2}.dat"
            values_label = "Stiffness values"

        else:
            header = f"OpenPulse - damping elastic link - imported table for {_label} @ "
            basename = f"elastic_link_damping_{_label}_linked_nodes_{self.nodeID_1}_{self.nodeID_2}.dat"
            values_label = "Damping values"
            
        header += f"linked nodes {self.nodeID_1}-{self.nodeID_2}\n"
        header += f"\nSource filename: {filename}\n"
        header += f"\nFrequency [Hz], {values_label} [{unit_label}]"
        # basename = filename + f"_{_label}_linked_nodes_{self.nodeID_1}_{self.nodeID_1}.dat"
    
        new_path_table = get_new_path(self.elastic_links_files_folder_path, basename)
        np.savetxt(new_path_table, data, delimiter=",", header=header)

        return values, basename

    def check_table_for_elastic_link_stiffness(self):

        Kx = Ky = Kz = None
        if self.lineEdit_path_table_Kx.text() != "":
            if self.Kx_table is None:
                if self.Kx_filename is None:
                    self.Kx_table, self.Kx_filename = self.load_table(self.lineEdit_path_table_Kx, "Kx", direct_load=True)
            if self.Kx_table is not None:
                Kx, self.Kx_basename = self.save_tables_files(self.Kx_table, self.Kx_filename, "Kx", "N/m")

        if self.lineEdit_path_table_Ky.text() != "":
            if self.Ky_table is None:
                if self.Ky_filename is None:
                    self.Ky_table, self.Ky_filename = self.load_table(self.lineEdit_path_table_Ky, "Ky", direct_load=True)
            if self.Ky_table is not None:
                Ky, self.Ky_basename = self.save_tables_files(self.Ky_table, self.Ky_filename, "Ky", "N/m")

        if self.lineEdit_path_table_Kz.text() != "":
            if self.Kz_table is None:
                if self.Kz_filename is None:
                    self.Kz_table, self.Kz_filename = self.load_table(self.lineEdit_path_table_Kz, "Kz", direct_load=True)
            if self.Kz_table is not None:
                Kz, self.Kz_basename = self.save_tables_files(self.Kz_table, self.Kz_filename, "Kz", "N/m")

        Krx = Kry = Krz = None
        if self.lineEdit_path_table_Krx.text() != "":
            if self.Krx_table is None:
                if self.Krx_filename is None:
                    self.Krx_table, self.Krx_filename = self.load_table(self.lineEdit_path_table_Krx, "Krx", direct_load=True)
            if self.Krx_table is not None:
                Krx, self.Krx_basename = self.save_tables_files(self.Krx_table, self.Krx_filename, "Krx", "N.m/rad")

        if self.lineEdit_path_table_Kry.text() != "":
            if self.Kry_table is None:
                if self.Kry_filename is None:
                    self.Kry_table, self.Kry_filename = self.load_table(self.lineEdit_path_table_Kry, "Kry", direct_load=True)
            if self.Kry_table is not None:
                Kry, self.Kry_basename = self.save_tables_files(self.Kry_table, self.Kry_filename, "Kry", "N.m/rad")

        if self.lineEdit_path_table_Krz.text() != "":
            if self.Krz_table is None:
                if self.Krz_filename is None:
                    self.Krz_table, self.Krz_filename = self.load_table(self.lineEdit_path_table_Krz, "Krz", direct_load=True)
            if self.Krz_table is not None:
                Krz, self.Krz_basename = self.save_tables_files(self.Krz_table, self.Krz_filename, "Krz", "N.m/rad")
        
        stiffness_parameters = [Kx, Ky, Kz, Krx, Kry, Krz]

        if sum([0 if bc is None else 1 for bc in stiffness_parameters]) != 0:
            self.flag_stiffness_parameters = True
            self.K_basenames = [self.Kx_basename, self.Ky_basename, self.Kz_basename, 
                                self.Krx_basename, self.Kry_basename, self.Krz_basename]
            self.stiffness_parameters = stiffness_parameters
            data = [stiffness_parameters, self.K_basenames]

            key = f"{self.nodeID_1}-{self.nodeID_2}"
            for node_id in [self.nodeID_1, self.nodeID_2]:
                node = self.preprocessor.nodes[node_id]
                if node.loaded_table_for_elastic_link_stiffness:
                    if key in node.elastic_nodal_link_stiffness.keys():
                        list_table_names = node.elastic_nodal_link_stiffness[key][1]
                        for basename in self.K_basenames:
                            if basename in list_table_names:
                                list_table_names.remove(basename)
                        self.process_table_file_removal(list_table_names)

            self.project.add_elastic_nodal_link_stiffness(self.nodeID_1, self.nodeID_2, data, True)
            return False
        else:
            return True

    def check_table_for_elastic_link_damping(self):
 
        Cx = Cy = Cz = None
        if self.lineEdit_path_table_Cx.text() != "":
            if self.Cx_table is None:
                if self.Cx_filename is None:
                    self.Cx_table, self.Cx_filename = self.load_table(self.lineEdit_path_table_Cx, "Cx", direct_load=True)
            if self.Cx_table is not None:
                Cx, self.Cx_basename = self.save_tables_files(self.Cx_table, self.Cx_filename, "Cx", "N.s/m")
        
            if self.lineEdit_path_table_Cy.text() != "":
                if self.Cy_table is None:
                    if self.Cy_filename is None:
                        self.Cy_table, self.Cy_filename = self.load_table(self.lineEdit_path_table_Cy, "Cy", direct_load=True)
                if self.Cy_table is not None:
                    Cy, self.Cy_basename = self.save_tables_files(self.Cy_table, self.Cy_filename, "Cy", "N.s/m")

            if self.lineEdit_path_table_Cz.text() != "":
                if self.Cz_table is None:
                    if self.Cz_filename is None:
                        self.Cz_table, self.Cz_filename = self.load_table(self.lineEdit_path_table_Cz, "Cz", direct_load=True)
                if self.Cz_table is not None:
                    Cz, self.Cz_basename = self.save_tables_files(self.Cz_table, self.Cz_filename, "Cz", "N.s/m")

            Crx = Cry = Crz = None
            if self.lineEdit_path_table_Crx.text() != "":
                if self.Crx_table is None:
                    if self.Crx_filename is None:
                        self.Crx_table, self.Crx_filename = self.load_table(self.lineEdit_path_table_Crx, "Crx", direct_load=True)
                if self.Crx_table is not None:
                    Crx, self.Crx_basename = self.save_tables_files(self.Crx_table, self.Crx_filename, "Crx", "N.m/rad/s")

            if self.lineEdit_path_table_Cry.text() != "":
                if self.Cry_table is None:
                    if self.Cry_filename is None:
                        self.Cry_table, self.Cry_filename = self.load_table(self.lineEdit_path_table_Cry, "Cry", direct_load=True)
                if self.Cry_table is not None:
                    Cry, self.Cry_basename = self.save_tables_files(self.Cry_table, self.Cry_filename, "Cry", "N.m/rad/s")

            if self.lineEdit_path_table_Crz.text() != "":
                if self.Crz_table is None:
                    if self.Crz_filename is None:
                        self.Crz_table, self.Crz_filename = self.load_table(self.lineEdit_path_table_Crz, "Crz", direct_load=True)
                if self.Crz_table is not None:
                    Crz, self.Crz_basename = self.save_tables_files(self.Crz_table, self.Crz_filename, "Crz", "N.m/rad/s")
                    
        damping_parameters = [Cx, Cy, Cz, Crx, Cry, Crz]
 
        if sum([0 if bc is None else 1 for bc in damping_parameters]) != 0:
            self.flag_damping_parameters = True
            self.C_basenames = [self.Cx_basename, self.Cy_basename, self.Cz_basename, 
                                self.Crx_basename, self.Cry_basename, self.Crz_basename]
            self.damping_parameters = damping_parameters
            data = [damping_parameters, self.C_basenames]
            
            key = f"{self.nodeID_1}-{self.nodeID_2}"

            for node_id in [self.nodeID_1, self.nodeID_2]:
                node = self.preprocessor.nodes[node_id]
                if node.loaded_table_for_elastic_link_dampings:
                    if key in node.elastic_nodal_link_dampings.keys():
                        list_table_names = node.elastic_nodal_link_dampings[key][1]
                        for basename in self.C_basenames:
                            if basename in list_table_names:
                                list_table_names.remove(basename)
                        self.process_table_file_removal(list_table_names)

            self.project.add_elastic_nodal_link_damping(self.nodeID_1, self.nodeID_2, data, True)
            return False
        else:
            return True
  
    def table_input_confirm(self):

        if self.check_all_nodes():
            return True

        self.check_table_for_elastic_link_stiffness()
        self.check_table_for_elastic_link_damping()

        if not (self.flag_stiffness_parameters or self.flag_damping_parameters):
            title = 'NONE TABLE SELECTED FOR STIFFNESS OR DAMPING'
            message = "Please, define at least a table of values to the stiffness or damping" 
            message += "before confirming the elastic link attribution."
            PrintMessageInput([title, message, window_title_1])
            return
      
        self.opv.updateRendererMesh()
        self.close()

    def remove_elastic_link_stiffness_table_files(self):
        for node_id in [self.nodeID_1, self.nodeID_2]:
            node = self.preprocessor.nodes[node_id]
            if node.loaded_table_for_elastic_link_stiffness:
                key = f"{self.nodeID_1}-{self.nodeID_2}"
                if key in node.elastic_nodal_link_stiffness.keys():
                    list_table_names = node.elastic_nodal_link_stiffness[key][1]
                    self.process_table_file_removal(list_table_names)

    def remove_elastic_link_damping_table_files(self):
        for node_id in [self.nodeID_1, self.nodeID_2]:
            node = self.preprocessor.nodes[node_id]
            if node.loaded_table_for_elastic_link_dampings:
                key = f"{self.nodeID_1}-{self.nodeID_2}"
                if key in node.elastic_nodal_link_dampings.keys():
                    list_table_names = node.elastic_nodal_link_dampings[key][1]
                    self.process_table_file_removal(list_table_names)

    def process_table_file_removal(self, list_table_names):
        for table_name in list_table_names:
            self.project.remove_structural_table_files_from_folder(table_name, folder_name="elastic_links_files")

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

    def skip_treeWidget_row(self, treeWidget):
        new = QTreeWidgetItem(["", "", ""])
        new.setTextAlignment(0, Qt.AlignCenter)
        new.setTextAlignment(1, Qt.AlignCenter)
        new.setTextAlignment(2, Qt.AlignCenter)
        treeWidget.addTopLevelItem(new)

    def load_elastic_links_stiffness_info(self):

        self.treeWidget_nodal_links_stiffness.clear()
        stiffness_labels = np.array(['k_x','k_y','k_z','k_rx','k_ry','k_rz']) 
        self.skip_treeWidget_row(self.treeWidget_nodal_links_stiffness)
        self.pushButton_remove_link_stiffness.setDisabled(False)

        for key in self.preprocessor.nodes_with_elastic_link_stiffness.keys():
            node_ids = [int(node) for node in key.split("-")]
            mask, _ = self.preprocessor.nodes[node_ids[0]].elastic_nodal_link_stiffness[key]
            new = QTreeWidgetItem([key, str(self.text_label(mask, stiffness_labels))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_nodal_links_stiffness.addTopLevelItem(new)

        self.update_main_tabs_visibility()
        # if len(self.preprocessor.nodes_with_elastic_link_stiffness) == 0:
        #     self.pushButton_remove_link_stiffness.setDisabled(True)

    def load_elastic_links_damping_info(self):

        self.treeWidget_nodal_links_damping.clear()
        damping_labels = np.array(['c_x','c_y','c_z','c_rx','c_ry','c_rz']) 
        self.skip_treeWidget_row(self.treeWidget_nodal_links_damping)
        self.pushButton_remove_link_damping.setDisabled(False)

        for key in self.preprocessor.nodes_with_elastic_link_dampings.keys():
            node_ids = [int(node) for node in key.split("-")]
            mask, _ = self.preprocessor.nodes[node_ids[0]].elastic_nodal_link_dampings[key]
            new = QTreeWidgetItem([key, str(self.text_label(mask, damping_labels))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_nodal_links_damping.addTopLevelItem(new)
        
        self.update_main_tabs_visibility()
        # if len(self.preprocessor.nodes_with_elastic_link_dampings) == 0:
        #     self.pushButton_remove_link_damping.setDisabled(True)

    def update_main_tabs_visibility(self):
        size_1 = len(self.preprocessor.nodes_with_elastic_link_stiffness)
        size_2 = len(self.preprocessor.nodes_with_elastic_link_dampings)
        if size_1 + size_2 == 0:
            self.tab_remove.setDisabled(True)
            self.tabWidget_general.setCurrentIndex(0)
            self.tabWidget_inputs.setCurrentIndex(0)
            self.reset_stiffness_input_fields(force_reset=False)
            self.reset_dampings_input_fields(force_reset=False)
        else:
            self.tab_remove.setDisabled(False)

    def on_click_item(self, item):
        self.lineEdit_node_ID_info.setText(item.text(0))

    def remove_selected_link_stiffness(self):
        if self.ext_key is None:
            key = self.lineEdit_node_ID_info.text()
        else:
            key = self.ext_key
        if key == "":
            title = "EMPTY SELECTION IN ELASTIC LINK REMOVAL"
            message = "Please, select a stiffness elastic link in the list before confirm the link removal."
            PrintMessageInput([title, message, window_title_2])
            return
        else:
            str_ids = key.split("-")
            self.nodeID_1, self.nodeID_2 = [int(str_id) for str_id in str_ids]
        
        key_strings = ["connecting stiffness", "connecting torsional stiffness"]
        if self.ext_key is None:    
            message = "The stiffness elastic link attributed to the \n\n"
            message += f"{key}\n\n link of node(s) have been removed."
        else:
            message = None

        remove_bc_from_file([key], self.structural_bc_info_path, key_strings, message, equals_keys=True)
        self.remove_elastic_link_stiffness_table_files()
        self.preprocessor.add_elastic_nodal_link(self.nodeID_1, self.nodeID_2, None, _stiffness=True)
        self.load_elastic_links_stiffness_info()
        self.opv.updateRendererMesh()
        self.lineEdit_node_ID_info.setText("")
        self.ext_key = None

    def remove_selected_link_damping(self):
        if self.ext_key is None:
            key = self.lineEdit_node_ID_info.text()
        else:
            key = self.ext_key
        if key == "":
            title = "EMPTY SELECTION IN ELASTIC LINK REMOVAL"
            message = "Please, select a damping elastic link in the list before confirm the link removal."
            PrintMessageInput([title, message, window_title_2])
            return
        else:
            str_ids = key.split("-")
            self.nodeID_1, self.nodeID_2 = [int(str_id) for str_id in str_ids]
        
        key_strings = ["connecting damping", "connecting torsional damping"]
        if self.ext_key is None: 
            message = "The damping elastic link attributed to the \n\n"
            message += f"{key}\n\n link of node(s) have been removed."
        else:
            message = None

        remove_bc_from_file([key], self.structural_bc_info_path, key_strings, message, equals_keys=True)
        self.remove_elastic_link_damping_table_files()
        self.preprocessor.add_elastic_nodal_link(self.nodeID_1, self.nodeID_2, None, _damping=True)
        self.load_elastic_links_damping_info()
        self.opv.updateRendererMesh()
        self.lineEdit_node_ID_info.setText("")

    def reset_all(self):

        title = "Remove all nodal elastic links added to the model"
        message = "Do you really want to remove all nodal elastic links from the structural model?\n\n\n"
        message += "Press the Continue button to proceed with removal or press Cancel or Close buttons to abort the current operation."
        read = CallDoubleConfirmationInput(title, message, leftButton_label='Cancel', rightButton_label='Continue')

        # if read._doNotRun:
        #     return

        if read._continue:
            temp_dict_stiffness = self.preprocessor.nodes_with_elastic_link_stiffness.copy()
            temp_dict_damping = self.preprocessor.nodes_with_elastic_link_dampings.copy()
            for key in temp_dict_stiffness.keys():
                
                self.ext_key = key
                self.remove_selected_link_stiffness()
            for key in temp_dict_damping.keys():
                
                self.ext_key = key
                self.remove_selected_link_damping()
            title = "Reseting process complete"
            message = "All elastic nodal links have been removed from the model."
            PrintMessageInput([title, message, window_title_2])
            self.ext_key = None
            self.reset_nodes_input_fields()
            self.close()

    def get_information(self):
        try:
            selected_link = self.lineEdit_node_ID_info.text()
            if selected_link != "":        
                GetInformationOfGroup(self.project, selected_link, "Lines")
            else:
                title = "UNSELECTED ELASTIC LINK"
                message = "Please, select an elastic link in the list to get the information."
                PrintMessageInput([title, message, window_title_2])
                
        except Exception as e:
            title = "ERROR WHILE GETTING INFORMATION OF SELECTED ELASTIC LINK"
            message = str(e)
            PrintMessageInput([title, message, window_title_1])

    def force_to_close(self):
        self.close()

    def reset_nodes_input_fields(self):
        self.lineEdit_node_ID_info.setText("")
        self.lineEdit_first_node_ID.setText("")
        self.lineEdit_last_node_ID.setText("")
        self.lineEdit_selected_node_ID.setText("")
    
    def reset_stiffness_input_fields(self, force_reset=False):
        if self.elastic_link_stiffness_inputs_from_node or force_reset:
            for lineEdit_constant_stiffness in self.list_lineEdit_constant_values_elastic_link_stiffness:    
                lineEdit_constant_stiffness.setText("")
            for lineEdit_table_stiffness in self.list_lineEdit_table_values_elastic_link_stiffness:
                lineEdit_table_stiffness.setText("")
            self.elastic_link_stiffness_inputs_from_node = False

    def reset_dampings_input_fields(self, force_reset=False):
        if self.elastic_link_dampings_inputs_from_node or force_reset:
            for lineEdit_constant_dampings in self.list_lineEdit_constant_values_elastic_link_dampings:    
                lineEdit_constant_dampings.setText("")
            for lineEdit_table_dampings in self.list_lineEdit_table_values_elastic_link_dampings:
                lineEdit_table_dampings.setText("")
            self.elastic_link_dampings_inputs_from_node = False

    def update(self):
      
        list_picked_nodes = self.opv.getListPickedPoints()
        # if list_picked_nodes != []:
        if len(list_picked_nodes) == 2:
            # picked_node = list_picked_nodes[0]
            first_node = min(list_picked_nodes)
            last_node = max(list_picked_nodes)
            key = f"{first_node}-{last_node}"
            node = self.preprocessor.nodes[first_node]
            self.writeNodes(self.opv.getListPickedPoints())
        else:
            return

        #Elastic link stiffness
        if node.there_are_elastic_nodal_link_stiffness:
            self.reset_stiffness_input_fields(force_reset=True)
            if key in node.elastic_nodal_link_stiffness.keys():
                if node.loaded_table_for_elastic_link_stiffness:
                    table_names = elastic_link_stiffness = node.elastic_nodal_link_stiffness[key][1]
                    self.tabWidget_inputs.setCurrentWidget(self.tab_table_values)
                    self.tabWidget_table_values.setCurrentWidget(self.tab_spring_table)
                    for index, lineEdit_table in enumerate(self.list_lineEdit_table_values_elastic_link_stiffness):
                        if table_names[index] is not None:
                            table_name = get_new_path(self.elastic_links_files_folder_path, table_names[index])
                            lineEdit_table.setText(table_name)
                else:
                    elastic_link_stiffness = node.elastic_nodal_link_stiffness[key][1]
                    self.tabWidget_inputs.setCurrentWidget(self.tab_constant_values)
                    self.tabWidget_constant_values.setCurrentWidget(self.tab_spring)
                    for index, lineEdit_constant in enumerate(self.list_lineEdit_constant_values_elastic_link_stiffness):
                        if elastic_link_stiffness[index] is not None:
                            lineEdit_constant.setText(str(elastic_link_stiffness[index]))
                self.elastic_link_stiffness_inputs_from_node = True
        else:
            self.reset_stiffness_input_fields()

        #Elastic link dampings
        if node.there_are_elastic_nodal_link_dampings:
            self.reset_dampings_input_fields(force_reset=True)
            if key in node.elastic_nodal_link_dampings.keys():
                if node.loaded_table_for_elastic_link_dampings:
                    table_names = node.elastic_nodal_link_dampings[key][1]
                    self.tabWidget_inputs.setCurrentWidget(self.tab_table_values)
                    self.tabWidget_table_values.setCurrentWidget(self.tab_damper_table)
                    for index, lineEdit_table in enumerate(self.list_lineEdit_table_values_elastic_link_dampings):
                        if table_names[index] is not None:
                            table_name = get_new_path(self.elastic_links_files_folder_path, table_names[index])
                            lineEdit_table.setText(table_name)
                else:
                    elastic_link_dampings = node.elastic_nodal_link_dampings[key][1]
                    self.tabWidget_inputs.setCurrentWidget(self.tab_constant_values)
                    self.tabWidget_constant_values.setCurrentWidget(self.tab_damper)
                    for index, lineEdit_constant in enumerate(self.list_lineEdit_constant_values_elastic_link_dampings):
                        if elastic_link_dampings[index] is not None:
                            lineEdit_constant.setText(str(elastic_link_dampings[index]))
                self.elastic_link_dampings_inputs_from_node = True
        else:
            self.reset_dampings_input_fields()
        

class GetInformationOfGroup(QDialog):
    def __init__(self, project, selected_link, label, *args, **kwargs):
        super().__init__(*args, **kwargs)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        uic.loadUi('data/user_input/ui/Model/Info/getGroupInformationInput.ui', self)

        self.label = label
        self.selected_link = selected_link
        self.node_IDs = [int(node) for node in selected_link.split("-")]

        self.project = project
        self.nodes = project.preprocessor.nodes
        self.dict_elastic_link_stiffness = {}
        self.dict_elastic_link_damping = {}

        self.title_label = self.findChild(QLabel, 'title_label')
        self.title_label.setText('INFORMATION OF SELECTED ELASTIC LINK')

        self.treeWidget_group_info = self.findChild(QTreeWidget, 'treeWidget_group_info')
        self.treeWidget_group_info.headerItem().setText(0, "Linked nodes")
        self.treeWidget_group_info.headerItem().setText(1, "Parameter")
        self.treeWidget_group_info.headerItem().setText(2, "Value")
        self.treeWidget_group_info.setColumnWidth(0, 100)
        self.treeWidget_group_info.setColumnWidth(1, 90)
        self.treeWidget_group_info.setColumnWidth(2, 120)
        self.treeWidget_group_info.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_group_info.headerItem().setTextAlignment(1, Qt.AlignCenter)
        self.treeWidget_group_info.headerItem().setTextAlignment(2, Qt.AlignCenter)
        
        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.force_to_close)
        
        self.load_file_info()
        self.update_treeWidget_info()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Enter:
            self.close()

    def update_dict(self):
        self.dict_lines_parameters = self.preprocessor.dict_lines_with_stress_stiffening
        self.dict_elements_parameters = self.preprocessor.group_elements_with_stress_stiffening

    def load_file_info(self):

        config = configparser.ConfigParser()
        config.read(self.project.file._node_structural_path)

        for str_node in config.sections():

            keys = list(config[str_node].keys())

            if "connecting stiffness" in keys and "connecting torsional stiffness" in keys:
                connecting_stiffness = config[str_node]['connecting stiffness'][1:-1].split(',')
                connecting_torsional_stiffness = config[str_node]['connecting torsional stiffness'][1:-1].split(',')
                out_stiffness = [value for _list in [connecting_stiffness, connecting_torsional_stiffness] for value in _list]
                self.dict_elastic_link_stiffness[str_node] = out_stiffness
        
            if "connecting damping" in keys and "connecting torsional damping" in keys:
                connecting_damping = config[str_node]['connecting damping'][1:-1].split(',')
                connecting_torsional_damping = config[str_node]['connecting torsional damping'][1:-1].split(',')
                out_damping = [value for _list in [connecting_damping, connecting_torsional_damping] for value in _list]
                self.dict_elastic_link_damping[str_node] = out_damping          
    
    def skip_treeWidget_row(self):
        new = QTreeWidgetItem(["", "", ""])
        new.setTextAlignment(0, Qt.AlignCenter)
        new.setTextAlignment(1, Qt.AlignCenter)
        new.setTextAlignment(2, Qt.AlignCenter)
        self.treeWidget_group_info.addTopLevelItem(new)

    def update_treeWidget_info(self):

        self.treeWidget_group_info.clear()
        
        try:

            mask_stiffness, _ = self.nodes[self.node_IDs[0]].elastic_nodal_link_stiffness[self.selected_link]
            stiffness_labels = np.array(['k_x','k_y','k_z','k_rx','k_ry','k_rz'])
            output_stiffness_labels = stiffness_labels[mask_stiffness]
            values_stiffness = np.array(self.dict_elastic_link_stiffness[self.selected_link])[mask_stiffness]        
            
            self.skip_treeWidget_row()
            for i, value in enumerate(values_stiffness):
                new = QTreeWidgetItem([str(self.selected_link), output_stiffness_labels[i], value])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                new.setTextAlignment(2, Qt.AlignCenter)
                self.treeWidget_group_info.addTopLevelItem(new)
        except:
            pass

        try:

            damping_labels = np.array(['c_x','c_y','c_z','c_rx','c_ry','c_rz']) 
            mask_damping, _ = self.nodes[self.node_IDs[0]].elastic_nodal_link_dampings[self.selected_link]
            output_damping_labels = damping_labels[mask_damping]
            values_damping = np.array(self.dict_elastic_link_damping[self.selected_link])[mask_damping]
            
            self.skip_treeWidget_row()
            for i, value in enumerate(values_damping):
                new = QTreeWidgetItem([str(self.selected_link), output_damping_labels[i], value])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                new.setTextAlignment(2, Qt.AlignCenter)
                self.treeWidget_group_info.addTopLevelItem(new)
        except:
            pass

    def force_to_close(self):
        self.close()


    # def remove_table_files(self, values):          
    #     for value in values:
    #         if value != 'None' and ".dat" in value:
    #             self.path_of_selected_table = get_new_path(self.elastic_links_tables_folder_path, value)
    #             # self.get_path_of_selected_table(value)
    #             try:
    #                 os.remove(self.path_of_selected_table)
    #             except:
    #                 pass

    # def remove_elastic_link_stiffness_from_file(self, section_key):

    #     path = self.project.file._node_structural_path
    #     config = configparser.ConfigParser()
    #     config.read(path)

    #     keys = list(config[section_key].keys())
    #     if "connecting stiffness" in keys and "connecting torsional stiffness" in keys:
    #         values_stiffness = config[section_key]["connecting stiffness"][1:-1].split(",")
    #         self.remove_table_files(values_stiffness)
    #         values_torsional_stiffness = config[section_key]["connecting torsional stiffness"][1:-1].split(",")
    #         self.remove_table_files(values_torsional_stiffness)
    #         config.remove_option(section=section_key, option="connecting stiffness")
    #         config.remove_option(section=section_key, option="connecting torsional stiffness")
    #         if len(list(config[section_key].keys())) == 0:
    #             config.remove_section(section=section_key)
    #     with open(path, 'w') as config_file:
    #         config.write(config_file)

    # def remove_elastic_link_damping_from_file(self, section_key):

    #     path = self.project.file._node_structural_path
    #     config = configparser.ConfigParser()
    #     config.read(path)        

    #     keys = list(config[section_key].keys())
    #     if "connecting damping" in keys and "connecting torsional damping" in keys:
    #         values_damping = config[section_key]["connecting damping"][1:-1].split(",")
    #         self.remove_table_files(values_damping)
    #         values_torsional_damping = config[section_key]["connecting torsional damping"][1:-1].split(",")
    #         self.remove_table_files(values_torsional_damping)
    #         config.remove_option(section=section_key, option="connecting damping")
    #         config.remove_option(section=section_key, option="connecting torsional damping")
    #         if len(list(config[section_key].keys())) == 0:
    #             config.remove_section(section=section_key)    
    #     with open(path, 'w') as config_file:
    #         config.write(config_file)