from PyQt5.QtWidgets import QDialog, QCheckBox, QFileDialog, QLabel, QLineEdit, QPushButton, QTableWidget, QTabWidget, QTableWidgetItem, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.interface.user_input.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from pulse.tools.utils import get_new_path

import os
import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

class ShakingForcesCriteriaInput(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "criterias/shaking_forces_criteria_widget.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)

        self.project = app().project
        self.preprocessor = app().project.preprocessor

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        # self._config_widgets()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):
        self.keep_window_open = True
        self.complete = False
        self.unit_label = "N"

    def _define_qt_variables(self):

        # QCheckBox
        self.checkBox_force_Fx : QCheckBox
        self.checkBox_force_Fy : QCheckBox
        self.checkBox_force_Fz : QCheckBox
        self.checkBox_resultant_force : QCheckBox

        # QLineEdit
        self.lineEdit_selection_id : QLineEdit

        # QPushButton
        self.pushButton_confirm : QPushButton

    def _config_widgets(self):
        ConfigWidgetAppearance(self, tool_tip=True)

    def _create_connections(self):
        self.pushButton_confirm.clicked.connect(self.plot_force_spectrum)
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):
        selected_lines = app().main_window.list_selected_lines()
        if selected_lines:
            text = ", ".join([str(i) for i in selected_lines])
            self.lineEdit_selection_id.setText(text)

    def process_shaking_forces_for_selected_lines(self):

        self.before_run = self.project.get_pre_solution_model_checks()

        lineEdit = self.lineEdit_selection_id
        stop, self.lines_typed = self.before_run.check_selected_ids(lineEdit.text(), "lines")
        if stop:
            lineEdit.setFocus()
            return True
        
        element_ids = list()
        for line_id in self.lines_typed:
            elements_from_line = self.preprocessor.line_to_elements[line_id]
            element_ids.extend(elements_from_line)
        
        pressure_external = 0
        frequencies = self.project.frequencies

        rows = self.preprocessor.DOFS_ELEMENT
        cols = len(frequencies)
        pressure_loads = np.zeros((rows, cols), dtype=complex)

        for row, element_id in enumerate(element_ids):

            element = self.preprocessor.structural_elements[element_id]

            pressure_first = self.project.solution_acoustic[element.first_node.global_index, :]
            pressure_last = self.project.solution_acoustic[element.last_node.global_index, :]
            pressure = np.c_[pressure_first, pressure_last].T

            pressure_loads += element.force_vector_acoustic_gcs(frequencies, pressure, pressure_external)

        F_x = pressure_loads[0] + pressure_loads[6]
        F_y = pressure_loads[1] + pressure_loads[7]
        F_z = pressure_loads[2] + pressure_loads[8]
        F_res = (F_x**2 + F_y** + F_z**2)**(1/2)

        shaking_forces = {
                            "F_x" : F_x,
                            "F_y" : F_y,
                            "F_z" : F_z,
                            "F_res" : F_res,
                         }

        return shaking_forces

    def plot_force_spectrum(self):

        shaking_forces = self.process_shaking_forces_for_selected_lines()

        x_data = self.project.frequencies

        self.results_to_plot = dict()
        if self.checkBox_force_Fx.isChecked():
            self.results_to_plot["F_x"] = {"x_data" : x_data,
                                           "y_data" : shaking_forces["F_x"]}

        if self.checkBox_force_Fy.isChecked():
            self.results_to_plot["F_y"] = {"x_data" : x_data,
                                           "y_data" : shaking_forces["F_y"]}

        if self.checkBox_force_Fz.isChecked():
            self.results_to_plot["F_z"] = {"x_data" : x_data,
                                           "y_data" : shaking_forces["F_z"]}

        if self.checkBox_resultant_force.isChecked():
            self.results_to_plot["F_res"] = {"x_data" : x_data,
                                             "y_data" : shaking_forces["F_res"]}

        self.call_plotter()

    def call_plotter(self):

        # if self.check_inputs():
        #     return

        self.join_model_data()
        self.plotter = FrequencyResponsePlotter()
        self.plotter._set_model_results_data_to_plot(self.model_results)

    def join_model_data(self):

        self.hide()

        self.model_results = dict()
        title = f"Shaking forces from lines {self.lines_typed}"

        for k, (label, data) in enumerate(self.results_to_plot.items()):

            key = ("lines", (label))
            legend_label = f"Shaking forces {label}"

            self.model_results[key] = { 
                                        "x_data" : data["x_data"],
                                        "y_data" : data["y_data"],
                                        "x_label" : "Frequency [Hz]",
                                        "y_label" : "Acoustic pressures ratio",
                                        "title" : title,
                                        "data_type" : "acoustic pressures ratio",
                                        "legend" : legend_label,
                                        "unit" : self.unit_label,
                                        "color" : self.get_color(k),
                                        "linestyle" : "-"
                                    }

    def get_color(self, index):
        colors = [  
                    (0,0,1), 
                    (1,0,0),
                    (1,0,1),
                    (0,0,0)
                 ]

        if index <= 3:
            return colors[index]
        else:
            return tuple(np.random.randint(0, 255, size=3))