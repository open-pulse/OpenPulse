from PyQt5.QtWidgets import QComboBox, QFrame, QPushButton, QSlider, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *

import numpy as np


class PlotStressesFieldForStaticAnalysis(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/results/structural/plot_stresses_field_for_static_analysis.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.project = app().main_window.project

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self.update_plot()
        self.load_user_preference_colormap()

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

        self.colormaps = ["jet",
                          "viridis",
                          "inferno",
                          "magma",
                          "plasma",
                          "grayscale"]

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_color_scale : QComboBox
        self.comboBox_colormaps : QComboBox
        self.comboBox_stress_type : QComboBox

        # QFrame
        self.frame_button : QFrame
        self.frame_button.setVisible(False)

        # QPushButton
        self.pushButton_plot : QPushButton

        # QSlider
        self.slider_transparency : QSlider

    def _create_connections(self):
        #
        self.comboBox_colormaps.currentIndexChanged.connect(self.update_colormap_type)
        self.comboBox_color_scale.currentIndexChanged.connect(self.update_plot)
        self.comboBox_stress_type.currentIndexChanged.connect(self.update_plot)
        #
        self.pushButton_plot.clicked.connect(self.update_plot)
        #
        self.slider_transparency.valueChanged.connect(self.update_transparency_callback)
        #
        self.update_animation_widget_visibility()
        self.update_colormap_type()

    def update_animation_widget_visibility(self):
        index = self.comboBox_color_scale.currentIndex()
        if index >= 2:
            app().main_window.results_viewer_wigdet.animation_widget.setDisabled(True)
        else:
            app().main_window.results_viewer_wigdet.animation_widget.setDisabled(False) 

    def load_user_preference_colormap(self):
        try:
            colormap = app().main_window.user_preferences["colormap"]
            if colormap in self.colormaps:
                index = self.colormaps.index(colormap)
                self.comboBox_colormaps.setCurrentIndex(index)
        except:
            self.comboBox_colormaps.setCurrentIndex(0)

    def update_colormap_type(self):
        index = self.comboBox_colormaps.currentIndex()
        colormap = self.colormaps[index]
        app().config.write_colormap_in_file(colormap)
        app().main_window.results_widget.set_colormap(colormap)
        self.update_plot()

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
        app().main_window.results_widget.show_stress_field(self.selected_index)

    def get_user_color_scale_setup(self):

        absolute = False
        real_values = False
        imag_values = False
        absolute_animation = False

        index = self.comboBox_color_scale.currentIndex()

        if index == 0:
            absolute_animation = True
        if index == 2:
            absolute = True
        elif index == 3:
            real_values = True
        elif index == 4:
            imag_values = True
        
        color_scale_setup = {   "absolute" : absolute,
                                "real_values" : real_values,
                                "imag_values" : imag_values,
                                "absolute_animation" : absolute_animation   }

        return color_scale_setup

    def update_transparency_callback(self):
        transparency = self.slider_transparency.value() / 100
        app().main_window.results_widget.set_tube_actors_transparency(transparency)

    def update_plot(self):
        self.update_animation_widget_visibility()
        self.selected_index = 0
        self.get_stress_data()

    def confirm_button(self):
        self.update_plot()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_plot()
        elif event.key() == Qt.Key_Escape:
            self.close()