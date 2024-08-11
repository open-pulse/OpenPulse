from PyQt5.QtWidgets import QDialog, QFileDialog, QLineEdit, QPushButton, QSpinBox, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QCloseEvent, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.tools.utils import get_new_path, remove_bc_from_file

import os
import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

class AcousticPressureInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/acoustic_pressure_input.ui"
        uic.loadUi(ui_path, self)

        self.project = app().main_window.project
        app().main_window.set_input_widget(self)

        self._initialize()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()

        ConfigWidgetAppearance(self, tool_tip=True)

        self.selection_callback()
        self.load_nodes_info()

        while self.keep_window_open:
            self.exec()

    def _initialize(self):

        self.keep_window_open = True

        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()

        self.user_path = os.path.expanduser('~')
        self.new_load_path_table = ""
        self.acoustic_bc_info_path = self.project.file._node_acoustic_path  
        self.acoustic_folder_path = self.project.file._acoustic_imported_data_folder_path
        self.acoustic_pressure_tables_folder_path = get_new_path(self.acoustic_folder_path, "acoustic_pressure_files")   
        
        self.nodes_typed = []
        self.inputs_from_node = False
        self.remove_acoustic_pressure = False
        self.acoustic_pressure = None
        self.list_Nones = [None, None, None, None, None, None]

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QLineEdit
        self.lineEdit_imag_value : QLineEdit
        self.lineEdit_real_value : QLineEdit
        self.lineEdit_selection_id : QLineEdit
        self.lineEdit_table_path : QLineEdit

        # QPushButton
        self.constant_value_confirm_button : QPushButton
        self.remove_button : QPushButton
        self.reset_button : QPushButton
        self.search_button : QPushButton
        self.table_values_confirm_button : QPushButton

        # QSpinBox
        self.spinBox_skip_wors : QSpinBox

        # QTabWidget
        self.tabWidget_acoustic_pressure : QTabWidget

        # QTreeWidget
        self.treeWidget_acoustic_pressure : QTreeWidget
        self.treeWidget_acoustic_pressure.setColumnWidth(1, 20)
        self.treeWidget_acoustic_pressure.setColumnWidth(2, 80)

    def _create_connections(self):
        #
        self.constant_value_confirm_button.clicked.connect(self.check_constant_values)
        self.remove_button.clicked.connect(self.remove_bc_from_node)
        self.reset_button.clicked.connect(self.reset_callback)
        self.table_values_confirm_button.clicked.connect(self.check_table_values)
        self.search_button.clicked.connect(self.load_acoustic_pressure_table)
        #
        self.tabWidget_acoustic_pressure.currentChanged.connect(self.tabEvent_acoustic_pressure)
        #
        self.treeWidget_acoustic_pressure.itemClicked.connect(self.on_click_item)
        self.treeWidget_acoustic_pressure.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        selected_nodes = app().main_window.list_selected_nodes()

        if selected_nodes:

            text = ", ".join([str(i) for i in selected_nodes])
            self.lineEdit_selection_id.setText(text)

            picked_node = selected_nodes[0]
            node = self.preprocessor.nodes[picked_node]

            if node.acoustic_pressure is not None:
                self.reset_input_fields(force_reset=True)
                if node.compressor_excitation_table_names == []:
                    if node.acoustic_pressure_table_name is not None:
                        table_name = node.acoustic_pressure_table_name
                        self.tabWidget_acoustic_pressure.setCurrentIndex(1)
                        table_name = get_new_path(self.acoustic_pressure_tables_folder_path, table_name)
                        self.lineEdit_table_path.setText(table_name)
                    else:
                        acoustic_pressure = node.acoustic_pressure
                        self.tabWidget_acoustic_pressure.setCurrentIndex(0)
                        self.lineEdit_real_value.setText(str(np.real(acoustic_pressure)))
                        self.lineEdit_imag_value.setText(str(np.imag(acoustic_pressure)))
                    self.inputs_from_node = True
            else:
                self.reset_input_fields()

    def tabEvent_acoustic_pressure(self):
        self.remove_button.setDisabled(True)
        if self.tabWidget_acoustic_pressure.currentIndex() == 2:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
        else:
            self.selection_callback()
            self.lineEdit_selection_id.setDisabled(False)

    def load_nodes_info(self):
        self.treeWidget_acoustic_pressure.clear()
        for node in self.preprocessor.nodes_with_acoustic_pressure:
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(node.acoustic_pressure))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_acoustic_pressure.addTopLevelItem(new)
        self.update_tabs_visibility()

    def check_complex_entries(self, lineEdit_real, lineEdit_imag):

        self.stop = False
        title = "Invalid entry to the acoustic pressure"
        if lineEdit_real.text() != "":
            try:
                real_F = float(lineEdit_real.text())
            except Exception:
                message = "Wrong input for real part of acoustic pressure."
                PrintMessageInput([window_title_1, title, message])
                self.lineEdit_real_value.setFocus()
                self.stop = True
                return
        else:
            real_F = 0

        if lineEdit_imag.text() != "":
            try:
                imag_F = float(lineEdit_imag.text())
            except Exception:
                message = "Wrong input for imaginary part of acoustic pressure."
                PrintMessageInput([window_title_1, title, message])
                self.lineEdit_imag_value.setFocus()
                self.stop = True
                return
        else:
            imag_F = 0
        
        if real_F == 0 and imag_F == 0:
            return None
        else:
            return real_F + 1j*imag_F

    def check_constant_values(self):

        lineEdit = self.lineEdit_selection_id.text()
        self.stop, self.nodes_typed = self.before_run.check_selected_ids(lineEdit, "nodes")
        if self.stop:
            self.lineEdit_selection_id.setFocus()
            return

        self.project.remove_volume_velocity_table_files(self.nodes_typed)
        self.project.remove_compressor_excitation_table_files(self.nodes_typed)
        self.project.reset_compressor_info_by_node(self.nodes_typed)

        acoustic_pressure = self.check_complex_entries(self.lineEdit_real_value, self.lineEdit_imag_value)

        if self.stop:
            return

        if acoustic_pressure is not None:

            self.acoustic_pressure = acoustic_pressure
            data = [self.acoustic_pressure, None]

            list_table_names = self.get_list_table_names_from_selected_nodes(self.nodes_typed)
            self.process_table_file_removal(list_table_names)

            if self.preprocessor.set_acoustic_pressure_bc_by_node(self.nodes_typed, data):
                return

            real_values = [np.real(acoustic_pressure)]
            imag_values = [np.imag(acoustic_pressure)]

            for node_id in self.nodes_typed:

                node = self.preprocessor.nodes[node_id]
                coords = list(np.round(node.coordinates, 5))

                prop_data = {   
                                "coords" : coords,
                                "real_values": real_values,
                                "imag_values": imag_values,
                            }

                self.project.model.properties.set_acoustic_pressure("acoustic pressure", prop_data, node_id)

            app().pulse_file.write_model_properties_in_file()
            app().main_window.update_plots()

            print(f"[Set Acoustic Pressure] - defined at node(s) {self.nodes_typed}")
            self.close()
        
        else:    
            title = "Additional inputs required"
            message = "You must inform at least one acoustic pressure " 
            message += "before confirming the input!"
            PrintMessageInput([window_title_1, title, message])
            self.lineEdit_real_value.setFocus()
            
    def load_table(self, lineEdit, direct_load=False):
        try:

            if direct_load:
                self.path_imported_table = lineEdit.text()
            else:
                window_label = 'Choose a table to import the acoustic pressure'
                self.path_imported_table, _ = QFileDialog.getOpenFileName(  None, 
                                                                            window_label, 
                                                                            self.user_path, 
                                                                            'Files (*.csv; *.dat; *.txt)'  )

            if self.path_imported_table == "":
                return None, None

            imported_filename = os.path.basename(self.path_imported_table)
            lineEdit.setText(self.path_imported_table)
                       
            imported_file = np.loadtxt(self.path_imported_table, delimiter=",")

            title = "Error reached while loading 'acoustic pressure' table"
            if imported_file.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum"
                message += " data must have only two columns to the frequencies and values."
                PrintMessageInput([window_title_1, title, message])
                return None, None
        
            imported_values = imported_file[:,1]

            if imported_file.shape[1] >= 3:

                self.frequencies = imported_file[:,0]
                self.f_min = self.frequencies[0]
                self.f_max = self.frequencies[-1]
                self.f_step = self.frequencies[1] - self.frequencies[0] 
               
                if self.project.change_project_frequency_setup(imported_filename, list(self.frequencies)):
                    self.lineEdit_reset(self.lineEdit_table_path)
                    return None, None
                else:
                    self.project.set_frequencies(self.frequencies, self.f_min, self.f_max, self.f_step)

            return imported_values, imported_filename

        except Exception as log_error:
            title = "Error reached while loading 'volume velocity' table"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            lineEdit.setFocus()
            return None, None

    def lineEdit_reset(self, lineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()

    def save_table_file(self, node_id, values, filename):
        try:

            self.project.create_folders_acoustic("acoustic_pressure_files")
        
            real_values = np.real(values)
            imag_values = np.imag(values)
            abs_values = np.abs(values)
            data = np.array([self.frequencies, real_values, imag_values, abs_values]).T

            header = f"OpenPulse - imported table for acoustic pressure @ node {node_id}\n"
            header += f"\nSource filename: {filename}\n"
            header += "\nFrequency [Hz], real[Pa], imaginary[Pa], absolute[Pa]"
            basename = f"acoustic_pressure_node_{node_id}.dat"
             
            new_path_table = get_new_path(self.acoustic_pressure_tables_folder_path, basename)
            np.savetxt(new_path_table, data, delimiter=",", header=header)
            return values, basename

        except Exception as log_error:
            title = "Error reached while saving table files"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            return None, None

    def load_acoustic_pressure_table(self):
        self.imported_values, self.filename_acoustic_pressure = self.load_table(self.lineEdit_table_path)
    
    def check_table_values(self):

        str_nodes = self.lineEdit_selection_id.text()
        self.stop, self.nodes_typed = self.before_run.check_selected_ids(str_nodes, "nodes")
        if self.stop:
            self.lineEdit_selection_id.setFocus()
            return

        self.project.remove_volume_velocity_table_files(self.nodes_typed)
        self.project.reset_compressor_info_by_node(self.nodes_typed)

        list_table_names = self.get_list_table_names_from_selected_nodes(self.nodes_typed)
        if self.lineEdit_table_path != "":

            if self.filename_acoustic_pressure is None:
                self.imported_values, self.filename_acoustic_pressure = self.load_table(self.lineEdit_table_path, 
                                                                                        direct_load=True)

            if self.imported_values is None:
                return

            else:
                self.acoustic_pressure, self.basename_acoustic_pressure = self.save_table_file( node_id, 
                                                                                                self.imported_values, 
                                                                                                self.filename_acoustic_pressure )
                if self.basename_acoustic_pressure in list_table_names:
                    list_table_names.remove(self.basename_acoustic_pressure)

                data = [self.acoustic_pressure, self.basename_acoustic_pressure]

                if self.preprocessor.set_acoustic_pressure_bc_by_node(self.nodes_typed, data):
                    return

            for node_id in self.nodes_typed:

                node = self.preprocessor.nodes[node_id]
                coords = list(node.coordinates)

                real_values = list(self.imported_values[:, 0])
                imag_values = list(self.imported_values[:, 1])

                prop_data = {
                                "coords" : coords,
                                "real_values": real_values,
                                "imag_values": imag_values,
                                "table_path": self.path_imported_table,
                            }

                self.project.model.properties.set_acoustic_pressure("acoustic pressure", prop_data, node_id)

            self.process_table_file_removal(list_table_names)
            app().pulse_file.write_model_properties_in_file()
            app().main_window.update_plots()

            print(f"[Set Acoustic Pressure] - defined at node(s) {self.nodes_typed}")   
            self.close()

        else:
            title = "Additional inputs required"
            message = "You must inform at least one acoustic pressure " 
            message += "table path before confirming the input!"
            PrintMessageInput([window_title_1, title, message])
            self.lineEdit_table_path.setFocus()

    def get_list_table_names_from_selected_nodes(self, list_node_ids):
        list_table_names = []
        for node_id in list_node_ids:
            node = self.preprocessor.nodes[node_id]
            if node.acoustic_pressure_table_name is not None:
                table_name = node.acoustic_pressure_table_name
                if table_name not in list_table_names:
                    list_table_names.append(table_name)
        return list_table_names

    def text_label(self, value):
        text = ""
        if isinstance(value, complex):
            value_label = str(value)
        elif isinstance(value, np.ndarray):
            value_label = 'Table'
        text = "{}".format(value_label)
        return text

    def on_click_item(self, item):
        self.remove_button.setDisabled(False)
        self.lineEdit_selection_id.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_selection_id.setText(item.text(0))
        self.remove_bc_from_node()

    def remove_bc_from_node(self):
        if self.lineEdit_selection_id.text() != "":

            str_nodes = self.lineEdit_selection_id.text()
            stop, nodes_typed = self.before_run.check_selected_ids(str_nodes, "nodes")
            if stop:
                return

            key_strings = ["acoustic pressure"]
            self.project.file.filter_bc_data_from_dat_file(nodes_typed, key_strings, self.acoustic_bc_info_path)
            list_table_names = self.get_list_table_names_from_selected_nodes(nodes_typed)
            self.preprocessor.set_acoustic_pressure_bc_by_node(nodes_typed, [None, None])
            self.process_table_file_removal(list_table_names)

            self.lineEdit_selection_id.setText("")
            self.remove_button.setDisabled(True)
            self.load_nodes_info()
            app().main_window.update_plots()
            # self.close()

    def process_table_file_removal(self, list_table_names):
        if list_table_names != []:
            for table_name in list_table_names:
                self.project.remove_acoustic_table_files_from_folder(table_name, "acoustic_pressure_files")

    def reset_callback(self):
        if self.preprocessor.nodes_with_acoustic_pressure:

            list_nodes = list()
            for node in self.preprocessor.nodes_with_acoustic_pressure:
                list_nodes.append(node.external_index)
            
            self.hide()

            title = f"Resetting of acoustic pressures"
            message = "Would you like to remove all acoustic pressures from the acoustic model?"
            
            buttons_config = {"left_button_label" : "No", "right_button_label" : "Yes"}
            read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

            if read._cancel:
                return
            
            if read._continue:

                _node_ids = list()
                _list_table_names = list()
                _nodes_with_acoustic_pressure = self.preprocessor.nodes_with_acoustic_pressure.copy()
                
                for node in _nodes_with_acoustic_pressure:

                    node_id = node.external_index
                    key_strings = ["acoustic pressure"]
                    table_name = node.acoustic_pressure_table_name

                    if table_name is not None:
                        if table_name not in _list_table_names:
                            _list_table_names.append(table_name)

                    if node_id not in _node_ids:
                        _node_ids.append(node_id)

                self.project.file.filter_bc_data_from_dat_file(_node_ids, key_strings, self.acoustic_bc_info_path)
                self.preprocessor.set_acoustic_pressure_bc_by_node(_node_ids, [None, None])
                self.process_table_file_removal(_list_table_names)

                self.close()
                app().main_window.update_plots()

    def reset_input_fields(self, force_reset=False):
        if self.inputs_from_node or force_reset:
            self.lineEdit_real_value.setText("")
            self.lineEdit_imag_value.setText("")
            self.lineEdit_table_path.setText("")
            self.inputs_from_node = False

    def update_tabs_visibility(self):
        if len(self.preprocessor.nodes_with_acoustic_pressure) == 0:
            self.tabWidget_acoustic_pressure.setCurrentIndex(0)
            self.tabWidget_acoustic_pressure.setTabVisible(2, False)
        else:
            self.tabWidget_acoustic_pressure.setTabVisible(2, True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_acoustic_pressure.currentIndex()==0:
                self.check_constant_values()
            if self.tabWidget_acoustic_pressure.currentIndex()==1:
                self.check_table_values()
        elif event.key() == Qt.Key_Delete:
            if self.tabWidget_acoustic_pressure.currentIndex()==2:
                self.remove_bc_from_node()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)