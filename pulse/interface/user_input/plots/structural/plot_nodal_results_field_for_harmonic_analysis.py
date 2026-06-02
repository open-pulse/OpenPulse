import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QTreeWidgetItem

from pulse import app
from pulse.interface.ui_generated.plots.results.structural.plot_nodal_results_field_for_harmonic_analysis_ui import (
    PlotNodalResultsFieldForHarmonicAnalysis_UI,
)
from pulse.interface.user_input.plots.general.animation_widget import AnimationWidget
from pulse.model import AnalysisID


class PlotNodalResultsFieldForHarmonicAnalysis(PlotNodalResultsFieldForHarmonicAnalysis_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initialize()
        self._config_window()
        self._define_qt_variables()
        self._add_animation_widget()
        self._create_connections()
        self.load_frequencies_vector()
        self.load_user_preference_colormap()
        self.select_first_frequency()

    def _initialize(self):

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
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

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
        self.animation_widget.setDisabled(index >= 4)

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

    def _config_treeWidget(self):
        widths = [80, 140]
        for i, width in enumerate(widths):
            self.treeWidget_frequencies.setColumnWidth(i, width)
            self.treeWidget_frequencies.headerItem().setTextAlignment(i, Qt.AlignCenter)
        #
        self.lineEdit_selected_frequency.setDisabled(True)

    def update_transparency_callback(self):
        transparency = self.slider_transparency.value() / 100
        app().main_window.results_widget.set_tube_actors_transparency(transparency)

    def update_plot(self):
        self.update_animation_widget_visibility()
        if self.lineEdit_selected_frequency.text() == "":
            return

        frequency_selected = float(self.lineEdit_selected_frequency.text())
        if frequency_selected in self.frequencies:
            # frequency = self.frequency_to_index[frequency_selected]
            frequency = self.frequencies.index(frequency_selected)
            color_scale_setup = self.get_user_color_scale_setup()
            app().project.set_color_scale_setup(color_scale_setup)
            app().main_window.results_widget.show_displacement_field(frequency)
            app().main_window.results_widget.clear_cache()


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

    def load_frequencies_vector(self):

        if app().project.analysis_id == AnalysisID.STRUCTURAL_STATIC:
            self.frequencies = [0]
            self.treeWidget_frequencies.setDisabled(True)
            self.plot_displacement_for_static_analysis()

        else:

            self.treeWidget_frequencies.setDisabled(False)
            if isinstance(app().project.model.frequencies, np.ndarray):
                _frequencies = app().project.model.frequencies
                self.frequencies = list(_frequencies)

            self.frequency_to_index = dict(zip(self.frequencies, np.arange(len(self.frequencies), dtype=int)))

        self.treeWidget_frequencies.clear()
        for index, frequency in enumerate(self.frequencies):

            item = QTreeWidgetItem([str(index+1), str(frequency)])
            for i in range(2):
                item.setTextAlignment(i, Qt.AlignCenter)
            self.treeWidget_frequencies.addTopLevelItem(item)

    def plot_displacement_for_static_analysis(self):
        #
        self.lineEdit_selected_frequency.setText("0.0")
        color_scale_setup = self.get_user_color_scale_setup()
        #
        app().project.set_color_scale_setup(color_scale_setup)
        app().main_window.results_widget.show_displacement_field(0)

    def select_first_frequency(self):
        if app().project.analysis_id == AnalysisID.STRUCTURAL_STATIC:
            return
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
        self.update_plot()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_plot()
        elif event.key() == Qt.Key_Escape:
            self.close()