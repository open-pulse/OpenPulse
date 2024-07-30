
from PyQt5.QtWidgets import QComboBox, QDialog, QCheckBox, QFileDialog, QLabel, QLineEdit, QPushButton, QRadioButton, QSpinBox, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import get_openpulse_icon
from pulse.interface.user_input.plots.general.advanced_cursor import AdvancedCursor
from pulse.preprocessing.perforated_plate import PerforatedPlate
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.postprocessing.plot_acoustic_data import get_acoustic_absortion, get_perforated_plate_impedance
from pulse.tools.utils import get_new_path, remove_bc_from_file

import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

window_title_1 = "Error"
window_title_2 = "Warning"

class PerforatedPlateInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/setup/acoustic/perforated_plate_input.ui"
        uic.loadUi(ui_path, self)

        self.valve_ids = kwargs.get("valve_ids", list())

        self.project = app().project
        self.opv = app().main_window.opv_widget
        app().main_window.input_ui.set_input_widget(self)

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.update()
        self.load_elements_info()
        self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.inputs_from_node = False
        self.table_to_save = False
        self.complete = False
        self.type_label = None
        self.basename = None
        self.imported_values = None
        self.imported_filename = None
        self.user_impedance = None
        self.new_load_path_table = ''
        self.dict_label = "PERFORATED PLATE || {}"
        self.tol = 1e-6
        self.userPath = os.path.expanduser('~')
        #
        self.dict_inputs = {}
        self.dict_inputs['type'] = 0
        self.dict_inputs['dimensionless impedance'] = None

        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()
        
        self.acoustic_folder_path = self.project.file._acoustic_imported_data_folder_path
        self.perforated_plate_tables_folder_path = get_new_path(self.acoustic_folder_path, "perforated_plate_files") 

        self.frequencies = self.project.frequencies
        self.acoustic_elements = self.project.preprocessor.acoustic_elements
        self.structural_elements = self.project.preprocessor.structural_elements
        self.group_elements_with_perforated_plates = self.project.preprocessor.group_elements_with_perforated_plate
        self.elements_id = app().main_window.list_selected_elements()

        self.elements_info_path = self.project.file._element_info_path

    def _define_qt_variables(self):
        # QCheckBox
        self.checkBox_remove_valve_structural_effects : QCheckBox
        self.checkBox_single_hole : QCheckBox
        self.checkBox_bias_flow_coefficient : QCheckBox
        self.checkBox_dimensionless_impedance : QCheckBox
        self.checkBox_nonlinear_discharge_coefficient : QCheckBox
        # QComboBox
        self.comboBox_data_type : QComboBox
        self.comboBox_parameter_to_plot : QComboBox
        self.comboBox_perforated_plate_model : QComboBox
        # QLabel
        self.label_selection : QLabel
        self.label_non_linear_discharge_coefficient : QLabel
        self.label_correction_factor : QLabel
        self.label_bias_flow_coefficient : QLabel
        # QLineEdit
        self.lineEdit_element_id : QLineEdit
        self.lineEdit_element_id_plot : QLineEdit
        self.lineEdit_nonlin_discharge : QLineEdit
        self.lineEdit_correction_factor : QLineEdit
        self.lineEdit_impedance_real : QLineEdit
        self.lineEdit_impedance_imag : QLineEdit
        self.lineEdit_load_table_path : QLineEdit
        self.lineEdit_specify_element_id : QLineEdit
        self.lineEdit_bias_flow_coefficient : QLineEdit
        self.lineEdit_hole_diameter : QLineEdit
        self.lineEdit_plate_thickness : QLineEdit
        self.lineEdit_area_porosity : QLineEdit
        self.lineEdit_discharge_coefficient : QLineEdit
        # QPushButton
        self.pushButton_plot_parameter : QPushButton
        self.pushButton_remove : QPushButton
        self.pushButton_reset : QPushButton
        self.pushButton_confirm : QPushButton
        self.pushButton_load_table : QPushButton
        # QRadioButton
        self.radioButton_impedance : QRadioButton
        self.radioButton_absortion : QRadioButton
        self.radioButton_plotReal : QRadioButton
        self.radioButton_plotImag : QRadioButton
        # QSpinBox
        self.spinBox_skiprows : QSpinBox
        # QTabWidget
        self.tabWidget_dimensionless : QTabWidget
        self.tabWidget_perforated_plate : QTabWidget
        self.tabWidget_setup : QTabWidget
        # QTreeWidget
        self.treeWidget_perforated_plate_preview : QTreeWidget
        self.treeWidget_perforated_plate_remove : QTreeWidget


    def _create_connections(self):
        #
        self.checkBox_bias_flow_coefficient.toggled.connect(self.checkBoxEvent_bias)
        self.checkBox_nonlinear_discharge_coefficient.toggled.connect(self.checkBoxEvent_nonlinear)
        self.checkBox_dimensionless_impedance.toggled.connect(self.checkBoxEvent_dimensionless)
        #
        self.comboBox_perforated_plate_model.currentIndexChanged.connect(self.perforated_plate_model_update)
        self.comboBox_parameter_to_plot.currentIndexChanged.connect(self.parameter_to_plot_callback)
        #
        self.pushButton_confirm.clicked.connect(self.confirm_perforated_plate_attribution)
        self.pushButton_load_table.clicked.connect(self.load_dimensionless_impedance_table)
        self.pushButton_remove.clicked.connect(self.remove_perforated_plate_by_group)
        self.pushButton_reset.clicked.connect(self.remove_all_perforated_plate)
        self.pushButton_plot_parameter.clicked.connect(self.pushButton_plot)
        #
        self.tabWidget_perforated_plate.currentChanged.connect(self.tabEvent_callback)
        #       
        self.treeWidget_perforated_plate_preview.itemClicked.connect(self.on_click_item_plot)
        self.treeWidget_perforated_plate_preview.itemDoubleClicked.connect(self.on_doubleclick_item_plot)
        self.treeWidget_perforated_plate_remove.itemClicked.connect(self.on_click_item_tab_remove)
        self.treeWidget_perforated_plate_remove.itemDoubleClicked.connect(self.on_doubleclick_item_tab_remove)
        #
        self.update_checkboxes()
        self.update_valve_ids()

    def _config_widgets(self):
        self.treeWidget_perforated_plate_preview.setColumnWidth(0, 80)
        self.treeWidget_perforated_plate_remove.setColumnWidth(0, 80)
        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")

    def update_valve_ids(self):
        if self.valve_ids:
            self.elements_id = self.valve_ids
            self.lineEdit_element_id.setDisabled(True)

    def tabEvent_callback(self):
        self.currentTab_ = self.tabWidget_perforated_plate.currentIndex()
        if self.currentTab_ == 0:
            self.write_ids(self.elements_id)
            self.label_selection.setText("Elements IDs")

        elif self.currentTab_ == 1: 
            self.label_selection.setText("Group")
            items = self.treeWidget_perforated_plate_preview.selectedItems()
            if items == []:
                self.lineEdit_element_id.setText('')
            else:
                self.on_click_item_tab_remove(items[0])

        elif self.currentTab_ == 2: 
            self.label_selection.setText("Group")
            items = self.treeWidget_perforated_plate_remove.selectedItems()
            if items == []:
                self.lineEdit_element_id.setText('')
            else:
                self.on_click_item_tab_remove(items[0])

    def checkBoxEvent_nonlinear(self):
        if self.checkBox_nonlinear_discharge_coefficient.isChecked():
            self.label_correction_factor.setDisabled(False)
            self.label_non_linear_discharge_coefficient.setDisabled(False)
            self.lineEdit_nonlin_discharge.setDisabled(False)
            self.lineEdit_correction_factor.setDisabled(False)

        else:
            self.label_correction_factor.setDisabled(True)
            self.label_non_linear_discharge_coefficient.setDisabled(True)
            self.lineEdit_nonlin_discharge.setDisabled(True)
            self.lineEdit_correction_factor.setDisabled(True)

    def checkBoxEvent_bias(self):
        self.flag_bias = self.checkBox_bias_flow_coefficient.isChecked()
        if self.flag_bias:
            self.label_bias_flow_coefficient.setDisabled(False)
            self.lineEdit_bias_flow_coefficient.setDisabled(False)

        else:
            self.label_bias_flow_coefficient.setDisabled(True)
            self.lineEdit_bias_flow_coefficient.setDisabled(True)

    def checkBoxEvent_dimensionless(self):
        if self.checkBox_dimensionless_impedance.isChecked():
            self.tabWidget_dimensionless.setDisabled(False)
            self.lineEdit_load_table_path.setDisabled(False)
            self.pushButton_load_table.setDisabled(False)

        else:
            self.tabWidget_dimensionless.setDisabled(True)
            self.lineEdit_load_table_path.setDisabled(True)
            self.pushButton_load_table.setDisabled(True)
 
    def update_checkboxes(self):
        self.checkBoxEvent_nonlinear()
        self.checkBoxEvent_bias()
        self.checkBoxEvent_dimensionless()

    def perforated_plate_model_update(self):

        self.lineEdit_plate_thickness.setDisabled(False)
        self.lineEdit_area_porosity.setDisabled(False)
        self.lineEdit_discharge_coefficient.setDisabled(False)
        self.checkBox_single_hole.setChecked(False)
        self.checkBox_single_hole.setDisabled(False)
        self.tabWidget_setup.setTabVisible(1, False)

        index = self.comboBox_perforated_plate_model.currentIndex()

        if index == 0:
            self.dict_inputs['type'] = 0

            self.checkBox_nonlinear_discharge_coefficient.setDisabled(False)
            self.checkBox_bias_flow_coefficient.setDisabled(False)
            self.checkBox_dimensionless_impedance.setDisabled(False)
            self.update_checkboxes()
            self.tabWidget_setup.setTabVisible(1, True)

        elif index == 1:            
            self.dict_inputs['type'] = 1

        elif index == 2:
            self.dict_inputs['type'] = 2

            self.lineEdit_plate_thickness.setText("")
            self.lineEdit_area_porosity.setText("")
            self.lineEdit_discharge_coefficient.setText("")
            self.lineEdit_plate_thickness.setDisabled(True)
            self.lineEdit_area_porosity.setDisabled(True)
            self.lineEdit_discharge_coefficient.setDisabled(True)
            self.checkBox_single_hole.setChecked(True)
            self.checkBox_single_hole.setDisabled(True)
            self.lineEdit_hole_diameter.setFocus()

    def check_input_parameters(self, string, label, not_None = False):
        title = "INPUT ERROR"
        if string != "":
            try:
                value = float(string)
                if value < 0:
                    message = f"The {label} must be a positive number."
                    PrintMessageInput([window_title_1, title, message])
                    return True
                else:
                    self.value = value
            except Exception:
                message = f"You have typed an invalid value to the {label}."
                PrintMessageInput([window_title_1, title, message])
                return True
        elif not_None:
            message = f"The {label} must be given."
            PrintMessageInput([window_title_1, title, message])
            return True
        else:
            self.value = None
        return False

    def check_svalues(self):
        if self.lineEdit_impedance_real.text() != "":
            try:
                z_real = float(self.lineEdit_impedance_real.text())
            except Exception:
                title = "INPUT ERROR"
                message = "Wrong input for real part of dimensionless impedance."
                PrintMessageInput([window_title_1, title, message])
                self.lineEdit_impedance_real.setFocus()
                return True
        else:
            z_real = 0

        if self.lineEdit_impedance_imag.text() != "":
            try:
                z_imag = float(self.lineEdit_impedance_imag.text())
            except Exception:
                title = "INPUT ERROR"
                message = "Wrong input for imaginary part of dimensionless impedance."
                PrintMessageInput([window_title_1, title, message])
                self.lineEdit_impedance_imag.setFocus()
                return True
        else:
            z_imag = 0
        
        if z_real == 0 and z_imag == 0:
            self.dict_inputs['dimensionless impedance'] = None
        else:
            self.dict_inputs['dimensionless impedance'] = z_real + 1j*z_imag
        return False

    def lineEdit_reset(self, lineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()

    def load_dimensionless_impedance_table(self):
        self.load_table(button_pressed=True)

    def load_table(self, button_pressed=False):

        self.table_to_save = False
        try:
            if self.lineEdit_load_table_path.text() == "" or button_pressed:
                window_label = 'Choose a table to import the dimensionless impedance'
                self.path_imported_table, _ = QFileDialog.getOpenFileName(None, window_label, self.userPath, 'Files (*.csv; *.dat; *.txt)')
            else:
                self.path_imported_table = self.lineEdit_load_table_path.text()

            if self.path_imported_table == "":
                return

            self.imported_filename = os.path.basename(self.path_imported_table)
            self.lineEdit_load_table_path.setText(self.path_imported_table)

        except Exception as log_error:
            title = "Error while loading dimensionless impedance table file"
            message = str(log_error) 
            PrintMessageInput([window_title_1, title, message])
            return

        try:
            skiprows = int(self.spinBox_skiprows.text())                
            imported_file = np.loadtxt(self.path_imported_table, delimiter=",", skiprows=skiprows)
        except Exception as log_error:
            title = "Dimensionless impedance input error"
            message = f"{str(log_error)} \n\nIt is recommended to skip the header rows." 
            PrintMessageInput([window_title_1, title, message])
            return
        
        if imported_file.shape[1] < 3:
            title = "Dimensionless impedance input error"
            message = "The imported table has insufficient number of columns. The spectrum data " 
            message += "must have three columns with frequencies, real and imaginary data."
            PrintMessageInput([window_title_1, title, message])
            return
    
        try:
            
            self.imported_values = imported_file[:,1] + 1j*imported_file[:,2]

            if imported_file.shape[1] >= 3:

                self.frequencies = imported_file[:,0]
                self.f_min = self.frequencies[0]
                self.f_max = self.frequencies[-1]
                self.f_step = self.frequencies[1] - self.frequencies[0] 

                if self.project.change_project_frequency_setup(self.imported_filename, list(self.frequencies)):
                    self.lineEdit_reset(self.lineEdit_load_table_path)
                    return
                else:
                    self.project.set_frequencies(self.frequencies, self.f_min, self.f_max, self.f_step)
                
                self.table_to_save = True
                        
        except Exception as log_error:
            title = "Dimensionless impedance input error"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            return

        self.dict_inputs['dimensionless impedance'] = self.imported_values

    def save_table_file(self, values, filename, ext_index=None):
        try:

            self.project.create_folders_acoustic("perforated_plate_files")
        
            real_values = np.real(values)
            imag_values = np.imag(values)
            abs_values = np.abs(values)
            data = np.array([self.frequencies, real_values, imag_values, abs_values]).T

            header = f"OpenPulse - imported table for dimensionless impedance @ elements {self.elements_typed}\n"
            header += f"\nSource filename: {filename}\n"
            header += "\nFrequency [Hz], real[-], imaginary[-], absolute[-]"
            table_index = len(self.preprocessor.group_elements_with_perforated_plate) + 1
            if ext_index is None:
                # self.basename = filename + f"_table#{table_index}.dat"
                self.basename = f"perforated_plate_dimensionless_impedance_table#{table_index}.dat"
            else:
                # self.basename = filename + f"_table#{ext_index}.dat"
                self.basename = f"perforated_plate_dimensionless_impedance_table#{ext_index}.dat"
            self.new_path_table = get_new_path(self.perforated_plate_tables_folder_path, self.basename)
            np.savetxt(self.new_path_table, data, delimiter=",", header=header)
            return False

        except Exception as log_error:
            title = "Error reached while saving table files"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            return True

    def check_perforated_plate(self):

        lineEdit = self.lineEdit_element_id.text()
        self.stop, self.elements_typed = self.before_run.check_input_ElementID(lineEdit)
        self.elements_typed.sort()
        
        if self.stop:
            self.lineEdit_element_id.setFocus()
            return True

        if self.elements_typed == []:
            return True
        else:
            elements_diameter = []
            elements_lengths = []
            for element_id in self.elements_typed:
                elements_diameter.append(self.acoustic_elements[element_id].cross_section.inner_diameter)
                elements_lengths.append(self.acoustic_elements[element_id].length)
        
        # if self.table_to_save:
        #     if self.save_table_file(self.imported_values, self.imported_filename):
        #         return True

        # Check hole diameter
        if self.check_input_parameters(self.lineEdit_hole_diameter.text(), 'hole diameter', True):
            self.lineEdit_hole_diameter.setFocus()
            return True
        else:
            self.min_diameter = min(elements_diameter)
            if self.value > self.min_diameter:
                title = "Invalid hole diameter value"
                message = "The hole diameter must be less than element inner diameter."
                PrintMessageInput([window_title_1, title, message])
                self.lineEdit_hole_diameter.setFocus()
                return True
            self.dict_inputs['hole diameter'] = self.value
        
        if self.dict_inputs['type'] == 2:
            self.dict_inputs['plate thickness'] = round(min(elements_lengths), 6)
            self.dict_inputs['area porosity'] = 0
            self.dict_inputs['discharge coefficient'] = 0
            self.dict_inputs['nonlinear effects'] = 0
            self.dict_inputs['nonlinear discharge coefficient'] = 0
            self.dict_inputs['correction factor'] = 0
            self.dict_inputs['bias flow effects'] = 0
            self.dict_inputs['bias flow coefficient'] = 0
        else:

            # Check plate thickness
            if self.check_input_parameters(self.lineEdit_plate_thickness.text(), 'plate thickness', True):
                self.lineEdit_plate_thickness.setFocus()
                return True
            else:
                for length in elements_lengths:
                    if np.abs(length - self.value)/length > 0.01:
                        title = "Plate thickness different from element length"
                        message = "If possible, use plate thickness equal to the element length for better precision."
                        PrintMessageInput([window_title_2, title, message])
                        self.lineEdit_plate_thickness.setFocus()
                self.dict_inputs['plate thickness'] = self.value

            # Check area porosity
            if self.check_input_parameters(self.lineEdit_area_porosity.text(), 'area porosity', True):
                self.lineEdit_area_porosity.setFocus()
                return True
            else:
                if self.value >= 1:
                    title = "Invalid area porosity value"
                    message = "The area porosity must be less than 1."
                    PrintMessageInput([window_title_1, title, message])
                    self.lineEdit_area_porosity.setFocus()
                    return True
                self.dict_inputs['area porosity'] = self.value

            # Check discharge coefficient
            if self.check_input_parameters(self.lineEdit_discharge_coefficient.text(), 'discharge coefficient'):
                self.lineEdit_discharge_coefficient.setFocus()
                return True
            else:
                if self.value > 1:
                    title = "Invalid discharge coefficient value"
                    message = "The discharge coefficient must be less than or equal to 1."
                    PrintMessageInput([window_title_1, title, message])
                    self.lineEdit_discharge_coefficient.setFocus()
                    return True
                self.dict_inputs['discharge coefficient'] = self.value

            self.dict_inputs['nonlinear effects'] = self.checkBox_nonlinear_discharge_coefficient.isChecked()

            # Check nonlinear discharge coefficient
            if self.check_input_parameters(self.lineEdit_nonlin_discharge.text(), 'nonlinear discharge coefficient'):
                self.lineEdit_nonlin_discharge.setFocus()
                return True
            else:
                if self.value > 1:
                    title = "Invalid nonlinear discharge coefficient value"
                    message = "The nonlinear discharge coefficient must be less than or equal to 1."
                    PrintMessageInput([window_title_1, title, message])
                    self.lineEdit_nonlin_discharge.setFocus()
                    return True
                self.dict_inputs['nonlinear discharge coefficient'] = self.value

            # Check correction factor
            if self.check_input_parameters(self.lineEdit_correction_factor.text(), 'correction factor'):
                self.lineEdit_correction_factor.setFocus()
                return True
            else:
                self.dict_inputs['correction factor'] = self.value

            self.dict_inputs['bias flow effects'] = self.flag_bias

            # Check bias flow
            if self.check_input_parameters(self.lineEdit_bias_flow_coefficient.text(), 'bias flow coefficient'):
                self.lineEdit_bias_flow_coefficient.setFocus()
                return True
            else:
                self.dict_inputs['bias flow coefficient'] = self.value

            # Check dimensionless impedance
            if self.tabWidget_dimensionless.currentIndex()==0:
                if self.check_svalues():
                    return True
        
        self.dict_inputs['single hole'] = self.checkBox_single_hole.isChecked()

        self.perforated_plate = PerforatedPlate(self.dict_inputs['hole diameter'], 
                                                self.dict_inputs['plate thickness'],
                                                self.dict_inputs['area porosity'],
                                                discharge_coefficient = self.dict_inputs['discharge coefficient'],
                                                single_hole = self.dict_inputs['single hole'],
                                                nonlinear_effect = self.dict_inputs['nonlinear effects'],
                                                nonlinear_discharge_coefficient = self.dict_inputs['nonlinear discharge coefficient'],
                                                correction_factor = self.dict_inputs['correction factor'],
                                                bias_effect = self.dict_inputs['bias flow effects'],
                                                bias_coefficient = self.dict_inputs['bias flow coefficient'],
                                                dimensionless_impedance = self.dict_inputs['dimensionless impedance'],
                                                type = self.dict_inputs['type'])
        
        if self.lineEdit_load_table_path.text() != "":
            if self.imported_values is None:
                self.load_table()
                return self.check_perforated_plate()
            else:
                self.perforated_plate.dimensionless_impedance_table_name = self.basename
                # self.perforated_plate.dimensionless_impedance = self.imported_values

    def confirm_perforated_plate_attribution(self):
        
        try:
            if self.check_perforated_plate():
                return

            section = self.dict_label.format("Selection-1")
            dict_keys = self.preprocessor.group_elements_with_perforated_plate.keys()
            if section in dict_keys:
                index = 1
                while section in dict_keys:
                    index += 1
                    section = self.dict_label.format(f"Selection-{index}")
            
            self.set_perforated_plate_to_elements(section, _print=True, remove_tables=True)
            self.replaced = False
            temp_dict = self.group_elements_with_perforated_plates.copy()

            for key, values in temp_dict.items():
                if self.elements_typed == list(np.sort(values[1])):
                    if self.replaced:
                        self.remove_function(key, reset=False, message_print=False)
                    else:
                        if self.lineEdit_load_table_path.text() != "": 
                            if self.table_to_save:
                                ext_index = int(key.split("Selection-")[1])
                                if self.save_table_file(self.imported_values, self.imported_filename, ext_index=ext_index):
                                    return
                                self.perforated_plate.dimensionless_impedance_table_name = self.basename
                        else:
                            self.perforated_plate.dimensionless_impedance_table_name = None

                        self.set_perforated_plate_to_elements(key)
                        self.replaced = True
                else:
                    count1, count2 = 0, 0
                    for element in self.elements_typed:
                        if element in values[1]:
                            count1 += 1
                    fill_rate1 = count1/len(self.elements_typed)

                    for element in values[1]:
                        if element in self.elements_typed:
                            count2 += 1
                    fill_rate2 = count2/len(values[1])
                    
                    if np.max([fill_rate1, fill_rate2])>0.5 :
                        if self.replaced:
                            self.remove_function(key, reset=False, message_print=False)
                        else:
                            if self.lineEdit_load_table_path.text() != "": 
                                if self.table_to_save:
                                    ext_index = int(key.split("Selection-")[1])
                                    if self.save_table_file(self.imported_values, self.imported_filename, ext_index=ext_index):
                                        return
                                    self.perforated_plate.dimensionless_impedance_table_name = self.basename
                            else:
                                self.perforated_plate.dimensionless_impedance_table_name = None

                            self.set_perforated_plate_to_elements(key)
                            self.replaced = True

            self.complete = True
            self.opv.updateRendererMesh()
            self.close()         

        except Exception as log_error:
            title = "Error with the perforated plate data"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            return

    def set_perforated_plate_to_elements(self, section, _print=False, remove_tables=False): 
        if remove_tables:
            self.remove_tables_from_selected_elements()
        self.project.set_perforated_plate_by_elements(self.elements_typed, self.perforated_plate, section)
        if _print:
            if len(self.elements_typed)>20:
                print(f"[Set Perforated Plate] - defined at {len(self.elements_typed)} selected elements")
            else:
                print(f"[Set Perforated Plate] - defined at elements {self.elements_typed}")
        self.load_elements_info()

    def get_dimensionless_impedance_table_names_in_typed_elements(self):
        list_table_names = []
        for element_id in self.elements_typed:
            element = self.preprocessor.acoustic_elements[element_id]
            if element.perforated_plate is not None:
                if element.perforated_plate.dimensionless_impedance_table_name is not None:
                    table_name = element.perforated_plate.dimensionless_impedance_table_name
                    if table_name not in list_table_names:
                        list_table_names.append(table_name)
        return list_table_names

    def remove_tables_from_selected_elements(self):
        list_table_names = []
        for element_id in self.elements_typed:
            element = self.preprocessor.acoustic_elements[element_id]
            if element.perforated_plate is not None:
                if element.perforated_plate.dimensionless_impedance_table_name is not None:
                    table_name = element.perforated_plate.dimensionless_impedance_table_name
                    if table_name not in list_table_names:
                        list_table_names.append(table_name)

        for table_name in list_table_names:
            self.process_table_file_removal(table_name)

    def remove_function(self, key, reset=True, message_print=True):
        section = key

        if message_print:
            group_label = section.split(" || ")[1]
            message = f"The perforated plate attributed to the {group_label}"
            message += "group of elements have been removed."
        else:
            message = None

        [_, list_elements] = self.group_elements_with_perforated_plates[section]
        key_strings = ['perforated plate data', 'dimensionless impedance', 'list of elements']
        remove_bc_from_file([section], self.elements_info_path, key_strings, message)
        # self.remove_perforated_plate_table_files_attributed_to_elements(list_elements)
        if reset:
            self.preprocessor.set_perforated_plate_by_elements(list_elements, None, section, delete_from_dict=True)
        else:
            if section in self.preprocessor.group_elements_with_perforated_plate.keys():
                self.preprocessor.group_elements_with_perforated_plate.pop(section) 
        if self.checkBox_remove_valve_structural_effects.isChecked():
            self.check_if_is_there_a_valve_and_remove_it(list_elements)
        self.load_elements_info()

    def remove_perforated_plate_by_group(self):
        key = self.dict_label.format(self.lineEdit_element_id.text())
        [perforated_plate, _] = self.group_elements_with_perforated_plates[key]
        table_name = perforated_plate.dimensionless_impedance_table_name
        self.process_table_file_removal(table_name)
        if key in self.group_elements_with_perforated_plates.keys():
            self.remove_function(key)
        self.lineEdit_element_id.setText("")
        self.opv.updateRendererMesh()
    
    def remove_all_perforated_plate(self):
        temp_dict = self.group_elements_with_perforated_plates.copy()
        _keys = temp_dict.keys()
        for key in _keys:
            [perforated_plate, _] = self.group_elements_with_perforated_plates[key]
            table_name = perforated_plate.dimensionless_impedance_table_name
            self.process_table_file_removal(table_name)
            self.remove_function(key, message_print=False)
        title = "Perforated plate resetting"
        message = "The perforated plate has been removed from all elements."
        PrintMessageInput([window_title_2, title, message])
        self.opv.updateRendererMesh()
        self.close()
 
    def process_table_file_removal(self, table_name):
        if table_name is not None:
            self.project.remove_acoustic_table_files_from_folder(table_name, "perforated_plate_files")

    def on_click_item_tab_remove(self, item):
        self.lineEdit_element_id.setText(item.text(0))

    def on_doubleclick_item_tab_remove(self, item):
        self.lineEdit_element_id.setText(item.text(0))
        self.get_information_of_group()

    def on_click_item_plot(self, item):
        self.lineEdit_element_id.setText(item.text(0))
        selected_key = self.dict_label.format(self.lineEdit_element_id.text())
        if "Selection-" in selected_key:
            [_, list_elements] = self.group_elements_with_perforated_plates[selected_key]
            self.lineEdit_element_id_plot.setText(str(list_elements))
            if len(list_elements) == 1:
                self.lineEdit_specify_element_id.setText(str(list_elements[0]))
            else:
                self.lineEdit_specify_element_id.setText('')
    
    def on_doubleclick_item_plot(self, item):
        self.lineEdit_element_id.setText(item.text(0))
        self.get_information_of_group()

    def parameter_to_plot_callback(self):
        parameter_index = self.comboBox_parameter_to_plot.currentIndex()
        if parameter_index == 1:
            self.comboBox_data_type.setDisabled(True)
        else:
            self.comboBox_data_type.setDisabled(False)      

    def check_select_element(self):        
        selected_key = self.dict_label.format(self.lineEdit_element_id.text())
        if "Selection-" in selected_key:
            value = self.group_elements_with_perforated_plates[selected_key]
            tokens = self.lineEdit_specify_element_id.text().strip().split(',')
            if value[0].type == 2:
                return True
            try:
                tokens.remove('')
            except:     
                pass
            specified_element = list(map(int, tokens))
            group_elements = value[1]
            if len(specified_element) > 1:
                title = "ERROR IN ELEMENT SELECTION"
                message = "Please, select only one element in the group to plot the preview."
                self.info_text = [window_title_1, title, message]
                PrintMessageInput(self.info_text)
                return True
            elif len(specified_element) == 0:
                title = "ERROR IN ELEMENT SELECTION"
                message = "Please, select an element in the group to plot the preview."
                self.info_text = [window_title_1, title, message]
                PrintMessageInput(self.info_text)
                return True
            elif specified_element[0] in group_elements:
                self.plot_select_element = specified_element
                return False
                
        else:
            title = "ERROR IN GROUP SELECTION"
            message = "Please, select a group in the list to plot the preview."
            self.info_text = [window_title_1, title, message]
            PrintMessageInput(self.info_text)
            return True

    def check_frequencies(self):
        if self.frequencies is None:
            title = "Frequencies definition"
            message = "The frequencies of analysis must be defined to run the preview."
            PrintMessageInput([window_title_1, title, message])
            return True
        else:
            return False

    def get_response(self):

        # self.lineEdit_specify_element_id
        element = self.acoustic_elements[self.plot_select_element[0]]

        parameter_index = self.comboBox_parameter_to_plot.currentIndex()
        data_index = self.comboBox_data_type.currentIndex()

        if parameter_index == 1: 
            output_data = get_acoustic_absortion(element, self.frequencies)

        elif parameter_index == 0:
            if data_index == 0:
                output_data = get_perforated_plate_impedance(element, 
                                                             self.frequencies, 
                                                             True)
            elif data_index == 1:
                output_data = get_perforated_plate_impedance(element, 
                                                             self.frequencies, 
                                                             False)

        return output_data

    def pushButton_plot(self):
        if self.check_select_element():
            return
        if self.check_frequencies():
            return
        self.plot()

    def plot(self):
        """
        """
        # TODO: replace by general frequency plotter
        plt.ion()
        fig = plt.figure(figsize=[12,7])
        ax = fig.add_subplot(1,1,1)

        frequencies = self.frequencies
        response = self.get_response()

        if self.comboBox_parameter_to_plot.currentIndex() == 0:
            if self.comboBox_data_type.currentIndex() == 0:
                ax.set_ylabel(("Normalized Impedance - Real [-]"), fontsize = 14, fontweight = 'bold')
            else:
                ax.set_ylabel(("Normalized Impedance - Imaginary [-]"), fontsize = 14, fontweight = 'bold')
        else: 
            ax.set_ylabel(("Absortion coefficient [-]"), fontsize = 14, fontweight = 'bold')
            ax.set_ylim(0,1)

        legend_label = "Response at element {}".format(self.plot_select_element)
        first_plot, = plt.plot(frequencies, response, color=[1,0,0], linewidth=2, label=legend_label)
        _legends = plt.legend(handles=[first_plot], labels=[legend_label])#, loc='upper right')

        plt.gca().add_artist(_legends)

        ax.set_title(('PERFORATED PLATE'), fontsize = 16, fontweight = 'bold')
        ax.set_xlabel(('Frequency [Hz]'), fontsize = 14, fontweight = 'bold')

        cursor = AdvancedCursor(ax, frequencies, response, True)
        plt.connect('motion_notify_event', cursor.mouse_move)

        plt.show()

    def load_elements_info(self):
        self.treeWidget_perforated_plate_preview.clear()
        for section, value in self.group_elements_with_perforated_plates.items():
            text = "d_h: {}m; t_p: {}m; φ: {}".format(value[0].hole_diameter, value[0].thickness, value[0].porosity)
            key = section.split(" || ")[1]
            new = QTreeWidgetItem([key, text])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_perforated_plate_preview.addTopLevelItem(new)  
            
        self.treeWidget_perforated_plate_preview.header().setStyleSheet('font: 16px; font-size: 9pt; font-family: Arial;')
        self.treeWidget_perforated_plate_preview.setStyleSheet('font: 16px; font-size: 9pt; font-family: Arial;')

        self.treeWidget_perforated_plate_remove.clear()
        for section, value in self.group_elements_with_perforated_plates.items():
            text = "d_h: {}m; t_p: {}m; φ: {}".format(value[0].hole_diameter, value[0].thickness, value[0].porosity)
            key = section.split(" || ")[1]
            new = QTreeWidgetItem([key, text])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)  
            self.treeWidget_perforated_plate_remove.addTopLevelItem(new)  

        self.treeWidget_perforated_plate_remove.header().setStyleSheet('font: 16px; font-size: 9pt; font-family: Arial;')
        self.treeWidget_perforated_plate_remove.setStyleSheet('font: 16px; font-size: 9pt; font-family: Arial;')
        self.update_tabs_visibility()

    def get_information_of_group(self):
        try:
            selected_key = self.dict_label.format(self.lineEdit_element_id.text())
            if "Selection-" in selected_key:
                value = self.group_elements_with_perforated_plates[selected_key]
                GetInformationOfGroup(value, selected_key)
            else:
                title = "ERROR IN GROUP SELECTION"
                message = "Please, select a group in the list to get the information."
                self.info_text = [window_title_1, title, message]
                PrintMessageInput(self.info_text)
        except Exception as log_error:
            title = "ERROR WHILE GETTING INFORMATION OF SELECTED GROUP"
            message = str(log_error)
            self.info_text = [window_title_1, title, message]
            PrintMessageInput(self.info_text)

    def reset_input_fields(self, force_reset=False):
        if self.inputs_from_node or force_reset:
            self.lineEdit_hole_diameter.setText("")
            self.lineEdit_plate_thickness.setText("")
            self.lineEdit_area_porosity.setText("")
            self.lineEdit_discharge_coefficient.setText("1")
            self.lineEdit_nonlin_discharge.setText("0.76")
            self.lineEdit_correction_factor.setText("1")
            self.lineEdit_bias_flow_coefficient.setText("1")
            self.lineEdit_impedance_real.setText("")
            self.lineEdit_impedance_imag.setText("")
            self.lineEdit_load_table_path.setText("")
            self.comboBox_perforated_plate_model.setCurrentIndex(0)
            self.checkBox_nonlinear_discharge_coefficient.setChecked(False)            
            self.checkBox_bias_flow_coefficient.setChecked(False)            
            self.inputs_from_node = False

    def update(self):
        
        if len(self.valve_ids) == 0:
            self.elements_id = app().main_window.list_selected_elements()
        
        if self.elements_id != []:
            self.elements_id.sort()
            self.write_ids(self.elements_id)
            
            element_id = self.elements_id[0]
            element = self.preprocessor.acoustic_elements[element_id]
            perforated_plate = element.perforated_plate

            if perforated_plate is not None:
                
                self.reset_input_fields(force_reset=True)
                
                self.lineEdit_hole_diameter.setText(str(perforated_plate.hole_diameter))
                self.lineEdit_plate_thickness.setText(str(perforated_plate.thickness))
                self.lineEdit_area_porosity.setText(str(perforated_plate.porosity))

                if perforated_plate.type == 0:
                    self.comboBox_perforated_plate_model.setCurrentIndex(0)

                elif perforated_plate.type == 1:
                    self.comboBox_perforated_plate_model.setCurrentIndex(1)

                elif perforated_plate.type == 2:
                    self.comboBox_perforated_plate_model.setCurrentIndex(2)
                    # self.perforated_plate_model_update()

                if perforated_plate.nonlinear_effect:
                    self.lineEdit_nonlin_discharge.setText(str(perforated_plate.nonlinear_discharge_coefficient))

                else:
                    if perforated_plate.linear_discharge_coefficient:
                        self.lineEdit_discharge_coefficient.setText(str(perforated_plate.linear_discharge_coefficient))
                
                if perforated_plate.bias_effect:
                    self.lineEdit_bias_flow_coefficient.setText(str(perforated_plate.bias_coefficient))

                _table_name = perforated_plate.dimensionless_impedance_table_name
                if _table_name is not None:
                    self.lineEdit_impedance_real.setText("")
                    self.lineEdit_impedance_imag.setText("")
                    self.tabWidget_dimensionless.setCurrentIndex(1)
                    _path = get_new_path(self.perforated_plate_tables_folder_path, _table_name)
                    self.lineEdit_load_table_path.setText(_path)

                elif perforated_plate.dimensionless_impedance is not None:
                    self.lineEdit_load_table_path.setText("")
                    self.tabWidget_dimensionless.setCurrentIndex(0)
                    self.lineEdit_impedance_real.setText(str(np.real(perforated_plate.dimensionless_impedance)))
                    self.lineEdit_impedance_imag.setText(str(np.imag(perforated_plate.dimensionless_impedance)))
                
                self.inputs_from_node = True
            else:
                self.reset_input_fields()

    def write_ids(self, list_elements_ids):
        text = ""
        for _id in list_elements_ids:
            text += "{}, ".format(_id)
        self.lineEdit_element_id.setText(text[:-2])
    
    def update_tabs_visibility(self):
        if len(self.preprocessor.group_elements_with_perforated_plate) == 0:
            self.tabWidget_perforated_plate.setCurrentIndex(0)
            self.tabWidget_perforated_plate.setTabVisible(1, False)
            self.tabWidget_perforated_plate.setTabVisible(2, False)
        else:
            self.tabWidget_perforated_plate.setTabVisible(1, True)
            self.tabWidget_perforated_plate.setTabVisible(2, True)

    def check_if_is_there_a_valve_and_remove_it(self, perforated_plate_elements):
        _update_renderer = False
        temp_dict = self.preprocessor.group_elements_with_valves.copy()
        for key, data in temp_dict.items():
            [valve_elements, valve_parameters] = data
            for element_id in perforated_plate_elements:
                if element_id in valve_elements:
                    self.project.add_valve_by_elements(valve_elements, None)
                    #
                    lists_element_indexes = []
                    first_element_id = min(valve_elements)
                    last_element_id = max(valve_elements)
                    lists_element_indexes.append([  first_element_id-1, first_element_id+1, 
                                                    last_element_id-1, last_element_id+1  ])
                    #
                    line_id = self.preprocessor.elements_to_line[valve_elements[0]]
                    first_element_id_from_line = self.preprocessor.line_to_elements[line_id][0]
                    last_element_id_from_line = self.preprocessor.line_to_elements[line_id][-1]
                    lists_element_indexes.append([  first_element_id_from_line-1, first_element_id_from_line+1, 
                                                    last_element_id_from_line-1, last_element_id_from_line+1  ])
                    #
                    for element_indexes in lists_element_indexes:
                        for _element_id in element_indexes:
                            if _element_id not in valve_elements:
                                cross = self.structural_elements[_element_id].cross_section
                                element_type = self.structural_elements[_element_id].element_type
                                if element_type == 'pipe_1':
                                    if cross:
                                        self.project.set_cross_section_by_elements(valve_elements, cross)
                                        self.project.add_cross_sections_expansion_joints_valves_in_file(valve_elements)
                                        _update_renderer = True
                                        
        if _update_renderer:
            self.opv.opvRenderer.plot()
            self.opv.plot_entities_with_cross_section()
    
    def actions_to_finalize(self):
        self.opv.updateRendererMesh()
        self.close()

class GetInformationOfGroup(QDialog):
    def __init__(self, value, selected_key, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/info/perforated_plate/get_perforated_plate_info.ui"
        uic.loadUi(ui_path, self)

        self.selected_key = selected_key
        self.perforated_plate = value[0]
        self.elements = value[1]

        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.load_group_info()
        self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon) 
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):
        # QLabel
        self.title_label : QLabel
        # QLiineEdit
        self.lineEdit_selection_label : QLineEdit
        self.lineEdit_perforated_plate_elements : QLineEdit
        self.lineEdit_hole_diameter : QLineEdit
        self.lineEdit_plate_thickness : QLineEdit
        self.lineEdit_area_porosity : QLineEdit
        self.lineEdit_discharge_coefficient : QLineEdit
        self.lineEdit_single_hole : QLineEdit
        self.lineEdit_non_linear_discharge_coefficient : QLineEdit
        self.lineEdit_correction_factor : QLineEdit
        self.lineEdit_bias_flow_coefficient : QLineEdit
        self.lineEdit_dimensionless_impedance : QLineEdit
        # QPushButton
        self.pushButton_close : QPushButton
        # QTreeWidget
        self.treeWidget_info : QTreeWidget

    def _create_connections(self):
        self.pushButton_close.clicked.connect(self.close)

    def _config_widgets(self):
        str_selection = self.selected_key.split(" || ")[1]
        self.lineEdit_selection_label.setText(f"{str_selection}")
        self.lineEdit_perforated_plate_elements.setText(str(self.elements)[1:-1])

    def load_group_info(self):

        self.lineEdit_hole_diameter.setText(str(self.perforated_plate.hole_diameter))
        self.lineEdit_plate_thickness.setText(str(self.perforated_plate.thickness))

        if self.perforated_plate.porosity:
            self.lineEdit_area_porosity.setText(str(self.perforated_plate.porosity))
   
        else:
            self.lineEdit_area_porosity.setText("---")

        if self.perforated_plate.linear_discharge_coefficient:
            self.lineEdit_discharge_coefficient.setText(str(self.perforated_plate.linear_discharge_coefficient))

        else:
            self.lineEdit_discharge_coefficient.setText("---")

        self.lineEdit_single_hole.setText(str(self.perforated_plate.single_hole))

        if self.perforated_plate.nonlinear_effect:
            self.lineEdit_non_linear_discharge_coefficient.setDisabled(False)
            self.lineEdit_non_linear_discharge_coefficient.setText(str(self.perforated_plate.nonlinear_discharge_coefficient))
            self.lineEdit_correction_factor.setText(str(self.perforated_plate.correction_factor))

        else:
            self.lineEdit_non_linear_discharge_coefficient.setDisabled(True)
            self.lineEdit_non_linear_discharge_coefficient.setText("---")
            self.lineEdit_correction_factor.setText("---")
            self.lineEdit_non_linear_discharge_coefficient.setDisabled(True)
            self.lineEdit_correction_factor.setDisabled(True)

        if self.perforated_plate.bias_effect:
            self.lineEdit_bias_flow_coefficient.setDisabled(False)
            self.lineEdit_bias_flow_coefficient.setText(str(self.perforated_plate.bias_coefficient))

        else:
            self.lineEdit_bias_flow_coefficient.setDisabled(True)
            self.lineEdit_bias_flow_coefficient.setText("---")

        if self.perforated_plate.dimensionless_impedance_table_name is not None:
            self.lineEdit_dimensionless_impedance.setText(self.perforated_plate.dimensionless_impedance_table_name)

        elif isinstance(self.perforated_plate.dimensionless_impedance, (int, float, complex)):
            self.lineEdit_dimensionless_impedance.setText(str(self.perforated_plate.dimensionless_impedance))

        else:
            self.lineEdit_dimensionless_impedance.setText("---")
            self.lineEdit_dimensionless_impedance.setDisabled(True)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()