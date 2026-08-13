from PySide6.QtCore import Qt

from pulse import app
from pulse.interface.ui_generated.plots.results.structural.get_stresses_for_harmonic_analysis_ui import GetStressesForHarmonicAnalysis_UI
from pulse.postprocessing.structural_postprocessing import get_stress_spectrum_data
from pulse.interface.user_input.data_handler.export_model_results import ExportModelResults
from pulse.interface.user_input.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from pulse.interface.user_input.project.loading_window import LoadingWindow


import logging
import numpy as np

class PlotStressesForHarmonicAnalysis(GetStressesForHarmonicAnalysis_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app().main_window.set_input_widget(self)

        self._config_window()
        self._initialize()
        self._load_structural_solver()
        self._create_connections()
        self.selection_callback()

    def _initialize(self):

        self.stresses_data = None

        self.stresses_labels = np.array(
            ["Normal axial", "Normal bending y", "Normal bending z", "Hoop", "Torsional shear", "Transversal shear xy", "Transversal shear xz"]
        )

        self.before_run = app().project.get_pre_solution_model_checks()

    @property
    def model(self):
        return app().project.model

    @property
    def structural_solver(self):
        return app().project.structural_solver

    def _load_structural_solver(self):

        if self.structural_solver is not None:
            return

        def process_cross_sections():
            logging.info("Processing the cross-sections [75%]")
            self.model.preprocessor.process_cross_sections_mapping()

        LoadingWindow(process_cross_sections).run()

        app().project.structural_solver = app().project.get_structural_solver()
        if self.structural_solver.solution is None:
            self.structural_solver.solution = self.model.structural_solution

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _create_connections(self):
        #
        self.checkBox_damping_effect.stateChanged.connect(self._update_damping_effect)
        #
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

    def get_stress_data(self, element_id):

        index = self.comboBox_stress_type.currentIndex()
        damping_effect = self.checkBox_damping_effect.isChecked()

        if self.stresses_data is None or self.update_damping:
            self.stresses_data = self.structural_solver.stress_calculate(damping=damping_effect)
            self.update_damping = False

        return get_stress_spectrum_data(self.stresses_data, element_id, index)
        
    def join_model_data(self):

        self.model_results = dict()
        title = f"Structural frequency response - {app().project.analysis_method} method"

        index = self.comboBox_stress_type.currentIndex()
        stress_label = self.stresses_labels[index]

        for k, element_id in enumerate(self.element_ids):
                
            key = ("element", element_id)
            legend_label = f"{stress_label} stress at element [{element_id}]"

            self.model_results[key] = {
                "x_data": self.model.frequencies,
                "y_data": self.get_stress_data(element_id),
                "x_label": "Frequency [Hz]",
                "y_label": "Stress",
                "title": title,
                "data_information": legend_label,
                "legend": legend_label,
                "unit": "Pa",
                "color": self.get_color(k),
                "linestyle": "-",
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