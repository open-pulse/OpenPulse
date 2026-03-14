from functools import partial

from PySide6.QtWidgets import QTreeWidgetItem, QPushButton, QLineEdit
from PySide6.QtCore import Qt

from pulse import app
from pulse.interface.ui_generated.model.setup.structural.mass_spring_damper_input_ui import MassSpringDamperInput_UI
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.interface.user_input.model.setup.structural.structural_nodes_input import StructuralNodesInput

import numpy as np


error_title ="Error"
warning_title = "Warning"


class MassSpringDamperInput(StructuralNodesInput, MassSpringDamperInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config_window()
        self._config_widgets()
        self._initialize()
        self._create_connections()

        self.load_nodes_info()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.lumped_masses_labels = ["Mx", "My", "Mz", "Jx", "Jy", "Jz"]
        self.lumped_stiffness_labels = ["Kx", "Ky", "Kz", "Krx", "Kry", "Krz"]
        self.lumped_dampings_labels = ["Cx", "Cy", "Cz", "Crx", "Cry", "Crz"]

        self.reset_table_variables()
        self.create_widgets_lists()

        self.keep_window_open = True
        self.lumped_element_applied = False

    def create_widgets_lists(self):
        self.constant_values_lumped_masses = [getattr(self, f"lineEdit_{label}") for label in self.lumped_masses_labels]
        self.table_values_lumped_masses = [getattr(self, f"lineEdit_{label}_table_path") for label in self.lumped_masses_labels]

        self.constant_values_lumped_stiffness = [getattr(self, f"lineEdit_{label}") for label in self.lumped_stiffness_labels]
        self.table_values_lumped_stiffness = [getattr(self, f"lineEdit_{label}_table_path") for label in self.lumped_stiffness_labels]

        self.constant_values_lumped_dampings = [getattr(self, f"lineEdit_{label}") for label in self.lumped_dampings_labels]
        self.table_values_lumped_dampings = [getattr(self, f"lineEdit_{label}_table_path") for label in self.lumped_dampings_labels]

    def reset_table_variables(self):
        for label in self.lumped_masses_labels:
            setattr(self, f"imported_{label}_values", None)
            setattr(self, f"{label}_table_path", None)

        for label in self.lumped_stiffness_labels:
            setattr(self, f"imported_{label}_values", None)
            setattr(self, f"{label}_table_path", None)

        for label in self.lumped_dampings_labels:
            setattr(self, f"imported_{label}_values", None)
            setattr(self, f"{label}_table_path", None)

    def _create_connections(self):
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)

        self.connect_load_table_push_buttons(self.table_values_lumped_masses, self.lumped_masses_labels)
        self.connect_load_table_push_buttons(self.table_values_lumped_stiffness, self.lumped_stiffness_labels)
        self.connect_load_table_push_buttons(self.table_values_lumped_dampings, self.lumped_dampings_labels)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_masses.itemClicked.connect(self.on_click_item_masses)
        self.treeWidget_masses.itemDoubleClicked.connect(
            self.on_doubleclick_item_masses
        )
        #
        self.treeWidget_springs.itemClicked.connect(self.on_click_item_springs)
        self.treeWidget_springs.itemDoubleClicked.connect(
            self.on_doubleclick_item_springs
        )
        #
        self.treeWidget_dampers.itemClicked.connect(self.on_click_item_dampings)
        self.treeWidget_dampers.itemDoubleClicked.connect(
            self.on_doubleclick_item_dampings
        )
        #
        app().main_window.selection_changed.connect(self.selection_callback)
        self.selection_callback()
    
    def connect_load_table_push_buttons(self, line_edits: list[QLineEdit], labels: list[str]):
        for line_edit, label in zip(line_edits, labels):
            push_button: QPushButton = getattr(self, f"pushButton_load_{label}_table")

            push_button.clicked.connect(partial(self.load_table_for_line_edit, line_edit=line_edit, dof_label=label))

    def selection_callback(self):

        selected_nodes = app().main_window.list_selected_nodes()
        if selected_nodes:
            text = ", ".join([str(i) for i in selected_nodes])
            self.lineEdit_node_ids.setText(text)

            self.reset_input_fields_masses()
            self.reset_input_fields_stiffness()
            self.reset_input_fields_dampings()

            if len(selected_nodes) == 1:
                node_id = selected_nodes[0]
                lm_data = self.properties._get_property(
                    "lumped_masses", node_ids=node_id
                )
                if isinstance(lm_data, dict):
                    # Lumped masses/inertias
                    if "table_names" in lm_data.keys():
                        self.tabWidget_inputs.setCurrentIndex(1)
                        self.tabWidget_table_values.setCurrentIndex(0)
                        for i, table_path in enumerate(lm_data["table_paths"]):
                            if table_path is not None:
                                lineEdit = self.table_values_lumped_masses[i]
                                lineEdit.setText(table_path)

                        else:
                            self.tabWidget_inputs.setCurrentIndex(0)
                            self.tabWidget_constant_values.setCurrentIndex(1)
                            for i, value in enumerate(lm_data["values"]):
                                if value is not None:
                                    lineEdit = self.constant_values_lumped_masses[i]
                                    lineEdit.setText(f"{value: .3e}")

                ls_data = self.properties._get_property(
                    "lumped_stiffness", node_ids=node_id
                )
                if isinstance(ls_data, dict):
                    # Lumped stiffness
                    if "table_names" in ls_data.keys():
                        self.tabWidget_inputs.setCurrentIndex(1)
                        self.tabWidget_table_values.setCurrentIndex(0)
                        for i, table_path in enumerate(ls_data["table_paths"]):
                            if table_path is not None:
                                lineEdit = self.table_values_lumped_stiffness[i]
                                lineEdit.setText(table_path)

                    else:

                        self.tabWidget_inputs.setCurrentIndex(0)
                        self.tabWidget_constant_values.setCurrentIndex(1)
                        for i, value in enumerate(ls_data["values"]):
                            if value is not None:
                                lineEdit = self.constant_values_lumped_stiffness[i]
                                lineEdit.setText(f"{value : .3e}")

                ld_data = self.properties._get_property(
                    "lumped_dampings", node_ids=node_id
                )
                if isinstance(ld_data, dict):
                    # Lumped dampings
                    if "table_names" in ld_data.keys():
                        self.tabWidget_inputs.setCurrentIndex(1)
                        self.tabWidget_table_values.setCurrentIndex(0)
                        for i, table_path in enumerate(ld_data["table_paths"]):
                            if table_path is not None:
                                lineEdit = self.table_values_lumped_dampings[i]
                                lineEdit.setText(table_path)

                    else:

                        self.tabWidget_inputs.setCurrentIndex(0)
                        self.tabWidget_constant_values.setCurrentIndex(1)
                        for i, value in enumerate(ld_data["values"]):
                            if value is not None:
                                lineEdit = self.constant_values_lumped_dampings[i]
                                lineEdit.setText(f"{value : .3e}")

    def _config_widgets(self):
        #
        self.cache_tab = self.tabWidget_main.currentIndex()
        #
        for i, width in enumerate([100, 150]):
            self.treeWidget_masses.setColumnWidth(i, width)
            self.treeWidget_springs.setColumnWidth(i, width)
            self.treeWidget_dampers.setColumnWidth(i, width)
            self.treeWidget_masses.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_springs.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_dampers.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def attribute_callback(self):

        str_nodes = self.lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            return True

        self.remove_properties_from_node(node_ids, properties = ["lumped_masses", "lumped_stiffness", "lumped_dampings"])

        if self.tabWidget_inputs.currentIndex() == 0:
            self.check_constant_values_inputs(node_ids)

        elif self.tabWidget_inputs.currentIndex() == 1:
            self.check_table_values_inputs(node_ids)

        self.actions_to_finalize()

    def check_constant_values_lumped_masses(self, node_ids: list):

        stop, Mx = self.check_entries(self.lineEdit_Mx, "Mx")
        if stop:
            return True

        stop, My = self.check_entries(self.lineEdit_My, "My")
        if stop:
            return True

        stop, Mz = self.check_entries(self.lineEdit_Mz, "Mz")
        if stop:
            return True

        stop, Jx = self.check_entries(self.lineEdit_Jx, "Jx")
        if stop:
            return True

        stop, Jy = self.check_entries(self.lineEdit_Jy, "Jy")
        if stop:
            return True

        stop, Jz = self.check_entries(self.lineEdit_Jz, "Jz")
        if stop:
            return True

        values = [Mx, My, Mz, Jx, Jy, Jz]

        if values.count(None) != 6:
            self.lumped_element_applied = True

            real_values = [
                value if value is None else np.real(value) for value in values
            ]
            imag_values = [
                value if value is None else np.imag(value) for value in values
            ]

            for node_id in node_ids:
                node = app().project.model.preprocessor.nodes[node_id]
                coords = np.round(node.coordinates, 5)

                data = {
                    "coords": list(coords),
                    "values": values,
                    "real_values": real_values,
                    "imag_values": imag_values,
                }

                self.properties._set_nodal_property("lumped_masses", data, node_id)

    def check_constant_values_lumped_stiffness(self, node_ids: list):

        stop, Kx = self.check_entries(self.lineEdit_Kx, "Kx")
        if stop:
            return True

        stop, Ky = self.check_entries(self.lineEdit_Ky, "Ky")
        if stop:
            return True

        stop, Kz = self.check_entries(self.lineEdit_Kz, "Kz")
        if stop:
            return True

        stop, Krx = self.check_entries(self.lineEdit_Krx, "Krx")
        if stop:
            return True

        stop, Kry = self.check_entries(self.lineEdit_Kry, "Kry")
        if stop:
            return True

        stop, Krz = self.check_entries(self.lineEdit_Krz, "Krz")
        if stop:
            return True

        values = [Kx, Ky, Kz, Krx, Kry, Krz]

        if values.count(None) != 6:
            self.lumped_element_applied = True

            real_values = [
                value if value is None else np.real(value) for value in values
            ]
            imag_values = [
                value if value is None else np.imag(value) for value in values
            ]

            for node_id in node_ids:
                node = app().project.model.preprocessor.nodes[node_id]
                coords = np.round(node.coordinates, 5)

                data = {
                    "coords": list(coords),
                    "values": values,
                    "real_values": real_values,
                    "imag_values": imag_values,
                }

                self.properties._set_nodal_property("lumped_stiffness", data, node_id)

    def check_constant_values_lumped_dampings(self, node_ids: list):

        stop, Cx = self.check_entries(self.lineEdit_Cx, "Cx")
        if stop:
            return True

        stop, Cy = self.check_entries(self.lineEdit_Cy, "Cy")
        if stop:
            return True

        stop, Cz = self.check_entries(self.lineEdit_Cz, "Cz")
        if stop:
            return True

        stop, Crx = self.check_entries(self.lineEdit_Crx, "Crx")
        if stop:
            return True

        stop, Cry = self.check_entries(self.lineEdit_Cry, "Cry")
        if stop:
            return True

        stop, Crz = self.check_entries(self.lineEdit_Crz, "Crz")
        if stop:
            return True

        values = [Cx, Cy, Cz, Crx, Cry, Crz]

        if values.count(None) != 6:
            self.lumped_element_applied = True

            real_values = [
                value if value is None else np.real(value) for value in values
            ]
            imag_values = [
                value if value is None else np.imag(value) for value in values
            ]

            for node_id in node_ids:
                node = app().project.model.preprocessor.nodes[node_id]
                coords = np.round(node.coordinates, 5)

                data = {
                    "coords": list(coords),
                    "values": values,
                    "real_values": real_values,
                    "imag_values": imag_values,
                }

                self.properties._set_nodal_property("lumped_dampings", data, node_id)

    def check_constant_values_inputs(self, node_ids: list):

        if self.check_constant_values_lumped_masses(node_ids):
            return

        if self.check_constant_values_lumped_stiffness(node_ids):
            return

        if self.check_constant_values_lumped_dampings(node_ids):
            return

        if not self.lumped_element_applied:
            title = "Additional inputs required"
            message = "You must inform at least one external element\n"
            message += "before confirming the input!"
            PrintMessageInput([error_title, title, message])
            return

        self.actions_to_finalize()
    
    def load_table_for_line_edit(self, line_edit, dof_label):
        return super().load_table_for_line_edit(line_edit, dof_label, "lumped element")

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

        self.update_analysis_setup_in_file(_frequencies)

        # real values vector
        real_values = imported_values[:, 1]
        
        # imaginary values vector
        imag_values = imported_values[:, 2]

        # array to be saved
        data = np.array([_frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("structural", table_name, data)

        return False

    def check_table_values_for_lumped_masses(self, node_ids: list):

        table_paths = list()
        
        for label in self.lumped_masses_labels:

            table_path_name = f"{label}_table_path"
            imported_values_name = f"imported_{label}_values"
            _imported_values = getattr(self, imported_values_name)

            if _imported_values is None:
                line_edit = getattr(self, f"lineEdit_{label}_table_path")

                _imported_values, _table_path = self.load_table(line_edit, "lumped element", dof_label=label, direct_load=True)
                setattr(self, imported_values_name, _imported_values)
                setattr(self, table_path_name, _table_path)

            _table_path_attr = getattr(self, table_path_name)
            table_paths.append(str(_table_path_attr))

        for node_id in node_ids:

            table_names = list()

            for label in self.lumped_masses_labels:
                imported_values_name = f"imported_{label}_values"
                _imported_values = getattr(self, imported_values_name)

                _table_name = None
                if isinstance(_imported_values, np.ndarray):
                    _table_name = self.get_table_name(f"lumped_{label}", node_id=node_id)
                    if self.save_table_values(_table_name, _imported_values):
                        return

                table_names.append(_table_name)

            if (table_names).count(None) != 6:

                self.lumped_element_applied = True

                node = app().project.model.preprocessor.nodes[node_id]
                coords = np.round(node.coordinates, 5)

                _data = {
                    "coords" : list(coords),
                    "table_names" : table_names,
                    "table_paths" : table_paths,
                    }

                self.properties._set_nodal_property("lumped_masses", _data, node_id)

    def check_table_values_for_lumped_stiffness(self, node_ids: list):

        table_paths = list()
        lumped_labels = self.lumped_stiffness_labels
        
        for label in lumped_labels:

            table_path_name = f"{label}_table_path"
            imported_values_name = f"imported_{label}_values"
            _imported_values = getattr(self, imported_values_name)

            if _imported_values is None:
                line_edit = getattr(self, f"lineEdit_{label}_table_path")

                _imported_values, _table_path = self.load_table(line_edit, "lumped element", dof_label=label, direct_load=True)
                setattr(self, imported_values_name, _imported_values)
                setattr(self, table_path_name, _table_path)

            _table_path_attr = getattr(self, table_path_name)
            table_paths.append(str(_table_path_attr))

        for node_id in node_ids:

            table_names = list()

            for label in lumped_labels:
                imported_values_name = f"imported_{label}_values"
                _imported_values = getattr(self, imported_values_name)

                _table_name = None
                if isinstance(_imported_values, np.ndarray):
                    _table_name = self.get_table_name(f"lumped_{label}", node_id=node_id)
                    if self.save_table_values(_table_name, _imported_values):
                        return

                table_names.append(_table_name)

            if (table_names).count(None) != 6:
                self.lumped_element_applied = True

                node = app().project.model.preprocessor.nodes[node_id]
                coords = np.round(node.coordinates, 5)

                data = {
                        "coords" : list(coords),
                        "table_names" : table_names,
                        "table_paths" : table_paths,
                        }

                self.properties._set_nodal_property("lumped_stiffness", data, node_id)

    def check_table_values_for_lumped_dampings(self, node_ids: list):

        table_paths = list()
        lumped_labels = self.lumped_dampings_labels

        for label in lumped_labels:

            table_path_name = f"{label}_table_path"
            imported_values_name = f"imported_{label}_values"
            _imported_values = getattr(self, imported_values_name)

            if _imported_values is None:
                line_edit = getattr(self, f"lineEdit_{label}_table_path")

                _imported_values, _table_path = self.load_table(line_edit, "lumped element", dof_label=label, direct_load=True)
                setattr(self, imported_values_name, _imported_values)
                setattr(self, table_path_name, _table_path)

            _table_path_attr = getattr(self, table_path_name)
            table_paths.append(str(_table_path_attr))

        for node_id in node_ids:

            table_names = list()

            for label in lumped_labels:
                imported_values_name = f"imported_{label}_values"
                _imported_values = getattr(self, imported_values_name)

                _table_name = None
                if isinstance(_imported_values, np.ndarray):
                    _table_name = self.get_table_name(f"lumped_{label}", node_id=node_id)
                    if self.save_table_values(_table_name, _imported_values):
                        return

                table_names.append(_table_name)

            if (table_names).count(None) != 6:
                self.lumped_element_applied = True

                node = app().project.model.preprocessor.nodes[node_id]
                coords = np.round(node.coordinates, 5)

                data = {
                        "coords" : list(coords),
                        "table_names" : table_names,
                        "table_paths" : table_paths,
                        }

                self.properties._set_nodal_property("lumped_dampings", data, node_id)

    def check_table_values_inputs(self, node_ids: list):

        if self.check_table_values_for_lumped_masses(node_ids):
            return

        if self.check_table_values_for_lumped_stiffness(node_ids):
            return

        if self.check_table_values_for_lumped_dampings(node_ids):
            return

        if not self.lumped_element_applied:
            title = "Additional inputs required"
            message = "Choose at least one external element table " 
            message += "file to proceed with model assignment."
            PrintMessageInput([error_title, title, message]) 
            return

        self.actions_to_finalize()

    def remove_callback(self):

        if self.lineEdit_node_ids.text() == "":
            self.hide()
            title = "Invalid selection"
            message = "You should to select an item from the list "
            message += "to proceed with the removal."
            PrintMessageInput([warning_title, title, message])
            return

        str_nodes = self.lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            return

        if self.checkBox_remove_mass.isChecked():
            self.properties._remove_nodal_property("lumped_masses", node_ids)

        if self.checkBox_remove_spring.isChecked():
            self.properties._remove_nodal_property("lumped_stiffness", node_ids)

        if self.checkBox_remove_damper.isChecked():
            self.properties._remove_nodal_property("lumped_dampings", node_ids)

        self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Resetting of lumped elements"
        message = (
            "Would you like to remove all lumped elements from the structural model?"
        )

        buttons_config = {
            "left_button_label": "Cancel",
            "right_button_label": "Continue",
        }
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        if self.checkBox_remove_mass.isChecked():
            self.properties._reset_nodal_property("lumped_masses")

        if self.checkBox_remove_spring.isChecked():
            self.properties._reset_nodal_property("lumped_stiffness")

        if self.checkBox_remove_damper.isChecked():
            self.properties._reset_nodal_property("lumped_dampings")

        self.actions_to_finalize()
    
    def update_tabs_visibility(self):
        self.pushButton_remove.setDisabled(True)
        self.tabWidget_main.setTabVisible(1, False)
        for _property, *args in self.properties.nodal_properties.keys():
            if _property in ["lumped_masses", "lumped_stiffness", "lumped_dampings"]:
                self.tabWidget_main.setTabVisible(1, True)
                return

    def tab_event_callback(self):

        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_main.currentIndex() == 1:
            self.selection_frame.setDisabled(True)

        else:
            if self.cache_tab == 1:
                self.lineEdit_node_ids.clear()
            self.selection_frame.setDisabled(False)
            self.selection_callback()

        self.cache_tab = self.tabWidget_main.currentIndex()

    def actions_to_finalize(self):
        self.reset_table_variables()
        super().actions_to_finalize(reset_camera=False)

    def load_nodes_info(self):

        self.treeWidget_masses.clear()
        self.treeWidget_springs.clear()
        self.treeWidget_dampers.clear()

        m_labels = np.array(["m_x", "m_y", "m_z", "Jx", "Jy", "Jz"])
        k_labels = np.array(["k_x", "k_y", "k_z", "k_rx", "k_ry", "k_rz"])
        c_labels = np.array(["c_x", "c_y", "c_z", "c_rx", "c_ry", "c_rz"])

        for (property, *args), data in self.properties.nodal_properties.items():
            if property == "lumped_stiffness":
                node_id = args[0]
                k_mask = [False if bc is None else True for bc in data["values"]]
                text = [str(node_id), str(self.text_label(k_mask, k_labels))]

                item = QTreeWidgetItem(text)
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_springs.addTopLevelItem(item)

            if property == "lumped_dampings":
                node_id = args[0]
                c_mask = [False if bc is None else True for bc in data["values"]]
                text = [str(node_id), str(self.text_label(c_mask, c_labels))]

                item = QTreeWidgetItem(text)
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_dampers.addTopLevelItem(item)

            if property == "lumped_masses":
                node_id = args[0]
                m_mask = [False if bc is None else True for bc in data["values"]]
                text = [str(node_id), str(self.text_label(m_mask, m_labels))]

                item = QTreeWidgetItem(text)
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_masses.addTopLevelItem(item)

        self.update_tabs_visibility()

    def on_click_item_masses(self, item):
        self.pushButton_remove.setDisabled(False)
        if item.text(0) != "":
            self.lineEdit_node_ids.setText(item.text(0))
            node_id = int(item.text(0))
            app().main_window.set_selection(nodes=[node_id])

    def on_doubleclick_item_masses(self, item):
        self.on_click_item_masses(item)

    def on_click_item_springs(self, item):
        self.pushButton_remove.setDisabled(False)
        if item.text(0) != "":
            self.lineEdit_node_ids.setText(item.text(0))
            node_id = int(item.text(0))
            app().main_window.set_selection(nodes=[node_id])

    def on_doubleclick_item_springs(self, item):
        self.on_click_item_springs(item)

    def on_click_item_dampings(self, item):
        self.pushButton_remove.setDisabled(False)
        if item.text(0) != "":
            self.lineEdit_node_ids.setText(item.text(0))
            node_id = int(item.text(0))
            app().main_window.set_selection(nodes=[node_id])

    def on_doubleclick_item_dampings(self, item):
        self.on_click_item_dampings(item)

    def reset_input_fields_masses(self):
        for lineEdit_constant_masses in self.constant_values_lumped_masses:
            lineEdit_constant_masses.clear()
        for lineEdit_table_masses in self.table_values_lumped_masses:
            lineEdit_table_masses.clear()

    def reset_input_fields_stiffness(self):
        for lineEdit_constant_stiffness in self.constant_values_lumped_stiffness:
            lineEdit_constant_stiffness.clear()
        for lineEdit_table_stiffness in self.table_values_lumped_stiffness:
            lineEdit_table_stiffness.clear()

    def reset_input_fields_dampings(self):
        for lineEdit_constant_dampings in self.constant_values_lumped_dampings:
            lineEdit_constant_dampings.clear()
        for lineEdit_table_dampings in self.table_values_lumped_dampings:
            lineEdit_table_dampings.clear()
