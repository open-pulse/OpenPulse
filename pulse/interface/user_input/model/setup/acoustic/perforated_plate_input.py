
from PyQt5.QtWidgets import QComboBox, QDialog, QCheckBox, QLabel, QLineEdit, QPushButton, QRadioButton, QSpinBox, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.plots.general.advanced_cursor import AdvancedCursor
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.model.perforated_plate import PerforatedPlate
from pulse.postprocessing.plot_acoustic_data import get_acoustic_absortion, get_perforated_plate_impedance

import os
import numpy as np
from pathlib import Path


window_title_1 = "Error"
window_title_2 = "Warning"

class PerforatedPlateInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/setup/acoustic/perforated_plate_input.ui"
        uic.loadUi(ui_path, self)

        self.valve_line_ids = kwargs.get("valve_line_ids", list())

        app().main_window.set_input_widget(self)

        self.preprocessor = app().project.preprocessor
        self.properties = app().project.model.properties

        self.before_run = app().project.get_pre_solution_model_checks()

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()

        self.selection_callback()
        self.load_elements_info()

        self.update_valve_line_id()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.complete = False

        self.imported_values = None
        self.table_path = None

        #
        self.dict_inputs = dict()
        self.dict_inputs['type'] = 0
        self.dict_inputs['dimensionless impedance'] = None

        self.frequencies = app().project.model.frequencies

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
        self.pushButton_attribute : QPushButton
        self.pushButton_cancel : QPushButton
        self.pushButton_remove : QPushButton
        self.pushButton_reset : QPushButton
        self.pushButton_load_table : QPushButton
        self.pushButton_plot_parameter : QPushButton

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
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_load_table.clicked.connect(self.load_table_button_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_plot_parameter.clicked.connect(self.pushButton_plot)
        #
        self.tabWidget_perforated_plate.currentChanged.connect(self.tab_event_callback)
        #       
        self.treeWidget_perforated_plate_preview.itemClicked.connect(self.on_click_item_plot)
        self.treeWidget_perforated_plate_preview.itemDoubleClicked.connect(self.on_doubleclick_item_plot)
        self.treeWidget_perforated_plate_remove.itemClicked.connect(self.on_click_item_tab_remove)
        self.treeWidget_perforated_plate_remove.itemDoubleClicked.connect(self.on_doubleclick_item_tab_remove)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        selected_elements = app().main_window.list_selected_elements()

        if selected_elements:

            selected_elements.sort()
            text = ", ".join([str(i) for i in selected_elements])
            self.lineEdit_element_id.setText(text)

            if len(selected_elements) == 1:

                element_id = selected_elements[0]                
                pp_data = self.properties._get_property("perforated_plate", element_id=element_id)
                if pp_data is not None:

                    self.reset_input_fields()
                    
                    self.lineEdit_hole_diameter.setText(str(pp_data["hole_diameter"]))
                    self.lineEdit_plate_thickness.setText(str(pp_data["thickness"]))
                    self.lineEdit_area_porosity.setText(str(pp_data["porosity"]))

                    self.comboBox_perforated_plate_model.setCurrentIndex(pp_data["type"])

                    if pp_data["nonlinear_effect"]:
                        self.lineEdit_nonlin_discharge.setText(str(pp_data["nonlinear_discharge_coefficient"]))

                    else:
                        if pp_data["linear_discharge_coefficient"]:
                            self.lineEdit_discharge_coefficient.setText(str(pp_data["linear_discharge_coefficient"]))
                    
                    if pp_data["bias_effect"]:
                        self.lineEdit_bias_flow_coefficient.setText(str(pp_data["bias_coefficient"]))

                    if "table path" in pp_data.keys():
                        _table_path = pp_data["table path"]
                        self.lineEdit_impedance_real.setText("")
                        self.lineEdit_impedance_imag.setText("")
                        self.tabWidget_dimensionless.setCurrentIndex(1)
                        self.lineEdit_load_table_path.setText(_table_path)

                    elif pp_data["dimensionless_impedance is not None"]:
                        self.lineEdit_load_table_path.setText("")
                        self.tabWidget_dimensionless.setCurrentIndex(0)
                        self.lineEdit_impedance_real.setText(str(np.real(pp_data["dimensionless_impedance"])))
                        self.lineEdit_impedance_imag.setText(str(np.imag(pp_data["dimensionless_impedance"])))

    def _config_widgets(self):
        self.treeWidget_perforated_plate_preview.setColumnWidth(0, 80)
        self.treeWidget_perforated_plate_remove.setColumnWidth(0, 80)
        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")
        self.update_checkboxes()

    def update_valve_line_id(self):

        element_ids = list()
        for line_id in self.valve_line_ids:
            for element_id in self.preprocessor.mesh.line_to_elements[line_id]:
                element_ids.append(element_id)

        if element_ids:
            app().main_window.set_selection(elements=element_ids)
            # text = ", ".join([str(i) for i in element_ids])
            # self.lineEdit_element_id.setText(text)
            self.lineEdit_element_id.setDisabled(True)

    def tab_event_callback(self):

        tab_index = self.tabWidget_perforated_plate.currentIndex()

        if tab_index == 0:
            self.label_selection.setText("Selected IDs:")
            self.selection_callback()

        elif tab_index == 1: 
            self.label_selection.setText("Group")
            items = self.treeWidget_perforated_plate_preview.selectedItems()
            if items == []:
                self.lineEdit_element_id.setText('')
            else:
                self.on_click_item_tab_remove(items[0])

        elif tab_index == 2: 
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

    def lineEdit_reset(self, lineEdit: QLineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()

    def load_table_button_callback(self):
        self.imported_values, self.table_path = self.load_table(button_pressed=True)

    def load_table(self, button_pressed=False):

        try:
            if self.lineEdit_load_table_path.text() == "" or button_pressed:

                last_path = app().config.get_last_folder_for("imported table folder")
                if last_path is None:
                    last_path = Path.home()

                caption = 'Choose a table to import the dimensionless impedance'
                imported_table_path, check = app().main_window.file_dialog.get_open_file_name(  caption, 
                                                                                                last_path, 
                                                                                                'Files (*.csv; *.dat; *.txt)'  )
                
                if not check:
                    return None, None

            else:
                imported_table_path = self.lineEdit_load_table_path.text()

            if imported_table_path == "":
                return None, None

            skiprows = int(self.spinBox_skiprows.text())                
            imported_file = np.loadtxt(imported_table_path, delimiter=",", skiprows=skiprows)
 
            imported_filename = os.path.basename(imported_table_path)
            self.lineEdit_load_table_path.setText(imported_table_path)         
            imported_file = np.loadtxt(imported_table_path, delimiter=",")
        
            if imported_file.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum "
                message += "data must have frequencies, real and imaginary columns."
                PrintMessageInput([window_title_1, title, message])
                self.lineEdit_load_table_path.setFocus()
                return None, None

            imported_values = imported_file[:,1] + 1j*imported_file[:,2]

            self.frequencies = imported_file[:,0]
            f_min = self.frequencies[0]
            f_max = self.frequencies[-1]
            f_step = self.frequencies[1] - self.frequencies[0] 
            
            app().main_window.config.write_last_folder_path_in_file("imported table folder", imported_table_path)

            if app().project.model.change_analysis_frequency_setup(list(self.frequencies)):

                self.lineEdit_reset(self.lineEdit_load_table_path)

                title = "Project frequency setup cannot be modified"
                message = f"The following imported table of values has a frequency setup\n"
                message += "different from the others already imported ones. The current\n"
                message += "project frequency setup is not going to be modified."
                message += f"\n\n{imported_filename}"
                PrintMessageInput([window_title_1, title, message])
                return None, None

            else:

                frequency_setup = { "f_min" : f_min,
                                    "f_max" : f_max,
                                    "f_step" : f_step }

                app().project.model.set_frequency_setup(frequency_setup)
            
        except Exception as log_error:
            title = "Dimensionless impedance input error"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            return
        
        self.dict_inputs['dimensionless impedance'] = imported_values

        return imported_values, imported_table_path

    def save_table_file(self, element_id: int, values: np.ndarray):

        table_name = f"perforated_plate_dimensionless_impedance_element_{element_id}"

        real_values = np.real(values)
        imag_values = np.imag(values)
        data = np.array([self.frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("structural", table_name, data)

        return table_name, data

    def attribute_callback(self):

        try:

            lineEdit = self.lineEdit_element_id.text()
            stop, element_ids = self.before_run.check_selected_ids(lineEdit, "elements")

            if stop:
                self.lineEdit_element_id.setFocus()
                return True

            if len(element_ids) == 0:
                return True

            elements_diameter = list()
            elements_lengths = list()
            for element_id in element_ids:
                element = app().project.model.preprocessor.acoustic_elements[element_id]
                elements_diameter.append(element.cross_section.inner_diameter)
                elements_lengths.append(element.length)

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

                    self.imported_values, self.table_path = self.load_table()
                    for element_id in element_ids:
                        self.save_table_file(element_id, self.imported_values)

                else:
                    self.perforated_plate.dimensionless_impedance_table_name = self.table_path
                    # self.perforated_plate.dimensionless_impedance = self.imported_values

            self.preprocessor.set_perforated_plate_by_elements(element_ids, self.perforated_plate)
            self.preprocessor.process_elements_to_update_indexes_after_remesh_in_element_info_file(element_ids)

            app().pulse_file.write_element_properties_in_file()

            if len(element_ids) > 20:
                print(f"[Set Perforated Plate] - defined at {len(element_ids)} selected elements")
            else:
                print(f"[Set Perforated Plate] - defined at elements {element_ids}")

            self.load_elements_info()
            app().main_window.update_plots()
            self.complete = True
            self.close()    

        except Exception as log_error:
            title = "Error with the perforated plate data"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            return

    def remove_callback(self):

        if  self.lineEdit_element_id.text() != "":

            str_elements = self.lineEdit_element_id.text()
            stop, element_ids = self.before_run.check_selected_ids(str_elements, "elements")
            if stop:
                return

            self.remove_table_files_from_elements(element_ids)

            for element_id in element_ids:
                self.properties._remove_nodal_property("perforated_plate", element_id)

            app().pulse_file.write_element_properties_in_file()

            self.lineEdit_element_id.setText("")
            self.pushButton_remove.setDisabled(True)
            self.load_elements_info()

            app().main_window.update_plots()
            # self.close()

    def remove_table_files_from_elements(self, node_ids : list):
        table_names = self.properties.get_element_related_table_names("perforated_plate", node_ids)
        self.process_table_file_removal(table_names)

    def reset_callback(self):

        self.hide()

        title = "Resetting of perforated plates"
        message = "Would you like to remove all perforated plates from the acoustic model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            element_ids = list()
            for (property, element_id) in self.properties.element_properties.values():
                if property == "perforated_plate":
                    element_ids.append(element_id)

            for element_id in element_ids:
                self.remove_table_files_from_elements(element_ids)

            self.properties._reset_element_property("perforated_plate")
            app().pulse_file.write_element_properties_in_file()
            app().main_window.update_plots()
            self.close()

    def process_table_file_removal(self, table_names : list):
        if table_names:
            for table_name in table_names:
                self.properties.remove_imported_tables("acoustic", table_name)
            app().pulse_file.write_imported_table_data_in_file()

    def on_click_item_tab_remove(self, item):
        self.lineEdit_element_id.setText(item.text(0))

    def on_doubleclick_item_tab_remove(self, item):
        self.lineEdit_element_id.setText(item.text(0))
        self.get_information_of_group()

    def on_click_item_plot(self, item):
        self.lineEdit_element_id.setText(item.text(0))
        element_id = int(item.text(0))
        perforated_plate = self.properties._get_property("perforated_plate", element_id=element_id)
        if perforated_plate is not None:
            if "list_of_elements" in perforated_plate.keys():
                pass
    
    def on_doubleclick_item_plot(self, item):
        self.lineEdit_element_id.setText(item.text(0))
        self.get_information_of_group(int(item.text(0)))

    def parameter_to_plot_callback(self):
        parameter_index = self.comboBox_parameter_to_plot.currentIndex()
        if parameter_index == 1:
            self.comboBox_data_type.setDisabled(True)
        else:
            self.comboBox_data_type.setDisabled(False)      

    def check_frequencies(self):
        if self.frequencies is None:
            title = "Frequencies definition"
            message = "The frequencies of analysis must be defined to run the preview."
            PrintMessageInput([window_title_1, title, message])
            return True
        else:
            return False

    def get_response(self, element_id: int):

        element = app().project.model.preprocessor.acoustic_elements[element_id]

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

        element_id = int(self.lineEdit_element_id.text())
        perforated_plate = self.properties._get_property("perforated_plate", element_id=element_id)

        if isinstance(perforated_plate, PerforatedPlate):
            if perforated_plate.type == 2:

                if self.check_frequencies():
                    return

                self.plot(element_id)

    def plot(self, element_id: int):
        """
        """
        import matplotlib.pyplot as plt

        # TODO: replace by general frequency plotter
        plt.ion()
        fig = plt.figure(figsize=[12,7])
        ax = fig.add_subplot(1,1,1)

        frequencies = self.frequencies
        response = self.get_response(element_id)

        if self.comboBox_parameter_to_plot.currentIndex() == 0:
            if self.comboBox_data_type.currentIndex() == 0:
                ax.set_ylabel(("Normalized Impedance - Real [-]"), fontsize = 14, fontweight = 'bold')
            else:
                ax.set_ylabel(("Normalized Impedance - Imaginary [-]"), fontsize = 14, fontweight = 'bold')
        else: 
            ax.set_ylabel(("Absortion coefficient [-]"), fontsize = 14, fontweight = 'bold')
            ax.set_ylim(0,1)

        legend_label = "Response at element {}".format(element_id)
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
        for (property, element_id), data in self.properties.element_properties.items():
            if property == "perforated_plate" and isinstance(data, PerforatedPlate):

                hole_diameter = data["hole_diameter"]
                thickness = data["thickness"]
                porosity = data["porosity"]
                hole_diameter = data["hole_diameter"]

                text = f"d_h: {hole_diameter}m; t_p: {thickness}m; φ: {porosity}"

                new = QTreeWidgetItem([str(element_id), text])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_perforated_plate_preview.addTopLevelItem(new)

        self.treeWidget_perforated_plate_remove.clear()
        for (property, element_id), data in self.properties.element_properties.items():
            if property == "perforated_plate" and isinstance(data, PerforatedPlate):

                hole_diameter = data["hole_diameter"]
                thickness = data["thickness"]
                porosity = data["porosity"]
                hole_diameter = data["hole_diameter"]

                text = f"d_h: {hole_diameter}m; t_p: {thickness}m; φ: {porosity}"

                new = QTreeWidgetItem([str(element_id), text])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)  
                self.treeWidget_perforated_plate_remove.addTopLevelItem(new)

        self.update_tabs_visibility()

    def get_information_of_group(self, element_id: int):
        try:

            perforated_plate = self.properties._get_property("perforated_plate", element_id=element_id)
            if perforated_plate is not None:
                if "list_of_elements" in perforated_plate.keys():
                    pass
                    #TODO: reimplement this

        except Exception as log_error:
            title = "ERROR WHILE GETTING INFORMATION OF SELECTED GROUP"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def reset_input_fields(self):
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
    
    def update_tabs_visibility(self):
        self.tabWidget_perforated_plate.setTabVisible(1, False)
        self.tabWidget_perforated_plate.setTabVisible(2, False)
        for (property, _) in self.properties.element_properties.keys():
            if property == "perforated_plate":
                self.tabWidget_perforated_plate.setCurrentIndex(0)
                self.tabWidget_perforated_plate.setTabVisible(1, True)
                self.tabWidget_perforated_plate.setTabVisible(2, True)
                return
    
    def actions_to_finalize(self):
        app().main_window.update_plots()
        self.close()

class GetInformationOfGroup(QDialog):
    def __init__(self, value, selected_key, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/info/perforated_plate/get_perforated_plate_info.ui"
        uic.loadUi(ui_path, self)

        self.selected_key = selected_key
        self.perforated_plate = value[0]
        self.elements = value[1]

        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.load_group_info()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon) 
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

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)    