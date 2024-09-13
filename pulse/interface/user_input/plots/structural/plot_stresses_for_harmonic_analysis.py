from PyQt5.QtWidgets import QCheckBox, QComboBox, QLineEdit, QPushButton, QRadioButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.postprocessing.plot_structural_data import get_stress_spectrum_data
from pulse.interface.user_input.data_handler.export_model_results import ExportModelResults
from pulse.interface.user_input.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from pulse.interface.user_input.project.loading_window import LoadingWindow

import logging
import numpy as np

class PlotStressesForHarmonicAnalysis(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/results/structural/get_stresses_for_harmonic_analysis.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)

        self._config_window()
        self._initialize()
        self._load_structural_solver()
        self._define_qt_variables()
        self._create_connections()
        self.selection_callback()

    def _initialize(self):
        
        self.keys = np.arange(7)
        self.labels = np.array(["Normal axial", 
                                "Normal bending y", 
                                "Normal bending z", 
                                "Hoop", 
                                "Torsional shear", 
                                "Transversal shear xy", 
                                "Transversal shear xz"])
        
        self.stress_data = list()

        self.before_run = app().project.get_pre_solution_model_checks()

        self.frequencies = app().project.model.frequencies
        self.analysis_method = app().project.analysis_method_label
    
    def _load_structural_solver(self):

        if app().project.structural_solver is None:

            logging.info("Processing the cross-sections [75%]")
            def callback():
                app().project.model.preprocessor.process_cross_sections_mapping()
            LoadingWindow(callback).run()

            self.structural_solver = app().project.get_structural_solver()
            if self.structural_solver.solution is None:
                self.structural_solver.solution = app().project.structural_solution

        else:
            self.structural_solver = app().project.structural_solver

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QCheckBox
        self.checkBox_damping_effect : QCheckBox

        # QComboBox
        self.comboBox_stress_type : QComboBox

        # QLineEdit
        self.lineEdit_element_id : QLineEdit

        # QPushButton
        self.pushButton_export_data : QPushButton
        self.pushButton_plot_data : QPushButton

    def _create_connections(self):
        #
        self.checkBox_damping_effect.stateChanged.connect(self._update_damping_effect)
        #
        self.pushButton_export_data.clicked.connect(self.call_data_exporter)
        self.pushButton_plot_data.clicked.connect(self.call_plotter)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):
        selected_elements = app().main_window.list_selected_elements()
        if selected_elements:
            text = ", ".join([str(i) for i in selected_elements])
            self.lineEdit_element_id.setText(text)

    def _update_damping_effect(self):
        self.update_damping = True

    def check_inputs(self):

        str_elements = self.lineEdit_element_id.text()
        stop, self.element_ids = self.before_run.check_selected_ids(str_elements, "elements")

        if stop:
            return True

        index = self.comboBox_stress_type.currentIndex()
        self.stress_label = self.labels[index]
        self.stress_key = self.keys[index]

    def get_stress_data(self, element_id):

        if len(self.stress_data) == 0 or self.update_damping:
            damping_effect = self.checkBox_damping_effect.isChecked()

            self.stress_data = self.structural_solver.stress_calculate(damping = damping_effect)
            self.update_damping = False

        response = get_stress_spectrum_data(
                                            self.stress_data, 
                                            element_id, 
                                            self.stress_key
                                            )

        return response
        
    def join_model_data(self):

        self.model_results = dict()
        title = f"Structural frequency response - {self.analysis_method}"

        for k, element_id in enumerate(self.element_ids):
                
            key = ("element", element_id)
            legend_label = f"{self.stress_label} stress at element [{element_id}]"

            self.model_results[key] = {  
                                        "x_data" : self.frequencies,
                                        "y_data" : self.get_stress_data(element_id),
                                        "x_label" : "Frequency [Hz]",
                                        "y_label" : "Stress",
                                        "title" : title,
                                        "data_information" : legend_label,
                                        "legend" : legend_label,
                                        "unit" : "Pa",
                                        "color" : self.get_color(k),
                                        "linestyle" : "-"  
                                       }

    def get_color(self, index):

        colors = [  (0,0,1), 
                    (0,0,0), 
                    (1,0,0),
                    (0,1,1), 
                    (1,0,1), 
                    (1,1,0),
                    (0.25,0.25,0.25)  ]
        
        if index <= 6:
            return colors[index]
        else:
            return tuple(np.random.randint(0, 255, size=3) / 255)

    def call_plotter(self):
        if self.check_inputs():
            return
        self.join_model_data()
        self.plotter = FrequencyResponsePlotter()
        self.plotter._set_model_results_data_to_plot(self.model_results)

    def call_data_exporter(self):
        if self.check_inputs():
            return
        self.join_model_data()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.call_plotter()
        elif event.key() == Qt.Key_Escape:
            self.close()