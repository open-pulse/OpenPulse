from PySide6.QtWidgets import QComboBox, QLabel, QLineEdit, QPushButton, QWidget
from PySide6.QtCore import Qt

from pulse import app, UI_DIR
from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf
from pulse.interface.user_input.plots.general.frequency_response_plotter import FrequencyResponsePlotter

from molde import load_ui

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

psi_to_Pa = (0.45359237 * 9.80665) / ((0.0254)**2)
kgf_cm2_to_Pa = 9.80665e4

class ReciprocatingPumpPulsationCriteriaInput(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "criterias/reciprocating_pump_pulsation_criteria_widget.ui"
        load_ui(ui_path, self)

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
        self.comboBox_line_ids: QComboBox

        # QLabel
        self.label_selected_id: QLabel

        # QLineEdit
        self.lineEdit_selected_id: QLineEdit
        self.lineEdit_internal_diameter : QLineEdit

        # QPushButton
        self.pushButton_plot_criteria : QPushButton

    def _create_connections(self):
        #
        self.pushButton_plot_criteria.clicked.connect(self.plot_pulsation_criteria)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        self.reset_input_fields()

        selected_nodes = app().main_window.list_selected_nodes()
        line_ids = self.preprocessor.get_line_from_node_id(selected_nodes)

        if len(selected_nodes) == 1:

            if len(line_ids) > 0:
                self.comboBox_line_ids.clear()
                for line_id in line_ids:
                    self.comboBox_line_ids.addItem(f"      {line_id}")

            inner_diameter = self.get_internal_diameter_from_line()
            if inner_diameter is None:
                return

            self.lineEdit_selected_id.setText(str(selected_nodes[0]))
            self.lineEdit_internal_diameter.setText(str(round(inner_diameter, 2)))
            self.pushButton_plot_criteria.setDisabled(False)

    def get_acoustic_pressure(self, node_id: int):

        response = get_acoustic_frf(self.preprocessor, self.solution, node_id)
        if complex(0) in response:
            response += np.ones(len(response), dtype=float)*(1e-12)

        return response

    def plot_pulsation_criteria(self):

        node_ids = app().main_window.list_selected_nodes()

        if len(node_ids) == 1:

            node_id = node_ids[0]
            acoustic_pressure = (2 / 1000) * self.get_acoustic_pressure(node_id)

            self.model_results = dict()
            title = "Allowable Pulsation Limits at and Beyond Line-side\n Connections of Pulsation Suppression Devices"       
            legend_label = "Acoustic pressure at node {}".format(node_id)

            key = ("acoustic_pressure", (node_id))

            self.model_results[key] = { 
                                        "x_data" : self.frequencies,
                                        "y_data" : acoustic_pressure,
                                        "x_label" : "Frequency [Hz]",
                                        "y_label" : "Acoustic pressure",
                                        "title" : title,
                                        "data_information" : legend_label,
                                        "legend" : legend_label,
                                        "unit" : "kPa (peak-to-peak)",
                                        "color" : [0,0,0],
                                        "linestyle" : "-" 
                                    }

            df = 0.2
            f_max = self.frequencies[-1]
            freq = np.arange(df, f_max + df, df)
            
            inner_diameter = self.get_internal_diameter_from_line()
            if inner_diameter is None:
                return

            # allowable peak-to-peak pulsation levels in kPa
            P_1 = 3500 / ((inner_diameter * freq)**(1/2))

            legend_label = "Pulsation criteria"

            key = ("pulsation_criteria", (node_id))

            self.model_results[key] = { 
                                        "x_data" : freq,
                                        "y_data" : P_1,
                                        "x_label" : "Frequency [Hz]",
                                        "y_label" : "Acoustic pressure",
                                        "title" : title,
                                        "data_information" : legend_label,
                                        "legend" : legend_label,
                                        "unit" : "kPa (peak-to-peak)",
                                        "color" : [1,0,0],
                                        "linestyle" : "-"  
                                    }

            self.plotter = FrequencyResponsePlotter()
            self.plotter._set_model_results_data_to_plot(self.model_results)

    def get_internal_diameter_from_line(self):

        line_id = int(self.comboBox_line_ids.currentText().replace(" ", ""))

        cross_section = self.model.properties._get_property("cross_section", line_id=line_id)
        if cross_section is None:
            return None

        inner_diameter = cross_section.inner_diameter

        return 1000 * inner_diameter

    def reset_input_fields(self):
        self.lineEdit_selected_id.setText("")
        self.lineEdit_internal_diameter.setText("")
        self.pushButton_plot_criteria.setDisabled(True)