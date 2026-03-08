from PySide6.QtWidgets import QLineEdit, QTreeWidgetItem
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt

from pulse import app
from pulse.interface.ui_generated.model.setup.acoustic.volume_velocity_input_ui import VolumeVelocityInput_UI
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.interface.user_input.common import CommonUserInputs, get_table_name, update_analysis_setup_in_file


import os
import numpy as np
from pathlib import Path

error_title = "Error"


class VolumeVelocityInput(VolumeVelocityInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties

        self._initialize()
        self._config_window()
        self._config_widgets()
        self._create_connections()

        self.selection_callback()
        self.load_nodes_info()
        
        while self.keep_window_open:
            self.exec()

    def _initialize(self):

        self.array = None
        self.table_name = None
        self.table_path = None
        self.table_values = None                

        self.keep_window_open = True

        self.before_run = app().project.get_pre_solution_model_checks()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _config_widgets(self):
        for i, width in enumerate([120]):
            self.treeWidget_nodal_info.setColumnWidth(i, width)

    def _create_connections(self):
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_search.clicked.connect(self.load_volume_velocity_table)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_nodal_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_nodal_info.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        self.reset_input_fields()
        selected_nodes = app().main_window.list_selected_nodes()

        if selected_nodes:
            text = ", ".join([str(i) for i in selected_nodes])
            self.lineEdit_node_ids.setText(text)

            if len(selected_nodes) == 1:
                for (property, *args), data in self.properties.nodal_properties.items():
                    if property == "volume_velocity" and selected_nodes == args:

                        if "table_paths" in data.keys():
                            table_paths = data["table_paths"]
                            self.lineEdit_table_path.setText(table_paths[0])
                        else:
                            real_value = float(data["real_values"][0])
                            imag_value = float(data["imag_values"][0])
                            self.lineEdit_real_value.setText(str(real_value))
                            self.lineEdit_imag_value.setText(str(imag_value))

    def tab_event_callback(self):
        self.lineEdit_node_ids.setText("")
        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_main.currentIndex() == 1:
            self.lineEdit_node_ids.setText("")
            self.lineEdit_node_ids.setDisabled(True)
        else:
            self.selection_callback()
            self.lineEdit_node_ids.setDisabled(False)

    def update_tabs_visibility(self):
        self.tabWidget_main.setTabVisible(1, False)
        for (property, *_) in self.properties.nodal_properties.keys():
            if property == "volume_velocity":
                self.tabWidget_main.setCurrentIndex(0)
                self.tabWidget_main.setTabVisible(1, True)
                return

    def load_nodes_info(self):

        self.treeWidget_nodal_info.clear()
        for (property, *args), data in self.properties.nodal_properties.items():

            if property == "volume_velocity":
                values = data["values"]
                new = QTreeWidgetItem([str(args[0]), str(self.text_label(values[0]))])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_nodal_info.addTopLevelItem(new)

        self.update_tabs_visibility()

    def attribute_callback(self):
        if self.tabWidget_inputs.currentIndex() == 0:
            self.constant_values_attribution_callback()
        else:
            self.table_values_attribution_callback()

    def check_complex_entries(self, lineEdit_real: QLineEdit, lineEdit_imag: QLineEdit):

        title = "Invalid entry to the volume velocity"

        if lineEdit_real.text() != "":

            _str_real = lineEdit_real.text()
            str_real = _str_real.replace(",", ".")

            try:
                real_F = float(str_real)
            except Exception:
                self.hide()
                message = "Wrong input for real part of volume velocity."
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
                message = "Wrong input for imaginary part of volume velocity."
                PrintMessageInput([error_title, title, message])
                lineEdit_imag.setFocus()
                app().main_window.set_input_widget(self)
                return True, None
        else:
            imag_F = 0

        if real_F == 0 and imag_F == 0:
            self.hide()
            message = "You must inform at least one volume velocity " 
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

        stop, volume_velocity = self.check_complex_entries(self.lineEdit_real_value, self.lineEdit_imag_value)

        if stop:
            return

        self.remove_conflicting_excitations(node_ids)

        real_values = [np.real(volume_velocity)]
        imag_values = [np.imag(volume_velocity)]

        for node_id in node_ids:

            node = app().project.model.preprocessor.nodes[node_id]
            coords = list(np.round(node.coordinates, 5))

            data = {   
                "coords" : coords,
                "real_values": real_values,
                "imag_values": imag_values,
                }

            self.properties._set_nodal_property("volume_velocity", data, node_id)

        self.actions_to_finalize()

    def lineEdit_reset(self, line_edit: QLineEdit):
        line_edit.setText("")
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

        update_analysis_setup_in_file(frequencies)

        # real values vector
        real_values = _imported_values[:, 1]
        
        # imaginary values vector
        imag_values = _imported_values[:, 2]

        # data to be stored
        data = np.array([frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("acoustic", table_name, data)

        return False

    def load_volume_velocity_table(self):
        self.imported_values, self.table_path = CommonUserInputs().load_table(self.lineEdit_table_path, "volume velocity")
        if self.table_path is None:
            self.lineEdit_reset(self.lineEdit_table_path)

    def table_values_attribution_callback(self):

        str_nodes = self.lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            self.lineEdit_node_ids.setFocus()
            return

        self.remove_conflicting_excitations(node_ids)

        if self.lineEdit_table_path == "":
            self.hide()
            title = "Additional inputs required"
            message = "You must inform at least one volume velocity " 
            message += "table path before confirming the input!"
            PrintMessageInput([error_title, title, message])
            self.lineEdit_table_path.setFocus()
            return
    
        if self.table_path is None:
            self.table_values, self.table_path = CommonUserInputs().load_table(
                                                                    self.lineEdit_table_path,
                                                                    direct_load=True,
                                                                    )

            if self.table_values is None:
                return

        for node_id in node_ids:

            _table_name = None
            if isinstance(self.imported_values, np.ndarray):
                _table_name = get_table_name("volume_velocity", node_id)
                if self.save_table_values(_table_name, self.imported_values):
                    return

            node = app().project.model.preprocessor.nodes[node_id]
            coords = np.round(node.coordinates, 5)

            data = {
                "coords" : list(coords),
                "table_names" : [_table_name],
                "table_paths" : [self.table_path],
                }

            self.properties._set_nodal_property("volume_velocity", data, node_id)

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

    def remove_conflicting_excitations(self, node_ids: int | list | tuple):

        if isinstance(node_ids, int):
            node_ids = [node_ids]

        for node_id in node_ids:
            for label in ["acoustic_pressure", "reciprocating_compressor_excitation", "reciprocating_pump_excitation", "volume_velocity"]:
                table_names = self.properties.get_nodal_related_table_names(label, node_id)

                self.properties._remove_nodal_property(label, node_id)
                self.process_table_file_removal(table_names)

        app().project.file.write_nodal_properties_in_file()

    def remove_table_files_from_nodes(self, node_ids : list):
        table_names = self.properties.get_nodal_related_table_names("volume_velocity", node_ids)
        self.process_table_file_removal(table_names)

    def process_table_file_removal(self, table_names : list):
        if table_names:
            for table_name in table_names:
                self.properties.remove_imported_tables("acoustic", table_name)
            app().project.file.write_imported_table_data_in_file()

    def remove_callback(self):

        if  self.lineEdit_node_ids.text() != "":

            str_nodes = self.lineEdit_node_ids.text()
            stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
            if stop:
                return

            self.remove_table_files_from_nodes(node_ids[0])
            self.properties._remove_nodal_property("volume_velocity", node_ids[0])
            self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = f"Resetting of volume velocities"
        message = "Would you like to remove all volume velocities from the acoustic model?"

        buttons_config = {"left_button_label" : "No", "right_button_label" : "Yes"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            node_ids = list()
            for (property, *args) in self.properties.nodal_properties.keys():
                if property == "volume_velocity":
                    node_ids.append(args[0])
            
            for node_id in node_ids:
                self.remove_table_files_from_nodes(node_id)

            self.properties._reset_nodal_property("volume_velocity")
            self.actions_to_finalize()

    def actions_to_finalize(self):
        app().project.file.write_nodal_properties_in_file()
        app().project.file.write_imported_table_data_in_file()
        app().main_window.update_plots(reset_camera=False)
        self.load_nodes_info()

    def reset_input_fields(self):
        self.lineEdit_node_ids.setText("")
        self.lineEdit_real_value.setText("")
        self.lineEdit_imag_value.setText("")
        self.lineEdit_table_path.setText("")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        app().main_window.selection_changed.disconnect(self.selection_callback)
        return super().closeEvent(a0)