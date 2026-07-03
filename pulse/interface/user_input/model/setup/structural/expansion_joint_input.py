from enum import IntEnum

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidgetItem

from pulse import app
from pulse.interface import error_title
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.ui_generated.model.setup.structural.expansion_joint_input_ui import (
    ExpansionJointInput_UI,
)
from pulse.interface.user_input.model.setup.structural.structural_lines_input import (
    StructuralLinesInput,
)
from pulse.interface.user_input.numeric_checks.double_validator import (
    StrictDoubleValidator,
)
from pulse.interface.user_input.project.get_user_confirmation_input import (
    GetUserConfirmationInput,
)
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.model.cross_section import CrossSection
from pulse.model.cross_sections.expansion_joint_cross_section import (
    ExpansionJointCrossSection,
)


class TabIndex(IntEnum):
    SETUP = 0
    LIST = 1


class DataType(IntEnum):
    CONSTANT_VALUES = 0
    TABULAR_VALUES = 1


class AxialStopRod(IntEnum):
    NOT_INCLUDED = 0
    INCLUDED = 1


class ExpansionJointInput(StructuralLinesInput, ExpansionJointInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.render_type = kwargs.get("render_type", "model")

        self._initialize()
        self._configure_validators()
        self._create_connections()
        self._configure_appearance()

        if self.render_type == "model":
            self._config_widgets()
            self.load_expansion_joints_info()
            self.selection_callback()
            self.exec_callback()

    def exec_callback(self):
        while self.keep_window_open:
            self.exec()

    def _configure_validators(self):

        general_validator = StrictDoubleValidator(1e-6, 1e8, 6)
        self.lineEdit_effective_diameter.setValidator(general_validator)
        self.lineEdit_ejoint_mass.setValidator(general_validator)

        offsets_validator = StrictDoubleValidator(-1e8, 1e8, 6)
        self.lineEdit_offset_y.setValidator(offsets_validator)
        self.lineEdit_offset_z.setValidator(offsets_validator)

        self.lineEdit_axial_locking_criteria.setValidator(StrictDoubleValidator(0, 10, 6))

        stiffness_validator = StrictDoubleValidator(0, 1e12, 6)
        self.lineEdit_Kx.setValidator(stiffness_validator)
        self.lineEdit_Krx.setValidator(stiffness_validator)
        self.lineEdit_Kyz.setValidator(stiffness_validator)
        self.lineEdit_Kryz.setValidator(stiffness_validator)

    def _initialize(self):
        self.stiffness_labels = ["Kx", "Kyz", "Krx", "Kryz"]

        self.lineEdit_expansion_joint_name.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_effective_diameter.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit_ejoint_mass.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.reset_table_variables()
        self.create_widgets_lists()

        self.complete = False
        self.keep_window_open = True

        self.expansion_joint_info = dict()

    def reset_table_variables(self):
        for label in self.stiffness_labels:
            setattr(self, f"imported_{label}_values", None)
            setattr(self, f"{label}_table_path", None)

    def create_widgets_lists(self):
        self.line_edits_table_path = [
            self.lineEdit_Kx_table_path,
            self.lineEdit_Kyz_table_path,
            self.lineEdit_Krx_table_path,
            self.lineEdit_Kryz_table_path,
        ]

    def _configure_appearance(self):

        if self.render_type == "model":
            self.selection_frame.setVisible(True)

        else:
            self.selection_frame.setVisible(False)
            self.tabWidget_main.setTabVisible(TabIndex.LIST, False)
            self.tabWidget_inputs.setTabVisible(DataType.TABULAR_VALUES, False)

        self.setMinimumHeight(520)

    def _config_widgets(self):
        #
        for i, width in enumerate([70, 120]):
            self.treeWidget_lines_info.setColumnWidth(i, width)
            self.treeWidget_lines_info.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.comboBox_axial_stop_rod.currentIndexChanged.connect(
            self.axial_stop_rod_callback
        )
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.connect_load_table_push_buttons(self.line_edits_table_path, self.stiffness_labels)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_lines_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_lines_info.itemDoubleClicked.connect(
            self.on_doubleclick_item
        )
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        selected_lines = app().main_window.list_selected_lines()
        if not selected_lines:
            return

        self.reset_input_fields()
        if self.comboBox_axial_stop_rod.currentIndex() == AxialStopRod.INCLUDED:
            self.lineEdit_axial_locking_criteria.setText("1.0")

        text = ", ".join([str(i) for i in selected_lines])
        self.lineEdit_selected_id.setText(text)

        if self.check_selection_type():
            return

        if len(selected_lines) != 1:
            return

        joint_data = self.properties._get_property("expansion_joint_info", line_id=selected_lines[0])
        if isinstance(joint_data, dict):
            self.load_input_fields(joint_data)

    def load_input_fields(self, joint_data: dict):

        self.lineEdit_expansion_joint_name.setText(joint_data.get("ejoint_name"))
        self.lineEdit_effective_diameter.setText(str(joint_data.get("effective_diameter")))
        self.lineEdit_ejoint_mass.setText(str(joint_data.get("ejoint_mass")))
        self.lineEdit_axial_locking_criteria.setText(str(joint_data.get("axial_locking_criteria", 1)))
        self.comboBox_axial_stop_rod.setCurrentIndex(int(joint_data.get("rods_included", False)))

        self.lineEdit_offset_y.clear()
        self.lineEdit_offset_z.clear()
        offset_y = joint_data.get("offset_y")
        offset_z = joint_data.get("offset_z")

        if isinstance(offset_y, float):
            self.lineEdit_offset_y.setText(f"{offset_y}")

        if isinstance(offset_z, float):
            self.lineEdit_offset_z.setText(f"{offset_z}")

        if "table_paths" in joint_data.keys():
            Kx_path, Kyz_path, Krx_path, Kryz_path = joint_data["table_paths"]
            self.tabWidget_inputs.setCurrentIndex(DataType.TABULAR_VALUES)
            self.lineEdit_Kx_table_path.setText(Kx_path)
            self.lineEdit_Kyz_table_path.setText(Kyz_path)
            self.lineEdit_Krx_table_path.setText(Krx_path)
            self.lineEdit_Kryz_table_path.setText(Kryz_path)
            return

        self.tabWidget_inputs.setCurrentIndex(DataType.CONSTANT_VALUES)
        Kx, Kyz, Krx, Kryz = joint_data['values']
        self.lineEdit_Kx.setText(f"{Kx : .6e}")
        self.lineEdit_Kyz.setText(f"{Kyz : .6e}")
        self.lineEdit_Krx.setText(f"{Krx : .6e}")
        self.lineEdit_Kryz.setText(f"{Kryz : .6e}")

    def axial_stop_rod_callback(self):

        axial_stop_rod = self.comboBox_axial_stop_rod.currentIndex() == AxialStopRod.INCLUDED
        self.label_axial_lock_criteria.setEnabled(axial_stop_rod)
        self.lineEdit_axial_locking_criteria.setEnabled(axial_stop_rod)

        if axial_stop_rod:
            if self.lineEdit_axial_locking_criteria.text() == "":
                self.lineEdit_axial_locking_criteria.setText("1.0")

        else:
            self.lineEdit_axial_locking_criteria.clear()

    def tab_event_callback(self):

        self.pushButton_remove.setDisabled(True)

        tab_list = self.tabWidget_main.currentIndex() == TabIndex.LIST
        self.selection_frame.setDisabled(tab_list)
        self.pushButton_attribute.setDisabled(tab_list)

        if not tab_list:
            self.treeWidget_lines_info.clearSelection()
            return

        self.lineEdit_selected_id.clear()

    def check_selection_type(self):

        lineEdit_selection = self.lineEdit_selected_id.text()
        stop, line_ids = self.before_run.check_selected_ids(lineEdit_selection, "lines")
        if stop:
            return True

        for line_id in line_ids:
            element_type = self.properties._get_property(
                "structural_element_type", line_id=line_id
            )
            if element_type in ["beam_1"]:
                stop = True
                self.lineEdit_selected_id.clear()
                self.lineEdit_selected_id.setFocus()
                return True

        return False

    def check_initial_inputs(self):

        self.expansion_joint_info.clear()

        joint_name = self.lineEdit_expansion_joint_name.text()
        if joint_name == "":
            self.lineEdit_expansion_joint_name.setFocus()
            return True

        self.expansion_joint_info["ejoint_name"] = joint_name
        axial_stop_rod = self.comboBox_axial_stop_rod.currentIndex() == AxialStopRod.INCLUDED

        if self.render_type == "model":
            if self.check_selection_type():
                return True

        line_edits = [
            self.lineEdit_effective_diameter,
            self.lineEdit_offset_y,
            self.lineEdit_offset_z,
            self.lineEdit_ejoint_mass,
        ]

        if axial_stop_rod:
            line_edits.append(self.lineEdit_axial_locking_criteria)

        for line_edit in line_edits:
            obj_name = line_edit.objectName()
            text_value = line_edit.text()
            if "offset" not in obj_name and text_value == "":
                line_edit.setFocus()
                return True
 
            var_name = obj_name.split("lineEdit_")[1]
            self.expansion_joint_info[var_name] = float(text_value) if text_value != "" else 0

        self.expansion_joint_info["rods_included"] = axial_stop_rod

    def check_constant_values_to_stiffness(self):

        constant_stiffness = list()

        line_edits = [
            self.lineEdit_Kx,
            self.lineEdit_Kyz,
            self.lineEdit_Krx,
            self.lineEdit_Kryz,
        ]

        for line_edit in line_edits:

            if line_edit.text() == "":
                line_edit.setFocus()
                return True

            constant_stiffness.append(float(line_edit.text()))

        self.expansion_joint_info["values"] = constant_stiffness

    def load_table_for_line_edit(self, line_edit, dof_label):
        if dof_label == "Kx":
            bc_label = "axial stiffness"
        elif dof_label == "Kyz":
            bc_label = "transversal stiffness"
        elif dof_label == "Krx":
            bc_label = "torsional stiffness"
        else:
            bc_label = "angular stiffness"

        return super().load_table_for_line_edit(line_edit, dof_label, bc_label)
   
    def save_table_values(self, table_name: str, imported_values: np.ndarray):

        # define the frequencies vector
        _frequencies = imported_values[:, 0]

        if app().project.model.change_analysis_frequency_setup(list(_frequencies)):
            self.hide()
            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup "
            message += "different from the others already imported. The current "
            message += "project frequency setup will not be modified."
            message += f"\n\n{table_name}"
            PrintMessageInput([error_title, title, message])
            return True

        self.update_analysis_setup_in_file(_frequencies)

        # real values vector
        real_values = imported_values[:, 1]
        
        # imaginary values vector
        imag_values = imported_values[:, 2]

        # array to be saved
        data = np.array([_frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("structural", table_name, data)

        return False

    def check_table_of_values(self, line_id: int):

        table_paths = list()
        imported_values = list()
        link_labels = ["Kx", "Kyz", "Krx", "Kryz"]

        for label in link_labels:

            table_path_name = f"{label}_table_path"
            imported_values_name = f"imported_{label}_values"
            _imported_values = getattr(self, imported_values_name)

            if _imported_values is None:
                line_edit = getattr(self, f"lineEdit_{label}_table_path")

                _imported_values, _table_path = self.load_table(line_edit, "nodal link", dof_label=label, direct_load=True)
                setattr(self, imported_values_name, _imported_values)
                setattr(self, table_path_name, _table_path)

            _table_path_attr = getattr(self, table_path_name)
            table_paths.append(str(_table_path_attr))
            imported_values.append(_imported_values)

        # check the minimum requisites before storing the tabular data
        if any(x is None for x in imported_values):
            title = "Insufficient inputs for the expansion joint"
            message = "The current setup have insufficient inputs "
            message += "for all required expansion joint stiffness.\n\n"
            message += "Required stiffness: "
            for i, value in enumerate(imported_values):
                if value is None:
                    message += f"{self.stiffness_labels[i]}, "

            self.hide()
            PrintMessageInput([error_title, title, message[:-2]])
            return True

        table_names = list()

        for label in link_labels:

            imported_values_name = f"imported_{label}_values"
            _imported_values = getattr(self, imported_values_name)

            _table_name = None
            if isinstance(_imported_values, np.ndarray):
                _table_name = self.get_table_name(f"expansion_joint_stiffness_{label}", line_id=line_id)
                if self.save_table_values(_table_name, _imported_values):
                    return

            table_names.append(_table_name)

        self.expansion_joint_info["table_names"] = table_names
        self.expansion_joint_info["table_paths"] = table_paths
        self.expansion_joint_info["values"] = self.properties.get_table_values("expansion_joint_info", table_names)

        return False

    def process_line_length(self, line_id: int):
        self.joint_elements = self.preprocessor.mesh.elements_from_line[line_id]
        joint_length = self.properties.get_line_length(line_id)
        return round(joint_length, 6)

    def attribute_callback(self):

        if self.render_type == "model":
            lineEdit = self.lineEdit_selected_id.text()
            stop, line_ids = self.before_run.check_selected_ids(lineEdit, "lines")
            if stop:
                return

        if self.check_initial_inputs():
            return

        if self.tabWidget_inputs.currentIndex() == DataType.CONSTANT_VALUES:
            if self.check_constant_values_to_stiffness():
                self.expansion_joint_info.clear()
                return

        if self.render_type == "model":
            for line_id in line_ids:

                if self.tabWidget_inputs.currentIndex() == DataType.TABULAR_VALUES:
                    if self.check_table_of_values(line_id):
                        self.expansion_joint_info.clear()
                        return

                self.expansion_joint_info["ejoint_length"] = self.process_line_length(
                    line_id
                )

                self.preprocessor.set_cross_section_by_lines(line_id, None)
                self.preprocessor.add_valve_by_lines(line_id, None)

                cross_sections = get_cross_sections_to_plot_expansion_joint(
                    self.joint_elements, 
                    self.expansion_joint_info["effective_diameter"],
                    self.expansion_joint_info["offset_y"],
                    self.expansion_joint_info["offset_z"],
                    )

                self.properties._remove_line_property("valve_info", line_id)
                self.properties._remove_line_property("section_parameters", line_id)
                self.properties._remove_line_property("section_properties", line_id)

                self.properties._set_line_property("structure_name", "expansion_joint", line_id)
                self.properties._set_line_property("section_type_label", "expansion_joint", line_id)
                self.properties._set_line_property("structural_element_type", "expansion_joint", line_id)
                self.properties._set_line_property("expansion_joint_info", self.expansion_joint_info, line_id)

                # get the updated property data to include, whenever applicable, the table values
                _expansion_joint_info = self.properties._get_property("expansion_joint_info", line_id=line_id)

                self.preprocessor.set_cross_section_by_elements(self.joint_elements, cross_sections)
                self.preprocessor.add_expansion_joint_by_lines(line_id, _expansion_joint_info)
                self.preprocessor.set_structural_element_type_by_lines(line_id, "expansion_joint")

            self.actions_to_finalize()

        self.complete = True
        self.close()

    def load_expansion_joints_info(self):
        self.treeWidget_lines_info.clear()
        for line_id, data in self.properties.line_properties.items():
            if "expansion_joint_info" in data.keys():
                ej_info = data["expansion_joint_info"]
                L = round(ej_info["ejoint_length"], 6)
                d_eff = ej_info["effective_diameter"]
                mass = ej_info["ejoint_mass"]
                rods_included = ej_info["rods_included"]

                if "table_names" in ej_info.keys():
                    pass
                else:
                    pass

                str_joint_info = f"{L}, {d_eff}, {mass}, {rods_included}, "
                if "table_names" in ej_info.keys():
                    str_joint_info += "Table, Table, Table, Table"
                else:
                    values = ej_info["values"]
                    str_joint_info += f"{values[0] : .2e}, {values[1] : .2e}, {values[2] : .2e}, {values[3] : .2e}"

                item = QTreeWidgetItem([str(line_id), str_joint_info[:-2]])
                item.setTextAlignment(0, Qt.AlignCenter)
                item.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_lines_info.addTopLevelItem(item)

        self.update_tab_visibility()

    def update_tab_visibility(self):

        self.tabWidget_main.setTabVisible(TabIndex.LIST, False)
        for data in self.properties.line_properties.values():
            if "expansion_joint_info" in data.keys():
                self.tabWidget_main.setTabVisible(TabIndex.LIST, True)
                return

        self.lineEdit_expansion_joint_name.setFocus()

    def on_click_item(self, item: QTreeWidgetItem):
        self.lineEdit_selected_id.setText(item.text(0))
        self.pushButton_remove.setEnabled(True)
        if item.text(0) != "":
            line_id = int(item.text(0))
            data = self.properties._get_property(
                "expansion_joint_info", line_id=line_id
            )
            if isinstance(data, dict):
                app().main_window.set_selection(lines=[line_id])

    def on_doubleclick_item(self, item: QTreeWidgetItem):
        self.on_click_item(item)

    def restore_the_cross_section(self, line_ids: list):

        line_to_elements = app().project.model.mesh.elements_from_line
        for line_id in line_ids:
            line_elements = line_to_elements[line_id]
            first_element_id_from_line = line_to_elements[line_id][0]
            last_element_id_from_line = line_to_elements[line_id][-1]

            element_ids = [
                first_element_id_from_line - 1, 
                first_element_id_from_line + 1, 
                last_element_id_from_line - 1,  
                last_element_id_from_line + 1
                ]

            cross_section = None
            structural_element_type = None

            for element_id in element_ids:
                if element_id in line_elements:
                    continue

                structural_element_type = self.preprocessor.get_element_cross_section(element_id)
                cross_section = self.preprocessor.get_element_cross_section(element_id)
                break

            if structural_element_type == "pipe_1" and isinstance(cross_section, CrossSection):
                self.preprocessor.set_cross_section_by_lines(line_id, cross_section)
                self.preprocessor.set_structural_element_type_by_lines(line_id, "pipe_1")

                pipe_info = {
                    "structure_name": "pipe",
                    "section_type_label": "pipe",
                    "section_parameters": cross_section.section_parameters,
                }

                self.properties._set_line_property("structural_element_type", structural_element_type, line_id)
                self.properties._set_multiple_line_properties(pipe_info, line_id)

    def remove_expansion_joint_properties(self, line_ids: int | list[int]):
        self.properties._remove_line_property("structure_name", line_ids)
        self.properties._remove_line_property("expansion_joint_info", line_ids)
        self.properties._remove_line_property("section_type_label", line_ids)
        self.properties._remove_line_property("structural_element_type", line_ids)

    def remove_callback(self):
        selected_items = self.treeWidget_lines_info.selectedItems()

        if not selected_items:
            return
    
        for selected_item in selected_items:
            line_id = int(selected_item.data(0, 0))

            self.reset_input_fields()
            self.remove_expansion_joint_properties(line_id)

            self.restore_the_cross_section([line_id])
            self.preprocessor.add_expansion_joint_by_lines(line_id, None)

            self.actions_to_finalize()
            self.load_expansion_joints_info()

    def reset_callback(self):

        self.hide()

        title = "Expansion joints resetting"
        message = "Would you like to remove all expansion joints from the model?"

        buttons_config = {
            "left_button_label": "Cancel",
            "right_button_label": "Continue",
        }
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        line_ids = list()
        for line_id, data in self.properties.line_properties.items():
            if "expansion_joint_info" in data.keys():
                line_ids.append(line_id)

        self.remove_expansion_joint_properties(line_ids)
    
        self.preprocessor.add_expansion_joint_by_lines(line_ids, None)
        self.restore_the_cross_section(line_ids)

        self.actions_to_finalize()
        self.load_expansion_joints_info()
        self.close()

    def actions_to_finalize(self):

        self.reset_table_variables()
        app().project.file.write_line_properties_in_file()
        app().project.file.write_imported_table_data_in_file()

        geometry_handler = GeometryHandler(app().project)
        geometry_handler.set_length_unit(app().project.model.mesh.length_unit)
        geometry_handler.process_pipeline()

        app().main_window.update_plots()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()

        elif event.key() == Qt.Key_Delete:
            if self.render_type == "model":
                self.remove_callback()

        elif event.key() == Qt.Key_Escape:
            self.close()
    
def get_cross_sections_to_plot_expansion_joint(
    joint_elements: list, effective_diameter: float, offset_y: float, offset_z: float
):
    """ "
    This auxiliary function returns a list of cross-sections
    from the expansion joint.
    """

    cross_sections = list()
    flanges_elements = [    
        joint_elements[0],
        joint_elements[1],
        joint_elements[-2],
        joint_elements[-1],
        ]

    for element in joint_elements:
        if element in flanges_elements:
            plot_key = "flanges"
        else:
            if np.remainder(element, 2) == 0:
                plot_key = "minor"
            else:
                plot_key = "major"

        expansion_joint_info = ExpansionJointCrossSection(
            effective_diameter, 
            offset_y, 
            offset_z, 
            plot_key,
        )

        cross = CrossSection(expansion_joint_info=expansion_joint_info)
        cross_sections.append(cross)

    return cross_sections
