from PyQt5.QtWidgets import QFrame, QLineEdit, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf
from pulse.interface.user_input.data_handler.export_model_results import ExportModelResults
from pulse.interface.user_input.plots.general.frequency_response_plotter import FrequencyResponsePlotter

window_title_1 = "Error"
window_title_2 = "Warning"

class GetAcousticFrequencyResponse(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        main_window = app().main_window

        ui_path = UI_DIR / "plots/results/acoustic/get_acoustic_frequency_response.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.project = main_window.project

        self._initialize()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self.selection_callback()

    def _initialize(self):
        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()
        self.nodes = self.preprocessor.nodes
        self.analysis_method = self.project.analysis_method_label
        self.frequencies = self.project.frequencies
        self.solution = self.project.get_acoustic_solution()

    def _config_window(self):        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)

    def _define_qt_variables(self):

        # QFrame
        self.frame_denominator : QFrame
        self.frame_numerator : QFrame

        # QLineEdit
        self.lineEdit_node_id : QLineEdit

        # QPushButton
        self.pushButton_plot_data : QPushButton
        self.pushButton_export_data : QPushButton

    def _create_connections(self):
        #
        self.pushButton_plot_data.clicked.connect(self.call_plotter)
        self.pushButton_export_data.clicked.connect(self.call_data_exporter)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):
        selected_nodes = app().main_window.selected_nodes
        if selected_nodes:
            text = ", ".join([str(i) for i in selected_nodes])
            self.lineEdit_node_id.setText(text)

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

    def check_inputs(self):
        lineEdit_node_id = self.lineEdit_node_id.text()
        stop, self.selected_node_ids = self.before_run.check_selected_ids(lineEdit_node_id, "nodes")
        if stop:
            self.lineEdit_node_id.setFocus()
            return True

    def get_response(self, node_id):
        response = get_acoustic_frf(self.preprocessor, self.solution, node_id)
        if complex(0) in response:
            response += 1e-12
        return response

    def join_model_data(self):

        self.title = f"Acoustic frequency response - {self.analysis_method}"
        legend_label = f"Acoustic pressure at node {self.selected_node_ids}"
        y_label = "Acoustic pressure"
        unit_label = "Pa"

        self.model_results = dict()
        for index, node_id in enumerate(self.selected_node_ids):
        
            key = ("line", (node_id))
            self.model_results[key] = {
                                        "x_data" : self.frequencies,
                                        "y_data" : self.get_response(node_id),
                                        "x_label" : "Frequency [Hz]",
                                        "y_label" : y_label,
                                        "title" : self.title,
                                        "data_information" : legend_label,
                                        "legend" : legend_label,
                                        "unit" : unit_label,
                                        "color" : self.get_color(index),
                                        "linestyle" : "-"
                                      }

    def get_color(self, index):

        colors = [  (0,0,1), (0,0,0), (1,0,0),
                    (0,1,1), (1,0,1), (1,1,0),
                    (0.25,0.25,0.25)  ]
        
        if index <= 6:
            return colors[index]
        else:
            return tuple(np.random.randint(0, 255, size=3) / 255)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.call_plotter()
        elif event.key() == Qt.Key_Escape:
            self.close()