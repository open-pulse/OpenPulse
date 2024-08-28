# fmt: off

from PyQt5.QtWidgets import QComboBox, QCheckBox, QDialog, QFrame, QLabel, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5 import uic

from pulse import app, UI_DIR
# from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.model.setup.acoustic.perforated_plate_input import PerforatedPlateInput
from pulse.model.cross_section import CrossSection
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

from pprint import pprint
import numpy as np
from collections import defaultdict

window_title_1 = "Error"
window_title_2 = "Warning"

class ValvesInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/structural/valve_input.ui"
        uic.loadUi(ui_path, self)

        self.render_type = kwargs.get("render_type", "model")

        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties
        self.preprocessor = app().project.model.preprocessor

        self.project = app().project

        self.before_run = app().project.get_pre_solution_model_checks()

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        if self.render_type == "model":

            self._config_widgets()
            self.load_valves_info()
            self.selection_callback()

        self._configure_appearance()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):
        self.complete = False
        self.keep_window_open = True

    def _define_qt_variables(self):

        # QCheckBox
        self.checkBox_remove_valve_acoustic_effects: QCheckBox

        # QComboBox
        self.comboBox_acoustic_effects: QComboBox
        self.comboBox_flange_setup: QComboBox

        # QFrame
        self.main_frame: QFrame
        self.selection_frame: QFrame

        # QLabel
        self.label_selected_id: QLabel
        self.label_flange_diameter: QLabel
        self.label_flange_diameter_unit: QLabel
        self.label_flange_length: QLabel
        self.label_flange_length_unit: QLabel
        self.label_orifice_plate_thickness: QLabel
        self.label_orifice_plate_thickness_unit: QLabel

        # QLineEdit
        self.lineEdit_selected_id: QLineEdit
        self.lineEdit_valve_name: QLineEdit
        self.lineEdit_stiffening_factor: QLineEdit
        self.lineEdit_valve_mass: QLineEdit
        self.lineEdit_effective_diameter: QLineEdit
        self.lineEdit_wall_thickness: QLineEdit
        self.lineEdit_orifice_plate_thickness: QLineEdit
        self.lineEdit_flange_length: QLineEdit
        self.lineEdit_flange_diameter: QLineEdit

        # QPushButton
        self.pushButton_attribute: QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_reset: QPushButton
        self.pushButton_remove: QPushButton

        # QTabWidget
        self.tabWidget_main: QTabWidget

        # QTreeWidget
        self.treeWidget_valves_info: QTreeWidget

    def _create_connections(self):
        #
        self.comboBox_acoustic_effects.currentIndexChanged.connect(self.valve_setup_callback)
        self.comboBox_flange_setup.currentIndexChanged.connect(self.valve_setup_callback)
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_valves_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_valves_info.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)
        #
        self.valve_setup_callback()

    def selection_callback(self):

        line_ids = app().main_window.list_selected_lines()

        if line_ids:

            text = ", ".join([str(i) for i in line_ids])
            self.lineEdit_selected_id.setText(text)

            if self.check_selection_type(line_ids):
                return

            if len(line_ids) == 1:

                line_id = line_ids[0]
                valve_info = self.properties._get_property("valve_info", line_id=line_id)
                if valve_info is None:
                    return

                valve_name = valve_info["valve_name"]
                valve_mass = valve_info["valve_mass"]
                stiffening_factor = valve_info["stiffening_factor"]

                self.lineEdit_valve_name.setText(valve_name)
                self.lineEdit_valve_mass.setText(str(valve_mass))
                self.lineEdit_stiffening_factor.setText(str(stiffening_factor))

                if "flange_diameter" in valve_info.keys():
                    flange_diameter = valve_info["flange_diameter"]
                    flange_length = valve_info["flange_length"]
                    self.lineEdit_flange_diameter.setText(str(flange_diameter))
                    self.lineEdit_flange_length.setText(str(flange_length))
                    self.comboBox_flange_setup.setCurrentIndex(1)
                else:
                    self.comboBox_flange_setup.setCurrentIndex(0)

                if "acoustic_effects" in valve_info.keys():
                    acoustic_effects = valve_info["acoustic_effects"]
                    if acoustic_effects:
                        self.comboBox_acoustic_effects.setCurrentIndex(1)
                    else:
                        self.comboBox_acoustic_effects.setCurrentIndex(0)

    def _configure_appearance(self):
        if self.render_type == "model":
            self.selection_frame.setVisible(True)
        else:
            self.selection_frame.setVisible(False)
            self.tabWidget_main.setTabVisible(1, False)

        self.adjustSize()

    def _config_widgets(self):
        # self.cache_tab = self.tabWidget_main.currentIndex()
        for i, w in enumerate([100, 120, 160]):
            self.treeWidget_valves_info.setColumnWidth(i, w)
            self.treeWidget_valves_info.headerItem().setTextAlignment(i, Qt.AlignCenter)

        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")

    def _create_lists_of_lineEdits(self):
        self.list_lineEdits =  [
                                self.lineEdit_selected_id,
                                self.lineEdit_stiffening_factor,
                                self.lineEdit_valve_mass,
                                self.lineEdit_orifice_plate_thickness,
                                self.lineEdit_flange_length,
                                self.lineEdit_flange_diameter,
                                self.lineEdit_valve_name
                                ]

    def reset_all_lineEdits(self):
        for lineEdit in self.list_lineEdits:
            lineEdit.setText("")

    def tab_event_callback(self):
        self.lineEdit_selected_id.setText("")
        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_main.currentIndex() == 2:
            self.selection_frame.setDisabled(True)
        else:
            # if self.cache_tab == 2:
            #     self.lineEdit_selected_id.setText("")
            self.selection_frame.setDisabled(False)
        # self.cache_tab = self.tabWidget_main.currentIndex()

    def valve_setup_callback(self):

        index_A = self.comboBox_acoustic_effects.currentIndex()
        index_B = self.comboBox_flange_setup.currentIndex()

        self.acoustic_effects_callback(bool(index_A))
        self.flanged_valves_callback(bool(index_B))

    def acoustic_effects_callback(self, enabled: bool):

        self.label_orifice_plate_thickness.setEnabled(enabled)
        self.label_orifice_plate_thickness_unit.setEnabled(enabled)
        self.lineEdit_orifice_plate_thickness.setEnabled(enabled)

        if not enabled:
            self.lineEdit_orifice_plate_thickness.setText("")

    def flanged_valves_callback(self, enabled: bool):
        self.label_flange_diameter.setEnabled(enabled)
        self.label_flange_diameter_unit.setEnabled(enabled)
        self.label_flange_length.setEnabled(enabled)
        self.label_flange_length_unit.setEnabled(enabled)
        self.lineEdit_flange_diameter.setEnabled(enabled)
        self.lineEdit_flange_length.setEnabled(enabled)

        if not enabled:
            self.lineEdit_flange_diameter.setText("")
            self.lineEdit_flange_length.setText("")

    def load_valves_info(self):

        self.pushButton_remove.setDisabled(True)
        self.treeWidget_valves_info.clear()

        for line_id, data in self.properties.line_properties.items():
            if "valve_info" in data.keys():

                valve_name = data["valve_name"]
                valve_info = data["valve_info"]
                mass = valve_info["valve_mass"]
                stiffening_factor = valve_info["stiffening_factor"]
                acoustic_effects = valve_info["acoustic_effects"]
                outer_diameter = data["section_parameters"][0]

                parameters = str([outer_diameter, stiffening_factor, mass, acoustic_effects])

                item = QTreeWidgetItem([valve_name, str(line_id), parameters])
                for i in range(3):
                    item.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_valves_info.addTopLevelItem(item)

        self.update_tab_visibility()

    def update_tab_visibility(self):
        self.tabWidget_main.setTabVisible(1, False)
        for data in self.properties.line_properties.values():
            if "valve_name" in data.keys():
                self.tabWidget_main.setTabVisible(1, True)
                return

    def check_flanges_by_lines(self):
        elements_from_line = defaultdict(list)
        for element_id in app().main_window.list_selected_elements():
            line = self.preprocessor.mesh.elements_to_line[element_id]
            elements_from_line[line].append(element_id)
        return elements_from_line

    def check_selection_type(self, line_ids: list):

        for line_id in line_ids:
            structural_element = self.properties._get_property("structural_element_type", line_id=line_id)
            if structural_element in ["beam_1", "expansion_joint"]:
                self.lineEdit_selected_id.setText("")
                self.lineEdit_selected_id.setFocus()
                return True

        return False

    def check_input_parameters(self, lineEdit: QLineEdit, label: str, _float=True):

        message = ""
        title = f"Invalid entry to the '{label}'"
        str_value = lineEdit.text()

        if str_value != "":

            try:

                str_value = str_value.replace(",", ".")
                if _float:
                    value = float(str_value)
                else:
                    value = int(str_value) 

                if value <= 0:
                    message = f"You cannot input a non-positive value to the '{label}'."

            except Exception as _log_error:
                message = f"You have typed an invalid value to the '{label}' input field."
                message += "The input value should be a positive float number.\n\n"
                message += f"{str(_log_error)}"
        else:
            message = f"An empty entry has been detected at the '{label}' input field. " 
            message += "You should to enter a positive value to proceed."

        if message != "":
            PrintMessageInput([window_title_1, title, message])
            return True, None
        else:
            return False, value

    def check_valve_parameters(self):

        self.valve_name = ""
        if self.lineEdit_valve_name.text() == "":
            self.lineEdit_valve_name.setFocus()
            return True

        self.valve_name = self.lineEdit_valve_name.text()
        self.valve_info["valve_name"] = self.valve_name

        stop, value = self.check_input_parameters(self.lineEdit_valve_mass, 'Valve mass')
        if stop:
            self.lineEdit_valve_mass.setFocus()
            return True

        self.valve_info["valve_mass"] = value

        stop, value = self.check_input_parameters(self.lineEdit_stiffening_factor, 'Stiffening factor')
        if stop:
            self.lineEdit_stiffening_factor.setFocus()
            return True

        self.valve_info["stiffening_factor"] = value

        stop, value = self.check_input_parameters(self.lineEdit_effective_diameter, 'Effective diameter')
        if stop:
            self.lineEdit_stiffening_factor.setFocus()
            return True

        self.valve_info["valve_effective_diameter"] = value

        stop, value = self.check_input_parameters(self.lineEdit_wall_thickness, 'Valve wall thickness')
        if stop:
            self.lineEdit_wall_thickness.setFocus()
            return True

        self.valve_info["valve_wall_thickness"] = value

    def check_flange_parameters(self):

        stop, value = self.check_input_parameters(self.lineEdit_flange_diameter, 'Flange diameter')
        if stop:
            self.lineEdit_flange_diameter.setFocus()
            return True

        self.valve_info["flange_diameter"] = value

        stop, value = self.check_input_parameters(self.lineEdit_flange_length, 'Flange length')
        if stop:
            self.lineEdit_flange_length.setFocus()
            return True

        self.valve_info["flange_length"] = value

        return False

    def check_orifice_plate_parameters(self):

        stop, value = self.check_input_parameters(self.lineEdit_orifice_plate_thickness, 'Orifice plate thickness')
        if stop:
            self.lineEdit_orifice_plate_thickness.setFocus()
            return True

        self.valve_info["orifice_plate_thickness"] = value

    def attribute_callback(self):

        self.valve_info = dict()

        if self.render_type == "model":

            lineEdit_selection = self.lineEdit_selected_id.text()
            stop, line_ids = self.before_run.check_selected_ids(lineEdit_selection, "lines")
            if stop:
                return

            if self.check_selection_type(line_ids):
                return

        if self.check_valve_parameters():
            return

        acoustic_effects = bool(self.comboBox_acoustic_effects.currentIndex())
        if acoustic_effects:
            if self.check_orifice_plate_parameters():
                return

        self.valve_info["acoustic_effects"] = acoustic_effects

        if self.comboBox_flange_setup.currentIndex() == 1:
            if self.check_flange_parameters():
                return

        #TODO: pass self.valve_info to pipeline editor

        if self.render_type == "model":

            if self.valve_info:

                for line_id in line_ids:
                    
                    self.add_section_parameters_into_valve_info(line_id)
                    self.properties._set_line_property("structural_element_type", "valve", line_ids=line_id)
                    self.properties._set_line_property("valve_name", self.valve_name, line_ids=line_id)
                    self.properties._set_line_property("valve_info", self.valve_info, line_ids=line_id)

                    line_data = self.properties.line_properties[line_id]
                    self.preprocessor.set_cross_sections_to_valve_elements(line_id, line_data)

                    self.remove_table_files_from_expansion_joints(line_id)
                    self.properties._remove_line_property("expansion_joint", line_id)

                self.actions_to_finalize()

                if self.valve_info["acoustic_effects"]:
                    self.configure_orifice_plate(line_ids)

        # pprint(self.valve_info)

        self.complete = True
        self.close()

    def actions_to_finalize(self):

        app().pulse_file.write_line_properties_in_file()

        # geometry_handler = GeometryHandler()
        # geometry_handler.set_length_unit(app().project.model.mesh.length_unit)
        # geometry_handler.process_pipeline()

        app().loader.load_project_data()
        self.project.initial_load_project_actions()
        app().loader.load_mesh_dependent_properties()
        app().main_window.initial_project_action(True)
        app().main_window.update_plots()
        self.complete = True

    def configure_orifice_plate(self, line_ids: list):
        
        self.hide()

        title = f"Orifice plate configuration"
        message = "Would you like to configure the orifice plate right now?"

        buttons_config = {"left_button_label" : "No", "right_button_label" : "Yes"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            element_ids = list()
            for line_id in line_ids:
                line_elements = app().project.model.mesh.line_to_elements[line_id]
                N = len(line_elements)
                if np.remainder(N, 2) == 0:
                    index = int(N/2) + 1
                else:
                    index = int((N+1)/2)

                element_ids.append(line_elements[index-1])

            perforated_plate = PerforatedPlateInput(valve_element_ids = element_ids)

            if not perforated_plate.complete:
                app().main_window.set_input_widget(self)
                return

    def add_section_parameters_into_valve_info(self, line_id: int):

        self.properties._set_line_property("section_type_label", "Valve", line_id)

        d_in = self.valve_info["valve_effective_diameter"]
        t = round(self.valve_info["valve_wall_thickness"], 6)
        d_out = round(d_in + 2 * t, 6)

        section_parameters = [d_out, t, 0, 0, 0, 0]
        self.valve_info["body_section_parameters"] = section_parameters

        if "flange_diameter" in self.valve_info.keys():
            df_out = self.valve_info["flange_diameter"]
            tf = round((df_out - d_in) / 2, 6)
            flange_section_parameters = [df_out, tf, 0, 0, 0, 0]
            self.valve_info["flange_section_parameters"] = flange_section_parameters

    def search_for_cross_section_in_neighborhood(self, line_id: int):

        outer_diameter = 0
        thickness = None
        offset_y = None
        offset_z = None
        self.inner_diameter = 0

        line_to_elements = app().project.model.mesh.line_to_elements
        line_elements = line_to_elements[line_id]

        element_ids = [ line_elements[0] - 1,
                        line_elements[0] + 1,
                        line_elements[-1] - 1, 
                        line_elements[-1] + 1 ]

        for element_id in element_ids:
            if element_id not in line_elements:
                if element_id in self.preprocessor.structural_elements.keys():
                    cross = self.preprocessor.structural_elements[element_id].cross_section 
                    element_type = self.preprocessor.structural_elements[element_id].element_type
                    if element_type == 'pipe_1':
                        if cross is None:
                            continue

                        if cross.outer_diameter > outer_diameter:
                            outer_diameter = cross.outer_diameter
                            thickness = cross.thickness
                            offset_y = cross.offset_y
                            offset_z = cross.offset_z
                            self.inner_diameter = cross.inner_diameter

        if None in [thickness, offset_y, offset_z]:
            valve_section_parameters = None
        else:
            valve_section_parameters = [outer_diameter, thickness, offset_y, offset_z, 0, 0]  

        return valve_section_parameters

    def on_click_item(self, item):
        self.lineEdit_selected_id.setText(item.text(0))
        self.pushButton_remove.setEnabled(True)
        if item.text(0) != "":
            line_ids = [int(item.text(1))]
            app().main_window.set_selection(lines = line_ids)

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

    def restore_the_cross_section(self, line_ids: list):

        line_to_elements = app().project.model.mesh.line_to_elements
        for line_id in line_ids:

            line_elements = line_to_elements[line_id]

            element_ids = [
                            line_elements[0] - 1, 
                            line_elements[0] + 1, 
                            line_elements[-1] - 1,  
                            line_elements[-1] + 1
                           ]
            cross = None
            element_type = None

            for element_id in element_ids:
                if element_id not in line_elements:

                    element = self.preprocessor.structural_elements[element_id]
                    cross = element.cross_section
                    element_type = element.element_type
                    break

            if element_type == 'pipe_1' and isinstance(cross, CrossSection):

                pipe_info = {   "section_type_label" : "Pipe",
                                "section_parameters" : cross.section_parameters   }

                self.properties._set_line_property("structural_element_type", element_type, line_id)
                self.properties._set_multiple_line_properties(pipe_info, line_id)

    def remove_table_files_from_expansion_joints(self, line_ids: list):
        table_names = list()
        for line_id, data in self.properties.line_properties.items():
            data: dict
            if "expansion_joint" in data.keys():
                ej_data = data["expansion_joint"]
                if line_id in line_ids and "table_names" in ej_data.keys():
                    table_names.append(ej_data["table_names"])

        if table_names:
            self.process_table_file_removal(table_names)

    def process_table_file_removal(self, table_names: list):
        if table_names:
            for table_name in table_names:
                self.properties.remove_imported_tables("structural", table_name)
            app().pulse_file.write_imported_table_data_in_file()

    def remove_callback(self):
        if self.lineEdit_selected_id.text() != "":

            line_id = int(self.lineEdit_selected_id.text())
            self.properties._remove_line_property("valve_name", line_id)
            self.properties._remove_line_property("flange_section_parameters", line_id)
            self.properties._remove_line_property("valve_info", line_id)

            self.restore_the_cross_section([line_id])

            self.load_valves_info()
            self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = f"Removal of all valves from model"
        message = "Would you like to remove all valves from the model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            line_ids = list()
            for line_id, data in self.properties.line_properties.items():
                data: dict
                if "valve_name" in data.keys():
                    line_ids.append(line_id)

            for line_id in line_ids:
                self.properties._remove_line_property("valve_name", line_id)
                self.properties._remove_line_property("flange_section_parameters", line_id)
                self.properties._remove_line_property("valve_info", line_id)
                self.restore_the_cross_section(line_ids)

            if line_ids:
                self.load_valves_info()
                self.actions_to_finalize()
                # self.close()

    def remove_valve_acoustic_effects_function(self, valve_names: list):
        
        element_ids = list()
        for valve_name in valve_names:
            for (property, element_id), data in self.properties.element_properties.items():
                if property == "perforated_plate":
                    if "valve_name" in data.keys():
                        if valve_name == data["valve_name"]:
                            element_ids.append(element_id)                        
                            break
        
        if element_ids:
            self.properties._remove_element_property("perforated_plate", element_ids)
            #TODO: remove existing imported tables

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)

    def get_valve_diameters(self, valve_elements: list, valve_diameter: float, flange_elements = list(), flange_thickness = 0) -> dict:

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

def get_V_linear_distribution(x, N,  reduction_start=0.0, reduction_half=0.5):

    if N == 3:
        reduction_start = 25

    output = np.zeros(N)
    x_i = x * (1 - reduction_start)
    x_m = x * (1 - reduction_half)

    if N == 1:
        return x_m

    if np.remainder(N,2) == 0:
        half = int(N/2)
        shift = 0
    else:
        half = int((N+1)/2)
        shift = 1

    output[0:half] = get_linear_distribution(x_i, x_m, half) 
    output[half-shift:] = get_linear_distribution(x_m, x_i, half)

    return output

def get_linear_distribution(x_initial, x_final, N):
    n = np.arange(N) / (N - 1)
    return (x_final - x_initial) * n + x_initial

# fmt: on