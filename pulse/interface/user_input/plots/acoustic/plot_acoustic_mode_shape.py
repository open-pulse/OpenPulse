from PyQt5.QtWidgets import QComboBox, QFrame, QLineEdit, QPushButton, QSlider, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
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
        self.update_colormap_type()

    def _config_widgets(self):

        self.frame_button.setVisible(False)
        self.lineEdit_natural_frequency.setDisabled(True)

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
        frequency = self.selected_natural_frequency
        self.mode_index = self.natural_frequencies.index(frequency)
            
        color_scale_setup = self.get_user_color_scale_setup()
        app().project.set_color_scale_setup(color_scale_setup)
        app().main_window.results_widget.show_pressure_field(self.mode_index)

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

        self.natural_frequencies = list(app().project.natural_frequencies_acoustic)
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
        natural_frequency = self.modes_to_frequencies[int(item.text(0))]
        self.lineEdit_natural_frequency.setText(str(natural_frequency))
        self.update_plot()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_plot()
        elif event.key() == Qt.Key_Escape:
            self.close()