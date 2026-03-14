from enum import IntEnum

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QTreeWidgetItem

from pulse import app
from pulse.interface.ui_generated.model.setup.structural.nodal_loads_input_ui import (
    NodalLoadsInput_UI,
)
from pulse.interface.user_input.model.setup.general.get_information_of_group import (
    GetInformationOfGroup,
)
from pulse.interface.user_input.project.get_user_confirmation_input import (
    GetUserConfirmationInput,
)
from pulse.interface.user_input.project.print_message import PrintMessageInput

from pulse.interface.user_input.model.setup.structural.structural_nodes_input import (
    StructuralNodesInput,
)

class TabType(IntEnum):
    CONSTANT = 0
    TABULAR = 1
    LIST = 2


error_title = "Error"
warning_title = "Warning"


class NodalLoadsInput(StructuralNodesInput, NodalLoadsInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config_widgets()
        self._initialize()
        self._create_connections()

        self.load_nodes_info()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):

        self.reset_table_variables()
        self.create_widgets_lists()

        self.keep_window_open = True

        self.list_Nones = [None, None, None, None, None, None]
        self.load_labels = np.array(["Fx", "Fy", "Fz", "Mx", "My", "Mz"])

    def create_widgets_lists(self):

        self.list_lineEdit_constant_values = [  
            [self.lineEdit_real_fx, self.lineEdit_imag_fx],
            [self.lineEdit_real_fy, self.lineEdit_imag_fy],
            [self.lineEdit_real_fz, self.lineEdit_imag_fz],
            [self.lineEdit_real_mx, self.lineEdit_imag_mx],
            [self.lineEdit_real_my, self.lineEdit_imag_my],
            [self.lineEdit_real_mz, self.lineEdit_imag_mz],
            ]

        self.list_lineEdit_table_values = [ 
            self.lineEdit_fx_table_path,
            self.lineEdit_fy_table_path,
            self.lineEdit_fz_table_path,
            self.lineEdit_mx_table_path,
            self.lineEdit_my_table_path,
            self.lineEdit_mz_table_path,
            ]

    def reset_table_variables(self):

        self.imported_fx_values = None
        self.imported_fy_values = None
        self.imported_fz_values = None
        self.imported_mx_values = None
        self.imported_my_values = None
        self.imported_mz_values = None

        self.fx_table_path = None
        self.fy_table_path = None
        self.fz_table_path = None
        self.mx_table_path = None
        self.my_table_path = None
        self.mz_table_path = None

    def _create_connections(self):
        #
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_attribute.clicked.connect(self.attribution_callback)
        self.pushButton_load_fx_table.clicked.connect(self.load_fx_table)
        self.pushButton_load_fy_table.clicked.connect(self.load_fy_table)
        self.pushButton_load_fz_table.clicked.connect(self.load_fz_table)
        self.pushButton_load_mx_table.clicked.connect(self.load_mx_table)
        self.pushButton_load_my_table.clicked.connect(self.load_my_table)
        self.pushButton_load_mz_table.clicked.connect(self.load_mz_table)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_nodal_loads.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_nodal_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_nodal_info.itemDoubleClicked.connect(self.on_double_click_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)
        self.selection_callback()

    def selection_callback(self):

        self.reset_input_fields()
        selected_nodes = app().main_window.list_selected_nodes()

        if selected_nodes:
            text = ", ".join([str(i) for i in selected_nodes])
            self.lineEdit_node_ids.setText(text)

            if len(selected_nodes) == 1:
                for (property, *args), data in self.properties.nodal_properties.items():
                    if property == "nodal_loads" and selected_nodes == args:
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
        for i, width in enumerate([80, 60]):
            self.treeWidget_nodal_info.setColumnWidth(i, width)
            self.treeWidget_nodal_info.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def check_complex_entries(self, lineEdit_real, lineEdit_imag, label):

        stop = False
        if lineEdit_real.text() != "":
            try:
                _real = float(lineEdit_real.text())
            except Exception:
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for real part of {label}."
                PrintMessageInput([error_title, title, message])
                stop = True
                return stop, None
        else:
            _real = 0

        if lineEdit_imag.text() != "":
            try:
                _imag = float(lineEdit_imag.text())
            except Exception:
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for imaginary part of {label}."
                PrintMessageInput([error_title, title, message])
                stop = True
                return stop, None
        else:
            _imag = 0

        if _real == 0 and _imag == 0:
            return stop, None
        else:
            return stop, _real + 1j*_imag
        
    def attribution_callback(self):
        tab_index = self.tabWidget_nodal_loads.currentIndex()
        if tab_index == TabType.CONSTANT:
            self.constant_values_attribution_callback()

        elif tab_index == TabType.TABULAR:
            self.table_values_attribution_callback()

    def constant_values_attribution_callback(self):

        str_nodes = self.lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            self.lineEdit_node_ids.setFocus()
            return

        stop, Fx = self.check_complex_entries(
            self.lineEdit_real_fx, self.lineEdit_imag_fx, "Fx"
        )
        if stop:
            return

        stop, Fy = self.check_complex_entries(
            self.lineEdit_real_fy, self.lineEdit_imag_fy, "Fy"
        )
        if stop:
            return

        stop, Fz = self.check_complex_entries(
            self.lineEdit_real_fz, self.lineEdit_imag_fz, "Fz"
        )
        if stop:
            return

        stop, Mx = self.check_complex_entries(
            self.lineEdit_real_mx, self.lineEdit_imag_mx, "Mx"
        )
        if stop:
            return

        stop, My = self.check_complex_entries(
            self.lineEdit_real_my, self.lineEdit_imag_my, "My"
        )
        if stop:
            return

        stop, Mz = self.check_complex_entries(
            self.lineEdit_real_mz, self.lineEdit_imag_mz, "Mz"
        )
        if stop:
            return

        nodal_loads = [Fx, Fy, Fz, Mx, My, Mz]
        
        if nodal_loads.count(None) == 6:
            self.hide()
            title = "Additional inputs required"
            message = "You must to inform at least one nodal load "
            message += "before confirming the input!"
            PrintMessageInput([error_title, title, message]) 
            return

        self.remove_properties_from_node(node_ids)

        real_values = [value if value is None else np.real(value) for value in nodal_loads]
        imag_values = [value if value is None else np.imag(value) for value in nodal_loads]

        for node_id in node_ids:

            node = app().project.model.preprocessor.nodes[node_id]
            coords = np.round(node.coordinates, 5)

            data = {
                    "coords" : list(coords),
                    "values" : nodal_loads,
                    "real_values" : real_values,
                    "imag_values" : imag_values
                    }

            self.properties._set_nodal_property("nodal_loads", data, node_id)

        self.actions_to_finalize()

    def load_fx_table(self):
        self.imported_fx_values, self.fx_table_path = CommonUserInputs(self).load_table(
            self.lineEdit_fx_table_path, 
            "nodal loads", 
            dof_label="Fx",
            )

        if self.fx_table_path is None:
            self.line_edit_reset(self.lineEdit_fx_table_path)

    def load_fy_table(self):
        self.imported_fy_values, self.fy_table_path = CommonUserInputs(self).load_table(
            self.lineEdit_fy_table_path, 
            "nodal loads", 
            dof_label="Fy",
            )

        if self.fy_table_path is None:
            self.line_edit_reset(self.lineEdit_fy_table_path)

    def load_fz_table(self):
        self.imported_fz_values, self.fz_table_path = CommonUserInputs(self).load_table(
            self.lineEdit_fz_table_path, 
            "nodal loads", 
            dof_label="Fz",
            )

        if self.fz_table_path is None:
            self.line_edit_reset(self.lineEdit_fz_table_path)

    def load_mx_table(self):
        self.imported_mx_values, self.mx_table_path = CommonUserInputs(self).load_table(
            self.lineEdit_mx_table_path, 
            "nodal loads", 
            dof_label="Mx",
            )

        if self.mx_table_path is None:
            self.line_edit_reset(self.lineEdit_mx_table_path)

    def load_my_table(self):
        self.imported_my_values, self.my_table_path = CommonUserInputs(self).load_table(
            self.lineEdit_my_table_path, 
            "nodal loads", 
            dof_label="My",
            )

        if self.my_table_path is None:
            self.line_edit_reset(self.lineEdit_my_table_path)

    def load_mz_table(self):
        self.imported_mz_values, self.mz_table_path = CommonUserInputs(self).load_table(
            self.lineEdit_mz_table_path, 
            "nodal loads", 
            dof_label="Mz",
            )

        if self.mz_table_path is None:
            self.line_edit_reset(self.lineEdit_mz_table_path)

    def line_edit_reset(self, lineEdit : QLineEdit):
        lineEdit.clear()
        lineEdit.setFocus() 

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

    def table_values_attribution_callback(self):

        str_nodes = self.lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            self.lineEdit_node_ids.setFocus()
            return

        self.remove_properties_from_node(node_ids)

        table_paths = list()
        load_labels = ["fx", "fy", "fz", "mx", "my", "mz"]

        for label in load_labels:

            table_path_name = f"{label}_table_path"
            imported_values_name = f"imported_{label}_values"
            _imported_values = getattr(self, imported_values_name)

            if _imported_values is None:
                line_edit = getattr(self, f"lineEdit_{label}_table_path")

                _imported_values, _table_path = CommonUserInputs(self).load_table(line_edit, "nodal loads", dof_label=label, direct_load=True)
                setattr(self, imported_values_name, _imported_values)
                setattr(self, table_path_name, _table_path)

            _table_path_attr = getattr(self, table_path_name)
            table_paths.append(_table_path_attr)

        for node_id in node_ids:

            table_names = list()

            for label in load_labels:
                imported_values_name = f"imported_{label}_values"
                _imported_values = getattr(self, imported_values_name)

                _table_name = None
                if isinstance(_imported_values, np.ndarray):
                    _table_name = get_table_name(f"nodal_load_{label}", node_id=node_id)
                    if self.save_table_values(_table_name, _imported_values):
                        return

                table_names.append(_table_name)

            if (table_names).count(None) == 6:
                title = "Additional inputs required"
                message = "You must inform at least one nodal load "
                message += "table path before confirming the input!"
                PrintMessageInput([error_title, title, message])
                return

            node = app().project.model.preprocessor.nodes[node_id]
            coords = np.round(node.coordinates, 5)

            data = {
                "coords" : list(coords),
                "table_names" : table_names,
                "table_paths" : table_paths,
                }

            self.properties._set_nodal_property("nodal_loads", data, node_id)

        app().project.file.write_nodal_properties_in_file()

        self.actions_to_finalize()

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

        self.tabWidget_nodal_loads.setTabVisible(2, False)
        for property, *_ in self.properties.nodal_properties.keys():
            if property == "nodal_loads":
                self.tabWidget_nodal_loads.setCurrentIndex(0)
                self.tabWidget_nodal_loads.setTabVisible(2, True)
                return

    def tab_event_callback(self):

        self.lineEdit_node_ids.clear()
        self.pushButton_remove.setDisabled(True)

        if self.tabWidget_nodal_loads.currentIndex() == 2:
            self.lineEdit_node_ids.setDisabled(True)
            items = self.treeWidget_nodal_info.selectedItems()
            if items == list():
                self.lineEdit_node_ids.clear()
            else:
                self.on_click_item(items[0])

        else:
            self.lineEdit_node_ids.setEnabled(True)
            self.selection_callback()

    def on_click_item(self, item):
        self.pushButton_remove.setDisabled(False)
        if item.text(0) != "":
            self.lineEdit_node_ids.setText(item.text(0))
            node_id = int(item.text(0))
            app().main_window.set_selection(nodes=[node_id])

    def on_double_click_item(self, item):
        # self.on_click_item(item)
        self.lineEdit_node_ids.setText(item.text(0))
        self.get_nodal_info(item)

    def get_nodal_info(self, item):
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

    def remove_properties_from_node(self, node_ids: int | list | tuple):

        if isinstance(node_ids, int):
            node_ids = [node_ids]

        for node_id in node_ids:
            for label in ["prescribed_dofs"]:
                self.properties._remove_nodal_property(label, node_id)

        app().project.file.write_nodal_properties_in_file()

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

        title = "Resetting of prescribed dofs"
        message = (
            "Would you like to remove all prescribed dofs from the structural model?"
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

        self.properties._reset_nodal_property("nodal_loads")
        self.actions_to_finalize()

    def actions_to_finalize(self):
        self.reset_table_variables()
        app().project.file.write_nodal_properties_in_file()
        app().project.file.write_imported_table_data_in_file()
        self.load_nodes_info()
        app().main_window.update_plots(reset_camera=False)

    def reset_input_fields(self):
        self.lineEdit_node_ids.clear()
        for [lineEdit_real, lineEdit_imag] in self.list_lineEdit_constant_values:
            lineEdit_real.clear()
            lineEdit_imag.clear()
        for lineEdit_table in self.list_lineEdit_table_values:
            lineEdit_table.clear()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_nodal_loads.currentIndex() == 0:
                self.constant_values_attribution_callback()
            elif self.tabWidget_nodal_loads.currentIndex() == 1:
                self.table_values_attribution_callback()

        elif event.key() == Qt.Key_Escape:
            self.close()
