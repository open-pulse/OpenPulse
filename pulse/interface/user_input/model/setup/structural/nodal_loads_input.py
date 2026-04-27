from enum import IntEnum

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHeaderView, QLineEdit, QTreeWidgetItem

from pulse import app
from pulse.interface.ui_generated.model.setup.structural.nodal_loads_input_ui import (
    NodalLoadsInput_UI,
)
from pulse.interface.user_input.model.setup.general.get_information_of_group import (
    GetInformationOfGroup,
)
from pulse.interface.user_input.model.setup.structural.structural_nodes_input import (
    StructuralNodesInput,
)
from pulse.interface.user_input.numeric_checks.double_validator import StrictDoubleValidator
from pulse.interface.user_input.project.get_user_confirmation_input import (
    GetUserConfirmationInput,
)
from pulse.interface.user_input.project.print_message import PrintMessageInput


class TabIndex(IntEnum):
    CONSTANT = 0
    TABULAR = 1
    LIST = 2


error_title = "Error"
warning_title = "Warning"


class NodalLoadsInput(StructuralNodesInput, NodalLoadsInput_UI):
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
        self.load_labels = np.array(["Fx", "Fy", "Fz", "Mx", "My", "Mz"])

        self.reset_table_variables()
        self.create_widgets_lists()

        self.keep_window_open = True

        self.list_Nones = [None, None, None, None, None, None]

    def _configure_validators(self):

        validator = StrictDoubleValidator(-1e10, 1e10, 6)

        for line_edit in self.findChildren(QLineEdit):
            obj_name = line_edit.objectName()

            if "real" in obj_name:
                line_edit.setValidator(validator)

            elif "imag" in obj_name:
                line_edit.setValidator(validator)

    def create_widgets_lists(self):

        self.list_lineEdit_constant_values = [
            [self.lineEdit_real_Fx, self.lineEdit_imag_Fx],
            [self.lineEdit_real_Fy, self.lineEdit_imag_Fy],
            [self.lineEdit_real_Fz, self.lineEdit_imag_Fz],
            [self.lineEdit_real_Mx, self.lineEdit_imag_Mx],
            [self.lineEdit_real_My, self.lineEdit_imag_My],
            [self.lineEdit_real_Mz, self.lineEdit_imag_Mz],
        ]

        self.list_lineEdit_table_values = [
            self.lineEdit_Fx_table_path,
            self.lineEdit_Fy_table_path,
            self.lineEdit_Fz_table_path,
            self.lineEdit_Mx_table_path,
            self.lineEdit_My_table_path,
            self.lineEdit_Mz_table_path,
        ]

    def reset_table_variables(self):
       for label in self.load_labels:
            setattr(self, f"imported_{label}_values", None)
            setattr(self, f"{label}_table_path", None)

    def _create_connections(self):
        #
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        #
        self.connect_load_table_push_buttons(self.list_lineEdit_table_values, self.load_labels)
        #
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_nodal_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_nodal_info.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)
        self.selection_callback()

    def selection_callback(self):
        selected_nodes = app().main_window.list_selected_nodes()

        if selected_nodes:
            text = ", ".join([str(i) for i in selected_nodes])
            self.lineEdit_node_ids.setText(text)

            if len(selected_nodes) != 1:
                return
        
            for (property, *args), data in self.properties.nodal_properties.items():
                if property != "nodal_loads":
                    continue

                if selected_nodes != args:
                    continue

                values = data["values"]

                if "table_paths" in data.keys():
                    table_paths = data["table_paths"]
                    for index, lineEdit_table in enumerate(
                        self.list_lineEdit_table_values
                    ):
                        table_path = table_paths[index]
                        if table_path is not None:
                            lineEdit_table.setText(table_path)

                else:
                    for index, [lineEdit_real, lineEdit_imag] in enumerate(
                        self.list_lineEdit_constant_values
                    ):
                        if values[index] is not None:
                            lineEdit_real.setText(str(np.real(values[index])))
                            lineEdit_imag.setText(str(np.imag(values[index])))

    def _config_widgets(self):
        #
        self.treeWidget_nodal_info.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #
        for i in range(2):
            self.treeWidget_nodal_info.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def check_complex_entries(self, lineEdit_real: QLineEdit, lineEdit_imag: QLineEdit):

        _real = 0
        if lineEdit_real.text() != "":
            _real = float(lineEdit_real.text())

        _imag = 0
        if lineEdit_imag.text() != "":
            _imag = float(lineEdit_imag.text())

        if _real == 0 and _imag == 0:
            return None

        return _real + 1j * _imag

    def attribute_callback(self):

        str_nodes = self.lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            self.lineEdit_node_ids.setFocus()
            return

        tab_index = self.tabWidget_main.currentIndex()
        if tab_index == TabIndex.CONSTANT:
            self.constant_values_attribution_callback(node_ids)

        elif tab_index == TabIndex.TABULAR:
            self.table_values_attribution_callback(
                node_ids = node_ids,
                property_label = "nodal_loads",
                dof_labels = self.load_labels,
                properties_to_remove = ["prescribed_dofs", "nodal_loads"],
                )

    def constant_values_attribution_callback(self, node_ids: list[int]):

        Fx = self.check_complex_entries(self.lineEdit_real_Fx, self.lineEdit_imag_Fx)
        Fy = self.check_complex_entries(self.lineEdit_real_Fy, self.lineEdit_imag_Fy)
        Fz = self.check_complex_entries(self.lineEdit_real_Fz, self.lineEdit_imag_Fz)
        Mx = self.check_complex_entries(self.lineEdit_real_Mx, self.lineEdit_imag_Mx)
        My = self.check_complex_entries(self.lineEdit_real_My, self.lineEdit_imag_My)
        Mz = self.check_complex_entries(self.lineEdit_real_Mz, self.lineEdit_imag_Mz)

        nodal_loads = [Fx, Fy, Fz, Mx, My, Mz]

        if nodal_loads.count(None) == 6:
            self.hide()
            title = "Additional inputs required"
            message = "You must to inform at least one nodal load "
            message += "before confirming the input!"
            PrintMessageInput([error_title, title, message])
            return

        self.remove_properties_from_node(node_ids, ["prescribed_dofs", "nodal_loads"])

        real_values = [value if value is None else np.real(value) for value in nodal_loads]
        imag_values = [value if value is None else np.imag(value) for value in nodal_loads]

        for node_id in node_ids:
            node = app().project.model.preprocessor.nodes[node_id]
            coords = np.round(node.coordinates, 5)

            data = {
                "coords": list(coords),
                "values": nodal_loads,
                "real_values": real_values,
                "imag_values": imag_values,
            }

            self.properties._set_nodal_property("nodal_loads", data, node_id)

        self.actions_to_finalize()

    def load_table_for_line_edit(self, line_edit, dof_label):
        return super().load_table_for_line_edit(line_edit, dof_label, "nodal loads")

    def load_nodes_info(self):

        self.treeWidget_nodal_info.clear()
        for (property, *args), data in self.properties.nodal_properties.items():
            if property == "nodal_loads":
                values = data["values"]
                constrained_dofs_mask = [
                    False if value is None else True for value in values
                ]
                new = QTreeWidgetItem(
                    [
                        str(args[0]),
                        str(self.text_label(constrained_dofs_mask, self.load_labels)),
                    ]
                )
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_nodal_info.addTopLevelItem(new)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):

        self.tabWidget_main.setTabVisible(TabIndex.LIST, False)
        for property, *_ in self.properties.nodal_properties.keys():
            if property == "nodal_loads":
                self.tabWidget_main.setCurrentIndex(TabIndex.CONSTANT)
                self.tabWidget_main.setTabVisible(TabIndex.LIST, True)
                return

    def tab_event_callback(self):

        tab_list = self.tabWidget_main.currentIndex() == TabIndex.LIST
        self.lineEdit_node_ids.setDisabled(tab_list)
        self.pushButton_attribute.setDisabled(tab_list)
        self.pushButton_remove.setDisabled(True)

        if not tab_list:
            self.lineEdit_node_ids.setEnabled(True)
            # self.selection_callback()
            return

        selected_items = self.treeWidget_nodal_info.selectedItems()
        if selected_items == list():
            self.lineEdit_node_ids.clear()
        else:
            self.on_click_item(selected_items[0])

    def on_click_item(self, item: QTreeWidgetItem):
        self.pushButton_remove.setDisabled(False)
        if item.text(0) != "":
            self.lineEdit_node_ids.setText(item.text(0))
            node_id = int(item.text(0))
            app().main_window.set_selection(nodes=[node_id])

    def on_double_click_item(self, item: QTreeWidgetItem):
        self.on_click_item(item)
        self.get_nodal_info(item)

    def get_nodal_info(self, item: QTreeWidgetItem):
        try:
            loads_info = dict()
            selected_node = int(item.text(0))

            for (property, *args), data in self.properties.nodal_properties.items():
                if property == "nodal_loads" and selected_node == args[0]:
                    values = data["values"]
                    nodal_loads_mask = [False if bc is None else True for bc in values]

                    for i, _bool in enumerate(nodal_loads_mask):
                        if _bool:
                            dof_label = self.load_labels[i]
                            loads_info[selected_node, dof_label] = values[i]

            if len(loads_info):
                self.hide()
                header_labels = ["Node ID", "DOF label", "Value"]
                GetInformationOfGroup(
                    group_label="Nodal loads",
                    selection_label="Node ID:",
                    header_labels=header_labels,
                    column_widths=[70, 140, 150],
                    data=data,
                )

        except Exception as error_log:
            title = "Error while gathering nodal loads information"
            message = str(error_log)
            PrintMessageInput([error_title, title, message])
            return

        self.show()

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

        self.properties._remove_nodal_property("nodal_loads", node_ids)
        self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Nodal loads resetting"
        message = "Would you like to remove all nodal loads from the structural model?"

        buttons_config = {
            "left_button_label": "Cancel",
            "right_button_label": "Continue",
        }
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        self.properties._reset_nodal_property("nodal_loads")
        self.actions_to_finalize()

    def actions_to_finalize(self):
        self.reset_table_variables()
        super().actions_to_finalize(reset_camera=False)

    def reset_input_fields(self):
        self.lineEdit_node_ids.clear()
        for [lineEdit_real, lineEdit_imag] in self.list_lineEdit_constant_values:
            lineEdit_real.clear()
            lineEdit_imag.clear()
        for lineEdit_table in self.list_lineEdit_table_values:
            lineEdit_table.clear()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()

        elif event.key() == Qt.Key_Escape:
            self.close()
