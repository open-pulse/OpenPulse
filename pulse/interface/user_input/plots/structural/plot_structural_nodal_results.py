from PyQt5.QtWidgets import QLineEdit, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import numpy as np

from pulse import app

class PlotNodalResultsForStaticAnalysis(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        main_window = app().main_window

        ui_path = Path(f"{main_window.ui_dir}/plots/results/structural/plot_nodal_response_for_static_analysis.ui")
        uic.loadUi(ui_path, self)

        self.opv = main_window.getOPVWidget()
        self.opv.setInputObject(self)
        self.project = main_window.getProject()
        
        solution = self.project.get_structural_solution()
        self.solution = np.real(solution)

        self._config_window()
        self._define_qt_variables()
        self.update()

    def _config_window(self):
        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Structural nodal response")

    def _define_qt_variables(self):
        #
        self.lineEdit_node_id = self.findChild(QLineEdit, 'lineEdit_node_id')
        self.lineEdit_response_ux = self.findChild(QLineEdit, 'lineEdit_response_ux')
        self.lineEdit_response_uy = self.findChild(QLineEdit, 'lineEdit_response_uy')
        self.lineEdit_response_uz = self.findChild(QLineEdit, 'lineEdit_response_uz')
        self.lineEdit_response_rx = self.findChild(QLineEdit, 'lineEdit_response_rx')
        self.lineEdit_response_ry = self.findChild(QLineEdit, 'lineEdit_response_ry')
        self.lineEdit_response_rz = self.findChild(QLineEdit, 'lineEdit_response_rz')
        #
        self.lineEdits = [  self.lineEdit_node_id,
                            self.lineEdit_response_ux,
                            self.lineEdit_response_uy,
                            self.lineEdit_response_uz,
                            self.lineEdit_response_rx,
                            self.lineEdit_response_ry,
                            self.lineEdit_response_rz  ]
        #
        self.pushButton_reset = self.findChild(QPushButton, 'pushButton_reset')
        self.pushButton_reset.clicked.connect(self.reset_selection)
        #
        self._config_lineEdits()

    def _config_lineEdits(self):
        for lineEdit in self.lineEdits:
            lineEdit.setDisabled(True)
            lineEdit.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")

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