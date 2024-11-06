from PyQt5.QtWidgets import QComboBox, QFrame, QLineEdit, QPushButton, QSlider, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

class PlotAcousticModeShape(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/results/acoustic/acoustic_mode_shape.ui"
        uic.loadUi(ui_path, self)

        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.load_natural_frequencies()
        self.load_user_preference_colormap()
       
    def _initialize(self):
        self.mode_index = None
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

        # QComboBox
        self.comboBox_color_scale : QComboBox
        self.comboBox_colormaps : QComboBox

        # QFrame
        self.frame_button : QFrame

        # QLineEdit
        self.lineEdit_natural_frequency : QLineEdit

        # QPushButton
        self.pushButton_plot : QPushButton

        # QLineEdit
        self.lineEdit_selected_frequency : QLineEdit

        # QPushButton
        self.pushButton_plot : QPushButton

        # QSlider
        self.slider_transparency : QSlider

        # QTreeWidget
        self.treeWidget_frequencies : QTreeWidget

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

        if isinstance(app().project.complex_natural_frequencies_acoustic, np.ndarray):
            widths = [60, 170]
            headers = ["Mode", "Damped frequency [Hz]", "Damping ratio [--]"]

        else:
            widths = [120, 160]
            headers = ["Mode", "Frequency [Hz]"]

        font = QFont()
        font.setPointSize(9)

        for i, header in enumerate(headers):
            self.treeWidget_frequencies.headerItem().setFont(i, font)
            self.treeWidget_frequencies.headerItem().setText(i, header)
            if i < 2:
                self.treeWidget_frequencies.setColumnWidth(i, widths[i])
            self.treeWidget_frequencies.headerItem().setTextAlignment(i, Qt.AlignCenter)
            
    def update_animation_widget_visibility(self):
        index = self.comboBox_color_scale.currentIndex()
        if index >= 2:
            app().main_window.animation_toolbar.setDisabled(True)
        else:
            app().main_window.animation_toolbar.setDisabled(False) 

    def load_user_preference_colormap(self):
        try:
            app().main_window.load_user_preferences()
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

    def update_plot(self):

        self.update_animation_widget_visibility()
        if self.lineEdit_natural_frequency.text() == "":
            return
        
        app().project.analysis_type_label = "Acoustic Modal Analysis"
        self.mode_index = self.natural_frequencies.index(self.selected_frequency)
            
        color_scale_setup = self.get_user_color_scale_setup()
        app().project.set_color_scale_setup(color_scale_setup)
        app().main_window.results_widget.show_pressure_field(self.mode_index)
        app().main_window.results_widget.clear_cache()

    def update_transparency_callback(self):
        transparency = self.slider_transparency.value() / 100
        app().main_window.results_widget.set_tube_actors_transparency(transparency)

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

    def load_natural_frequencies(self):

        if isinstance(app().project.complex_natural_frequencies_acoustic, np.ndarray):
            self.natural_frequencies = list(app().project.complex_natural_frequencies_acoustic)

        else:
            self.natural_frequencies = list(app().project.natural_frequencies_acoustic)

        modes = np.arange(1, len(self.natural_frequencies) + 1, 1)
        self.modes_to_frequencies = dict(zip(modes, self.natural_frequencies))

        self.treeWidget_frequencies.clear()
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

    def on_click_item(self, item):

        selected_frequency = self.modes_to_frequencies[int(item.text(0))]

        if isinstance(selected_frequency, complex):
            damping_ratio = -np.real(selected_frequency) / np.abs(selected_frequency)
            damped_frequency = np.abs(selected_frequency) * ((1-damping_ratio**2)**(1/2))
            self.lineEdit_natural_frequency.setText(str(round(damped_frequency, 4)))
        else:
            self.lineEdit_natural_frequency.setText(str(round(selected_frequency, 4)))

        self.selected_frequency = selected_frequency
        self.update_plot()

    def on_doubleclick_item(self, item):
        self.on_click_item(item)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_plot()
    #     elif event.key() == Qt.Key_Escape:
    #         self.close()