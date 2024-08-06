from PyQt5.QtWidgets import QLineEdit, QPushButton, QRadioButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.postprocessing.plot_structural_data import get_structural_frf
from pulse.interface.user_input.data_handler.export_model_results import ExportModelResults
from pulse.interface.user_input.plots.general.frequency_response_plotter import FrequencyResponsePlotter


class GetNodalResultsForHarmonicAnalysis(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/results/structural/get_nodal_results_for_harmonic_analysis.ui"
        uic.loadUi(ui_path, self)

        main_window = app().main_window

        app().main_window.set_input_widget(self)
        self.project = main_window.project

        self._initialize()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self.selection_callback()

    def _initialize(self):
        self.dof_labels = ["Ux", "Uy", "Uz", "Rx", "Ry", "Rz"]

        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()
        self.nodes = self.project.preprocessor.nodes
        self.analysisMethod = self.project.analysis_method_label
        self.frequencies = self.project.frequencies
        self.solution = self.project.get_structural_solution()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # LineEdit
        self.lineEdit_node_id : QLineEdit

        # PushButton
        self.pushButton_export_data : QPushButton
        self.pushButton_plot_data : QPushButton

        # RadioButton
        self.radioButton_ux : QRadioButton
        self.radioButton_uy : QRadioButton
        self.radioButton_uz : QRadioButton
        self.radioButton_rx : QRadioButton
        self.radioButton_ry : QRadioButton
        self.radioButton_rz : QRadioButton

    def _create_connections(self):
        #
        self.pushButton_export_data.clicked.connect(self.call_data_exporter)
        self.pushButton_plot_data.clicked.connect(self.call_plotter)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):
        selected_nodes = app().main_window.list_selected_nodes()
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

        str_nodes = self.lineEdit_node_id.text()
        stop, self.node_ids = self.before_run.check_selected_ids(str_nodes, "nodes", single_id=True)
        if stop:
            self.lineEdit_node_id.setFocus()
            return True

        if self.radioButton_ux.isChecked():
            self.local_dof = 0

        elif self.radioButton_uy.isChecked():
            self.local_dof = 1

        elif self.radioButton_uz.isChecked():
            self.local_dof = 2

        elif self.radioButton_rx.isChecked():
            self.local_dof = 3

        elif self.radioButton_ry.isChecked():
            self.local_dof = 4

        else:
            self.local_dof = 5

        self.local_dof_label = self.dof_labels[self.local_dof]

        if self.local_dof in [0, 1, 2]:
            self.unit_label = "m"
        else:
            self.unit_label = "rad"

        return False

    def get_response(self, node_id):
        response = get_structural_frf(  self.preprocessor,
                                        self.solution,
                                        node_id, 
                                        self.local_dof  )
        return response

    def join_model_data(self):

        self.model_results = dict()
        self.title = f"Structural frequency response - {self.analysisMethod}"
        legend_label = f"Response {self.local_dof_label} at node {self.node_ids}"
        data_information = f"Structural nodal response {self.local_dof_label} at node {self.node_ids}"

        for node_id in self.node_ids:

            key = ("node", node_id)
            self.model_results[key] = {  
                                        "x_data" : self.frequencies,
                                        "y_data" : self.get_response(node_id),
                                        "x_label" : "Frequency [Hz]",
                                        "y_label" : "Nodal response",
                                        "title" : self.title,
                                        "data_information" : data_information,
                                        "legend" : legend_label,
                                        "unit" : self.unit_label,
                                        "color" : [0,0,1],
                                        "linestyle" : "-"  
                                        }

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.call_plotter()
        elif event.key() == Qt.Key_Escape:
            self.close()