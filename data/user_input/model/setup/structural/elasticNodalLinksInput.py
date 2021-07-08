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

from pulse.preprocessing.compressor_model import CompressorModel
from data.user_input.project.printMessageInput import PrintMessageInput

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"

class ElasticNodalLinksInput(QDialog):
    def __init__(self, project,  opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Model/Setup/Structural/elasticNodalLinksInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.opv = opv
        self.opv.setInputObject(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.project = project
        self.mesh = project.mesh
        self.nodes = self.project.mesh.nodes
        self.node_id = self.opv.getListPickedPoints()

        self.project_folder_path = project.project_folder_path 
        self.userPath = os.path.expanduser('~')       
        self.stop = False
        self.complete = False
        self.aquisition_parameters_processed = False
        self.node_ID_remove = None
        self.ext_key = None
        
        self.lineEdit_selected_node_ID = self.findChild(QLineEdit, 'lineEdit_selected_node_ID')
        self.lineEdit_first_node_ID = self.findChild(QLineEdit, 'lineEdit_first_node_ID')
        self.lineEdit_last_node_ID = self.findChild(QLineEdit, 'lineEdit_last_node_ID')

        self.lineEdit_Kx = self.findChild(QLineEdit, 'lineEdit_Kx')
        self.lineEdit_Ky = self.findChild(QLineEdit, 'lineEdit_Ky')
        self.lineEdit_Kz = self.findChild(QLineEdit, 'lineEdit_Kz')
        self.lineEdit_Krx = self.findChild(QLineEdit, 'lineEdit_Krx')
        self.lineEdit_Kry = self.findChild(QLineEdit, 'lineEdit_Kry')
        self.lineEdit_Krz = self.findChild(QLineEdit, 'lineEdit_Krz')

        self.lineEdit_Cx = self.findChild(QLineEdit, 'lineEdit_Cx')
        self.lineEdit_Cy = self.findChild(QLineEdit, 'lineEdit_Cy')
        self.lineEdit_Cz = self.findChild(QLineEdit, 'lineEdit_Cz')
        self.lineEdit_Crx = self.findChild(QLineEdit, 'lineEdit_Crx')
        self.lineEdit_Cry = self.findChild(QLineEdit, 'lineEdit_Cry')
        self.lineEdit_Crz = self.findChild(QLineEdit, 'lineEdit_Crz')

        self.lineEdit_path_table_Kx = self.findChild(QLineEdit, 'lineEdit_path_table_Kx')
        self.lineEdit_path_table_Ky = self.findChild(QLineEdit, 'lineEdit_path_table_Ky')
        self.lineEdit_path_table_Kz = self.findChild(QLineEdit, 'lineEdit_path_table_Kz')
        self.lineEdit_path_table_Krx = self.findChild(QLineEdit, 'lineEdit_path_table_Krx')
        self.lineEdit_path_table_Kry = self.findChild(QLineEdit, 'lineEdit_path_table_Kry')
        self.lineEdit_path_table_Krz = self.findChild(QLineEdit, 'lineEdit_path_table_Krz')

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

        self.tabWidget_inputs = self.findChild(QTabWidget, 'tabWidget_inputs')
        # self.tabWidget_inputs.currentChanged.connect(self.tabEvent)

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

        self.writeNodes(self.opv.getListPickedPoints())
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
        self.lineEdit_selected_node_ID.setText(text)
        if len(list_node_ids) == 2:
            self.lineEdit_first_node_ID.setText(str(min(list_node_ids[-2:])))
            self.lineEdit_last_node_ID.setText(str(max(list_node_ids[-2:])))
        elif len(list_node_ids) == 1:
            self.lineEdit_first_node_ID.setText(str(list_node_ids[-1]))
            self.lineEdit_last_node_ID.setText("")

    def update(self):
        self.writeNodes(self.opv.getListPickedPoints())
             
    def check_all_nodes(self):
        
        lineEdit_nodeID = self.lineEdit_first_node_ID.text()
        self.stop, self.nodeID = self.mesh.check_input_NodeID(lineEdit_nodeID, single_ID=True)
        if self.stop:
            return True
        temp_nodeID_1 = self.nodeID
        
        lineEdit_nodeID = self.lineEdit_last_node_ID.text()
        self.stop, self.nodeID = self.mesh.check_input_NodeID(lineEdit_nodeID, single_ID=True)
        if self.stop:
            return True           
        temp_nodeID_2 = self.nodeID

        if temp_nodeID_1 == temp_nodeID_2:
            title = "ERROR IN NODES SELECTION"
            message = "The selected nodes must differ. Try to choose another pair of nodes."
            PrintMessageInput([title, message, window_title1])
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
                    PrintMessageInput([title, message, window_title1])
                    return True
                else:
                    self.value = value
            except Exception:
                message = "You have typed an invalid value to the {}.".format(label)
                PrintMessageInput([title, message, window_title1])
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
            PrintMessageInput([title, message, window_title1])

    def constant_input_confirm(self):
        if self.check_all_inputs():
            return
        if self.parameters_K is not None:
            self.project.add_elastic_nodal_link_stiffness(self.nodeID_1, self.nodeID_2, self.parameters_K, False)
        if self.parameters_C is not None:
            self.project.add_elastic_nodal_link_damping(self.nodeID_1, self.nodeID_2, self.parameters_C, False)
        if (self.parameters_K or self.parameters_C) is not None:
            self.opv.updateRendererMesh()
            self.close()

    def load_table(self, lineEdit, text, header, direct_load=False):

        self.project.file.temp_table_name = None
        
        if direct_load:
            self.path_imported_table = lineEdit.text()
        else:
            self.basename = ""
            window_label = 'Choose a table to import the {} nodal load'.format(text)
            self.path_imported_table, _type = QFileDialog.getOpenFileName(None, window_label, self.userPath, 'Files (*.dat; *.csv)')
            lineEdit.setText(self.path_imported_table)

        if self.path_imported_table == "":
            return "", ""

        self.basename = os.path.basename(self.path_imported_table)
        if self.basename != "":
            self.imported_table_name = self.basename
        
        if "\\" in self.project_folder_path:
            self.new_load_path_table = "{}\\{}".format(self.project_folder_path, self.basename)
        elif "/" in self.project_folder_path:
            self.new_load_path_table = "{}/{}".format(self.project_folder_path, self.basename)

        try:                
            imported_file = np.loadtxt(self.path_imported_table, delimiter=",")
        except Exception as err:
            title = "ERROR WHILE LOADING {} TABLE".format(text)
            message = str(err)
            PrintMessageInput([title, message, window_title1])
            
        if imported_file.shape[1]<2:
            title = "ERROR WHILE LOADING {} TABLE".format(text)
            message = "The imported table has insufficient number of columns. The spectrum data must have only two columns to the frequencies and values."
            PrintMessageInput([title, message, window_title1])
            return
    
        try:
            self.imported_values = imported_file[:,1]
            if imported_file.shape[1]>=2:

                self.frequencies = imported_file[:,0]
                self.f_min = self.frequencies[0]
                self.f_max = self.frequencies[-1]
                self.f_step = self.frequencies[1] - self.frequencies[0] 
                self.project.set_frequencies(self.frequencies, self.f_min, self.f_max, self.f_step)
                self.imported_table = True
               
                data = np.array([self.frequencies, self.imported_values, np.zeros_like(self.frequencies)]).T
                np.savetxt(self.new_load_path_table, data, delimiter=",", header=header)

        except Exception as err:
            title = "ERROR WHILE LOADING {} TABLE".format(text)
            message = str(err)
            PrintMessageInput([title, message, window_title1])

        return self.imported_values, self.basename

    def load_Kx_table(self):
        header = "Kx || Frequency [Hz], Value [N/m]"
        self.Kx_table, self.basename_Kx = self.load_table(self.lineEdit_path_table_Kx, "Kx", header)

    def load_Ky_table(self):
        header = "Ky || Frequency [Hz], Value [N/m]"
        self.Ky_table, self.basename_Ky = self.load_table(self.lineEdit_path_table_Ky, "Ky", header)

    def load_Kz_table(self):
        header = "Kz || Frequency [Hz], Value [N/m]"
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
        header = "Crx || Frequency [Hz], value[N.m.s/rad]"
        self.Crx_table, self.basename_Crx = self.load_table(self.lineEdit_path_table_Crx, "Crx", header)

    def load_Cry_table(self):
        header = "Cry || Frequency [Hz], value[N.m.s/rad]"
        self.Cry_table, self.basename_Cry = self.load_table(self.lineEdit_path_table_Cry, "Cry", header)

    def load_Crz_table(self):
        header = "Crz || Frequency [Hz], value[N.m.s/rad]"
        self.Crz_table, self.basename_Crz = self.load_table(self.lineEdit_path_table_Crz, "Crz", header)

    def check_table_for_elastic_link_stiffness(self):

        Kx = Ky = Kz = None
        if self.lineEdit_path_table_Kx.text() != "":
            if self.Kx_table is None:
                header = "Kx || Frequency [Hz], Value [N/m]"
                Kx, self.basename_Kx = self.load_table(self.lineEdit_path_table_Kx, "Kx", header, direct_load=True)
            else:
                Kx = self.Kx_table
        
        if self.lineEdit_path_table_Ky.text() != "":
            if self.Ky_table is None:
                header = "Ky || Frequency [Hz], Value [N/m]"
                Ky, self.basename_Ky = self.load_table(self.lineEdit_path_table_Ky, "Ky", header, direct_load=True)                
            else:
                Ky = self.Ky_table

        if self.lineEdit_path_table_Kz.text() != "":
            if self.Kz_table is None:
                header = "Kz || Frequency [Hz], Value [N/m]"
                Kz, self.basename_Kz = self.load_table(self.lineEdit_path_table_Kz, "Kz", header, direct_load=True)                
            else:
                Kz = self.Kz_table

        Krx = Kry = Krz = None
        if self.lineEdit_path_table_Krx.text() != "":
            if self.Krx_table is None:
                header = "Krx || Frequency [Hz], Value [N.m/rad]"
                Krx, self.basename_Krx = self.load_table(self.lineEdit_path_table_Krx, "Krx", header, direct_load=True)
            else:
                Krx = self.Krx_table
        
        if self.lineEdit_path_table_Kry.text() != "":
            if self.Kry_table is None:
                header = "Kry || Frequency [Hz], Value [N.m/rad]"
                Kry, self.basename_Kry = self.load_table(self.lineEdit_path_table_Kry, "Kry", header, direct_load=True)            
            else:
                Kry = self.Kry_table
        
        if self.lineEdit_path_table_Krz.text() != "":
            if self.Krz_table is not None:
                header = "Krz || Frequency [Hz], Value [N.m/rad]"
                Krz, self.basename_Krz = self.load_table(self.lineEdit_path_table_Krz, "Krz", header, direct_load=True)            
            else:
                Krz = self.Krz_table
        
        stiffness_parameters = [Kx, Ky, Kz, Krx, Kry, Krz]

        if sum([1 if bc is not None else 0 for bc in stiffness_parameters]) != 0:
            self.flag_stiffness_parameters = True
            self.basenames = [self.basename_Kx, self.basename_Ky, self.basename_Kz, self.basename_Krx, self.basename_Kry, self.basename_Krz]
            self.stiffness_parameters = stiffness_parameters
            self.project.add_elastic_nodal_link_stiffness(self.nodeID_1, self.nodeID_2, self.stiffness_parameters, True, table_name=self.basenames)
            return False
        else:
            return True

    def check_table_for_elastic_link_damping(self):

        Cx = Cy = Cz = None
        if self.lineEdit_path_table_Cx.text() != "":
            if self.Cx_table is None:
                header = "Cx || Frequency [Hz], Value [N.s/m]"
                Cx, self.basename_Cx = self.load_table(self.lineEdit_path_table_Cx, "Cx", header, direct_load=True)            
            else:
                Cx = self.Cx_table
        
        if self.lineEdit_path_table_Cy.text() != "":
            if self.Cy_table is None:
                header = "Cy || Frequency [Hz], Value [N.s/m]"
                Cy, self.basename_Cy = self.load_table(self.lineEdit_path_table_Cy, "Cy", header, direct_load=True)
            else:
                Cy = self.Cy_table
        
        if self.lineEdit_path_table_Cz.text() != "":
            if self.Cz_table is None:
                header = "Cz || Frequency [Hz], Value [N.s/m]"
                Cz, self.basename_Cz = self.load_table(self.lineEdit_path_table_Cz, "Cz", header, direct_load=True)
            else:
                Cz = self.Cz_table

        Crx = Cry = Crz = None
        if self.lineEdit_path_table_Crx.text() != "":
            if self.Crx_table is None:
                header = "Crx || Frequency [Hz], Value [N.m.s/rad]"
                Crx, self.basename_Crx = self.load_table(self.lineEdit_path_table_Crx, "Crx", header, direct_load=True)
            else:
                Crx = self.Crx_table
        
        if self.lineEdit_path_table_Cry.text() != "":
            if self.Cry_table is None:
                header = "Cry || Frequency [Hz], Value [N.m.s/rad]"
                Cry, self.basename_Cry = self.load_table(self.lineEdit_path_table_Cry, "Cry", header, direct_load=True)
            else:
                Cry = self.Cry_table
        
        if self.lineEdit_path_table_Crz.text() != "":
            if self.Crz_table is None:
                header = "Crz || Frequency [Hz], Value [N.m.s/rad]"
                Crz, self.basename_Crz = self.load_table(self.lineEdit_path_table_Crz, "Crz", header, direct_load=True)
            else:
                Crz = self.Crz_table
                    
        damping_parameters = [Cx, Cy, Cz, Crx, Cry, Crz]

        if sum([1 if bc is not None else 0 for bc in damping_parameters]) != 0:
            self.flag_damping_parameters = True
            self.basenames = [self.basename_Cx, self.basename_Cy, self.basename_Cz, self.basename_Crx, self.basename_Cry, self.basename_Crz]
            self.damping_parameters = damping_parameters
            self.project.add_elastic_nodal_link_damping(self.nodeID_1, self.nodeID_2, self.damping_parameters, True, table_name=self.basenames)
            return False
        else:
            return True
  
    def table_input_confirm(self):

        if self.check_all_nodes():
            return True

        if self.check_table_for_elastic_link_stiffness() and self.check_table_for_elastic_link_damping():
            title = 'NONE TABLE SELECTED FOR STIFFNESS OR DAMPING'
            message = 'Please, define at least a table of values to the stiffness or damping before confirming the attribution.'
            PrintMessageInput([title, message, window_title1])
            return

        if not (self.flag_stiffness_parameters or self.flag_damping_parameters):
            title = "ERROR"
            message = "You must to add at least one external element before confirm the input!"
            PrintMessageInput([title, message, window_title1])
            return
        
        self.opv.updateRendererMesh()
        self.close()

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

        for key in self.mesh.dict_nodes_with_elastic_link_stiffness.keys():
            node_ids = [int(node) for node in key.split("-")]
            mask, _ = self.project.mesh.nodes[node_ids[0]].elastic_nodal_link_stiffness[key]
            new = QTreeWidgetItem([key, str(self.text_label(mask, stiffness_labels))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_nodal_links_stiffness.addTopLevelItem(new)

        if len(self.mesh.dict_nodes_with_elastic_link_stiffness) == 0:
            self.pushButton_remove_link_stiffness.setDisabled(True)

    def load_elastic_links_damping_info(self):

        self.treeWidget_nodal_links_damping.clear()
        damping_labels = np.array(['c_x','c_y','c_z','c_rx','c_ry','c_rz']) 
        self.skip_treeWidget_row(self.treeWidget_nodal_links_damping)
        self.pushButton_remove_link_damping.setDisabled(False)

        for key in self.mesh.dict_nodes_with_elastic_link_damping.keys():
            node_ids = [int(node) for node in key.split("-")]
            mask, _ = self.project.mesh.nodes[node_ids[0]].elastic_nodal_link_damping[key]
            new = QTreeWidgetItem([key, str(self.text_label(mask, damping_labels))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_nodal_links_damping.addTopLevelItem(new)

        if len(self.mesh.dict_nodes_with_elastic_link_damping) == 0:
            self.pushButton_remove_link_damping.setDisabled(True)

    def on_click_item(self, item):
        self.lineEdit_node_ID_info.setText(item.text(0))

    def get_information(self):
        try:
            selected_link = self.lineEdit_node_ID_info.text()
            if selected_link != "":        
                GetInformationOfGroup(self.project, selected_link, "Lines")
            else:
                title = "UNSELECTED ELASTIC LINK"
                message = "Please, select an elastic link in the list to get the information."
                PrintMessageInput([title, message, window_title2])
                
        except Exception as e:
            title = "ERROR WHILE GETTING INFORMATION OF SELECTED ELASTIC LINK"
            message = str(e)
            PrintMessageInput([title, message, window_title1])

    def remove_table_files(self, values):          
        for value in values:
            if value != 'None' and ".dat" in value:
                self.get_path_of_selected_table(value)
                try:
                    os.remove(self.path_of_selected_table)
                except:
                    pass

    def remove_elastic_link_stiffness_from_file(self, section_key):

        path = self.project.file._node_structural_path
        config = configparser.ConfigParser()
        config.read(path)

        keys = list(config[section_key].keys())
        if "connecting stiffness" in keys and "connecting torsional stiffness" in keys:
            values_stiffness = config[section_key]["connecting stiffness"][1:-1].split(",")
            self.remove_table_files(values_stiffness)
            values_torsional_stiffness = config[section_key]["connecting torsional stiffness"][1:-1].split(",")
            self.remove_table_files(values_torsional_stiffness)
            config.remove_option(section=section_key, option="connecting stiffness")
            config.remove_option(section=section_key, option="connecting torsional stiffness")
            if len(list(config[section_key].keys())) == 0:
                config.remove_section(section=section_key)
        with open(path, 'w') as config_file:
            config.write(config_file)

    def remove_elastic_link_damping_from_file(self, section_key):

        path = self.project.file._node_structural_path
        config = configparser.ConfigParser()
        config.read(path)        

        keys = list(config[section_key].keys())
        if "connecting damping" in keys and "connecting torsional damping" in keys:
            values_damping = config[section_key]["connecting damping"][1:-1].split(",")
            self.remove_table_files(values_damping)
            values_torsional_damping = config[section_key]["connecting torsional damping"][1:-1].split(",")
            self.remove_table_files(values_torsional_damping)
            config.remove_option(section=section_key, option="connecting damping")
            config.remove_option(section=section_key, option="connecting torsional damping")
            if len(list(config[section_key].keys())) == 0:
                config.remove_section(section=section_key)    
        with open(path, 'w') as config_file:
            config.write(config_file)

    def remove_selected_link_stiffness(self):
        if self.ext_key is None:
            key = self.lineEdit_node_ID_info.text()
        else:
            key = self.ext_key
        if key == "":
            title = "EMPTY SELECTION IN ELASTIC LINK REMOVAL"
            message = "Please, select a stiffness elastic link in the list before confirm the link removal."
            PrintMessageInput([title, message, window_title2])
            return

        node_IDs = [int(nodeID) for nodeID in key.split("-")]

        if key in self.project.mesh.dict_nodes_with_elastic_link_stiffness.keys():
            self.project.mesh.dict_nodes_with_elastic_link_stiffness.pop(key)
            for node_ID in node_IDs:
                self.nodes[node_ID].elastic_nodal_link_stiffness.pop(key)
            self.remove_elastic_link_stiffness_from_file(key)
            self.load_elastic_links_stiffness_info()
            self.opv.updateRendererMesh()
            self.lineEdit_node_ID_info.setText("")
        else:
            title = "REMOVAL OF ELASTIC NODAL LINKS - STIFFNESS"
            message = "The selected elastic link is invalid thus cannot be removed."
            PrintMessageInput([title, message, window_title1])

    def remove_selected_link_damping(self):
        if self.ext_key is None:
            key = self.lineEdit_node_ID_info.text()
        else:
            key = self.ext_key
        if key == "":
            title = "EMPTY SELECTION IN ELASTIC LINK REMOVAL"
            message = "Please, select a damping elastic link in the list before confirm the link removal."
            PrintMessageInput([title, message, window_title2])
            return

        node_IDs = [int(nodeID) for nodeID in key.split("-")]

        if key in self.project.mesh.dict_nodes_with_elastic_link_damping.keys():
            self.project.mesh.dict_nodes_with_elastic_link_damping.pop(key)
            for node_ID in node_IDs:
                self.nodes[node_ID].elastic_nodal_link_damping.pop(key)
            self.remove_elastic_link_damping_from_file(key)
            self.load_elastic_links_damping_info()
            self.opv.updateRendererMesh()
            self.lineEdit_node_ID_info.setText("")
        else:
            title = "REMOVAL OF ELASTIC NODAL LINKS - DAMPING"
            message = "The selected elastic link are invalid thus cannot be removed."
            PrintMessageInput([title, message, window_title2])

    def reset_all(self):
        if self.double_confirm_action():
            return
        temp_dict_stiffness = self.project.mesh.dict_nodes_with_elastic_link_stiffness.copy()
        temp_dict_damping = self.project.mesh.dict_nodes_with_elastic_link_damping.copy()
        for key in temp_dict_stiffness.keys():
            self.ext_key = key
            self.remove_selected_link_stiffness()
        for key in temp_dict_damping.keys():
            self.ext_key = key
            self.remove_selected_link_damping()
        title = "RESET OF ELASTIC NODAL LINKS"
        message = "All elastic nodal links have been removed from the model."
        PrintMessageInput([title, message, window_title1])
        self.ext_key = None

    def double_confirm_action(self):
        confirm_act = QMessageBox.question(
            self,
            "QUIT",
            "Are you sure you want to remove all elastic links attributed to the structural model?",
            QMessageBox.No | QMessageBox.Yes)
        
        if confirm_act == QMessageBox.Yes:
            return False
        else:
            return True

    def get_path_of_selected_table(self, selected_table):
        if "\\" in self.project_folder_path:
            self.path_of_selected_table = "{}\\{}".format(self.project_folder_path, selected_table)
        elif "/" in self.project_folder_path:
            self.path_of_selected_table = "{}/{}".format(self.project_folder_path, selected_table)

    def force_to_close(self):
        self.close()

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
        self.nodes = project.mesh.nodes
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
        self.dict_lines_parameters = self.project.mesh.dict_lines_with_stress_stiffening
        self.dict_elements_parameters = self.project.mesh.group_elements_with_stress_stiffening

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
            mask_damping, _ = self.nodes[self.node_IDs[0]].elastic_nodal_link_damping[self.selected_link]
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