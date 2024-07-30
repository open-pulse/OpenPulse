from PyQt5.QtWidgets import QLineEdit, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *

import numpy as np
from pathlib import Path


class GetNodalResultsForStaticAnalysis(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/results/structural/get_nodal_results_for_static_analysis.ui"
        uic.loadUi(ui_path, self)

        main_window = app().main_window

        self.opv = main_window.opv_widget
        app().main_window.input_ui.set_input_widget(self)
        self.project = main_window.project

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_list_lineEdits()
        self._create_connections()
        self._config_widgets()
        self.update()

    def _initialize(self):
        solution = self.project.get_structural_solution()
        self.solution = np.real(solution)

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):
        #
        self.lineEdit_node_id : QLineEdit
        self.lineEdit_response_ux : QLineEdit
        self.lineEdit_response_uy : QLineEdit
        self.lineEdit_response_uz : QLineEdit
        self.lineEdit_response_rx : QLineEdit
        self.lineEdit_response_ry : QLineEdit
        self.lineEdit_response_rz : QLineEdit
        #
        self.pushButton_reset : QPushButton

    def _create_connections(self):
        self.pushButton_reset.clicked.connect(self.reset_selection)

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
        self.opv.opvRenderer.updateColors()
        self.opv.opvRenderer.update()

    def _update_lineEdit(self):    
        node_id = self.list_node_IDs[0]
        node = self.project.preprocessor.nodes[node_id]
        results = self.solution[node.global_dof, 0]
        self.lineEdit_response_ux.setText("{:.6e}".format(results[0]))
        self.lineEdit_response_uy.setText("{:.6e}".format(results[1]))
        self.lineEdit_response_uz.setText("{:.6e}".format(results[2]))
        self.lineEdit_response_rx.setText("{:.6e}".format(results[3]))
        self.lineEdit_response_ry.setText("{:.6e}".format(results[4]))
        self.lineEdit_response_rz.setText("{:.6e}".format(results[5]))

    def update(self):
        self.list_node_IDs = self.opv.getListPickedPoints()
        if len(self.list_node_IDs) == 1:
            self.lineEdit_node_id.setText(str(self.list_node_IDs[0]))
            self._update_lineEdit()
        else:
            self._reset_lineEdits()