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
from pulse.utils import create_new_folder, get_new_path
from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput
from data.user_input.model.setup.structural.crossSectionInput import CrossSectionInput


window_title_1 = "ERROR MESSAGE"
window_title_2 = "WARNING MESSAGE"

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
        self.preprocessor = project.preprocessor
        self.before_run = self.preprocessor.get_model_checks()
        self.nodes = self.project.preprocessor.nodes
        
        self.structural_elements = self.project.preprocessor.structural_elements
        self.dict_tag_to_entity = self.project.preprocessor.dict_tag_to_entity

        self.project_folder_path = project.project_folder_path 
        self.userPath = os.path.expanduser('~')     
        self.folder_name = "imported_data"  
        self._entity_path = self.project.file._entity_path
        self._project_path = self.project.file._project_path
        self.stop = False
        self.complete = False
        self.aquisition_parameters_processed = False
        self.node_ID_remove = None
        self.ext_key = None

        self.label_selected_id = self.findChild(QLabel, 'label_selected_id')
        self.label_selected_id_2 = self.findChild(QLabel, 'label_selected_id_2')
        
        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
        self.lineEdit_selected_info = self.findChild(QLineEdit, 'lineEdit_selected_info') 
        
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

        self.pushButton_remove_expansion_joint_by_line = self.findChild(QPushButton, 'pushButton_remove_expansion_joint_by_line')
        self.pushButton_remove_expansion_joint_by_line.clicked.connect(self.remove_selected_expansion_joint_by_line)
        self.pushButton_remove_expansion_joint_by_line.setDisabled(True)

        self.pushButton_remove_expansion_joint_by_elements = self.findChild(QPushButton, 'pushButton_remove_expansion_joint_by_elements')
        self.pushButton_remove_expansion_joint_by_elements.clicked.connect(self.remove_selected_expansion_joint_by_group_elements)
        self.pushButton_remove_expansion_joint_by_elements.setDisabled(True)

        self.pushButton_see_details_from_selection = self.findChild(QPushButton, 'pushButton_see_details_from_selection')
        self.pushButton_see_details_from_selection.clicked.connect(self.get_information)

        self.pushButton_reset_all = self.findChild(QPushButton, 'pushButton_reset_all')
        self.pushButton_reset_all.clicked.connect(self.reset_all)

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.force_to_close)

        self.pushButton_get_length = self.findChild(QPushButton, 'pushButton_get_length')
        self.pushButton_get_length.clicked.connect(self.get_length)

        # self.pushButton_get_length.clicked.connect(self.force_to_close)

        self.tabWidget_main = self.findChild(QTabWidget, 'tabWidget_main')
        self.tabWidget_main.currentChanged.connect(self.tabEvent_main)
        self.current_tab_main = self.tabWidget_main.currentIndex()

        self.tab_setup = self.findChild(QWidget, "tab_setup")
        self.tab_remove = self.findChild(QWidget, "tab_remove")
  
        self.lineEdit_node_ID_info = self.findChild(QLineEdit, 'lineEdit_node_ID_info')
        # self.lineEdit_parameters_info = self.findChild(QLineEdit, 'lineEdit_parameters_info')

        self.treeWidget_expansion_joint_by_lines = self.findChild(QTreeWidget, 'treeWidget_expansion_joint_by_lines')
        self.treeWidget_expansion_joint_by_lines.itemClicked.connect(self.on_click_item)

        self.treeWidget_expansion_joint_by_elements = self.findChild(QTreeWidget, 'treeWidget_expansion_joint_by_elements')
        self.treeWidget_expansion_joint_by_elements.itemClicked.connect(self.on_click_item)

        self.config_treeWidget_headers()
        
        self.update()
        self.load_expansion_joint_by_line_info()
        self.load_expansion_joint_by_elements_info()
        self.update_tabs()
        self.exec_()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_inputs.currentIndex() == 0:
                self.constant_input_confirm()
            elif self.tabWidget_inputs.currentIndex() == 1: 
                self.table_input_confirm() 
        if event.key() == Qt.Key_Escape:
            self.close()

    def update_tabs(self):
        size_1 = len(self.preprocessor.dict_lines_with_expansion_joints)
        size_2 = len(self.preprocessor.group_elements_with_expansion_joints)
        if size_1 + size_2 == 0:
            self.tab_remove.setDisabled(True)
            self.tabWidget_main.setCurrentWidget(self.tab_setup)
        else:
            self.tab_remove.setDisabled(False)

    def config_treeWidget_headers(self):     
        self.treeWidget_expansion_joint_by_lines.setColumnWidth(0, 80)
        self.treeWidget_expansion_joint_by_lines.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_expansion_joint_by_lines.headerItem().setTextAlignment(1, Qt.AlignCenter)
        self.treeWidget_expansion_joint_by_elements.setColumnWidth(0, 80)
        self.treeWidget_expansion_joint_by_elements.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_expansion_joint_by_elements.headerItem().setTextAlignment(1, Qt.AlignCenter)

    def get_length(self):
        lineEdit_lineID = self.lineEdit_selected_ID.text()
        if lineEdit_lineID != "":
            self.stop, self.line_id = self.before_run.check_input_LineID(lineEdit_lineID, single_ID=True)
            if self.stop:
                self.lineEdit_selected_ID.setText("")
                self.lineEdit_joint_length.setText("")
                self.lineEdit_selected_ID.setFocus()
                return True  
            joint_length = self.preprocessor.get_line_length(self.line_id) 
            self.lineEdit_joint_length.setText(str(round(joint_length,6)))

    def write_id(self, selected_id):
        self.lineEdit_selected_ID.setText(str(selected_id[0]))

    def update(self):

        self.update_selected_id()
        self.update_selection_lineEdit_visibility()
        
        if self.line_id != []:
            self.write_id(self.line_id)
            self.radioButton_line_selection.setChecked(True)
            length = self.preprocessor.get_line_length(self.line_id[0])
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
            self.pushButton_get_length.setVisible(False)
            if self.line_id != []:
                self.lineEdit_selected_ID.setText("")      

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
    
    def update_selection_lineEdit_visibility(self, state_has_changed=False):
        if state_has_changed:
            new_state = [self.selection_by_line,self.selection_by_node,self.selection_by_element] 
            for i, label in enumerate(["Line ID:", "Node ID:", "Element ID:"]):
                if new_state[i]:
                    self.label_selected_id.setText(label)
        else:
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
            self.update_selection_flags()

    def update_selection_flags(self):
        self.selection_by_line = self.radioButton_line_selection.isChecked()
        self.selection_by_node = self.radioButton_node_selection.isChecked()
        self.selection_by_element = self.radioButton_element_selection.isChecked()
        self.update_get_length_button_visibility()

    def radioButtonEvent_selection_type(self):  
        current_state = [self.selection_by_line,self.selection_by_node,self.selection_by_element] 
        self.update_selection_flags()
        new_state = [self.selection_by_line,self.selection_by_node,self.selection_by_element] 
        if current_state == new_state:
            state_has_changed = False
        else:
            state_has_changed = True
        self.update_selected_id()
        self.update_selection_lineEdit_visibility(state_has_changed=state_has_changed)

        if self.line_id != []:
            if self.selection_by_line:
                self.write_id(self.line_id)
            
        elif self.node_id != []:
            if self.selection_by_node:
                self.write_id(self.node_id)
                    
        elif self.element_id != []:
            if self.selection_by_element:
                self.write_id(self.element_id)     

        else:
            self.lineEdit_selected_ID.setText("")       

    def radioButtonEvent_rods(self):
        self.add_rods = self.radioButton_add_rods.isChecked()

    def tabEvent_main(self):
        self.current_tab_main = self.tabWidget_main.currentIndex()
        if self.current_tab_main == 0:
            self.lineEdit_selected_info.setText("")
        if self.current_tab_main == 1:
            self.update_remove_buttons()

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
        if self.lineEdit_axial_locking_criteria.text() not in ["1", "1.0"]:
            self.lineEdit_axial_locking_criteria.setText("")
        self.lineEdit_axial_stiffness.setText("")
        self.lineEdit_transversal_stiffness.setText("")
        self.lineEdit_torsional_stiffness.setText("")
        self.lineEdit_angular_stiffness.setText("")

    def load_input_fields(self):
        if self.line_id != []: 
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
                    self.radioButton_not_add_rods.setChecked(True) 
                
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
                PrintMessageInput([title, message, window_title_1])

    def get_nodes_elements_according_joint_length(self):
        if self.selection_by_node:
            self.list_nodes, self.list_elements = self.preprocessor.get_neighbor_nodes_and_elements_by_node(self.nodeID, self.joint_length)
        elif self.selection_by_element:
            self.list_nodes, self.list_elements = self.preprocessor.get_neighbor_nodes_and_elements_by_element(self.elementID, self.joint_length)

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
            PrintMessageInput([title, message, window_title_1])
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

        self.add_rods_key = float(self.add_rods)
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


    def constant_input_confirm(self):
        
        if self.check_initial_inputs():
            return
        
        if self.check_constant_values_to_stiffness():
            return

        self.all_parameters = [self.list_parameters, self.list_stiffness, []]
            
        if self.selection_by_line:

            self.project.set_cross_section_by_line(self.lineID, None)
            self.list_elements = self.preprocessor.line_to_elements[self.lineID]
            list_cross = get_list_cross_sections_to_plot_expansion_joint(   self.list_elements, 
                                                                            self.effective_diameter )
            self.project.preprocessor.set_cross_section_by_element(self.list_elements, list_cross)
            self.project.add_expansion_joint_by_line(self.lineID, self.all_parameters, False)

        else:

            self.get_nodes_elements_according_joint_length()
            self.lines_to_apply_cross_section = self.get_list_of_lines_to_update_cross_section() 
            if self.lines_to_apply_cross_section != []:
                read = CrossSectionInput(   self.project, 
                                            self.opv, 
                                            pipe_to_beam = False, 
                                            beam_to_pipe = True, 
                                            lines_to_update_cross_section = self.lines_to_apply_cross_section)
                if not read.complete:
                    return
            self.check_expansion_joint_already_added_to_elements(self.list_elements, self.all_parameters)            
            self.project.add_expansion_joint_by_elements(self.list_elements, self.all_parameters, False)

        self.update_plots()
        self.close()

    def get_list_of_lines_to_update_cross_section(self):
        list_lines = []
        for element_id in self.list_elements:
            line_id = self.preprocessor.elements_to_line[element_id]
            list_elements_from_line = self.preprocessor.line_to_elements[line_id]
            for element_id_from_line in list_elements_from_line:
                element = self.structural_elements[element_id_from_line]
                if element.element_type in [None, "beam_1"] or element.cross_section in [None]:
                    if line_id not in list_lines:
                        list_lines.append(line_id)
        return list_lines

    def get_pipe_cross_section_from_neighbors(self, line_id, list_elements):

        line_elements = self.preprocessor.line_to_elements[line_id]
        lower_id = list_elements[0] - 1
        upper_id = list_elements[-1] + 1

        cross = None
        structural_element_type = None
        
        if lower_id in line_elements:
            element = self.structural_elements[lower_id]
            cross = element.cross_section
            structural_element_type = element.element_type
        
        elif upper_id in line_elements:
            element = self.structural_elements[upper_id]
            cross = element.cross_section
            structural_element_type = element.element_type
        
        return cross, structural_element_type

    def check_expansion_joint_already_added_to_elements(self, list_elements_new, parameters_new):
        changed = False
        temp_dict = self.preprocessor.group_elements_with_expansion_joints.copy()
        
        for key, data in temp_dict.items():
            [list_elements_current, _] = data
            
            outside = True
            for id_current in list_elements_current:
                if id_current in list_elements_new:
                    line_id = self.preprocessor.elements_to_line[id_current]
                    outside = False
                    break
                else:
                    outside = True
            
            if not outside:
                
                cross, etype = self.get_pipe_cross_section_from_neighbors(line_id, list_elements_current)
                self.preprocessor.set_structural_element_type_by_element(list_elements_current, etype)
                self.project.add_expansion_joint_by_elements(   list_elements_current, 
                                                                None, 
                                                                False, 
                                                                update_element_type=False, 
                                                                reset_cross=False   )
                self.project.set_cross_section_by_elements(list_elements_current, cross)
                self.preprocessor.group_elements_with_expansion_joints.pop(key)
                changed = True
              
        return changed
       
    def _get_list_of_values_from_string(self, input_string, are_values_int=True):
        
        input_string = input_string[1:-1].split(',')
        list_values = []
        
        if are_values_int:
            for value in input_string:
                list_values.append(int(value))
        else:
            for value in input_string:
                list_values.append(float(value))

        return list_values

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
        
        self.project_table_path = create_new_folder(self.project_folder_path, self.folder_name)
        self.new_load_path_table = get_new_path(self.project_table_path, self.basename)
        
        try:                
            imported_file = np.loadtxt(self.path_imported_table, delimiter=",")
        except Exception as err:
            title = "Error while loading {} table".format(text)
            message = str(err)
            PrintMessageInput([title, message, window_title_1])
            
        if imported_file.shape[1]<2:
            title = "Error while loading {} table".format(text)
            message = "The imported table has insufficient number of columns. The spectrum"
            message += " data must have only two columns to the frequencies and values."
            PrintMessageInput([title, message, window_title_1])
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
            title = "Error while loading {} table".format(text)
            message = str(err)
            PrintMessageInput([title, message, window_title_1])

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
        try:
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

        except Exception as log_error:
            title = "Error while loading stiffness table of values"
            message = str(log_error)
            PrintMessageInput([title, message, window_title_1])
            return True

        self.labels = [ "Axial stiffness", "Transversal stiffness", 
                        "Torsional stiffness", "Angular stiffness"  ]
        self.loaded_stiffness_tables = [Kx, Kyz, Krx, Kryz]

        list_labels = []
        for index, value in enumerate(self.loaded_stiffness_tables):
            if isinstance(value, np.ndarray):
                continue
            elif value is None:
                list_labels.append(self.labels[index])
        
        if list_labels != []:
            title = 'None table selected to expansion joint stiffness'
            message = "Please, define at least one table of values to the:\n\n"
            message += f" {list_labels} \n\nbefore confirming the attribution."
            PrintMessageInput([title, message, window_title_1])
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

        self.all_parameters = [self.list_parameters, self.loaded_stiffness_tables, self.basenames]

        if self.selection_by_line:
            
            self.project.set_cross_section_by_line(self.lineID, None)
            self.list_elements = self.preprocessor.line_to_elements[self.lineID]
            list_cross = get_list_cross_sections_to_plot_expansion_joint(   self.list_elements, 
                                                                            self.effective_diameter )
            self.preprocessor.set_cross_section_by_element(self.list_elements, list_cross)
            self.project.add_expansion_joint_by_line(self.lineID, self.all_parameters, True, self.basenames)

        else:
            
            self.get_nodes_elements_according_joint_length()
            self.lines_to_apply_cross_section = self.get_list_of_lines_to_update_cross_section() 
            if self.lines_to_apply_cross_section != []:
                read = CrossSectionInput(   self.project, 
                                            self.opv, 
                                            pipe_to_beam = False, 
                                            beam_to_pipe = True, 
                                            lines_to_update_cross_section = self.lines_to_apply_cross_section)
                if not read.complete:
                    return
            self.check_expansion_joint_already_added_to_elements(self.list_elements, self.all_parameters)
                          
            self.project.add_expansion_joint_by_elements(self.list_elements, self.all_parameters, True, self.basenames)
        
        self.update_plots()  
        self.close()


    def skip_treeWidget_row(self, treeWidget):
        new = QTreeWidgetItem(["", ""])
        new.setTextAlignment(0, Qt.AlignCenter)
        new.setTextAlignment(1, Qt.AlignCenter)
        treeWidget.addTopLevelItem(new)
    
    def _get_offset_from_string(self, offset):
        offset = offset[1:-1].split(',')
        offset_y = offset_z = 0.0
        if len(offset) == 2:
            if offset[0] != '0.0':
                offset_y = float(offset[0])
            if offset[1] != '0.0':
                offset_z = float(offset[1])
        return offset_y, offset_z

    def load_expansion_joint_by_line_info(self):
        self.treeWidget_expansion_joint_by_lines.clear()
        for line_id, parameters in self.preprocessor.dict_lines_with_expansion_joints.items():
           
            if get_string_from_joint_paramters(parameters):
                str_joint_data = f"{str(parameters[0])[1:-1]}, {'Table, Table, Table, Table'}"
            else:
                str_joint_data = f"{str(parameters[0])[1:-1]}, {str(parameters[1])[1:-1]}"

            new = QTreeWidgetItem([str(line_id), str_joint_data])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_expansion_joint_by_lines.addTopLevelItem(new)

    def load_expansion_joint_by_elements_info(self):
        self.treeWidget_expansion_joint_by_elements.clear()
        for group_id, [_, parameters] in self.preprocessor.group_elements_with_expansion_joints.items():
           
            if get_string_from_joint_paramters(parameters):
                str_joint_data = f"{str(parameters[0])[1:-1]}, {'Table, Table, Table, Table'}"
            else:
                str_joint_data = f"{str(parameters[0])[1:-1]}, {str(parameters[1])[1:-1]}"

            new = QTreeWidgetItem([str(group_id), str_joint_data])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_expansion_joint_by_elements.addTopLevelItem(new)

    def update_remove_buttons(self):

        if len(self.preprocessor.dict_lines_with_expansion_joints) == 0:
            self.pushButton_remove_expansion_joint_by_line.setDisabled(True)
        else:
            self.pushButton_remove_expansion_joint_by_line.setDisabled(False)

        if len(self.preprocessor.group_elements_with_expansion_joints) == 0:
            self.pushButton_remove_expansion_joint_by_elements.setDisabled(True)
        else:
            self.pushButton_remove_expansion_joint_by_elements.setDisabled(False)


    def on_click_item(self, item):
        self.lineEdit_selected_info.setText(item.text(0))
        selection = item.text(0)
        if selection != "":
            self.update_remove_buttons()
            # self.pushButton_see_details_from_selection.setDisabled(True)
            return
  
        # self.pushButton_see_details_from_selection.setDisabled(False)
        # self.pushButton_remove_expansion_joint_by_line.setDisabled(False)
        # self.pushButton_remove_expansion_joint_by_elements.setDisabled(False)

    def get_information(self):
        try:
            selection = self.lineEdit_selected_info.text()
            if selection != "":        
                GetInformationOfGroup(self.project, selection)
            else:
                title = "UNSELECTED EXPANSION JOINT"
                message = "Please, select an expansion joint in the list to get the information."
                PrintMessageInput([title, message, window_title_2])
                
        except Exception as log_error:
            title = "Error while getting information of expansion joint"
            message = str(log_error)
            PrintMessageInput([title, message, window_title_1])


    def remove_selected_expansion_joint_by_line(self):
        if self.lineEdit_selected_info.text() == "":
            title = "Empty selection in expansion joint"
            message = "Please, select an expansion joint in the list\n before confirm the joint removal."
            PrintMessageInput([title, message, window_title_2])
            return

        line_id = int(self.lineEdit_selected_info.text())
        
        title = "Removal of the expansion joint"
        message = "Are you really sure you want to remove the expansion joint \n" 
        message += f"added to the line {line_id}?\n\n\n"
        message += "Press the Continue button to proceed with removal or press \n"
        message += "Cancel or Close buttons to abort the current operation."
        read = CallDoubleConfirmationInput(title, message)

        if read._doNotRun:
            return
        
        if read._continue:
            if line_id in list(self.preprocessor.dict_lines_with_expansion_joints.keys()):
                self.remove_expansion_joint_by_line(line_id)
                self.update_plots()

            title = "Removal of the expansion joint"
            message = f"The expansion joint added to the line {line_id} \nhas been removed from the model."
            PrintMessageInput([title, message, window_title_1])


    def remove_selected_expansion_joint_by_group_elements(self):
        if self.lineEdit_selected_info.text() == "":
            title = "Empty selection in expansion joint"
            message = "Please, select an expansion joint in the list\n before confirm the joint removal."
            PrintMessageInput([title, message, window_title_2])
            return

        selected_group = self.lineEdit_selected_info.text()
        title = "Removal of the expansion joint"
        message = "Are you really sure you want to remove the expansion joint\n" 
        message += f"added to the following group ?\n\n"
        message += f"{selected_group}\n"
        message += "\n\nPress the Continue button to proceed with removal or press \n"
        message += "Cancel or Close buttons to abort the current operation."
        read = CallDoubleConfirmationInput(title, message)

        if read._doNotRun:
            return

        if read._continue:
            self.remove_expansion_joint_by_group_of_elements(selected_group)
            self.update_plots()
                
        title = "Removal of the expansion joint"
        message = f"The expansion joint added to the group {selected_group} \nhas been removed from the model."
        PrintMessageInput([title, message, window_title_1])


    def remove_expansion_joint_by_line(self, line_id):

        self.remove_table_files_from_imported_data_folder_by_line(line_id)
        self.project.add_expansion_joint_by_line(line_id, None, False) 


    def remove_expansion_joint_by_group_of_elements(self, selected_group):

        if selected_group in self.preprocessor.group_elements_with_expansion_joints.keys():
            [list_elements, _] = self.preprocessor.group_elements_with_expansion_joints[selected_group]
            list_lines = []
            for element_id in list_elements:
                line_id = self.preprocessor.elements_to_line[element_id]
                if line_id not in list_lines:
                    list_lines.append(line_id)

        self.remove_table_files_from_imported_data_folder_by_elements(list_elements)
        
        for line_id in list_lines:
            cross, etype = self.get_pipe_cross_section_from_neighbors(line_id, list_elements)
            self.preprocessor.set_structural_element_type_by_element(list_elements, etype)
            self.project.set_cross_section_by_elements(list_elements, cross)
            self.project.add_expansion_joint_by_elements(   list_elements, 
                                                            None, 
                                                            False, 
                                                            update_element_type=False,
                                                            reset_cross=False   )
            self.preprocessor.group_elements_with_expansion_joints.pop(selected_group)
        

    def reset_all(self):

        title = "Remove all expansion joints added to the model"
        message = "Are you really sure you want to remove all expansion joints from the model?\n\n\n"
        message += "Press the Continue button to proceed with removal or press Cancel or Close buttons to abort the current operation."
        read = CallDoubleConfirmationInput(title, message)

        if read._doNotRun:
            return

        if read._continue:

            temp_dict_1 = self.preprocessor.dict_lines_with_expansion_joints.copy()
            for line_id in temp_dict_1.keys():
                self.remove_expansion_joint_by_line(line_id)
            
            temp_dict_2 = self.preprocessor.group_elements_with_expansion_joints.copy()
            for group in temp_dict_2.keys(): 
               self.remove_expansion_joint_by_group_of_elements(group)

            self.update_plots()

            title = "Removal of expansion joints"
            message = "All expansion joints have been removed from the model."
            PrintMessageInput([title, message, window_title_1])

    def update_plots(self):
        self.load_expansion_joint_by_line_info()
        self.load_expansion_joint_by_elements_info()
        self.update_remove_buttons()
        self.update_tabs()
        self.opv.opvRenderer.plot()
        # self.opv.opvAnalisysRenderer.plot()
        self.opv.changePlotToEntitiesWithCrossSection() 
    
    def remove_table_files_from_imported_data_folder_by_elements(self, list_elements):

        config = configparser.ConfigParser()
        config.read(self._entity_path)
        sections = config.sections()

        list_table_names = []
        list_joint_stiffness = []
        for section in sections:
            keys = list(config[section].keys())
            if 'list of elements' in keys:
                str_list_elements_from_file = config[section]['list of elements']
                if str_list_elements_from_file == str(list_elements):
                    if 'expansion joint stiffness' in keys:
                        read_joint_stiffness = config[section]['expansion joint stiffness']
                        list_joint_stiffness = read_joint_stiffness[1:-1].replace(" ","").split(',')
                        cache_section = section
        
        if list_joint_stiffness == []:
            return

        for stiffness_value in list_joint_stiffness:
            try:
                float(stiffness_value)
                return
            except:
                break
        
        list_table_multiple_joints = []
        list_table_names = list_joint_stiffness
        
        for section in sections:
            if section != cache_section:
                keys = list(config[section].keys())
                if 'expansion joint stiffness' in keys:
                    read_table_names = config[section]['expansion joint stiffness']
                    for table_name in list_table_names:
                        if table_name in read_table_names:
                            list_table_multiple_joints.append(table_name)
        
        if len(list_table_multiple_joints)==0:
            self.confirm_table_file_removal(list_table_names)


    def remove_table_files_from_imported_data_folder_by_line(self, line_id):

        str_line_id = str(line_id)
        config = configparser.ConfigParser()
        config.read(self._entity_path)
        sections = config.sections()

        list_table_names = []
        list_joint_stiffness = []
        if str_line_id in sections:
            keys = list(config[str_line_id].keys())
            if 'expansion joint stiffness' in keys:
                read_joint_stiffness = config[str_line_id]['expansion joint stiffness']
                list_joint_stiffness = read_joint_stiffness[1:-1].replace(" ","").split(',')
                cache_section = str_line_id
        
        if list_joint_stiffness == []:
            return

        for stiffness_value in list_joint_stiffness:
            try:
                float(stiffness_value)
                return
            except:
                break
        
        list_table_multiple_joints = []
        list_table_names = list_joint_stiffness
        
        for section in sections:
            if section != cache_section:
                keys = list(config[section].keys())
                if 'expansion joint stiffness' in keys:
                    read_table_names = config[section]['expansion joint stiffness']
                    for table_name in list_table_names:
                        if table_name in read_table_names:
                            list_table_multiple_joints.append(table_name)
        
        if len(list_table_multiple_joints)==0:
            self.confirm_table_file_removal(list_table_names)


    def confirm_table_file_removal(self, list_tables):

        title = "Removal of imported table files"
        message = "Do you want to remove the following unused imported table \nfrom the project folder?\n\n"
        for table in list_tables:
            message += f"{table}\n"
        message += "\n\nPress the Continue button to proceed with removal or press Cancel or \nClose buttons to abort the current operation."
        read = CallDoubleConfirmationInput(title, message)

        if read._doNotRun:
            return

        if read._continue:
            for table_name in list_tables:
                self.project.remove_file_or_folder_from_project_directory(table_name, folder_name="imported_data")
            self.project.remove_imported_data_folder_if_empty()             
        
    def force_to_close(self):
        self.close()

class GetInformationOfGroup(QDialog):
    def __init__(self, project, selection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Model/Info/getExpansionJointInformationInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.project = project
        self.selection = selection
        self.preprocessor = project.preprocessor
        self._entity_path = self.project.file._entity_path

        self.title_label = self.findChild(QLabel, 'title_label')
        self.title_label.setText('Information of selected expansion joint')
        self.treeWidget_group_info = self.findChild(QTreeWidget, 'treeWidget_group_info')

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.force_to_close)
        
        self.update_header_labels()
        self.update_treeWidget_joint_parameters_info()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Enter:
            self.close()

    def update_treeWidget_header(self):
        column_widths = [80, 602]
        for i, width in enumerate(column_widths):
            self.treeWidget_group_info.headerItem().setText(i, self.header_labels[i])
            self.treeWidget_group_info.setColumnWidth(i, width)
            self.treeWidget_group_info.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def update_header_labels(self):
        if "group" in self.selection:
            if self.selection in self.preprocessor.group_elements_with_expansion_joints.keys():
                self.header_labels = ["Element ID", "Joint parameters [length, effective_diameter, mass, axial locking ε, rods, kx, kyz, krx, kryz]"]
                self.update_treeWidget_header()   
        else:    
            if int(self.selection) in self.preprocessor.dict_lines_with_expansion_joints.keys():
                self.header_labels = ["Line ID", "Joint parameters [length, effective_diameter, mass, axial locking ε, rods, kx, kyz, krx, kryz]"]
                self.update_treeWidget_header()   
    
    def skip_treeWidget_row(self):
        new = QTreeWidgetItem(["", ""])
        for i in range(len(self.header_labels)):
            new.setTextAlignment(i, Qt.AlignCenter)
        self.treeWidget_group_info.addTopLevelItem(new)

    def update_treeWidget_joint_parameters_info(self):

        self.treeWidget_group_info.clear()

        if "group" in  self.selection:
            if self.selection in self.preprocessor.group_elements_with_expansion_joints.keys():
                data = self.preprocessor.group_elements_with_expansion_joints[self.selection]
                [list_elements, all_joint_parameters] = data
                [joint_parameters, joint_stiffness, table_names] = all_joint_parameters
                
                str_joint_parameters = str(joint_parameters)
                if get_string_from_joint_paramters(all_joint_parameters):
                    str_table_names = f"{table_names[0]}, {table_names[1]}, {table_names[2]}, {table_names[3]}"
                    str_joint_data = f"{str_joint_parameters[1:-1]}, {str_table_names}"
                else:
                    str_joint_stiffness = str(joint_stiffness)
                    str_joint_data = f"{str_joint_parameters[1:-1]}, {str_joint_stiffness[1:-1]}"
                
                for element_id in list_elements:
                    new = QTreeWidgetItem([str(element_id), str_joint_data])
                    for i in range(len(self.header_labels)):
                        new.setTextAlignment(i, Qt.AlignCenter)
                    self.treeWidget_group_info.addTopLevelItem(new)
                
        else:

            if int(self.selection) in self.preprocessor.dict_lines_with_expansion_joints.keys():
                all_joint_parameters = self.preprocessor.dict_lines_with_expansion_joints[int(self.selection)]
                [joint_parameters, joint_stiffness, table_names] = all_joint_parameters

                str_joint_parameters = str(joint_parameters)
                if get_string_from_joint_paramters(all_joint_parameters):
                    str_table_names = f"{table_names[0]}, {table_names[1]}, {table_names[2]}, {table_names[3]}"
                    str_joint_data = f"{str_joint_parameters[1:-1]}, {str_table_names}"
                else:
                    str_joint_stiffness = str(joint_stiffness)
                    str_joint_data = f"{str_joint_parameters[1:-1]}, {str_joint_stiffness[1:-1]}"

                new = QTreeWidgetItem([self.selection, str_joint_data])
                for i in range(len(self.header_labels)):
                    new.setTextAlignment(i, Qt.AlignCenter)
                self.treeWidget_group_info.addTopLevelItem(new)


    def force_to_close(self):
        self.close()


def get_list_cross_sections_to_plot_expansion_joint(list_elements, effective_diameter):

    """"This auxiliary function returns a list of CrossSection relative to the expansion joints."""

    list_cross_sections = []
    flanges_elements = [    list_elements[0],
                            list_elements[1],
                            list_elements[-2],
                            list_elements[-1]  ]
    
    for element in list_elements:

        if element in flanges_elements:
            plot_key = "flanges"
        else:
            if np.remainder(element,2) == 0:
                plot_key = "minor"
            else:
                plot_key = "major"

        expansion_joint_info = [    "Expansion joint section", 
                                    plot_key,
                                    effective_diameter ]

        list_cross_sections.append(CrossSection(expansion_joint_info=expansion_joint_info))
    return list_cross_sections 

def get_string_from_joint_paramters(parameters):
    for parameter in parameters:
        for value in parameter:
            if isinstance(value, np.ndarray):
                return True
    return False