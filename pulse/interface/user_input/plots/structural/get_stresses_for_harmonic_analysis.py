from PyQt5.QtWidgets import QCheckBox, QComboBox, QLineEdit, QPushButton, QRadioButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np

from pulse.postprocessing.plot_structural_data import get_stress_spectrum_data
from pulse.interface.user_input.data_handler.export_model_results import ExportModelResults
from pulse.interface.user_input.plots.general.frequency_response_plotter import FrequencyResponsePlotter

from pulse import app, UI_DIR

def get_icons_path(filename):
    path = f"data/icons/{filename}"
    if os.path.exists(path):
        return str(Path(path))

class GetStressesForHarmonicAnalysis(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = Path(f"{UI_DIR}/plots/results/structural/get_stresses_for_harmonic_analysis.ui")
        uic.loadUi(ui_path, self)

        main_window = app().main_window

        self.opv = main_window.opv_widget
        self.opv.setInputObject(self)
        self.project = main_window.project

        self._initialize()    
        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self.update()

    def _initialize(self):
        self.element_id = None
        self.keys = np.arange(7)
        self.labels = np.array(["Normal axial", 
                                "Normal bending y", 
                                "Normal bending z", 
                                "Hoop", 
                                "Torsional shear", 
                                "Transversal shear xy", 
                                "Transversal shear xz"])
        self.stress_data = []
        self.unit_label = "Pa"
        self.y_label = "Stress"

        self.preprocessor = self.project.preprocessor
        self.before_run = self.project.get_pre_solution_model_checks()
        self.frequencies = self.project.frequencies
        self.solve = self.project.structural_solve 
        self.analysis_method = self.project.analysis_method_label

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.pulse_icon)

    def _load_icons(self):
        self.pulse_icon = QIcon(get_icons_path('pulse.png'))
        self.update_icon = QIcon(get_icons_path('update_icon.jpg'))

    def _define_qt_variables(self):
        # QCheckBox
        self.checkBox_damping_effect = self.findChild(QCheckBox, 'checkBox_damping_effect')
        # QComboBox
        self.comboBox_stress_type = self.findChild(QComboBox, 'comboBox_stress_type')
        # QLineEdit
        self.lineEdit_element_id = self.findChild(QLineEdit, 'lineEdit_element_id')
        # QPushButton
        self.pushButton_export_data = self.findChild(QPushButton, 'pushButton_export_data')
        self.pushButton_plot_data = self.findChild(QPushButton, 'pushButton_plot_data')

    def _create_connections(self):
        #
        self.checkBox_damping_effect.stateChanged.connect(self._update_damping_effect)
        self.pushButton_export_data.clicked.connect(self.call_data_exporter)
        self.pushButton_plot_data.clicked.connect(self.call_plotter)

    def _update_damping_effect(self):
        self.update_damping = True

    def update(self):
        self.writeElements(self.opv.getListPickedElements())

    def writeElements(self, list_elements_ids):
        text = ""
        for node in list_elements_ids:
            text += "{}, ".format(node)
        self.lineEdit_element_id.setText(text)

    def check_inputs(self, export=False):

        lineEdit = self.lineEdit_element_id.text()
        stop, self.element_id = self.before_run.check_input_ElementID(lineEdit, 
                                                                      single_ID=True)
        
        if stop:
            return True
        
        index = self.comboBox_stress_type.currentIndex()
        self.stress_label = self.labels[index]
        self.stress_key = self.keys[index]

    def get_stress_data(self):

        if self.stress_data == [] or self.update_damping:
            _damping = self.checkBox_damping_effect.isChecked()
            self.stress_data = self.solve.stress_calculate(pressure_external = 0, 
                                                           damping_flag = _damping)
            self.update_damping = False

        response = get_stress_spectrum_data(self.stress_data, 
                                            self.element_id, 
                                            self.stress_key)
        
        return response
        
    def join_model_data(self):
        self.model_results = dict()
        self.title = "Structural frequency response - {}".format(self.analysis_method)
        legend_label = "{} stress at element {}".format(self.stress_label,
                                                        self.element_id)
        self.model_results = {  "x_data" : self.frequencies,
                                "y_data" : self.get_stress_data(),
                                "x_label" : "Frequency [Hz]",
                                "y_label" : self.y_label,
                                "title" : self.title,
                                "data_information" : legend_label,
                                "legend" : legend_label,
                                "unit" : self.unit_label,
                                "color" : [0,0,1],
                                "linestyle" : "-"  }

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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.call_plotter()
        elif event.key() == Qt.Key_Escape:
            self.close()