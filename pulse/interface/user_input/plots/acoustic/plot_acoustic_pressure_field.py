from PySide6.QtWidgets import QComboBox, QFrame, QLineEdit, QPushButton, QSlider, QTreeWidget, QTreeWidgetItem, QWidget
from PySide6.QtCore import Qt

from pulse import app, UI_DIR

from molde import load_ui

import numpy as np


class PlotAcousticPressureField(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        ui_path = UI_DIR / "plots/results/acoustic/plot_acoustic_pressure_field_for_harmonic_analysis.ui"
        load_ui(ui_path, self, UI_DIR)

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self.load_frequencies_vector()
        self.load_user_preference_colormap()

    def _initialize(self):
        self.frequencies = app().project.model.frequencies
        self.frequency_to_index = dict(zip(self.frequencies, np.arange(len(self.frequencies), dtype=int)))
        self.frequency = None
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

    def _config_window(self):
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_color_scale : QComboBox
        self.comboBox_colormaps : QComboBox

        # QFrame
        self.frame_button : QFrame
        self.frame_button.setVisible(False)

        # QLineEdit
        self.lineEdit_selected_frequency : QLineEdit

        # QPushButton
        self.pushButton_plot : QPushButton

        # QSlider
        self.slider_transparency : QSlider

        # QTreeWidget
        self.treeWidget_frequencies : QTreeWidget
        self._config_treeWidget()

    def _create_connections(self):
        #
        self.comboBox_colormaps.currentIndexChanged.connect(self.update_colormap_type)
        self.comboBox_color_scale.currentIndexChanged.connect(self.update_plot)
        #
        self.pushButton_plot.clicked.connect(self.update_plot)
        #
        self.slider_transparency.valueChanged.connect(self.update_transparency_callback)
        #
        self.treeWidget_frequencies.itemClicked.connect(self.on_click_item)
        self.treeWidget_frequencies.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        self.update_animation_widget_visibility()
        self.load_user_preference_colormap()
        self.update_colormap_type()

    def _config_treeWidget(self):
        widths = [80, 140]
        for i, width in enumerate(widths):
            self.treeWidget_frequencies.setColumnWidth(i, width)
            self.treeWidget_frequencies.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def update_animation_widget_visibility(self):
        index = self.comboBox_color_scale.currentIndex()
        if index >= 2:
            app().main_window.animation_toolbar.setDisabled(True)
        else:
            app().main_window.animation_toolbar.setDisabled(False) 

    def load_user_preference_colormap(self):
        try:
            colormap = app().config.user_preferences.color_map
            if colormap in self.colormaps:
                index = self.colormaps.index(colormap)
                self.comboBox_colormaps.setCurrentIndex(index)
        except:
            self.comboBox_colormaps.setCurrentIndex(0)

    def update_colormap_type(self):
        index = self.comboBox_colormaps.currentIndex()
        colormap = self.colormaps[index]
        app().main_window.results_widget.set_colormap(colormap)
        self.update_plot()

    def update_transparency_callback(self):
        transparency = self.slider_transparency.value() / 100
        app().main_window.results_widget.set_tube_actors_transparency(transparency)

    def update_plot(self):

        self.update_animation_widget_visibility()
        if self.lineEdit_selected_frequency.text() == "":
            return

        frequency_selected = float(self.lineEdit_selected_frequency.text())
        self.frequency = self.frequency_to_index[frequency_selected]

        color_scale_setup = self.get_user_color_scale_setup()
        app().project.set_color_scale_setup(color_scale_setup)
        app().main_window.results_widget.show_pressure_field(self.frequency)
        app().main_window.results_widget.clear_cache()

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

    def load_frequencies_vector(self):
        self.treeWidget_frequencies.clear()
        for index, frequency in enumerate(self.frequencies):
            new = QTreeWidgetItem([str(index+1), str(frequency)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_frequencies.addTopLevelItem(new)

    def on_click_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(1))
        self.update_plot()

    def on_doubleclick_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(1))
        self.update_plot()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_plot()
        elif event.key() == Qt.Key_Escape:
            self.close()