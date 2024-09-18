from PyQt5.QtWidgets import QComboBox, QFrame, QPushButton, QSlider, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.project.loading_window import LoadingWindow

import logging
import numpy as np


class PlotStressesFieldForStaticAnalysis(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/results/structural/plot_stresses_field_for_static_analysis.ui"
        uic.loadUi(ui_path, self)

        self._config_window()
        self._initialize()
        self._load_structural_solver()
        self._define_qt_variables()
        self._create_connections()
        self.update_plot()
        self.load_user_preference_colormap()

    def _initialize(self):

        self.stress_data = list()
        self.keys = np.arange(7)
        self.selected_index = None

        self.colormaps = ["jet",
                          "viridis",
                          "inferno",
                          "magma",
                          "plasma",
                          "bwr",
                          "PiYG",
                          "PRGn",
                          "BrBG",
                          "PuOR",
                          "grayscale",
                          ]

        self.labels = np.array(["Normal axial",
                                "Normal bending y",
                                "Normal bending z",
                                "Hoop",
                                "Torsional shear",
                                "Transversal shear xy",
                                "Transversal shear xz"])

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
            app().main_window.animation_toolbar.setDisabled(True)
        else:
            app().main_window.animation_toolbar.setDisabled(False) 

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
        stress_label = self.labels[index]
        stress_key = self.keys[index]

        app().project.model.frequencies = np.array([0.], dtype=float)

        if len(self.stress_data) == 0:
            self.stress_data = self.structural_solver.stress_calculate(static_analysis=True)

        stress_field = { key:array[stress_key, self.selected_index] for key, array in self.stress_data.items() }

        stress_list = list(stress_field.values())
        min_stress = np.min(stress_list)
        max_stress = np.max(stress_list)

        app().project.set_stresses_values_for_color_table(stress_field)
        app().project.set_min_max_type_stresses(min_stress, max_stress, stress_label)

        color_scale_setup = self.get_user_color_scale_setup()
        app().project.set_color_scale_setup(color_scale_setup)
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
        app().main_window.results_widget.clear_cache()

    def confirm_button(self):
        self.update_plot()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_plot()
        elif event.key() == Qt.Key_Escape:
            self.close()