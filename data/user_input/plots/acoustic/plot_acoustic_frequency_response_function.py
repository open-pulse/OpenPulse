from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
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

class PlotAcousticFrequencyResponseFunctionInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui_files/plots_/results_/acoustic_/plot_acoustic_frequency_response_function.ui'), self)
        
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
        self.update()
        self.exec()

    def _load_icons(self):
        self.pulse_icon = QIcon(get_icons_path('pulse.png'))
        self.export_icon = QIcon(get_icons_path('send_to_disk.png'))
        self.update_icon = QIcon(get_icons_path('update_icon.jpg'))
        self.setWindowIcon(self.pulse_icon)

    def _reset_variables(self):
        pass

    def _define_qt_variables(self):
        # QFrame
        self.frame_denominator = self.findChild(QFrame, 'frame_denominator')
        self.frame_numerator = self.findChild(QFrame, 'frame_numerator')
        # QLineEdit
        self.lineEdit_input_node_id = self.findChild(QLineEdit, 'lineEdit_input_node_id')
        self.lineEdit_output_node_id = self.findChild(QLineEdit, 'lineEdit_output_node_id')
        self.current_lineEdit = self.lineEdit_output_node_id
        # QPushButton
        self.pushButton_call_data_exporter = self.findChild(QPushButton, 'pushButton_call_data_exporter')
        self.pushButton_flip_selection = self.findChild(QPushButton, 'pushButton_flip_selection')
        self.pushButton_plot_frequency_response = self.findChild(QPushButton, 'pushButton_plot_frequency_response')
        #
        self.pushButton_call_data_exporter.setIcon(self.export_icon)
        self.pushButton_flip_selection.setIcon(self.update_icon)

    def _create_connections(self):
        self.pushButton_call_data_exporter.clicked.connect(self.call_data_exporter)
        self.pushButton_plot_frequency_response.clicked.connect(self.call_plotter)
        self.pushButton_flip_selection.clicked.connect(self.flip_nodes)
        #
        self.clickable(self.lineEdit_input_node_id).connect(self.lineEdit_1_clicked)
        self.clickable(self.lineEdit_output_node_id).connect(self.lineEdit_2_clicked)

    def clickable(self, widget):
        class Filter(QObject):
            clicked = pyqtSignal()

            def eventFilter(self, obj, event):
                if obj == widget and event.type() == QEvent.MouseButtonRelease and obj.rect().contains(event.pos()):
                    self.clicked.emit()
                    return True
                else:
                    return False

        filter = Filter(widget)
        widget.installEventFilter(filter)
        return filter.clicked

    def lineEdit_1_clicked(self):
        self.current_lineEdit = self.lineEdit_input_node_id

    def lineEdit_2_clicked(self):
        self.current_lineEdit = self.lineEdit_output_node_id

    def writeNodes(self, list_node_ids):
        node_id = list_node_ids[0]
        self.current_lineEdit.setText(str(node_id))

    def update(self):
        self.list_node_IDs = self.opv.getListPickedPoints()
        if self.list_node_IDs != []:
            self.writeNodes(self.list_node_IDs)
        else:
            self.current_lineEdit.setFocus()

    def flip_nodes(self):
        temp_text_input = self.lineEdit_input_node_id.text()
        temp_text_output = self.lineEdit_output_node_id.text()
        self.lineEdit_input_node_id.setText(temp_text_output)
        self.lineEdit_output_node_id.setText(temp_text_input) 

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
        lineEdit_input_node_id = self.lineEdit_input_node_id.text()
        stop, self.node_ID_1 = self.before_run.check_input_NodeID(lineEdit_input_node_id, single_ID=True)
        if stop:
            self.lineEdit_input_node_id.setFocus()
            return True
        
        lineEdit_output_node_id = self.lineEdit_output_node_id.text()
        stop, self.node_ID_2 = self.before_run.check_input_NodeID(lineEdit_output_node_id, single_ID=True)
        if stop:
            self.lineEdit_output_node_id.setFocus()
            return True

    def get_response(self):
        
        numerator = get_acoustic_frf(   self.preprocessor, 
                                        self.solution,
                                        self.node_ID_2   )

        denominator = get_acoustic_frf( self.preprocessor, 
                                        self.solution,
                                        self.node_ID_1 )
        if complex(0) in denominator:
            denominator += 1e-12

        response = numerator/denominator
        if complex(0) in response:
            response += 1e-12

        return response

    def join_model_data(self):

        self.title = "Acoustic frequency response - {}".format(self.analysis_method)
        legend_label = "Acoustic pressure ratio between nodes {} and {}".format(self.node_ID_1, self.node_ID_2)
        unit_label = "--"
        y_label = "Acoustic pressure ratio"

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