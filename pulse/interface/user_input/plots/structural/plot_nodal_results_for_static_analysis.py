from PySide6.QtWidgets import QLineEdit, QPushButton, QWidget
from PySide6.QtCore import Qt

from pulse import app
from pulse.interface.ui_generated.plots.results.structural.get_nodal_results_for_static_analysis_ui import GetNodalResultsForStaticAnalysis_UI


import numpy as np


class PlotNodalResultsForStaticAnalysis(GetNodalResultsForStaticAnalysis_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app().main_window.set_input_widget(self)
        self.project = app().main_window.project

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_list_lineEdits()
        self._create_connections()
        self._config_widgets()
        self.selection_callback()

    def _initialize(self):
        solution = self.project.get_structural_solution()
        self.solution = np.real(solution)

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):
        pass

    def _create_connections(self):
        #
        self.pushButton_reset.clicked.connect(self.reset_selection)
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):
        selected_nodes = app().main_window.list_selected_nodes()
        if len(selected_nodes) == 1:
            node_id = selected_nodes[0]
            self.lineEdit_node_id.setText(str(node_id))
            self._update_lineEdit(selected_nodes)
        else:
            self._reset_lineEdits()

    def _create_list_lineEdits(self):
        self.lineEdits = [  self.lineEdit_node_id,
                            self.lineEdit_response_ux,
                            self.lineEdit_response_uy,
                            self.lineEdit_response_uz,
                            self.lineEdit_response_rx,
                            self.lineEdit_response_ry,
                            self.lineEdit_response_rz  ]

    def _config_widgets(self):
        return

    def _reset_lineEdits(self):
        for lineEdit in self.lineEdits:
            lineEdit.setText("")

    def reset_selection(self):
        self._reset_lineEdits()

    def _update_lineEdit(self, selected_nodes : list):
        node_id = selected_nodes[0]
        node = self.project.model.preprocessor.nodes[node_id]
        results = self.solution[node.global_dof, 0]
        self.lineEdit_response_ux.setText("{:.6e}".format(results[0]))
        self.lineEdit_response_uy.setText("{:.6e}".format(results[1]))
        self.lineEdit_response_uz.setText("{:.6e}".format(results[2]))
        self.lineEdit_response_rx.setText("{:.6e}".format(results[3]))
        self.lineEdit_response_ry.setText("{:.6e}".format(results[4]))
        self.lineEdit_response_rz.setText("{:.6e}".format(results[5]))