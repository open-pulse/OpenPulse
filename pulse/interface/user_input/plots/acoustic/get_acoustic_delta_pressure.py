from PyQt5.QtWidgets import QLineEdit, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QEvent, QObject, Qt
from PyQt5 import uic
from pathlib import Path

import os

from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf
from pulse.interface.user_input.data_handler.export_model_results import ExportModelResults
from pulse.interface.user_input.plots.general.frequency_response_plotter import FrequencyResponsePlotter

from pulse import app, UI_DIR

def get_icons_path(filename):
    path = f"data/icons/{filename}"
    if os.path.exists(path):
        return str(Path(path))

class GetAcousticDeltaPressure(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        main_window = app().main_window

        ui_path = Path(f"{UI_DIR}/plots/results/acoustic/get_acoustic_delta_pressures.ui")
        uic.loadUi(ui_path, self)

        self.opv = main_window.getOPVWidget()
        self.opv.setInputObject(self)
        self.project = main_window.getProject()

        self._initialize()
        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self.update()

    def _initialize(self):
        self.unit_label = "Pa"
        self.analysis_method = self.project.analysis_method_label
        self.frequencies = self.project.frequencies
        self.solution = self.project.get_acoustic_solution()
        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()

    def _load_icons(self):
        self.pulse_icon = QIcon(get_icons_path('pulse.png'))
        self.update_icon = QIcon(get_icons_path('update_icon.jpg'))

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.pulse_icon)

    def _define_qt_variables(self):
        # QLineEdit
        self.lineEdit_input_node_id = self.findChild(QLineEdit, 'lineEdit_input_node_id')   
        self.lineEdit_output_node_id = self.findChild(QLineEdit, 'lineEdit_output_node_id')
        self.current_lineEdit = self.lineEdit_input_node_id
        # QPushButton
        self.pushButton_flip_nodes = self.findChild(QPushButton, 'pushButton_flip_nodes')
        self.pushButton_export_data = self.findChild(QPushButton, 'pushButton_export_data')
        self.pushButton_plot_data = self.findChild(QPushButton, 'pushButton_plot_data')
        self.pushButton_flip_nodes.setIcon(self.update_icon)

    def _create_connections(self):
        self.pushButton_export_data.clicked.connect(self.call_data_exporter)
        self.pushButton_plot_data.clicked.connect(self.call_plotter)
        self.pushButton_flip_nodes.clicked.connect(self.flip_nodes)
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
        self.list_node_ids = self.opv.getListPickedPoints()
        if self.list_node_ids != []:
            self.writeNodes(self.list_node_ids)
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
        stop, self.input_node_id = self.before_run.check_input_NodeID(lineEdit_input_node_id, single_ID=True)
        if stop:
            self.lineEdit_input_node_id.setFocus()
            return True

        lineEdit_output_node_id = self.lineEdit_output_node_id.text()
        stop, self.output_node_id = self.before_run.check_input_NodeID(lineEdit_output_node_id, single_ID=True)
        if stop:
            self.lineEdit_output_node_id.setFocus()
            return True

    def get_delta_pressures(self):

        P_input = get_acoustic_frf(self.input_node_id)
        P_output = get_acoustic_frf(self.output_node_id)

        delta_pressure = P_input - P_output
        
        if complex(0) in delta_pressure:
            # the zero_shift constant is summed to delta pressures to avoid zero values in log type plots
            zero_shift = 1e-12 
            delta_pressure += zero_shift 
        return delta_pressure

    def join_model_data(self):
        self.model_results = dict()
        self.title = "Acoustic frequency response - {}".format(self.analysis_method)
        legend_label = "Delta pressure between nodes {} and {}".format(self.input_node_id, self.output_node_id)
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