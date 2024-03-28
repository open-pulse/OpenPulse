from PyQt5.QtWidgets import QDialog, QCheckBox, QFileDialog, QLabel, QLineEdit, QPushButton, QSpinBox, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
from numpy.core.numeric import False_  

from pulse import UI_DIR
from pulse.preprocessing.compressor_model import CompressorModel
from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.before_run import BeforeRun
from pulse.tools.utils import create_new_folder, get_new_path
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.call_double_confirmation import CallDoubleConfirmationInput
from pulse.interface.formatters.icons import get_openpulse_icon

window_title_1 = "Error"
window_title_2 = "Warning"

class FlangesInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        uic.loadUi(UI_DIR / "model/setup/structural/flangesInput.ui", self)

        self.opv = opv
        self.opv.setInputObject(self)

        self.project = project
        self.preprocessor = project.preprocessor
        self.before_run = project.get_pre_solution_model_checks()
        self.nodes = self.project.preprocessor.nodes
        self.preprocessor._map_lines_to_nodes()
        
        self.structural_elements = self.project.preprocessor.structural_elements
   
        self.element_size = self.project.file._element_size
        self.stop = False
        self.complete = False
        self.multiple_selection = False
        self.aquisition_parameters_processed = False
        self.node_ID_remove = None
        self.ext_key = None
        self.list_frequencies = []
        
        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
        self.label_selected_id = self.findChild(QLabel, 'label_selected_id')
        self.label_selected_id_2 = self.findChild(QLabel, 'label_selected_id_2')
        self.label_number_elements = self.findChild(QLabel, 'label_number_elements')
        self.label_first = self.findChild(QLabel, 'label_first')
        self.label_last = self.findChild(QLabel, 'label_last')
        
        self.lineEdit_element_size_line = self.findChild(QLineEdit, 'lineEdit_element_size_line')
        self.lineEdit_element_size_line.setText(str(self.element_size))
        self.lineEdit_flange_length_line = self.findChild(QLineEdit, 'lineEdit_flange_length_line')
        self.lineEdit_outer_diameter_line = self.findChild(QLineEdit, 'lineEdit_outer_diameter_line')
        self.lineEdit_first_line = self.findChild(QLineEdit, 'lineEdit_first_line')
        self.lineEdit_last_line = self.findChild(QLineEdit, 'lineEdit_last_line')
        
        self.lineEdit_element_size_node = self.findChild(QLineEdit, 'lineEdit_element_size_node')
        self.lineEdit_element_size_node.setText(str(self.element_size))
        self.lineEdit_flange_length_node = self.findChild(QLineEdit, 'lineEdit_flange_length_node')
        self.lineEdit_outer_diameter_node = self.findChild(QLineEdit, 'lineEdit_outer_diameter_node')
        self.lineEdit_outer_diameter_element = self.findChild(QLineEdit, 'lineEdit_outer_diameter_element')
        
        self.lineEdit_outer_diameter = self.findChild(QLineEdit, 'lineEdit_outer_diameter')
        self.lineEdit_inner_diameter = self.findChild(QLineEdit, 'lineEdit_inner_diameter')
        self.lineEdit_offset_y = self.findChild(QLineEdit, 'lineEdit_offset_y')
        self.lineEdit_offset_z = self.findChild(QLineEdit, 'lineEdit_offset_z')
        self.lineEdit_insulation_thickness = self.findChild(QLineEdit, 'lineEdit_insulation_thickness')
        self.lineEdit_insulation_density = self.findChild(QLineEdit, 'lineEdit_insulation_density')

        self.line_id = self.opv.getListPickedLines()
        self.node_id = self.opv.getListPickedPoints()
        self.element_id = self.opv.getListPickedElements()
        
        self.spinBox_number_elements_line = self.findChild(QSpinBox, 'spinBox_number_elements_line') 
        self.spinBox_number_elements_line.valueChanged.connect(self.update_flange_length_line)
        self.update_flange_length_line()

        self.spinBox_number_elements_node = self.findChild(QSpinBox, 'spinBox_number_elements_node') 
        self.spinBox_number_elements_node.valueChanged.connect(self.update_flange_length_node)        
        self.update_flange_length_node()

        self.radioButton_line_selection = self.findChild(QRadioButton, 'radioButton_line_selection')
        self.radioButton_node_selection = self.findChild(QRadioButton, 'radioButton_node_selection')
        self.radioButton_element_selection = self.findChild(QRadioButton, 'radioButton_element_selection')
        self.radioButton_line_selection.clicked.connect(self.radioButtonEvent_selection_type)
        self.radioButton_node_selection.clicked.connect(self.radioButtonEvent_selection_type)
        self.radioButton_element_selection.clicked.connect(self.radioButtonEvent_selection_type)
        self.selection_by_line = self.radioButton_line_selection.isChecked()
        self.selection_by_node = self.radioButton_node_selection.isChecked()
        self.selection_by_element = self.radioButton_element_selection.isChecked()
                
        self.radioButton_both_nodes = self.findChild(QRadioButton, 'radioButton_both_nodes')
        self.radioButton_first_node = self.findChild(QRadioButton, 'radioButton_first_node')
        self.radioButton_last_node = self.findChild(QRadioButton, 'radioButton_last_node')

        self.radioButton_both_nodes.clicked.connect(self.radioButtonEvent_node_advanced_selection)
        self.radioButton_first_node.clicked.connect(self.radioButtonEvent_node_advanced_selection)
        self.radioButton_last_node.clicked.connect(self.radioButtonEvent_node_advanced_selection)

        self.selection_by_both_nodes = self.radioButton_both_nodes.isChecked()
        self.selection_by_first_node = self.radioButton_first_node.isChecked()
        self.selection_by_last_node = self.radioButton_last_node.isChecked()

        self.treeWidget_flange_by_elements = self.findChild(QTreeWidget, 'treeWidget_flange_by_elements')
        self.load_elements_treeWidget_info()

        self.pushButton_constant_input_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_constant_input_confirm.clicked.connect(self.add_flange_to_selected_elements)

        # self.tabWidget_main = self.findChild(QTabWidget, 'tabWidget_main')
        # self.tab_setup = self.tabWidget_main.findChild(QWidget, "tab_setup")

        self.tabWidget_inputs = self.findChild(QTabWidget, 'tabWidget_inputs')
        # self.tabWidget_inputs.currentChanged.connect(self.tabEvent_inputs)
        self.tab_lines = self.tabWidget_inputs.findChild(QWidget, "tab_lines")
        self.tab_nodes = self.tabWidget_inputs.findChild(QWidget, "tab_nodes")
        self.tab_elements = self.tabWidget_inputs.findChild(QWidget, "tab_elements")
        self.tab_section_parameters = self.tabWidget_inputs.findChild(QWidget, "tab_section_parameters")
        self.tabWidget_inputs.clear()
        self.tabWidget_inputs.addTab(self.tab_lines, "Line selection")
        
        if len(self.line_id) + len(self.node_id) + len(self.element_id) == 0:
            self.opv.plot_entities_with_cross_section()
        
        self.checkBox_event_update()

        self.checkBox_get_cross_section = self.findChild(QCheckBox, 'checkBox_get_cross_section')
        self.checkBox_get_cross_section.clicked.connect(self.checkBox_event_update)
        self.flag_checkBox = self.checkBox_get_cross_section.isChecked()

        self.update()
        self._load_icons()
        self._config_window()
        self.exec()
    
    def _load_icons(self):
        self.icon = get_openpulse_icon()
    
    def _config_window(self):
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_main.currentIndex() == 0:
                self.add_flange_to_selected_elements()

        if event.key() == Qt.Key_Escape:
            self.close()

    def force_to_close(self):
        self.close()

    def checkBox_event_update(self):
        self.flag_checkBox = self.checkBox_get_cross_section.isChecked()
        if self.flag_checkBox:
            self.tabWidget_inputs.removeTab(1)
        else:

            self.tabWidget_inputs.addTab(self.tab_section_parameters, 'Section parameters')
            
            if self.selection_by_line:
                if self.lineEdit_outer_diameter_line.text() != "":
                    outer_diameter = self.lineEdit_outer_diameter_line.text()
                    self.lineEdit_outer_diameter.setText(outer_diameter) 

            if self.selection_by_node:
                if self.lineEdit_outer_diameter_node.text() != "":
                    outer_diameter = self.lineEdit_outer_diameter_node.text()
                    self.lineEdit_outer_diameter.setText(outer_diameter) 

            if self.selection_by_element:
                if self.lineEdit_outer_diameter_element.text() != "":
                    outer_diameter = self.lineEdit_outer_diameter_element.text()
                    self.lineEdit_outer_diameter.setText(outer_diameter) 

    def radioButtonEvent_node_advanced_selection(self):
        self.selection_by_both_nodes = self.radioButton_both_nodes.isChecked()
        self.selection_by_first_node = self.radioButton_first_node.isChecked()
        self.selection_by_last_node = self.radioButton_last_node.isChecked()
        self.update()

    def radioButtonEvent_selection_type(self): 
        self.line_id = []
        self.node_id = []
        self.element_id = []

        self.update_selection_flags()
        if self.update_selected_id():
            return
        self.update_selection_texts_info()    

    def update_flange_length_line(self):
        self.flange_length = self.spinBox_number_elements_line.value()*self.element_size
        self.lineEdit_flange_length_line.setText(str(self.flange_length))
   
    def update_flange_length_node(self):
        self.flange_length = self.spinBox_number_elements_node.value()*self.element_size
        self.lineEdit_flange_length_node.setText(str(self.flange_length))
 
    def update(self):
        if self.update_selected_id():
            return
        self.update_selection_flags()
        self.update_selection_texts_info()
                    
    def update_selected_id(self): 
        
        if self.opv.getListPickedPoints() != [] and self.opv.getListPickedElements() != []:
            title = "Multiples node(s) and element(s) selected"
            message = "Dear user, the current selection includes multiples node(s) and element(s). "
            message += "You should to select node(s) or element(s) separately to proceed. "
            self.multiple_selection = True
            self.reset_selection()
            PrintMessageInput([window_title_1, title, message])
            return True

        elif self.opv.getListPickedLines() != []:
            self.line_id = self.opv.getListPickedLines()
            self.node_id = []
            self.element_id = []

        elif self.opv.getListPickedPoints() != []:
            self.node_id = self.opv.getListPickedPoints()
            self.line_id = []
            self.element_id = []

        elif self.opv.getListPickedElements() != []:
            self.element_id = self.opv.getListPickedElements()
            self.line_id = []
            self.node_id = []
        
        else:
            return True

        self.process_tabs_after_selection()

        return False

    def reset_selection(self):
        self.lineEdit_selected_ID.setText("")
        self.line_id = []
        self.node_id = []
        self.element_id = []
        self.treeWidget_flange_by_elements.clear()
        self.opv.plot_mesh()

    def process_tabs_after_selection(self):
        if self.line_id != []:
            self.radioButton_line_selection.setChecked(True)
        
        elif self.node_id != []:
            self.radioButton_node_selection.setChecked(True)
        
        elif self.element_id != []:
            self.radioButton_element_selection.setChecked(True)
        return

    def write_ids(self, list_selected_ids):
        text = ""
        for _id in list_selected_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_ID.setText(text[:-2])  
        if self.check_selection_type():
            return True
        return False

    def update_selection_texts_info(self):
    
        try:
            _state = [self.selection_by_line, self.selection_by_node, self.selection_by_element] 
            for i, label in enumerate(["Line ID:", "Node ID:", "Element ID:"]):
                if _state[i]:
                    self.label_selected_id.setText(label)
            if self.selection_by_line:
                if self.line_id != []:
                    if self.write_ids(self.line_id):
                        return
                     
                    self.update_flange_length_line()
                    self.radioButton_line_selection.setChecked(True)
                    self.get_elements_from_start_end_line()
                
                    if len(self.line_id) == 1:
                        line_id = self.line_id[0]
                        first_node = self.preprocessor.dict_line_to_nodes[line_id][0]
                        last_node = self.preprocessor.dict_line_to_nodes[line_id][1]
                        self.lineEdit_first_node.setText(str(first_node))
                        self.lineEdit_last_node.setText(str(last_node))
                        if self.selection_by_first_node:
                            self.lineEdit_last_node.setText("---")
                        if self.selection_by_last_node:
                            self.lineEdit_first_node.setText("---")
                    else:
                        self.lineEdit_first_node.setText("multiples")
                        self.lineEdit_last_node.setText("multiples")
                else:
                    self.lineEdit_selected_ID.setText("")
                    self.lineEdit_first_node.setText("")
                    self.lineEdit_last_node.setText("")

            if self.selection_by_node:
                if self.node_id != []:
                    if self.write_ids(self.node_id):
                        return
                    self.update_flange_length_node()
                    self.radioButton_node_selection.setChecked(True)
                else:
                    self.lineEdit_selected_ID.setText("")

            if self.selection_by_element:
                if self.element_id != []:
                    if self.write_ids(self.element_id):
                        return
                    self.load_elements_treeWidget_info()
                    self.radioButton_element_selection.setChecked(True)
                else:
                    self.lineEdit_selected_ID.setText("")

        except Exception as log_error:
            print(str(log_error))

    def update_selection_flags(self):
        
        if self.opv.change_plot_to_mesh and self.radioButton_line_selection.isChecked():
            self.opv.plot_entities_with_cross_section()

        self.selection_by_line = self.radioButton_line_selection.isChecked()
        self.selection_by_node = self.radioButton_node_selection.isChecked()
        self.selection_by_element = self.radioButton_element_selection.isChecked()

        self.tabWidget_inputs.clear()
        if self.selection_by_line:
            self.tabWidget_inputs.addTab(self.tab_lines, "Line selection")
            if self.opv.change_plot_to_mesh:
                self.opv.plot_entities_with_cross_section()
        else:
            if not self.opv.change_plot_to_mesh:
                self.opv.plot_mesh()
        
        if self.selection_by_node:
            if self.opv.getListPickedElements() != []:
                self.opv.plot_mesh()
            self.tabWidget_inputs.addTab(self.tab_nodes, "Node selection")
            
        if self.selection_by_element:
            if self.opv.getListPickedPoints() != []:
                self.opv.plot_mesh()
            self.tabWidget_inputs.addTab(self.tab_elements, "Element selection")
        else:
            self.treeWidget_flange_by_elements.clear()
        
        return False

    def get_elements_from_start_end_line(self):
        number_elements = self.spinBox_number_elements_line.value()
        _list_elements = []

        for line_id in self.line_id:  
            elements_from_line = np.sort(self.preprocessor.line_to_elements[line_id])
            elements_from_start = elements_from_line[0:number_elements]
            elements_from_end = elements_from_line[-number_elements:]

            if self.selection_by_both_nodes:
                for element_id_start in elements_from_start:
                    _list_elements.append(element_id_start)
                for element_id_end in elements_from_end:
                    _list_elements.append(element_id_end)
            
            if self.selection_by_first_node:
                for element_id_start in elements_from_start:
                    _list_elements.append(element_id_start)
                
            if self.selection_by_last_node:
                for element_id_end in elements_from_end:
                    _list_elements.append(element_id_end)

        return _list_elements

    def get_neighbors_elements_from_nodes(self):
        self.update_flange_length_node()
        list_all_elements = []
        self.node_to_elements_inside_flange_length = defaultdict(list)
        for node_id in self.node_id:
            length = 2*self.flange_length
            _, list_elements = self.preprocessor.get_neighbor_nodes_and_elements_by_node(node_id, length)
            for element_id in list_elements:
                if element_id not in list_all_elements:
                    list_all_elements.append(element_id)
        return list_all_elements

    def config_treeWidget_flange_elements_headers(self):     
        self.treeWidget_flange_by_elements.setColumnWidth(0, 80)
        self.treeWidget_flange_by_elements.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_flange_by_elements.headerItem().setTextAlignment(1, Qt.AlignCenter)

    def check_flanges_by_lines(self):
        elements_from_line = defaultdict(list)
        for element_id in self.element_id:
            line = self.preprocessor.elements_to_line[element_id]
            elements_from_line[line].append(element_id)
        return elements_from_line

    def load_elements_treeWidget_info(self):
        self.treeWidget_flange_by_elements.clear()
        elements_from_line = self.check_flanges_by_lines()
        for line_id, list_elements in elements_from_line.items():
            flange_length = len(list_elements)*self.element_size
            new = QTreeWidgetItem([str(line_id), str(flange_length)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_flange_by_elements.addTopLevelItem(new)

    def check_selection_type(self):

        _stop = False
        lineEdit_selection = self.lineEdit_selected_ID.text()

        if self.selection_by_line:
            _stop, self.lineID = self.before_run.check_input_LineID(lineEdit_selection)
            for line_id in self.lineID:
                entity = self.preprocessor.dict_tag_to_entity[line_id]
                if entity.structural_element_type in ["beam_1", "expansion_joint"]:
                    _stop = True
                    break
                   
        elif self.selection_by_node:
            _stop, self.nodeID = self.before_run.check_input_NodeID(lineEdit_selection)
            for node_id in self.nodeID:
                node = self.preprocessor.nodes[node_id]
                elements_connected_to_node = self.preprocessor.elements_connected_to_node[node]
                if len(elements_connected_to_node) > 2:
                    _stop = True
                for element in elements_connected_to_node:
                    if element.element_type in ["beam_1", "expansion_joint"]:
                        _stop = True
                        break
                if _stop:
                    break

        elif self.selection_by_element:
            _stop, self.elementID = self.before_run.check_input_ElementID(lineEdit_selection)
            for element_id in self.elementID:
                element = self.structural_elements[element_id]
                if element.element_type in ["beam_1", "expansion_joint"]:
                    _stop = True
                    break

        if _stop:
            self.lineEdit_selected_ID.setText("")
            self.lineEdit_selected_ID.setFocus()
            return True

        return False

    def check_input_parameters(self, lineEdit, label, _float=True, _zero_if_empty=False, _only_positive=True):
        message = ""
        title = f"Invalid entry to the '{label}'"
        value_string = lineEdit.text()
        if value_string != "":
            try:
                if _float:
                    value = float(value_string)
                else:
                    value = int(value_string) 
                if value < 0 and _only_positive:
                    message = f"You cannot input a non-positive value at the '{label}' input field."
                elif value == 0 and not _zero_if_empty:
                    message = f"You cannot input a zero value at the '{label}' input field."
                else:
                    self.value = value
            except Exception as _log_error:
                message = f"You have typed an invalid value at the '{label}' input field."
                message += "The input value should be a positive float number.\n\n"
                message += f"{str(_log_error)}"
        elif _zero_if_empty:
            self.value = float(0)
        else:
            message = f"An empty entry has been detected at the '{label}' input field.\n\n" 
            message += "You should enter a positive value to proceed."
            self.value = None
        if message != "":
            PrintMessageInput([window_title_1, title, message])
            return True
        else:
            return False

    def check_all_cross_section_parameters(self):
        if self.check_input_parameters(self.lineEdit_outer_diameter, 'Outer diameter'):
            self.tabWidget_inputs.setCurrentIndex(1)
            self.lineEdit_outer_diameter.setFocus()
            return True
        else:
            self.outer_diameter = self.value        
        
        if self.check_input_parameters(self.lineEdit_inner_diameter, 'Inner diameter'):
            self.tabWidget_inputs.setCurrentIndex(1)
            self.lineEdit_inner_diameter.setFocus()
            return True
        else:
            self.inner_diameter = self.value        

        if self.check_input_parameters(self.lineEdit_offset_y, 'Offset y', _zero_if_empty=True, _only_positive=False):
            self.tabWidget_inputs.setCurrentIndex(1)
            self.lineEdit_offset_y.setFocus()
            return True
        else:
            self.offset_y = self.value        

        if self.check_input_parameters(self.lineEdit_offset_z, 'Offset z', _zero_if_empty=True, _only_positive=False):
            self.tabWidget_inputs.setCurrentIndex(1)
            self.lineEdit_offset_z.setFocus()
            return True
        else:
            self.offset_z = self.value        

        if self.check_input_parameters(self.lineEdit_insulation_thickness, 'Insulation thickness', _zero_if_empty=True):
            self.tabWidget_inputs.setCurrentIndex(1)
            self.lineEdit_insulation_thickness.setFocus()
            return True
        else:
            self.insulation_thickness = self.value        

        if self.check_input_parameters(self.lineEdit_insulation_density, 'Insulation density', _zero_if_empty=True):
            self.tabWidget_inputs.setCurrentIndex(1)
            self.lineEdit_insulation_density.setFocus()
            return True
        else:
            self.insulation_density = self.value        
        
        return False

    def check_outer_diameter_input(self):
        if self.selection_by_line:
            if self.check_input_parameters(self.lineEdit_outer_diameter_line, 'Outer diameter'):
                self.lineEdit_outer_diameter_line.setFocus()
                self.tabWidget_inputs.setCurrentIndex(0)
                return True
            else:
                self.outer_diameter = self.value
        
        if self.selection_by_node:
            if self.check_input_parameters(self.lineEdit_outer_diameter_node, 'Outer diameter'):
                self.lineEdit_outer_diameter_node.setFocus()
                self.tabWidget_inputs.setCurrentIndex(1)
                return True
            else:
                self.outer_diameter = self.value
        
        if self.selection_by_element:
            if self.check_input_parameters(self.lineEdit_outer_diameter_element, 'Outer diameter'):
                self.lineEdit_outer_diameter_element.setFocus()
                self.tabWidget_inputs.setCurrentIndex(2)
                return True
            else:
                self.outer_diameter = self.value
                
        return False

    def add_flange_to_selected_elements(self):

        if self.check_selection_type():
            return

        self.checkBox_event_update()

        if self.flag_checkBox:
            if self.check_outer_diameter_input():
                return
        else:
            if self.check_all_cross_section_parameters():
                return           
            
        if self.selection_by_line:
            list_elements = self.get_elements_from_start_end_line()

        elif self.selection_by_node:            
            list_elements = self.get_neighbors_elements_from_nodes()

        elif self.selection_by_element:
            list_elements = self.elementID

        if self.set_flange_cross_section_to_list_elements(list_elements):
            return
        
        self.actions_to_finalize(list_elements)

    def set_flange_cross_section_to_list_elements(self, list_elements):
        section_parameters = {}

        for element_id in list_elements:
            element = self.structural_elements[element_id]
            if self.flag_checkBox:
                cross_section = element.cross_section
                if cross_section is None:
                    section_parameters = {}
                    return True
                else:
                    outer_diameter = self.outer_diameter
                    inner_diameter = cross_section.inner_diameter
                    thickness = (self.outer_diameter - inner_diameter)/2
                    offset_y = cross_section.offset_y
                    offset_z = cross_section.offset_z
                    insulation_thickness = cross_section.insulation_thickness
                    insulation_density = cross_section.insulation_density
            else:
                outer_diameter = self.outer_diameter
                inner_diameter = self.inner_diameter
                thickness = (outer_diameter - inner_diameter)/2
                offset_y = self.offset_y
                offset_z = self.offset_z
                insulation_thickness = self.insulation_thickness
                insulation_density = self.insulation_density   

            if outer_diameter <= inner_diameter:
                section_parameters = {}
                title = "Invalid input to the outer/inner diameters"
                message = "The outer diameter input should be greater than the inner diameter. \n"
                message += "This condition must be satified to proceed."
                PrintMessageInput([window_title_1, title, message])
                return True

            section_parameters[element_id] = {  "outer_diameter" : outer_diameter,
                                                "thickness" : thickness, 
                                                "offset_y" : offset_y, 
                                                "offset_z" : offset_z, 
                                                "insulation_thickness" : insulation_thickness, 
                                                "insulation_density" : insulation_density  }             
                    
        for element_id in list_elements:

            pipe_section_info = {   "section_type_label" : "Pipe section" ,
                                    "section_parameters" : section_parameters[element_id]  }

            self.cross_section = CrossSection(pipe_section_info=pipe_section_info)
            self.project.set_cross_section_by_elements([element_id], self.cross_section)

        return False

    def actions_to_finalize(self, list_elements):
        self.project.add_cross_sections_expansion_joints_valves_in_file(list_elements)
        self.preprocessor.add_lids_to_variable_cross_sections()
        self.opv.update_section_radius()
        self.opv.plot_entities_with_cross_section()   
        self.close()