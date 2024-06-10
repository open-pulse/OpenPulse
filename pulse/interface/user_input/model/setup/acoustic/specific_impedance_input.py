from PyQt5.QtWidgets import QDialog, QFileDialog, QLineEdit, QPushButton, QSpinBox, QTabWidget, QToolButton, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.call_double_confirmation import CallDoubleConfirmationInput
from pulse.tools.utils import remove_bc_from_file, get_new_path

import os
import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

class SpecificImpedanceInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/specific_impedance_input.ui"
        uic.loadUi(ui_path, self)

        self.project = app().main_window.project
        self.opv = app().main_window.opv_widget
        self.opv.setInputObject(self)

        self._initialize()
        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self.update()
        self.load_nodes_info()
        self.exec()

    def _initialize(self):

        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()

        self.user_path = os.path.expanduser('~')
        self.new_load_path_table = ""
        self.acoustic_bc_info_path = self.project.file._node_acoustic_path  
        self.acoustic_folder_path = self.project.file._acoustic_imported_data_folder_path
        self.specific_impedance_tables_folder_path = get_new_path(self.acoustic_folder_path, "specific_impedance_files")   
        
        self.nodes_typed = []
        self.inputs_from_node = False
        self.remove_specific_impedance = False
        self.specific_impedance = None
        self.list_Nones = [None, None, None, None, None, None]
        
    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
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
        self.tabWidget_specific_impedance : QTabWidget
        # QTreeWidget
        self.treeWidget_specific_impedance : QTreeWidget
        self.treeWidget_specific_impedance.setColumnWidth(1, 20)
        self.treeWidget_specific_impedance.setColumnWidth(2, 80)

    def _create_connections(self):
        #
        self.constant_value_confirm_button.clicked.connect(self.check_constant_values)
        self.remove_button.clicked.connect(self.check_remove_bc_from_node)
        self.reset_button.clicked.connect(self.reset_callback)
        self.table_values_confirm_button.clicked.connect(self.check_table_values)
        self.search_button.clicked.connect(self.load_specific_impedance_table)
        #
        self.tabWidget_specific_impedance.currentChanged.connect(self.tabEvent_specific_impedance)
        #
        self.treeWidget_specific_impedance.itemClicked.connect(self.on_click_item)
        self.treeWidget_specific_impedance.itemDoubleClicked.connect(self.on_doubleclick_item)

    def tabEvent_specific_impedance(self):
        if self.tabWidget_specific_impedance.currentIndex() == 2:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
        else:
            self.update()
            self.lineEdit_selection_id.setDisabled(False)

    def load_nodes_info(self):
        self.treeWidget_specific_impedance.clear()
        for node in self.preprocessor.nodes_with_specific_impedance:
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(node.specific_impedance))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)            
            self.treeWidget_specific_impedance.addTopLevelItem(new)
        self.update_tabs_visibility()

    def check_complex_entries(self, lineEdit_real, lineEdit_imag):

        self.stop = False
        title = "Invalid entry to the specific impedance"
        if lineEdit_real.text() != "":
            try:
                real_F = float(lineEdit_real.text())
            except Exception:
                message = "Wrong input for real part of specific impedance."
                PrintMessageInput([window_title_1, title, message])
                lineEdit_real.setFocus()
                self.stop = True
                return
        else:
            real_F = 0

        if lineEdit_imag.text() != "":
            try:
                imag_F = float(lineEdit_imag.text())
            except Exception:
                message = "Wrong input for imaginary part of specific impedance."
                PrintMessageInput([window_title_1, title, message])
                lineEdit_imag.setFocus()
                self.stop = True
                return
        else:
            imag_F = 0
        
        if real_F == 0 and imag_F == 0:
            return None
        else:
            return real_F + 1j*imag_F

    def check_constant_values(self):

        lineEdit_selection_id = self.lineEdit_selection_id.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_selection_id)
        if self.stop:
            self.lineEdit_selection_id.setFocus()
            return

        specific_impedance = self.check_complex_entries(self.lineEdit_real_value, self.lineEdit_imag_value)
 
        if self.stop:
            return

        if specific_impedance is not None:
            self.specific_impedance = specific_impedance
            data = [self.specific_impedance, None]
            list_table_names = self.get_list_table_names_from_selected_nodes(self.nodes_typed)
            self.process_table_file_removal(list_table_names) 
            self.project.set_specific_impedance_bc_by_node(self.nodes_typed, data, False)
            self.opv.updateRendererMesh()
            print(f"[Set Specific Impedance] - defined at node(s) {self.nodes_typed}")
            self.close()
        else:    
            title = "Additional inputs required"
            message = "You must inform at least one specific impedance "
            message += "before confirming the input!"
            PrintMessageInput([window_title_1, title, message])
            self.lineEdit_real_value.setFocus()

    def load_table(self, lineEdit, direct_load=False):
        try:

            if direct_load:
                self.path_imported_table = lineEdit.text()
            else:
                window_label = 'Choose a table to import the specific impedance'
                self.path_imported_table, _ = QFileDialog.getOpenFileName(  None, 
                                                                            window_label, 
                                                                            self.user_path, 
                                                                            'Files (*.csv; *.dat; *.txt)'  )

            if self.path_imported_table == "":
                return None, None

            imported_filename = os.path.basename(self.path_imported_table)
            lineEdit.setText(self.path_imported_table)
            
            imported_file = np.loadtxt(self.path_imported_table, delimiter=",")

            title = "Error reached while loading 'specific impedance' table"
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
            title = "Error reached while loading 'specific impedance' table"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            lineEdit.setFocus()
            return None, None

    def lineEdit_reset(self, lineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()

    def save_table_file(self, node_id, values, filename):
        try:

            self.project.create_folders_acoustic("specific_impedance_files")
        
            real_values = np.real(values)
            imag_values = np.imag(values)
            abs_values = np.abs(values)
            data = np.array([self.frequencies, real_values, imag_values, abs_values]).T

            header = f"OpenPulse - imported table for specific impedance @ node {node_id}\n"
            header += f"\nSource filename: {filename}\n"
            header += "\nFrequency [Hz], real[Pa], imaginary[Pa], absolute[Pa]"
            basename = f"specific_impedance_node_{node_id}.dat"
            
            new_path_table = get_new_path(self.specific_impedance_tables_folder_path, basename)
            np.savetxt(new_path_table, data, delimiter=",", header=header)
            return values, basename

        except Exception as log_error:
            title = "Error reached while saving table files"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            return None, None

    def load_specific_impedance_table(self):
        self.imported_values, self.filename_specific_impedance = self.load_table(self.lineEdit_table_path)
    
    def check_table_values(self):
        lineEdit_selection_id = self.lineEdit_selection_id.text()
        self.stop, self.nodes_typed = self.before_run.check_input_NodeID(lineEdit_selection_id)
        if self.stop:
            self.lineEdit_selection_id.setFocus()
            return

        list_table_names = self.get_list_table_names_from_selected_nodes(self.nodes_typed)
        if self.lineEdit_table_path != "":
            for node_id in self.nodes_typed:
                if self.filename_specific_impedance is None:
                    self.imported_values, self.filename_specific_impedance = self.load_table(self.lineEdit_table_path, 
                                                                                             direct_load=True)
                if self.imported_values is None:
                    return
                else:
                    self.specific_impedance, self.basename_specific_impedance = self.save_table_file(   node_id, 
                                                                                                        self.imported_values, 
                                                                                                        self.filename_specific_impedance   )
                    if self.basename_specific_impedance in list_table_names:
                        list_table_names.remove(self.basename_specific_impedance)
                    data = [self.specific_impedance, self.basename_specific_impedance]
                    self.project.set_specific_impedance_bc_by_node([node_id], data, True)

            self.process_table_file_removal(list_table_names)
            self.opv.updateRendererMesh()
            print(f"[Set Specific Impedance] - defined at node(s) {self.nodes_typed}")   
            self.close()
        else:
            title = "Additional inputs required"
            message = "You must inform at least one specific impedance " 
            message += "table path before confirming the input!"
            PrintMessageInput([window_title_1, title, message])
            self.lineEdit_table_path.setFocus()

    def get_list_table_names_from_selected_nodes(self, list_node_ids):
        list_table_names = []
        for node_id in list_node_ids:
            node = self.preprocessor.nodes[node_id]
            if node.specific_impedance_table_name is not None:
                table_name = node.specific_impedance_table_name
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
        self.lineEdit_selection_id.setText(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_selection_id.setText(item.text(0))
        self.check_remove_bc_from_node()
    
    def check_remove_bc_from_node(self):
        if self.lineEdit_selection_id.text() != "":
            picked_node_id = int(self.lineEdit_selection_id.text())
            node = self.preprocessor.nodes[picked_node_id]            
            if node in self.preprocessor.nodes_with_specific_impedance:
                key_strings = ["specific impedance"]
                message = f"The specific impedance attributed to the {picked_node_id} node has been removed."
                remove_bc_from_file([picked_node_id], self.acoustic_bc_info_path, key_strings, message)
                list_table_names = self.get_list_table_names_from_selected_nodes([picked_node_id])
                self.process_table_file_removal(list_table_names)
                self.preprocessor.set_specific_impedance_bc_by_node(picked_node_id, [None, None])
                self.opv.updateRendererMesh()
                self.load_nodes_info()
                # self.close()  

    def process_table_file_removal(self, list_table_names):
        if list_table_names != []:
            for table_name in list_table_names:
                self.project.remove_acoustic_table_files_from_folder(table_name, "specific_impedance_files")    

    def reset_callback(self):
        if len(self.preprocessor.nodes_with_specific_impedance) > 0:

            list_nodes = list()
            for node in self.preprocessor.nodes_with_specific_impedance:
                list_nodes.append(node.external_index)
            
            title = f"Removal of all applied specific impedances"
            message = "Would you like to remove the specific impedance(s) "
            message += "applied to the following node(s)?\n"
            message += f"\n{list_nodes}"

            buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
            read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)

            if read._doNotRun:
                return

            if read._continue:

                _list_table_names = []
                _nodes_with_specific_impedance = self.preprocessor.nodes_with_specific_impedance.copy()

                for node in _nodes_with_specific_impedance:
                    node_id = node.external_index
                    key_strings = ["specific impedance"]
                    table_name = node.specific_impedance_table_name
                    if table_name is not None:
                        if table_name not in _list_table_names:
                            _list_table_names.append(table_name)
                    remove_bc_from_file([node_id], self.acoustic_bc_info_path, key_strings, None)
                    self.preprocessor.set_specific_impedance_bc_by_node(node_id, [None, None])
                
                self.process_table_file_removal(_list_table_names)
                self.load_nodes_info()

                title = "Specific impedance resetting process complete"
                message = "All specific impedances applied to the acoustic " 
                message += "model have been removed from the model."
                PrintMessageInput([window_title_2, title, message])

                self.opv.updateRendererMesh()
                self.close()

    def reset_input_fields(self, force_reset=False):
        if self.inputs_from_node or force_reset:
            self.lineEdit_real_value.setText("")
            self.lineEdit_imag_value.setText("")
            self.lineEdit_table_path.setText("")
            self.inputs_from_node = False

    def update(self):
        list_picked_nodes = self.opv.getListPickedPoints()
        if list_picked_nodes != []:
            picked_node = list_picked_nodes[0]
            node = self.preprocessor.nodes[picked_node]
            if node.specific_impedance is not None:
                self.reset_input_fields(force_reset=True)
                if node.specific_impedance_table_name is not None:
                    table_name = node.specific_impedance_table_name
                    self.tabWidget_specific_impedance.setCurrentIndex(1)
                    table_name = get_new_path(self.specific_impedance_tables_folder_path, table_name)
                    self.lineEdit_table_path.setText(table_name)
                else:
                    specific_impedance = node.specific_impedance
                    self.tabWidget_specific_impedance.setCurrentIndex(0)
                    self.lineEdit_real_value.setText(str(np.real(specific_impedance)))
                    self.lineEdit_imag_value.setText(str(np.imag(specific_impedance)))
                self.inputs_from_node = True
            else:
                self.reset_input_fields()
            self.writeNodes(self.opv.getListPickedPoints())

    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        if self.tabWidget_specific_impedance.currentIndex() != 2:
            self.lineEdit_selection_id.setText(text[:-2])

    def update_tabs_visibility(self):
        if len(self.preprocessor.nodes_with_specific_impedance) == 0:
            self.tabWidget_specific_impedance.setCurrentIndex(0)
            self.tabWidget_specific_impedance.setTabVisible(2, False)
        else:
            self.tabWidget_specific_impedance.setTabVisible(2, True)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_specific_impedance.currentIndex() == 0:
                self.check_constant_values()
            if self.tabWidget_specific_impedance.currentIndex() == 1:
                self.check_table_values()
        elif event.key() == Qt.Key_Delete:
            if self.tabWidget_specific_impedance.currentIndex() == 2:
                self.check_remove_bc_from_node()
        elif event.key() == Qt.Key_Escape:
            self.close()