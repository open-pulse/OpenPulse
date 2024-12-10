from PyQt5.QtWidgets import QComboBox, QDialog, QLabel, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.model.setup.fluid.set_fluid_input_simplified import SetFluidInputSimplified

from pulse.editor.pulsation_damper import PulsationDamper
from pulse.model.properties.fluid import Fluid
from pulse.model.properties.material import Material

from pulse.utils.interface_utils import check_inputs

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

class PulsationDamperEditorInputs(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/editor/pulsation_damper_editor_inputs.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties
        self.preprocessor = app().project.model.preprocessor

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        self.load_pulsation_damper_info()
        self.selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.keep_window_open = True

        self.gas_fluid = None
        self.liquid_fluid = None
        self.selected_fluid = None
        self.selected_material = None

        self.state_properties = dict()
        self.nodes_from_removed_lines = list()

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_damper_type: QComboBox
        self.comboBox_main_axis: QComboBox
        self.comboBox_fluid_data_source: QComboBox
        self.comboBox_volume_unit: QComboBox
        self.comboBox_pressure_units: QComboBox
        self.comboBox_temperature_units: QComboBox
        self.comboBox_volume_sections: QComboBox

        # QLabel
        self.label_damper_volume_unit: QLabel
        self.label_gas_volume_unit: QLabel
        
        # QLineEdit
        self.lineEdit_damper_label: QLineEdit
        self.lineEdit_connecting_coord_x: QLineEdit
        self.lineEdit_connecting_coord_y: QLineEdit
        self.lineEdit_connecting_coord_z: QLineEdit
        self.lineEdit_damper_volume: QLineEdit
        self.lineEdit_gas_volume: QLineEdit
        self.lineEdit_outside_diameter_liquid: QLineEdit
        self.lineEdit_wall_thickness_liquid: QLineEdit
        self.lineEdit_outside_diameter_gas: QLineEdit
        self.lineEdit_wall_thickness_gas: QLineEdit
        self.lineEdit_outside_diameter_neck: QLineEdit
        self.lineEdit_neck_height: QLineEdit
        self.lineEdit_polytropic_exponent: QLineEdit
        self.lineEdit_gas_pressure: QLineEdit
        self.lineEdit_gas_temperature: QLineEdit
        self.lineEdit_selected_liquid_fluid: QLineEdit
        self.lineEdit_selected_gas_fluid: QLineEdit
        self.lineEdit_selected_damper_label: QLabel
        self.lineEdit_damper_type: QLabel

        # QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_create: QPushButton
        self.pushButton_get_liquid_fluid: QPushButton
        self.pushButton_get_gas_fluid: QPushButton
        self.pushButton_remove: QPushButton
        self.pushButton_reset: QPushButton
        self.pushButton_reset_entries: QPushButton

        # QTabWidget
        self.tabWidget_main: QTabWidget

        # QTreeWidget
        self.treeWidget_pulsation_damper_info: QTreeWidget

    def _create_connections(self):
        #
        self.comboBox_volume_sections.currentIndexChanged.connect(self.volume_sections_callback)
        self.comboBox_volume_unit.currentIndexChanged.connect(self.update_volume_unit_callback)
        self.comboBox_pressure_units.currentIndexChanged.connect(self.load_state_properties)
        self.comboBox_temperature_units.currentIndexChanged.connect(self.load_state_properties)
        #
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_create.clicked.connect(self.create_pulsation_damper_callback)
        self.pushButton_get_gas_fluid.clicked.connect(self.get_gas_fluid_callback)
        self.pushButton_get_liquid_fluid.clicked.connect(self.get_liquid_fluid_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_pulsation_damper_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_pulsation_damper_info.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)
        #
        self.volume_sections_callback()

    def selection_callback(self):

        selected_nodes = app().main_window.list_selected_nodes()

        if len(selected_nodes) == 1:

            node = self.preprocessor.nodes[selected_nodes[0]]
            self.lineEdit_connecting_coord_x.setText(str(round(node.x, 6)))
            self.lineEdit_connecting_coord_y.setText(str(round(node.y, 6)))
            self.lineEdit_connecting_coord_z.setText(str(round(node.z, 6)))

            elements = self.preprocessor.structural_elements_connected_to_node[node.external_index]

            self.selected_material = None
            material = elements[0].material

            if material is None:
                return

            self.selected_material = material

    def load_fluid_properties(self, fluid: Fluid):

        pressure = fluid.pressure
        temperature = fluid.temperature
        isentropic_exponent = fluid.isentropic_exponent

        self.lineEdit_gas_pressure.setText(f"{pressure : .8e}")
        self.lineEdit_gas_temperature.setText(f"{temperature : .6f}")
        self.lineEdit_polytropic_exponent.setText(f"{isentropic_exponent : .6f}")

    def _config_widgets(self):
        #
        self.lineEdit_damper_label.setFocus()
        self.lineEdit_selected_damper_label.setDisabled(True)
        self.lineEdit_damper_type.setDisabled(True)
        self.pushButton_remove.setDisabled(True)
        #
        self.config_treeWidget()        

    def config_treeWidget(self):
        widths = [120, 140, 160, 40]
        header_labels = ["Label", "Damper type", "Connection point", "Lines"]
        for col, label in enumerate(header_labels):
            self.treeWidget_pulsation_damper_info.headerItem().setText(col, label)
            self.treeWidget_pulsation_damper_info.headerItem().setTextAlignment(col, Qt.AlignCenter)
            self.treeWidget_pulsation_damper_info.setColumnWidth(col, widths[col])

    def get_liquid_fluid_callback(self):
        self.fluid_state = "liquid"
        self.get_fluid_callback()

    def get_gas_fluid_callback(self):
        self.fluid_state = "gas"
        self.get_fluid_callback()

    def get_fluid_callback(self):
        self.hide()
        self.fluid_dialog = SetFluidInputSimplified(state_properties = self.state_properties)
        self.fluid_dialog.fluid_widget.pushButton_attribute.setText("Select fluid")
        self.fluid_dialog.pushButton_attribute.clicked.connect(self.get_selected_fluid)
        self.fluid_dialog.exec_and_keep_window_open()
        app().main_window.set_input_widget(self)

    def get_selected_fluid(self):

        selected_fluid = self.fluid_dialog.get_selected_fluid()

        if isinstance(selected_fluid, Fluid):

            self.fluid_dialog.close()
            if selected_fluid.name in self.fluid_dialog.fluid_widget.fluid_name_to_refprop_data.keys():
                self.comboBox_fluid_data_source.setCurrentIndex(0)

            if self.fluid_state == "liquid":
                self.lineEdit_selected_liquid_fluid.setText(selected_fluid.name)
                self.liquid_fluid = selected_fluid
                self.state_properties["pressure"] = selected_fluid.pressure
                self.state_properties["temperature"] = selected_fluid.temperature

            else:
                self.lineEdit_selected_gas_fluid.setText(selected_fluid.name)
                self.lineEdit_polytropic_exponent.setText(f"{selected_fluid.isentropic_exponent : .6f}")
                self.gas_fluid = selected_fluid

            self.load_state_properties()

    def tab_event_callback(self):
        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_main.currentIndex() == 0:
            self.pushButton_cancel.setDisabled(False)
            self.pushButton_create.setDisabled(False)
        else:
            self.pushButton_cancel.setDisabled(True)
            self.pushButton_create.setDisabled(True)

    def on_click_item(self, item):

        self.pushButton_remove.setDisabled(False)
        self.lineEdit_selected_damper_label.setText(item.text(0))

        if item.text(0) in self.pulsation_damper_lines.keys():
            damper_lines = self.pulsation_damper_lines[item.text(0)]
            app().main_window.set_selection(lines = damper_lines)

    def on_double_click_item(self, item):
        self.on_click_item(item)

    def load_state_properties(self):

        if self.state_properties:

            pressure_Pa = self.state_properties["pressure"]
            temperature_K = self.state_properties["temperature"]

            tu_index = self.comboBox_temperature_units.currentIndex()
            if tu_index == 0:
                temperature_C = temperature_K - 273.15
                self.lineEdit_gas_temperature.setText(f"{temperature_C}")

            else:
                self.lineEdit_gas_temperature.setText(f"{temperature_K}")

            pu_index = self.comboBox_pressure_units.currentIndex()
            if pu_index >= 4:
                pressure_Pa_g = pressure_Pa - 101325

            if pu_index == 0:
                pressure_value = pressure_Pa / 9.80665e4

            elif pu_index == 1:
                pressure_value = pressure_Pa / 1e5

            elif pu_index == 2:
                pressure_value = pressure_Pa / 1e3                

            elif pu_index == 3:
                pressure_value = pressure_Pa / 1

            elif pu_index == 4:
                pressure_value = pressure_Pa_g / 9.80665e4

            elif pu_index == 5:
                pressure_value = pressure_Pa_g / 1e5

            elif pu_index == 6:
                pressure_value = pressure_Pa_g / 1e3                

            elif pu_index == 7:
                pressure_value = pressure_Pa_g / 1

            self.lineEdit_gas_pressure.setText(f"{pressure_value : .8e}")

    def update_volume_unit_callback(self):

        index = self.comboBox_volume_unit.currentIndex()

        if index == 0:
            unit_label = "m³"
        elif index == 1:
            unit_label = "cm³"
        else:
            unit_label = "L"

        self.label_damper_volume_unit.setText(f"[{unit_label}]")
        self.label_gas_volume_unit.setText(f"[{unit_label}]")

    def volume_sections_callback(self):

        index = self.comboBox_volume_sections.currentIndex()
        self.lineEdit_outside_diameter_gas.setEnabled(bool(index))
        self.lineEdit_wall_thickness_gas.setEnabled(bool(index))

        if index == 0:
            outside_diameter = self.lineEdit_outside_diameter_liquid.text()
            wall_thickness = self.lineEdit_wall_thickness_liquid.text()
            self.lineEdit_outside_diameter_gas.setText(outside_diameter)
            self.lineEdit_wall_thickness_gas.setText(wall_thickness)

    def check_connecting_coords(self):

        coord_x = check_inputs(self.lineEdit_connecting_coord_x, "'connecting coord. x'", only_positive=False)
        if coord_x is None:
            self.lineEdit_connecting_coord_x.setFocus()
            return True

        coord_y = check_inputs(self.lineEdit_connecting_coord_y, "'connecting coord. y'", only_positive=False)
        if coord_y is None:
            self.lineEdit_connecting_coord_y.setFocus()
            return True
        
        coord_z = check_inputs(self.lineEdit_connecting_coord_z, "'connecting coord. z'", only_positive=False)
        if coord_z is None:
            self.lineEdit_connecting_coord_z.setFocus()
            return True
        
        self._pulsation_damper_data["connecting_coords"] = [round(coord_x, 6), round(coord_y, 6), round(coord_z, 6)]

    def check_volumes(self):

        damper_volume = check_inputs(self.lineEdit_damper_volume, "'damper volume'", only_positive=False)
        if damper_volume is None:
            self.lineEdit_damper_volume.setFocus()
            return True

        gas_volume = check_inputs(self.lineEdit_gas_volume, "'gas volume'", only_positive=False)
        if gas_volume is None:
            self.lineEdit_gas_volume.setFocus()
            return True
        
        self._pulsation_damper_data["damper_volume"] = damper_volume
        self._pulsation_damper_data["gas_volume"] = gas_volume

    def check_geometric_entries(self):

        outside_diameter_liquid = check_inputs(self.lineEdit_outside_diameter_liquid, "'outside diameter (liquid)'", only_positive=False)
        if outside_diameter_liquid is None:
            self.lineEdit_outside_diameter_liquid.setFocus()
            return True

        wall_thickness_liquid = check_inputs(self.lineEdit_wall_thickness_liquid, "'wall thickness (liquid)'", only_positive=False)
        if wall_thickness_liquid is None:
            self.lineEdit_wall_thickness_liquid.setFocus()
            return True

        outside_diameter_gas = check_inputs(self.lineEdit_outside_diameter_gas, "'outside diameter (gas)'", only_positive=False)
        if outside_diameter_gas is None:
            self.lineEdit_outside_diameter_gas.setFocus()
            return True

        wall_thickness_gas = check_inputs(self.lineEdit_wall_thickness_gas, "'wall thickness (gas)'", only_positive=False)
        if wall_thickness_gas is None:
            self.lineEdit_wall_thickness_gas.setFocus()
            return True

        outside_diameter_neck = check_inputs(self.lineEdit_outside_diameter_neck, "'outside diameter (neck)'", only_positive=False)
        if outside_diameter_neck is None:
            self.lineEdit_outside_diameter_neck.setFocus()
            return True

        neck_height = check_inputs(self.lineEdit_neck_height, "'neck heght'", only_positive=False)
        if neck_height is None:
            self.lineEdit_neck_height.setFocus()
            return True

        self._pulsation_damper_data["outside_diameter_liquid"] = outside_diameter_liquid
        self._pulsation_damper_data["wall_thickness_liquid"] = wall_thickness_liquid
        self._pulsation_damper_data["outside_diameter_gas"] = outside_diameter_gas
        self._pulsation_damper_data["wall_thickness_gas"] = wall_thickness_gas
        self._pulsation_damper_data["outside_diameter_neck"] = outside_diameter_neck
        self._pulsation_damper_data["neck_height"] = neck_height

    def check_fluids(self):

        if self.liquid_fluid is None:
            self.get_liquid_fluid_callback()
            return True

        if self.gas_fluid is None:
            self.get_gas_fluid_callback()
            return True

        self._pulsation_damper_data["liquid_fluid_id"] = self.liquid_fluid.identifier
        self._pulsation_damper_data["gas_fluid_id"] = self.gas_fluid.identifier

    def check_pulsation_damper_inputs(self):

        self._pulsation_damper_data = dict()

        self._pulsation_damper_data["main_axis"] = self.comboBox_main_axis.currentText()[1:]
        self._pulsation_damper_data["damper_type"] = self.comboBox_damper_type.currentText()

        if self.check_connecting_coords():
            return True

        if self.check_volumes():
            return True

        if self.check_geometric_entries():
            return True
        
        if self.check_fluids():
            return True

    def get_values(self, values: np.ndarray):
        return list(np.array(np.round(values, 6), dtype=float))

    def create_pulsation_damper_callback(self):

        stop, damper_label = self.check_pulsation_damper_label()
        if stop:
            return

        if self.check_pulsation_damper_inputs():
            self._pulsation_damper_data.clear()
            return

        aux = self.damper_data.copy()
        for key, data in aux.items():
            if data == self._pulsation_damper_data:
                self.damper_data.pop(key)
                break
        
        self.damper_data[damper_label] = self._pulsation_damper_data

        device = PulsationDamper(self._pulsation_damper_data)

        self.close()
        self.build_device(damper_label, device)
        self.actions_to_finalize()

        # remember, you should to generate the mesh
        self.set_element_length_corrections(damper_label, device)

    def build_device(self, damper_label: str, device: (PulsationDamper)):

        lines_properties = self.properties.line_properties
        line_tags = list(lines_properties.keys())

        if line_tags:
            shifted_line = max(line_tags) + 1
        else:
            shifted_line = 1

        device.process_segment_data()

        for i in range(len(device.segment_data)):

            start_coords, end_coords, section_data, segment_label, fluid_id = device.segment_data[i]

            if isinstance(section_data, list):

                aux = { 
                        "structure_name" : "pipe",
                        "start_coords" : self.get_values(start_coords),
                        "end_coords" : self.get_values(end_coords),
                        "section_type_label" : "Pipe",
                        "section_parameters" : section_data,
                        "structural_element_type" : "pipe_1",
                        "pulsation_damper_name" : damper_label,
                        "pulsation_damper_segment" : segment_label,
                        "fluid_id" : fluid_id
                       }
                
                if isinstance(self.selected_material, Material):
                    aux["material_id"] = self.selected_material.identifier

                tag = int(shifted_line + i)
                self.properties._set_multiple_line_properties(aux, tag)

        app().pulse_file.write_line_properties_in_file()
        self.write_pulsation_damper_element_properties_in_file(damper_label, device)

    def write_pulsation_damper_element_properties_in_file(self, damper_label: str, device: (PulsationDamper)):

        if self.damper_data is None:
            return

        index = 0
        if damper_label in self.damper_data.keys():
            for (_coords, _elc_type) in device.elc_data:
                index += 1
                coords = self.get_values(_coords)
                key = f"element_length_correction - {index}"
                self.damper_data[damper_label][key] = {   
                                                       "connection_coords" : coords,
                                                       "elc_type" : _elc_type 
                                                       }

        app().pulse_file.write_pulsation_damper_data_in_file(self.damper_data)

    def remove_pulsation_damper_related_line_properties(self, damper_labels: str | list):

        if isinstance(damper_labels, str):
            damper_labels = [damper_labels]

        lines_data = app().pulse_file.read_line_properties_from_file()
        if lines_data is None:
            return

        self.nodes_from_removed_lines.clear()

        remove_gaps = False
        for line_id, data in lines_data.items():
            if "pulsation_damper_name" in data.keys():

                if data["pulsation_damper_name"] in damper_labels:
                    self.properties._remove_line(line_id)
                    line_nodes = self.preprocessor.mesh.nodes_from_line[int(line_id)]
                    self.nodes_from_removed_lines.extend(list(line_nodes))
                    remove_gaps = True

        app().pulse_file.write_line_properties_in_file()

        if remove_gaps:
            app().pulse_file.remove_line_gaps_from_line_properties_file()

    def set_element_length_corrections(self, damper_label: str, device: (PulsationDamper)):

        for (coords, elc_type) in device.elc_data:

            node_id = self.preprocessor.get_node_id_by_coordinates(coords)
            neigh_elements = self.preprocessor.acoustic_elements_connected_to_node[node_id]
            element_ids = [int(element.index) for element in neigh_elements]

            if elc_type == "side-branch":
                _type = 1

            else:
                _type = 0

            data = {
                    "correction_type" : _type,
                    "coords" : list(np.round(coords, 5)),
                    "pulsation_damper_name" : damper_label
                    }

            self.preprocessor.set_element_length_correction_by_element(element_ids, data)
            self.properties._set_element_property("element_length_correction", data, element_ids)
            app().pulse_file.write_element_properties_in_file()

    def remove_pulsation_damper_related_element_properties(self, damper_label: str):

        element_ids = list()
        for (_property, element_id), data in self.properties.element_properties.items():
            if _property == "element_length_correction":
                data: dict
                if "pulsation_damper_name" in data.keys():
                    if damper_label == "_remove_all_":
                        element_ids.append(element_id)
                    elif damper_label == data["pulsation_damper_name"]:
                        element_ids.append(element_id)

        self.preprocessor.set_element_length_correction_by_element(element_ids, None)
        self.properties._remove_element_property("element_length_correction", element_ids) 
        app().pulse_file.write_element_properties_in_file()

    def remove_callback(self):

        if self.lineEdit_selected_damper_label.text() != "":

            damper_label = self.lineEdit_selected_damper_label.text()

            if damper_label in self.damper_data.keys():
                self.damper_data.pop(damper_label)

            self.remove_pulsation_damper_related_line_properties(damper_label)
            self.remove_pulsation_damper_related_element_properties(damper_label)
            self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Pulsation Dampers resetting"
        message = "Would you like to remove all the created Pulsation Dampers from the model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Proceed"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            damper_labels = list(self.damper_data.keys())
            self.damper_data.clear()

            self.remove_pulsation_damper_related_line_properties(damper_labels)
            self.remove_pulsation_damper_related_element_properties("_remove_all_")
            self.actions_to_finalize()

    def load_pulsation_damper_info(self):

        self.treeWidget_pulsation_damper_info.clear()
        self.pulsation_damper_lines = app().loader.get_pulsation_damper_related_lines()

        self.damper_data = app().pulse_file.read_pulsation_damper_data_from_file()
        if self.damper_data is None:
            self.damper_data = dict()

        for key, damper_data in self.damper_data.items():

            coords = damper_data["connecting_coords"]
            damper_type = damper_data["damper_type"]

            new = QTreeWidgetItem([key, damper_type, str(coords), str(self.pulsation_damper_lines[key])])
            for col in range(4):
                new.setTextAlignment(col, Qt.AlignCenter)
            self.treeWidget_pulsation_damper_info.addTopLevelItem(new)

        if self.damper_data:
            self.tabWidget_main.setTabVisible(1, True)
        else:
            self.tabWidget_main.setCurrentIndex(0)
            self.tabWidget_main.setTabVisible(1, False)

    def check_pulsation_damper_label(self):

        message = ""
        damper_label = self.lineEdit_damper_label.text()

        if damper_label == "":
            self.lineEdit_damper_label.setFocus()
            title = "Empty field detected"
            message = "Enter a damper label to proceed."

        elif damper_label in self.damper_data.keys():
            self.lineEdit_damper_label.setFocus()

            title = "Invalid input"
            message = f"The typed damper label '{damper_label}' has already been applied to other Pulsation Damper. "
            message += "You should enter a different label to proceed with the Pulsation Damper configuration."

        if message != "":
            self.hide()
            PrintMessageInput([window_title_2, title, message])
            app().main_window.set_input_widget(self)
            return True, None

        return False, damper_label

    def attribute_callback(self):
        pass

    def check_input_parameters(self, lineEdit: QLineEdit, label: str, _float=True):

        title = "Input error"
        message = ""

        value_string = lineEdit.text()

        if value_string != "":

            value_string = value_string.replace(",", ".")

            try:

                if _float:
                    value = float(value_string)
                else:
                    value = int(value_string)

                if value < 0:
                    message = f"You cannot input a negative value to the {label}."

            except Exception:
                return None
                message = f"You have typed an invalid value to the {label}."

        else:
            message = f"None value has been typed to the {label}."
            return None

        if message != "":
            self.hide()
            PrintMessageInput([window_title_1, title, message])
            return None

        return value

    def get_device_tag(self):
        index = 1
        _run = True
        while _run:
            if index in self.damper_data.keys():
                index += 1
            else:
                _run = False
        return index

    def actions_to_finalize(self):

        app().main_window.set_selection()
        app().pulse_file.write_pulsation_damper_data_in_file(self.damper_data)

        app().loader.load_project_data()
        app().project.initial_load_project_actions()

        if app().pulse_file.check_pipeline_data():
            app().loader.load_mesh_dependent_properties()
            app().main_window.initial_project_action(True)
        else:
            self.preprocessor.mesh._create_gmsh_geometry()

        self.load_pulsation_damper_info()
        # app().main_window.use_model_setup_workspace()

        app().main_window.update_plots()
        self.pushButton_cancel.setText("Exit")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.create_pulsation_damper_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)
    
    # def calculate_effective_volume(self):

    #     dV = self.check_input_parameters(self.lineEdit_fluctuating_volume, "Fluctuating volume of reciprocating pump")
    #     if dV is None:
    #         self.lineEdit_effective_volume.setText("")
    #         self.lineEdit_volume_at_average_pressure.setText("")
    #         return
        
    #     phi = self.doubleSpinBox_pressure_ratio.value()
    #     x = self.doubleSpinBox_residual_pulsation.value() / 100
    #     k = self.doubleSpinBox_isentropic_exponent.value()

    #     V0 = dV / ((phi/(1-x))**(1/k) - (phi/(1+x))**(1/k))
    #     Vm = V0 * (phi**(1/k))

    #     unit_label = self.comboBox_volume_unit.currentText()

    #     if unit_label == " cubic centimeters":
    #         V0 = V0 * 1e6
    #         Vm = Vm * 1e6

    #     elif unit_label == " liters":
    #         V0 = V0 * 1e3
    #         Vm = Vm * 1e6

    #     self.lineEdit_effective_volume.setText(f"{V0 : .8e}")
    #     self.lineEdit_volume_at_average_pressure.setText(f"{Vm : .8e}")