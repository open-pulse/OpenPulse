
from PyQt5.QtWidgets import QDialog, QCheckBox, QFileDialog, QLabel, QLineEdit, QPushButton, QRadioButton, QSpinBox, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np
import matplotlib.pyplot as plt

from pulse.tools.advanced_cursor import AdvancedCursor
from pulse.postprocessing.plot_acoustic_data import get_acoustic_absortion, get_perforated_plate_impedance
from pulse.preprocessing.perforated_plate import PerforatedPlate
from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput
from pulse.utils import get_new_path, remove_bc_from_file

window_title_1 = "ERROR"
window_title_2 = "WARNING"


class PerforatedPlateInput(QDialog):
    def __init__(self, project, opv, valve_ids=[], *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui_files/Model/Setup/Acoustic/perforatedPlateInput.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)

        self.valve_ids = valve_ids
        self.project = project
        self.preprocessor = project.preprocessor
        self.before_run = project.get_pre_solution_model_checks()
        
        self.acoustic_folder_path = self.project.file._acoustic_imported_data_folder_path
        self.perforated_plate_tables_folder_path = get_new_path(self.acoustic_folder_path, "perforated_plate_files") 

        self.frequencies = project.frequencies
        self.acoustic_elements = project.preprocessor.acoustic_elements
        self.structural_elements = project.preprocessor.structural_elements
        self.group_elements_with_perforated_plates = project.preprocessor.group_elements_with_perforated_plate
        self.group_elements_with_valves = self.preprocessor.group_elements_with_valves
        self.elements_id = self.opv.getListPickedElements()
        
        if self.valve_ids:
            self.elements_id = self.valve_ids
            self.lineEdit_elementID.setDisabled(True)

        self.elements_info_path = project.file._element_info_path

        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.update()
        self.load_elements_info()
        self.exec()

    def _reset_variables(self):
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

    def _define_qt_variables(self):
        #
        # QCheckBox
        self.checkBox_remove_valve_structural_effects = self.findChild(QCheckBox, 'checkBox_remove_valve_structural_effects')
        self.checkBox_single_hole = self.findChild(QCheckBox, 'checkBox_single_hole')
        self.checkBox_bias = self.findChild(QCheckBox, 'checkBox_bias')
        self.checkBox_nonlinear = self.findChild(QCheckBox, 'checkBox_nonlinear')
        self.checkBox_dimensionless = self.findChild(QCheckBox, 'checkBox_dimensionless')
        # QLabel
        self.label_selection = self.findChild(QLabel, 'label_selection')
        self.label_nonlinDischarge = self.findChild(QLabel, 'label_nonlinDischarge')
        self.label_bias = self.findChild(QLabel, 'label_bias')
        self.label_correction = self.findChild(QLabel, 'label_correction')
        self.label_dimensionless = self.findChild(QLabel, 'label_dimensionless')
        self.label_elementID_plot = self.findChild(QLabel, 'label_elementID_plot')
        # QLineEdit
        self.lineEdit_elementID = self.findChild(QLineEdit, 'lineEdit_elementID')
        self.lineEdit_nonlinDischarge = self.findChild(QLineEdit, 'lineEdit_nonlinDischarge')
        self.lineEdit_correction = self.findChild(QLineEdit, 'lineEdit_correction')
        self.lineEdit_impedance_real = self.findChild(QLineEdit, 'lineEdit_impedance_real')
        self.lineEdit_impedance_imag = self.findChild(QLineEdit, 'lineEdit_impedance_imag')
        self.lineEdit_load_table_path = self.findChild(QLineEdit, 'line_load_table_path')
        self.lineEdit_specify_elementID = self.findChild(QLineEdit, 'lineEdit_specify_elementID')
        self.lineEdit_bias = self.findChild(QLineEdit, 'lineEdit_bias')
        self.lineEdit_HoleDiameter = self.findChild(QLineEdit, 'lineEdit_HoleDiameter')
        self.lineEdit_thickness = self.findChild(QLineEdit, 'lineEdit_thickness')
        self.lineEdit_porosity = self.findChild(QLineEdit, 'lineEdit_porosity')
        self.lineEdit_discharge = self.findChild(QLineEdit, 'lineEdit_discharge')
        # QPushButton
        self.pushButton_plot_parameter = self.findChild(QPushButton, 'pushButton_plot_parameter')
        self.pushButton_get_information_remove = self.findChild(QPushButton, 'pushButton_get_information_remove')
        self.pushButton_remove = self.findChild(QPushButton, 'pushButton_remove')
        self.pushButton_reset = self.findChild(QPushButton, 'pushButton_reset')
        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_load_table = self.findChild(QPushButton, 'pushButton_load_table')
        self.pushButton_get_information_plot = self.findChild(QPushButton, 'pushButton_get_information_plot')
        # QRadioButton
        self.radioButton_OpenPulse = self.findChild(QRadioButton, 'radioButton_OpenPulse')        
        self.radioButton_melling = self.findChild(QRadioButton, 'radioButton_melling')
        self.radioButton_common_pipe_section = self.findChild(QRadioButton, 'radioButton_common_pipe_section')
        self.radioButton_impedance = self.findChild(QRadioButton, 'radioButton_impedance')
        self.radioButton_absortion = self.findChild(QRadioButton, 'radioButton_absortion')
        self.radioButton_plotReal = self.findChild(QRadioButton, 'radioButton_plotReal')
        self.radioButton_plotImag = self.findChild(QRadioButton, 'radioButton_plotImag')
        # QSpinBox
        self.spinBox_skiprows = self.findChild(QSpinBox, 'spinBox')
        # QTabWidget
        self.tabWidget_perforated_plate = self.findChild(QTabWidget, 'tabWidget_perforated_plate')
        self.tabWidget_setup = self.tabWidget_perforated_plate.findChild(QTabWidget, 'tabWidget_setup')
        self.tabWidget_dimensionless = self.findChild(QTabWidget, "tabWidget_dimensionless")
        # QTreeWidget
        self.treeWidget_perforated_plate_plot = self.findChild(QTreeWidget, 'treeWidget_perforated_plate_plot')
        self.treeWidget_perforated_plate_remove = self.findChild(QTreeWidget, 'treeWidget_perforated_plate_remove')
        self.treeWidget_perforated_plate_plot.setColumnWidth(0, 80)
        self.treeWidget_perforated_plate_remove.setColumnWidth(0, 80)
        # QWidget
        self.tab_setup = self.tabWidget_perforated_plate.findChild(QWidget, 'tab_setup')
        self.tab_preview = self.tabWidget_perforated_plate.findChild(QWidget, 'tab_preview')
        self.tab_remove = self.tabWidget_perforated_plate.findChild(QWidget, 'tab_remove')
        self.tab_main = self.tabWidget_setup.findChild(QWidget, 'tab_main')
        self.tab_advanced = self.tabWidget_setup.findChild(QWidget, 'tab_advanced')
        self.tab_constant_value = self.tabWidget_dimensionless.findChild(QWidget, "tab_constant_value")
        self.tab_table_values = self.tabWidget_dimensionless.findChild(QWidget, "tab_table_values")

    def _create_connections(self):
        #
        self.checkBox_bias.toggled.connect(self.checkBoxEvent_bias)
        self.checkBox_nonlinear.toggled.connect(self.checkBoxEvent_nonlinear)
        self.checkBox_dimensionless.toggled.connect(self.checkBoxEvent_dimensionless)
        #
        self.pushButton_confirm.clicked.connect(self.confirm_perforated_plate_attribution)
        self.pushButton_get_information_remove.clicked.connect(self.get_information_of_group)
        self.pushButton_remove.clicked.connect(self.remove_perforated_plate_by_group)
        self.pushButton_reset.clicked.connect(self.remove_all_perforated_plate)
        self.pushButton_plot_parameter.clicked.connect(self.pushButton_plot)
        self.pushButton_get_information_plot.clicked.connect(self.get_information_of_group)
        #
        self.radioButton_impedance.toggled.connect(self.radioButtonEvent_preview)
        self.radioButton_absortion.toggled.connect(self.radioButtonEvent_preview)
        self.radioButton_plotReal.toggled.connect(self.radioButtonEvent_preview)
        self.radioButton_plotImag.toggled.connect(self.radioButtonEvent_preview)
        self.radioButton_OpenPulse.toggled.connect(self.radioButtonEvent_setup)
        self.radioButton_melling.toggled.connect(self.radioButtonEvent_setup)
        self.radioButton_common_pipe_section.toggled.connect(self.radioButtonEvent_setup)
        #
        self.tabWidget_perforated_plate.currentChanged.connect(self.tabEvent_)
        #
        self.toolButton_load_table.clicked.connect(self.load_dimensionless_impedance_table)
        #        
        self.treeWidget_perforated_plate_plot.itemClicked.connect(self.on_click_item_plot)
        self.treeWidget_perforated_plate_plot.itemDoubleClicked.connect(self.on_doubleclick_item_plot)
        self.treeWidget_perforated_plate_remove.itemClicked.connect(self.on_click_item)
        self.treeWidget_perforated_plate_remove.itemDoubleClicked.connect(self.on_doubleclick_item_remove)
        #
        self.flag_impedance = self.radioButton_impedance.isChecked()
        self.flag_absortion = self.radioButton_absortion.isChecked()
        self.flag_plotReal = self.radioButton_plotReal.isChecked()
        self.flag_plotImag = self.radioButton_plotImag.isChecked()
        self.checkBoxEvent_bias()


    def tabEvent_(self):
        self.currentTab_ = self.tabWidget_perforated_plate.currentIndex()
        if self.currentTab_ == 0:
            self.write_ids(self.elements_id)
            self.label_selection.setText("Elements IDs")
        elif self.currentTab_ == 1: 
            self.label_selection.setText("Group")
            items = self.treeWidget_perforated_plate_plot.selectedItems()
            if items == []:
                self.lineEdit_elementID.setText('')
            else:
                self.on_click_item(items[0])
        elif self.currentTab_ == 2: 
            self.label_selection.setText("Group")
            items = self.treeWidget_perforated_plate_remove.selectedItems()
            if items == []:
                self.lineEdit_elementID.setText('')
            else:
                self.on_click_item(items[0])
    
    def checkBoxEvent_nonlinear(self):
        if self.checkBox_nonlinear.isChecked():
            self.lineEdit_nonlinDischarge.setDisabled(False)
            self.label_nonlinDischarge.setDisabled(False)
            self.lineEdit_correction.setDisabled(False)
            self.label_correction.setDisabled(False)
        else:
            self.lineEdit_nonlinDischarge.setDisabled(True)
            self.label_nonlinDischarge.setDisabled(True)
            self.lineEdit_correction.setDisabled(True)
            self.label_correction.setDisabled(True)

    def checkBoxEvent_bias(self):
        self.flag_bias = self.checkBox_bias.isChecked()
        if self.flag_bias:
            self.lineEdit_bias.setDisabled(False)
            self.label_bias.setDisabled(False)
        else:
            self.lineEdit_bias.setDisabled(True)
            self.label_bias.setDisabled(True)

    def checkBoxEvent_dimensionless(self):
        if self.checkBox_dimensionless.isChecked():
            self.tabWidget_dimensionless.setDisabled(False)
            self.label_dimensionless.setDisabled(False)
            self.lineEdit_load_table_path.setDisabled(False)
            self.toolButton_load_table.setDisabled(False)
        else:
            self.tabWidget_dimensionless.setDisabled(True)
            self.label_dimensionless.setDisabled(True)
            self.lineEdit_load_table_path.setDisabled(True)
            self.toolButton_load_table.setDisabled(True)
 
    def radioButtonEvent_setup(self):
        self.flag_common_pipe_section = self.radioButton_common_pipe_section.isChecked()
        self.lineEdit_thickness.setDisabled(False)
        self.lineEdit_porosity.setDisabled(False)
        self.lineEdit_discharge.setDisabled(False)
        self.checkBox_single_hole.setChecked(False)
        self.checkBox_single_hole.setDisabled(False)
        self.tabWidget_setup.removeTab(1)

        if self.radioButton_OpenPulse.isChecked():

            self.checkBox_nonlinear.setDisabled(False)
            self.checkBoxEvent_nonlinear()

            self.checkBox_bias.setDisabled(False)
            self.checkBoxEvent_bias()

            self.checkBox_dimensionless.setDisabled(False)
            self.checkBoxEvent_dimensionless()
            self.tabWidget_setup.addTab(self.tab_advanced, "Advanced")
            self.dict_inputs['type'] = 0

        elif self.radioButton_melling.isChecked():
            
            self.dict_inputs['type'] = 1

        elif self.flag_common_pipe_section:
            
            self.lineEdit_thickness.setText("")
            self.lineEdit_porosity.setText("")
            self.lineEdit_discharge.setText("")
            self.lineEdit_thickness.setDisabled(True)
            self.lineEdit_porosity.setDisabled(True)
            self.lineEdit_discharge.setDisabled(True)
            self.checkBox_single_hole.setChecked(True)
            self.checkBox_single_hole.setDisabled(True)
            self.lineEdit_HoleDiameter.setFocus()

            self.dict_inputs['type'] = 2

    def check_input_parameters(self, string, label, not_None = False):
        title = "INPUT ERROR"
        if string != "":
            try:
                value = float(string)
                if value < 0:
                    message = f"The {label} must be a positive number."
                    PrintMessageInput([title, message, window_title_1])
                    return True
                else:
                    self.value = value
            except Exception:
                message = f"You have typed an invalid value to the {label}."
                PrintMessageInput([title, message, window_title_1])
                return True
        elif not_None:
            message = f"The {label} must be given."
            PrintMessageInput([title, message, window_title_1])
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
                PrintMessageInput([title, message, window_title_1])
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
                PrintMessageInput([title, message, window_title_1])
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
            PrintMessageInput([title, message, window_title_1])
            return

        try:
            skiprows = int(self.spinBox_skiprows.text())                
            imported_file = np.loadtxt(self.path_imported_table, delimiter=",", skiprows=skiprows)
        except Exception as log_error:
            title = "Dimensionless impedance input error"
            message = f"{str(log_error)} \n\nIt is recommended to skip the header rows." 
            PrintMessageInput([title, message, window_title_1])
            return
        
        if imported_file.shape[1] < 3:
            title = "Dimensionless impedance input error"
            message = "The imported table has insufficient number of columns. The spectrum \ndata " 
            message += "must have frequencies, real and imaginary columns."
            PrintMessageInput([title, message, window_title_1])
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
            PrintMessageInput([title, message, window_title_1])
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
            PrintMessageInput([title, message, window_title_1])
            return True

    def check_perforated_plate(self):

        lineEdit = self.lineEdit_elementID.text()
        self.stop, self.elements_typed = self.before_run.check_input_ElementID(lineEdit)
        self.elements_typed.sort()
        
        if self.stop:
            self.lineEdit_elementID.setFocus()
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
        if self.check_input_parameters(self.lineEdit_HoleDiameter.text(), 'hole diameter', True):
            self.lineEdit_HoleDiameter.setFocus()
            return True
        else:
            self.min_diameter = min(elements_diameter)
            if self.value > self.min_diameter:
                title = "Invalid hole diameter value"
                message = "The hole diameter must be less than element inner diameter."
                PrintMessageInput([title, message, window_title_1])
                self.lineEdit_HoleDiameter.setFocus()
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
            if self.check_input_parameters(self.lineEdit_thickness.text(), 'plate thickness', True):
                self.lineEdit_thickness.setFocus()
                return True
            else:
                aux = np.append(np.array(elements_lengths) > self.value-self.tol, np.array(elements_lengths) < self.value+self.tol)
                if not all(aux):
                    title = "Plate thickness different from element length"
                    message = "If possible, use plate thickness equal to the element length for better precision."
                    PrintMessageInput([title, message, "WARNING MESSAGE"])
                    self.lineEdit_thickness.setFocus()
                self.dict_inputs['plate thickness'] = self.value

            # Check area porosity
            if self.check_input_parameters(self.lineEdit_porosity.text(), 'area porosity', True):
                self.lineEdit_porosity.setFocus()
                return True
            else:
                if self.value >= 1:
                    title = "Invalid area porosity value"
                    message = "The area porosity must be less than 1."
                    PrintMessageInput([title, message, window_title_1])
                    self.lineEdit_porosity.setFocus()
                    return True
                self.dict_inputs['area porosity'] = self.value

            # Check discharge coefficient
            if self.check_input_parameters(self.lineEdit_discharge.text(), 'discharge coefficient'):
                self.lineEdit_discharge.setFocus()
                return True
            else:
                if self.value > 1:
                    title = "Invalid discharge coefficient value"
                    message = "The discharge coefficient must be less than or equal to 1."
                    PrintMessageInput([title, message, window_title_1])
                    self.lineEdit_discharge.setFocus()
                    return True
                self.dict_inputs['discharge coefficient'] = self.value

            self.dict_inputs['nonlinear effects'] = self.checkBox_nonlinear.isChecked()

            # Check nonlinear discharge coefficient
            if self.check_input_parameters(self.lineEdit_nonlinDischarge.text(), 'nonlinear discharge coefficient'):
                self.lineEdit_nonlinDischarge.setFocus()
                return True
            else:
                if self.value > 1:
                    title = "Invalid nonlinear discharge coefficient value"
                    message = "The nonlinear discharge coefficient must be less than or equal to 1."
                    PrintMessageInput([title, message, window_title_1])
                    self.lineEdit_nonlinDischarge.setFocus()
                    return True
                self.dict_inputs['nonlinear discharge coefficient'] = self.value

            # Check correction factor
            if self.check_input_parameters(self.lineEdit_correction.text(), 'correction factor'):
                self.lineEdit_correction.setFocus()
                return True
            else:
                self.dict_inputs['correction factor'] = self.value

            self.dict_inputs['bias flow effects'] = self.flag_bias

            # Check bias flow
            if self.check_input_parameters(self.lineEdit_bias.text(), 'bias flow coefficient'):
                self.lineEdit_bias.setFocus()
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
            PrintMessageInput([title, message, window_title_1])
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
            message = f"The perforated plate attributed to the {group_label}\n"
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
        key = self.dict_label.format(self.lineEdit_elementID.text())
        [perforated_plate, _] = self.group_elements_with_perforated_plates[key]
        table_name = perforated_plate.dimensionless_impedance_table_name
        self.process_table_file_removal(table_name)
        if key in self.group_elements_with_perforated_plates.keys():
            self.remove_function(key)
        self.lineEdit_elementID.setText("")
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
        message = "The perforated plate has been removed\n from all elements."
        PrintMessageInput([title, message, window_title_2])
        self.opv.updateRendererMesh()
        self.close()
 
    def process_table_file_removal(self, table_name):
        if table_name is not None:
            self.project.remove_acoustic_table_files_from_folder(table_name, "perforated_plate_files")

    def on_click_item(self, item):
        self.lineEdit_elementID.setText(item.text(0))

    def on_doubleclick_item_remove(self, item):
        self.lineEdit_elementID.setText(item.text(0))
        self.remove_perforated_plate_by_group()

    def on_click_item_plot(self, item):
        self.lineEdit_elementID.setText(item.text(0))
        selected_key = self.dict_label.format(self.lineEdit_elementID.text())
        if "Selection-" in selected_key:
            [_, list_elements] = self.group_elements_with_perforated_plates[selected_key]
            self.label_elementID_plot.setText(str(list_elements))
            if len(list_elements) == 1:
                self.lineEdit_specify_elementID.setText(str(list_elements[0]))
            else:
                self.lineEdit_specify_elementID.setText('')
    
    def on_doubleclick_item_plot(self, item):
        self.lineEdit_elementID.setText(item.text(0))

    def radioButtonEvent_preview(self):
        self.flag_impedance = self.radioButton_impedance.isChecked()
        self.flag_absortion = self.radioButton_absortion.isChecked()

        if self.flag_absortion: 
            self.radioButton_plotReal.setDisabled(True)
            self.radioButton_plotImag.setDisabled(True)
        else:
            self.radioButton_plotReal.setDisabled(False)
            self.radioButton_plotImag.setDisabled(False)
            self.flag_plotReal = self.radioButton_plotReal.isChecked()
            self.flag_plotImag = self.radioButton_plotImag.isChecked()        

    def check_select_element(self):        
        selected_key = self.dict_label.format(self.lineEdit_elementID.text())
        if "Selection-" in selected_key:
            value = self.group_elements_with_perforated_plates[selected_key]
            tokens = self.lineEdit_specify_elementID.text().strip().split(',')
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
                self.info_text = [title, message, window_title_1]
                PrintMessageInput(self.info_text)
                return True
            elif len(specified_element) == 0:
                title = "ERROR IN ELEMENT SELECTION"
                message = "Please, select an element in the group to plot the preview."
                self.info_text = [title, message, window_title_1]
                PrintMessageInput(self.info_text)
                return True
            elif specified_element[0] in group_elements:
                self.plot_select_element = specified_element
                return False
                
        else:
            title = "ERROR IN GROUP SELECTION"
            message = "Please, select a group in the list to plot the preview."
            self.info_text = [title, message, window_title_1]
            PrintMessageInput(self.info_text)
            return True

    def check_frequencies(self):
        if self.frequencies is None:
            title = "Frequencies definition"
            message = "The frequencies of analysis must be defined to run the preview."
            PrintMessageInput([title, message, window_title_1])
            return True
        else:
            return False

    def get_response(self):
        self.lineEdit_specify_elementID
        element = self.acoustic_elements[self.plot_select_element[0]]
        if self.flag_absortion: 
            output_data = get_acoustic_absortion(element, self.frequencies)
        elif self.flag_impedance:
            if self.flag_plotReal:
                output_data = get_perforated_plate_impedance(element, self.frequencies, True)
            elif self.flag_plotImag:
                output_data = get_perforated_plate_impedance(element, self.frequencies, False)
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
        plt.ion()
        fig = plt.figure(figsize=[12,7])
        ax = fig.add_subplot(1,1,1)

        frequencies = self.frequencies
        response = self.get_response()

        if self.flag_impedance:
            if self.flag_plotReal:
                ax.set_ylabel(("Normalized Impedance - Real [-]"), fontsize = 14, fontweight = 'bold')
            elif self.flag_plotImag:
                ax.set_ylabel(("Normalized Impedance - Imaginary [-]"), fontsize = 14, fontweight = 'bold')
        elif self.flag_absortion: 
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
        self.treeWidget_perforated_plate_plot.clear()
        for section, value in self.group_elements_with_perforated_plates.items():
            text = "d_h: {}m; t_p: {}m; φ: {}".format(value[0].hole_diameter, value[0].thickness, value[0].porosity)
            key = section.split(" || ")[1]
            new = QTreeWidgetItem([key, text])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_perforated_plate_plot.addTopLevelItem(new)  
            
        self.treeWidget_perforated_plate_plot.header().setStyleSheet('font: 16px; font-size: 9pt; font-family: Arial;')
        self.treeWidget_perforated_plate_plot.setStyleSheet('font: 16px; font-size: 9pt; font-family: Arial;')

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
            selected_key = self.dict_label.format(self.lineEdit_elementID.text())
            if "Selection-" in selected_key:
                value = self.group_elements_with_perforated_plates[selected_key]
                GetInformationOfGroup(value, selected_key)
            else:
                title = "ERROR IN GROUP SELECTION"
                message = "Please, select a group in the list to get the information."
                self.info_text = [title, message, window_title_1]
                PrintMessageInput(self.info_text)
        except Exception as log_error:
            title = "ERROR WHILE GETTING INFORMATION OF SELECTED GROUP"
            message = str(log_error)
            self.info_text = [title, message, window_title_1]
            PrintMessageInput(self.info_text)

    def reset_input_fields(self, force_reset=False):
        if self.inputs_from_node or force_reset:
            self.lineEdit_HoleDiameter.setText("")
            self.lineEdit_thickness.setText("")
            self.lineEdit_porosity.setText("")
            self.lineEdit_discharge.setText("1")
            self.lineEdit_nonlinDischarge.setText("0.76")
            self.lineEdit_correction.setText("1")
            self.lineEdit_bias.setText("1")
            self.lineEdit_impedance_real.setText("")
            self.lineEdit_impedance_imag.setText("")
            self.lineEdit_load_table_path.setText("")
            self.radioButton_OpenPulse.setChecked(True)
            self.checkBox_nonlinear.setChecked(False)            
            self.checkBox_bias.setChecked(False)            
            self.inputs_from_node = False

    def update(self):
        
        if len(self.valve_ids) == 0:
            self.elements_id = self.opv.getListPickedElements()
        
        if self.elements_id != []:
            self.elements_id.sort()
            self.write_ids(self.elements_id)
            
            element_id = self.elements_id[0]
            element = self.preprocessor.acoustic_elements[element_id]
            perforated_plate = element.perforated_plate

            if perforated_plate is not None:
                
                self.reset_input_fields(force_reset=True)
                
                self.lineEdit_HoleDiameter.setText(str(perforated_plate.hole_diameter))
                self.lineEdit_thickness.setText(str(perforated_plate.thickness))
                self.lineEdit_porosity.setText(str(perforated_plate.porosity))

                if perforated_plate.type == 0:
                    self.radioButton_OpenPulse.setChecked(True)
                elif perforated_plate.type == 1:
                    self.radioButton_melling.setChecked(True)
                elif perforated_plate.type == 2:
                    self.radioButton_common_pipe_section.setChecked(True)
                    self.radioButtonEvent_setup()

                if perforated_plate.nonlinear_effect:
                    self.lineEdit_nonlinDischarge.setText(str(perforated_plate.nonlinear_discharge_coefficient))
                else:
                    if perforated_plate.linear_discharge_coefficient:
                        self.lineEdit_discharge.setText(str(perforated_plate.linear_discharge_coefficient))
                
                if perforated_plate.bias_effect:
                    self.lineEdit_bias.setText(str(perforated_plate.bias_coefficient))

                _table_name = perforated_plate.dimensionless_impedance_table_name
                if _table_name is not None:
                    self.lineEdit_impedance_real.setText("")
                    self.lineEdit_impedance_imag.setText("")
                    self.tabWidget_dimensionless.setCurrentWidget(self.tab_table_values)
                    _path = get_new_path(self.perforated_plate_tables_folder_path, _table_name)
                    self.lineEdit_load_table_path.setText(_path)
                elif perforated_plate.dimensionless_impedance is not None:
                    self.lineEdit_load_table_path.setText("")
                    self.tabWidget_dimensionless.setCurrentWidget(self.tab_constant_value)
                    self.lineEdit_impedance_real.setText(str(np.real(perforated_plate.dimensionless_impedance)))
                    self.lineEdit_impedance_imag.setText(str(np.imag(perforated_plate.dimensionless_impedance)))
                
                self.inputs_from_node = True
            else:
                self.reset_input_fields()

    def write_ids(self, list_elements_ids):
        text = ""
        for _id in list_elements_ids:
            text += "{}, ".format(_id)
        self.lineEdit_elementID.setText(text[:-2])
    
    def update_tabs_visibility(self):
        if len(self.preprocessor.group_elements_with_perforated_plate) == 0:
            self.tabWidget_perforated_plate.setCurrentWidget(self.tab_setup)
            self.tab_remove.setDisabled(True)
            self.tab_preview.setDisabled(True)
        else:
            self.tab_remove.setDisabled(False)
            self.tab_preview.setDisabled(False)

    def check_if_is_there_a_valve_and_remove_it(self, perforated_plate_elements):
        _update_renderer = False
        temp_dict = self.group_elements_with_valves.copy()
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
            self.opv.changePlotToEntitiesWithCrossSection()
    
    def actions_to_finalize(self):
        self.opv.updateRendererMesh()
        self.close()
       
class GetInformationOfGroup(QDialog):
    def __init__(self, value, selected_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(Path('data/user_input/ui_files/Model/Info/getGroupInformationPerforatedPlate.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon) 

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.perforated_plate = value[0]
        self.elements = value[1]

        self.title_label = self.findChild(QLabel, 'title_label')
        self.title_label.setText(f"{selected_key} information")

        self.treeWidget_info = self.findChild(QTreeWidget, 'treeWidget_group_info')

        self.Label_dh = self.findChild(QLabel, 'Label_dh')
        self.Label_tp = self.findChild(QLabel, 'Label_tp')
        self.Label_phi = self.findChild(QLabel, 'Label_phi')
        self.Label_sigma = self.findChild(QLabel, 'Label_sigma')
        self.Label_single_hole = self.findChild(QLabel, 'Label_single_hole')
        self.Label_nl_effects = self.findChild(QLabel, 'Label_nl_effects')
        self.Label_nl_sigma = self.findChild(QLabel, 'Label_nl_sigma')
        self.Label_correction = self.findChild(QLabel, 'Label_correction')
        self.Label_bias_effects = self.findChild(QLabel, 'Label_bias_effects')
        self.Label_bias_coefficient = self.findChild(QLabel, 'Label_bias_coefficient')
        self.Label_dimensionless_impedance = self.findChild(QLabel, 'Label_dimensionless_impedance')

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.force_to_close)

        self.load_group_info()
        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def load_group_info(self):
        new = QTreeWidgetItem([str(self.elements)])
        new.setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_group_info.addTopLevelItem(new)
        
        self.Label_dh.setText(str(self.perforated_plate.hole_diameter))
        self.Label_tp.setText(str(self.perforated_plate.thickness))
        
        if self.perforated_plate.porosity:
            self.Label_phi.setText(str(self.perforated_plate.porosity))
        else:
            self.Label_phi.setText("___")
            
        if self.perforated_plate.linear_discharge_coefficient:
            self.Label_sigma.setText(str(self.perforated_plate.linear_discharge_coefficient))
        else:
            self.Label_sigma.setText("___")

        self.Label_single_hole.setText(str(self.perforated_plate.single_hole))
        if self.perforated_plate.nonlinear_effect:
            self.Label_nl_effects.setText("On")
            self.Label_nl_sigma.setText(str(self.perforated_plate.nonlinear_discharge_coefficient))
            self.Label_correction.setText(str(self.perforated_plate.correction_factor))
        else:
            self.Label_nl_effects.setText("Off")
            self.Label_nl_sigma.setText("___")
            self.Label_correction.setText("___")
            self.Label_nl_sigma.setDisabled(True)
            self.Label_correction.setDisabled(True)
        if self.perforated_plate.bias_effect:
            self.Label_bias_effects.setText("On")
            self.Label_bias_coefficient.setText(str(self.perforated_plate.bias_coefficient))
        else:
            self.Label_bias_effects.setText("Off")
            self.Label_bias_coefficient.setText("___")
            self.Label_bias_coefficient.setDisabled(True)
        
        if self.perforated_plate.dimensionless_impedance_table_name is not None:
            self.Label_dimensionless_impedance.setText(self.perforated_plate.dimensionless_impedance_table_name)
        elif isinstance(self.perforated_plate.dimensionless_impedance, (int, float, complex)):
            self.Label_dimensionless_impedance.setText(str(self.perforated_plate.dimensionless_impedance))
        else:
            self.Label_dimensionless_impedance.setText("___")
            self.Label_dimensionless_impedance.setDisabled(True)
    
    def force_to_close(self):
        self.close()