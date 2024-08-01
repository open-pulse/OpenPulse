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

        app().main_window.input_ui.set_input_widget(self)
        self.project = main_window.project

        self._initialize()
        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self.update()

    def _initialize(self):
        self.list_node_IDs = self.opv.getListPickedPoints()
        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()
        self.nodes = self.preprocessor.nodes
        self.analysis_method = self.project.analysis_method_label
        self.frequencies = self.project.frequencies
        self.solution = self.project.get_acoustic_solution()

    def _load_icons(self):
        self.pulse_icon = get_openpulse_icon()

    def _config_window(self):        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.pulse_icon)

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
        self.pushButton_plot_data.clicked.connect(self.call_plotter)
        self.pushButton_export_data.clicked.connect(self.call_data_exporter)

    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        self.lineEdit_node_id.setText(text)

    def update(self):
        self.list_node_IDs = self.opv.getListPickedPoints()
        if self.list_node_IDs != []:
            self.writeNodes(self.list_node_IDs)
        else:
            self.lineEdit_node_id.setFocus()

    def call_plotter(self):
        if self.check_inputs():
            return
        self.join_model_data()
        self.plotter = FrequencyResponsePlotter()
        self.plotter._set_data_to_plot(self.model_results)

    def call_data_exporter(self):
        if self.check_inputs():
            return
        self.join_model_data()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def check_inputs(self):
        lineEdit_node_id = self.lineEdit_node_id.text()
        stop, self.node_ID = self.before_run.check_input_NodeID(lineEdit_node_id, single_ID=True)
        if stop:
            self.lineEdit_node_id.setFocus()
            return True
        
    def get_response(self):
        
        response = get_acoustic_frf(self.preprocessor, self.solution, self.node_ID)

        if complex(0) in response:
            response += 1e-12

        return response

    def join_model_data(self):

        self.title = "Acoustic frequency response - {}".format(self.analysis_method)
        legend_label = "Acoustic pressure at node {}".format(self.node_ID)
        unit_label = "Pa"
        y_label = "Acoustic pressure"

        self.model_results = dict()
        self.model_results = {  "x_data" : self.frequencies,
                                "y_data" : self.get_response(),
                                "x_label" : "Frequency [Hz]",
                                "y_label" : y_label,
                                "title" : self.title,
                                "data_information" : legend_label,
                                "legend" : legend_label,
                                "unit" : unit_label,
                                "color" : [0,0,1],
                                "linestyle" : "-"  }

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.call_plotter()
        elif event.key() == Qt.Key_Escape:
            self.close()