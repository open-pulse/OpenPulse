import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QTreeWidgetItem

from pulse import app
from pulse.interface.ui_generated.plots.results.acoustic.plot_acoustic_pressure_field_for_harmonic_analysis_ui import (
    PlotAcousticPressureFieldForHarmonicAnalysis_UI,
)
from pulse.interface.user_input.plots.general.animation_widget import AnimationWidget


class PlotAcousticPressureField(PlotAcousticPressureFieldForHarmonicAnalysis_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._add_animation_widget()
        self.load_frequencies_vector()
        self.load_user_preference_colormap()
        self.select_first_frequency()

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

    def _define_qt_variables(self):
        self.frame_button.setVisible(False)
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
    
    def _add_animation_widget(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_animation.setLayout(self.grid_layout)

        self.animation_widget = AnimationWidget()
        self.grid_layout.addWidget(self.animation_widget)
        self.frame_animation.adjustSize()

    def update_animation_widget_visibility(self):
        if not hasattr(self, "animation_widget"):
            return
        index = self.comboBox_color_scale.currentIndex()
        self.animation_widget.setDisabled(index >= 2)

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

        color_scale = self.comboBox_color_scale.currentText()

        color_scale_setup = {   
            "absolute" : color_scale == "Absolute values",
            "real_values" : color_scale == "Real values",
            "imag_values" : color_scale == "Imaginary values",
            "absolute_animation" : color_scale == "Animation (absolute)",
            }

        return color_scale_setup

    def load_frequencies_vector(self):
        self.treeWidget_frequencies.clear()
        for index, frequency in enumerate(self.frequencies):
            new = QTreeWidgetItem([str(index+1), str(frequency)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_frequencies.addTopLevelItem(new)

    def select_first_frequency(self):
        if self.treeWidget_frequencies.topLevelItemCount() == 0:
            return
        item = self.treeWidget_frequencies.topLevelItem(0)
        self.treeWidget_frequencies.setCurrentItem(item)
        self.on_click_item(item)

    def on_click_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(1))
        self.animation_widget.reset_sliders()
        self.update_plot()

    def on_doubleclick_item(self, item):
        self.lineEdit_selected_frequency.setText(item.text(1))
        self.animation_widget.reset_sliders()
        self.update_plot()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_plot()
        elif event.key() == Qt.Key_Escape:
            self.close()