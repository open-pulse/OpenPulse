from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np

from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf
from data.user_input.data_handler.export_model_results import ExportModelResults
from data.user_input.plots.general.frequency_response_plotter import FrequencyResponsePlotter

def get_icons_path(filename):
    path = f"data/icons/{filename}"
    if os.path.exists(path):
        return str(Path(path))

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"

class PlotAcousticFrequencyResponseInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui_files/plots_/results_/acoustic_/plot_acoustic_frequency_response_input.ui'), self)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)
        self.list_node_IDs = self.opv.getListPickedPoints()

        self.projec = project
        self.preprocessor = project.preprocessor
        self.before_run = project.get_pre_solution_model_checks()

        self.nodes = self.preprocessor.nodes
        self.analysis_method = project.analysis_method_label
        self.frequencies = project.frequencies
        self.solution = project.get_acoustic_solution()

        self._load_icons()
        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.writeNodes(self.list_node_IDs)
        self.exec()

    def _load_icons(self):
        self.pulse_icon = QIcon(get_icons_path('pulse.png'))
        self.export_icon = QIcon(get_icons_path('send_to_disk.png'))
        self.setWindowIcon(self.pulse_icon)

    def _reset_variables(self):
        self.unit_label = "Pa"

    def _define_qt_variables(self):
        self.lineEdit_node_id = self.findChild(QLineEdit, 'lineEdit_node_id')
        self.pushButton_call_data_exporter = self.findChild(QPushButton, 'pushButton_call_data_exporter')
        self.pushButton_plot_frequency_response = self.findChild(QPushButton, 'pushButton_plot_frequency_response')
        self.pushButton_call_data_exporter.setIcon(self.export_icon)

    def _create_connections(self):
        self.pushButton_call_data_exporter.clicked.connect(self.call_data_exporter)
        self.pushButton_plot_frequency_response.clicked.connect(self.call_plotter)
    
    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        self.lineEdit_node_id.setText(text)

    def update(self):
        self.list_node_IDs = self.opv.getListPickedPoints()
        if self.list_node_IDs != []:
            self.writeNodes(self.list_node_IDs)

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
        response = get_acoustic_frf(self.preprocessor, 
                                      self.solution,
                                      self.node_ID)
        if complex(0) in response:
            response += np.ones(len(response), dtype=float)*(1e-12)
        return response

    def join_model_data(self):
        # if float(0) in self.frequencies:
        #     shift = 1
        # else:
        #     shift = 0
        self.model_results = dict()
        self.title = "Acoustic frequency response - {}".format(self.analysis_method)
        legend_label = "Acoustic pressure at node {}".format(self.node_ID)
        self.model_results = {  "x_data" : self.frequencies,
                                "y_data" : self.get_response(),
                                "x_label" : "Frequency [Hz]",
                                "y_label" : "Nodal response",
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