import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGridLayout, QTreeWidgetItem

from pulse import app
from pulse.interface.ui_generated.plots.results.acoustic.acoustic_mode_shape_ui import AcousticModeShape_UI
from pulse.interface.user_input.plots.general.animation_widget import AnimationWidget
from pulse.interface.viewer_3d.coloring.color_palettes import COLORMAP_NAMES


class PlotAcousticModeShape(AcousticModeShape_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initialize()
        self._create_connections()
        self._add_animation_widget()
        

    def _initialize(self):
        self.mode_index = None

    def _create_connections(self):
        #
        self.comboBox_colormaps.currentIndexChanged.connect(self.update_colormap_type)
        self.comboBox_color_scale.currentIndexChanged.connect(self.update_plot)
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

        self.lineEdit_natural_frequency.setDisabled(True)

        if isinstance(app().project.complex_natural_frequencies_acoustic, np.ndarray):
            widths = [60, 170]
            headers = ["Mode", "Damped frequency [Hz]", "Damping ratio [--]"]

        else:
            widths = [120, 160]
            headers = ["Mode", "Frequency [Hz]"]

        font = QFont()
        font.setPointSize(9)

        # full reset of the treeWidget_frequencies
        self.treeWidget_frequencies.clear()
        self.treeWidget_frequencies.setColumnCount(0)
        self.treeWidget_frequencies.setHeaderLabels([])

        for i, header in enumerate(headers):
            self.treeWidget_frequencies.headerItem().setFont(i, font)
            self.treeWidget_frequencies.headerItem().setText(i, header)
            if i < 2:
                self.treeWidget_frequencies.setColumnWidth(i, widths[i])
            self.treeWidget_frequencies.headerItem().setTextAlignment(i, Qt.AlignCenter)
    
    def _add_animation_widget(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_animation.setLayout(self.grid_layout)

        self.animation_widget = AnimationWidget()
        self.grid_layout.addWidget(self.animation_widget)
        self.frame_animation.adjustSize()
        self.animation_widget.set_magnification_slider_visible(False)
            
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

    def update_plot(self):

        self.update_animation_widget_visibility()
        if self.lineEdit_natural_frequency.text() == "":
            return

        self.mode_index = self.natural_frequencies.index(self.selected_frequency)
            
        color_scale_setup = self.get_user_color_scale_setup()
        app().project.set_color_scale_setup(color_scale_setup)
        app().main_window.results_widget.show_pressure_field(self.mode_index)
        app().main_window.results_widget.clear_cache()

    def update_transparency_callback(self):
        transparency = self.slider_transparency.value() / 100
        app().main_window.results_widget.set_tube_actors_transparency(transparency)

    def get_user_color_scale_setup(self):

        color_scale = self.comboBox_color_scale.currentText()

        color_scale_setup = {   
            "absolute" : color_scale == "Absolute values",
            "real_values" : color_scale == "Real values",
            "imag_values" : color_scale == "Imaginary values",
            "absolute_animation" : color_scale == "Animation (absolute)",
            }

        return color_scale_setup

    def load_natural_frequencies(self):

        self._config_widgets()

        if isinstance(app().project.complex_natural_frequencies_acoustic, np.ndarray):
            self.natural_frequencies = list(app().project.complex_natural_frequencies_acoustic)

        else:
            self.natural_frequencies = list(app().project.natural_frequencies_acoustic)

        modes = np.arange(1, len(self.natural_frequencies) + 1, 1)
        self.modes_to_frequencies = dict(zip(modes, self.natural_frequencies))

        for mode, value in self.modes_to_frequencies.items():
            if isinstance(value, complex):
                cols = 3
                damping_ratio = -np.real(value) / np.abs(value)
                damped_frequency = np.abs(value) * ((1-damping_ratio**2)**(1/2))
                new = QTreeWidgetItem([str(mode), str(round(damped_frequency, 4)), str(round(damping_ratio, 4))])
            else:
                cols = 2
                new = QTreeWidgetItem([str(mode), str(round(value,4))])

            for i in range(cols):
                new.setTextAlignment(i, Qt.AlignCenter)
            
            self.treeWidget_frequencies.addTopLevelItem(new)

        self.select_first_frequency()

    def select_first_frequency(self):
        if self.treeWidget_frequencies.topLevelItemCount() == 0:
            return
        item = self.treeWidget_frequencies.topLevelItem(0)
        self.treeWidget_frequencies.setCurrentItem(item)
        self.on_click_item(item)

    def on_click_item(self, item):

        selected_frequency = self.modes_to_frequencies[int(item.text(0))]

        if isinstance(selected_frequency, complex):
            damping_ratio = -np.real(selected_frequency) / np.abs(selected_frequency)
            damped_frequency = np.abs(selected_frequency) * ((1-damping_ratio**2)**(1/2))
            self.lineEdit_natural_frequency.setText(str(round(damped_frequency, 4)))
        else:
            self.lineEdit_natural_frequency.setText(str(round(selected_frequency, 4)))

        self.selected_frequency = selected_frequency
        self.animation_widget.reset_sliders()
        self.update_plot()

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_plot()