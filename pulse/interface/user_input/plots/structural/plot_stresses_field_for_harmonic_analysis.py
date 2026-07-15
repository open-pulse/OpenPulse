import logging
from enum import IntEnum

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QTreeWidgetItem

from pulse import app
from pulse.interface.ui_generated.plots.results.structural.plot_stresses_field_for_harmonic_analysis_ui import PlotStressesFieldForHarmonicAnalysis_UI
from pulse.interface.user_input.plots.general.animation_widget import AnimationWidget
from pulse.interface.user_input.project.loading_window import LoadingWindow
from pulse.interface.viewer_3d.coloring.color_palettes import COLORMAP_NAMES


class DampingEffect(IntEnum):
    EXCLUDED = 0
    INCLUDED = 1


class PlotStressesFieldForHarmonicAnalysis(PlotStressesFieldForHarmonicAnalysis_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._initialize()
        self._create_connection()
        self._add_animation_widget()

    def _initialize(self):

        self.selected_index = None
        self.update_damping = False

        self.stress_field = list()
        self.stress_data = list()

        self.keys = np.arange(7)
        self.labels = np.array(
            ["Normal axial",
             "Normal bending y",
             "Normal bending z",
             "Hoop",
             "Torsional shear",
             "Transversal shear xy",
             "Transversal shear xz"]
        )

    def _load_structural_solver(self):

        if app().project.structural_solver is None:

            def callback():
                logging.info("Processing the cross-sections [75%]")
                app().project.model.preprocessor.process_cross_sections_mapping()

            LoadingWindow(callback).run()

            self.structural_solver = app().project.get_structural_solver()
            if self.structural_solver.solution is None:
                self.structural_solver.solution = app().project.model.structural_solution

        else:
            self.structural_solver = app().project.structural_solver

    def _create_connection(self):
        #
        self.comboBox_damping_effect.currentIndexChanged.connect(self._update_damping_effect)
        #
        self.comboBox_color_scale.currentIndexChanged.connect(self.update_plot)
        self.comboBox_colormaps.currentIndexChanged.connect(self.update_colormap_type)
        self.comboBox_stress_type.currentIndexChanged.connect(self.update_plot)
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

    def _update_damping_effect(self):
        self.update_damping = True
        self.update_plot()

    def update_animation_widget_visibility(self):
        if not hasattr(self, "animation_widget"):
            return
        is_animation = self.comboBox_color_scale.currentText().startswith("Animation")
        self.animation_widget.setDisabled(not is_animation)

    def load_user_preference_colormap(self):
        try:
            colormap = app().config.user_preferences.color_map
            if colormap in COLORMAP_NAMES:
                index = COLORMAP_NAMES.index()
                self.comboBox_colormaps.setCurrentIndex(index)

        except Exception:
            self.comboBox_colormaps.setCurrentIndex(0)

    def update_colormap_type(self):
        colormap = self.get_colormap()
        app().config.user_preferences.color_map = colormap
        app().config.update_config_file()
        try:
            app().main_window.results_widget.set_colormap(colormap)
            self.update_plot()
        except AttributeError:
            pass

    def get_colormap(self) -> str:
        index = self.comboBox_colormaps.currentIndex()
        if not (0 <= index < len(COLORMAP_NAMES)):
            return "jet"
        return COLORMAP_NAMES[index]

    def update_transparency_callback(self):
        transparency = self.slider_transparency.value() / 100
        app().main_window.results_widget.set_tube_actors_transparency(transparency)

    def update_plot(self):
        self.update_animation_widget_visibility()
        if self.lineEdit_selected_frequency.text() == "":
            return

        frequency_selected = float(self.lineEdit_selected_frequency.text())
        if frequency_selected in self.frequencies:
            self.selected_index = self.frequency_to_index[frequency_selected]
            self.get_stress_data()

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

    def get_stress_data(self):

        index = self.comboBox_stress_type.currentIndex()
        stress_label = self.labels[index]
        stress_key = self.keys[index]
        damping_effect = self.comboBox_damping_effect.currentIndex() == DampingEffect.INCLUDED

        if len(self.stress_data) == 0 or self.update_damping:

            self.stress_data = self.structural_solver.stress_calculate(damping=damping_effect)
            self.update_damping = False

        stress_field = { key:array[stress_key, self.selected_index] for key, array in self.stress_data.items() }

        stress_list = list(stress_field.values())
        min_stress = np.min(stress_list)
        max_stress = np.max(stress_list)

        app().project.model.set_stresses_values_for_color_table(stress_field)
        app().project.model.set_min_max_type_stresses(min_stress, max_stress, stress_label)

        color_scale_setup = self.get_user_color_scale_setup()
        print(color_scale_setup)
        app().project.set_color_scale_setup(color_scale_setup)
        app().main_window.results_widget.show_stress_field(self.selected_index)

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
        self.on_click_item(item)

    def load_frequencies(self):
        self._load_structural_solver()
        self.treeWidget_frequencies.clear()
        _frequencies = app().project.model.frequencies

        for index, frequency in enumerate(_frequencies):
            new = QTreeWidgetItem([str(index+1), str(frequency)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_frequencies.addTopLevelItem(new)

        if isinstance(_frequencies, np.ndarray):
            self.frequencies = list(_frequencies)

        elif isinstance(_frequencies, list):
            self.frequencies = _frequencies

        self.frequency_to_index = dict(zip(self.frequencies, np.arange(len(self.frequencies), dtype=int)))
        
        self.select_first_frequency()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_plot()