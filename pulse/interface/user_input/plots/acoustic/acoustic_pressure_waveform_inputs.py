from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from pulse import app
from pulse.interface.ui_generated.plots.results.acoustic.acoustic_pressure_waveform_inputs_ui import AcousticPressureWaveformInputs_UI
from pulse.interface.user_input.data_handler.export_model_results import ExportModelResults
from pulse.interface.user_input.plots.general.frequency_response_plotter import DataFormat, FrequencyResponsePlotter
from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf

from pulse.utils.signal_processing import process_ifft_from_one_sided_spectrum_signal

import numpy as np


class AcousticPressureWaveformInputs(AcousticPressureWaveformInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app().main_window.set_input_widget(self)

        self.project = app().project
        self.model = app().project.model
        self.mesh = app().project.model.mesh

        self._initialize()
        self._create_connections()
    
    def _initialize(self):

        self.exporter = None
        self.plotter = None
        self.unit_label = "Pa"
        self.model_results = dict()

        self.frequencies = self.model.frequencies
        self.solution = self.project.get_acoustic_solution()
        self.before_run = self.project.get_pre_solution_model_checks()
        self.analysis_method = self.project.analysis_method

    def showEvent(self, event):
        super().showEvent(event)

    def _create_connections(self):
        #
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):

        selected_nodes = selected_nodes = app().main_window.list_selected_nodes()
        if selected_nodes:
            text = ", ".join([str(i) for i in selected_nodes])
            self.lineEdit_selection_id.setText(text)

    def check_selected_ids(self):
        selection_id = self.lineEdit_selection_id.text()
        stop, self.selected_ids = self.before_run.check_selected_ids(selection_id, "nodes")
        if stop:
            self.lineEdit_selection_id.setFocus()
            return True

    def plot_data_callback(self):

        if self.check_selected_ids():
            return

        self.join_model_data()
        self.plotter = FrequencyResponsePlotter()
        self.plotter = FrequencyResponsePlotter(close_dialogs=True)
        self.plotter.comboBox_data_format.setCurrentIndex(DataFormat.REAL)
        self.plotter.data_format_changed_callback()
        self.plotter.frame_hlines_main.setDisabled(True)
        self.plotter._set_model_results_data_to_plot(self.model_results)

    def export_data_callback(self):

        if self.check_selected_ids():
            return

        self.join_model_data()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def get_response(self, node_id: int):

        response = get_acoustic_frf(app().project.model.preprocessor, self.solution, node_id)
        if complex(0) in response:
            response += 1e-12

        return response

    def join_model_data(self):

        self.model_results.clear()
        self.title = "Acoustic pressure waveform"

        for i, selected_id in enumerate(self.selected_ids):

            key = ("node", (selected_id))
            legend_label = f"Acoustic pressure at node [{selected_id}]"

            Xf = self.get_response(selected_id)
            time_vector, acoustic_pressure = process_ifft_from_one_sided_spectrum_signal(
                self.frequencies, 
                Xf,
                )

            self.model_results[key] = { 
                "x_data" : time_vector,
                "y_data" : acoustic_pressure,
                "x_label" : "Time [s]",
                "y_label" : "Acoustic pressure",
                "title" : self.title,
                "data_type" : "acoustic pressure",
                "legend" : legend_label,
                "unit" : self.unit_label,
                "color" : self.get_color(i),
                "linestyle" : "-"  
            }

    def get_color(self, index):

        colors = [  
                  (0,0,1), 
                  (0,0,0), 
                  (1,0,0),
                  (0,1,1), 
                  (1,0,1), 
                  (1,1,0),
                  (0.25,0.25,0.25)
                  ]

        if index <= 6:
            return colors[index]
        else:
            return tuple(np.random.randint(0, 255, size=3) / 255)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.plot_data_callback()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        if self.exporter is not None:
            self.exporter.close()

        if self.plotter is not None:
            self.plotter.close()

        return super().closeEvent(a0)
