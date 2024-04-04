from PyQt5.QtWidgets import QDialog, QCheckBox, QComboBox, QFrame, QLabel, QLineEdit, QPushButton, QSpinBox, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.user_input.model.setup.acoustic.perforated_plate_input import PerforatedPlateInput
from pulse.preprocessing.cross_section import CrossSection
from pulse.tools.utils import get_V_linear_distribution, remove_bc_from_file
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.call_double_confirmation import CallDoubleConfirmationInput

import numpy as np
from collections import defaultdict

window_title_1 = "Error"
window_title_2 = "Warning"

class ValvesInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/structural/set_valve_input.ui"
        uic.loadUi(ui_path, self)

        self.project = app().project
        self.opv = app().main_window.opv_widget
        self.opv.setInputObject(self)

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.load_valves_info()
        self.update()
        #self.show()
        self.exec()


        
        print("oi exec1")
        #self.exec()
        #print("oi exec2")

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
        self.nodes = self.preprocessor.nodes
        self.preprocessor._map_lines_to_nodes()

        self.structural_elements = self.preprocessor.structural_elements

        self.element_size = self.project.file._element_size
        self.elements_info_path = self.project.file._element_info_path
        
        self.stop = False
        self.complete = False
        self.allow_to_update = True
        self.flange_outer_diameter = None

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_selection : QComboBox
        # QCheckBox
        self.checkBox_add_flanges_to_the_valve : QCheckBox
        self.checkBox_enable_acoustic_effects : QCheckBox
        self.checkBox_remove_valve_acoustic_effects : QCheckBox
        # QFrame
        self.main_frame : QFrame
        self.selection_frame : QFrame
        # QLabel
        self.label_selected_id : QLabel
        self.label_outer_diameter : QLabel
        self.label_outer_diameter_unit : QLabel
        self.label_number_of_elements : QLabel
        self.label_flange_length : QLabel
        self.label_flange_length_unit : QLabel
        # QLineEdit
        self.lineEdit_selected_id : QLineEdit
        self.lineEdit_stiffening_factor : QLineEdit
        self.lineEdit_valve_mass : QLineEdit
        self.lineEdit_valve_length : QLineEdit
        self.lineEdit_flange_length : QLineEdit
        self.lineEdit_outer_diameter : QLineEdit   
        # QSpinBox
        self.spinBox_number_elements_flange : QSpinBox
        # QPushButton
        self.pushButton_confirm : QPushButton
        self.pushButton_reset : QPushButton
        self.pushButton_remove : QPushButton
        # QTabWidget
        self.tabWidget_main : QTabWidget
        # QTreeWidget
        self.treeWidget_valve_remove : QTreeWidget

    def _create_connections(self):
        self.checkBox_add_flanges_to_the_valve.stateChanged.connect(self.checkBox_event_update)
        self.comboBox_selection.currentIndexChanged.connect(self.selection_type_callback)
        self.pushButton_confirm.clicked.connect(self.add_valve_to_selection)
        self.pushButton_remove.clicked.connect(self.remove_valve_by_selection)
        self.pushButton_reset.clicked.connect(self.reset_valves)
        self.spinBox_number_elements_flange.valueChanged.connect(self.update_flange_length)
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        self.treeWidget_valve_remove.itemClicked.connect(self.on_click_item)
        self.treeWidget_valve_remove.itemDoubleClicked.connect(self.on_doubleclick_item)
        self.update_flange_length()

    def _config_widgets(self):
        self.cache_tab = self.tabWidget_main.currentIndex()
        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")

    def tab_event_callback(self):
        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_main.currentIndex() == 2:
            self.selection_frame.setDisabled(True)
        else:
            if self.cache_tab == 2:
                self.lineEdit_selected_id.setText("")
            self.selection_frame.setDisabled(False)
        self.cache_tab = self.tabWidget_main.currentIndex()
        self.update_flange_length()

    def checkBox_event_update(self):
        if self.checkBox_add_flanges_to_the_valve.isChecked():
            self.label_outer_diameter.setDisabled(False)
            self.label_outer_diameter_unit.setDisabled(False)
            self.label_number_of_elements.setDisabled(False)
            self.label_flange_length.setDisabled(False)
            self.label_flange_length_unit.setDisabled(False)
            self.lineEdit_outer_diameter.setDisabled(False)
            self.lineEdit_outer_diameter.setDisabled(False)
            self.spinBox_number_elements_flange.setDisabled(False)

        else:
            self.label_outer_diameter.setDisabled(True)
            self.label_outer_diameter_unit.setDisabled(True)
            self.label_number_of_elements.setDisabled(True)
            self.label_flange_length.setDisabled(True)
            self.label_flange_length_unit.setDisabled(True)
            self.lineEdit_outer_diameter.setDisabled(True)
            self.lineEdit_flange_length.setText("")
            self.spinBox_number_elements_flange.setDisabled(True)

    def selection_type_callback(self):

        line_id = self.opv.getListPickedLines()
        element_id = self.opv.getListPickedElements()

        self.lineEdit_selected_id.setText("")

        if self.comboBox_selection.currentIndex() == 0:

            self.label_selected_id.setText("Line ID:")
            self.lineEdit_valve_length.setDisabled(True)
            
            if not self.opv.change_plot_to_entities_with_cross_section:
                self.opv.plot_entities_with_cross_section()
                if len(line_id):
                    self.opv.opvRenderer.highlight_lines(line_id)

        else:

            self.label_selected_id.setText("Element ID:")
            self.lineEdit_valve_length.setDisabled(False)

            if not self.opv.change_plot_to_mesh:
                self.opv.plot_mesh()
                if element_id:
                    self.opv.opvRenderer.highlight_elements(element_id)

        if self.allow_to_update:
            self.update()

    def update(self):

        line_id = self.opv.getListPickedLines()
        element_id = self.opv.getListPickedElements()

        if line_id:
            element_id = list()
            self.allow_to_update = False
            self.comboBox_selection.setCurrentIndex(0)

        elif element_id:
            line_id = list()
            self.allow_to_update = False
            self.comboBox_selection.setCurrentIndex(1)

        else:
            return

        self.allow_to_update = True

        try:

            if line_id:

                if self.write_ids(line_id):
                    self.lineEdit_selected_id.setText("")
                    return

                if len(line_id) == 1:
                    self.get_line_length()
                else:
                    self.lineEdit_valve_length.setText("multiple")

            elif element_id:

                if self.write_ids(element_id):
                    self.lineEdit_selected_id.setText("")
                    return

            self.update_valve_info()

        except Exception as log_error:
            title = "Error in 'update_selection_info' function"
            message = str(log_error) 
            PrintMessageInput([window_title_1, title, message])

    def update_valve_length_line_selection(self):
        valve_length = self.spinBox_number_elements_flange.value()*self.element_size
        self.lineEdit_flange_length.setText(str(round(valve_length, 6)))

    def update_flange_length(self):
        self.flange_length = self.spinBox_number_elements_flange.value()*self.element_size
        self.lineEdit_flange_length.setText(str(round(self.flange_length, 6)))

    def load_valves_info(self):
        self.pushButton_remove.setDisabled(True)
        self.treeWidget_valve_remove.clear()
        for group_key, [_, parameters] in self.preprocessor.group_elements_with_valves.items():

            length = parameters['valve_length']
            sitffening_factor = parameters['stiffening_factor']
            mass = parameters['valve_mass']
            outer_diameter = parameters['valve_section_parameters'][0]
            valve_info = str([outer_diameter, length, sitffening_factor, mass])

            new = QTreeWidgetItem([group_key, valve_info])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)  
            self.treeWidget_valve_remove.addTopLevelItem(new)

        self.update_tab_visibility()

    def update_tab_visibility(self):    
        if len(self.preprocessor.group_elements_with_valves) == 0:
            self.tabWidget_main.setTabVisible(1, False)
            self.tabWidget_main.setCurrentIndex(0)
        else:
            self.tabWidget_main.setTabVisible(1, True)

    def write_ids(self, list_selected_ids):
        text = ""
        for _id in list_selected_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_id.setText(text[:-2])  
        if self.check_selection_type():
            return True
        return False

    def get_line_length(self):
        lineEdit_lineID = self.lineEdit_selected_id.text()
        if lineEdit_lineID != "":

            self.stop, _line_id = self.before_run.check_input_LineID(lineEdit_lineID, single_ID=True)
            if self.stop:
                self.lineEdit_selected_id.setText("")
                self.lineEdit_valve_length.setText("")
                self.lineEdit_selected_id.setFocus()
                return True

            valve_length, _ = self.preprocessor.get_line_length(_line_id) 
            self.lineEdit_valve_length.setText(str(round(valve_length, 6)))

    def update_valve_info(self):

        line_id = self.opv.getListPickedLines()
        element_id = self.opv.getListPickedElements()

        valve_parameters = None
        if len(line_id) == 1:

            entity = self.preprocessor.dict_tag_to_entity[line_id[0]]
            list_of_elements = self.preprocessor.line_to_elements[line_id[0]]

            if entity.valve_parameters is not None:
                valve_parameters = entity.valve_parameters

        elif len(element_id) == 1:

            element = self.structural_elements[element_id[0]]
            list_of_elements = element_id

            if element.valve_parameters:
                valve_parameters = element.valve_parameters

        if valve_parameters is not None:

            valve_length = valve_parameters["valve_length"]
            self.lineEdit_valve_length.setText(str(valve_length))

            valve_mass = valve_parameters["valve_mass"]
            self.lineEdit_valve_mass.setText(str(valve_mass))

            stiffening_factor = valve_parameters["stiffening_factor"]
            self.lineEdit_stiffening_factor.setText(str(stiffening_factor))

            if "flange_section_parameters" in valve_parameters.keys():
                flange_outer_diameter = valve_parameters["flange_section_parameters"][0]
                self.lineEdit_outer_diameter.setText(str(flange_outer_diameter))
                self.checkBox_add_flanges_to_the_valve.setChecked(True)

                if "number_flange_elements" in valve_parameters.keys():
                    N = int(valve_parameters["number_flange_elements"] / 2)
                    self.spinBox_number_elements_flange.setValue(N)
                    flange_length = N*self.element_size
                    self.lineEdit_flange_length.setText(str(round(flange_length, 6)))

            else:
                self.checkBox_add_flanges_to_the_valve.setChecked(False)

            aux = self.preprocessor.group_elements_with_perforated_plate
            for [_, elements_from_pp] in aux.values():
                for element_id in elements_from_pp:
                    if element_id in list_of_elements:
                        self.checkBox_enable_acoustic_effects.setChecked(True)
                        return

            self.checkBox_enable_acoustic_effects.setChecked(False)

    def check_flanges_by_lines(self):
        elements_from_line = defaultdict(list)
        for element_id in self.opv.getListPickedElements():
            line = self.preprocessor.elements_to_line[element_id]
            elements_from_line[line].append(element_id)
        return elements_from_line

    def check_selection_type(self):

        _stop = False
        lineEdit_selection = self.lineEdit_selected_id.text()

        if self.comboBox_selection.currentIndex() == 0:
            _stop, self.selected_lines = self.before_run.check_input_LineID(lineEdit_selection)
            for line_id in self.selected_lines:
                entity = self.preprocessor.dict_tag_to_entity[line_id]
                if entity.structural_element_type in ["beam_1", "expansion_joint"]:
                    _stop = True
                    break
                   
        else:
            _stop, self.selected_elements = self.before_run.check_input_ElementID(lineEdit_selection)
            for element_id in self.selected_elements:
                element = self.structural_elements[element_id]
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
            message = f"An empty entry has been detected at the '{label}' input field.\n\n" 
            message += "You should enter a positive value to proceed."
            self.value = None
        if message != "":
            PrintMessageInput([window_title_1, title, message])
            return True
        else:
            return False

    def check_flange_parameters(self):
        if self.check_input_parameters(self.lineEdit_flange_length, 'Flange length'):
            self.tabWidget_main.setCurrentIndex(1)
            self.lineEdit_flange_length.setFocus()
            return True
        else:
            self.flange_length = self.value 

        if self.check_input_parameters(self.lineEdit_outer_diameter, 'Outer flange diameter'):
            self.tabWidget_main.setCurrentIndex(1)
            self.lineEdit_outer_diameter.setFocus()
            return True
        else:
            self.flange_outer_diameter = self.value        
        
        # if self.check_input_parameters(self.lineEdit_inner_diameter, 'Inner diameter'):
        #     self.tabWidget_main.setCurrentIndex(1)
        #     self.lineEdit_inner_diameter.setFocus()
        #     return True
        # else:
        #     self.flange_inner_diameter = self.value                
        
        return False

    def check_valve_parameters(self):

        if self.check_input_parameters(self.lineEdit_valve_mass, 'Valve mass'):
            self.lineEdit_valve_mass.setFocus()
            return True
        else:
            self.valve_mass = self.value

        if self.check_input_parameters(self.lineEdit_stiffening_factor, 'Stiffening factor'):
            self.lineEdit_stiffening_factor.setFocus()
            return True
        else:
            self.stiffening_factor = self.value

    def get_start_end_elements_from_line(self, line_id):
        number_flange_elements = self.spinBox_number_elements_flange.value()
        elements_from_line = np.sort(self.preprocessor.line_to_elements[line_id])
        if number_flange_elements < len(elements_from_line): 
            lists_elements = [  elements_from_line[:number_flange_elements], 
                                elements_from_line[-number_flange_elements:]  ]
            flange_elements = [_id for list_elements in lists_elements for _id in list_elements]
            return flange_elements
        else:
            title = "Invalid number of flange elements"
            message = "The selected number of flange elements must be less than the line number of elements. "
            message += "We recommend reducing the flange number of elements to proceed.\n"
            message += f"\nLine: {line_id}"
            message += f"\nNumber of elements: {number_flange_elements}"
            PrintMessageInput([window_title_1, title, message])
            return []

    def get_valve_diameters(self, valve_elements, valve_diameter, flange_elements = list(), flange_thickness = 0):

        number_valve_elements = len(valve_elements)
        number_flange_elements = len(flange_elements)
        N = number_valve_elements - number_flange_elements

        if number_flange_elements == 0:
            outer_diameters =  get_V_linear_distribution(valve_diameter, N)
            inner_diameters = outer_diameters - 2*self.valve_thickness

        else:
            nf = int(number_flange_elements/2)
            outer_diameters = np.ones(number_valve_elements)*self.flange_outer_diameter
            inner_diameters = outer_diameters - 2*flange_thickness
            outer_diameters[nf:-nf] = get_V_linear_distribution(valve_diameter, N)
            inner_diameters[nf:-nf] = outer_diameters[nf:-nf] - 2*self.valve_thickness 
  
        diameters_data = dict()
        for i, element_id in enumerate(valve_elements):
            diameters_data[element_id] = [outer_diameters[i], inner_diameters[i]]

        return diameters_data

    def get_selected_ids(self):
        if self.comboBox_selection.currentIndex() == 0:
            selected_ids = self.selected_lines
        else:
            selected_ids = self.selected_elements
        return selected_ids

    def add_valve_to_selection(self):

        if self.check_selection_type():
            return

        if self.check_valve_parameters():
            self.tabWidget_main.setCurrentIndex(0)
            return

        if self.checkBox_add_flanges_to_the_valve.isChecked():
            if self.check_flange_parameters():
                return   

        if self.checkBox_enable_acoustic_effects.isChecked():
            if self.comboBox_selection.currentIndex() == 1:
                valve_ids = self.selected_elements
            else:
                valve_ids = []
                for line_id in self.selected_lines:    
                    list_elements = self.preprocessor.line_to_elements[line_id]
                    N = len(list_elements)
                    if np.remainder(N, 2) == 0:
                        index = int(N/2)
                        half_ids = list_elements[index]
                    else:
                        index = int((N-1)/2)
                        half_ids = list_elements[index]
                    valve_ids.append(half_ids)

            self.hide()
            #self.show()
            #print("oi 2")
            #self.setVisible(False)


            perforated_plate = PerforatedPlateInput(valve_ids = valve_ids)
            if not perforated_plate.complete:
                self.opv.setInputObject(self)
                self.exec()
                print("oi 2")
                return

        valve_parameters = dict()
        self.inner_diameter = 0

        for tag_id in self.get_selected_ids():

            if self.comboBox_selection.currentIndex() == 0:

                if self.checkBox_add_flanges_to_the_valve.isChecked():
                    flange_elements = self.get_start_end_elements_from_line(tag_id)
                    if flange_elements == []:
                        return
                else:
                    flange_elements = list()

                valve_length, edge_nodes = self.preprocessor.get_line_length(tag_id)
                valve_length = round(valve_length, 6)
                self.lineEdit_valve_length.setText(str(valve_length))
                self.valve_center_coordinates = list(np.round((edge_nodes[0].coordinates + edge_nodes[1].coordinates)/2, 6))
            
                valve_elements = list(self.preprocessor.line_to_elements[tag_id])
                valve_section_parameters = self.search_for_cross_section_in_neighborhood(valve_elements)
            
            else:

                if self.check_input_parameters(self.lineEdit_valve_length, 'Valve length'):
                    self.lineEdit_valve_length.setFocus()
                    return True
                else:
                    valve_length = self.value

                element =self.structural_elements[tag_id]
                self.valve_center_coordinates = list(np.round(element.element_center_coordinates, 6))
                _, valve_elements = self.preprocessor.get_neighbor_nodes_and_elements_by_element(tag_id, valve_length)
                number_valve_elements = len(valve_elements)

                if self.check_previous_attributions_to_elements(valve_elements):
                    return

                number_flange_elements = self.spinBox_number_elements_flange.value()
                if self.check_number_valve_and_flange_elements(number_valve_elements, number_flange_elements):
                    return

                lists_elements = [  valve_elements[:number_flange_elements], 
                                    valve_elements[-number_flange_elements:]  ]
                flange_elements = [_id for list_elements in lists_elements for _id in list_elements]
                valve_section_parameters = self.search_for_cross_section_in_neighborhood(valve_elements, set_by_elements=True)

            if valve_section_parameters:

                valve_outer_diameter = valve_section_parameters[0]
                self.valve_thickness = valve_section_parameters[1]

                if self.checkBox_add_flanges_to_the_valve.isChecked():

                    flange_thickness = round((self.flange_outer_diameter - self.inner_diameter)/2, 6)
                    flange_section_parameters = [self.flange_outer_diameter, flange_thickness, 0, 0, 0, 0]
                    valve_diameters = self.get_valve_diameters( valve_elements,
                                                                valve_outer_diameter, 
                                                                flange_elements = flange_elements,
                                                                flange_thickness = flange_thickness)

                    valve_parameters[tag_id] = {   "valve_elements" : valve_elements,
                                                    "number_flange_elements" : len(flange_elements),
                                                    "flange_elements" : flange_elements,
                                                    "valve_section_parameters" : valve_section_parameters,  
                                                    "valve_length" : valve_length,
                                                    "stiffening_factor" : self.stiffening_factor,
                                                    "valve_mass" : self.valve_mass,
                                                    "valve_center_coordinates" : self.valve_center_coordinates,
                                                    "flange_section_parameters" : flange_section_parameters,
                                                    "valve_diameters" : valve_diameters   }

                else:

                    valve_diameters = self.get_valve_diameters( valve_elements,
                                                                valve_outer_diameter )

                    valve_parameters[tag_id] = {   "valve_elements" : valve_elements,
                                                    "valve_section_parameters" : valve_section_parameters,  
                                                    "valve_length" : valve_length,
                                                    "stiffening_factor" : self.stiffening_factor,
                                                    "valve_mass" : self.valve_mass,
                                                    "valve_center_coordinates" : self.valve_center_coordinates,
                                                    "valve_diameters" : valve_diameters   }

        if valve_parameters:
            if self.comboBox_selection.currentIndex() == 0:
                if self.set_valve_by_lines(valve_parameters):
                    return            
            else:
                if self.set_valve_by_elements(valve_parameters):
                    return
        else:
            return

        # if none_pipe_section:
        #     title = "No pipe cross-section has been detected in the valve neighborhood"
        #     message = "There are no pipe cross-sections defined in the valve neighbor elements. " 
        #     message += "You must define cross-sections to the neighbor valve elements to proceed."    
        #     PrintMessageInput([window_title_2, title, message])

        self.complete = True
        self.opv.update_section_radius()
        self.opv.plot_mesh()
        # self.opv.plot_entities_with_cross_section()

        if self.isVisible():
            self.close()

    def set_valve_by_lines(self, valve_data):
        message = ""
        for line_id, data in valve_data.items():

            valve_elements = data["valve_elements"]
            valve_diameters = data["valve_diameters"]

            valve_section_parameters = data["valve_section_parameters"]
            outer_diameter = valve_section_parameters[0]

            if self.checkBox_add_flanges_to_the_valve.isChecked():

                if "flange_elements" in data.keys():
                    flange_elements = data["flange_elements"]

                flange_outer_diameter = data["flange_section_parameters"][0]
                offset_y = valve_section_parameters[2]
                offset_z = valve_section_parameters[3]

                if outer_diameter != 0:
                    if flange_outer_diameter <= self.inner_diameter:
                        title = "Invalid input to the outer/inner diameters"
                        message = "The outer diameter input should be greater than the inner diameter. \n"
                        message += "This condition must  be satified to proceed."
                        PrintMessageInput([window_title_1, title, message])
                        return True

                    else:
                        outer_diameter = self.flange_outer_diameter
                        thickness = round((self.flange_outer_diameter - self.inner_diameter)/2, 6)
                        flange_section_parameters = [outer_diameter, thickness, offset_y, offset_z, 0, 0]
                        data["flange_section_parameters"] = flange_section_parameters

                    self.project.add_valve_by_line(line_id, data)
                    if self.set_cross_section_to_list_elements(flange_elements, flange_section_parameters, valve_diameters):
                        return

                    _valve_elements = [element_id for element_id in valve_elements if element_id not in flange_elements]
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
                PrintMessageInput([window_title_1, title, message])
                return True

    def set_valve_by_elements(self, valve_data):
        message = ""
        for data in valve_data.values():

            valve_elements = data["valve_elements"]  
            valve_diameters = data["valve_diameters"]
            valve_section_parameters = data["valve_section_parameters"]
            outer_diameter = valve_section_parameters[0]

            if self.checkBox_add_flanges_to_the_valve.isChecked():

                if "flange_elements" in data.keys():
                    flange_elements = data["flange_elements"]

                flange_outer_diameter = data["flange_section_parameters"][0]
                offset_y = valve_section_parameters[2]
                offset_z = valve_section_parameters[3]

                if outer_diameter != 0:
                    if flange_outer_diameter <= self.inner_diameter:
                        title = "Invalid input to the outer/inner diameters"
                        message = "The outer diameter input should be greater than the inner diameter. \n"
                        message += "This condition must  be satified to proceed."
                        PrintMessageInput([window_title_1, title, message])
                        return True

                    else:
                        outer_diameter = self.flange_outer_diameter
                        thickness = round((self.flange_outer_diameter - self.inner_diameter)/2, 6)
                        flange_section_parameters = [outer_diameter, thickness, offset_y, offset_z, 0, 0] 
                        data["flange_section_parameters"] = flange_section_parameters

                    self.project.add_valve_by_elements(valve_elements, data)
                    if self.set_cross_section_to_list_elements(flange_elements, flange_section_parameters, valve_diameters):
                        return

                    _valve_elements = [element_id for element_id in valve_elements if element_id not in flange_elements]
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
                PrintMessageInput([window_title_1, title, message])
                return True

    def set_cross_section_to_list_elements(self, list_elements, section_parameters, valve_diameters): 

        list_cross_sections = list()
        valve_section_info = {  "section_type_label" : "Valve section" ,
                                "section_parameters" : section_parameters  }

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
                PrintMessageInput([window_title_1, title, message])
                return True
        return False

    def check_number_valve_and_flange_elements(self, number_valve_elements, number_flange_elements):
        if number_valve_elements <= number_flange_elements:
            title = "Invalid number of flange elements"
            message = "The selected number of flange elements must be less than the valve number of elements. "
            message += "We recommend reducing the flange number of elements to proceed.\n"
            message += f"\nNumber of valve elements: {number_valve_elements}"
            message += f"\nNumber of flange elements: {number_flange_elements}"
            PrintMessageInput([window_title_1, title, message])
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
            valve_section_parameters = [outer_diameter, thickness, offset_y, offset_z, 0, 0]  

        return valve_section_parameters

    def on_click_item(self, item):
        self.lineEdit_selected_id.setText(item.text(0))
        self.pushButton_remove.setDisabled(False)
        if item.text(0) in self.preprocessor.group_elements_with_valves.keys():
            valve_elements, *args = self.preprocessor.group_elements_with_valves[item.text(0)]
            self.opv.opvRenderer.highlight_elements(valve_elements)

    def on_doubleclick_item(self, item):
        self.on_click_item(item)
        self.load_valves_info()

    def reset_valve_attributes_from_lines(self, elements):
        lines = list()
        for element_id in elements:
            line_id = self.preprocessor.elements_to_line[element_id]
            if line_id not in lines:
                lines.append(line_id)

        for line in lines:
            entity = self.preprocessor.dict_tag_to_entity[line]
            entity.valve_parameters = None

    def remove_valve_function(self, key):
        if key in self.preprocessor.group_elements_with_valves.keys():

            [valve_elements, _] = self.preprocessor.group_elements_with_valves[key]
            self.project.add_valve_by_elements(valve_elements, None)

            self.reset_valve_attributes_from_lines(valve_elements)
            self.remove_existing_perforated_plate(valve_elements)
            self.restore_the_cross_section(valve_elements)

    def restore_the_cross_section(self, input_elements):

        lists_element_indexes = []
        first_element_id = min(input_elements)
        last_element_id = max(input_elements)
        lists_element_indexes.append([  first_element_id - 1, 
                                        first_element_id + 1,
                                        last_element_id - 1,  
                                        last_element_id + 1  ])

        line_id = self.preprocessor.elements_to_line[input_elements[0]]
        first_element_id_from_line = self.preprocessor.line_to_elements[line_id][0]
        last_element_id_from_line = self.preprocessor.line_to_elements[line_id][-1]
        lists_element_indexes.append([  first_element_id_from_line - 1, 
                                        first_element_id_from_line + 1, 
                                        last_element_id_from_line - 1,  
                                        last_element_id_from_line + 1  ])

        for element_indexes in lists_element_indexes:
            for element_id in element_indexes:
                if element_id not in input_elements:
                    cross = self.structural_elements[element_id].cross_section
                    element_type = self.structural_elements[element_id].element_type
                    if element_type == 'pipe_1':
                        if cross:
                            self.project.set_cross_section_by_elements(input_elements, cross)
                            self.project.add_cross_sections_expansion_joints_valves_in_file(input_elements)
                            return self.load_valves_info()

    def remove_valve_by_selection(self):
        if self.lineEdit_selected_id.text() != "":

            key = self.lineEdit_selected_id.text()
            if key in self.preprocessor.group_elements_with_valves.keys():
                self.remove_valve_function(key)

            self.lineEdit_selected_id.setText("")
            self.opv.plot_entities_with_cross_section()

    def reset_valves(self):

        self.setVisible(False)
        title = f"Removal of all valves from model"
        message = "Would you like to remove all valves from the model?"
        
        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)

        if read._stop:
            self.setInputObject(self)
            self.setVisible(True)
            return

        aux = self.preprocessor.group_elements_with_valves.copy()
        for key in aux.keys():
            self.remove_valve_function(key)

        self.opv.plot_entities_with_cross_section()

    def remove_existing_perforated_plate(self, elements_from_valve):
        temp_dict = self.preprocessor.group_elements_with_perforated_plate.copy()
        for key, [perforated_plate, elements_from_pp] in temp_dict.items():
            for element_id in elements_from_pp:
                if element_id in elements_from_valve:
                    table_name = perforated_plate.dimensionless_impedance_table_name
                    self.process_table_file_removal(table_name)
                    if self.checkBox_remove_valve_acoustic_effects.isChecked():
                        self.remove_valve_acoustic_effects_function(key)

    def process_table_file_removal(self, table_name):
        if table_name is not None:
            self.project.remove_acoustic_table_files_from_folder(table_name, "perforated_plate_files")

    def remove_valve_acoustic_effects_function(self, key, message_print=False):

        if message_print:
            group_label = key.split(" || ")[1]
            message = f"The perforated plate attributed to the {group_label}\n"
            message += "group of elements have been removed."
        else:
            message = None

        [_, list_elements] = self.preprocessor.group_elements_with_perforated_plate[key]
        key_strings = ['perforated plate data', 'dimensionless impedance', 'list of elements']
        remove_bc_from_file([key], self.elements_info_path, key_strings, message)

        self.preprocessor.set_perforated_plate_by_elements(list_elements, None, key, delete_from_dict=True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.add_valve_to_selection()
        if event.key() == Qt.Key_Escape:
            self.close()