from enum import IntEnum
from functools import partial

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHeaderView, QLineEdit, QPushButton, QTreeWidgetItem

from pulse import app
from pulse.interface.ui_generated.model.setup.structural.mass_spring_damper_input_ui import (
    MassSpringDamperInput_UI,
)
from pulse.interface.user_input.model.setup.structural.structural_nodes_input import (
    StructuralNodesInput,
)
from pulse.interface.user_input.numeric_checks.validators import StrictDoubleValidator
from pulse.interface.user_input.project.get_user_confirmation_input import (
    GetUserConfirmationInput,
)
from pulse.interface.user_input.project.print_message import PrintMessageInput


class TabIndex(IntEnum):
    CONSTANT = 0
    TABULAR = 1
    LIST = 2


class TabList(IntEnum):
    MULTIPLE = 0
    MASS = 1
    STIFFNESS = 2
    DAMPING = 3


class LumpedElementType(IntEnum):
    MASS = 0
    STIFFNESS = 1
    DAMPING = 2


error_title ="Error"
warning_title = "Warning"


class MassSpringDamperInput(StructuralNodesInput, MassSpringDamperInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._initialize()
        self._config_widgets()
        self._configure_validators()
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

    def _config_widgets(self):
        #
        self.cache_tab = self.tabWidget_main.currentIndex()
        #
        self.treeWidget_mass.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.treeWidget_stiffness.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.treeWidget_damping.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #
        for i in range(2):
            self.treeWidget_mass.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_stiffness.headerItem().setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_damping.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def _configure_validators(self):

        validator = StrictDoubleValidator(-1e10, 1e10, 6)

        for line_edit in self.findChildren(QLineEdit):
            obj_name = line_edit.objectName()

            if "table_path" in obj_name:
                continue

            if obj_name == "lineEdit_node_ids":
                continue

            line_edit.setValidator(validator)

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
        self.treeWidget_mass.itemClicked.connect(self.on_click_item_masses)
        self.treeWidget_mass.itemDoubleClicked.connect(
            self.on_doubleclick_item_masses
        )
        #
        self.treeWidget_stiffness.itemClicked.connect(self.on_click_item_stiffness)
        self.treeWidget_stiffness.itemDoubleClicked.connect(
            self.on_doubleclick_item_stiffness
        )
        #
        self.treeWidget_damping.itemClicked.connect(self.on_click_item_dampings)
        self.treeWidget_damping.itemDoubleClicked.connect(
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

            if len(selected_nodes) != 1:
                return

            node_id = selected_nodes[0]

            # Lumped masses/inertias
            lm_data = self.properties._get_property("lumped_masses", node_ids=node_id)

            if isinstance(lm_data, dict):
                if "table_names" in lm_data.keys():
                    self.tabWidget_main.setCurrentIndex(TabIndex.TABULAR)
                    self.tabWidget_table_values.setCurrentIndex(LumpedElementType.MASS)
                    for i, table_path in enumerate(lm_data["table_paths"]):
                        if table_path is not None:
                            lineEdit = self.table_values_lumped_masses[i]
                            lineEdit.setText(table_path)

                else:
                    self.tabWidget_main.setCurrentIndex(TabIndex.CONSTANT)
                    self.tabWidget_constant_values.setCurrentIndex(LumpedElementType.MASS)
                    for i, value in enumerate(lm_data["values"]):
                        if isinstance(value, complex):
                            _value = np.real(value)
                            lineEdit = self.constant_values_lumped_masses[i]
                            lineEdit.setText(f"{_value : .3e}")

            # Lumped stiffness
            ls_data = self.properties._get_property("lumped_stiffness", node_ids=node_id)

            if isinstance(ls_data, dict):
                if "table_names" in ls_data.keys():
                    self.tabWidget_main.setCurrentIndex(TabIndex.TABULAR)
                    self.tabWidget_table_values.setCurrentIndex(LumpedElementType.STIFFNESS)
                    for i, table_path in enumerate(ls_data["table_paths"]):
                        if table_path is not None:
                            lineEdit = self.table_values_lumped_stiffness[i]
                            lineEdit.setText(table_path)

                else:
                    self.tabWidget_main.setCurrentIndex(TabIndex.CONSTANT)
                    self.tabWidget_constant_values.setCurrentIndex(LumpedElementType.STIFFNESS)
                    for i, value in enumerate(ls_data["values"]):
                        if isinstance(value, complex):
                            _value = np.real(value)
                            lineEdit = self.constant_values_lumped_stiffness[i]
                            lineEdit.setText(f"{_value : .3e}")

            # Lumped dampings
            ld_data = self.properties._get_property("lumped_dampings", node_ids=node_id)

            if isinstance(ld_data, dict):
                if "table_names" in ld_data.keys():
                    self.tabWidget_main.setCurrentIndex(TabIndex.TABULAR)
                    self.tabWidget_table_values.setCurrentIndex(LumpedElementType.DAMPING)                   
                    for i, table_path in enumerate(ld_data["table_paths"]):
                        if table_path is not None:
                            lineEdit = self.table_values_lumped_dampings[i]
                            lineEdit.setText(table_path)

                else:
                    self.tabWidget_main.setCurrentIndex(TabIndex.CONSTANT)
                    self.tabWidget_constant_values.setCurrentIndex(LumpedElementType.DAMPING)
                    for i, value in enumerate(ld_data["values"]):
                          if isinstance(value, complex):
                            _value = np.real(value)
                            lineEdit = self.constant_values_lumped_dampings[i]
                            lineEdit.setText(f"{_value : .3e}")

    def load_table_for_line_edit(self, line_edit, dof_label):
        return super().load_table_for_line_edit(line_edit, dof_label, "lumped element")

    def attribute_callback(self):

        str_nodes = self.lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            return True

        self.remove_properties_from_node(node_ids, ["lumped_masses", "lumped_stiffness", "lumped_dampings"])

        str_nodes = self.lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            self.lineEdit_node_ids.setFocus()
            return

        tab_index = self.tabWidget_main.currentIndex()
        if tab_index == TabIndex.CONSTANT:
            self.check_constant_values_inputs(node_ids)

        elif tab_index == TabIndex.TABULAR:
            self.check_table_values_inputs(node_ids)

        self.actions_to_finalize()

    def check_constant_values_lumped_masses(self, node_ids: list):

        Mx = self.check_entries(self.lineEdit_Mx)
        My = self.check_entries(self.lineEdit_My)
        Mz = self.check_entries(self.lineEdit_Mz)
        Jx = self.check_entries(self.lineEdit_Jx)
        Jy = self.check_entries(self.lineEdit_Jy)
        Jz = self.check_entries(self.lineEdit_Jz)

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

        Kx = self.check_entries(self.lineEdit_Kx)
        Ky = self.check_entries(self.lineEdit_Ky)
        Kz = self.check_entries(self.lineEdit_Kz)
        Krx = self.check_entries(self.lineEdit_Krx)
        Kry = self.check_entries(self.lineEdit_Kry)
        Krz = self.check_entries(self.lineEdit_Krz)

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

        Cx = self.check_entries(self.lineEdit_Cx)
        Cy = self.check_entries(self.lineEdit_Cy)
        Cz = self.check_entries(self.lineEdit_Cz)
        Crx = self.check_entries(self.lineEdit_Crx)
        Cry = self.check_entries(self.lineEdit_Cry)
        Crz = self.check_entries(self.lineEdit_Crz)

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

    def check_table_values_inputs(self, node_ids: list):

        assigned_properties = list()
        for lumped_label in ["lumped_masses", "lumped_stiffness", "lumped_dampings"]:

            assigned = self.table_values_attribution_callback(
                node_ids = node_ids,
                property_label = lumped_label,
                dof_labels = getattr(self, f"{lumped_label}_labels"),
                properties_to_remove = [],
                ignore_empty = True,
                )

            assigned_properties.append(assigned)

        if not any(assigned_properties):
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

        if self.checkBox_remove_stiffness.isChecked():
            self.properties._remove_nodal_property("lumped_stiffness", node_ids)

        if self.checkBox_remove_damping.isChecked():
            self.properties._remove_nodal_property("lumped_dampings", node_ids)

        self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Lumped elements resetting"
        message = "Would you like to remove all lumped elements from the structural model?"

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

        if self.checkBox_remove_stiffness.isChecked():
            self.properties._reset_nodal_property("lumped_stiffness")

        if self.checkBox_remove_damping.isChecked():
            self.properties._reset_nodal_property("lumped_dampings")

        self.actions_to_finalize()

    def actions_to_finalize(self):
        self.reset_table_variables()
        super().actions_to_finalize(reset_camera=False)

    def update_tabs_visibility(self):

        properties = [
            "lumped_masses", 
            "lumped_stiffness", 
            "lumped_dampings",
            ]

        check_boxes = [
            self.checkBox_remove_mass,
            self.checkBox_remove_stiffness,
            self.checkBox_remove_damping,
            ]

        self.pushButton_remove.setDisabled(True)
        self.checkBox_remove_mass.setChecked(False)
        self.checkBox_remove_stiffness.setChecked(False)
        self.checkBox_remove_damping.setChecked(False)

        self.tabWidget_main.setTabVisible(TabIndex.LIST, False)
        self.tabWidget_remove.setTabVisible(TabList.MASS, False)
        self.tabWidget_remove.setTabVisible(TabList.STIFFNESS, False)
        self.tabWidget_remove.setTabVisible(TabList.DAMPING, False)

        for _property, *args in self.properties.nodal_properties.keys():
            if _property in properties:
                index = properties.index(_property)
                self.tabWidget_main.setTabVisible(TabIndex.LIST, True)
                self.tabWidget_remove.setTabVisible(index + 1, True)
                check_boxes[index].setChecked(True)

        if not self.tabWidget_main.isVisible():
            self.tabWidget_main.setCurrentIndex(TabIndex.CONSTANT)
            self.tabWidget_constant_values.setCurrentIndex(LumpedElementType.MASS)
            self.lineEdit_Mx.setFocus()

        for check_box in check_boxes:
            is_checked = check_box.isChecked()
            check_box.setEnabled(is_checked)

    def load_nodes_info(self):

        self.treeWidget_mass.clear()
        self.treeWidget_stiffness.clear()
        self.treeWidget_damping.clear()

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

                self.treeWidget_stiffness.addTopLevelItem(item)

            if property == "lumped_dampings":
                node_id = args[0]
                c_mask = [False if bc is None else True for bc in data["values"]]
                text = [str(node_id), str(self.text_label(c_mask, c_labels))]

                item = QTreeWidgetItem(text)
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_damping.addTopLevelItem(item)

            if property == "lumped_masses":
                node_id = args[0]
                m_mask = [False if bc is None else True for bc in data["values"]]
                text = [str(node_id), str(self.text_label(m_mask, m_labels))]

                item = QTreeWidgetItem(text)
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_mass.addTopLevelItem(item)

        self.update_tabs_visibility()

    def tab_event_callback(self):

        tab_list = self.tabWidget_main.currentIndex() == TabIndex.LIST

        self.pushButton_remove.setDisabled(True)      
        self.pushButton_attribute.setDisabled(tab_list)
        self.selection_frame.setDisabled(tab_list)

        # if not tab_list:
        #     if self.cache_tab == TabIndex.LIST:
        #         self.lineEdit_node_ids.clear()

        # self.cache_tab = self.tabWidget_main.currentIndex()

    def update_and_highlight_node(self, node_id: str):
        self.lineEdit_node_ids.setText(node_id)
        _node_id = int(node_id)
        app().main_window.selection_changed.disconnect(self.selection_callback)
        app().main_window.set_selection(nodes=[_node_id])
        app().main_window.selection_changed.connect(self.selection_callback)

    def on_click_item_masses(self, item):
        self.pushButton_remove.setDisabled(False)
        if item.text(0) != "":
            self.update_and_highlight_node(item.text(0))

    def on_doubleclick_item_masses(self, item):
        self.on_click_item_masses(item)

    def on_click_item_stiffness(self, item):
        self.pushButton_remove.setDisabled(False)
        if item.text(0) != "":
            self.update_and_highlight_node(item.text(0))

    def on_doubleclick_item_stiffness(self, item):
        self.on_click_item_stiffness(item)

    def on_click_item_dampings(self, item):
        self.pushButton_remove.setDisabled(False)
        if item.text(0) != "":
            self.update_and_highlight_node(item.text(0))

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


    # def check_table_values_for_lumped_masses(self, node_ids: list):

    #     table_paths = list()
        
    #     for label in self.lumped_masses_labels:

    #         table_path_name = f"{label}_table_path"
    #         imported_values_name = f"imported_{label}_values"
    #         _imported_values = getattr(self, imported_values_name)

    #         if _imported_values is None:
    #             line_edit = getattr(self, f"lineEdit_{label}_table_path")

    #             _imported_values, _table_path = self.load_table(line_edit, "lumped element", dof_label=label, direct_load=True)
    #             setattr(self, imported_values_name, _imported_values)
    #             setattr(self, table_path_name, _table_path)

    #         _table_path_attr = getattr(self, table_path_name)
    #         table_paths.append(str(_table_path_attr))

    #     for node_id in node_ids:

    #         table_names = list()

    #         for label in self.lumped_masses_labels:
    #             imported_values_name = f"imported_{label}_values"
    #             _imported_values = getattr(self, imported_values_name)

    #             _table_name = None
    #             if isinstance(_imported_values, np.ndarray):
    #                 _table_name = self.get_table_name(f"lumped_{label}", node_id=node_id)
    #                 if self.save_table_values(_table_name, _imported_values):
    #                     return

    #             table_names.append(_table_name)

    #         if (table_names).count(None) != 6:

    #             self.lumped_element_applied = True

    #             node = app().project.model.preprocessor.nodes[node_id]
    #             coords = np.round(node.coordinates, 5)

    #             _data = {
    #                 "coords" : list(coords),
    #                 "table_names" : table_names,
    #                 "table_paths" : table_paths,
    #                 }

    #             self.properties._set_nodal_property("lumped_masses", _data, node_id)

    # def check_table_values_for_lumped_stiffness(self, node_ids: list):

    #     table_paths = list()
    #     lumped_labels = self.lumped_stiffness_labels
        
    #     for label in lumped_labels:

    #         table_path_name = f"{label}_table_path"
    #         imported_values_name = f"imported_{label}_values"
    #         _imported_values = getattr(self, imported_values_name)

    #         if _imported_values is None:
    #             line_edit = getattr(self, f"lineEdit_{label}_table_path")

    #             _imported_values, _table_path = self.load_table(line_edit, "lumped element", dof_label=label, direct_load=True)
    #             setattr(self, imported_values_name, _imported_values)
    #             setattr(self, table_path_name, _table_path)

    #         _table_path_attr = getattr(self, table_path_name)
    #         table_paths.append(str(_table_path_attr))

    #     for node_id in node_ids:

    #         table_names = list()

    #         for label in lumped_labels:
    #             imported_values_name = f"imported_{label}_values"
    #             _imported_values = getattr(self, imported_values_name)

    #             _table_name = None
    #             if isinstance(_imported_values, np.ndarray):
    #                 _table_name = self.get_table_name(f"lumped_{label}", node_id=node_id)
    #                 if self.save_table_values(_table_name, _imported_values):
    #                     return

    #             table_names.append(_table_name)

    #         if (table_names).count(None) != 6:
    #             self.lumped_element_applied = True

    #             node = app().project.model.preprocessor.nodes[node_id]
    #             coords = np.round(node.coordinates, 5)

    #             data = {
    #                     "coords" : list(coords),
    #                     "table_names" : table_names,
    #                     "table_paths" : table_paths,
    #                     }

    #             self.properties._set_nodal_property("lumped_stiffness", data, node_id)

    # def check_table_values_for_lumped_dampings(self, node_ids: list):

    #     table_paths = list()
    #     lumped_labels = self.lumped_dampings_labels

    #     for label in lumped_labels:

    #         table_path_name = f"{label}_table_path"
    #         imported_values_name = f"imported_{label}_values"
    #         _imported_values = getattr(self, imported_values_name)

    #         if _imported_values is None:
    #             line_edit = getattr(self, f"lineEdit_{label}_table_path")

    #             _imported_values, _table_path = self.load_table(line_edit, "lumped element", dof_label=label, direct_load=True)
    #             setattr(self, imported_values_name, _imported_values)
    #             setattr(self, table_path_name, _table_path)

    #         _table_path_attr = getattr(self, table_path_name)
    #         table_paths.append(str(_table_path_attr))

    #     for node_id in node_ids:

    #         table_names = list()

    #         for label in lumped_labels:
    #             imported_values_name = f"imported_{label}_values"
    #             _imported_values = getattr(self, imported_values_name)

    #             _table_name = None
    #             if isinstance(_imported_values, np.ndarray):
    #                 _table_name = self.get_table_name(f"lumped_{label}", node_id=node_id)
    #                 if self.save_table_values(_table_name, _imported_values):
    #                     return

    #             table_names.append(_table_name)

    #         if (table_names).count(None) != 6:
    #             self.lumped_element_applied = True

    #             node = app().project.model.preprocessor.nodes[node_id]
    #             coords = np.round(node.coordinates, 5)

    #             data = {
    #                     "coords" : list(coords),
    #                     "table_names" : table_names,
    #                     "table_paths" : table_paths,
    #                     }

    #             self.properties._set_nodal_property("lumped_dampings", data, node_id)