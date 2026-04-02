import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QComboBox,
    QHeaderView,
    QLineEdit,
    QTreeWidgetItem,
)

from pulse import app
from pulse.editor.pulsation_damper import PulsationDamper
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.numeric_checks.unit_utilities import (
    convert_temperature_unit, 
    convert_pressure_unit, 
    PressureUnits, 
    TemperatureUnits,
    pressure_units_labels,
    temperature_units_labels,
)
from pulse.interface.user_input.numeric_checks.validator import StrictDoubleValidator
from pulse.interface.user_input.model.setup.fluid.set_fluid_input_simplified import SetFluidInputSimplified
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.viewer_3d.render_widgets.damper_preview_render_widget import DamperPreviewRenderWidget
from pulse.interface.ui_generated.model.editor.pulsation_damper_editor_inputs_ui import PulsationDamperEditorInputs_UI

from pulse.model.node import Node
from pulse.model.properties.fluid import Fluid
from pulse.model.properties.material import Material
from pulse.editor.structures.point import Point

import re
from enum import IntEnum
from numbers import Number
from pint import UnitRegistry


class VolumeSections(IntEnum):
    EQUAL = 0
    DISTINCT = 1


error_title = "Error"
warning_title = "Warning"


class PulsationDamperEditorInputs(PulsationDamperEditorInputs_UI):

    def __init__(self, *args, device_to_delete=None, **kwargs):
        super().__init__()
        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties
        self.preprocessor = app().project.model.preprocessor
        self.default_style_sheet = self.styleSheet()

        self._config_window()
        self._initialize()
        self._configure_widgets()
        self._create_connections()
        self._config_widgets()

        self.load_pulsation_damper_info()
        self.process_line_edits()
        self.preview_callback()
        self.automatic_preview()
        self._store_deafult_parameters()

        if device_to_delete is not None:
            self.tabWidget_main.setCurrentIndex(1)
            devices = self.treeWidget_pulsation_damper_info.findItems(device_to_delete, Qt.MatchExactly)
            if devices:
                self.treeWidget_pulsation_damper_info.setCurrentItem(devices[0])
                self.on_click_item(devices[0])

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):
        self.keep_window_open = True
        self.edited_damper = False

        self.gas_fluid = None
        self.liquid_fluid = None
        self.selected_fluid = None
        self.selected_material = None
        self.error_title = None
        self.fluid_dialog = None
        self.error_message = None

        self.state_properties = dict()
        self.nodes_from_removed_lines = list()

    def _configure_widgets(self):
        
        # disable the connecting coordinates QLineEdits to prevent the user from typing
        self.lineEdit_connecting_coord_x.setDisabled(True)
        self.lineEdit_connecting_coord_y.setDisabled(True)
        self.lineEdit_connecting_coord_z.setDisabled(True)

        self.preview_widget: DamperPreviewRenderWidget

        self._load_units_labels()
        self.configure_dynamic_validators()
        self.configure_static_validators()

    def _load_units_labels(self):
        # clear data from unit combo boxes
        self.comboBox_pressure_units.clear()
        self.comboBox_temperature_units.clear()

        # add temperature and pressure labels into unit combo boxes
        self.comboBox_pressure_units.addItems(pressure_units_labels)
        self.comboBox_temperature_units.addItems(temperature_units_labels)

        # set default units
        self.comboBox_pressure_units.setCurrentText("bar (a)")
        self.comboBox_temperature_units.setCurrentText("°C")

    def configure_static_validators(self):

        # configure validator for coordinates inputs
        coords_validator = StrictDoubleValidator(-1e8, 1e8, 8)
        self.lineEdit_connecting_coord_x.setValidator(coords_validator)
        self.lineEdit_connecting_coord_y.setValidator(coords_validator)
        self.lineEdit_connecting_coord_z.setValidator(coords_validator)

        # configure validator for geometry-related inputs
        geom_validator = StrictDoubleValidator(1e-6, 1e8, 8)
        self.lineEdit_gas_volume.setValidator(geom_validator)
        self.lineEdit_damper_volume.setValidator(geom_validator)
        self.lineEdit_outside_diameter_liquid.setValidator(geom_validator)
        self.lineEdit_wall_thickness_liquid.setValidator(geom_validator)
        self.lineEdit_outside_diameter_gas.setValidator(geom_validator)
        self.lineEdit_wall_thickness_gas.setValidator(geom_validator)
        self.lineEdit_outside_diameter_neck.setValidator(geom_validator)
        self.lineEdit_neck_height.setValidator(geom_validator)

        # configure validator for polytric exponent
        self.lineEdit_polytropic_exponent.setValidator(StrictDoubleValidator(1e-8, 1e8, 6))

    def configure_dynamic_validators(self):

        # adjust temperature bounds (t_min -> zero absolute)
        t_min = 0
        t_max = 1e4
        if self.comboBox_temperature_units.currentIndex() == TemperatureUnits.CELSIUS:
            t_min = -273.15
        elif self.comboBox_temperature_units.currentIndex() == TemperatureUnits.FARENHEIT:
            t_min = -459.67

        # adjust pressure bounds (p_min -> perfect vacuum)      
        p_min = 0 
        p_max = 1e8

        punit_index = self.comboBox_pressure_units.currentIndex()
        if punit_index == PressureUnits.Pa_g:
            p_min = -101325

        elif punit_index == PressureUnits.kPa_g:
            p_min = -101.325

        elif punit_index == PressureUnits.bar_g:
            p_min = -1.101325
            p_max = 2e3

        elif punit_index == PressureUnits.kgf_cm2_g:
            p_min = -(9.80665*1e4)

        elif punit_index == PressureUnits.psi_g:
            p_min = -(0.45359237*9.80665) / (0.0254**2)

        elif punit_index == PressureUnits.ksi_g:
            p_min = -(0.45359237*9.80665) / (1e3 * (0.0254**2))
            p_max = 1e3

        # configure validator for pressure and temeperature inputs
        self.lineEdit_gas_pressure.setValidator(StrictDoubleValidator(p_min, p_max, 6))
        self.lineEdit_gas_temperature.setValidator(StrictDoubleValidator(t_min, t_max, 6))

    def _store_deafult_parameters(self):
        self.deafult_parameters = dict()
        for key, value in self.__dict__.items():
            if isinstance(value, QLineEdit):
                self.deafult_parameters[key] = value.text()
            elif isinstance(value, QComboBox):
                self.deafult_parameters[key] = value.currentIndex()

    def _create_connections(self):
        #
        self.comboBox_volume_sections.currentIndexChanged.connect(self.volume_sections_callback)
        self.comboBox_volume_unit.currentIndexChanged.connect(self.update_volume_unit_callback)
        self.comboBox_pressure_units.currentIndexChanged.connect(self.configure_dynamic_validators)
        self.comboBox_temperature_units.currentIndexChanged.connect(self.configure_dynamic_validators)
        #
        self.lineEdit_outside_diameter_liquid.textEdited.connect(self.update_sections_info_callback)
        self.lineEdit_wall_thickness_liquid.textEdited.connect(self.update_sections_info_callback)
        #
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_show_errors.clicked.connect(self.show_error_window_for_parameters)
        self.pushButton_create.clicked.connect(self.create_pulsation_damper_callback)
        self.pushButton_get_gas_fluid.clicked.connect(self.get_gas_fluid_callback)
        self.pushButton_get_liquid_fluid.clicked.connect(self.get_liquid_fluid_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_edit.clicked.connect(self.edit_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_copy.clicked.connect(self.copy_callback)
        self.pushButton_reset_entries.clicked.connect(self.reset_entries_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_pulsation_damper_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_pulsation_damper_info.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)
        #
        self.selection_callback()
        self.volume_sections_callback()

    def selection_callback(self):

        self.selected_material = None
        selected_nodes = app().main_window.list_selected_nodes()
        selected_points = app().project.pipeline.selected_points

        if len(selected_nodes) == 1:

            node_id = selected_nodes[0]
            if node_id not in self.preprocessor.mesh.geometry_points:
                return

            node = self.preprocessor.nodes.get(node_id)
            if node is None:
                return

            self.load_nodal_coordinates_of_selected_point(node)

            elements = self.preprocessor.structural_elements_connected_to_node[node.external_index]
            material = elements[0].material

            if isinstance(material, Material):
                self.selected_material = material

        elif len(selected_points) == 1:
            point = selected_points[0]
            self.load_nodal_coordinates_of_selected_point(point)

            node_id = self.preprocessor.get_node_id_by_coordinates(point.coords())
            if isinstance(node_id, Number):
                node = self.preprocessor.nodes.get(node_id)
                if node is None:
                    return

                elements = self.preprocessor.structural_elements_connected_to_node[node.external_index]
                material = elements[0].material

            if isinstance(material, Material):
                self.selected_material = material

        app().main_window.selection_changed.connect(self.selection_callback)
        app().main_window.geometry_widget.left_released.connect(self.selection_callback)

    def load_nodal_coordinates_of_selected_point(self, selection: Node | Point):
        self.lineEdit_connecting_coord_x.setText(f"{selection.x:.6f}")
        self.lineEdit_connecting_coord_y.setText(f"{selection.y:.6f}")
        self.lineEdit_connecting_coord_z.setText(f"{selection.z:.6f}")

    def update_sections_info_callback(self):
        if self.comboBox_volume_sections.currentIndex() == VolumeSections.DISTINCT:
            return

        _outside_diameter = self.lineEdit_outside_diameter_liquid.text()
        self.lineEdit_outside_diameter_gas.setText(_outside_diameter)

        _wall_thickness = self.lineEdit_wall_thickness_liquid.text()
        self.lineEdit_wall_thickness_gas.setText(_wall_thickness)

    def load_fluid_properties(self, fluid: Fluid):
        pressure = fluid.pressure
        temperature = fluid.temperature
        isentropic_exponent = fluid.isentropic_exponent

        self.lineEdit_gas_pressure.setText(f"{pressure: .8e}")
        self.lineEdit_gas_temperature.setText(f"{temperature: .6f}")
        self.lineEdit_polytropic_exponent.setText(f"{isentropic_exponent: .6f}")

    def _config_widgets(self):
        # Replace placeholder widget with the actual render widget
        self.preview_widget = DamperPreviewRenderWidget()
        self.preview_widget.set_isometric_view()
        self.preview_widget_placeholder.parent().layout().replaceWidget(
            self.preview_widget_placeholder,
            self.preview_widget,
        )
        #
        self.lineEdit_damper_label.setFocus()
        self.lineEdit_selected_damper_label.setDisabled(True)
        self.lineEdit_damper_type.setDisabled(True)
        self.pushButton_remove.setDisabled(True)
        self.pushButton_edit.setDisabled(True)
        self.pushButton_copy.setDisabled(True)
        #
        self.config_treeWidget()

    def config_treeWidget(self):

        header_labels = ["Label", "Damper type", "Gas volume [m³]", "Lines"]
        for col, label in enumerate(header_labels):
            self.treeWidget_pulsation_damper_info.headerItem().setText(col, label)
            self.treeWidget_pulsation_damper_info.headerItem().setTextAlignment(col, Qt.AlignCenter)

        self.treeWidget_pulsation_damper_info.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def get_liquid_fluid_callback(self):
        self.fluid_state = "liquid"
        self.get_fluid_callback()

    def get_gas_fluid_callback(self):
        self.fluid_state = "gas"
        self.get_fluid_callback()

    def get_fluid_callback(self):
        self.hide()
        if not self.state_properties:

            self.state_properties["editable_state"] = True

        if self.lineEdit_gas_pressure.text() != "":
            self.state_properties["pressure"] = float(self.lineEdit_gas_pressure.text())
            self.state_properties["pressure_unit"] = self.comboBox_pressure_units.currentText()

        if self.lineEdit_gas_temperature.text() != "":
            self.state_properties["temperature"] = float(self.lineEdit_gas_temperature.text())
            self.state_properties["temperature_unit"] = self.comboBox_temperature_units.currentText()

        check_ideal_gas = False
        if isinstance(self.selected_fluid, Fluid) and isinstance(self.gas_fluid, Fluid):
            check_ideal_gas = self.selected_fluid == self.gas_fluid

        if self.lineEdit_selected_liquid_fluid.text() != "":
            self.state_properties["editable_state"] = False

        self.state_properties["check_ideal_gas"] = check_ideal_gas

        self.fluid_dialog = SetFluidInputSimplified(state_properties=self.state_properties)
        self.fluid_dialog.fluid_widget.pushButton_attribute.setText("Select fluid")
        self.fluid_dialog.pushButton_attribute.clicked.connect(self.get_selected_fluid)
        self.fluid_dialog.exec_and_keep_window_open()
        app().main_window.set_input_widget(self)

    def update_state_properties_from_fluid(self, selected_fluid: Fluid | None):
        if selected_fluid is None:
            return

        pressure_Pa = selected_fluid.pressure
        temperature_K = selected_fluid.temperature

        pres_unit = self.comboBox_pressure_units.currentText()
        temp_unit = self.comboBox_temperature_units.currentText()

        _pressure = convert_pressure_unit(pressure_Pa, "Pa", pres_unit)
        _temperature = convert_temperature_unit(temperature_K, "K", temp_unit)

        self.state_properties["pressure"] = _pressure
        self.state_properties["temperature"] = _temperature

        self.lineEdit_gas_pressure.setText(f"{_pressure : .8e}")
        self.lineEdit_gas_temperature.setText(f"{_temperature : .6f}")

        if self.fluid_state == "liquid":
            return

        self.lineEdit_polytropic_exponent.setText(f"{selected_fluid.isentropic_exponent}")

    def get_selected_fluid(self, fluid: Fluid | None = None):
        if fluid is False:
            selected_fluid = self.fluid_dialog.get_selected_fluid()

        elif isinstance(fluid, Fluid):
            selected_fluid = fluid

        else:
            raise TypeError("Invalid fluid")

        if not isinstance(selected_fluid, Fluid):
            return

        if self.fluid_dialog is not None:
            self.fluid_dialog.close()

            if selected_fluid.name in self.fluid_dialog.fluid_widget.fluid_name_to_refprop_data.keys():
                self.comboBox_fluid_data_source.setCurrentIndex(0)

        if self.fluid_state == "liquid":
            self.lineEdit_selected_liquid_fluid.setText(selected_fluid.name)
            self.liquid_fluid = selected_fluid
            self.state_properties["editable_state"] = True

        else:
            self.lineEdit_selected_gas_fluid.setText(selected_fluid.name)
            self.gas_fluid = selected_fluid

        self.update_state_properties_from_fluid(selected_fluid)

    def tab_event_callback(self):
        self.pushButton_remove.setDisabled(True)
        self.pushButton_edit.setDisabled(True)
        self.pushButton_copy.setDisabled(True)
        if self.tabWidget_main.currentIndex() == 0:
            self.pushButton_create.setDisabled(False)
        else:
            self.pushButton_create.setDisabled(True)

    def on_click_item(self, item):
        self.pushButton_remove.setDisabled(False)
        self.pushButton_edit.setDisabled(False)
        self.pushButton_copy.setDisabled(False)
        self.lineEdit_selected_damper_label.setText(item.text(0))

        if item.text(0) in self.pulsation_damper_lines.keys():
            damper_lines = self.pulsation_damper_lines[item.text(0)]
            app().main_window.set_selection(lines=damper_lines)

    def on_double_click_item(self, item):
        self.on_click_item(item)

    # def load_state_properties(self):

    #     if not self.state_properties:
    #         return

    #     pressure = self.state_properties["pressure"]
    #     temperature = self.state_properties["temperature"]

    #     press_unit = self.state_properties.get("pressure_unit", "kgf/cm² (a)")
    #     temp_unit = self.state_properties.get("temperature_unit", "°C")

    #     self.lineEdit_gas_temperature.setText(f"{temperature}")
    #     self.lineEdit_gas_pressure.setText(f"{pressure : .8e}")

    #     self.comboBox_temperature_units.setCurrentText(temp_unit)
    #     self.comboBox_pressure_units.setCurrentText(press_unit)

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
        equal_sections = self.comboBox_volume_sections.currentIndex() == VolumeSections.EQUAL
        self.lineEdit_outside_diameter_gas.setDisabled(equal_sections)
        self.lineEdit_wall_thickness_gas.setDisabled(equal_sections)

        if equal_sections:
            outside_diameter = self.lineEdit_outside_diameter_liquid.text()
            wall_thickness = self.lineEdit_wall_thickness_liquid.text()
            self.lineEdit_outside_diameter_gas.setText(outside_diameter)
            self.lineEdit_wall_thickness_gas.setText(wall_thickness)

    def check_connecting_coords(self):

        line_edits = [
            self.lineEdit_connecting_coord_x,
            self.lineEdit_connecting_coord_y,
            self.lineEdit_connecting_coord_z,
        ]

        coords = list()
        for line_edit in line_edits:
            if line_edit.text() == "":
                line_edit.setFocus()
                return True

            coords.append(round(float(line_edit.text()), 6))

        self._pulsation_damper_data["connecting_coords"] = coords

    def check_volumes(self):

        line_edits = [
            self.lineEdit_damper_volume,
            self.lineEdit_gas_volume,
        ]

        for line_edit in line_edits:
            if line_edit.text() == "":
                line_edit.setFocus()
                return True

        damper_volume = float(self.lineEdit_damper_volume.text())
        gas_volume = float(self.lineEdit_gas_volume.text())

        unit_label = self.comboBox_volume_unit.currentText()

        u_reg = UnitRegistry()
        if unit_label == "cubic centimeters":
            cubic_centimeter = u_reg("1 cm**3")
            volume_unit_factor = cubic_centimeter.to('m**3')

        elif unit_label == "liters":
            liter = u_reg("1 liter")
            volume_unit_factor = liter.to('m**3')

        else:
            volume_unit_factor = u_reg("1 m**3")

        self._pulsation_damper_data["damper_volume"] = damper_volume * volume_unit_factor.magnitude
        self._pulsation_damper_data["gas_volume"] = gas_volume * volume_unit_factor.magnitude

        if gas_volume > damper_volume:
            self.error_title = "Invalid gas volume"
            self.error_message = "The gas volume must be less than the damper volume."
            self.lineEdit_gas_volume.setFocus()
            return True

    def check_geometric_entries(self):

        line_edits = [
            self.lineEdit_outside_diameter_liquid,
            self.lineEdit_wall_thickness_liquid,
            self.lineEdit_outside_diameter_gas,
            self.lineEdit_wall_thickness_gas,
            self.lineEdit_outside_diameter_neck,
            self.lineEdit_neck_height,
        ]

        for line_edit in line_edits:

            if line_edit.isEnabled():
                if line_edit.text() == "":    
                    line_edit.setFocus()
                    return True           

            key = line_edit.objectName().replace("lineEdit_", "")
            self._pulsation_damper_data[key] = float(line_edit.text()) if line_edit.text() != "" else 0.

    def check_fluids(self):
        if self.liquid_fluid is None:
            self.get_liquid_fluid_callback()
            return True

        if self.gas_fluid is None:
            self.get_gas_fluid_callback()
            return True

        self._pulsation_damper_data["liquid_fluid_id"] = self.liquid_fluid.identifier
        self._pulsation_damper_data["gas_fluid_id"] = self.gas_fluid.identifier

    def check_pulsation_damper_geometric_inputs(self):
        self._pulsation_damper_data = dict()
        self._pulsation_damper_data["main_axis"] = self.comboBox_main_axis.currentText()
        self._pulsation_damper_data["damper_type"] = self.comboBox_damper_type.currentText()

        if self.check_connecting_coords():
            return True

        if self.check_volumes():
            return True

        if self.check_geometric_entries():
            return True

    def check_pulsation_damper_inputs(self):
        if self.check_pulsation_damper_geometric_inputs():
            return True

        if self.check_fluids():
            return True

    def get_values(self, values: np.ndarray):
        return list(np.array(np.round(values, 6), dtype=float))

    def is_valid_number(self, value: str, include_zero: bool = True):
        if value == "":
            return False

        try:
            _value = float(value.replace(",", "."))
            if include_zero:
                return True
            elif _value > 0:
                return True
        except Exception:
            return False

        return False

    def process_line_edits(self):
        line_edits = list()
        for line_edit in self.findChildren(QLineEdit):
            line_edits.append(line_edit)

        self.line_edits = line_edits
        self.possible_zeros = [
            self.lineEdit_connecting_coord_x,
            self.lineEdit_connecting_coord_y,
            self.lineEdit_connecting_coord_z,
            self.lineEdit_gas_temperature,
        ]

    def preview_callback(self):
        if self.check_pulsation_damper_geometric_inputs():
            for line_edit in self.findChildren(QLineEdit):
                line_edit: QLineEdit

                if not line_edit.isEnabled():
                    continue

                include_zero = False
                if line_edit in self.possible_zeros:
                    include_zero = True

                if line_edit == self.lineEdit_damper_label:
                    is_valid = len(line_edit.text()) > 0

                else:
                    is_valid = self.is_valid_number(line_edit.text(), include_zero=include_zero)

                style_sheet = self.default_style_sheet if is_valid else "border: 2px solid red"
                line_edit.setStyleSheet(style_sheet)
            self.preview_widget.turn_red()
            self.pushButton_show_errors.setDisabled(False)

        else:
            for line_edit in self.findChildren(QLineEdit):
                line_edit.setStyleSheet(self.default_style_sheet)

            self.pushButton_show_errors.setDisabled(True)
            self._pulsation_damper_data["liquid_fluid_id"] = "placeholder"
            self._pulsation_damper_data["gas_fluid_id"] = "placeholder"

            self.preview_widget.build_device_preview(self._pulsation_damper_data)
            self.preview_widget.config_view()
            self.preview_widget.update()

            self._pulsation_damper_data["liquid_fluid_id"] = None
            self._pulsation_damper_data["gas_fluid_id"] = None

    def automatic_preview(self):
        for line_edit in self.findChildren(QLineEdit):
            if line_edit is not self.lineEdit_damper_label:
                line_edit.textEdited.connect(self.preview_callback)

        for combo_box in self.findChildren(QComboBox):
            combo_box.currentIndexChanged.connect(self.preview_callback)

    def create_pulsation_damper_callback(self):
        if self.edited_damper:
            if self.previous_damper_label in self.dampers_data:
                self.remove_callback(self.previous_damper_label)

        stop, damper_label, _, _, _ = self.check_pulsation_damper_label()
        if stop:
            self.show_error_window_for_label()
            return

        if self.check_pulsation_damper_inputs():
            self.show_error_window_for_parameters()
            self._pulsation_damper_data.clear()
            return

        self.dampers_data[damper_label] = self._pulsation_damper_data

        self.preview_widget.close_preview()

        device = PulsationDamper(self._pulsation_damper_data)

        self.close()

        geometry_handler = GeometryHandler(app().project)
        geometry_handler.set_pipeline(geometry_handler.pipeline)
        geometry_handler.set_length_unit(geometry_handler.length_unit)
        geometry_handler.export_model_data_file()

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
                    "structure_name": "pipe",
                    "start_coords": self.get_values(start_coords),
                    "end_coords": self.get_values(end_coords),
                    "section_type_label": "pipe",
                    "section_parameters": section_data,
                    "structural_element_type": "pipe_1",
                    "pulsation_damper_label": damper_label,
                    "pulsation_damper_segment": segment_label,
                    "fluid_id": fluid_id,
                }

                if isinstance(self.selected_material, Material):
                    aux["material_id"] = self.selected_material.identifier

                tag = int(shifted_line + i)
                self.properties._set_multiple_line_properties(aux, tag)

        app().project.file.write_line_properties_in_file()
        self.write_pulsation_damper_element_properties_in_file(damper_label, device)

    def write_pulsation_damper_element_properties_in_file(self, damper_label: str, device: (PulsationDamper)):
        if self.dampers_data is None:
            return

        index = 0
        if damper_label in self.dampers_data.keys():
            for _coords, _elc_type in device.elc_data:
                index += 1
                coords = self.get_values(_coords)
                key = f"element_length_correction - {index}"
                self.dampers_data[damper_label][key] = {
                    "connection_coords": coords,
                    "elc_type": _elc_type,
                }

        app().project.file.write_pulsation_damper_data_in_file(self.dampers_data)

    def remove_pulsation_damper_related_line_properties(self, damper_labels: str | list):
        if isinstance(damper_labels, str):
            damper_labels = [damper_labels]

        lines_data = app().project.file.read_line_properties_from_file()
        if lines_data is None:
            return

        self.nodes_from_removed_lines.clear()

        remove_gaps = False
        for line_id, data in lines_data.items():
            pulsation_damper_label = data.get("pulsation_damper_label")
            if pulsation_damper_label is None:
                continue

            if pulsation_damper_label in damper_labels:
                self.properties._remove_line(line_id)
                line_nodes = self.preprocessor.mesh.nodes_from_line[int(line_id)]
                self.nodes_from_removed_lines.extend(list(line_nodes))
                remove_gaps = True

        app().project.file.write_line_properties_in_file()

        if remove_gaps:
            app().project.file.remove_line_gaps_from_line_properties_file()

    def set_element_length_corrections(self, damper_label: str, device: (PulsationDamper)):
        for coords, elc_type in device.elc_data:
            node_id = self.preprocessor.get_node_id_by_coordinates(coords)
            neigh_elements = self.preprocessor.acoustic_elements_connected_to_node[node_id]
            element_ids = [int(element.index) for element in neigh_elements]

            if elc_type == "side-branch":
                _type = 1

            else:
                _type = 0

            data = {
                "correction_type": _type,
                "coords": list(np.round(coords, 5)),
                "pulsation_damper_label": damper_label,
            }

            self.preprocessor.set_element_length_correction_by_element(element_ids, data)
            self.properties._set_element_property("element_length_correction", data, element_ids)
            app().project.file.write_element_properties_in_file()

    def remove_pulsation_damper_related_element_properties(self, damper_label: str):
        element_ids = list()
        for (_property, element_id), data in self.properties.element_properties.items():
            if _property == "element_length_correction":
                data: dict
                if "pulsation_damper_label" in data.keys():
                    if damper_label == "_remove_all_":
                        element_ids.append(element_id)
                    elif damper_label == data["pulsation_damper_label"]:
                        element_ids.append(element_id)

        self.preprocessor.set_element_length_correction_by_element(element_ids, None)
        self.properties._remove_element_property("element_length_correction", element_ids)
        app().project.file.write_element_properties_in_file()

    def remove_callback(self, label: str | None = None):

        damper_label = label if isinstance(label, str) else self.lineEdit_selected_damper_label.text()

        if not damper_label:
            return

        if damper_label in self.dampers_data.keys():
            self.dampers_data.pop(damper_label)

        self.remove_pulsation_damper_related_line_properties(damper_label)
        self.remove_pulsation_damper_related_element_properties(damper_label)
        self.actions_to_finalize()
        self.pushButton_remove.setDisabled(True)
        self.pushButton_edit.setDisabled(True)
        self.pushButton_copy.setDisabled(True)

    def insert_damper_data_on_interface(self, damper_label, coords: bool = True):
        if damper_label == "" or damper_label not in self.dampers_data:
            return

        data = self.dampers_data[damper_label]

        self.lineEdit_damper_label.setText(damper_label)

        if coords:
            cx, cy, cz = data["connecting_coords"]
            self.lineEdit_connecting_coord_x.setText(str(cx))
            self.lineEdit_connecting_coord_y.setText(str(cy))
            self.lineEdit_connecting_coord_z.setText(str(cz))

        damper_type = data["damper_type"]
        idx = self.comboBox_damper_type.findText(damper_type)
        if idx >= 0:
            self.comboBox_damper_type.setCurrentIndex(idx)

        idx = self.comboBox_main_axis.findText(data["main_axis"])
        if idx >= 0:
            self.comboBox_main_axis.setCurrentIndex(idx)

        # volume unit remains cubic meters because the values are automatically converted
        self.lineEdit_damper_volume.setText(str(data["damper_volume"]))
        self.lineEdit_gas_volume.setText(str(data["gas_volume"]))

        self.lineEdit_outside_diameter_liquid.setText(str(data["outside_diameter_liquid"]))
        self.lineEdit_wall_thickness_liquid.setText(str(data["wall_thickness_liquid"]))

        self.lineEdit_outside_diameter_gas.setText(str(data["outside_diameter_gas"]))
        self.lineEdit_wall_thickness_gas.setText(str(data["wall_thickness_gas"]))

        self.lineEdit_outside_diameter_neck.setText(str(data["outside_diameter_neck"]))
        self.lineEdit_neck_height.setText(str(data["neck_height"]))

        liquid_id = data["liquid_fluid_id"]
        gas_id = data["gas_fluid_id"]

        self.properties.set_fluids_library(self.properties.fluids_library)
        liquid = self.properties.fluids_library.get(liquid_id)
        gas = self.properties.fluids_library.get(gas_id)

        if liquid is not None:
            self.fluid_state = "liquid"
            self.get_selected_fluid(liquid)

        if gas is not None:
            self.fluid_state = "gas"
            self.get_selected_fluid(gas)

    def edit_callback(self):
        self.pushButton_create.setText("Confirm")
        self.pushButton_exit.setText("Cancel")

        damper_label = self.lineEdit_selected_damper_label.text()

        self.insert_damper_data_on_interface(damper_label)

        self.tabWidget_main.setCurrentIndex(0)
        self.preview_callback()

        self.edited_damper = True
        self.previous_damper_label = damper_label

    def copy_callback(self):
        damper_label = self.lineEdit_selected_damper_label.text()

        self.insert_damper_data_on_interface(damper_label, coords=False)

        self.tabWidget_main.setCurrentIndex(0)
        self.preview_callback()

        for coord in [
            self.lineEdit_connecting_coord_x,
            self.lineEdit_connecting_coord_y,
            self.lineEdit_connecting_coord_z,
        ]:
            coord.setText("")

        self.lineEdit_connecting_coord_x.setFocus()

    def reset_callback(self):
        self.hide()

        title = "Pulsation Dampers resetting"
        message = "Would you like to remove all the created Pulsation Dampers from the model?"

        buttons_config = {
            "left_button_label": "Cancel",
            "right_button_label": "Proceed",
        }
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        damper_labels = list(self.dampers_data.keys())
        self.dampers_data.clear()

        self.remove_pulsation_damper_related_line_properties(damper_labels)
        self.remove_pulsation_damper_related_element_properties("_remove_all_")
        self.actions_to_finalize()

    def reset_entries_callback(self):
        for key, value in self.__dict__.items():
            if isinstance(value, QLineEdit):
                value.setText(self.deafult_parameters[key])
        for key, value in self.__dict__.items():
            if isinstance(value, QComboBox):
                value.setCurrentIndex(self.deafult_parameters[key])

        self.preview_callback()

    def load_pulsation_damper_info(self):
        self.treeWidget_pulsation_damper_info.clear()
        self.pulsation_damper_lines = app().project.loader.get_pulsation_damper_related_lines()

        self.dampers_data = app().project.file.read_pulsation_damper_data_from_file()
        if self.dampers_data is None:
            self.dampers_data = dict()

        for key, damper_data in self.dampers_data.items():
            gas_volume = damper_data["gas_volume"]
            damper_type = damper_data["damper_type"]

            new = QTreeWidgetItem(
                [
                    key,
                    damper_type,
                    str(gas_volume),
                    str(self.pulsation_damper_lines[key]),
                ]
            )
            for col in range(4):
                new.setTextAlignment(col, Qt.AlignCenter)
            self.treeWidget_pulsation_damper_info.addTopLevelItem(new)

        self.tabWidget_main.setTabVisible(1, True)
        self.tabWidget_main.setCurrentIndex(0)

        self.pushButton_reset.setEnabled(bool(self.dampers_data))

    def get_duplicated_name(self, name: str) -> str:
        ends_with_copy_pattern = re.compile(r"\(\d+\)")
        digits_pattern = re.compile(r"\d+")

        def decouple_copy(text: str) -> tuple[str, str]:
            match = ends_with_copy_pattern.search(text)
            if match is None:
                return text, ""

            suffix = match.group().strip()
            preffix = text[: -len(suffix)].strip()
            return preffix, suffix

        def get_copy_number(copy_text: str) -> int:
            match = digits_pattern.search(copy_text)
            if match is None:
                return -1
            return int(match.group())

        preffix, suffix = decouple_copy(name)
        max_copy = get_copy_number(suffix)

        for name in self.dampers_data.keys():
            item_preffix, item_suffix = decouple_copy(name)
            if item_preffix == preffix:
                copy_number = get_copy_number(item_suffix)
                max_copy = max(max_copy, copy_number)

        name = f"{preffix} ({max_copy + 1})"

        self.lineEdit_damper_label.setText(name)

    def check_pulsation_damper_label(self):
        message = ""
        damper_label = self.lineEdit_damper_label.text()

        if damper_label == "":
            self.lineEdit_damper_label.setFocus()
            title = "Empty field detected"
            message = "Enter a damper label to proceed."

        elif damper_label in self.dampers_data.keys():
            self.get_duplicated_name(damper_label)
            damper_label = self.lineEdit_damper_label.text()

        if message != "":
            self.hide()
            return True, None, warning_title, title, message

        return False, damper_label, None, None, None

    def show_error_window_for_label(self):
        _, _, window_title, title, message = self.check_pulsation_damper_label()
        if window_title is not None and title is not None and message is not None:
            app().main_window.set_input_widget(self)
            PrintMessageInput([window_title, title, message])

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
                return None, None, None
                message = f"You have typed an invalid value to the {label}."

        else:
            message = f"None value has been typed to the {label}."
            return None

        if message != "":
            self.hide()
            return error_title, title, message

        return value, None, None

    def show_error_window_for_parameters(self):
        if warning_title is not None and self.error_title is not None and self.error_message is not None:
            app().main_window.set_input_widget(self)
            PrintMessageInput([warning_title, self.error_title, self.error_message])

        else:
            PrintMessageInput(
                [
                    warning_title,
                    "Invalid input",
                    "An empty or invalid field was detected",
                ]
            )

    def get_device_tag(self):
        index = 1
        _run = True
        while _run:
            if index in self.dampers_data.keys():
                index += 1
            else:
                _run = False
        return index

    def actions_to_finalize(self):
        app().main_window.reset_solution()
        app().main_window.set_selection()
        app().project.file.write_pulsation_damper_data_in_file(self.dampers_data)

        app().project.loader.load_project_data()
        app().project.initial_load_project_actions()

        if app().project.file.check_pipeline_data():
            app().project.loader.load_mesh_dependent_properties()
            app().main_window.initial_project_action(True)
        else:
            self.preprocessor.mesh._create_gmsh_geometry()

        self.load_pulsation_damper_info()

        app().main_window.update_plots()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.create_pulsation_damper_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        self.preview_widget.close_preview()
        return super().closeEvent(a0)
