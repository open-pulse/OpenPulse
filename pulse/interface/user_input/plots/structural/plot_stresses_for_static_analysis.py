from PySide6.QtWidgets import QLineEdit, QPushButton, QWidget
from PySide6.QtCore import Qt

from pulse import app, UI_DIR
from pulse.interface.user_input.project.loading_window import LoadingWindow

from molde import load_ui

import logging
import numpy as np

class PlotStressesForStaticAnalysis(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/results/structural/get_stresses_for_static_analysis.ui"
        load_ui(ui_path, self, UI_DIR)

        app().main_window.set_input_widget(self)

        self._config_window()
        self._initialize()
        self._load_structural_solver()
        self._define_qt_variables()
        self._create_list_lineEdits()
        self._create_connections()
        self.selection_callback()

    def _initialize(self):
        self.stress_labels = [  "Normal axial", 
                                "Normal bending y", 
                                "Normal bending z", 
                                "Hoop", 
                                "Torsional shear", 
                                "Transversal shear xy", 
                                "Transversal shear xz"]

    def _load_structural_solver(self):

        if app().project.structural_solver is None:

            def callback():
                logging.info("Processing the cross-sections [75%]")
                app().project.model.preprocessor.process_cross_sections_mapping()
            LoadingWindow(callback).run()

            self.structural_solver = app().project.get_structural_solver()
            if self.structural_solver.solution is None:
                self.structural_solver.solution = app().project.structural_solution

        else:
            self.structural_solver = app().project.structural_solver

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QLineEdit
        self.lineEdit_element_id : QLineEdit
        self.lineEdit_axial_stress : QLineEdit
        self.lineEdit_bending_stress_y : QLineEdit
        self.lineEdit_bending_stress_z : QLineEdit
        self.lineEdit_hoop_stress : QLineEdit
        self.lineEdit_torsional_stress : QLineEdit
        self.lineEdit_shear_stress_xy : QLineEdit
        self.lineEdit_shear_stress_yz : QLineEdit

        # QPushButton
        self.pushButton_reset : QPushButton

    def _create_list_lineEdits(self):
        self.lineEdits = [  self.lineEdit_element_id,
                            self.lineEdit_axial_stress,
                            self.lineEdit_bending_stress_y,
                            self.lineEdit_bending_stress_z,
                            self.lineEdit_hoop_stress,
                            self.lineEdit_torsional_stress,
                            self.lineEdit_shear_stress_xy,
                            self.lineEdit_shear_stress_yz  ]

    def _create_connections(self):
        #
        self.pushButton_reset.clicked.connect(self.reset_selection)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):
        selected_elements = app().main_window.list_selected_elements()
        if len(selected_elements) == 1:
            self.lineEdit_element_id.setText(str(selected_elements[0]))
            self._update_lineEdit(selected_elements[0])
        else:
            self._reset_lineEdits()

    def _reset_lineEdits(self):
        for lineEdit in self.lineEdits:
            lineEdit.setText("")

    def _update_lineEdit(self, selected_element : int):

        self.stress_data = self.structural_solver.stress_calculate(static_analysis=True)
        stresses = np.real(np.array(self.stress_data[selected_element][:,0]))

        self.lineEdit_axial_stress.setText("{:.6e}".format(stresses[0]))
        self.lineEdit_bending_stress_y.setText("{:.6e}".format(stresses[1]))
        self.lineEdit_bending_stress_z.setText("{:.6e}".format(stresses[2]))
        self.lineEdit_hoop_stress.setText("{:.6e}".format(stresses[3]))
        self.lineEdit_torsional_stress.setText("{:.6e}".format(stresses[4]))
        self.lineEdit_shear_stress_xy.setText("{:.6e}".format(stresses[5]))
        self.lineEdit_shear_stress_yz.setText("{:.6e}".format(stresses[6]))

    def reset_selection(self):
        self._reset_lineEdits()