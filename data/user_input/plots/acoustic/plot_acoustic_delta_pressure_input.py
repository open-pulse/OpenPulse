from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os

from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf
from data.user_input.data_handler.export_model_results import ExportModelResults
from data.user_input.plots.general.frequency_response_plotter import FrequencyResponsePlotter

def get_icons_path(filename):
    path = f"data/icons/{filename}"
    if os.path.exists(path):
        return str(Path(path))


class PlotAcousticDeltaPressuresInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui_files/plots_/results_/acoustic_/plot_acoustic_delta_pressures_input.ui'), self)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)

        self.projec = project
        self.analysis_method = project.analysis_method_label
        self.frequencies = project.frequencies
        self.solution = project.get_acoustic_solution()

        self.preprocessor = project.preprocessor
        self.before_run = project.get_pre_solution_model_checks()

        self._load_icons()
        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.writeNodes(self.opv.getListPickedPoints())
        self.exec()

    def _reset_variables(self):
        self.unit_label = "Pa"

    def _load_icons(self):
        self.pulse_icon = QIcon(get_icons_path('pulse.png'))
        self.update_icon = QIcon(get_icons_path('update_icon.jpg'))
        self.setWindowIcon(self.pulse_icon)

    def _define_qt_variables(self):
        # QLineEdit
        self.lineEdit_input_node_id = self.findChild(QLineEdit, 'lineEdit_input_node_id')   
        self.lineEdit_output_node_id = self.findChild(QLineEdit, 'lineEdit_output_node_id')
        # QPushButton
        self.pushButton_flip_nodes_1 = self.findChild(QPushButton, 'pushButton_flip_nodes_1')
        self.pushButton_flip_nodes_2 = self.findChild(QPushButton, 'pushButton_flip_nodes_2')
        self.pushButton_call_data_exporter = self.findChild(QPushButton, 'pushButton_call_data_exporter')
        self.pushButton_plot_frequency_response = self.findChild(QPushButton, 'pushButton_plot_frequency_response')
        self.pushButton_flip_nodes_1.setIcon(self.update_icon)
        self.pushButton_flip_nodes_2.setIcon(self.update_icon)

    def _create_connections(self):
        self.pushButton_call_data_exporter.clicked.connect(self.call_data_exporter)
        self.pushButton_plot_frequency_response.clicked.connect(self.call_plotter)
        self.pushButton_flip_nodes_1.clicked.connect(self.flip_nodes)
        self.pushButton_flip_nodes_2.clicked.connect(self.flip_nodes)

    def writeNodes(self, list_node_ids):
        if len(list_node_ids) == 2:
            self.lineEdit_input_node_id.setText(str(list_node_ids[-2]))
            self.lineEdit_output_node_id.setText(str(list_node_ids[-1]))
        elif len(list_node_ids) == 1:
            self.lineEdit_input_node_id.setText(str(list_node_ids[-1]))
            self.lineEdit_output_node_id.setText("")

    def flip_nodes(self):
        temp_text_input = self.lineEdit_input_node_id.text()
        temp_text_output = self.lineEdit_output_node_id.text()
        self.lineEdit_input_node_id.setText(temp_text_output)
        self.lineEdit_output_node_id.setText(temp_text_input)

    def update(self):
        self.writeNodes(self.opv.getListPickedPoints())

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

        lineEdit_input = self.lineEdit_input_node_id.text()
        stop, self.input_node_ID = self.before_run.check_input_NodeID(lineEdit_input, single_ID=True)
        if stop:
            self.lineEdit_input_node_id.setFocus()
            return True

        lineEdit_output = self.lineEdit_output_node_id.text()
        stop, self.output_node_ID = self.before_run.check_input_NodeID(lineEdit_output, single_ID=True)
        if stop:
            self.lineEdit_output_node_id.setFocus()
            return True

    def get_delta_pressures(self):

        P_input = get_acoustic_frf(self.preprocessor, self.solution, self.input_node_ID)
        P_output = get_acoustic_frf(self.preprocessor, self.solution, self.output_node_ID)

        delta_pressure = P_input - P_output
        
        if complex(0) in delta_pressure:
            # the zero_shift constant is summed to delta pressures to avoid zero values in log type plots
            zero_shift = 1*1e-12 
            delta_pressure += zero_shift 
        return delta_pressure

    def join_model_data(self):
        self.model_results = dict()
        self.title = "Acoustic frequency response - {}".format(self.analysis_method)
        legend_label = "Delta pressure between nodes {} and {}".format(self.input_node_ID, self.output_node_ID)
        self.model_results = {  "x_data" : self.frequencies,
                                "y_data" : self.get_delta_pressures(),
                                "x_label" : "Frequency [Hz]",
                                "y_label" : "Delta pressure",
                                "title" : self.title,
                                "data_information" : legend_label,
                                "legend" : legend_label,
                                "unit" : self.unit_label,
                                "color" : [0,0,1],
                                "linestyle" : "-"  }

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.call_plotter()
        elif event.key() == Qt.Key_Escape:
            self.close()