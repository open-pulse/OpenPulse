from PyQt5.QtWidgets import QDialog, QCheckBox, QFrame, QLabel, QLineEdit, QPushButton, QRadioButton, QSpinBox, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

from data.user_input.model.setup.acoustic.perforatedPlateInput import PerforatedPlateInput
from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.before_run import BeforeRun
from pulse.utils import get_V_linear_distribution, remove_bc_from_file
from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput

window_title_1 = "ERROR MESSAGE"
window_title_2 = "WARNING MESSAGE"

class ValvesInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui_files/Model/Setup/Structural/valvesInput.ui'), self)
        
        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)

        self.project = project
        self.preprocessor = project.preprocessor
        self.before_run = project.get_pre_solution_model_checks()
        self.nodes = self.project.preprocessor.nodes
        self.preprocessor._map_lines_to_nodes()
        self.group_elements_with_valves = self.preprocessor.group_elements_with_valves
        self.group_elements_with_perforated_plate = self.preprocessor.group_elements_with_perforated_plate
        
        self.structural_elements = self.project.preprocessor.structural_elements
   
        self.element_size = self.project.file._element_size
        self.elements_info_path = project.file._element_info_path
        self.stop = False
        self.complete = False
        self.multiple_selection = False
        self.aquisition_parameters_processed = False
        self.node_ID_remove = None
        self.ext_key = None
        self.list_frequencies = []
        self.flange_outer_diameter = None

        self.line_id = self.opv.getListPickedLines()
        self.element_id = self.opv.getListPickedElements()

        self.main_frame = self.findChild(QFrame, 'main_frame')

        self.label_selected_id = self.findChild(QLabel, 'label_selected_id')
        
        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
        self.lineEdit_stiffening_factor_line = self.findChild(QLineEdit, 'lineEdit_stiffening_factor_line')
        self.lineEdit_valve_mass_line = self.findChild(QLineEdit, 'lineEdit_valve_mass_line')

        self.lineEdit_valve_length_line = self.findChild(QLineEdit, 'lineEdit_valve_length_line')
        self.lineEdit_valve_length_element = self.findChild(QLineEdit, 'lineEdit_valve_length_element')
        # self.lineEdit_valve_length_line.setDisabled(False)
        self.lineEdit_stiffening_factor_element = self.findChild(QLineEdit, 'lineEdit_stiffening_factor_element')
        self.lineEdit_valve_mass_element = self.findChild(QLineEdit, 'lineEdit_valve_mass_element') 
        self.lineEdit_valve_mass_line = self.findChild(QLineEdit, 'lineEdit_valve_mass_line') 

        self.lineEdit_flange_length = self.findChild(QLineEdit, 'lineEdit_flange_length')
        self.lineEdit_flange_length.setToolTip("valve_length = number_elements*element_size")
        self.lineEdit_outer_diameter = self.findChild(QLineEdit, 'lineEdit_outer_diameter')

        self.radioButton_line_selection = self.findChild(QRadioButton, 'radioButton_line_selection')
        self.radioButton_element_selection = self.findChild(QRadioButton, 'radioButton_element_selection')
        self.radioButton_line_selection.clicked.connect(self.radioButtonEvent_selection_type)
        self.radioButton_element_selection.clicked.connect(self.radioButtonEvent_selection_type)
        self.selection_by_line = self.radioButton_line_selection.isChecked()
        self.selection_by_element = self.radioButton_element_selection.isChecked()

        self.spinBox_number_elements_flange = self.findChild(QSpinBox, 'spinBox_number_elements_flange') 
        self.spinBox_number_elements_flange.valueChanged.connect(self.update_flange_length)
        self.update_flange_length()

        self.checkBox_add_flanges_to_the_valve = self.findChild(QCheckBox, 'checkBox_add_flanges_to_the_valve')
        self.checkBox_add_flanges_to_the_valve.clicked.connect(self.checkBox_event_update)
        self.flag_checkBox = self.checkBox_add_flanges_to_the_valve.isChecked()

        self.checkBox_enable_acoustic_effects = self.findChild(QCheckBox, 'checkBox_enable_acoustic_effects')
        self.checkBox_enable_acoustic_effects.clicked.connect(self.checkBox_enable_acoustic_effects_event_update)
        self.enable_acoustic_effects = self.checkBox_enable_acoustic_effects.isChecked()

        self.checkBox_remove_valve_acoustic_effects = QCheckBox("Remove valve acoustic effects", self.main_frame)
        self.checkBox_remove_valve_acoustic_effects.setChecked(True)
        self.checkBox_remove_valve_acoustic_effects.setVisible(False)
        self.config_remove_valve_acoustic_effects_checkBox_appearance()

        self.tabWidget_inputs = self.findChild(QTabWidget, 'tabWidget_inputs')
        self.tab_line_selection = self.tabWidget_inputs.findChild(QWidget, "tab_insert_by_line")
        self.tab_element_selection = self.tabWidget_inputs.findChild(QWidget, "tab_insert_by_element")
        self.tab_flange_setup = self.tabWidget_inputs.findChild(QWidget, "tab_flange_setup")
        self.tab_remove = self.tabWidget_inputs.findChild(QWidget, "tab_remove")
        self.tabWidget_inputs.removeTab(2)
        self.treeWidget_valve_remove = self.findChild(QTreeWidget, 'treeWidget_valve_remove')
        self.treeWidget_valve_remove.itemClicked.connect(self.on_click_item_remove)
        self.treeWidget_valve_remove.itemDoubleClicked.connect(self.on_doubleclick_item_remove)
        # self.tabWidget_inputs.addTab(self.tab_line_selection, "Line selection")

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.add_valve_to_selected_elements)

        self.pushButton_reset = self.findChild(QPushButton, 'pushButton_reset')
        self.pushButton_reset.clicked.connect(self.remove_all_valves)

        self.pushButton_remove = self.findChild(QPushButton, 'pushButton_remove')
        self.pushButton_remove.clicked.connect(self.remove_valve_by_selection)

        if len(self.line_id) + len(self.element_id) == 0:
            self.opv.changePlotToEntitiesWithCrossSection()

        self.update()
        # self.checkBox_event_update()
        self.load_valves_info()
        self.tabWidget_inputs.setCurrentIndex(0)
        self.checkBox_enable_acoustic_effects_event_update()
        self.tabWidget_inputs.currentChanged.connect(self.tabEvent_inputs)
        self.exec()

    def tabEvent_inputs(self):

        currentTab = self.tabWidget_inputs.currentWidget()

        if currentTab == self.tab_remove:
            self.checkBox_remove_valve_acoustic_effects.setVisible(True)
            self.checkBox_add_flanges_to_the_valve.setVisible(False)
            self.checkBox_enable_acoustic_effects.setVisible(False)
        else:
            self.checkBox_remove_valve_acoustic_effects.setVisible(False)
            self.checkBox_add_flanges_to_the_valve.setVisible(True)
            self.checkBox_enable_acoustic_effects.setVisible(True)

    def config_remove_valve_acoustic_effects_checkBox_appearance(self):
        font = QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setPointSize(12)
        self.checkBox_add_flanges_to_the_valve.setFont(font)
        self.checkBox_enable_acoustic_effects.setFont(font)
        self.checkBox_remove_valve_acoustic_effects.setFont(font)
        # self.checkBox_remove_valve_acoustic_effects.setStyleSheet("color:black")
        # self.checkBox_remove_valve_acoustic_effects.setText("Remove perforated plate")
        # self.checkBox_remove_valve_acoustic_effects.setGeometry(QRect(175, 300, 150, 36))
        self.checkBox_remove_valve_acoustic_effects.setMinimumSize(QSize(300, 36))
        self.checkBox_remove_valve_acoustic_effects.setMaximumSize(QSize(300, 36))
        self.checkBox_remove_valve_acoustic_effects.move(QPoint(130, 70))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.add_valve_to_selected_elements()
        if event.key() == Qt.Key_Escape:
            self.close()

    def force_to_close(self):
        self.close()

    def checkBox_event_update(self):
        self.flag_checkBox = self.checkBox_add_flanges_to_the_valve.isChecked()
        if self.flag_checkBox:
            self.tabWidget_inputs.addTab(self.tab_flange_setup, 'Flange setup')
        else:
            self.tabWidget_inputs.removeTab(1)
        self.update_remove_tab()

    def update_remove_tab(self):        
        #
        currentIndex = self.tabWidget_inputs.currentIndex()
        number_tabs = self.tabWidget_inputs.count()
        self.tabWidget_inputs.setCurrentIndex(number_tabs-1)
        currentTab = self.tabWidget_inputs.currentWidget()
        #
        if currentTab == self.tab_remove:
            if len(self.preprocessor.group_elements_with_valves) == 0:
                self.tabWidget_inputs.removeTab(number_tabs-1) 
                self.tabWidget_inputs.setCurrentIndex(0)
        else:     
            if len(self.preprocessor.group_elements_with_valves) != 0:
                self.tabWidget_inputs.addTab(self.tab_remove, "Remove")
                self.tabWidget_inputs.setCurrentIndex(0)  
            else:
                self.tabWidget_inputs.setCurrentIndex(currentIndex)      

    def checkBox_enable_acoustic_effects_event_update(self):
        self.enable_acoustic_effects = self.checkBox_enable_acoustic_effects.isChecked()

    def radioButtonEvent_selection_type(self): 
        self.line_id = []
        self.element_id = []
        self.lineEdit_selected_ID.setText("")
        
        if self.radioButton_line_selection.isChecked():
            self.opv.changePlotToEntitiesWithCrossSection()

        if self.radioButton_element_selection.isChecked():
            self.opv.changePlotToMesh()

        self.opv.update()

        self.update_selection_flags()
        self.update_selected_id()
        self.update_selection_texts_info()    

    def update_valve_length_line_selection(self):
        valve_length = self.spinBox_number_elements_flange.value()*self.element_size
        self.lineEdit_flange_length.setText(str(valve_length))
 
    def update_flange_length(self):
        self.flange_length = self.spinBox_number_elements_flange.value()*self.element_size
        self.lineEdit_flange_length.setText(str(round(self.flange_length,6)))

    def update(self):
        self.update_selected_id()
        self.update_selection_flags()
        self.checkBox_event_update()
        self.update_selection_texts_info()
                    
    def update_selected_id(self): 
        if self.opv.getListPickedLines() != []:
            self.line_id = self.opv.getListPickedLines()
            self.element_id = []
        elif self.opv.getListPickedElements() != []:
            self.element_id = self.opv.getListPickedElements()
            self.line_id = []
        self.process_tabs_after_selection()

    def reset_selection(self):
        self.lineEdit_selected_ID.setText("")
        self.line_id = []
        self.element_id = []
        self.opv.changePlotToMesh()

    def process_tabs_after_selection(self):
        if self.line_id != []:
            self.radioButton_line_selection.setChecked(True)
        elif self.element_id != []:
            self.radioButton_element_selection.setChecked(True)

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
            self.checkBox_event_update()
            _state = [self.selection_by_line, self.selection_by_element] 
            for i, label in enumerate(["Line ID:", "Element ID:"]):
                if _state[i]:
                    self.label_selected_id.setText(label)
            
            if self.selection_by_line:
                if self.line_id != []:
                    self.lineEdit_selected_ID.setText("")
                    if self.write_ids(self.line_id):
                        return
                    self.radioButton_line_selection.setChecked(True)
                    if len(self.line_id) == 1:
                        self.get_line_length()
                        self.update_valve_info()
                    else:
                        self.lineEdit_valve_length_line.setText("multiples")

            if self.selection_by_element:
                if self.element_id != []:
                    self.lineEdit_selected_ID.setText("")
                    if self.write_ids(self.element_id):
                        return
                    self.update_valve_info()
                    self.radioButton_element_selection.setChecked(True)

        except Exception as log_error:
            print(str(log_error))

    def update_selection_flags(self):

        if self.opv.change_plot_to_mesh and self.radioButton_line_selection.isChecked():
            self.opv.changePlotToEntitiesWithCrossSection()
        self.selection_by_line = self.radioButton_line_selection.isChecked()
        self.selection_by_element = self.radioButton_element_selection.isChecked()
        
        self.tabWidget_inputs.clear()
        if self.selection_by_line:
            self.tabWidget_inputs.addTab(self.tab_line_selection, "Line selection")
            if self.opv.change_plot_to_mesh:
                self.opv.changePlotToEntitiesWithCrossSection()
     
        if self.selection_by_element:
            if not self.opv.change_plot_to_mesh:
                self.opv.changePlotToMesh()
            if self.opv.getListPickedPoints() != []:
                self.opv.changePlotToMesh()
            self.tabWidget_inputs.addTab(self.tab_element_selection, "Element selection")

        return False

    def get_line_length(self):
        lineEdit_lineID = self.lineEdit_selected_ID.text()
        if lineEdit_lineID != "":
            self.stop, _line_id = self.before_run.check_input_LineID(lineEdit_lineID, single_ID=True)
            if self.stop:
                self.lineEdit_selected_ID.setText("")
                self.lineEdit_valve_length_line.setText("")
                self.lineEdit_selected_ID.setFocus()
                return True  
            joint_length, _ = self.preprocessor.get_line_length(_line_id) 
            self.lineEdit_valve_length_line.setText(str(round(joint_length,6)))
    
    def update_valve_info(self):
        
        valve_parameters = None
        if len(self.line_id) == 1:
            
            line = self.line_id[0]
            entity = self.preprocessor.dict_tag_to_entity[line]
            
            if entity.valve_parameters:
                valve_parameters = entity.valve_parameters
                valve_length = valve_parameters["valve_length"]
                self.lineEdit_valve_length_line.setText(str(valve_length))

                valve_mass = valve_parameters["valve_mass"]
                self.lineEdit_valve_mass_line.setText(str(valve_mass))

                stiffening_factor = valve_parameters["stiffening_factor"]
                self.lineEdit_stiffening_factor_line.setText(str(stiffening_factor))

        elif len(self.element_id) == 1:

            element_id = self.element_id[0]
            element = self.structural_elements[element_id]
            
            if element.valve_parameters:
                valve_parameters = element.valve_parameters
            
                valve_length = valve_parameters["valve_length"]
                self.lineEdit_valve_length_element.setText(str(valve_length))

                valve_mass = valve_parameters["valve_mass"]
                self.lineEdit_valve_mass_element.setText(str(valve_mass))

                stiffening_factor = valve_parameters["stiffening_factor"]
                self.lineEdit_stiffening_factor_element.setText(str(stiffening_factor))
      
        if valve_parameters:
                    
            if "flange_section_parameters" in valve_parameters.keys():
                
                flange_outer_diameter = valve_parameters["flange_section_parameters"]["outer_diameter"]
                self.lineEdit_outer_diameter.setText(str(flange_outer_diameter))
                
                N = len(self.list_flange_elements)
                self.spinBox_number_elements_flange.setValue(N)

                flange_length = N*self.element_size
                self.lineEdit_flange_length.setText(str(round(flange_length,6)))

    def check_flanges_by_lines(self):
        elements_from_line = defaultdict(list)
        for element_id in self.element_id:
            line = self.preprocessor.elements_to_line[element_id]
            elements_from_line[line].append(element_id)
        return elements_from_line

    def check_selection_type(self):

        _stop = False
        lineEdit_selection = self.lineEdit_selected_ID.text()

        if self.selection_by_line:
            _stop, self.lineID = self.before_run.check_input_LineID(lineEdit_selection)
            for line_id in self.lineID:
                entity = self.preprocessor.dict_tag_to_entity[line_id]
                if entity.structural_element_type in ["beam_1"]:
                    _stop = True
                    break
                   
        elif self.selection_by_element:
            _stop, self.elementID = self.before_run.check_input_ElementID(lineEdit_selection)
            for element_id in self.elementID:
                element = self.structural_elements[element_id]
                if element.element_type in ["beam_1"]:
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
            PrintMessageInput([title, message, window_title_1])
            return True
        else:
            return False

    def check_flange_parameters(self):
        if self.check_input_parameters(self.lineEdit_flange_length, 'Flange length'):
            self.tabWidget_inputs.setCurrentIndex(1)
            self.lineEdit_flange_length.setFocus()
            return True
        else:
            self.flange_length = self.value 

        if self.check_input_parameters(self.lineEdit_outer_diameter, 'Outer flange diameter'):
            self.tabWidget_inputs.setCurrentIndex(1)
            self.lineEdit_outer_diameter.setFocus()
            return True
        else:
            self.flange_outer_diameter = self.value        
        
        # if self.check_input_parameters(self.lineEdit_inner_diameter, 'Inner diameter'):
        #     self.tabWidget_inputs.setCurrentIndex(1)
        #     self.lineEdit_inner_diameter.setFocus()
        #     return True
        # else:
        #     self.flange_inner_diameter = self.value                
        
        return False

    def check_valve_parameters(self):

        if self.selection_by_line:
            if self.check_input_parameters(self.lineEdit_valve_length_line, 'Valve length'):
                self.lineEdit_valve_length_line.setFocus()
                self.tabWidget_inputs.setCurrentIndex(0)
                return True
            else:
                self.valve_length = self.value        

            if self.check_input_parameters(self.lineEdit_valve_mass_line, 'Valve mass'):
                self.lineEdit_valve_mass_line.setFocus()
                self.tabWidget_inputs.setCurrentIndex(0)
                return True
            else:
                self.valve_mass = self.value

            if self.check_input_parameters(self.lineEdit_stiffening_factor_line, 'Stiffening factor'):
                self.lineEdit_stiffening_factor_line.setFocus()
                self.tabWidget_inputs.setCurrentIndex(0)
                return True
            else:
                self.stiffening_factor = self.value

        if self.selection_by_element:
            if self.check_input_parameters(self.lineEdit_valve_length_element, 'Valve length'):
                self.lineEdit_valve_length_element.setFocus()
                self.tabWidget_inputs.setCurrentIndex(0)
                return True
            else:
                self.valve_length = self.value        

            if self.check_input_parameters(self.lineEdit_valve_mass_element, 'Valve mass'):
                self.lineEdit_valve_mass_element.setFocus()
                self.tabWidget_inputs.setCurrentIndex(0)
                return True
            else:
                self.valve_mass = self.value

            if self.check_input_parameters(self.lineEdit_stiffening_factor_element, 'Stiffening factor'):
                self.lineEdit_stiffening_factor_element.setFocus()
                self.tabWidget_inputs.setCurrentIndex(0)
                return True
            else:
                self.stiffening_factor = self.value

    def get_start_end_elements_from_line(self, line_id):
        number_flange_elements = self.spinBox_number_elements_flange.value()
        elements_from_line = np.sort(self.preprocessor.line_to_elements[line_id])
        if number_flange_elements < len(elements_from_line): 
            lists_elements = [  elements_from_line[:number_flange_elements], 
                                elements_from_line[-number_flange_elements:]  ]
            list_flange_elements = [_id for list_elements in lists_elements for _id in list_elements]
            return list_flange_elements
        else:
            title = "Invalid number of flange elements"
            message = "The selected number of flange elements must be less than the line number of elements. "
            message += "We recommend reducing the flange number of elements to proceed.\n"
            message += f"\nLine: {line_id}"
            message += f"\nNumber of elements: {number_flange_elements}"
            PrintMessageInput([title, message, window_title_1])
            return []

    def get_valve_diameters(self, valve_diameter):
        number_valve_elements = len(self.list_valve_elements)
        number_flange_elements = len(self.list_flange_elements)
        N = number_valve_elements - number_flange_elements
        dict_diameters = {}
        if number_flange_elements == 0:
            list_outer_diameters =  get_V_linear_distribution(valve_diameter, N)
            list_inner_diameters = list_outer_diameters - 2*self.valve_thickness
        else:
            nf = int(number_flange_elements/2)
            list_outer_diameters = np.ones(number_valve_elements)*self.flange_outer_diameter
            list_inner_diameters = list_outer_diameters - 2*self.flange_thickness
            list_outer_diameters[nf:-nf] = get_V_linear_distribution(valve_diameter, N)
            list_inner_diameters[nf:-nf] = list_outer_diameters[nf:-nf] - 2*self.valve_thickness 
        for i, element_id in enumerate(self.list_valve_elements):
            dict_diameters[element_id] = [list_outer_diameters[i], list_inner_diameters[i]]
        return dict_diameters

    def add_valve_to_selected_elements(self):

        if self.check_selection_type():
            return

        if self.check_valve_parameters():
            return

        self.checkBox_event_update()

        if self.flag_checkBox:
            if self.check_flange_parameters():
                return   

        if self.enable_acoustic_effects:
            if self.selection_by_element:
                valve_ids = self.elementID
            elif self.selection_by_line:
                valve_ids = []
                for line_id in self.lineID:    
                    list_elements = self.preprocessor.line_to_elements[line_id]
                    N = len(list_elements)
                    if np.remainder(N, 2) == 0:
                        index = int(N/2)
                        half_ids = list_elements[index]
                    else:
                        index = int((N-1)/2)
                        half_ids = list_elements[index]
                    valve_ids.append(half_ids)
                
            pp = PerforatedPlateInput(self.project, self.opv, valve_ids=valve_ids) 
            if not pp.complete:
                return 

        valve_parameters = {} 
        self.inner_diameter = 0
        none_pipe_section = False    
         
        if self.selection_by_line:
            for line_id in self.lineID:
                
                if self.checkBox_add_flanges_to_the_valve.isChecked():
                    self.list_flange_elements = self.get_start_end_elements_from_line(line_id)
                    if self.list_flange_elements == []:
                        return
                joint_length, edge_nodes = self.preprocessor.get_line_length(line_id) 
                self.lineEdit_valve_length_line.setText(str(round(joint_length, 6)))
                self.valve_center_coordinates = list(np.round((edge_nodes[0].coordinates + edge_nodes[1].coordinates)/2, decimals=6))
            
                self.list_valve_elements = list(self.preprocessor.line_to_elements[line_id])
                valve_section_parameters = self.search_for_cross_section_in_neighborhood(self.list_valve_elements)

                if valve_section_parameters:
                
                    self.valve_outer_diameter = valve_section_parameters["outer_diameter"]
                    self.valve_thickness = valve_section_parameters["thickness"]
                    self.flange_thickness = round((self.flange_outer_diameter - self.inner_diameter)/2, 6)
                    valve_diameters = self.get_valve_diameters(self.valve_outer_diameter)

                    if self.checkBox_add_flanges_to_the_valve.isChecked():                
                        
                        valve_parameters[line_id] = {   "valve_elements" : self.list_valve_elements,
                                                        "number_flange_elements" : len(self.list_flange_elements),
                                                        "flange_elements" : self.list_flange_elements,
                                                        "valve_section_parameters" : valve_section_parameters,  
                                                        "valve_length" : self.valve_length,
                                                        "stiffening_factor" : self.stiffening_factor,
                                                        "valve_mass" : self.valve_mass,
                                                        "valve_center_coordinates" : self.valve_center_coordinates,
                                                        "flange_section_parameters" : self.flange_outer_diameter,
                                                        "valve_diameters" : valve_diameters   }
                    
                    else:
                        
                        valve_parameters[line_id] = {   "valve_elements" : self.list_valve_elements,
                                                        "valve_section_parameters" : valve_section_parameters,  
                                                        "valve_length" : self.valve_length,
                                                        "stiffening_factor" : self.stiffening_factor,
                                                        "valve_mass" : self.valve_mass,
                                                        "valve_center_coordinates" : self.valve_center_coordinates,
                                                        "valve_diameters" : valve_diameters   }
                
                    if self.set_valve_by_lines(valve_parameters):
                        return
                else:
                    none_pipe_section = True

        if self.selection_by_element:
            for element_id in self.elementID:
                self.valve_center_coordinates = list(np.round(self.structural_elements[element_id].element_center_coordinates, decimals=6))
                _, self.list_valve_elements = self.preprocessor.get_neighbor_nodes_and_elements_by_element(element_id, self.valve_length)
                number_valve_elements = len(self.list_valve_elements)
                
                if self.check_previous_attributions_to_elements(self.list_valve_elements):
                    return
                
                number_flange_elements = self.spinBox_number_elements_flange.value()
                if self.check_number_valve_and_flange_elements(number_valve_elements, number_flange_elements):
                    return

                lists_elements = [  self.list_valve_elements[:number_flange_elements], 
                                    self.list_valve_elements[-number_flange_elements:]  ]
                self.list_flange_elements = [_id for list_elements in lists_elements for _id in list_elements]
                valve_section_parameters = self.search_for_cross_section_in_neighborhood(self.list_valve_elements, set_by_elements=True)

                if valve_section_parameters:
                    self.valve_outer_diameter = valve_section_parameters["outer_diameter"]
                    self.valve_thickness = valve_section_parameters["thickness"]
                    self.flange_thickness = round((self.flange_outer_diameter - self.inner_diameter)/2, 6) 
                    valve_diameters = self.get_valve_diameters(self.valve_outer_diameter)

                    if self.checkBox_add_flanges_to_the_valve.isChecked():

                        valve_parameters[element_id] = {"valve_elements" : self.list_valve_elements,
                                                        "number_flange_elements" : len(self.list_flange_elements),
                                                        "flange_elements" : self.list_flange_elements,
                                                        "valve_section_parameters" : valve_section_parameters,
                                                        "valve_length" : self.valve_length,
                                                        "stiffening_factor" : self.stiffening_factor,
                                                        "valve_mass" : self.valve_mass,
                                                        "valve_center_coordinates" : self.valve_center_coordinates,
                                                        "flange_section_parameters" : self.flange_outer_diameter,
                                                        "valve_diameters" : valve_diameters}

                    else:
                        
                        valve_parameters[line_id] = {   "valve_elements" : self.list_valve_elements,
                                                        "valve_section_parameters" : valve_section_parameters,  
                                                        "valve_length" : self.valve_length,
                                                        "stiffening_factor" : self.stiffening_factor,
                                                        "valve_mass" : self.valve_mass,
                                                        "valve_center_coordinates" : self.valve_center_coordinates,
                                                        "valve_diameters" : valve_diameters   }

                    if self.set_valve_by_elements(valve_parameters):
                        return
                else:
                    none_pipe_section = True
 
        if none_pipe_section:
            title = "No pipe cross-section has been detected in the valve neighborhood"
            message = "There are no pipe cross-sections defined in the valve neighbor elements. " 
            message += "You must define cross-sections to the neighbor valve elements to proceed."    
            PrintMessageInput([title, message, window_title_2])
        else:
            self.actions_to_finalize()

    def set_valve_by_lines(self, valve_data):
        message = ""
        for line_id, data in valve_data.items():
            valve_elements = data["valve_elements"]
            valve_diameters = data["valve_diameters"] 
            valve_section_parameters = data["valve_section_parameters"]
            outer_diameter = valve_section_parameters["outer_diameter"]
            if self.checkBox_add_flanges_to_the_valve.isChecked():
                flange_outer_diameter = data["flange_section_parameters"]
                offset_y = valve_section_parameters["offset_y"]
                offset_z = valve_section_parameters["offset_z"]
                if outer_diameter != 0:
                    if flange_outer_diameter <= self.inner_diameter:
                        title = "Invalid input to the outer/inner diameters"
                        message = "The outer diameter input should be greater than the inner diameter. \n"
                        message += "This condition must  be satified to proceed."
                        PrintMessageInput([title, message, window_title_1])
                        return True
                    else:
                        outer_diameter = self.flange_outer_diameter
                        thickness = round((self.flange_outer_diameter - self.inner_diameter)/2, 6)
                        flange_section_parameters = {   "outer_diameter" : outer_diameter,
                                                        "thickness" : thickness, 
                                                        "offset_y" : offset_y, 
                                                        "offset_z" : offset_z, 
                                                        "insulation_thickness" : 0, 
                                                        "insulation_density" : 0   }    
                        data["flange_section_parameters"] = flange_section_parameters
                    self.project.add_valve_by_line(line_id, data)
                    if self.set_cross_section_to_list_elements(self.list_flange_elements, flange_section_parameters, valve_diameters):
                        return
                    _valve_elements = [element_id for element_id in valve_elements if element_id not in self.list_flange_elements]
                    if self.set_cross_section_to_list_elements(_valve_elements, valve_section_parameters, valve_diameters):
                        return
                else:
                    title = "None cross-section defined"
                    message = "The selected lines or elements has no cross-section defined. "
                    message += "Please, define a pipe cross-section before proceed."   
            else:
                if outer_diameter != 0:
                    self.project.add_valve_by_line(line_id, data)
                    if self.set_cross_section_to_list_elements(valve_elements, valve_section_parameters, valve_diameters):
                        return
                else:
                    title = "None cross-section defined"
                    message = "The selected lines or elements has no cross-section defined. "
                    message += "Please, define a pipe cross-section before proceed."
            
            if message != "":
                PrintMessageInput([title, message, window_title_1])
                return True

    def set_valve_by_elements(self, valve_data):
        message = ""
        for data in valve_data.values():
            valve_elements = data["valve_elements"]  
            valve_diameters = data["valve_diameters"]
            valve_section_parameters = data["valve_section_parameters"]
            outer_diameter = valve_section_parameters["outer_diameter"]
            if self.checkBox_add_flanges_to_the_valve.isChecked():
                flange_outer_diameter = data["flange_section_parameters"]
                offset_y = valve_section_parameters["offset_y"]
                offset_z = valve_section_parameters["offset_z"]
                if outer_diameter != 0:
                    if flange_outer_diameter <= self.inner_diameter:
                        title = "Invalid input to the outer/inner diameters"
                        message = "The outer diameter input should be greater than the inner diameter. \n"
                        message += "This condition must  be satified to proceed."
                        PrintMessageInput([title, message, window_title_1])
                        return True
                    else:
                        outer_diameter = self.flange_outer_diameter
                        thickness = round((self.flange_outer_diameter - self.inner_diameter)/2, 6)
                        flange_section_parameters = {   "outer_diameter" : outer_diameter,
                                                        "thickness" : thickness, 
                                                        "offset_y" : offset_y, 
                                                        "offset_z" : offset_z, 
                                                        "insulation_thickness" : 0, 
                                                        "insulation_density" : 0   }    
                        data["flange_section_parameters"] = flange_section_parameters
                    self.project.add_valve_by_elements(valve_elements, data)
                    if self.set_cross_section_to_list_elements(self.list_flange_elements, flange_section_parameters, valve_diameters):
                        return
                    _valve_elements = [element_id for element_id in valve_elements if element_id not in self.list_flange_elements]
                    if self.set_cross_section_to_list_elements(_valve_elements, valve_section_parameters, valve_diameters):
                        return
                else:
                    title = "None cross-section defined"
                    message = "The selected lines or elements has no cross-section defined. "
                    message += "Please, define a pipe cross-section before proceed."   
            else:
                if outer_diameter != 0:
                    self.project.add_valve_by_elements(valve_elements, data)
                    if self.set_cross_section_to_list_elements(valve_elements, valve_section_parameters, valve_diameters):
                        return
                else:
                    title = "None cross-section defined"
                    message = "The selected lines or elements has no cross-section defined. "
                    message += "Please, define a pipe cross-section before proceed."
            
            if message != "":
                PrintMessageInput([title, message, window_title_1])
                return True

    def set_cross_section_to_list_elements(self, list_elements, section_parameters, valve_diameters): 
        valve_section_info = {   "section_type_label" : "Valve section" ,
                                    "section_parameters" : section_parameters   }
        list_cross_sections = []
        for element_id in list_elements:             
            valve_section_info["diameters_to_plot"] = valve_diameters[element_id] 
            cross_section = CrossSection(valve_section_info=valve_section_info)
            list_cross_sections.append(cross_section)
        self.project.set_cross_section_by_elements(list_elements, list_cross_sections)
        return False
    
    def check_previous_attributions_to_elements(self, list_elements):
        for element_id in list_elements:
            element = self.structural_elements[element_id]
            if element.element_type == "expansion_joint":
                title = "Expansion joint detected in the elements selection"
                message = "In the present element list, at least one 'expansion joint' element was found. "
                message += "To avoid unwanted expansion joint setup modifications, we recommend removing any " 
                message += "already existing expansion joint in the vicinity of the 'new valve' elements."
                PrintMessageInput([title, message, window_title_1])
                return True
        return False

    def check_number_valve_and_flange_elements(self, number_valve_elements, number_flange_elements):
        if number_valve_elements <= number_flange_elements:
            title = "Invalid number of flange elements"
            message = "The selected number of flange elements must be less than the valve number of elements. "
            message += "We recommend reducing the flange number of elements to proceed.\n"
            message += f"\nNumber of valve elements: {number_valve_elements}"
            message += f"\nNumber of flange elements: {number_flange_elements}"
            PrintMessageInput([title, message, window_title_1])
            return True

    def search_for_cross_section_in_neighborhood(self, valve_elements, set_by_elements=False):

        outer_diameter = 0
        thickness = None
        offset_y = None
        offset_z = None
        self.inner_diameter = 0
        cross = None
        search_at_neighborhood = True

        for element_id in valve_elements:
            cross = self.structural_elements[element_id].cross_section 
            element_type = self.structural_elements[element_id].element_type
            if element_type == 'pipe_1':
                if cross:
                    if cross.outer_diameter > outer_diameter:
                        outer_diameter = cross.outer_diameter
                        thickness = cross.thickness
                        offset_y = cross.offset_y
                        offset_z = cross.offset_z
                        self.inner_diameter = cross.inner_diameter
                        search_at_neighborhood = False
                        break
            else:
                continue

        if search_at_neighborhood:

            lists_element_indexes = []
            first_element_id = min(valve_elements)
            last_element_id = max(valve_elements)
            lists_element_indexes.append([  first_element_id-1, first_element_id+1, 
                                            last_element_id-1, last_element_id+1  ])

            if set_by_elements:
                element_id = valve_elements[0]
                line_id = self.preprocessor.elements_to_line[element_id]
                first_element_id_from_line = self.preprocessor.line_to_elements[line_id][0]
                last_element_id_from_line = self.preprocessor.line_to_elements[line_id][-1]
                lists_element_indexes.append([  first_element_id_from_line-1, first_element_id_from_line+1, 
                                                last_element_id_from_line-1, last_element_id_from_line+1  ])

            for element_indexes in lists_element_indexes:
                if cross:
                    break
                for element_id in element_indexes:
                    if element_id not in valve_elements:
                        cross = self.structural_elements[element_id].cross_section
                        element_type = self.structural_elements[element_id].element_type
                        if element_type == 'pipe_1':
                            if cross:
                                if cross.outer_diameter > outer_diameter:
                                    outer_diameter = cross.outer_diameter
                                    thickness = cross.thickness
                                    offset_y = cross.offset_y
                                    offset_z = cross.offset_z   
                                    self.inner_diameter = cross.inner_diameter
                                    break
                        else:
                            continue      

        if None in [thickness, offset_y, offset_z]:
            valve_section_parameters = None
        else:
            valve_section_parameters = {"outer_diameter" : outer_diameter,
                                        "thickness" : thickness, 
                                        "offset_y" : offset_y, 
                                        "offset_z" : offset_z, 
                                        "insulation_thickness" : 0, 
                                        "insulation_density" : 0}   

        return valve_section_parameters

    def actions_to_finalize(self):
        self.complete = True
        self.opv.updateEntityRadius()
        self.opv.changePlotToMesh()
        # self.opv.changePlotToEntitiesWithCrossSection()   
        self.close()
    
    def load_valves_info(self):
        self.treeWidget_valve_remove.clear()
        for group_key, [_, parameters] in self.preprocessor.group_elements_with_valves.items():
            length = parameters['valve_length']
            sitffening_factor = parameters['stiffening_factor']
            mass = parameters['valve_mass']
            outer_diameter = parameters['valve_section_parameters']['outer_diameter']
            valve_info = f"d_v: {outer_diameter}m; length: {length}m; Kf: {sitffening_factor}; mass: {mass}kg"
            #
            new = QTreeWidgetItem([group_key, valve_info])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)  
            self.treeWidget_valve_remove.addTopLevelItem(new)  

        self.treeWidget_valve_remove.header().setStyleSheet('font: 16px; font-size: 9pt; font-family: Arial;')
        self.treeWidget_valve_remove.setStyleSheet('font: 16px; font-size: 9pt; font-family: Arial;')
        self.update_remove_tab()
    
    def on_click_item_remove(self, item):
        [valve_elements, _] = self.group_elements_with_valves[item.text(0)]
        self.opv.opvRenderer.highlight_elements(valve_elements)
        self.opv.opvRenderer.update()
        self.lineEdit_selected_ID.setText(item.text(0))

    def on_doubleclick_item_remove(self, item):
        key = item.text(0)
        self.lineEdit_selected_ID.setText(key)
        if key in self.group_elements_with_valves.keys():
            self.remove_valve_function(key)
        self.load_valves_info()
        self.lineEdit_selected_ID.setText("")
        self.opv.opvRenderer.plot()
        self.opv.changePlotToEntitiesWithCrossSection()

    def remove_valve_function(self, key):
        [valve_elements, _] = self.group_elements_with_valves[key]
        self.project.add_valve_by_elements(valve_elements, None)
        self.check_if_is_there_a_perforated_plate_and_remove_it(valve_elements)
        #
        lists_element_indexes = []
        first_element_id = min(valve_elements)
        last_element_id = max(valve_elements)
        lists_element_indexes.append([  first_element_id-1, first_element_id+1, 
                                        last_element_id-1, last_element_id+1  ])

        line_id = self.preprocessor.elements_to_line[valve_elements[0]]
        first_element_id_from_line = self.preprocessor.line_to_elements[line_id][0]
        last_element_id_from_line = self.preprocessor.line_to_elements[line_id][-1]
        lists_element_indexes.append([  first_element_id_from_line-1, first_element_id_from_line+1, 
                                        last_element_id_from_line-1, last_element_id_from_line+1  ])
        #
        for element_indexes in lists_element_indexes:
            for element_id in element_indexes:
                if element_id not in valve_elements:
                    cross = self.structural_elements[element_id].cross_section
                    element_type = self.structural_elements[element_id].element_type
                    if element_type == 'pipe_1':
                        if cross:
                            self.project.set_cross_section_by_elements(valve_elements, cross)
                            self.project.add_cross_sections_expansion_joints_valves_in_file(valve_elements)
                            return self.load_valves_info()

    def remove_valve_by_selection(self):
        key = self.lineEdit_selected_ID.text()
        if key in self.group_elements_with_valves.keys():
            self.remove_valve_function(key)
        self.lineEdit_selected_ID.setText("")
        title = "Valve removal complete"
        message = "The selectect valve has been removed from model."
        message += f"\n\n ID: {key}"
        PrintMessageInput([title, message, window_title_2])
        self.opv.opvRenderer.plot()
        self.opv.changePlotToEntitiesWithCrossSection()

    def remove_all_valves(self):
        title = f"Removal of all valves from model"
        message = "Are you really sure you want to remove all valves from the model?\n\n\n"
        message += "Press the Continue button to proceed with removal or press Cancel or Close buttons to abort the current operation."
        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)

        if read._stop:
            return
        
        temp_dict = self.group_elements_with_valves.copy()
        _keys = temp_dict.keys()
        for key in _keys:
            self.remove_valve_function(key)
        title = "Valves resetting complete"
        message = "The valves has been removed from all elements."
        PrintMessageInput([title, message, window_title_2])
        self.opv.opvRenderer.plot()
        self.opv.changePlotToEntitiesWithCrossSection()

    def check_if_is_there_a_perforated_plate_and_remove_it(self, elements_from_valve):
        temp_dict = self.group_elements_with_perforated_plate.copy()
        for key, [perforated_plate, elements_from_pp] in temp_dict.items():
            for element_id in elements_from_pp:
                if element_id in elements_from_valve:
                    table_name = perforated_plate.dimensionless_impedance_table_name
                    self.process_table_file_removal(table_name)
                    if self.checkBox_remove_valve_acoustic_effects.isChecked():
                        self.remove_valve_acoustic_effects_function(key, message_print=False)

    def process_table_file_removal(self, table_name):
        if table_name is not None:
            self.project.remove_acoustic_table_files_from_folder(table_name, "perforated_plate_files")

    def remove_valve_acoustic_effects_function(self, key, message_print=True):

        if message_print:
            group_label = key.split(" || ")[1]
            message = f"The perforated plate attributed to the {group_label}\n"
            message += "group of elements have been removed."
        else:
            message = None
        
        [_, list_elements] = self.group_elements_with_perforated_plate[key]
        key_strings = ['perforated plate data', 'dimensionless impedance', 'list of elements']
        remove_bc_from_file([key], self.elements_info_path, key_strings, message)
        
        self.preprocessor.set_perforated_plate_by_elements(list_elements, None, key, delete_from_dict=True)