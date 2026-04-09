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


class TabType(IntEnum):
    CONSTANT = 0
    TABULAR = 1
    LIST = 2


error_title = "Error"
warning_title = "Warning"


class AcousticPressureInput(AcousticNodesInput, AcousticPropertyInput_UI):
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
        self.label_bondary_condition.setText("Acoustic pressure:")
        self.label_unit.setText("[Pa]")
        self.label_title.setText("Acoustic pressure prescription setup")
        #
        self.treeWidget_nodal_info.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def _create_connections(self):
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_search.clicked.connect(self.load_acoustic_pressure_table)
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
                if property != "acoustic_pressure":
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
        tab_list = self.tabWidget_main.currentIndex() == TabType.LIST
        if not tab_list:
            self.selection_callback()

        self.lineEdit_node_ids.setDisabled(tab_list)
        self.pushButton_attribute.setDisabled(tab_list)

    def update_tabs_visibility(self):
        self.tabWidget_main.setTabVisible(TabType.LIST, False)
        for property, *_ in self.properties.nodal_properties.keys():
            if property == "acoustic_pressure":
                self.tabWidget_main.setCurrentIndex(TabType.CONSTANT)
                self.tabWidget_main.setTabVisible(TabType.LIST, True)
                return

    def load_nodes_info(self):

        self.treeWidget_nodal_info.clear()
        for (property, *args), data in self.properties.nodal_properties.items():
            if property != "acoustic_pressure":
                continue

            values = data["values"]
            new = QTreeWidgetItem([str(args[0]), str(self.text_label(values[0]))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_nodal_info.addTopLevelItem(new)

        self.update_tabs_visibility()

    def attribute_callback(self):

        tab_index = self.tabWidget_main.currentIndex()      
        if tab_index == TabType.CONSTANT:
            self.constant_values_attribution_callback()

        elif tab_index == TabType.TABULAR:
            self.table_values_attribution_callback()

    def constant_values_attribution_callback(self):

        lineEdit = self.lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(lineEdit, "nodes")
        if stop:
            self.lineEdit_node_ids.setFocus()
            return

        stop, acoustic_pressure = self.check_complex_entries(self.lineEdit_real_value, self.lineEdit_imag_value, "acoustic pressure")

        if stop:
            return

        self.remove_properties_from_node(node_ids)

        real_values = [np.real(acoustic_pressure)]
        imag_values = [np.imag(acoustic_pressure)]

        for node_id in node_ids:

            node = app().project.model.preprocessor.nodes[node_id]
            coords = list(np.round(node.coordinates, 5))

            data = {   
                "coords" : coords,
                "real_values": real_values,
                "imag_values": imag_values,
                }

            self.properties._set_nodal_property("acoustic_pressure", data, node_id)

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
        frequencies = _imported_values[:, 0]

        if app().project.model.change_analysis_frequency_setup(list(frequencies)):
            self.hide()
            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup "
            message += "different from the others already imported ones. The current "
            message += "project frequency setup is not going to be modified."
            message += f"\n\n{table_name}"
            PrintMessageInput([error_title, title, message])
            return True

        self.update_analysis_setup_in_file(frequencies)

        # real values vector
        real_values = _imported_values[:, 1]
        
        # imaginary values vector
        imag_values = _imported_values[:, 2]

        # data to be stored
        data = np.array([frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("acoustic", table_name, data)

        return False

    def load_acoustic_pressure_table(self):
        self.imported_values, self.table_path = self.load_table(
            self.lineEdit_table_path, 
            "acoustic pressure",
            )

        if self.table_path is None:
            self.line_edit_reset(self.lineEdit_table_path)

    def table_values_attribution_callback(self):

        str_nodes = self.lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            self.lineEdit_node_ids.setFocus()
            return

        self.remove_properties_from_node(node_ids)

        if self.lineEdit_table_path == "":
            title = "Additional inputs required"
            message = "You must inform at least one acoustic pressure " 
            message += "table path before confirming the input!"
            PrintMessageInput([error_title, title, message])
            self.lineEdit_table_path.setFocus()
            return
    
        if self.imported_values is None:
            self.imported_values, self.table_path = self.load_table(
                self.lineEdit_table_path,
                "acoustic pressure",
                direct_load = True,
                )

            if self.imported_values is None:
                return

        for node_id in node_ids:

            _table_name = None
            if isinstance(self.imported_values, np.ndarray):
                _table_name = self.get_table_name("acoustic_pressure", node_id=node_id)
                if self.save_table_values(_table_name, self.imported_values):
                    return

            node = app().project.model.preprocessor.nodes[node_id]
            coords = np.round(node.coordinates, 5)

            data = {
                "coords" : list(coords),
                "table_names" : [_table_name],
                "table_paths" : [self.table_path],
                }

            self.properties._set_nodal_property("acoustic_pressure", data, node_id)

        self.actions_to_finalize()

    def text_label(self, value):
        text = ""
        if isinstance(value, complex):
            value_label = str(value)
        elif isinstance(value, np.ndarray):
            value_label = 'Table'
        text = "{}".format(value_label)
        return text

    def on_click_item(self, item):
        self.pushButton_remove.setDisabled(False)
        if item.text(0) != "":
            self.lineEdit_node_ids.setText(item.text(0))
            node_id = int(item.text(0))
            app().main_window.set_selection(nodes=[node_id])

    def on_doubleclick_item(self, item):
        self.lineEdit_node_ids.setText(item.text(0))

    def remove_properties_from_node(self, node_ids: int | list):

        if isinstance(node_ids, int):
            node_ids = [node_ids]

        for node_id in node_ids:
            for label in ["acoustic_pressure", "volume_velocity", "reciprocating_compressor_excitation", "reciprocating_pump_excitation"]:
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

        self.properties._remove_nodal_property("acoustic_pressure", node_ids)
        self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Resetting of acoustic pressures"
        message = "Would you like to remove all acoustic pressures from the acoustic model?"

        buttons_config = {"left_button_label" : "No", "right_button_label" : "Yes"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        self.properties._reset_nodal_property("acoustic_pressure")
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