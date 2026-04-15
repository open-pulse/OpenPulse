from collections import defaultdict
from enum import IntEnum

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QTreeWidgetItem

from pulse import app
from pulse.interface.ui_generated.model.setup.structural.valve_input_ui import (
    ValveInput_UI,
)
from pulse.interface.user_input.model.setup.acoustic.perforated_plate_input import (
    PerforatedPlateInput,
)
from pulse.interface.user_input.model.setup.structural.structural_lines_input import (
    StructuralLinesInput,
)
from pulse.interface.user_input.numeric_checks.validators import StrictDoubleValidator
from pulse.interface.user_input.project.get_user_confirmation_input import (
    GetUserConfirmationInput,
)
from pulse.model.cross_section import CrossSection


class TabIndex(IntEnum):
    SETUP = 0
    LIST = 1


class FlangeSetup(IntEnum):
    UNFLANGED = 0
    FLANGED = 1


class AcousticBehavior(IntEnum):
    OPEN = 0
    PARTIALLY_CLOSED = 1
    CLOSED = 2


error_title = "Error"


class ValvesInput(StructuralLinesInput, ValveInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.render_type = kwargs.get("render_type", "model")

        self._initialize()
        self._configure_validators()
        self._create_connections()
        self._configure_appearance()

        if self.render_type == "model":
            self._config_widgets()
            self.load_valves_info()
            self.selection_callback()
            self.exec_callback()

    def exec_callback(self):
        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.complete = False
        self.keep_window_open = True

    def _configure_validators(self):

        validator = StrictDoubleValidator(0, 1e10, 6)

        for line_edit in self.findChildren(QLineEdit):
            obj_name = line_edit.objectName()

            if obj_name in ["lineEdit_selected_id", "lineEdit_valve_name"]:
                continue

            line_edit.setValidator(validator)

    def _configure_appearance(self):
        if self.render_type == "model":
            self.selection_frame.setVisible(True)
        else:
            self.selection_frame.setVisible(False)
            self.tabWidget_main.setTabVisible(1, False)

        self.setMinimumHeight(620)

    def _config_widgets(self):
        #
        for i, width in enumerate([100, 120, 160]):
            self.treeWidget_valves_info.setColumnWidth(i, width)
            self.treeWidget_valves_info.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.comboBox_acoustic_behavior.currentIndexChanged.connect(self.valve_setup_callback)
        self.comboBox_flange_setup.currentIndexChanged.connect(self.valve_setup_callback)
        #
        self.pushButton_reset_entries.clicked.connect(self.reset_entries_callback)
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
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

            if len(line_ids) != 1:
                return
        
            line_id = line_ids[0]
            valve_info = self.properties._get_property(
                "valve_info", line_id=line_id
            )
            if valve_info is None:
                return
            
            self.load_valve_info(valve_info)

    def load_valve_info(self, valve_info: dict):

        for key, value in valve_info.items():
            if isinstance(value, float):
                value = str(value)

            try:
                widget = getattr(self, f"lineEdit_{key}")
            except Exception:
                continue

            if isinstance(widget, QLineEdit):
                widget.setText(value)

        if "flange_diameter" in valve_info.keys():
            self.comboBox_flange_setup.setCurrentIndex(FlangeSetup.FLANGED)
        else:
            self.comboBox_flange_setup.setCurrentIndex(FlangeSetup.UNFLANGED)

        if "acoustic_behavior" in valve_info.keys():
            self.comboBox_acoustic_behavior.setCurrentIndex(valve_info.get("acoustic_behavior"))

    def tab_event_callback(self):
        self.pushButton_remove.setDisabled(True)
        tab_list = self.tabWidget_main.currentIndex() == TabIndex.LIST
        self.selection_frame.setDisabled(tab_list)
        self.pushButton_attribute.setDisabled(tab_list)

        if tab_list:
            selected_items = self.treeWidget_valves_info.selectedItems()
            if selected_items == list():
                self.lineEdit_selected_id.clear()
            else:
                self.on_click_item(selected_items[0])

            # self.selection_callback()
            self.lineEdit_selected_id.setEnabled(True)
            return


    def valve_setup_callback(self):
        self.acoustic_effects_callback()
        self.flanged_valves_callback()

    def acoustic_effects_callback(self):

        index = self.comboBox_acoustic_behavior.currentIndex()
        open_valve = index == AcousticBehavior.OPEN

        if index == AcousticBehavior.PARTIALLY_CLOSED:
            self.label_valve_internal_length.setText("Orifice plate thickness:")

        elif index == AcousticBehavior.CLOSED:
            self.label_valve_internal_length.setText("Valve blocking length:")

        self.label_valve_internal_length.setDisabled(open_valve)
        self.label_valve_internal_length_unit.setDisabled(open_valve)
        self.lineEdit_internal_valve_length.setDisabled(open_valve)

        if open_valve:
            self.lineEdit_internal_valve_length.clear()

    def flanged_valves_callback(self):

        flanged = self.comboBox_flange_setup.currentIndex() == FlangeSetup.FLANGED

        self.label_flange_diameter.setEnabled(flanged)
        self.label_flange_diameter_unit.setEnabled(flanged)
        self.label_flange_length.setEnabled(flanged)
        self.label_flange_length_unit.setEnabled(flanged)
        self.lineEdit_flange_diameter.setEnabled(flanged)
        self.lineEdit_flange_length.setEnabled(flanged)

        if not flanged:
            self.lineEdit_flange_diameter.clear()
            self.lineEdit_flange_length.clear()

    def load_valves_info(self):

        self.pushButton_remove.setDisabled(True)
        self.treeWidget_valves_info.clear()

        for line_id, data in self.properties.line_properties.items():
            if "valve_info" in data.keys():
                valve_info = data["valve_info"]
                valve_name = valve_info["valve_name"]
                mass = valve_info["valve_mass"]
                stiffening_factor = valve_info["stiffening_factor"]
                acoustic_effects = valve_info["acoustic_behavior"]
                effective_diameter = valve_info["valve_effective_diameter"]

                parameters = str(
                    [effective_diameter, stiffening_factor, mass, acoustic_effects]
                )

                item = QTreeWidgetItem([valve_name, str(line_id), parameters])
                for i in range(3):
                    item.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_valves_info.addTopLevelItem(item)

        self.update_tab_visibility()

    def update_tab_visibility(self):

        self.pushButton_remove.setDisabled(True)
        for data in self.properties.line_properties.values():
            if "valve_info" not in data.keys():
                continue

            self.tabWidget_main.setTabVisible(TabIndex.LIST, True)
            return
            
        self.tabWidget_main.setTabVisible(TabIndex.LIST, False)
        self.tabWidget_main.setCurrentIndex(TabIndex.SETUP)
        self.lineEdit_valve_name.setFocus()

        if not self.lineEdit_selected_id.isEnabled():
            self.lineEdit_selected_id.setEnabled(True)     

    def check_flanges_by_lines(self):
        elements_from_line = defaultdict(list)
        for element_id in app().main_window.list_selected_elements():
            line = self.preprocessor.mesh.line_from_element[element_id]
            elements_from_line[line].append(element_id)

        return elements_from_line

    def check_selection_type(self, line_ids: list):

        for line_id in line_ids:
            structural_element = self.properties._get_property(
                "structural_element_type", line_id=line_id
            )
            if structural_element in ["beam_1", "expansion_joint"]:
                self.lineEdit_selected_id.clear()
                self.lineEdit_selected_id.setFocus()
                return True

        return False

    def check_valve_parameters(self):

        self.valve_name = ""
        if self.lineEdit_valve_name.text() == "":
            self.lineEdit_valve_name.setFocus()
            return True

        self.valve_name = self.lineEdit_valve_name.text()
        self.valve_info["valve_name"] = self.valve_name

        line_edits = [
            self.lineEdit_valve_mass,
            self.lineEdit_stiffening_factor,
            self.lineEdit_valve_effective_diameter,
            self.lineEdit_valve_wall_thickness,
            ]

        for line_edit in line_edits:
            if line_edit.text() == "":
                line_edit.setFocus()
                return True

            obj_name = line_edit.objectName()
            var_name = obj_name.split("lineEdit_")[1]

            self.valve_info[var_name] = float(line_edit.text())

    def check_flange_parameters(self):

        line_edits = [
            self.lineEdit_flange_diameter,
            self.lineEdit_flange_length,
        ]

        for line_edit in line_edits:
            if line_edit.text() == "":
                line_edit.setFocus()
                return True

            obj_name = line_edit.objectName()
            var_name = obj_name.split("lineEdit_")[1]

            self.valve_info[var_name] = float(line_edit.text())

        return False

    def check_internal_valve_parameters(self):

        if self.lineEdit_internal_valve_length.text() == "":
            self.lineEdit_internal_valve_length.setFocus()
            return True

        value = float(self.lineEdit_internal_valve_length.text())

        if self.comboBox_acoustic_behavior.currentIndex() == AcousticBehavior.PARTIALLY_CLOSED:
            self.valve_info["orifice_plate_thickness"] = value

        elif self.comboBox_acoustic_behavior.currentIndex() == AcousticBehavior.CLOSED:
            self.valve_info["blocking_length"] = value

    def attribute_callback(self):

        self.valve_info = dict()

        if self.render_type == "model":
            lineEdit_selection = self.lineEdit_selected_id.text()
            stop, line_ids = self.before_run.check_selected_ids(
                lineEdit_selection, "lines"
            )
            if stop:
                return

            if self.check_selection_type(line_ids):
                return

        if self.check_valve_parameters():
            return

        acoustic_behavior = self.comboBox_acoustic_behavior.currentIndex()
        if acoustic_behavior != AcousticBehavior.OPEN:
            if self.check_internal_valve_parameters():
                return

        self.valve_info["acoustic_behavior"] = acoustic_behavior

        if self.comboBox_flange_setup.currentIndex() == FlangeSetup.FLANGED:
            if self.check_flange_parameters():
                return

        self.add_section_parameters_into_valve_info()

        if self.render_type == "model":
            if self.valve_info:
                for line_id in line_ids:
                    self.properties._set_line_property("structure_name", "valve", line_id)
                    self.properties._set_line_property("section_type_label", "valve", line_id)
                    self.properties._set_line_property("structural_element_type", "valve", line_ids=line_id)
                    self.properties._set_line_property("valve_info", self.valve_info, line_ids=line_id)

                    line_data = self.properties.line_properties[line_id]
                    self.preprocessor.set_cross_sections_to_valve_elements(line_id, line_data)

                    self.properties._remove_line_property("section_parameters", line_id)
                    self.properties._remove_line_property("expansion_joint_info", line_id)

                self.actions_to_finalize()

                if acoustic_behavior == 1:
                    self.configure_orifice_plate(line_ids)

        self.complete = True
        self.close()

    def actions_to_finalize(self):

        app().project.file.write_line_properties_in_file()
        app().project.file.write_imported_table_data_in_file()

        # geometry_handler = GeometryHandler(app().project)
        # geometry_handler.set_length_unit(app().project.model.mesh.length_unit)
        # geometry_handler.process_pipeline()

        app().project.loader.load_project_data()
        app().project.initial_load_project_actions()
        app().project.loader.load_mesh_dependent_properties()
        app().main_window.initial_project_action(True)
        app().main_window.update_plots()
        self.complete = True

    def configure_orifice_plate(self, line_ids: list):

        self.hide()

        title = "Orifice plate configuration"
        message = "Would you like to configure the orifice plate right now?"

        buttons_config = {"left_button_label": "No", "right_button_label": "Yes"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        element_ids = list()
        for line_id in line_ids:
            line_elements = app().project.model.mesh.elements_from_line[line_id]
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

    def add_section_parameters_into_valve_info(self):

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

        line_to_elements = app().project.model.mesh.elements_from_line
        line_elements = line_to_elements[line_id]

        element_ids = [
            line_elements[0] - 1,
            line_elements[0] + 1,
            line_elements[-1] - 1,
            line_elements[-1] + 1,
        ]

        for element_id in element_ids:
            if element_id not in line_elements:
                if element_id in self.preprocessor.structural_elements.keys():
                    cross = self.preprocessor.structural_elements[
                        element_id
                    ].cross_section
                    element_type = self.preprocessor.structural_elements[
                        element_id
                    ].element_type
                    if element_type == "pipe_1":
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
            valve_section_parameters = [
                outer_diameter,
                thickness,
                offset_y,
                offset_z,
                0,
                0,
            ]

        return valve_section_parameters

    def on_click_item(self, item: QTreeWidgetItem):
        self.lineEdit_selected_id.setText(item.text(0))
        self.pushButton_remove.setEnabled(True)
        if item.text(0) != "":
            line_ids = [int(item.text(1))]
            app().main_window.set_selection(lines=line_ids)

    def on_doubleclick_item(self, item: QTreeWidgetItem):
        self.on_click_item(item)

    def restore_the_cross_section(self, line_ids: list):

        line_to_elements = app().project.model.mesh.elements_from_line
        for line_id in line_ids:
            line_elements = line_to_elements[line_id]

            element_ids = [
                line_elements[0] - 1,
                line_elements[0] + 1,
                line_elements[-1] - 1,
                line_elements[-1] + 1,
            ]
            cross = None
            element_type = None

            for element_id in element_ids:
                # get the cross-section of the first out-of-line valid element
                if element_id not in line_elements:
                    element = self.preprocessor.structural_elements[element_id]
                    cross = element.cross_section
                    element_type = element.element_type
                    break

            if element_type == "pipe_1" and isinstance(cross, CrossSection):
                pipe_info = {
                    "structure_name" : "pipe",
                    "section_type_label" : "pipe",
                    "section_parameters" : cross.section_parameters,
                    }

                self.properties._set_line_property("structural_element_type", element_type, line_id)
                self.properties._set_multiple_line_properties(pipe_info, line_id)

    def remove_callback(self):
        if self.lineEdit_selected_id.text() != "":
            line_id = int(self.lineEdit_selected_id.text())

            self.properties._remove_line_property("valve_info", line_id)

            self.restore_the_cross_section([line_id])

            self.load_valves_info()
            self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Removal of all valves from model"
        message = "Would you like to remove all valves from the model?"

        buttons_config = {
            "left_button_label": "Cancel",
            "right_button_label": "Continue",
        }
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        line_ids = list()
        for line_id, data in self.properties.line_properties.items():
            data: dict
            if "valve_info" in data.keys():
                line_ids.append(line_id)

        for line_id in line_ids:
            self.properties._remove_line_property("valve_info", line_id)
            self.restore_the_cross_section(line_ids)

        if line_ids:
            self.load_valves_info()
            self.actions_to_finalize()

    def remove_valve_acoustic_effects_function(self, valve_names: list):

        element_ids = list()
        for valve_name in valve_names:
            for (
                property,
                element_id,
            ), data in self.properties.element_properties.items():
                if property == "perforated_plate":
                    if "valve_info" in data.keys():
                        if valve_name == data["valve_info"]["valve_name"]:
                            element_ids.append(element_id)
                            break

        if element_ids:
            self.properties._remove_element_property("perforated_plate", element_ids)
            # TODO: remove existing imported tables

    def reset_entries_callback(self):
        for line_edit in self.findChildren(QLineEdit):
            line_edit.clear()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()

        if event.key() == Qt.Key_Delete:
            if self.render_type == "model":
                self.remove_callback()

        if event.key() == Qt.Key_Escape:
            self.close()


def get_V_linear_distribution(x, N, reduction_start=0.0, reduction_half=0.5):

    if N == 3:
        reduction_start = 25

    output = np.zeros(N)
    x_i = x * (1 - reduction_start)
    x_m = x * (1 - reduction_half)

    if N == 1:
        return x_m

    if np.remainder(N, 2) == 0:
        half = int(N / 2)
        shift = 0
    else:
        half = int((N + 1) / 2)
        shift = 1

    output[0:half] = get_linear_distribution(x_i, x_m, half)
    output[half - shift :] = get_linear_distribution(x_m, x_i, half)

    return output


def get_linear_distribution(x_initial, x_final, N):
    n = np.arange(N) / (N - 1)
    return (x_final - x_initial) * n + x_initial