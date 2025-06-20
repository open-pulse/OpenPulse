import numpy as np
from molde import load_ui
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QTabWidget,
    QTreeWidget,
    QTreeWidgetItem,
)

from pulse import UI_DIR, app
from pulse.editor.pulsation_damper import PulsationDamper
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.model.setup.fluid.set_fluid_input_simplified import (
    SetFluidInputSimplified,
)
from pulse.interface.user_input.project.get_user_confirmation_input import (
    GetUserConfirmationInput,
)
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.viewer_3d.render_widgets.damper_preview_render_widget import (
    DamperPreviewRenderWidget,
)
from pulse.model.properties.fluid import Fluid
from pulse.model.properties.material import Material

window_title_1 = "Error"
window_title_2 = "Warning"


class PulsationDamperEditorInputs(QDialog):
    def __init__(self, *args, device_to_delete=None, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/editor/pulsation_damper_editor_inputs.ui"
        load_ui(ui_path, self, ui_path.parent)

        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties
        self.preprocessor = app().project.model.preprocessor
        self.default_style_sheet = self.styleSheet()

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()

        self.load_pulsation_damper_info()
        self.process_line_edits()
        self.selection_callback()
        self.update_pulsation_damper_label()
        self.preview_callback()
        self.automatic_preview()
        self._store_deafult_parameters()

        if device_to_delete is not None:
            self.tabWidget_main.setCurrentIndex(1)
            devices = self.treeWidget_pulsation_damper_info.findItems(
                device_to_delete, Qt.MatchExactly
            )
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

        self.gas_fluid = None
        self.liquid_fluid = None
        self.selected_fluid = None
        self.selected_material = None
        self.error_title = None
        self.error_message = None

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
        self.pushButton_show_errors: QPushButton
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

        # Qwidget
        self.preview_widget: DamperPreviewRenderWidget

    def _store_deafult_parameters(self):
        self.deafult_parameters = dict()
        for key, value in self.__dict__.items():
            if isinstance(value, QLineEdit):
                self.deafult_parameters[key] = value.text()
            elif isinstance(value, QComboBox):
                self.deafult_parameters[key] = value.currentIndex()

    def _create_connections(self):
        #
        self.comboBox_volume_sections.currentIndexChanged.connect(
            self.volume_sections_callback
        )
        self.comboBox_volume_unit.currentIndexChanged.connect(
            self.update_volume_unit_callback
        )
        self.comboBox_pressure_units.currentIndexChanged.connect(
            self.load_state_properties
        )
        self.comboBox_temperature_units.currentIndexChanged.connect(
            self.load_state_properties
        )
        #
        self.lineEdit_outside_diameter_liquid.textEdited.connect(
            self.update_sections_info_callback
        )
        self.lineEdit_wall_thickness_liquid.textEdited.connect(
            self.update_sections_info_callback
        )
        #
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_show_errors.clicked.connect(
            self.show_error_window_for_parameters
        )
        self.pushButton_create.clicked.connect(self.create_pulsation_damper_callback)
        self.pushButton_get_gas_fluid.clicked.connect(self.get_gas_fluid_callback)
        self.pushButton_get_liquid_fluid.clicked.connect(self.get_liquid_fluid_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_reset_entries.clicked.connect(self.reset_entries_callback)

        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_pulsation_damper_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_pulsation_damper_info.itemDoubleClicked.connect(
            self.on_double_click_item
        )
        #
        app().main_window.selection_changed.connect(self.selection_callback)
        #
        self.volume_sections_callback()

    def selection_callback(self):
        selected_nodes = app().main_window.list_selected_nodes()
        selected_points = app().project.pipeline.selected_points

        if len(selected_nodes) == 1:
            node = self.preprocessor.nodes[selected_nodes[0]]
            self.lineEdit_connecting_coord_x.setText(f"{node.x:.3f}")
            self.lineEdit_connecting_coord_y.setText(f"{node.y:.3f}")
            self.lineEdit_connecting_coord_z.setText(f"{node.z:.3f}")

            elements = self.preprocessor.structural_elements_connected_to_node[
                node.external_index
            ]
            self.selected_material = None
            material = elements[0].material

            if material is None:
                return

            self.selected_material = material
            app().main_window.selection_changed.connect(self.selection_callback)

        elif len(selected_points) == 1:
            point = selected_points[0]
            self.lineEdit_connecting_coord_x.setText(f"{point.x:.3f}")
            self.lineEdit_connecting_coord_y.setText(f"{point.y:.3f}")
            self.lineEdit_connecting_coord_z.setText(f"{point.z:.3f}")

        app().main_window.geometry_widget.left_released.connect(self.selection_callback)

    def update_sections_info_callback(self):
        if self.comboBox_volume_sections.currentIndex() == 0:
            try:
                _outside_diameter = self.lineEdit_outside_diameter_liquid.text()
                _outside_diameter = _outside_diameter.replace(",", ".")
                float(_outside_diameter)
                self.lineEdit_outside_diameter_gas.setText(_outside_diameter)

            except Exception:
                self.lineEdit_outside_diameter_gas.setText("")

            try:
                _wall_thickness = self.lineEdit_wall_thickness_liquid.text()
                _wall_thickness = _wall_thickness.replace(",", ".")
                float(_wall_thickness)
                self.lineEdit_wall_thickness_gas.setText(_wall_thickness)

            except Exception:
                self.lineEdit_wall_thickness_gas.setText("")

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
        #
        self.config_treeWidget()

    def config_treeWidget(self):
        widths = [120, 140, 160, 40]
        header_labels = ["Label", "Damper type", "Gas volume [m³]", "Lines"]
        for col, label in enumerate(header_labels):
            self.treeWidget_pulsation_damper_info.headerItem().setText(col, label)
            self.treeWidget_pulsation_damper_info.headerItem().setTextAlignment(
                col, Qt.AlignCenter
            )
            self.treeWidget_pulsation_damper_info.setColumnWidth(col, widths[col])

    def get_liquid_fluid_callback(self):
        self.fluid_state = "liquid"
        self.get_fluid_callback()

    def get_gas_fluid_callback(self):
        self.fluid_state = "gas"
        self.get_fluid_callback()

    def get_fluid_callback(self):
        self.hide()
        self.fluid_dialog = SetFluidInputSimplified(
            state_properties=self.state_properties
        )
        self.fluid_dialog.fluid_widget.pushButton_attribute.setText("Select fluid")
        self.fluid_dialog.pushButton_attribute.clicked.connect(self.get_selected_fluid)
        self.fluid_dialog.exec_and_keep_window_open()
        app().main_window.set_input_widget(self)

    def get_selected_fluid(self):
        selected_fluid = self.fluid_dialog.get_selected_fluid()

        if isinstance(selected_fluid, Fluid):
            self.fluid_dialog.close()
            if (
                selected_fluid.name
                in self.fluid_dialog.fluid_widget.fluid_name_to_refprop_data.keys()
            ):
                self.comboBox_fluid_data_source.setCurrentIndex(0)

            if self.fluid_state == "liquid":
                self.lineEdit_selected_liquid_fluid.setText(selected_fluid.name)
                self.liquid_fluid = selected_fluid
                self.state_properties["pressure"] = selected_fluid.pressure
                self.state_properties["temperature"] = selected_fluid.temperature

            else:
                self.lineEdit_selected_gas_fluid.setText(selected_fluid.name)
                self.lineEdit_polytropic_exponent.setText(
                    f"{selected_fluid.isentropic_exponent: .6f}"
                )
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
            app().main_window.set_selection(lines=damper_lines)

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

            else:
                raise ValueError(f'Invalid pu_index "{pu_index}"')

            self.lineEdit_gas_pressure.setText(f"{pressure_value: .8e}")

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

    def check_inputs(
        self, lineEdit, label, only_positive=True, zero_included=False, title=None
    ):
        message = ""
        if title is None:
            title = "Invalid input"

        if lineEdit.text() != "":
            try:
                str_value = lineEdit.text().replace(",", ".")
                out = float(str_value)

                if only_positive:
                    if zero_included:
                        if out < 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nZero value is allowed."
                            return None
                    else:
                        if out <= 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nZero value is not allowed."
                            return None

            except Exception as error_log:
                message = f"Wrong input for {label}.\n\n"
                message += str(error_log)
                return None

        else:
            if zero_included:
                return float(0)
            else:
                message = f"Insert some value at the {label} input field."
                return None

        return out

    def check_connecting_coords(self):
        coord_x = self.check_inputs(
            self.lineEdit_connecting_coord_x,
            "'connecting coord. x'",
            only_positive=False,
        )
        if coord_x is None:
            self.lineEdit_connecting_coord_x.setFocus()
            return True

        coord_y = self.check_inputs(
            self.lineEdit_connecting_coord_y,
            "'connecting coord. y'",
            only_positive=False,
        )
        if coord_y is None:
            self.lineEdit_connecting_coord_y.setFocus()
            return True

        coord_z = self.check_inputs(
            self.lineEdit_connecting_coord_z,
            "'connecting coord. z'",
            only_positive=False,
        )
        if coord_z is None:
            self.lineEdit_connecting_coord_z.setFocus()
            return True

        self._pulsation_damper_data["connecting_coords"] = [
            round(coord_x, 6),
            round(coord_y, 6),
            round(coord_z, 6),
        ]

    def check_volumes(self):
        damper_volume = self.check_inputs(
            self.lineEdit_damper_volume, "'damper volume'", only_positive=False
        )
        if damper_volume is None:
            self.lineEdit_damper_volume.setFocus()
            return True

        gas_volume = self.check_inputs(
            self.lineEdit_gas_volume, "'gas volume'", only_positive=False
        )
        if gas_volume is None:
            self.lineEdit_gas_volume.setFocus()
            return True

        unit_label = self.comboBox_volume_unit.currentText()

        if unit_label == " cubic centimeters":
            volume_unit_factor = 1e-6

        elif unit_label == " liters":
            volume_unit_factor = 1e-3

        else:
            volume_unit_factor = 1

        self._pulsation_damper_data["damper_volume"] = (
            damper_volume * volume_unit_factor
        )
        self._pulsation_damper_data["gas_volume"] = gas_volume * volume_unit_factor

    def check_geometric_entries(self):
        outside_diameter_liquid = self.check_inputs(
            self.lineEdit_outside_diameter_liquid,
            "'outside diameter (liquid)'",
            only_positive=False,
        )
        if (
            outside_diameter_liquid is None or outside_diameter_liquid == 0
        ) and self.lineEdit_outside_diameter_liquid.isEnabled():
            self.lineEdit_outside_diameter_liquid.setFocus()
            return True

        wall_thickness_liquid = self.check_inputs(
            self.lineEdit_wall_thickness_liquid,
            "'wall thickness (liquid)'",
            only_positive=False,
        )
        if (
            wall_thickness_liquid is None or wall_thickness_liquid == 0
        ) and self.lineEdit_wall_thickness_liquid.isEnabled():
            self.lineEdit_wall_thickness_liquid.setFocus()
            return True

        outside_diameter_gas = self.check_inputs(
            self.lineEdit_outside_diameter_gas,
            "'outside diameter (gas)'",
            only_positive=False,
        )
        if (
            outside_diameter_gas is None or outside_diameter_gas == 0
        ) and self.lineEdit_outside_diameter_gas.isEnabled():
            self.lineEdit_outside_diameter_gas.setFocus()
            return True

        wall_thickness_gas = self.check_inputs(
            self.lineEdit_wall_thickness_gas,
            "'wall thickness (gas)'",
            only_positive=False,
        )
        if (
            wall_thickness_gas is None or wall_thickness_gas == 0
        ) and self.lineEdit_wall_thickness_gas.isEnabled():
            self.lineEdit_wall_thickness_gas.setFocus()
            return True

        outside_diameter_neck = self.check_inputs(
            self.lineEdit_outside_diameter_neck,
            "'outside diameter (neck)'",
            only_positive=False,
        )
        if (
            outside_diameter_neck is None or outside_diameter_neck == 0
        ) and self.lineEdit_outside_diameter_neck.isEnabled():
            self.lineEdit_outside_diameter_neck.setFocus()
            return True

        neck_height = self.check_inputs(
            self.lineEdit_neck_height, "'neck heght'", only_positive=False
        )
        if (
            neck_height is None or neck_height == 0
        ) and self.lineEdit_neck_height.isEnabled():
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

    def check_pulsation_damper_geometric_inputs(self):
        self._pulsation_damper_data = dict()

        self._pulsation_damper_data["main_axis"] = (
            self.comboBox_main_axis.currentText()[1:]
        )
        self._pulsation_damper_data["damper_type"] = (
            self.comboBox_damper_type.currentText()
        )

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
                    is_valid = self.is_valid_number(
                        line_edit.text(), include_zero=include_zero
                    )

                style_sheet = (
                    self.default_style_sheet if is_valid else "border: 2px solid red"
                )
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
        stop, damper_label, _, _, _ = self.check_pulsation_damper_label()
        if stop:
            self.show_error_window_for_label()
            return

        if self.check_pulsation_damper_inputs():
            self.show_error_window_for_parameters()
            self._pulsation_damper_data.clear()
            return

        self.preview_widget.close_preview()
        aux = self.damper_data.copy()
        for key, data in aux.items():
            if data == self._pulsation_damper_data:
                self.damper_data.pop(key)
                break

        self.damper_data[damper_label] = self._pulsation_damper_data

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
            start_coords, end_coords, section_data, segment_label, fluid_id = (
                device.segment_data[i]
            )

            if isinstance(section_data, list):
                aux = {
                    "structure_name": "pipe",
                    "start_coords": self.get_values(start_coords),
                    "end_coords": self.get_values(end_coords),
                    "section_type_label": "pipe",
                    "section_parameters": section_data,
                    "structural_element_type": "pipe_1",
                    "pulsation_damper_name": damper_label,
                    "pulsation_damper_segment": segment_label,
                    "fluid_id": fluid_id,
                }

                if isinstance(self.selected_material, Material):
                    aux["material_id"] = self.selected_material.identifier

                tag = int(shifted_line + i)
                self.properties._set_multiple_line_properties(aux, tag)

        app().project.file.write_line_properties_in_file()
        self.write_pulsation_damper_element_properties_in_file(damper_label, device)

    def write_pulsation_damper_element_properties_in_file(
        self, damper_label: str, device: (PulsationDamper)
    ):
        if self.damper_data is None:
            return

        index = 0
        if damper_label in self.damper_data.keys():
            for _coords, _elc_type in device.elc_data:
                index += 1
                coords = self.get_values(_coords)
                key = f"element_length_correction - {index}"
                self.damper_data[damper_label][key] = {
                    "connection_coords": coords,
                    "elc_type": _elc_type,
                }

        app().project.file.write_pulsation_damper_data_in_file(self.damper_data)

    def remove_pulsation_damper_related_line_properties(
        self, damper_labels: str | list
    ):
        if isinstance(damper_labels, str):
            damper_labels = [damper_labels]

        lines_data = app().project.file.read_line_properties_from_file()
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

        app().project.file.write_line_properties_in_file()

        if remove_gaps:
            app().project.file.remove_line_gaps_from_line_properties_file()

    def set_element_length_corrections(
        self, damper_label: str, device: (PulsationDamper)
    ):
        for coords, elc_type in device.elc_data:
            node_id = self.preprocessor.get_node_id_by_coordinates(coords)
            neigh_elements = self.preprocessor.acoustic_elements_connected_to_node[
                node_id
            ]
            element_ids = [int(element.index) for element in neigh_elements]

            if elc_type == "side-branch":
                _type = 1

            else:
                _type = 0

            data = {
                "correction_type": _type,
                "coords": list(np.round(coords, 5)),
                "pulsation_damper_name": damper_label,
            }

            self.preprocessor.set_element_length_correction_by_element(
                element_ids, data
            )
            self.properties._set_element_property(
                "element_length_correction", data, element_ids
            )
            app().project.file.write_element_properties_in_file()

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
        self.properties._remove_element_property(
            "element_length_correction", element_ids
        )
        app().project.file.write_element_properties_in_file()

    def remove_callback(self):
        if self.lineEdit_selected_damper_label.text() != "":
            damper_label = self.lineEdit_selected_damper_label.text()

            if damper_label in self.damper_data.keys():
                self.damper_data.pop(damper_label)

            self.remove_pulsation_damper_related_line_properties(damper_label)
            self.remove_pulsation_damper_related_element_properties(damper_label)
            self.actions_to_finalize()
            self.pushButton_remove.setDisabled(True)

    def reset_callback(self):
        self.hide()

        title = "Pulsation Dampers resetting"
        message = (
            "Would you like to remove all the created Pulsation Dampers from the model?"
        )

        buttons_config = {
            "left_button_label": "Cancel",
            "right_button_label": "Proceed",
        }
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:
            damper_labels = list(self.damper_data.keys())
            self.damper_data.clear()

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
        self.pulsation_damper_lines = (
            app().project.loader.get_pulsation_damper_related_lines()
        )

        self.damper_data = app().project.file.read_pulsation_damper_data_from_file()
        if self.damper_data is None:
            self.damper_data = dict()

        for key, damper_data in self.damper_data.items():
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

        if self.damper_data:
            self.tabWidget_main.setTabVisible(1, True)
        else:
            self.tabWidget_main.setCurrentIndex(0)
            self.tabWidget_main.setTabVisible(1, False)

    def update_pulsation_damper_label(self):
        damper_label = self.lineEdit_damper_label.text()
        if damper_label in self.damper_data.keys():
            sufix = 0
            max_iter = 100
            _damper_label = damper_label

            while _damper_label in self.damper_data.keys() and sufix < max_iter:
                sufix += 1
                _damper_label = damper_label + f"_{sufix}"

            if _damper_label in self.damper_data.keys():
                damper_label = ""
            else:
                damper_label = _damper_label

        self.lineEdit_damper_label.setText(damper_label)

    def check_pulsation_damper_label(self):
        message = ""
        damper_label = self.lineEdit_damper_label.text()

        if damper_label == "":
            self.lineEdit_damper_label.setFocus()
            title = "Empty field detected"
            message = "Enter a damper label to proceed."

        elif damper_label in self.damper_data.keys():
            self.update_pulsation_damper_label()
            damper_label = self.lineEdit_damper_label.text()

        if message != "":
            self.hide()
            return True, None, window_title_2, title, message

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
            return window_title_1, title, message

        return value, None, None

    def show_error_window_for_parameters(self):
        if (
            window_title_2 is not None
            and self.error_title is not None
            and self.error_message is not None
        ):
            app().main_window.set_input_widget(self)
            PrintMessageInput([window_title_2, self.error_title, self.error_message])

        else:
            PrintMessageInput(
                [
                    window_title_2,
                    "Invalid input",
                    "An empty or invalid field was detected",
                ]
            )

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
        app().project.file.write_pulsation_damper_data_in_file(self.damper_data)

        app().project.loader.load_project_data()
        app().project.initial_load_project_actions()

        if app().project.file.check_pipeline_data():
            app().project.loader.load_mesh_dependent_properties()
            app().main_window.initial_project_action(True)
        else:
            self.preprocessor.mesh._create_gmsh_geometry()

        self.load_pulsation_damper_info()

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
        self.preview_widget.close_preview()
        return super().closeEvent(a0)
