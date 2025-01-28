from PyQt5.QtWidgets import QComboBox, QLineEdit, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf
from pulse.interface.user_input.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from pulse.interface.user_input.project.print_message import PrintMessageInput

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

psi_to_Pa = (0.45359237 * 9.80665) / ((0.0254)**2)
kgf_cm2_to_Pa = 9.80665e4

class ReciprocatingCompressorPulsationCriteriaInput(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "criterias/pulsation_criteria_widget.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.project = app().project
        self.model = app().project.model
        self.preprocessor = app().project.model.preprocessor
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()        
        self._define_qt_variables()
        self._create_connections()
        self.selection_callback()

    def _initialize(self):

        self.before_run = self.project.get_pre_solution_model_checks()
        self.frequencies = self.model.frequencies

        self.solution = self.project.get_acoustic_solution()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_line_ids : QComboBox

        # QLineEdit
        self.lineEdit_compressor_node_id : QLineEdit
        self.lineEdit_pressure_ratio : QLineEdit
        self.lineEdit_unfiltered_criteria : QLineEdit
        #        
        self.lineEdit_nozzle_id : QLineEdit
        self.lineEdit_line_pressure : QLineEdit
        self.lineEdit_speed_of_sound : QLineEdit
        self.lineEdit_internal_diameter : QLineEdit

        # QPushButton
        self.pushButton_plot_unfiltered_criteria : QPushButton
        self.pushButton_plot_filtered_criteria : QPushButton

    def _create_connections(self):
        #
        self.pushButton_plot_unfiltered_criteria.clicked.connect(self.plot_unfiltered_criteria)
        self.pushButton_plot_filtered_criteria.clicked.connect(self.plot_filtered_criteria)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        self.reset_unfiltered_fields()
        self.reset_filtered_fields()

        selected_nodes = app().main_window.list_selected_nodes()
        self.line_ids = self.preprocessor.get_line_from_node_id(selected_nodes)

        self.pushButton_plot_unfiltered_criteria.setDisabled(True)
        self.pushButton_plot_filtered_criteria.setDisabled(True)

        if len(selected_nodes) == 1:

            node_id = selected_nodes[0]
            compressor_data = self.properties._get_property("reciprocating_compressor_excitation", node_ids=node_id)

            if isinstance(compressor_data, dict):
                self.pushButton_plot_unfiltered_criteria.setDisabled(False)
                self.lineEdit_compressor_node_id.setText(str(selected_nodes[0]))
                self.get_existing_compressor_info(node_id)
                return

        if len(selected_nodes) == 1:
            self.pushButton_plot_filtered_criteria.setDisabled(False)
            self.lineEdit_nozzle_id.setText(str(selected_nodes[0]))        
        
        if len(self.line_ids) > 0:

            self.comboBox_line_ids.clear()
            for line_id in self.line_ids:
                self.comboBox_line_ids.addItem(f"      {line_id}")

            speed_of_sound, line_pressure, inner_diameter = self.get_line_properties()
            self.lineEdit_speed_of_sound.setText(str(round(speed_of_sound, 2)))
            self.lineEdit_line_pressure.setText(str(round(line_pressure, 2)))
            self.lineEdit_internal_diameter.setText(str(round(inner_diameter, 2)))

    def reset_unfiltered_fields(self):
        self.lineEdit_compressor_node_id.setText("")
        self.lineEdit_pressure_ratio.setText("")
        self.lineEdit_unfiltered_criteria.setText("")

    def reset_filtered_fields(self):
        self.comboBox_line_ids.clear()
        self.lineEdit_nozzle_id.setText("")
        self.lineEdit_internal_diameter.setText("")
        self.lineEdit_line_pressure.setText("")
        self.lineEdit_speed_of_sound.setText("")

    def get_existing_compressor_info(self, node_id: int):
        comp_data = self.properties._get_property("reciprocating_compressor_excitation", node_ids=node_id)
        if isinstance(comp_data, dict):
            self.update_compressor_data(comp_data)

    def update_compressor_data(self, stage_data: dict):

        parameters = stage_data.get("parameters", None)
        if parameters is None:
            return

        self.suction_pressure = parameters["pressure_at_suction"]
        self.pressure_ratio = parameters["pressure_ratio"]
        self.unfiltered_criteria = min([7, 3*self.pressure_ratio])
        self.lineEdit_pressure_ratio.setText(str(self.pressure_ratio))
        self.lineEdit_unfiltered_criteria.setText(str(round(self.unfiltered_criteria, 4)))

    def get_acoustic_pressure(self, node_id: int):
        response = get_acoustic_frf(self.preprocessor, self.solution, node_id)
        if complex(0) in response:
            response += np.ones(len(response), dtype=float)*(1e-12)
        return response

    def plot_unfiltered_criteria(self):

        node_ids = app().main_window.list_selected_nodes()
        if len(node_ids) == 1:
            node_id = node_ids[0]

        # change to peak-to-peak pressure
        acoustic_pressure = 2 * self.get_acoustic_pressure(node_id)
        self.absolute_line_pressure = self.get_line_pressure()
        avg_ratio = acoustic_pressure / self.absolute_line_pressure

        self.model_results = dict()
        self.title = "Maximum Allowable Compressor Cylinder Flange Pressure Pulsation"
        legend_label = "Acoustic pressure at node {}".format(node_id)

        key = ("pressure_ratio", (node_id))

        self.model_results[key] = { 
                                    "x_data" : self.frequencies,
                                    "y_data" : 100*avg_ratio,
                                    "x_label" : "Frequency [Hz]",
                                    "y_label" : "Cylinder pressure ratio",
                                    "title" : self.title,
                                    "data_information" : legend_label,
                                    "legend" : legend_label,
                                    "unit" : "%",
                                    "color" : [0,0,0],
                                    "linestyle" : "-" 
                                   }
        
        P_cf = np.ones_like(self.frequencies)*self.unfiltered_criteria
        # NOTE: Pcf is the maximum allowable unfiltered peak-to-peak pulsation level, as a 
        # percentage of average absolute line pressure at the compressor cylinder flange.

        legend_label = "Unfiltered criteria: {}%".format(round(self.unfiltered_criteria,2))

        key = ("unfiltered_criteria", (node_id))

        self.model_results[key] = {  
                                    "x_data" : self.frequencies,
                                    "y_data" : P_cf,
                                    "x_label" : "Frequency [Hz]",
                                    "y_label" : "Cylinder pressure ratio",
                                    "title" : self.title,
                                    "data_information" : legend_label,
                                    "legend" : legend_label,
                                    "unit" : "%",
                                    "color" : [1,0,0],
                                    "linestyle" : "-"  
                                   }

        self.plotter = FrequencyResponsePlotter()
        self.plotter._set_model_results_data_to_plot(self.model_results)

    def plot_filtered_criteria(self):

        node_ids = app().main_window.list_selected_nodes()
        if len(node_ids) == 1:
            node_id = node_ids[0]

        self.absolute_line_pressure = self.get_line_pressure()
        acoustic_pressure = 2 * self.get_acoustic_pressure(node_id)
        pulsation_ratio = acoustic_pressure / self.absolute_line_pressure

        self.model_results = dict()
        self.title = "Maximum Allowable Pulsation Limits at and Beyond Line-side\n Connections of Pulsation Suppression Devices"       
        legend_label = "Acoustic pressure at node {}".format(node_id)

        key = ("pressure_ratio", (node_id))

        self.model_results[key] = { 
                                    "x_data" : self.frequencies,
                                    "y_data" : 100*pulsation_ratio,
                                    "x_label" : "Frequency [Hz]",
                                    "y_label" : "Cylinder pressure ratio",
                                    "title" : self.title,
                                    "data_information" : legend_label,
                                    "legend" : legend_label,
                                    "unit" : "%",
                                    "color" : [0,0,0],
                                    "linestyle" : "-" 
                                   }

        df = 0.2
        f_max = self.frequencies[-1]
        freq = np.arange(df, f_max + df, df)

        speed_of_sound, line_pressure, inner_diameter = self.get_line_properties()
        P_1 = 400 * ((speed_of_sound / (350 * line_pressure * inner_diameter * freq))**(1/2))

        legend_label = "Filtered criteria"

        key = ("filtered_criteria", (node_id))

        self.model_results[key] = { 
                                    "x_data" : freq,
                                    "y_data" : P_1,
                                    "x_label" : "Frequency [Hz]",
                                    "y_label" : "Cylinder pressure ratio",
                                    "title" : self.title,
                                    "data_information" : legend_label,
                                    "legend" : legend_label,
                                    "unit" : "%",
                                    "color" : [1,0,0],
                                    "linestyle" : "-"  
                                   }
        
        self.plotter = FrequencyResponsePlotter()
        self.plotter._set_model_results_data_to_plot(self.model_results)

    def get_line_properties(self):

        line_id = int(self.comboBox_line_ids.currentText().replace(" ", ""))
        fluid = self.model.properties._get_property("fluid", line_id=line_id)
        if fluid is None:
            return None, None, None
        
        cross_section = self.model.properties._get_property("cross_section", line_id=line_id)
        if cross_section is None:
            return None, None, None

        speed_of_sound = fluid.speed_of_sound
        line_pressure = fluid.pressure
        inner_diameter = cross_section.inner_diameter

        return speed_of_sound, line_pressure/1e5, 1000*inner_diameter
    
    def get_line_pressure(self):
        if len(self.line_ids) == 1:
            fluid = self.model.properties._get_property("fluid", line_id=self.line_ids[0])
            if fluid is None:
                return None
            return fluid.pressure
        else:
            return None