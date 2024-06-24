from PyQt5.QtWidgets import QComboBox, QFrame, QLineEdit, QPushButton, QSlider, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *

import numpy as np


class PlotNodalResultsFieldForHarmonicAnalysis(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/results/structural/plot_nodal_results_field_for_harmonic_analysis.ui"
        uic.loadUi(ui_path, self)

        main_window = app().main_window

        self.opv = main_window.opv_widget
        self.opv.setInputObject(self)
        self.project = main_window.project

        self._initialize()
        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self.load_frequencies_vector()
        self.load_user_preference_colormap()

    def _initialize(self):
        self.frequencies = self.project.frequencies
        self.frequency_to_index = dict(zip(self.frequencies, np.arange(len(self.frequencies), dtype=int)))
        self.frequency = None
        self.colormaps = ["jet",
                          "viridis",
                          "inferno",
                          "magma",
                          "plasma",
                          "grayscale"]

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)

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
        self.update_colormap_type()

    def update_animation_widget_visibility(self):
        index = self.comboBox_color_scale.currentIndex()
        if index >= 4:
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
        self.update_plot()

    def _config_treeWidget(self):
        widths = [80, 140]
        for i, width in enumerate(widths):
            self.treeWidget_frequencies.setColumnWidth(i, width)
            self.treeWidget_frequencies.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def update_transparency_callback(self):
        transparency = self.slider_transparency.value() / 100
        
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
                self.frequency = self.frequency_to_index[frequency_selected]
                color_scale_setup = self.get_user_color_scale_setup()
                self.project.set_color_scale_setup(color_scale_setup)
                self.opv.plot_displacement_field(self.frequency)
                app().main_window.results_widget.show_displacement_field(self.frequency)


    def get_user_color_scale_setup(self):

        absolute = False
        ux_abs_values = False
        uy_abs_values = False
        uz_abs_values = False
        ux_real_values = False
        uy_real_values = False
        uz_real_values = False
        ux_imag_values = False
        uy_imag_values = False
        uz_imag_values = False
        absolute_animation = False
        ux_animation = False
        uy_animation = False
        uz_animation = False

        index = self.comboBox_color_scale.currentIndex()

        if index == 0:
            absolute_animation = True
        elif index == 1:
            ux_animation = True
        elif index == 2:
            uy_animation = True
        elif index == 3:
            uz_animation = True
        elif index == 4:
            absolute = True
        elif index == 5:
            ux_abs_values = True
        elif index == 6:
            uy_abs_values = True
        elif index == 7:
            uz_abs_values = True
        elif index == 8:
            ux_real_values = True
        elif index == 9:
            uy_real_values = True
        elif index == 10:
            uz_real_values = True
        elif index == 11:
            ux_imag_values = True
        elif index == 12:
            uy_imag_values = True
        elif index == 13:
            uz_imag_values = True

        color_scale_setup = {   "absolute" : absolute,
                                "ux_abs_values" : ux_abs_values,
                                "uy_abs_values" : uy_abs_values,
                                "uz_abs_values" : uz_abs_values,
                                "ux_real_values" : ux_real_values,
                                "uy_real_values" : uy_real_values,
                                "uz_real_values" : uz_real_values,
                                "ux_imag_values" : ux_imag_values,
                                "uy_imag_values" : uy_imag_values,
                                "uz_imag_values" : uz_imag_values,
                                "absolute_animation" : absolute_animation,
                                "ux_animation" : ux_animation,
                                "uy_animation" : uy_animation,
                                "uz_animation" : uz_animation   }

        return color_scale_setup

    def load_frequencies_vector(self):

        if self.project.analysis_ID == 7:
            self.plot_displacement_for_static_analysis()
            
        self.treeWidget_frequencies.clear()
        for index, frequency in enumerate(self.frequencies):
            new = QTreeWidgetItem([str(index+1), str(frequency)])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_frequencies.addTopLevelItem(new)

    def plot_displacement_for_static_analysis(self):
        self.lineEdit_selected_frequency.setDisabled(True)
        self.treeWidget_frequencies.setDisabled(True)
        self.frequency = [0]
        self.lineEdit_selected_frequency.setText(str(self.frequency[0]))
        color_scale_setup = self.get_user_color_scale_setup()
        self.project.set_color_scale_setup(color_scale_setup)
        self.opv.plot_displacement_field(self.frequency[0])
        app().main_window.results_widget.show_displacement_field(self.frequency[0])

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