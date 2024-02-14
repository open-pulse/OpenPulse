from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QRadioButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os

from pulse.postprocessing.plot_structural_data import get_structural_frf
from pulse.interface.user_input.data_handler.export_model_results import ExportModelResults
from pulse.interface.user_input.plots.general.frequency_response_plotter import FrequencyResponsePlotter

def get_icons_path(filename):
    path = f"data/icons/{filename}"
    if os.path.exists(path):
        return str(Path(path))

class PlotStructuralFrequencyResponseInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('pulse/interface/ui_files/plots/results/structural/plot_structural_frequency_response.ui'), self)

        self.opv = opv
        self.opv.setInputObject(self)
        
        self.preprocessor = project.preprocessor
        self.before_run = project.get_pre_solution_model_checks()
        self.list_node_IDs = self.opv.getListPickedPoints()

        self.nodes = project.preprocessor.nodes
        self.analysisMethod = project.analysis_method_label
        self.frequencies = project.frequencies
        self.solution = project.get_structural_solution()

        self._config_window()
        self._load_icons()
        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.writeNodes(self.list_node_IDs)
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

    def _define_qt_variables(self):
        # LineEdit
        self.lineEdit_node_id = self.findChild(QLineEdit, 'lineEdit_node_id')
        # PushButton
        self.pushButton_call_data_exporter = self.findChild(QPushButton, 'pushButton_call_data_exporter')
        self.pushButton_plot_frequency_response = self.findChild(QPushButton, 'pushButton_plot_frequency_response')
        self.pushButton_call_data_exporter.setIcon(self.export_icon)
        # RadioButton
        self.radioButton_ux = self.findChild(QRadioButton, 'radioButton_ux')
        self.radioButton_uy = self.findChild(QRadioButton, 'radioButton_uy')
        self.radioButton_uz = self.findChild(QRadioButton, 'radioButton_uz')
        self.radioButton_rx = self.findChild(QRadioButton, 'radioButton_rx')
        self.radioButton_ry = self.findChild(QRadioButton, 'radioButton_ry')
        self.radioButton_rz = self.findChild(QRadioButton, 'radioButton_rz')

    def _reset_variables(self):
        self.dof_labels = ["Ux", "Uy", "Uz", "Rx", "Ry", "Rz"]

    def _create_connections(self):
        self.pushButton_call_data_exporter.clicked.connect(self.call_data_exporter)
        self.pushButton_plot_frequency_response.clicked.connect(self.call_plotter)
    
    def _load_icons(self):
        self.pulse_icon = QIcon(get_icons_path('pulse.png'))
        self.export_icon = QIcon(get_icons_path('send_to_disk.png'))
        self.setWindowIcon(self.pulse_icon)

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

    def get_response(self):
        response = get_structural_frf(self.preprocessor, 
                                      self.solution,
                                      self.node_ID, 
                                      self.local_dof)
        return response

    def join_model_data(self):
        self.model_results = dict()
        self.title = "Structural frequency response - {}".format(self.analysisMethod)
        legend_label = "Response {} at node {}".format(self.local_dof_label, self.node_ID)
        data_information = "Structural nodal response {} at node {}".format(self.local_dof_label, self.node_ID)
        self.model_results = {  "x_data" : self.frequencies,
                                "y_data" : self.get_response(),
                                "x_label" : "Frequency [Hz]",
                                "y_label" : "Nodal response",
                                "title" : self.title,
                                "data_information" : data_information,
                                "legend" : legend_label,
                                "unit" : self.unit_label,
                                "color" : [0,0,1],
                                "linestyle" : "-"  }

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.call_plotter()
        elif event.key() == Qt.Key_Escape:
            self.close()