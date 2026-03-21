# fmt: off

from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt, QEvent, QObject, Signal

from pulse import app
from pulse.interface.ui_generated.model.setup.acoustic.acoustic_transfer_element_input_ui import AcousticTransferElementInput_UI
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.interface.user_input.data_handler.file_managers.file_manager import FileManager
from pulse.interface.user_input.data_handler.file_dialog_service import FileDialogService



import os
import numpy as np
from pathlib import Path


error_title = "Error"
warning_title = "Warning"


class AddAcousticTransferElementInput(AcousticTransferElementInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties
        self.preprocessor = app().project.model.preprocessor

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        # self._config_widgets()
        self.load_nodal_info()
        self.selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.keep_window_open = True
        self.element_transfer_data = dict()

        self.before_run = app().project.get_pre_solution_model_checks()
    
    def _define_qt_variables(self):
        self.current_lineEdit = self.lineEdit_output_node_id


    def _create_connections(self):
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_invert_selection.clicked.connect(self.invert_selection_callback)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_search.clicked.connect(self.search_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_nodal_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_nodal_info.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        self.clickable(self.lineEdit_input_node_id).connect(self.lineEdit_1_clicked)
        self.clickable(self.lineEdit_output_node_id).connect(self.lineEdit_2_clicked)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):
        selected_nodes = selected_nodes = app().main_window.list_selected_nodes()
        if selected_nodes:
            if len(selected_nodes) == 1:
                node_id = selected_nodes[0]
                self.current_lineEdit.setText(str(node_id))                

    def clickable(self, widget):
        class Filter(QObject):
            clicked = Signal()

            def eventFilter(self, obj, event):
                if obj == widget and event.type() == QEvent.MouseButtonRelease and obj.rect().contains(event.pos()):
                    self.clicked.emit()
                    return True
                else:
                    return False

        filter = Filter(widget)
        widget.installEventFilter(filter)

        return filter.clicked

    def lineEdit_1_clicked(self):
        self.current_lineEdit = self.lineEdit_input_node_id

    def lineEdit_2_clicked(self):
        self.current_lineEdit = self.lineEdit_output_node_id

    def invert_selection_callback(self):
        temp_text_input = self.lineEdit_input_node_id.text()
        temp_text_output = self.lineEdit_output_node_id.text()
        self.lineEdit_input_node_id.setText(temp_text_output)
        self.lineEdit_output_node_id.setText(temp_text_input) 

    def attribute_callback(self):

        path = self.lineEdit_spreadsheet_path.text()

        if not path:
            if self.search_callback():
                return
            
        if self.check_inputs():
            return

        if os.path.exists(path):

            try:
                self.import_element_transfer_data(path)

                if self.element_transfer_data:
                    self.process_acoustic_element_transfer_data(path)
                    self.actions_to_finalize()

            except Exception as error_log:
                self.hide()
                title = "Invalid data imported"
                message = "An invalid data has been imported to the acoustic transfer element. "
                message += "Check the acoustic element transfer data type and modify it if necessary."
                PrintMessageInput([error_title, title, message])
                return

    def remove_callback(self):

        if  self.lineEdit_selected_id.text() == "":
            self.hide()
            title = "Invalid selection"
            message = "You should to select an item from the list "
            message += "to proceed with the removal."
            PrintMessageInput([warning_title, title, message])
            return

        linked_nodes = self.lineEdit_selected_id.text()
        node_ids = [int(node_id) for node_id in linked_nodes.split("-")]

        self.properties._remove_nodal_property("acoustic_transfer_element", node_ids)
        self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = f"Resetting of acoustic transfer element"
        message = "Would you like to remove all acoustic transfer element from the acoustic model?"

        buttons_config = {"left_button_label" : "No", "right_button_label" : "Yes"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        self.properties._reset_nodal_property("acoustic_transfer_element")
        self.actions_to_finalize()

    def search_callback(self):
        caption = f"Choose a file to import element transfer data"
        last_folder = app().config.get_last_folder_for("imported_table_folder")
        file_extensions = ["xls", "xlsx"]
    
        imported_path = FileDialogService.open_file(file_extensions, caption=caption, last_folder=last_folder)

        if not imported_path:
            info_message = "Select the spreadsheet file to import "
            info_message += "the acoustic transfer element data."
            self.lineEdit_spreadsheet_path.setToolTip(info_message)
            return True
        
        path = str(imported_path)
        self.lineEdit_spreadsheet_path.setText(path)
        self.lineEdit_spreadsheet_path.setToolTip(path)

        app().config.write_last_folder_path_in_file("imported_table_folder", path)

    def check_inputs(self):

        input_node_id = self.lineEdit_input_node_id.text()
        stop, self.input_node_id = self.before_run.check_selected_ids(input_node_id, "nodes", single_id=True)
        if stop:
            self.lineEdit_input_node_id.setFocus()
            return True
        
        output_node_id = self.lineEdit_output_node_id.text()
        stop, self.output_node_id = self.before_run.check_selected_ids(output_node_id, "nodes", single_id=True)
        if stop:
            self.lineEdit_output_node_id.setFocus()
            return True

    def import_element_transfer_data(self, imported_path: str):
        self.element_transfer_data.clear()
    
        imported_file = FileManager().read_text_file(imported_path)

        for sheet in imported_file.sheets:
            if sheet.name:
                self.element_transfer_data[sheet.name] = sheet.data

    def update_frequency_setup(self, frequencies: np.ndarray, path: str):

        if app().project.model.change_analysis_frequency_setup(list(frequencies)):

            self.lineEdit_spreadsheet_path.setText("")

            title = "Project frequency setup cannot be modified"
            message = f"The following imported table of values has a frequency setup\n"
            message += "different from the others already imported ones. The current\n"
            message += "project frequency setup is not going to be modified."
            message += f"\n\n{os.path.basename(path)}"
            PrintMessageInput([error_title, title, message])
            return None, None

        else:

            analysis_setup = app().project.model.analysis_setup
            app().project.file.write_analysis_setup_in_file(analysis_setup)

    def process_acoustic_element_transfer_data(self, path: str):

        aux = dict()
        table_names = list()
        linked_nodes = f"{self.input_node_id}_{self.output_node_id}"

        self.aij_labels = ["a11", "a21", "a12", "a22"]
        self.hij_labels = ["h11", "h21", "h12", "h22"]

        for k, (sheetname, et_data) in enumerate(self.element_transfer_data.items()):

            if not isinstance(et_data, np.ndarray):
                continue

            freq_mask = et_data[:, 0] > 0
            _et_data = et_data[freq_mask, :]

            if k == 0:
                self.update_frequency_setup(_et_data[:, 0], path)

            if self.comboBox_data_type.currentIndex() == 1:                 
                if et_data.shape[1] == 9:
                    for i, aij_label in enumerate(self.aij_labels):

                        data_ij = np.array([
                            _et_data[:, 0], 
                            _et_data[:, 2*i+1], 
                            _et_data[:, 2*i+2]
                            ], dtype=float).T

                        table_name = f"admittance_matrix_data_{aij_label}_nodes_{linked_nodes}"
                        aux[aij_label] = {
                            "values" : data_ij,
                            "table_name" : table_name,
                            }

                elif et_data.shape[1] in [3, 4]:
                    for aij_abel in self.aij_labels:
                        if aij_abel in sheetname:
                            table_name = f"admittance_matrix_data_{aij_abel}_nodes_{linked_nodes}"
                            aux[aij_abel] = {
                                "values" : data_ij,
                                "table_name" : table_name,
                                }
                            break

            else:

                for hij_label in self.hij_labels:
                    if hij_label in sheetname:
                        table_name = f"transfer_function_{hij_label}_nodes_{linked_nodes}"
                        aux[hij_label] = {
                            "values" : et_data,
                            "table_name" : table_name,
                            }

        for _data in aux.values():
            values = _data["values"]
            table_name = _data["table_name"]
            self.properties.add_imported_tables("acoustic", table_name, values)

        coords = list()
        node_ids = [self.input_node_id, self.output_node_id]
        for node_id in node_ids:
            node = app().project.model.preprocessor.nodes[node_id]
            coords.extend(list(np.round(node.coordinates, 5)))

        table_names = list()

        if self.comboBox_data_type.currentIndex() == 0:
            data_source = "transfer_functions"
            for key in self.hij_labels:
                table_names.append(aux[key]["table_name"])

        else:
            data_source = "admittance_matrix"
            for key in self.aij_labels:
                table_names.append(aux[key]["table_name"])

        data = {
            "coords" : coords,
            "table_names" : table_names,
            "table_paths" : [path],
            "element_transfer_data_source" : data_source,
            }

        self.properties._set_nodal_property("acoustic_transfer_element", data, node_ids)

    def actions_to_finalize(self):
        app().project.file.write_nodal_properties_in_file()
        app().project.file.write_imported_table_data_in_file()
        app().main_window.update_plots(reset_camera=False)
        self.load_nodal_info()

    def on_click_item(self, item):
        input_node_id = int(item.text(1))
        output_node_id = int(item.text(2))
        self.pushButton_remove.setEnabled(True)
        self.lineEdit_selected_id.setText(f"{input_node_id}-{output_node_id}")
        app().main_window.set_selection(nodes=(input_node_id, output_node_id))

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

    def tab_event_callback(self):
        self.lineEdit_selected_id.setText("")
        self.pushButton_remove.setDisabled(True)
        # if self.tabWidget_main.currentIndex() == 1:
        #     self.lineEdit_selected_id.setText("")
        # else:
        #     self.selection_callback()

    def load_nodal_info(self):

        index = 0
        self.treeWidget_nodal_info.clear()

        for (property, *args), data in self.properties.nodal_properties.items():
            if property == "acoustic_transfer_element":
                if "values" in data.keys():
                    index += 1
                    new = QTreeWidgetItem([str(index), str(args[0]), str(args[1])])
                    for i in range(3):
                        new.setTextAlignment(i, Qt.AlignCenter)
                    self.treeWidget_nodal_info.addTopLevelItem(new)

        self.tabWidget_main.setTabVisible(1, False)
        for (_property, *_) in self.properties.nodal_properties.keys():
            if _property == "acoustic_transfer_element":
                self.tabWidget_main.setCurrentIndex(0)
                self.tabWidget_main.setTabVisible(1, True)
                return

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

# fmt: on