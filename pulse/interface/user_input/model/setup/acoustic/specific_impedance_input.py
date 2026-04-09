
from enum import IntEnum

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHeaderView, QLineEdit, QTreeWidgetItem

from pulse import app
from pulse.interface.ui_generated.model.setup.acoustic.acoustic_property_input_ui import (
    AcousticPropertyInput_UI,
)
from pulse.interface.user_input.model.setup.acoustic.acoustic_nodes_input import (
    AcousticNodesInput,
)
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


class SpecificImpedanceInput(AcousticNodesInput, AcousticPropertyInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._initialize()
        self._config_widgets()
        self._create_connections()

        self.selection_callback()
        self.load_nodes_info()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):
        self.table_path = None             
        self.keep_window_open = True

    def _config_widgets(self):
        #
        self.label_bondary_condition.setText("Specific impedance:")
        self.label_unit.setText("[kg/m².s]")
        self.label_title.setText("Specific impedance setup")
        #
        self.treeWidget_nodal_info.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def _create_connections(self):
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_search.clicked.connect(self.load_specific_impedance_table)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_nodal_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_nodal_info.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):
        selected_nodes = app().main_window.list_selected_nodes()

        if selected_nodes:
            text = ", ".join([str(i) for i in selected_nodes])
            self.lineEdit_node_ids.setText(text)

            if len(selected_nodes) != 1:
                return

            for (property, *args), data in self.properties.nodal_properties.items():
                if property != "specific_impedance":
                    continue

                if selected_nodes != args:
                    continue

                if "table_paths" in data.keys():
                    table_paths = data["table_paths"]
                    self.lineEdit_table_path.setText(table_paths[0])

                else:
                    real_value = float(data["real_values"][0])
                    imag_value = float(data["imag_values"][0])
                    self.lineEdit_real_value.setText(str(real_value))
                    self.lineEdit_imag_value.setText(str(imag_value))

    def tab_event_callback(self):
        self.lineEdit_node_ids.clear()
        self.pushButton_remove.setDisabled(True)
        tab_list = self.tabWidget_main.currentIndex() == TabIndex.LIST
        if not tab_list:
            self.selection_callback()

        self.lineEdit_node_ids.setDisabled(tab_list)
        self.pushButton_attribute.setDisabled(tab_list)

    def update_tabs_visibility(self):
        self.tabWidget_main.setTabVisible(TabIndex.LIST, False)
        for property, *_ in self.properties.nodal_properties.keys():
            if property == "specific_impedance":
                self.tabWidget_main.setCurrentIndex(TabIndex.CONSTANT)
                self.tabWidget_main.setTabVisible(TabIndex.LIST, True)
                return

    def load_nodes_info(self):

        self.treeWidget_nodal_info.clear()
        for (property, *args), data in self.properties.nodal_properties.items():
            if property != "specific_impedance":
                continue

            values = data["values"]
            new = QTreeWidgetItem([str(args[0]), str(self.text_label(values[0]))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_nodal_info.addTopLevelItem(new)

        self.update_tabs_visibility()

    def attribute_callback(self):
        properties = ["specific_impedance", "radiation_impedance"]
        input_name = "specific_impedance"
        reset_camera = False

        tab_index = self.tabWidget_main.currentIndex()
        if tab_index == TabIndex.CONSTANT:
            self.constant_values_attribution_callback(
                self.lineEdit_node_ids,
                self.lineEdit_real_value,
                self.lineEdit_imag_value,
                input_name,
                properties,
                reset_camera,
            )
        elif tab_index == TabIndex.TABULAR:
            self.table_values_attribution_callback()

    def are_there_internal_nodes(self, node_ids: list[int]):
        for node_id in node_ids:
            neigh_elements = app().project.model.preprocessor.structural_elements_connected_to_node.get(node_id)
            if isinstance(neigh_elements, list):
                if len(neigh_elements) != 1:
                    self.hide()
                    title = "Internal nodes detected"
                    message = "At least one internal node was detected in the list of "
                    message += "nodes entered. The specific impedances are only allowed "
                    message += "for termination nodes."
                    PrintMessageInput([warning_title, title, message])
                    return True

    def check_complex_entries(self, lineEdit_real: QLineEdit, lineEdit_imag: QLineEdit):

        title = "Invalid entry to the specific impedace"

        if lineEdit_real.text() != "":

            _str_real = lineEdit_real.text()
            str_real = _str_real.replace(",", ".")

            try:
                real_F = float(str_real)
            except Exception:
                self.hide()
                message = "Wrong input for real part of specific impedace."
                PrintMessageInput([error_title, title, message])
                lineEdit_real.setFocus()
                app().main_window.set_input_widget(self)
                return True, None
        else:
            real_F = 0

        if lineEdit_imag.text() != "":

            _str_imag = lineEdit_imag.text()
            str_imag = _str_imag.replace(",", ".")

            try:
                imag_F = float(str_imag)
            except Exception:
                self.hide()
                message = "Wrong input for imaginary part of specific impedace."
                PrintMessageInput([error_title, title, message])
                lineEdit_imag.setFocus()
                app().main_window.set_input_widget(self)
                return True, None
        else:
            imag_F = 0

        if real_F == 0 and imag_F == 0:
            self.hide()
            message = "You must inform at least one specific impedace " 
            message += "before confirming the input!"
            PrintMessageInput([error_title, title, message])
            self.lineEdit_real_value.setFocus()
            app().main_window.set_input_widget(self)
            return True, None

        else:
            return False, real_F + 1j*imag_F

    def constant_values_attribution_callback(self):

        lineEdit = self.lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(lineEdit, "nodes")
        if stop:
            self.lineEdit_node_ids.setFocus()
            return

        if self.are_there_internal_nodes(node_ids):
            return

        stop, specific_impedance = self.check_complex_entries(self.lineEdit_real_value, self.lineEdit_imag_value)
        if stop:
            return

        self.remove_properties_from_node(node_ids)

        real_values = [np.real(specific_impedance)]
        imag_values = [np.imag(specific_impedance)]

        for node_id in node_ids:

            node = app().project.model.preprocessor.nodes[node_id]
            coords = list(np.round(node.coordinates, 5))

            data = {   
                "coords" : coords,
                "real_values": real_values,
                "imag_values": imag_values,
                }

            self.properties._set_nodal_property("specific_impedance", data, node_id)

        self.actions_to_finalize()

    def line_edit_reset(self, line_edit: QLineEdit):
        line_edit.clear()
        line_edit.setFocus()

    def save_table_values(self, table_name: str, imported_values: np.ndarray, filter_zero: bool = True):

        if filter_zero:
            mask_filter = imported_values[:, 0] > 0
            _imported_values = imported_values[mask_filter, :]
        else:
            _imported_values = imported_values

        # define the frequencies vector
        _frequencies = _imported_values[:, 0]

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
        real_values = _imported_values[:, 1]
        
        # imaginary values vector
        imag_values = _imported_values[:, 2]

        # data to be stored
        data = np.array([_frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("acoustic", table_name, data)

        return False

    def load_specific_impedance_table(self):
        self.imported_values, self.table_path = self.load_table(
            self.lineEdit_table_path, 
            "specific impedance",
            )

        if self.table_path is None:
            self.line_edit_reset(self.lineEdit_table_path)

    def table_values_attribution_callback(self):

        str_nodes = self.lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            self.lineEdit_node_ids.setFocus()
            return

        if self.are_there_internal_nodes(node_ids):
            return

        self.remove_properties_from_node(node_ids)

        if self.lineEdit_table_path == "":
            title = "Additional inputs required"
            message = "You must inform at least one specific impedance " 
            message += "table path before confirming the input!"
            PrintMessageInput([error_title, title, message])
            self.lineEdit_table_path.setFocus()
            return

        if self.imported_values is None:
            self.imported_values, self.table_path = self.load_table(
                self.lineEdit_table_path,
                "specific impedance",
                direct_load = True,
                )

            if self.imported_values is None:
                return

        for node_id in node_ids:

            _table_name = None
            if isinstance(self.imported_values, np.ndarray):
                _table_name = self.get_table_name("specific_impedance", node_id=node_id)
                if self.save_table_values(_table_name, self.imported_values):
                    return

            node = app().project.model.preprocessor.nodes[node_id]
            coords = np.round(node.coordinates, 5)

            data = {
                "coords" : list(coords),
                "table_names" : [_table_name],
                "table_paths" : [self.table_path],
                }

            self.properties._set_nodal_property("specific_impedance", data, node_id)

        self.actions_to_finalize()

    def text_label(self, value):
        text = ""
        if isinstance(value, complex):
            value_label = str(value)
        elif isinstance(value, np.ndarray):
            value_label = 'Table'
        text = "{}".format(value_label)
        return text

    def on_click_item(self, item: QTreeWidgetItem):
        self.pushButton_remove.setDisabled(False)
        if item.text(0) != "":
            self.lineEdit_node_ids.setText(item.text(0))
            node_id = int(item.text(0))
            app().main_window.set_selection(nodes=[node_id])

    def on_doubleclick_item(self, item: QTreeWidgetItem):
        self.lineEdit_node_ids.setText(item.text(0))

    def remove_properties_from_node(self, node_ids: int | list):

        if isinstance(node_ids, int):
            node_ids = [node_ids]

        for node_id in node_ids:
            for label in ["specific_impedance", "radiation_impedance"]:
                self.properties._remove_nodal_property(label, node_id)

        app().project.file.write_nodal_properties_in_file()

    def remove_callback(self):

        if  self.lineEdit_node_ids.text() == "":
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

        self.properties._remove_nodal_property("specific_impedance", node_ids)
        self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Resetting of specific impedances"
        message = (
            "Would you like to remove all specific impedances from the acoustic model?"
        )

        buttons_config = {"left_button_label": "No", "right_button_label": "Yes"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        self.properties._reset_nodal_property("specific_impedance")
        self.actions_to_finalize()

    def actions_to_finalize(self):
        app().project.file.write_nodal_properties_in_file()
        app().project.file.write_imported_table_data_in_file()
        app().main_window.update_plots(reset_camera=False)
        self.load_nodes_info()

    def reset_input_fields(self):
        self.lineEdit_node_ids.clear()
        self.lineEdit_real_value.clear()
        self.lineEdit_imag_value.clear()
        self.lineEdit_table_path.clear()