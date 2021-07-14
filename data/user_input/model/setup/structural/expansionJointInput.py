from re import M
from PyQt5.QtWidgets import QLineEdit, QDialog, QFileDialog, QTreeWidget, QTreeWidgetItem, QTabWidget, QPushButton, QLabel, QComboBox, QWidget, QToolButton, QMessageBox, QRadioButton
from os.path import basename
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import uic, QtCore
import configparser
from collections import defaultdict
import os
import numpy as np
import matplotlib.pyplot as plt  

from pulse.preprocessing.compressor_model import CompressorModel
from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.before_run import BeforeRun
from data.user_input.project.printMessageInput import PrintMessageInput

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"

class ClickableLineEdit(QLineEdit):
    
    def __init__(self, *args):
        super().__init__(*args)
       
        # self.setFixedWidth(100)
        # self.setFixedHeight(26)
        # self.setAlignment(Qt.AlignHCenter)
        # self.setStyleSheet("color:red")
        # self.set_font()        
        
    def set_font(self):
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setFamily("Arial")
        font.setWeight(81)
        self.setFont(font)

    def mousePressEvent(self, event):
        self.clicked.emit()

class ExpansionJointInput(QDialog):
    def __init__(self, project,  opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Model/Setup/Structural/expansionJointInput.ui', self)
        
        clicked = QtCore.pyqtSignal()

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)
        self.node_id = self.opv.getListPickedPoints()
        self.line_id = self.opv.getListPickedEntities()
        self.element_id = self.opv.getListPickedElements()

        self.project = project
        self.mesh = project.mesh
        self.before_run = self.mesh.get_model_checks()
        self.nodes = self.project.mesh.nodes
        
        self.structural_elements = self.project.mesh.structural_elements
        self.dict_tag_to_entity = self.project.mesh.dict_tag_to_entity

        self.project_folder_path = project.project_folder_path 
        self.userPath = os.path.expanduser('~')       
        self.stop = False
        self.complete = False
        self.aquisition_parameters_processed = False
        self.node_ID_remove = None
        self.ext_key = None

        self.label_selected_id = self.findChild(QLabel, 'label_selected_id')
        
        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
        self.lineEdit_effective_diameter = self.findChild(QLineEdit, 'lineEdit_effective_diameter')
        self.lineEdit_joint_mass = self.findChild(QLineEdit, 'lineEdit_joint_mass')
        self.lineEdit_joint_length = self.findChild(QLineEdit, 'lineEdit_joint_length')
        self.lineEdit_axial_locking_criteria = self.findChild(QLineEdit, 'lineEdit_axial_locking_criteria')

        self.lineEdit_axial_stiffness = self.findChild(QLineEdit, 'lineEdit_axial_stiffness')
        self.lineEdit_transversal_stiffness = self.findChild(QLineEdit, 'lineEdit_transversal_stiffness')
        self.lineEdit_torsional_stiffness = self.findChild(QLineEdit, 'lineEdit_torsional_stiffness')
        self.lineEdit_angular_stiffness = self.findChild(QLineEdit, 'lineEdit_angular_stiffness')

        self.lineEdit_path_table_axial_stiffness = self.findChild(QLineEdit, 'lineEdit_path_table_axial_stiffness')
        self.lineEdit_path_table_transversal_stiffness = self.findChild(QLineEdit, 'lineEdit_path_table_transversal_stiffness')
        self.lineEdit_path_table_torsional_stiffness = self.findChild(QLineEdit, 'lineEdit_path_table_torsional_stiffness')
        self.lineEdit_path_table_angular_stiffness = self.findChild(QLineEdit, 'lineEdit_path_table_angular_stiffness')

        self.toolButton_load_table_axial_stiffness = self.findChild(QToolButton, 'toolButton_load_table_axial_stiffness')
        self.toolButton_load_table_transversal_stiffness = self.findChild(QToolButton, 'toolButton_load_table_transversal_stiffness')
        self.toolButton_load_table_torsional_stiffness = self.findChild(QToolButton, 'toolButton_load_table_torsional_stiffness')
        self.toolButton_load_table_angular_stiffness = self.findChild(QToolButton, 'toolButton_load_table_angular_stiffness')

        self.toolButton_load_table_axial_stiffness.clicked.connect(self.load_Kx_table)
        self.toolButton_load_table_transversal_stiffness.clicked.connect(self.load_Kyz_table)
        self.toolButton_load_table_torsional_stiffness.clicked.connect(self.load_Krx_table)
        self.toolButton_load_table_angular_stiffness.clicked.connect(self.load_Kryz_table)

        self.Kx_table = None
        self.Kyz_table = None
        self.Krx_table = None
        self.Kryz_table = None
        
        self.basename_Kx = None
        self.basename_Kyz = None
        self.basename_Krx = None
        self.basename_Kryz = None

        self.flag_stiffness_parameters = False
        self.flag_damping_parameters = False

        self.radioButton_line_selection = self.findChild(QRadioButton, 'radioButton_line_selection')
        self.radioButton_node_selection = self.findChild(QRadioButton, 'radioButton_node_selection')
        self.radioButton_element_selection = self.findChild(QRadioButton, 'radioButton_element_selection')
        self.radioButton_line_selection.clicked.connect(self.radioButtonEvent_selection_type)
        self.radioButton_node_selection.clicked.connect(self.radioButtonEvent_selection_type)
        self.radioButton_element_selection.clicked.connect(self.radioButtonEvent_selection_type)
        self.selection_by_line = self.radioButton_line_selection.isChecked()
        self.selection_by_node = self.radioButton_node_selection.isChecked()
        self.selection_by_element = self.radioButton_element_selection.isChecked()
        self.previous_flag = self.selection_by_line
        
        self.radioButton_add_rods = self.findChild(QRadioButton, 'radioButton_add_rods')
        self.radioButton_not_add_rods = self.findChild(QRadioButton, 'radioButton_not_add_rods')
        self.radioButton_add_rods.clicked.connect(self.radioButtonEvent_rods)
        self.radioButton_not_add_rods.clicked.connect(self.radioButtonEvent_rods)
        self.add_rods = self.radioButton_add_rods.isChecked()

        self.pushButton_constant_input_confirm = self.findChild(QPushButton, 'pushButton_constant_input_confirm')
        self.pushButton_constant_input_confirm.clicked.connect(self.constant_input_confirm)

        self.pushButton_table_input_confirm = self.findChild(QPushButton, 'pushButton_table_input_confirm')
        self.pushButton_table_input_confirm.clicked.connect(self.table_input_confirm)

        # self.pushButton_remove_link_stiffness = self.findChild(QPushButton, 'pushButton_remove_link_stiffness')
        # self.pushButton_remove_link_stiffness.clicked.connect(self.remove_selected_link_stiffness)

        # self.pushButton_remove_link_damping = self.findChild(QPushButton, 'pushButton_remove_link_damping')
        # self.pushButton_remove_link_damping.clicked.connect(self.remove_selected_link_damping)

        # self.pushButton_see_details_selected_link = self.findChild(QPushButton, 'pushButton_see_details_selected_link')
        # self.pushButton_see_details_selected_link.clicked.connect(self.get_information)

        # self.pushButton_reset_all = self.findChild(QPushButton, 'pushButton_reset_all')
        # self.pushButton_reset_all.clicked.connect(self.reset_all)

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.force_to_close)

        self.pushButton_get_length = self.findChild(QPushButton, 'pushButton_get_length')
        self.pushButton_get_length.clicked.connect(self.get_length)

        # self.pushButton_get_length.clicked.connect(self.force_to_close)

        # self.tabWidget_main = self.findChild(QTabWidget, 'tabWidget_main')
        # self.tabWidget_main.currentChanged.connect(self.tabEvent_selection_type)
        # self.current_tab_selection_type = self.tabWidget_main.currentIndex()
        # self.tab_setup = self.findChild(QWidget, "tab_setup")
        # self.tab_remove = self.findChild(QWidget, "tab_remove")
  
        self.lineEdit_node_ID_info = self.findChild(QLineEdit, 'lineEdit_node_ID_info')
        # self.lineEdit_parameters_info = self.findChild(QLineEdit, 'lineEdit_parameters_info')

        # self.treeWidget_nodal_links_stiffness = self.findChild(QTreeWidget, 'treeWidget_nodal_links_stiffness')
        # self.treeWidget_nodal_links_stiffness.setColumnWidth(0, 120)
        # self.treeWidget_nodal_links_stiffness.itemClicked.connect(self.on_click_item)
        # self.treeWidget_nodal_links_stiffness.headerItem().setTextAlignment(0, Qt.AlignCenter)
        # self.treeWidget_nodal_links_stiffness.headerItem().setTextAlignment(1, Qt.AlignCenter)

        # self.treeWidget_nodal_links_damping = self.findChild(QTreeWidget, 'treeWidget_nodal_links_damping')
        # self.treeWidget_nodal_links_damping.setColumnWidth(0, 120)
        # self.treeWidget_nodal_links_damping.itemClicked.connect(self.on_click_item)
        # self.treeWidget_nodal_links_damping.headerItem().setTextAlignment(0, Qt.AlignCenter)
        # self.treeWidget_nodal_links_damping.headerItem().setTextAlignment(1, Qt.AlignCenter)

        self.update()
        # self.write_id(self.opv.getListPickedPoints())
        # self.load_elastic_links_stiffness_info()
        # self.load_elastic_links_damping_info()
        self.exec_()

    # def mousePressEvent(self, event):
    #     clicked = QtCore.pyqtSignal()
    #     # self.lineEdit_axial_stiffness.clicked.emit()
    #     print(event)
        # self.lineEdit_axial_stiffness.clicked.connect(self.print_message)

    # def print_message(self):
    #     print("Alguma mensagem deve ser printada!")
    
    def get_length(self):
        lineEdit_lineID = self.lineEdit_selected_ID.text()
        if lineEdit_lineID != "":
            self.stop, self.line_id = self.before_run.check_input_LineID(lineEdit_lineID, single_ID=True)
            if self.stop:
                self.lineEdit_selected_ID.setText("")
                self.lineEdit_joint_length.setText("")
                self.lineEdit_selected_ID.setFocus()
                return True  
            length = self.mesh.get_line_length(self.line_id) 
            self.lineEdit_joint_length.setText(str(round(length,8)))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_inputs.currentIndex() == 0:
                self.constant_input_confirm()
            elif self.tabWidget_inputs.currentIndex() == 1: 
                self.table_input_confirm() 
        if event.key() == Qt.Key_Escape:
            self.close()

    def write_id(self, selected_id):
        self.lineEdit_selected_ID.setText(str(selected_id[0]))

    def update(self):

        self.update_selected_id()
        self.update_selection_lineEdit_visibility()
        
        if self.line_id != []:
            self.write_id(self.line_id)
            self.radioButton_line_selection.setChecked(True)
            length = self.mesh.get_line_length(self.line_id[0])
            self.lineEdit_joint_length.setText(str(round(length,8)))
        
        elif self.node_id != []:
            self.write_id(self.node_id)
            self.radioButton_node_selection.setChecked(True)
          
        elif self.element_id != []:
            self.write_id(self.element_id)
            self.radioButton_element_selection.setChecked(True)
        self.load_input_fields()
        

    def update_get_length_button_visibility(self):
        if self.selection_by_line:
            self.pushButton_get_length.setVisible(True)
        else:
            if self.line_id == []:
                self.pushButton_get_length.setVisible(False)      

    def update_selected_id(self):
        
        self.node_id = self.opv.getListPickedPoints()
        self.line_id = self.opv.getListPickedEntities()
        self.element_id = self.opv.getListPickedElements()
        
        if self.previous_flag:
            if self.node_id != [] or self.element_id != []:
                self.lineEdit_joint_length.setText("")
                self.lineEdit_joint_length.setEnabled(True)
            if not self.selection_by_line and self.line_id == []:
                self.lineEdit_joint_length.setText("")
                self.lineEdit_joint_length.setEnabled(True)
        
        elif self.selection_by_line:
            if self.node_id == [] or self.element_id == []:
                self.lineEdit_joint_length.setEnabled(False)

        self.previous_flag = self.selection_by_line
    
    def update_selection_lineEdit_visibility(self):

        if self.line_id != []:
            self.label_selected_id.setText("Line ID:")
            self.lineEdit_selected_ID.setText("")
            self.radioButton_line_selection.setChecked(True)
        
        elif self.node_id != []:
            self.label_selected_id.setText("Node ID:")
            self.radioButton_node_selection.setChecked(True)

        elif self.element_id != []:
            self.label_selected_id.setText("Element ID:")
            self.radioButton_element_selection.setChecked(True)

    def update_selection_flags(self):
        self.selection_by_line = self.radioButton_line_selection.isChecked()
        self.selection_by_node = self.radioButton_node_selection.isChecked()
        self.selection_by_element = self.radioButton_element_selection.isChecked()
        self.update_get_length_button_visibility()

    def radioButtonEvent_selection_type(self):   

        self.update_selection_flags()
        self.update_selected_id()
        self.update_selection_lineEdit_visibility()

        if self.line_id != []:
            self.write_id(self.line_id)
            
        elif self.node_id != []:
            self.write_id(self.node_id)
                    
        elif self.element_id != []:
            self.write_id(self.element_id)     

        else:
            self.lineEdit_selected_ID.setText("")       

    def radioButtonEvent_rods(self):
        self.add_rods = self.radioButton_add_rods.isChecked()

    def tabEvent_selection_type(self):
        self.current_tab_selection_type = self.tabWidget_selection_type.currentIndex()

    def check_selection_type(self):

        if self.selection_by_line:
            
            lineEdit_lineID = self.lineEdit_selected_ID.text()
            self.stop, self.lineID = self.before_run.check_input_LineID(lineEdit_lineID, single_ID=True)
            if self.stop:
                self.lineEdit_selected_ID.setText("")
                self.lineEdit_joint_length.setText("")
                self.lineEdit_selected_ID.setFocus()
                return True
            self.get_length()
        
        elif self.selection_by_node:  

            lineEdit_nodeID = self.lineEdit_selected_ID.text()
            self.stop, self.nodeID = self.before_run.check_input_NodeID(lineEdit_nodeID, single_ID=True)
            if self.stop:
                return True

        elif self.selection_by_element:

            lineEdit_elementID = self.lineEdit_selected_ID.text()
            self.stop, self.elementID = self.before_run.check_input_ElementID(lineEdit_elementID, single_ID=True)
            if self.stop:
                return True

        return False

    def reset_all_lineEdits(self):
        self.lineEdit_joint_length.setText("")
        self.lineEdit_effective_diameter.setText("")
        self.lineEdit_joint_mass.setText("")
        self.lineEdit_axial_locking_criteria.setText("")
        self.lineEdit_axial_stiffness.setText("")
        self.lineEdit_transversal_stiffness.setText("")
        self.lineEdit_torsional_stiffness.setText("")
        self.lineEdit_angular_stiffness.setText("")

    def load_input_fields(self):
        if self.line_id == []:
            self.reset_all_lineEdits()
        else:    
            entity = self.dict_tag_to_entity[self.line_id[0]]
            if entity.expansion_joint_parameters is None:
                return

            [read_parameters, read_stiffness]  = entity.expansion_joint_parameters
          
            # if isinstance(_parameters, list):
            #     read_parameters = _parameters

            try:
                self.lineEdit_joint_length.setText(str(read_parameters[0]))
                self.lineEdit_effective_diameter.setText(str(read_parameters[1]))
                self.lineEdit_joint_mass.setText(str(read_parameters[2]))
                self.lineEdit_axial_locking_criteria.setText(str(read_parameters[3]))
                if read_parameters[4] == 1:
                    self.radioButton_add_rods.setChecked(True)
                elif read_parameters[4] == 0:
                    self.radioButton_add_rods.setChecked(False) 
                
                if isinstance(read_stiffness[0], np.ndarray):
                    pass
                else:
                    self.lineEdit_axial_stiffness.setText(str(read_stiffness[0]))
                
                if isinstance(read_stiffness[1], np.ndarray):
                    pass
                else:    
                    self.lineEdit_transversal_stiffness.setText(str(read_stiffness[1]))
                
                if isinstance(read_stiffness[2], np.ndarray):
                    pass
                else:                
                    self.lineEdit_torsional_stiffness.setText(str(read_stiffness[2]))
                
                if isinstance(read_stiffness[3], np.ndarray):
                    pass
                else:
                    self.lineEdit_angular_stiffness.setText(str(read_stiffness[3]))

            except Exception as _log_error:
                title = "Error while loading info from entity"
                message = str(_log_error)
                PrintMessageInput([title, message, window_title1])
        pass

    # def check_input_length(self):
    #     try:

    #         self.length = float(self.lineEdit_joint_length.text())
            
    #     except Exception as log_error:
    #         title = "Invalid value to the joint length"
    #         message = "An invalid value has been typed to the joint length."
    #         message += "The input value must be a positive float number.\n\n"
    #         message += f"{str(log_error)}"
    #         PrintMessageInput([title, message, window_title1])

    def get_nodes_elements_according_joint_length(self):
        if self.selection_by_node:
            self.list_nodes, self.list_elements = self.mesh.get_neighbor_nodes_and_elements_by_node(self.nodeID, self.length)
        elif self.selection_by_element:
            self.list_nodes, self.list_elements = self.mesh.get_neighbor_nodes_and_elements_by_element(self.elementID, self.length)

    def check_input_parameters(self, lineEdit, label, _float=True):
        message = ""
        title = f"Invalid entry to the '{label}'"
        value_string = lineEdit.text()
        if value_string != "":
            try:
                if _float:
                    value = float(value_string)
                else:
                    value = int(value_string) 
                if value <= 0:
                    message = f"You cannot input a non-positive value to the '{label}'."
                else:
                    self.value = value
            except Exception as _log_error:
                message = f"You have typed an invalid value to the '{label}' input field."
                message += "The input value should be a positive float number.\n\n"
                message += f"{str(_log_error)}"
        else:
            message = f"An empty entry has been detected at the '{label}' input field.\n\n" 
            message += "You should to enter a positive value to proceed."
            self.value = None
        if message != "":
            PrintMessageInput([title, message, window_title1])
            return True
        else:
            return False
    
    def check_initial_inputs(self):

        self.list_parameters = []
                
        if self.check_selection_type():
            return True
            
        if self.check_input_parameters(self.lineEdit_joint_length, 'Joint length'):
            self.lineEdit_joint_length.setFocus()
            return True
        else:
            self.joint_length = self.value

        if self.check_input_parameters(self.lineEdit_effective_diameter, 'Effective diameter'):
            self.lineEdit_effective_diameter.setFocus()
            return True
        else:
            self.effective_diameter = self.value
        
        if self.check_input_parameters(self.lineEdit_joint_mass, 'Joint mass'):
            self.lineEdit_joint_mass.setFocus()
            return True
        else:
            self.joint_mass = self.value

        if self.check_input_parameters(self.lineEdit_axial_locking_criteria, 'Axial locking criteria'):
            self.lineEdit_axial_locking_criteria.setFocus()
            return True
        else:
            self.axial_locking_criteria = self.value

        self.add_rods_key = int(self.add_rods)
        self.list_parameters =  [   self.joint_length,
                                    self.effective_diameter,  
                                    self.joint_mass, 
                                    self.axial_locking_criteria,
                                    self.add_rods_key    ]

    def check_constant_values_to_stiffness(self):
        self.list_stiffness = []       
        if self.check_input_parameters(self.lineEdit_axial_stiffness, 'Axial stiffness'):
            self.lineEdit_axial_stiffness.setFocus()
            return True
        else:
            self.list_stiffness.append(self.value)

        if self.check_input_parameters(self.lineEdit_transversal_stiffness, 'Transversal stiffness'):
            self.lineEdit_transversal_stiffness.setFocus()
            return True
        else:
            self.list_stiffness.append(self.value)

        if self.check_input_parameters(self.lineEdit_torsional_stiffness, 'Torsional stiffness'):
            self.lineEdit_torsional_stiffness.setFocus()
            return True
        else:
            self.list_stiffness.append(self.value)

        if self.check_input_parameters(self.lineEdit_angular_stiffness, 'Angular stiffness'):
            self.lineEdit_angular_stiffness.setFocus()
            return True
        else:
            self.list_stiffness.append(self.value)

        # list_stiffness_parameters = [Kx, Kyz, Krx, Kryz]
                
        # if len(list_stiffness_parameters) == 4:
        #     for _value in list_stiffness_parameters:
        #         self.list_parameters.append(_value)
        #     return False
        # else:
        #     return True

    def constant_input_confirm(self):
        
        if self.check_initial_inputs():
            return
        
        if self.check_constant_values_to_stiffness():
            return

        self.all_parameters = [self.list_parameters, self.list_stiffness]

        # if self.list_parameters != []:
            
        if self.selection_by_line:

            self.project.set_cross_section_by_line(self.lineID, None)

            self.list_elements = self.project.mesh.line_to_elements[self.lineID]
            list_cross = get_list_cross_sections_to_plot_expansion_joint(   self.list_elements, 
                                                                            self.effective_diameter )
            
            self.project.mesh.set_cross_section_by_element(self.list_elements, list_cross)
            self.project.add_expansion_joint_by_line(self.lineID, self.all_parameters, False)
            self.opv.updatePlots()
            self.opv.changePlotToEntitiesWithCrossSection()
        else:
            return
            self.project.add_expansion_joint_by_elements(self.list_elements, self.all_parameters, False)
        # self.opv.updateRendererMesh()
        self.close()
        # else:
        #     title = 'EMPTY INPUTS FOR EXPASION JOINT STIFFNESS'
        #     message = 'Please insert at least a stiffness value value to proceed.'
        #     PrintMessageInput([title, message, window_title1])

    # def get_parameters(self):
    #     [   effective_diameter,
    #         joint_length,
    #         joint_mass,
    #         axial_locking_criteria,
    #         add_rods_key,  
    #         axial_stiffness,
    #         transversal_stiffness,
    #         torsional_stiffness,
    #         angular_stiffness   ] = self.list_parameters

    #     data =  {   "joint_length" : joint_length,   
    #                 "effective_diameter" : effective_diameter, 
    #                 "joint_mass" : joint_mass,
    #                 "axial_locking_criteria" : axial_locking_criteria,
    #                 "rods_included" : add_rods_key,
    #                 "axial_stiffness" : axial_stiffness,
    #                 "transversal_stiffness" : transversal_stiffness,
    #                 "torsional_stiffness" : torsional_stiffness,
    #                 "angular_stiffness" : angular_stiffness }
    #     return data

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
            message = "The imported table has insufficient number of columns. The spectrum"
            message += " data must have only two columns to the frequencies and values."
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
        label = "Axial stiffness"
        header = f"{label} || Frequency [Hz], Value [N/m]"
        self.Kx_table, self.basename_Kx = self.load_table(self.lineEdit_path_table_axial_stiffness, label, header)

    def load_Kyz_table(self):
        label = "Transversal stiffness"
        header = f"{label} || Frequency [Hz], Value [N/m]"
        self.Kyz_table, self.basename_Kyz = self.load_table(self.lineEdit_path_table_transversal_stiffness, label, header)

    def load_Krx_table(self):
        label = "Torsional stiffness"
        header = f"{label} || Frequency [Hz], Value [N.m/rad]"
        self.Krx_table, self.basename_Krx = self.load_table(self.lineEdit_path_table_torsional_stiffness, label, header)

    def load_Kryz_table(self):
        label = "Angular stiffness"
        header = f"{label} || Frequency [Hz], Value [N.m/rad]"
        self.Kryz_table, self.basename_Kryz = self.load_table(self.lineEdit_path_table_angular_stiffness, label, header)

    def check_table_of_values(self):

        self.loaded_stiffness = None
        
        Kx = Kyz = Krx = Kryz = None
        if self.lineEdit_path_table_axial_stiffness.text() != "":
            if self.Kx_table is None:
                label = "Axial stiffness"
                header = f"{label} || Frequency [Hz], Value [N/m]"
                lineEdit = self.lineEdit_path_table_axial_stiffness
                Kx, self.basename_Kx = self.load_table(lineEdit, label, header, direct_load=True)
            else:
                Kx = self.Kx_table

        if self.lineEdit_path_table_transversal_stiffness.text() != "":
            if self.Kyz_table is None:
                label = "Transversal stiffness"
                header = f"{label} || Frequency [Hz], Value [N/m]"
                lineEdit = self.lineEdit_path_table_transversal_stiffness
                Kyz, self.basename_Kyz = self.load_table(lineEdit, label, header, direct_load=True)
            else:
                Kyz = self.Kyz_table

        if self.lineEdit_path_table_torsional_stiffness.text() != "":
            if self.Krx_table is None:
                label = "Torsional stiffness"
                header = f"{label} || Frequency [Hz], Value [N.m/m]"
                lineEdit = self.lineEdit_path_table_torsional_stiffness
                Krx, self.basename_Krx = self.load_table(lineEdit, label, header, direct_load=True)
            else:
                Krx = self.Krx_table

        if self.lineEdit_path_table_angular_stiffness.text() != "":
            if self.Kryz_table is None:
                label = "Angular stiffness"
                header = f"{label} || Frequency [Hz], Value [N.m/m]"
                lineEdit = self.lineEdit_path_table_angular_stiffness
                Kryz, self.basename_Kryz = self.load_table(lineEdit, label, header, direct_load=True)
            else:
                Kryz = self.Kryz_table

        self.labels = ["Axial stiffness", "Transversal stiffness", "Torsional stiffness", "Angular stiffness"]
        self.loaded_stiffness_tables = [Kx, Kyz, Krx, Kryz]

        if None in self.loaded_stiffness_tables:
            list_labels = []
            for index, value in enumerate(self.loaded_stiffness_tables):
                if value is None:
                    list_labels.append(self.labels[index])

            title = 'NONE TABLE SELECTED FOR STIFFNESS'
            message = f"Please, define at least one table of values to the:\n\n {list_labels} \n\n"
            message += "before confirming the attribution."
            PrintMessageInput([title, message, window_title1])
            return True
        else:
            self.basenames = [  self.basename_Kx, self.basename_Kyz, 
                                self.basename_Krx, self.basename_Kryz   ]    
            return False


    def table_input_confirm(self):

        if self.check_initial_inputs():
            return

        if self.check_table_of_values():
            return

        self.all_parameters = [self.list_parameters, self.list_stiffness]
        if self.selection_by_line:
            self.project.add_expansion_joint_by_line(self.lineID, self.all_parameters, True, self.basenames)
            self.opv.updatePlots()
            self.opv.changePlotToEntitiesWithCrossSection()
        else:
            return
            self.project.add_expansion_joint_by_elements(self.list_elements, self.all_parameters, True, self.basenames)
        
        # self.opv.updateRendererMesh()
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

    # def load_elastic_links_stiffness_info(self):

    #     self.treeWidget_nodal_links_stiffness.clear()
    #     stiffness_labels = np.array(['k_x','k_y','k_z','k_rx','k_ry','k_rz']) 
    #     self.skip_treeWidget_row(self.treeWidget_nodal_links_stiffness)
    #     self.pushButton_remove_link_stiffness.setDisabled(False)

    #     for key in self.mesh.dict_nodes_with_elastic_link_stiffness.keys():
    #         node_ids = [int(node) for node in key.split("-")]
    #         mask, _ = self.project.mesh.nodes[node_ids[0]].elastic_nodal_link_stiffness[key]
    #         new = QTreeWidgetItem([key, str(self.text_label(mask, stiffness_labels))])
    #         new.setTextAlignment(0, Qt.AlignCenter)
    #         new.setTextAlignment(1, Qt.AlignCenter)
    #         self.treeWidget_nodal_links_stiffness.addTopLevelItem(new)

    #     if len(self.mesh.dict_nodes_with_elastic_link_stiffness) == 0:
    #         self.pushButton_remove_link_stiffness.setDisabled(True)

    # def load_elastic_links_damping_info(self):

    #     self.treeWidget_nodal_links_damping.clear()
    #     damping_labels = np.array(['c_x','c_y','c_z','c_rx','c_ry','c_rz']) 
    #     self.skip_treeWidget_row(self.treeWidget_nodal_links_damping)
    #     self.pushButton_remove_link_damping.setDisabled(False)

    #     for key in self.mesh.dict_nodes_with_elastic_link_damping.keys():
    #         node_ids = [int(node) for node in key.split("-")]
    #         mask, _ = self.project.mesh.nodes[node_ids[0]].elastic_nodal_link_damping[key]
    #         new = QTreeWidgetItem([key, str(self.text_label(mask, damping_labels))])
    #         new.setTextAlignment(0, Qt.AlignCenter)
    #         new.setTextAlignment(1, Qt.AlignCenter)
    #         self.treeWidget_nodal_links_damping.addTopLevelItem(new)

    #     if len(self.mesh.dict_nodes_with_elastic_link_damping) == 0:
    #         self.pushButton_remove_link_damping.setDisabled(True)

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


def get_list_cross_sections_to_plot_expansion_joint(list_elements, effective_diameter):
    list_cross_sections = []
    flanges_elements = [    list_elements[0],
                            list_elements[1],
                            list_elements[-2],
                            list_elements[-1]  ]
    
    # self.project.set_cross_section_by_line(self.lineID, None)
    
    for element in list_elements:

        if element in flanges_elements:
            plot_key = "flanges"
        else:
            if np.remainder(element,2) == 0:
                plot_key = "minor"
            else:
                plot_key = "major"

        expansion_joint_info = [    "expansion joint", 
                                    plot_key,
                                    effective_diameter ]

        list_cross_sections.append(CrossSection(expansion_joint_info=expansion_joint_info))
    return list_cross_sections
    