from PyQt5.QtWidgets import QComboBox, QFrame, QLineEdit, QPushButton, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *

import numpy as np
from pathlib import Path

window_title_1 = "Error"
window_title_2 = "Warning"

class PlotStructuralModeShape(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        main_window = app().main_window

        ui_path = Path(f"{UI_DIR}/plots/results/structural/plot_structural_mode_shape.ui")
        uic.loadUi(ui_path, self)

        self.opv = main_window.opv_widget
        self.opv.setInputObject(self)
        self.project = main_window.project

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self.load_natural_frequencies()

    def _initialize(self):
        self.mode_index = None

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_color_scale = self.findChild(QComboBox, 'comboBox_color_scale')
        # QFrame
        self.frame_button = self.findChild(QFrame, 'frame_button')
        self.frame_button.setVisible(False)
        # QLineEdit
        self.lineEdit_natural_frequency = self.findChild(QLineEdit, 'lineEdit_natural_frequency')
        self.lineEdit_natural_frequency.setDisabled(True)
        # QPushButton
        self.pushButton_plot = self.findChild(QPushButton, 'pushButton_plot')
        # QTreeWidget
        self.treeWidget_frequencies = self.findChild(QTreeWidget, 'treeWidget_frequencies')
        self._config_treeWidget()

    def _create_connections(self):
        self.comboBox_color_scale.currentIndexChanged.connect(self.update_plot)
        self.pushButton_plot.clicked.connect(self.update_plot)
        self.treeWidget_frequencies.itemClicked.connect(self.on_click_item)
        self.treeWidget_frequencies.itemDoubleClicked.connect(self.on_doubleclick_item)
        self.update_animation_widget_visibility()

    def update_animation_widget_visibility(self):
        index = self.comboBox_color_scale.currentIndex()
        if index <= 9:
            app().main_window.results_viewer_wigdet.animation_widget.setDisabled(True)
        else:
            app().main_window.results_viewer_wigdet.animation_widget.setDisabled(False)

    def _config_treeWidget(self):
        widths = [80, 140]
        for i, width in enumerate(widths):
            self.treeWidget_frequencies.setColumnWidth(i, width)
            self.treeWidget_frequencies.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def update_plot(self):
        self.update_animation_widget_visibility()
        if self.lineEdit_natural_frequency.text() == "":
            return
        else:
            self.project.analysis_type_label = "Structural Modal Analysis"
            frequency = self.selected_natural_frequency
            self.mode_index = self.natural_frequencies.index(frequency)
            color_scale_setup = self.get_user_color_scale_setup()
            self.project.set_color_scale_setup(color_scale_setup)
            self.opv.plot_displacement_field(self.mode_index)

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
            absolute = True
        elif index == 1:
            ux_abs_values = True
        elif index == 2:
            uy_abs_values = True
        elif index == 3:
            uz_abs_values = True
        elif index == 4:
            ux_real_values = True
        elif index == 5:
            uy_real_values = True
        elif index == 6:
            uz_real_values = True
        elif index == 7:
            ux_imag_values = True
        elif index == 8:
            uy_imag_values = True
        elif index == 9:
            uz_imag_values = True
        elif index == 10:
            absolute_animation = True
        elif index == 11:
            ux_animation = True
        elif index == 12:
            uy_animation = True
        else:
            uz_animation = True  

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

    def load_natural_frequencies(self):
        
        self.natural_frequencies = self.project.natural_frequencies_structural
        modes = np.arange(1, len(self.natural_frequencies)+1, 1)
        self.dict_modes_frequencies = dict(zip(modes, self.natural_frequencies))

        self.treeWidget_frequencies.clear()
        for mode, natural_frequency in self.dict_modes_frequencies.items():
            new = QTreeWidgetItem([str(mode), str(round(natural_frequency,4))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_frequencies.addTopLevelItem(new)
        
        # data = np.zeros((len(self.dict_modes_frequencies),2))
        # data[:,0] = np.array(list(self.dict_modes_frequencies.keys()))
        # data[:,1] = np.array(list(self.dict_modes_frequencies.values()))
        # header = "Mode || Natural frequency [Hz]"
        # np.savetxt("natural_frequencies_reference.dat", data, delimiter=";", header=header)

    def on_click_item(self, item):
        self.selected_natural_frequency = self.dict_modes_frequencies[int(item.text(0))]
        self.lineEdit_natural_frequency.setText(str(round(self.selected_natural_frequency,4)))
        self.update_plot()

    def on_doubleclick_item(self, item):
        self.selected_natural_frequency = self.dict_modes_frequencies[int(item.text(0))]
        self.lineEdit_natural_frequency.setText(str(round(self.selected_natural_frequency,4)))
        self.update_plot()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.update_plot()
        elif event.key() == Qt.Key_Escape:
            self.close()