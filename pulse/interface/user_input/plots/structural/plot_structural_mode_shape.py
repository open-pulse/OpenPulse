from PySide6.QtWidgets import QTreeWidgetItem, QGridLayout
from PySide6.QtCore import Qt

from pulse import app
from pulse.interface.ui_generated.plots.results.structural.plot_structural_mode_shape_ui import PlotStructuralModeShape_UI
from pulse.interface.user_input.plots.general.animation_widget import AnimationWidget


import numpy as np


class PlotStructuralModeShape(PlotStructuralModeShape_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._config_window()
        self._initialize()
        self._create_connections()
        self._add_animation_widget()
        self._config_widgets()
        self.load_natural_frequencies()
        self.load_user_preference_colormap()

    def _initialize(self):
        self.mode_index = None
        self.colormaps = [
            "jet",
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
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

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

    def _config_widgets(self):

        self.frame_button.setVisible(False)
        self.lineEdit_natural_frequency.setDisabled(True)

        widths = [100, 140]
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
        index = self.comboBox_color_scale.currentIndex()
        return
        if index >= 4:
            app().main_window.animation_toolbar.setDisabled(True)
        else:
            app().main_window.animation_toolbar.setDisabled(False)

    def load_user_preference_colormap(self):
        try:
            colormap = app().config.user_preferences.color_map
            if colormap in self.colormaps:
                index = self.colormaps.index(colormap)
                self.comboBox_colormaps.setCurrentIndex(index)
        except Exception:
            self.comboBox_colormaps.setCurrentIndex(0)

    def update_colormap_type(self):
        index = self.comboBox_colormaps.currentIndex()
        colormap = self.colormaps[index]
        app().main_window.results_widget.set_colormap(colormap)
        self.update_plot()

    def update_plot(self):

        self.update_animation_widget_visibility()
        if self.lineEdit_natural_frequency.text() == "":
            return

        frequency = self.selected_natural_frequency
        self.mode_index = self.natural_frequencies.index(frequency)
        color_scale_setup = self.get_user_color_scale_setup()

        app().project.set_color_scale_setup(color_scale_setup)
        app().main_window.results_widget.show_displacement_field(self.mode_index)
        app().main_window.results_widget.clear_cache()

    def update_transparency_callback(self):
        transparency = self.slider_transparency.value() / 100
        app().main_window.results_widget.set_tube_actors_transparency(transparency)

    def get_user_color_scale_setup(self):

        color_scale = self.comboBox_color_scale.currentText()

        color_scale_setup = {   
            "absolute" : color_scale == "Absolute (resultant)",
            "ux_abs_values" : color_scale == "Absolute (Ux)",
            "uy_abs_values" : color_scale == "Absolute (Uy)",
            "uz_abs_values" : color_scale == "Absolute (Uz)",
            "ux_real_values" : color_scale == "Real - Ux",
            "uy_real_values" : color_scale == "Real - Uy",
            "uz_real_values" : color_scale == "Real - Uz",
            "ux_imag_values" : color_scale == "Imaginary - Ux",
            "uy_imag_values" : color_scale == "Imaginary - Uy",
            "uz_imag_values" : color_scale == "Imaginary - Uz",
            "absolute_animation" : color_scale == "Animation (absolute)",
            "ux_animation" : color_scale == "Animation (Ux)",
            "uy_animation" : color_scale == "Animation (Uy)",
            "uz_animation" : color_scale == "Animation (Uz)",
            }

        return color_scale_setup

    def load_natural_frequencies(self):
        
        self.natural_frequencies = list(app().project.natural_frequencies_structural)
        modes = np.arange(1, len(self.natural_frequencies) + 1, 1)
        self.modes_to_frequencies = dict(zip(modes, self.natural_frequencies))

        self.treeWidget_frequencies.clear()
        for mode, natural_frequency in self.modes_to_frequencies.items():
            new = QTreeWidgetItem([str(mode), str(round(natural_frequency,4))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_frequencies.addTopLevelItem(new)

    def on_click_item(self, item):
        self.selected_natural_frequency = self.modes_to_frequencies[int(item.text(0))]
        self.lineEdit_natural_frequency.setText(str(round(self.selected_natural_frequency,4)))
        self.update_plot()

    def on_doubleclick_item(self, item):
        self.selected_natural_frequency = self.modes_to_frequencies[int(item.text(0))]
        self.lineEdit_natural_frequency.setText(str(round(self.selected_natural_frequency,4)))
        self.update_plot()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_plot()
        elif event.key() == Qt.Key_Escape:
            self.close()