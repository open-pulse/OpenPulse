from PyQt5.QtWidgets import QComboBox, QFrame, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *

import numpy as np
from pathlib import Path


class PlotStressesFieldForStaticAnalysis(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = Path(f"{UI_DIR}/plots/results/structural/plot_stresses_field_for_static_analysis.ui")
        uic.loadUi(ui_path, self)

        main_window = app().main_window

        self.opv = main_window.opv_widget
        self.opv.setInputObject(self)
        self.project = main_window.project

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self.plot_stress_field()

    def _initialize(self):
        self.selected_index = None
        self.stress_field = []
        self.stress_data = []
        self.keys = np.arange(7)
        self.labels = np.array(["Normal axial",
                                "Normal bending y",
                                "Normal bending z",
                                "Hoop",
                                "Torsional shear",
                                "Transversal shear xy",
                                "Transversal shear xz"])

        self.solve = self.project.structural_solve
        self.preprocessor = self.project.preprocessor

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_color_scaling = self.findChild(QComboBox, 'comboBox_color_scaling')
        self.comboBox_stress_type = self.findChild(QComboBox, 'comboBox_stress_type')
        # QFrame
        self.frame_button = self.findChild(QFrame, 'frame_button')
        self.frame_button.setVisible(False)
        # QPushButton
        self.pushButton_plot = self.findChild(QPushButton, 'pushButton_plot')

    def _create_connections(self):
        self.comboBox_color_scaling.currentIndexChanged.connect(self.plot_stress_field)
        self.comboBox_stress_type.currentIndexChanged.connect(self.plot_stress_field)
        self.pushButton_plot.clicked.connect(self.plot_stress_field)
        self.update_animation_widget_visibility()

    def update_animation_widget_visibility(self):
        index = self.comboBox_color_scale.currentIndex()
        if index <= 2:
            app().main_window.results_viewer_wigdet.animation_widget.setDisabled(True)
        else:
            app().main_window.results_viewer_wigdet.animation_widget.setDisabled(False) 

    def get_stress_data(self):

        index = self.comboBox_stress_type.currentIndex()
        self.stress_label = self.labels[index]
        self.stress_key = self.keys[index]

        if self.stress_data == []:
            self.stress_data = self.solve.stress_calculate( pressure_external = 0, 
                                                            damping_flag = False )
            
        self.stress_field = { key:array[self.stress_key, self.selected_index] for key, array in self.stress_data.items() }
        self.project.set_stresses_values_for_color_table(self.stress_field)
        self.project.set_min_max_type_stresses( np.min(list(self.stress_field.values())), 
                                                np.max(list(self.stress_field.values())), 
                                                self.stress_label )

        color_scale_setup = self.get_user_color_scale_setup()
        self.project.set_color_scale_setup(color_scale_setup)
        self.opv.plot_stress_field(self.selected_index)
        
    def plot_stress_field(self):
        self.update_animation_widget_visibility()
        self.selected_index = 0
        self.get_stress_data()

    def confirm_button(self):
        self.plot_stress_field()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.plot_stress_field()
        elif event.key() == Qt.Key_Escape:
            self.close()