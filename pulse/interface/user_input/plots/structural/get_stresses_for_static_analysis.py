from PyQt5.QtWidgets import QLineEdit, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *

import numpy as np

class GetStressesForStaticAnalysis(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/results/structural/get_stresses_for_static_analysis.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)

        self.project = app().main_window.project

        self._initialize()
        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_list_lineEdits()
        self._create_connections()
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
        self.pushButton_reset.clicked.connect(self.reset_selection)

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

    def update(self):
        self.list_elements_IDs = app().main_window.list_selected_elements()
        if len(self.list_elements_IDs) == 1:
            self.lineEdit_element_id.setText(str(self.list_elements_IDs[0]))
            self._update_lineEdit()
        else:
            self._reset_lineEdits()