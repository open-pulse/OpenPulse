# fmt: off

from PyQt5.QtWidgets import QComboBox, QCheckBox, QDialog, QFrame, QLabel, QLineEdit, QPushButton, QRadioButton, QSpinBox, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.plots.general.frequency_response_plotter import FrequencyResponsePlotter
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

        self.valve_element_ids = kwargs.get("valve_element_ids", list())

        app().main_window.set_input_widget(self)

        self.preprocessor = app().project.model.preprocessor
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

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.complete = False
        self.keep_window_open = True

        self.imported_values = None
        self.table_path = None

        #
        self.perforated_plate_inputs = dict()
        self.perforated_plate_inputs['type'] = 0
        self.perforated_plate_inputs['dimensionless_impedance'] = None

        self.frequencies = app().project.model.frequencies

    def _define_qt_variables(self):

        # QCheckBox
        self.checkBox_remove_valve_structural_effects : QCheckBox
        self.checkBox_single_hole : QCheckBox
        self.checkBox_bias_flow_coefficient : QCheckBox
        self.checkBox_dimensionless_impedance : QCheckBox
        self.checkBox_nonlinear_discharge_coefficient : QCheckBox

        # QComboBox
        self.comboBox_perforated_plate_model : QComboBox

        # QLabel
        self.label_selection : QLabel
        self.label_area_porosity: QLabel
        self.label_non_linear_discharge_coefficient : QLabel
        self.label_correction_factor : QLabel
        self.label_bias_flow_coefficient : QLabel

        # QFrame
        self.selection_frame: QFrame

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
        self.pushButton_plot_impedance : QPushButton
        self.pushButton_plot_absorption_coefficient : QPushButton

        # QRadioButton
        self.radioButton_impedance : QRadioButton
        self.radioButton_absortion : QRadioButton
        self.radioButton_plotReal : QRadioButton
        self.radioButton_plotImag : QRadioButton

        # QSpinBox
        self.spinBox_skiprows : QSpinBox

        # QTabWidget
        self.tabWidget_dimensionless : QTabWidget
        self.tabWidget_main : QTabWidget
        self.tabWidget_setup : QTabWidget

        # QTreeWidget
        self.treeWidget_elements_info : QTreeWidget

    def _create_connections(self):
        #
        self.checkBox_bias_flow_coefficient.toggled.connect(self.checkBoxEvent_bias)
        self.checkBox_nonlinear_discharge_coefficient.toggled.connect(self.checkBoxEvent_nonlinear)
        self.checkBox_dimensionless_impedance.toggled.connect(self.checkBoxEvent_dimensionless)
        self.checkBox_single_hole.stateChanged.connect(self.single_hole_perforated_plate_callback)
        #
        self.comboBox_perforated_plate_model.currentIndexChanged.connect(self.perforated_plate_model_update)
        #
        self.lineEdit_hole_diameter.textChanged.connect(self.single_hole_perforated_plate_callback)
        #
        self.pushButton_attribute.clicked.connect(self.attribute_callback)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_load_table.clicked.connect(self.load_table_button_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_plot_impedance.clicked.connect(self.plot_impedance_callback)
        self.pushButton_plot_absorption_coefficient.clicked.connect(self.plot_absorption_coefficient_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_elements_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_elements_info.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        selected_elements = app().main_window.list_selected_elements()

        if selected_elements:

            selected_elements.sort()
            text = ", ".join([str(i) for i in selected_elements])
            self.lineEdit_element_id.setText(text)

            self.single_hole_perforated_plate_callback()

            if len(selected_elements) == 1:

                element_id = selected_elements[0]                
                pp_data = self.properties._get_property("perforated_plate", element_id=element_id)
                if isinstance(pp_data, dict):

                    self.reset_input_fields()
                    
                    self.lineEdit_hole_diameter.setText(str(pp_data["hole_diameter"]))
                    self.lineEdit_plate_thickness.setText(str(pp_data["plate_thickness"]))

                    if pp_data["single_hole"]:
                        self.checkBox_single_hole.setChecked(pp_data["single_hole"])

                    area_porosity = pp_data["area_porosity"]
                    self.lineEdit_area_porosity.setText(str(round(area_porosity, 8)))

                    self.comboBox_perforated_plate_model.setCurrentIndex(pp_data["type"])

                    if "nonlinear_effects" in pp_data.keys():
                        nl_effects = pp_data["nonlinear_effects"]
                        self.checkBox_nonlinear_discharge_coefficient.setChecked(nl_effects)
                        if nl_effects:
                            self.lineEdit_nonlin_discharge.setText(str(pp_data["nonlinear_discharge_coefficient"]))
                    else:
                        self.checkBox_nonlinear_discharge_coefficient.setChecked(False)

                    if "linear_discharge_coefficient" in pp_data.keys():
                        self.lineEdit_discharge_coefficient.setText(str(pp_data["linear_discharge_coefficient"]))

                    if "bias_flow_effects" in pp_data.keys():
                        bias_flow_effects = pp_data["bias_flow_effects"]
                        self.checkBox_bias_flow_coefficient.setChecked(bias_flow_effects)
                        if bias_flow_effects:
                            self.lineEdit_bias_flow_coefficient.setText(str(pp_data["bias_flow_coefficient"]))
                    else:
                        self.checkBox_bias_flow_coefficient.setChecked(False)

                    if "table path" in pp_data.keys():
                        _table_path = pp_data["table path"]
                        self.lineEdit_impedance_real.setText("")
                        self.lineEdit_impedance_imag.setText("")
                        self.tabWidget_dimensionless.setCurrentIndex(1)
                        self.lineEdit_load_table_path.setText(_table_path)

                    elif pp_data["dimensionless_impedance"] is not None:
                        self.lineEdit_load_table_path.setText("")
                        self.tabWidget_dimensionless.setCurrentIndex(0)
                        dim_impedance = pp_data["dimensionless_impedance"]
                        self.lineEdit_impedance_real.setText(str(np.real(dim_impedance)))
                        self.lineEdit_impedance_imag.setText(str(np.imag(dim_impedance)))

    def _config_widgets(self):
        #
        for i, w in enumerate([120, 160]):
            self.treeWidget_elements_info.setColumnWidth(i, w)

        self.update_checkboxes()

    def update_valve_line_id(self):

        if self.valve_element_ids:
            app().main_window.set_selection(elements=self.valve_element_ids)
            self.lineEdit_element_id.setDisabled(True)

    def tab_event_callback(self):

        self.pushButton_plot_impedance.setDisabled(True)
        self.pushButton_plot_absorption_coefficient.setDisabled(True)

        if self.tabWidget_main.currentIndex() == 0:
            self.pushButton_remove.setDisabled(True)
            self.lineEdit_element_id.setText("")
            self.selection_callback()

        else:
            items = self.treeWidget_elements_info.selectedItems()
            if items == list():
                self.lineEdit_element_id.setText("")
            else:
                self.on_click_item(items[0])

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

    def get_area_porosity(self, element_id: int):
        element = self.preprocessor.structural_elements[element_id]
        if element.element_type == "pipe_1":
            if element.cross_section is not None:

                cross_section = element.cross_section
                d_in = cross_section.inner_diameter
                if self.lineEdit_hole_diameter.text() != "":

                    str_hole_diameter = self.lineEdit_hole_diameter.text()
                    str_hole_diameter = str_hole_diameter.replace(",", ".")

                    try:
                        hole_diameter = float(str_hole_diameter)
                        area_porosity = (hole_diameter / d_in)**2
                    except:
                        return None

                    return area_porosity

    def single_hole_perforated_plate_callback(self):
        key = self.checkBox_single_hole.isChecked()
        self.label_area_porosity.setDisabled(key)
        self.lineEdit_area_porosity.setDisabled(key)
        if key:
            selected_elements = app().main_window.list_selected_elements()
            if selected_elements:
                if len(selected_elements) == 1:
                    area_porosity = self.get_area_porosity(selected_elements[0])
                    if isinstance(area_porosity, float):
                        self.lineEdit_area_porosity.setText(str(round(area_porosity, 8)))
                    else:
                        self.lineEdit_area_porosity.setText("")
                else:
                    self.lineEdit_area_porosity.setText("multiple porosities")

    def perforated_plate_model_update(self):

        self.lineEdit_plate_thickness.setDisabled(False)
        self.lineEdit_area_porosity.setDisabled(False)
        self.lineEdit_discharge_coefficient.setDisabled(False)
        self.checkBox_single_hole.setChecked(False)
        self.checkBox_single_hole.setDisabled(False)
        self.tabWidget_setup.setTabVisible(1, False)

        index = self.comboBox_perforated_plate_model.currentIndex()

        if index == 0:
            self.perforated_plate_inputs['type'] = 0

            self.checkBox_nonlinear_discharge_coefficient.setDisabled(False)
            self.checkBox_bias_flow_coefficient.setDisabled(False)
            self.checkBox_dimensionless_impedance.setDisabled(False)
            self.update_checkboxes()
            self.tabWidget_setup.setTabVisible(1, True)

        elif index == 1:            
            self.perforated_plate_inputs['type'] = 1

        elif index == 2:
            self.perforated_plate_inputs['type'] = 2

            self.lineEdit_plate_thickness.setText("")
            self.lineEdit_area_porosity.setText("")
            self.lineEdit_discharge_coefficient.setText("")
            self.lineEdit_plate_thickness.setDisabled(True)
            self.lineEdit_area_porosity.setDisabled(True)
            self.lineEdit_discharge_coefficient.setDisabled(True)
            self.checkBox_single_hole.setChecked(True)
            self.checkBox_single_hole.setDisabled(True)
            self.lineEdit_hole_diameter.setFocus()

    def check_input_parameters(self, lineEdit: QLineEdit, label: str, _float=True):

        message = ""
        title = f"Invalid entry to the '{label}'"
        str_value = lineEdit.text()

        if str_value != "":

            try:

                str_value = str_value.replace(",", ".")
                if _float:
                    value = float(str_value)
                else:
                    value = int(str_value) 

                if value <= 0:
                    message = f"You cannot input a non-positive value to the '{label}'."

            except Exception as _log_error:
                message = f"You have typed an invalid value to the '{label}' input field."
                message += "The input value should be a positive float number.\n\n"
                message += f"{str(_log_error)}"
        else:
            message = f"An empty entry has been detected at the '{label}' input field. " 
            message += "You should to enter a positive value to proceed."

        if message != "":
            PrintMessageInput([window_title_1, title, message])
            return True, value
        else:
            return False, value

    def check_svalues(self):
        if self.lineEdit_impedance_real.text() != "":
            try:
                z_real = float(self.lineEdit_impedance_real.text())
            except Exception:
                title = "Input error"
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
                title = "Input error"
                message = "Wrong input for imaginary part of dimensionless impedance."
                PrintMessageInput([window_title_1, title, message])
                self.lineEdit_impedance_imag.setFocus()
                return True
        else:
            z_imag = 0
        
        if z_real == 0 and z_imag == 0:
            self.perforated_plate_inputs['dimensionless_impedance'] = None
        else:
            self.perforated_plate_inputs['dimensionless_impedance'] = z_real + 1j*z_imag
        return False

    def lineEdit_reset(self, lineEdit: QLineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()

    def load_table_button_callback(self):
        self.imported_values, self.table_path = self.load_table(button_pressed=True)

    def load_table(self, button_pressed=False):

        try:
            if self.lineEdit_load_table_path.text() == "" or button_pressed:

                last_path = app().config.get_last_folder_for("imported_table_folder")
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
            
            app().main_window.config.write_last_folder_path_in_file("imported_table_folder", imported_table_path)

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
            title = "Dimensionless impedance Input error"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            return
        
        self.perforated_plate_inputs['dimensionless_impedance'] = imported_values

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
            stop, hole_diameter = self.check_input_parameters(self.lineEdit_hole_diameter, 'Hole diameter')
            if stop:
                self.lineEdit_hole_diameter.setFocus()
                return True

            if hole_diameter > min(elements_diameter):
                title = "Invalid hole diameter value"
                message = "The hole diameter must be less than element inner diameter."
                PrintMessageInput([window_title_1, title, message])
                self.lineEdit_hole_diameter.setFocus()
                return True

            self.perforated_plate_inputs['hole_diameter'] = hole_diameter

            if self.perforated_plate_inputs['type'] == 2:
                self.perforated_plate_inputs['plate_thickness'] = round(min(elements_lengths), 6)
                self.perforated_plate_inputs['area_porosity'] = 0
                self.perforated_plate_inputs['discharge_coefficient'] = 1
                self.perforated_plate_inputs['nonlinear_effects'] = False
                self.perforated_plate_inputs['nonlinear_discharge_coefficient'] = 1
                self.perforated_plate_inputs['correction_factor'] = 0
                self.perforated_plate_inputs['bias_flow_effects'] = False
                self.perforated_plate_inputs['bias_flow_coefficient'] = 0

            else:

                # Check plate thickness
                stop, plate_thickness = self.check_input_parameters(self.lineEdit_plate_thickness, 'Plate thickness')
                if stop:
                    self.lineEdit_plate_thickness.setFocus()
                    return True

                for length in elements_lengths:
                    if np.abs(length - plate_thickness)/length > 0.01:
                        title = "Plate thickness different from element length"
                        message = "If possible, use plate thickness equal to the element length for better precision."
                        PrintMessageInput([window_title_2, title, message])
                        self.lineEdit_plate_thickness.setFocus()

                self.perforated_plate_inputs['plate_thickness'] = plate_thickness

                # Check area porosity
                if not self.checkBox_single_hole.isChecked():
                    stop, area_porosity = self.check_input_parameters(self.lineEdit_area_porosity, 'Area porosity')
                    if stop:
                        self.lineEdit_area_porosity.setFocus()
                        return True

                    if area_porosity >= 1:
                        title = "Invalid area porosity value"
                        message = "The area porosity must be less than 1."
                        PrintMessageInput([window_title_1, title, message])
                        self.lineEdit_area_porosity.setFocus()
                        return True

                    self.perforated_plate_inputs['area_porosity'] = area_porosity

                # Check discharge coefficient
                stop, discharge_coefficient = self.check_input_parameters(self.lineEdit_discharge_coefficient, 'Discharge coefficient')
                if stop:
                    self.lineEdit_discharge_coefficient.setFocus()
                    return True

                if discharge_coefficient > 1:
                    title = "Invalid discharge coefficient value"
                    message = "The discharge coefficient must be less than or equal to 1."
                    PrintMessageInput([window_title_1, title, message])
                    self.lineEdit_discharge_coefficient.setFocus()
                    return True

                self.perforated_plate_inputs['discharge_coefficient'] = discharge_coefficient
                self.perforated_plate_inputs['nonlinear_effects'] = self.checkBox_nonlinear_discharge_coefficient.isChecked()

                # Check nonlinear discharge coefficient
                stop, nl_discharge_coefficient = self.check_input_parameters(self.lineEdit_nonlin_discharge, 'Non-linear discharge coefficient')
                if stop:
                    self.lineEdit_nonlin_discharge.setFocus()
                    return True

                if nl_discharge_coefficient > 1:
                    title = "Invalid nonlinear discharge coefficient value"
                    message = "The nonlinear discharge coefficient must be less than or equal to 1."
                    PrintMessageInput([window_title_1, title, message])
                    self.lineEdit_nonlin_discharge.setFocus()
                    return True

                self.perforated_plate_inputs['nonlinear_discharge_coefficient'] = nl_discharge_coefficient

                # Check correction factor
                stop, correction_factor = self.check_input_parameters(self.lineEdit_correction_factor, 'Correction factor')
                if stop:
                    self.lineEdit_correction_factor.setFocus()
                    return True
                
                self.perforated_plate_inputs['correction_factor'] = correction_factor
                self.perforated_plate_inputs['bias_flow_effects'] = self.flag_bias

                # Check bias flow
                stop, bias_flow_coefficient = self.check_input_parameters(self.lineEdit_bias_flow_coefficient, 'Bias flow coefficient')
                if stop:
                    self.lineEdit_bias_flow_coefficient.setFocus()
                    return True

                self.perforated_plate_inputs['bias_flow_coefficient'] = bias_flow_coefficient

                # Check dimensionless impedance
                if self.tabWidget_dimensionless.currentIndex()==0:
                    if self.check_svalues():
                        return True
            
            self.perforated_plate_inputs['single_hole'] = self.checkBox_single_hole.isChecked()

            for element_id in element_ids:

                if self.checkBox_single_hole.isChecked():
                    area_porosity = self.get_area_porosity(element_id)
                    if area_porosity is None:
                        return

                    self.perforated_plate_inputs['area_porosity'] = area_porosity

                perforated_plate = PerforatedPlate(self.perforated_plate_inputs)

                if self.lineEdit_load_table_path.text() != "":
                    if self.imported_values is None:
                        self.imported_values, self.table_path = self.load_table()
                        self.save_table_file(element_id, self.imported_values)                           

                    else:
                        perforated_plate.dimensionless_impedance_table_name = self.table_path
                        # self.perforated_plate.dimensionless_impedance = self.imported_values
                
                coords = list()
                element = self.preprocessor.acoustic_elements[element_id]
                coords.extend(list(np.round(element.first_node.coordinates, 5)))
                coords.extend(list(np.round(element.last_node.coordinates, 5)))

                self.perforated_plate_inputs["coords"] = coords

                self.preprocessor.set_perforated_plate_by_elements(element_ids, perforated_plate)

                self.properties._set_element_property(  
                                                      "perforated_plate", 
                                                      self.perforated_plate_inputs, 
                                                      element_ids=element_id 
                                                      )

            self.actions_to_finalize()

            if len(element_ids) > 20:
                print(f"[Set Perforated Plate] - defined at {len(element_ids)} selected elements")
            else:
                print(f"[Set Perforated Plate] - defined at elements {element_ids}")

        except Exception as log_error:
            title = "Error with the perforated plate data"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            return

    def remove_callback(self):

        if  self.lineEdit_element_id.text() != "":

            element_id = int(self.lineEdit_element_id.text())

            self.remove_table_files_from_elements([element_id])
            self.properties._remove_element_property("perforated_plate", element_id)
            app().project.file.write_element_properties_in_file()

            self.preprocessor.set_perforated_plate_by_elements(element_id, None)
            self.actions_to_finalize()

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
            for (property, element_id) in self.properties.element_properties.keys():
                if property == "perforated_plate":
                    element_ids.append(element_id)

            for element_id in element_ids:
                self.remove_table_files_from_elements(element_ids)

            for element_id in element_ids:
                self.properties._remove_element_property("perforated_plate", element_id)

            self.preprocessor.set_perforated_plate_by_elements(element_ids, None)
            self.actions_to_finalize()

    def actions_to_finalize(self):
        app().project.file.write_element_properties_in_file()
        app().main_window.update_plots()
        self.load_elements_info()
        self.lineEdit_element_id.setText("")
        self.pushButton_cancel.setText("Exit")
        self.complete = True   

    def process_table_file_removal(self, table_names : list):
        if table_names:
            for table_name in table_names:
                self.properties.remove_imported_tables("acoustic", table_name)
            app().project.file.write_imported_table_data_in_file()

    def on_click_item(self, item):
        if item.text(0) != "":

            self.pushButton_remove.setEnabled(True)
            self.lineEdit_element_id.setText(item.text(0))

            element_id = int(self.lineEdit_element_id.text())
            data = self.properties._get_property("perforated_plate", element_id=element_id)

            if isinstance(data, dict):
                if data["type"] == 2:
                    self.pushButton_plot_impedance.setEnabled(True)
                    self.pushButton_plot_absorption_coefficient.setEnabled(True)
                else:
                    self.pushButton_plot_impedance.setDisabled(True)
                    self.pushButton_plot_absorption_coefficient.setDisabled(True)

    def on_doubleclick_item(self, item):
        self.on_click_item(item)
        element_id = int(item.text(0))
        self.get_information_of_group(element_id)

    def check_frequencies(self):
        if self.frequencies is None:
            title = "Frequencies definition"
            message = "The frequencies of analysis must be defined to run the preview."
            PrintMessageInput([window_title_1, title, message])
            return True
        else:
            return False

    def get_response(self, element_id: int, impedance=False, absorption=False):

        element = app().project.model.preprocessor.acoustic_elements[element_id]

        if absorption: 
            return get_acoustic_absortion(element, self.frequencies)

        elif impedance:
            return get_perforated_plate_impedance(element, self.frequencies)

    def plot_impedance_callback(self):

        if self.lineEdit_element_id.text() != "":

            element_id = int(self.lineEdit_element_id.text())
            data = self.properties._get_property("perforated_plate", element_id=element_id)

            if isinstance(data, dict):
                if data["type"] == 2:

                    if self.check_frequencies():
                        return

                    self.plot(element_id, impedance=True)

    def plot_absorption_coefficient_callback(self):

        if self.lineEdit_element_id.text() != "":
    
            element_id = int(self.lineEdit_element_id.text())
            data = self.properties._get_property("perforated_plate", element_id=element_id)

            if isinstance(data, dict):
                if data["type"] == 2:

                    if self.check_frequencies():
                        return

                    self.plot(element_id, absorption=True)

    def plot(self, element_id: int, **kargs):
        """
        """

        frequencies = self.frequencies
        response = self.get_response(element_id, **kargs)

        self.results_to_plot = dict()
        self.results_to_plot["data"] = { 
                                        "x_data" : frequencies,
                                        "y_data" : response
                                        }

        self.call_plotter()

    def call_plotter(self):

        # if self.check_inputs():
        #     return

        self.join_model_data()
        self.plotter = FrequencyResponsePlotter()
        self.plotter._set_model_results_data_to_plot(self.model_results)

    def join_model_data(self):

        self.hide()

        self.model_results = dict()
        title = "Perforated plate dimensionless impedance"

        for k, (label, data) in enumerate(self.results_to_plot.items()):

            key = ("element", (label))
            legend_label = "Impedance"

            self.model_results[key] = { 
                                        "x_data" : data["x_data"],
                                        "y_data" : data["y_data"],
                                        "x_label" : "Frequency [Hz]",
                                        "y_label" : "Dimensionless impedance",
                                        "title" : title,
                                        "legend" : legend_label,
                                        "unit" : "--",
                                        "color" : (0,0,255),
                                        "linestyle" : "-"
                                       }

    def load_elements_info(self):

        self.treeWidget_elements_info.clear()
        self.pushButton_remove.setDisabled(True)

        for (property, element_id), data in self.properties.element_properties.items():
            if property == "perforated_plate" and isinstance(data, dict):

                hole_diameter = data.get("hole_diameter", "")
                plat_thickness = data.get("plate_thickness", "")
                porosity = data.get("area_porosity", "")

                text = f"[{hole_diameter}, {plat_thickness}, {round(porosity, 8)}]"

                item = QTreeWidgetItem([str(element_id), text])
                for i in range(2):
                    item.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_elements_info.addTopLevelItem(item)

        self.update_tabs_visibility()

    def update_tabs_visibility(self):
        self.tabWidget_main.setTabVisible(1, False)
        self.tabWidget_main.setTabVisible(2, False)
        for (property, _) in self.properties.element_properties.keys():
            if property == "perforated_plate":
                self.tabWidget_main.setCurrentIndex(0)
                self.tabWidget_main.setTabVisible(1, True)
                self.tabWidget_main.setTabVisible(2, True)
                return

    def get_information_of_group(self, element_id: int):
        try:
            self.hide()
            pp_data = self.properties._get_property("perforated_plate", element_id=element_id)
            if isinstance(pp_data, dict):
                GetInformationOfGroup(element_id, pp_data)

        except Exception as log_error:
            title = "Error while getting information of the selected perforated plate"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def reset_input_fields(self):
        self.lineEdit_hole_diameter.setText("")
        self.lineEdit_plate_thickness.setText("")
        self.lineEdit_area_porosity.setText("")
        self.lineEdit_discharge_coefficient.setText("1.0")
        self.lineEdit_nonlin_discharge.setText("0.76")
        self.lineEdit_correction_factor.setText("1")
        self.lineEdit_bias_flow_coefficient.setText("1")
        self.lineEdit_impedance_real.setText("")
        self.lineEdit_impedance_imag.setText("")
        self.lineEdit_load_table_path.setText("")
        self.comboBox_perforated_plate_model.setCurrentIndex(0)
        self.checkBox_nonlinear_discharge_coefficient.setChecked(False)            
        self.checkBox_bias_flow_coefficient.setChecked(False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)


class GetInformationOfGroup(QDialog):
    def __init__(self, element_id, pp_data, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/info/get_perforated_plate_info.ui"
        uic.loadUi(ui_path, self)

        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.load_group_info(element_id, pp_data)
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon) 
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QLabel
        self.title_label : QLabel

        # QLineEdit
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
        pass

    def load_group_info(self, element_id: int, pp_data: dict):

        self.lineEdit_perforated_plate_elements.setText(str(element_id))

        self.lineEdit_hole_diameter.setText(str(pp_data["hole_diameter"]))
        self.lineEdit_plate_thickness.setText(str(pp_data["plate_thickness"]))

        if pp_data["area_porosity"]:
            area_porosity = round(pp_data["area_porosity"], 6)
            self.lineEdit_area_porosity.setText(str(area_porosity))

        else:
            self.lineEdit_area_porosity.setText("---")

        if "discharge_coefficient" in pp_data.keys():
            self.lineEdit_discharge_coefficient.setText(str(pp_data["linear_discharge_coefficient"]))

        else:
            self.lineEdit_discharge_coefficient.setText("---")

        self.lineEdit_single_hole.setText(str(pp_data["single_hole"]))

        if pp_data["nonlinear_effects"]:
            self.lineEdit_non_linear_discharge_coefficient.setDisabled(False)
            self.lineEdit_non_linear_discharge_coefficient.setText(str(pp_data["nonlinear_discharge_coefficient"]))
            self.lineEdit_correction_factor.setText(str(pp_data["correction_factor"]))

        else:
            self.lineEdit_non_linear_discharge_coefficient.setDisabled(True)
            self.lineEdit_non_linear_discharge_coefficient.setText("---")
            self.lineEdit_correction_factor.setText("---")
            self.lineEdit_non_linear_discharge_coefficient.setDisabled(True)
            self.lineEdit_correction_factor.setDisabled(True)

        if pp_data["bias_flow_effects"]:
            self.lineEdit_bias_flow_coefficient.setDisabled(False)
            self.lineEdit_bias_flow_coefficient.setText(str(pp_data["bias_flow_coefficient"]))

        else:
            self.lineEdit_bias_flow_coefficient.setDisabled(True)
            self.lineEdit_bias_flow_coefficient.setText("---")

        if "dimensionless_impedance_table_name" in pp_data.keys():
            self.lineEdit_dimensionless_impedance.setText(pp_data["dimensionless_impedance_table_name"])

        elif isinstance(pp_data["dimensionless_impedance"], (int, float, complex)):
            self.lineEdit_dimensionless_impedance.setText(str(pp_data["dimensionless_impedance"]))

        else:
            self.lineEdit_dimensionless_impedance.setText("---")
            self.lineEdit_dimensionless_impedance.setDisabled(True)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

# fmt: on