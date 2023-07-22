from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from pathlib import Path

import numpy as np

class PlotStructuralNodalResults(QDialog):
    def __init__(self, project, opv, solution, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui/analysis_/structural_/nodal_response_plot.ui'), self)

        self.project = project

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Structural nodal response")

        self.opv = opv
        self.opv.setInputObject(self)
        
        self.solution = np.real(solution)

        self._define_qt_variables()
        self.update()
        self.exec()

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
        self._config_lineEdits()

    def _config_lineEdits(self):
        for lineEdit in self.lineEdits:
            lineEdit.setDisabled(True)
            lineEdit.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")

    def _reset_lineEdits(self):
        for lineEdit in self.lineEdits:
            lineEdit.setText("")

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