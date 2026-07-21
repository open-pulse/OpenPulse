import logging

import numpy as np
from PySide6.QtWidgets import QLineEdit

from pulse import app
from pulse.interface.ui_generated.plots.results.structural.get_stresses_for_static_analysis_ui import GetStressesForStaticAnalysis_UI
from pulse.interface.user_input.project.loading_window import LoadingWindow


class PlotStressesForStaticAnalysis(GetStressesForStaticAnalysis_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._initialize()
        self._load_structural_solver()
        self._create_list_line_edits()
        self._create_connections()
        self.selection_callback()

    def _initialize(self):

        self.stresses_data = None

    @property
    def model(self):
        return app().project.model
    
    @property
    def structural_solver(self):
        return app().project.structural_solver

    def _load_structural_solver(self):

        if self.structural_solver is not None:
            return

        def process_cross_sections():
            logging.info("Processing the cross-sections [75%]")
            self.model.preprocessor.process_cross_sections_mapping()

        LoadingWindow(process_cross_sections).run()

        app().project.structural_solver = app().project.get_structural_solver()
        if self.structural_solver.solution is None:
            self.structural_solver.solution = self.model.structural_solution

    def _create_list_line_edits(self):
        self.line_edits: list[QLineEdit] = [
            self.lineEdit_element_id,
            self.lineEdit_axial_stress,
            self.lineEdit_bending_stress_y,
            self.lineEdit_bending_stress_z,
            self.lineEdit_hoop_stress,
            self.lineEdit_torsional_stress,
            self.lineEdit_shear_stress_xy,
            self.lineEdit_shear_stress_yz,
        ]

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
            self.reset_line_edits()

    def _update_lineEdit(self, selected_element : int):

        if self.stresses_data is None:
            self.stresses_data = self.structural_solver.stress_calculate(static_analysis=True)

        stresses = np.real(self.stresses_data[selected_element, :, 0])

        for i, line_edit in enumerate(self.line_edits[1:]):
            line_edit.setText("{:.6e}".format(stresses[i]))

    def reset_line_edits(self):
        for line_edit in self.line_edits:
            line_edit.clear()

    def reset_selection(self):
        self.reset_line_edits()