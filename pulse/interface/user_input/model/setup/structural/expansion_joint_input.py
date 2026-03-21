from PySide6.QtWidgets import QLineEdit, QTreeWidgetItem
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt

from pulse import app
from pulse.interface.ui_generated.model.setup.structural.expansion_joint_input_ui import ExpansionJointInput_UI
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.interface.user_input.common import CommonUserInputs, get_table_name, update_analysis_setup_in_file
from pulse.model.cross_section import CrossSection

import numpy as np
from enum import IntEnum

error_title = "Error"
stiffess_labels = ["Kx", "Kyz", "Krx", "Kryz"]


class DataType(IntEnum):
    CONSTANT_VALUES = 0
    TABULAR_VALUES = 1


class ExpansionJointInput(ExpansionJointInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.render_type = kwargs.get("render_type", "model")

        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties
        self.preprocessor = app().project.model.preprocessor

        self.before_run = app().project.get_pre_solution_model_checks()

        self._config_window()
        self._initialize()
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

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")
    
    def _initialize(self):

        self.reset_table_variables()
        self.create_widgets_lists()

        self.complete = False
        self.keep_window_open = True

        self.expansion_joint_info = dict()

    def reset_table_variables(self):

        self.imported_Kx_values = None
        self.imported_Kyz_values = None
        self.imported_Krx_values = None
        self.imported_Kryz_values = None

        self.Kx_table_path = None
        self.Kyz_table_path = None
        self.Krx_table_path = None
        self.Kryz_table_path = None

    def create_widgets_lists(self):

        self.list_line_edits = [
            self.lineEdit_expansion_joint_name,
            self.lineEdit_effective_diameter,
            self.lineEdit_joint_mass,
            self.lineEdit_axial_locking_criteria,
            self.lineEdit_Kx,
            self.lineEdit_Kyz,
            self.lineEdit_Krx,
            self.lineEdit_Kryz,
            self.lineEdit_Kx_table_path,
            self.lineEdit_Kyz_table_path,
            self.lineEdit_Krx_table_path,
            self.lineEdit_Kryz_table_path,
            ]

    def _create_connections(self):
        #
        self.comboBox_axial_stop_rod.currentIndexChanged.connect(self.axial_stop_rod_callback)
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.pushButton_load_table_Kx.clicked.connect(self.load_Kx_table)
        self.pushButton_load_table_Kyz.clicked.connect(self.load_Kyz_table)
        self.pushButton_load_table_Krx.clicked.connect(self.load_Krx_table)
        self.pushButton_load_table_Kryz.clicked.connect(self.load_Kryz_table)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_expansion_joints_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_expansion_joints_info.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        try:

            selected_lines = app().main_window.list_selected_lines()

            if selected_lines:

                text = ", ".join([str(i) for i in selected_lines])
                self.lineEdit_selected_id.setText(text)

                if self.check_selection_type():
                    return

                if len(selected_lines) == 1:            
                    self.load_input_fields(selected_lines[0])                

        except Exception as log_error:
            title = "Error in 'update' function"
            message = str(log_error) 
            PrintMessageInput([error_title, title, message])

    def _configure_appearance(self):

        if self.render_type == "model":
            self.selection_frame.setVisible(True)

        else:
            self.selection_frame.setVisible(False)
            self.tabWidget_main.setTabVisible(1, False)
            self.tabWidget_inputs.setTabVisible(1, False)

        self.setMinimumHeight(520)

    def _config_widgets(self):
        #
        for i, width in enumerate([70, 120]):
            self.treeWidget_expansion_joints_info.setColumnWidth(i, width)
            self.treeWidget_expansion_joints_info.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def axial_stop_rod_callback(self):
        if self.comboBox_axial_stop_rod.currentIndex() == 0:
            self.label_axial_lock_criteria.setDisabled(True)
            self.lineEdit_axial_locking_criteria.setText("")
            self.lineEdit_axial_locking_criteria.setDisabled(True)
        else:
            self.label_axial_lock_criteria.setDisabled(False)
            self.lineEdit_axial_locking_criteria.setDisabled(False)

    def tab_event_callback(self):
        self.pushButton_remove.setDisabled(True)
        tab_remove = self.tabWidget_main.currentIndex() == 1
        self.selection_frame.setDisabled(tab_remove)

    def check_selection_type(self):

        lineEdit_selection = self.lineEdit_selected_id.text()
        stop, line_ids = self.before_run.check_selected_ids(lineEdit_selection, "lines")
        if stop:
            return True

        for line_id in line_ids:
            element_type = self.properties._get_property("structural_element_type", line_id=line_id)
            if element_type in ["beam_1"]:
                stop = True
                self.lineEdit_selected_id.setText("")
                self.lineEdit_selected_id.setFocus()
                return True

        return False

    def reset_all_line_edits(self):
        for lineEdit in self.list_line_edits:
            lineEdit.setText("")

    def load_input_fields(self, line_id: int):

        joint_data = self.properties._get_property("expansion_joint_info", line_id=line_id)
        if joint_data is None:
            return

        try:

            self.reset_all_line_edits()
            self.lineEdit_effective_diameter.setText(str(joint_data["effective_diameter"]))
            self.lineEdit_joint_mass.setText(str(joint_data["joint_mass"]))
            self.lineEdit_axial_locking_criteria.setText(str(joint_data["axial_locking_criteria"]))
            self.comboBox_axial_stop_rod.setCurrentIndex(int(joint_data["rods"]))

            if "table_paths" in joint_data.keys():
                self.tabWidget_inputs.setCurrentIndex(1)
                self.lineEdit_Kx_table_path.setText(joint_data["table_paths"][0])
                self.lineEdit_Kyz_table_path.setText(joint_data["table_paths"][1])
                self.lineEdit_Krx_table_path.setText(joint_data["table_paths"][2])
                self.lineEdit_Kryz_table_path.setText(joint_data["table_paths"][3])

            else:
                self.tabWidget_inputs.setCurrentIndex(0)
                Kx, Kyz, Krx, Kryz = joint_data['values']
                self.lineEdit_Kx.setText(f"{Kx : .3e}")
                self.lineEdit_Kyz.setText(f"{Kyz : .3e}")
                self.lineEdit_Krx.setText(f"{Krx : .3e}")
                self.lineEdit_Kryz.setText(f"{Kryz : .3e}")

        except Exception as error_log:
            title = "Error while loading info from entity"
            message = str(error_log)
            PrintMessageInput([error_title, title, message])

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
            PrintMessageInput([error_title, title, message])
            return True, None
        else:
            return False, value

    def check_initial_inputs(self):

        self.expansion_joint_info.clear()

        if self.lineEdit_expansion_joint_name.text() == "":
            self.lineEdit_expansion_joint_name.setFocus()
            return True

        self.expansion_joint_info["expansion_joint_name"] = self.lineEdit_expansion_joint_name.text()

        if self.render_type == "model":
            if self.check_selection_type():
                return True

        stop, value = self.check_input_parameters(self.lineEdit_effective_diameter, 'Effective diameter')
        if stop:
            self.lineEdit_effective_diameter.setFocus()
            return True
        self.expansion_joint_info["effective_diameter"] = value

        stop, value = self.check_input_parameters(self.lineEdit_joint_mass, 'Joint mass')
        if stop:    
            self.lineEdit_joint_mass.setFocus()
            return True
        self.expansion_joint_info["joint_mass"] = value

        stop, value = self.check_input_parameters(self.lineEdit_axial_locking_criteria, 'Axial locking criteria')
        if stop:
            self.lineEdit_axial_locking_criteria.setFocus()
            return True
        self.expansion_joint_info["axial_locking_criteria"] = value

        self.expansion_joint_info["rods"] = int(self.comboBox_axial_stop_rod.currentIndex())

    def check_constant_values_to_stiffness(self):
        
        _stiffness = list()

        stop, value = self.check_input_parameters(self.lineEdit_Kx, 'Kx (axial stiffness)')
        if stop:
            self.lineEdit_Kx.setFocus()
            return True
        _stiffness.append(value)

        stop, value = self.check_input_parameters(self.lineEdit_Kyz, 'Kyz (transversal stiffness)')
        if stop:
            self.lineEdit_Kyz.setFocus()
            return True
        _stiffness.append(value)

        stop, value = self.check_input_parameters(self.lineEdit_Krx, 'Krx (torsional stiffness)')
        if stop:
            self.lineEdit_Krx.setFocus()
            return True
        _stiffness.append(value)

        stop, value = self.check_input_parameters(self.lineEdit_Kryz, 'Kryz (angular stiffness)')
        if stop:
            self.lineEdit_Kryz.setFocus()
            return True
        _stiffness.append(value)

        self.expansion_joint_info["values"] = _stiffness

    def load_Kx_table(self):
        self.imported_Kx_values, self.Kx_table_path = CommonUserInputs(self).load_table(
            self.lineEdit_Kx_table_path, 
            "Kx", 
            dof_label="axial stiffness",
            )

        if self.imported_Kx_values is None:
            self.line_edit_reset(self.lineEdit_Kx_table_path)

    def load_Kyz_table(self):
        self.imported_Kyz_values, self.Kyz_table_path = CommonUserInputs(self).load_table(
            self.lineEdit_Kyz_table_path, 
            "Kyz", 
            dof_label="transversal stiffness",
            )

        if self.imported_Kyz_values is None:
            self.line_edit_reset(self.lineEdit_Kyz_table_path)

    def load_Krx_table(self):
        self.imported_Krx_values, self.Krx_table_path = CommonUserInputs(self).load_table(
            self.lineEdit_Krx_table_path, 
            "Krx", 
            dof_label="torsional stiffness",
            )

        if self.imported_Krx_values is None:
            self.line_edit_reset(self.lineEdit_Krx_table_path)

    def load_Kryz_table(self):
        self.imported_Kryz_values, self.Kryz_table_path = CommonUserInputs(self).load_table(
            self.lineEdit_Kryz_table_path, 
            "Kryz", 
            dof_label="angular stiffness"
            )

        if self.Kryz_table_path is None:
            self.line_edit_reset(self.lineEdit_Kryz_table_path)

    def line_edit_reset(self, line_edit: QLineEdit):
        line_edit.setText("")
        line_edit.setFocus()
   
    def save_table_values(self, table_name: str, imported_values: np.ndarray):

        # define the frequencies vector
        _frequencies = imported_values[:, 0]

        if app().project.model.change_analysis_frequency_setup(list(_frequencies)):
            self.hide()
            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup "
            message += "different from the others already imported ones. The current "
            message += "project frequency setup is not going to be modified."
            message += f"\n\n{table_name}"
            PrintMessageInput([error_title, title, message])
            return True

        update_analysis_setup_in_file(_frequencies)

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

                _imported_values, _table_path = CommonUserInputs(self).load_table(line_edit, "nodal link", dof_label=label, direct_load=True)
                setattr(self, imported_values_name, _imported_values)
                setattr(self, table_path_name, _table_path)

            _table_path_attr = getattr(self, table_path_name)
            table_paths.append(_table_path_attr)
            imported_values.append(_imported_values)

        # check the minimum requisites before storing the tabular data
        if any(x is None for x in imported_values):
            title = "Insufficient inputs for the expansion joint"
            message = "The current setup have insufficient inputs "
            message += "for all required expansion joint stiffness.\n\n"
            message += "Required stiffness: "
            for i, value in enumerate(imported_values):
                if value is None:
                    message += f"{stiffess_labels[i]}, "

            self.hide()
            PrintMessageInput([error_title, title, message[:-2]])
            return True

        table_names = list()

        for label in link_labels:

            imported_values_name = f"imported_{label}_values"
            _imported_values = getattr(self, imported_values_name)

            _table_name = None
            if isinstance(_imported_values, np.ndarray):
                _table_name = get_table_name(f"expansion_joint_stiffness_{label}", line_id=line_id)
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

                self.expansion_joint_info["joint_length"] = self.process_line_length(line_id)

                self.preprocessor.set_cross_section_by_lines(line_id, None)
                self.preprocessor.add_valve_by_lines(line_id, None)

                cross_sections = get_cross_sections_to_plot_expansion_joint(
                    self.joint_elements, 
                    self.expansion_joint_info["effective_diameter"],
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
        self.treeWidget_expansion_joints_info.clear()
        for line_id, data in self.properties.line_properties.items():
            if "expansion_joint_info" in data.keys():

                ej_info = data["expansion_joint_info"]
                L = round(ej_info["joint_length"], 6)
                d_eff = ej_info["effective_diameter"]
                mass = ej_info["joint_mass"]
                rods = ej_info["rods"]

                if "table_names" in ej_info.keys():
                    pass
                else:
                    pass

                str_joint_info = f"{L}, {d_eff}, {mass}, {rods}, "
                if "table_names" in ej_info.keys():
                    str_joint_info += "Table, Table, Table, Table"
                else:
                    values = ej_info["values"]
                    str_joint_info += f"{values[0] : .2e}, {values[1] : .2e}, {values[2] : .2e}, {values[3] : .2e}"

                item = QTreeWidgetItem([str(line_id), str_joint_info[:-2]])
                item.setTextAlignment(0, Qt.AlignCenter)
                item.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_expansion_joints_info.addTopLevelItem(item)

        self.update_tab_visibility()

    def update_tab_visibility(self):
        self.tabWidget_main.setTabVisible(1, False)
        for data in self.properties.line_properties.values():
            if "expansion_joint_info" in data.keys():
                self.tabWidget_main.setTabVisible(1, True)
                return

    def on_click_item(self, item):
        self.lineEdit_selected_id.setText(item.text(0))
        self.pushButton_remove.setEnabled(True)
        if item.text(0) != "":
            line_id = int(item.text(0))
            data = self.properties._get_property("expansion_joint_info", line_id=line_id)
            if isinstance(data, dict):
                app().main_window.set_selection(lines = [line_id])

    def on_doubleclick_item(self, item):
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

            cross = None
            element_type = None

            for element_id in element_ids:
                if element_id not in line_elements:

                    element = self.preprocessor.structural_elements[element_id]
                    cross = element.cross_section
                    element_type = element.element_type
                    break

            if element_type == 'pipe_1' and isinstance(cross, CrossSection):

                self.preprocessor.set_cross_section_by_lines(line_id, cross)
                self.preprocessor.set_structural_element_type_by_lines(line_id, "pipe_1")

                pipe_info = {   "section_type_label" : "pipe",
                                "section_parameters" : cross.section_parameters   }

                self.properties._set_line_property("structural_element_type", element_type, line_id)
                self.properties._set_multiple_line_properties(pipe_info, line_id)

    def remove_callback(self):

        if self.lineEdit_selected_id.text() != "":

            line_id = int(self.lineEdit_selected_id.text())
            self.reset_all_line_edits()

            self.properties._remove_line_property("expansion_joint_info", line_id)

            self.restore_the_cross_section([line_id])
            self.preprocessor.add_expansion_joint_by_lines(line_id, None)

            self.actions_to_finalize()
            self.load_expansion_joints_info()

    def reset_callback(self):

        self.hide()

        title = "Resetting of expansion joints"
        message = "Would you like to remove all expansion joints from the model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return
        
        line_ids = list()
        for line_id, data in self.properties.line_properties.items():
            if "expansion_joint_info" in data.keys():
                line_ids.append(line_id)

        self.properties._remove_line_property("expansion_joint_info", line_ids)
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

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        app().main_window.selection_changed.disconnect(self.selection_callback)
        return super().closeEvent(a0)
    

    # def get_pipe_cross_section_from_neighbors(self, line_id, list_elements):

    #     line_elements = self.preprocessor.elements_from_line[line_id]
    #     lower_id = list_elements[0] - 1
    #     upper_id = list_elements[-1] + 1

    #     cross = None
    #     structural_element_type = None

    #     try:
    #         if lower_id in line_elements:
    #             element = self.preprocessor.structural_elements[lower_id]
    #             cross = element.cross_section
    #             structural_element_type = element.element_type

    #         elif upper_id in line_elements:
    #             element = self.preprocessor.structural_elements[upper_id]
    #             cross = element.cross_section
    #             structural_element_type = element.element_type
    #     except:
    #         pass

    #     return cross, structural_element_type


def get_cross_sections_to_plot_expansion_joint(joint_elements: list, effective_diameter: float):

    """"
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

        expansion_joint_info = [
                                "expansion_joint", 
                                plot_key,
                                effective_diameter 
                                ]

        cross = CrossSection(expansion_joint_info = expansion_joint_info)
        cross_sections.append(cross)

    return cross_sections