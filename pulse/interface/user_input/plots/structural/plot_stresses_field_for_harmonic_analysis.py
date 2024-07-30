from PyQt5.QtWidgets import QCheckBox, QComboBox, QFrame, QLineEdit, QPushButton, QSlider, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *

import numpy as np


class PlotStressesFieldForHarmonicAnalysis(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/results/structural/plot_stresses_field_for_harmonic_analysis.ui"
        uic.loadUi(ui_path, self)

        main_window = app().main_window
        self.opv = main_window.opv_widget
        app().main_window.input_widget.set_input_widget(self)
        self.project = main_window.project
        
        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connection()
        self.load_frequencies()
        self.load_user_preference_colormap()

    def _initialize(self):

        self.selected_index = None
        self.update_damping = False

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
        self.frequencies = self.project.frequencies
        self.dict_frequency_to_index = dict(zip(self.frequencies, np.arange(len(self.frequencies), dtype=int)))

        self.colormaps = ["jet",
                          "viridis",
                          "inferno",
                          "magma",
                          "plasma",
                          "grayscale"]

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

    def _define_qt_variables(self):

        # QCheckBox
        self.checkBox_damping_effect : QCheckBox
        self.comboBox_colormaps : QComboBox

        # QComboBox
        self.comboBox_color_scale : QComboBox
        self.comboBox_stress_type : QComboBox

        # QFrame
        self.frame_button : QFrame
        self.frame_button.setVisible(False)

        # QLineEdit
        self.lineEdit_selected_frequency : QLineEdit

        # QSlider
        self.slider_transparency : QSlider

        # QPushButton
        self.pushButton_plot : QPushButton

        # QTreeWidget
        self.treeWidget_frequencies : QTreeWidget
    
    def _create_connection(self):
        #
        self.checkBox_damping_effect.stateChanged.connect(self._update_damping_effect)
        #
        self.comboBox_color_scale.currentIndexChanged.connect(self.update_plot)
        self.comboBox_colormaps.currentIndexChanged.connect(self.update_colormap_type)
        self.comboBox_stress_type.currentIndexChanged.connect(self.update_plot)
        #
        self.slider_transparency.valueChanged.connect(self.update_transparency_callback)
        #
        self.pushButton_plot.clicked.connect(self.update_plot)
        #
        self.treeWidget_frequencies.itemClicked.connect(self.on_click_item)
        self.treeWidget_frequencies.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        self.update_animation_widget_visibility()
        self.update_colormap_type()

    def _update_damping_effect(self):
        self.update_damping = True
        self.update_plot()

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
        self.opv.opvAnalysisRenderer.set_colormap(colormap)
        app().main_window.results_widget.set_colormap(colormap)
        self.update_plot()

    def update_transparency_callback(self):
        transparency = self.slider_transparency.value() / 100
        app().main_window.results_widget.set_tube_actors_transparency(transparency)
        
        if self.opv.opvAnalysisRenderer.getInUse():
            self.opv.opvAnalysisRenderer.set_tube_actors_transparency(transparency)
        else:
            self.opv.opvRenderer.set_tube_actors_transparency(transparency)

    def update_plot(self):
        self.update_animation_widget_visibility()
        if self.lineEdit_selected_frequency.text() == "":
            return
        else:
            frequency_selected = float(self.lineEdit_selected_frequency.text())
            if frequency_selected in self.frequencies:
                self.selected_index = self.dict_frequency_to_index[frequency_selected]
                self.get_stress_data()

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

    def get_stress_data(self):

        index = self.comboBox_stress_type.currentIndex()
        self.stress_label = self.labels[index]
        self.stress_key = self.keys[index]
        self.flag_damping_effect = self.checkBox_damping_effect.isChecked()

        if self.stress_data == [] or self.update_damping:
            self.stress_data = self.solve.stress_calculate( pressure_external = 0, 
                                                            damping_flag = self.flag_damping_effect )
            self.update_damping = False
            
        self.stress_field = { key:array[self.stress_key, self.selected_index] for key, array in self.stress_data.items() }
        self.project.set_stresses_values_for_color_table(self.stress_field)
        self.project.set_min_max_type_stresses( np.min(list(self.stress_field.values())), 
                                                np.max(list(self.stress_field.values())), 
                                                self.stress_label )
        
        color_scale_setup = self.get_user_color_scale_setup()
        self.project.set_color_scale_setup(color_scale_setup)
        self.opv.plot_stress_field(self.selected_index)
        app().main_window.results_widget.show_stress_field(self.selected_index)

    def on_click_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(0))
        self.update_plot()

    def on_doubleclick_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(0))
        self.update_plot()

    def load_frequencies(self):
        for index, frequency in enumerate(self.frequencies):
            new = QTreeWidgetItem([str(index+1), str(frequency)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_frequencies.addTopLevelItem(new)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_plot()
        elif event.key() == Qt.Key_Escape:
            self.close()