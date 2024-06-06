from PyQt5.QtWidgets import QDialog, QCheckBox, QComboBox, QLabel, QLineEdit, QPushButton, QSpinBox, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.preprocessing.cross_section import CrossSection
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

import numpy as np
from copy import deepcopy
from collections import defaultdict 

window_title_1 = "Error"
window_title_2 = "Warning"

class ConnectingFlangesInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/structural/connecting_flanges_input.ui"
        uic.loadUi(ui_path, self)

        self.main_window = app().main_window
        self.project = app().project
        self.opv = app().main_window.opv_widget
        self.opv.setInputObject(self)

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.update()
        self.exec()
        
    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("OpenPulse")
    
    def _initialize(self):

        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()
        self.preprocessor._map_lines_to_nodes()

        self.element_size = self.project.file._element_size
        self.complete = False
        self.allow_to_update = True
        self.multiple_selection = False

    def _define_qt_variables(self):

        # QCheckBox
        self.checkBox_get_cross_section : QCheckBox

        # QComboBox
        self.comboBox_ending_setup : QComboBox
        self.comboBox_selection_type : QComboBox

        # QLabel
        self.label_selected_id : QLabel
        self.label_number_elements : QLabel
        self.label_first : QLabel
        self.label_last : QLabel

        # QLineEdit
        self.lineEdit_selected_id : QLineEdit

        self.lineEdit_element_size_line : QLineEdit
        self.lineEdit_flange_length_line : QLineEdit
        self.lineEdit_outer_diameter_line : QLineEdit
        self.lineEdit_first_node : QLineEdit
        self.lineEdit_last_node : QLineEdit

        self.lineEdit_element_size_node : QLineEdit
        self.lineEdit_flange_length_node : QLineEdit
        self.lineEdit_outer_diameter_node : QLineEdit
        self.lineEdit_outer_diameter_element : QLineEdit

        self.lineEdit_outer_diameter : QLineEdit
        self.lineEdit_inner_diameter : QLineEdit
        self.lineEdit_offset_y : QLineEdit
        self.lineEdit_offset_z : QLineEdit
        self.lineEdit_insulation_thickness : QLineEdit
        self.lineEdit_insulation_density : QLineEdit

        # QPushButton
        self.pushButton_confirm : QPushButton

        # QSpinBox
        self.spinBox_number_elements_line : QSpinBox
        self.spinBox_number_elements_node : QSpinBox

        # QTabWidget
        self.tabWidget_inputs : QTabWidget

        # QTreeWidget
        self.treeWidget_flange_by_elements : QTreeWidget

    def _create_connections(self):
        self.checkBox_get_cross_section.clicked.connect(self.checkBox_event_update)
        self.comboBox_selection_type.currentIndexChanged.connect(self.selection_type_callback)
        self.pushButton_confirm.clicked.connect(self.add_flange_to_selected_elements)
        self.spinBox_number_elements_line.valueChanged.connect(self.update_flange_length_line)
        self.spinBox_number_elements_node.valueChanged.connect(self.update_flange_length_node)

    def _config_widgets(self):
        self.lineEdit_element_size_line.setText(str(self.element_size))
        self.lineEdit_element_size_node.setText(str(self.element_size))
        self.tabWidget_inputs.setTabVisible(1, False)
        self.tabWidget_inputs.setTabVisible(2, False)
        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")

    def checkBox_event_update(self):

        if self.checkBox_get_cross_section.isChecked():
            self.tabWidget_inputs.setTabVisible(3, True)
        else:
            self.tabWidget_inputs.setTabVisible(3, False)

        tab_index = self.comboBox_selection_type.currentIndex()

        if tab_index == 0:
            if self.lineEdit_outer_diameter_line.text() != "":
                outer_diameter = self.lineEdit_outer_diameter_line.text()
                self.lineEdit_outer_diameter.setText(outer_diameter) 

        elif tab_index == 1:
            if self.lineEdit_outer_diameter_node.text() != "":
                outer_diameter = self.lineEdit_outer_diameter_node.text()
                self.lineEdit_outer_diameter.setText(outer_diameter) 

        elif tab_index == 2:
            if self.lineEdit_outer_diameter_element.text() != "":
                outer_diameter = self.lineEdit_outer_diameter_element.text()
                self.lineEdit_outer_diameter.setText(outer_diameter)    

    def selection_type_callback(self):

        line_id = self.opv.getListPickedLines()
        node_id = self.opv.getListPickedPoints()
        element_id = self.opv.getListPickedElements()

        self.lineEdit_selected_id.setText("")
        self.tabWidget_inputs.setTabVisible(0, False)
        self.tabWidget_inputs.setTabVisible(1, False)
        self.tabWidget_inputs.setTabVisible(2, False)

        selection_index = self.comboBox_selection_type.currentIndex()

        if selection_index == 0:

            self.tabWidget_inputs.setTabVisible(0, True)
            self.tabWidget_inputs.setCurrentIndex(0)
            self.label_selected_id.setText("Lines ID:")

            if not self.opv.change_plot_to_entities_with_cross_section:
                self.opv.plot_entities_with_cross_section()
                if len(line_id):
                    self.opv.opvRenderer.highlight_lines(line_id)

        elif selection_index == 1:

            self.tabWidget_inputs.setTabVisible(1, True)
            self.tabWidget_inputs.setCurrentIndex(1)
            self.label_selected_id.setText("Nodes ID:")

            if not self.opv.change_plot_to_mesh:
                self.main_window.update_plot_mesh()
                if len(node_id):
                    self.opv.opvRenderer.highlight_nodes(node_id)

        elif selection_index == 2:
            self.tabWidget_inputs.setTabVisible(2, True)
            self.tabWidget_inputs.setCurrentIndex(2)
            self.label_selected_id.setText("Elements ID:")

            if not self.opv.change_plot_to_mesh:
                self.main_window.update_plot_mesh()
                if element_id:
                    self.opv.opvRenderer.highlight_elements(element_id)

        if self.allow_to_update:
            self.update()

    def update(self):

        line_id = self.opv.getListPickedLines()
        node_id = self.opv.getListPickedPoints()
        element_id = self.opv.getListPickedElements()

        if node_id and element_id:
            title = "Multiples node(s) and element(s) in selection"
            message = "The current selection includes multiples node(s) and element(s). "
            message += "You should to select node(s) or element(s) separately to proceed. "
            self.multiple_selection = True
            self.reset_selection()
            PrintMessageInput([window_title_1, title, message])
            return

        elif line_id:
            node_id = []
            element_id = []
            self.allow_to_update = False
            self.comboBox_selection_type.setCurrentIndex(0)

        elif node_id:
            line_id = []
            element_id = []
            self.allow_to_update = False
            self.comboBox_selection_type.setCurrentIndex(1)

        elif element_id:
            line_id = []
            node_id = []
            self.allow_to_update = False
            self.comboBox_selection_type.setCurrentIndex(2)

        else:
            return

        self.allow_to_update = True

        try:

            if line_id:

                if self.write_ids(line_id):
                    self.lineEdit_selected_id.setText("")
                    self.lineEdit_first_node.setText("")
                    self.lineEdit_last_node.setText("")
                    return

                self.update_flange_length_line()
                self.get_elements_from_start_end_line()
                
                if len(line_id) == 1:
                    first_node = self.preprocessor.dict_line_to_nodes[line_id[0]][0]
                    last_node = self.preprocessor.dict_line_to_nodes[line_id[0]][1]
                    self.lineEdit_first_node.setText(str(first_node))
                    self.lineEdit_last_node.setText(str(last_node))

                else:
                    self.lineEdit_first_node.setText("multiples")
                    self.lineEdit_last_node.setText("multiples")

                if self.comboBox_ending_setup.currentIndex() == 1:
                    self.lineEdit_last_node.setText("---")

                if self.comboBox_ending_setup.currentIndex() == 2:
                    self.lineEdit_first_node.setText("---")

            elif node_id:

                if self.write_ids(node_id):
                    self.lineEdit_selected_id.setText("")
                    return

                self.update_flange_length_node()

            elif element_id :

                if self.write_ids(element_id):
                    self.lineEdit_selected_id.setText("")
                    return

                self.load_elements_treeWidget_info()

        except Exception as log_error:
            title = "Error in 'update' function"
            message = str(log_error) 
            PrintMessageInput([window_title_1, title, message])

    def update_flange_length_line(self):
        self.flange_length = self.spinBox_number_elements_line.value()*self.element_size
        self.lineEdit_flange_length_line.setText(str(self.flange_length))

    def update_flange_length_node(self):
        self.flange_length = self.spinBox_number_elements_node.value()*self.element_size
        self.lineEdit_flange_length_node.setText(str(self.flange_length))

    def reset_selection(self):
        self.lineEdit_selected_id.setText("")
        self.treeWidget_flange_by_elements.clear()
        self.main_window.update_plot_mesh()

    def get_elements_from_start_end_line(self):
        number_elements = self.spinBox_number_elements_line.value()
        _list_elements = []

        for line_id in self.opv.getListPickedLines():  
            elements_from_line = np.sort(self.preprocessor.line_to_elements[line_id])
            elements_from_start = elements_from_line[0:number_elements]
            elements_from_end = elements_from_line[-number_elements:]

            if self.comboBox_ending_setup.currentIndex() == 0:
                for element_id_start in elements_from_start:
                    _list_elements.append(element_id_start)
                for element_id_end in elements_from_end:
                    _list_elements.append(element_id_end)
            
            elif self.comboBox_ending_setup.currentIndex() == 1:
                for element_id_start in elements_from_start:
                    _list_elements.append(element_id_start)
                
            elif self.comboBox_ending_setup.currentIndex() == 2:
                for element_id_end in elements_from_end:
                    _list_elements.append(element_id_end)

        return _list_elements

    def get_neighbors_elements_from_nodes(self):
        self.update_flange_length_node()
        list_all_elements = []
        self.node_to_elements_inside_flange_length = defaultdict(list)
        for node_id in self.opv.getListPickedPoints():
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
        for element_id in self.opv.getListPickedElements():
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
        lineEdit_selection = self.lineEdit_selected_id.text()

        selection_index = self.comboBox_selection_type.currentIndex()
        if selection_index == 0:
            _stop, self.lineID = self.before_run.check_input_LineID(lineEdit_selection)
            for line_id in self.lineID:
                entity = self.preprocessor.dict_tag_to_entity[line_id]
                if entity.structural_element_type in ["beam_1", "expansion_joint"]:
                    _stop = True
                    break
                   
        elif selection_index == 1:
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

        elif selection_index == 2:
            _stop, self.elementID = self.before_run.check_input_ElementID(lineEdit_selection)
            for element_id in self.elementID:
                element = self.preprocessor.structural_elements[element_id]
                if element.element_type in ["beam_1", "expansion_joint"]:
                    _stop = True
                    break

        if _stop:
            self.lineEdit_selected_id.setText("")
            self.lineEdit_selected_id.setFocus()
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
            message = f"An empty entry has been detected at the '{label}' input field. " 
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

        selection_index = self.comboBox_selection_type.currentIndex()
        if selection_index == 0:
            if self.check_input_parameters(self.lineEdit_outer_diameter_line, 'Outer diameter'):
                self.lineEdit_outer_diameter_line.setFocus()
                self.tabWidget_inputs.setCurrentIndex(0)
                return True
            else:
                self.outer_diameter = self.value

        elif selection_index == 1:
            if self.check_input_parameters(self.lineEdit_outer_diameter_node, 'Outer diameter'):
                self.lineEdit_outer_diameter_node.setFocus()
                self.tabWidget_inputs.setCurrentIndex(1)
                return True
            else:
                self.outer_diameter = self.value

        elif selection_index == 2:
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

        if self.checkBox_get_cross_section.isChecked():
            if self.check_outer_diameter_input():
                return
        else:
            if self.check_all_cross_section_parameters():
                return 
                      
        selection_index = self.comboBox_selection_type.currentIndex()    
        if selection_index == 0:
            list_elements = self.get_elements_from_start_end_line()

        elif selection_index == 1:            
            list_elements = self.get_neighbors_elements_from_nodes()

        elif selection_index == 2:
            list_elements = self.elementID

        if self.set_flange_cross_section_to_list_elements(list_elements):
            return
        
        self.actions_to_finalize(list_elements)

    def set_flange_cross_section_to_list_elements(self, list_elements):

        section_parameters = {}
        for element_id in list_elements:
            element = self.preprocessor.structural_elements[element_id]
            if self.checkBox_get_cross_section.isChecked():

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
                title = "Invalid input to the outer/inner diameters"
                message = "The outer diameter input should be greater than the inner diameter. "
                message += "This condition must be satified to proceed."
                PrintMessageInput([window_title_1, title, message])
                return True

            section_parameters[element_id] = [  outer_diameter, 
                                                thickness, 
                                                offset_y, 
                                                offset_z, 
                                                insulation_thickness, 
                                                insulation_density  ]             

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

    def write_ids(self, list_selected_ids):
        text = ""
        for _id in list_selected_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_id.setText(text[:-2])  
        if self.check_selection_type():
            return True
        return False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_main.currentIndex() == 0:
                self.add_flange_to_selected_elements()

        elif event.key() == Qt.Key_Escape:
            self.close()