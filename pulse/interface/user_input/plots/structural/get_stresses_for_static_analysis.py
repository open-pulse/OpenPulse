from PyQt5.QtWidgets import QLineEdit, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.postprocessing.plot_structural_data import get_stress_spectrum_data

import numpy as np
from pathlib import Path


class GetStressesForStaticAnalysis(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = Path(f"{UI_DIR}/plots/results/structural/get_stresses_for_static_analysis.ui")
        uic.loadUi(ui_path, self)

        main_window = app().main_window

        self.opv = main_window.opv_widget
        self.opv.setInputObject(self)
        self.project = main_window.project

        self._initialize()
        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self.update()

    def _initialize(self):
        self.stress_labels = [  "Normal axial", 
                                "Normal bending y", 
                                "Normal bending z", 
                                "Hoop", 
                                "Torsional shear", 
                                "Transversal shear xy", 
                                "Transversal shear xz"]

        self.solve = self.project.structural_solve

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Plot stresses for static analysis")

    def _define_qt_variables(self):
        #
        self.lineEdit_element_id = self.findChild(QLineEdit, 'lineEdit_element_id')
        self.lineEdit_axial_stress = self.findChild(QLineEdit, 'lineEdit_axial_stress')
        self.lineEdit_bending_stress_y = self.findChild(QLineEdit, 'lineEdit_bending_stress_y')
        self.lineEdit_bending_stress_z = self.findChild(QLineEdit, 'lineEdit_bending_stress_z')
        self.lineEdit_hoop_stress = self.findChild(QLineEdit, 'lineEdit_hoop_stress')
        self.lineEdit_torsional_stress = self.findChild(QLineEdit, 'lineEdit_torsional_stress')
        self.lineEdit_shear_stress_xy = self.findChild(QLineEdit, 'lineEdit_shear_stress_xy')
        self.lineEdit_shear_stress_yz = self.findChild(QLineEdit, 'lineEdit_shear_stress_yz')
        #
        self.lineEdits = [  self.lineEdit_element_id,
                            self.lineEdit_axial_stress,
                            self.lineEdit_bending_stress_y,
                            self.lineEdit_bending_stress_z,
                            self.lineEdit_hoop_stress,
                            self.lineEdit_torsional_stress,
                            self.lineEdit_shear_stress_xy,
                            self.lineEdit_shear_stress_yz  ]
        #
        self.pushButton_reset = self.findChild(QPushButton, 'pushButton_reset')
        self.pushButton_reset.clicked.connect(self.reset_selection)
        self._config_lineEdits()

    def _config_lineEdits(self):
        for k, lineEdit in enumerate(self.lineEdits):
            lineEdit.setDisabled(True)
            lineEdit.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")

    def _reset_lineEdits(self):
        for lineEdit in self.lineEdits:
            lineEdit.setText("")

    def _update_lineEdit(self):

        element_id = self.list_elements_IDs[0]
        self.stress_data = self.solve.stress_calculate(pressure_external = 0, damping_flag = False)
        stresses = np.real(np.array(self.stress_data[element_id][:,0]))
        #
        self.lineEdit_axial_stress.setText("{:.6e}".format(stresses[0]))
        self.lineEdit_bending_stress_y.setText("{:.6e}".format(stresses[1]))
        self.lineEdit_bending_stress_z.setText("{:.6e}".format(stresses[2]))
        self.lineEdit_hoop_stress.setText("{:.6e}".format(stresses[3]))
        self.lineEdit_torsional_stress.setText("{:.6e}".format(stresses[4]))
        self.lineEdit_shear_stress_xy.setText("{:.6e}".format(stresses[5]))
        self.lineEdit_shear_stress_yz.setText("{:.6e}".format(stresses[6]))

    def reset_selection(self):
        self._reset_lineEdits()
        self.opv.opvRenderer.updateColors()
        self.opv.opvRenderer.update()

    def update(self):
        self.list_elements_IDs = self.opv.getListPickedElements()
        if len(self.list_elements_IDs) == 1:
            self.lineEdit_element_id.setText(str(self.list_elements_IDs[0]))
            self._update_lineEdit()
        else:
            self._reset_lineEdits()