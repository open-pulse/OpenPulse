from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

from data.user_input.plots.mpl_canvas import MplCanvas
from pulse.tools.advanced_cursor import AdvancedCursor

def get_icons_path(filename):
    path = f"data/icons/{filename}"
    if os.path.exists(path):
        return str(Path(path))

class FrequencyResponsePlotter(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui/plots_/results_/frequency_response_plot.ui'), self)

        self.icon = QIcon(get_icons_path('pulse.png'))
        self.search_icon = QIcon(get_icons_path('searchFile.png'))
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Frequency response plotter")

        self._reset_variables()
        self._initialize_canvas()
        self._define_qt_variables()
        self._create_connections()

    def _reset_variables(self):
        self._layout = None
        self.x_data = None
        self.y_data = None
        self.title = ""
        self.font_weight = "normal"
        self.data_to_plot = dict()

    def _define_qt_variables(self):
        # QCheckBox
        self.checkBox_grid = self.findChild(QCheckBox, 'checkBox_grid')
        self.checkBox_legends = self.findChild(QCheckBox, 'checkBox_legends')
        self.checkBox_cursor_legends = self.findChild(QCheckBox, 'checkBox_cursor_legends')
        # QComboBox
        self.comboBox_plot_type = self.findChild(QComboBox, 'comboBox_plot_type')
        # QFrame
        self.frame_vertical_lines = self.findChild(QFrame, 'frame_vertical_lines') 
        # QRadioButton
        self.radioButton_plotAbs = self.findChild(QRadioButton, 'radioButton_plotAbs')
        self.radioButton_plotReal = self.findChild(QRadioButton, 'radioButton_plotReal')
        self.radioButton_plotImag = self.findChild(QRadioButton, 'radioButton_plotImag')
        self.radioButton_disable_cursors = self.findChild(QRadioButton, 'radioButton_disable_cursors')
        self.radioButton_cross_cursor = self.findChild(QRadioButton, 'radioButton_cross_cursor')
        self.radioButton_harmonic_cursor = self.findChild(QRadioButton, 'radioButton_harmonic_cursor')
        # QWidget
        self.widget_plot = self.findChild(QWidget, 'widget_plot')

    def _create_connections(self):
        self.comboBox_plot_type.currentIndexChanged.connect(self._update_plot_type)
        self.checkBox_grid.stateChanged.connect(self.plot_data_in_freq_domain)
        self.checkBox_legends.stateChanged.connect(self.plot_data_in_freq_domain)
        self.checkBox_cursor_legends.stateChanged.connect(self.plot_data_in_freq_domain)
        self.radioButton_plotReal.clicked.connect(self._update_comboBox)
        self.radioButton_plotImag.clicked.connect(self._update_comboBox)
        self.radioButton_plotAbs.clicked.connect(self._update_comboBox)
        self.radioButton_disable_cursors.clicked.connect(self.update_cursor_controls)
        self.radioButton_cross_cursor.clicked.connect(self.update_cursor_controls)
        self.radioButton_harmonic_cursor.clicked.connect(self.update_cursor_controls)
        self._update_comboBox()
        self.update_cursor_controls()

    def _update_comboBox(self):
        self.aux_bool = self.radioButton_plotReal.isChecked() + self.radioButton_plotImag.isChecked()
        if self.aux_bool:
            self.comboBox_plot_type.setCurrentIndex(2)
            self.comboBox_plot_type.setDisabled(True)
        else:
            self.comboBox_plot_type.setCurrentIndex(0)
            self.comboBox_plot_type.setDisabled(False)
        self.plot_type = self.comboBox_plot_type.currentText()
        self.plot_data_in_freq_domain()

    def _update_plot_type(self):
        self.plot_type = self.comboBox_plot_type.currentText()
        self.plot_data_in_freq_domain()

    def update_cursor_controls(self):
        if self.radioButton_disable_cursors.isChecked():
            self.checkBox_cursor_legends.setChecked(False)
            self.checkBox_cursor_legends.setDisabled(True)
            self.frame_vertical_lines.setDisabled(True)
        else:
            self.checkBox_cursor_legends.setDisabled(False)
            if self.radioButton_harmonic_cursor.isChecked():
                self.frame_vertical_lines.setDisabled(False)
        self.plot_data_in_freq_domain()

    def _initialize_canvas(self):
        self.mpl_canvas_frequency_plot = MplCanvas(self, width=8, height=6, dpi=110)
        self.ax = self.mpl_canvas_frequency_plot.axes
        self.fig = self.mpl_canvas_frequency_plot.fig

    def load_data_to_plot(self, data):
        if "x_data" in data.keys():
            self.x_data = data["x_data"]
        if "y_data" in data.keys():
            self.y_data = self.get_y_axis_data(data["y_data"])
        if "unit" in data.keys():
            self.unit = data["unit"]
        if "x_label" in data.keys():
            self.x_label = data["x_label"]
        if "y_label" in data.keys():
            text = data["y_label"]
            self.y_label = self.get_y_axis_label(text)
        if "color" in data.keys():
            self.color = data["color"]
        if "linestyle" in data.keys():
            self.linestyle = data["linestyle"]
        if "legend" in data.keys():
            self.legend = data["legend"]
        if "title" in data.keys():
            self.title = data["title"]

    def get_y_axis_data(self, data):
        if self.radioButton_plotReal.isChecked():
            return np.real(data)
        elif self.radioButton_plotImag.isChecked():
            return np.imag(data)
        else:
            return np.abs(data)

    def get_y_axis_label(self, label):
        if self.radioButton_plotReal.isChecked():
            type_label = "real"
        elif self.radioButton_plotImag.isChecked():
            type_label = "imaginary"
        else:
            type_label = "absolute"
        return f"{label} - {type_label} [{self.unit}]"

    def plot_data_in_freq_domain(self):

        self.ax.cla()
        self.legends = []
        self.plots = []

        for key, data in self.data_to_plot.items():
            self.load_data_to_plot(data)
            self.current_plot = 1

            if self.y_data is not None:
                self.mask_x = self.x_data <= 0
                self.mask_y = self.y_data <= 0
                if self.aux_bool:
                    _plot = self.call_lin_lin_plot()
                elif True in (self.mask_x + self.mask_y):
                    _plot = self.get_plot_considering_invalid_log_values()
                elif "log-log" in self.plot_type:
                    _plot = self.call_log_log_plot()
                elif "log-y" in self.plot_type:
                    _plot = self.call_semilog_y_plot()
                else:
                    _plot = self.call_lin_lin_plot()

                self.legends.append(self.legend)
                self.plots.append(_plot)

                if self._layout is None:
                    toolbar = NavigationToolbar2QT(self.mpl_canvas_frequency_plot, self)
                    self._layout = QVBoxLayout()
                    self._layout.addWidget(toolbar)
                    self._layout.addWidget(self.mpl_canvas_frequency_plot)
                    self._layout.setContentsMargins(2, 2, 2, 2)
                    self.widget_plot.setLayout(self._layout)

        if len(self.plots) != 0:
            if self.checkBox_legends.isChecked():
                self.ax.legend(handles=self.plots, labels=self.legends)
                
            self.call_cursor()
            self.ax.set_xlabel(self.x_label, fontsize = 11, fontweight = self.font_weight)
            self.ax.set_ylabel(self.y_label, fontsize = 11, fontweight = self.font_weight)
            self.ax.set_title(self.title, fontsize = 12, fontweight = self.font_weight)

            if self.checkBox_grid.isChecked():
                self.ax.grid()
            self.mpl_canvas_frequency_plot.draw()

    def call_semilog_y_plot(self, first_index=0):
        _plot, = self.ax.semilogy(  self.x_data[first_index:], 
                                    self.y_data[first_index:], 
                                    linewidth = 1,
                                    color = self.color, 
                                    linestyle = self.linestyle  )
        return _plot
    
    def call_semilog_x_plot(self, first_index=0):
        _plot, = self.ax.semilogx(  self.x_data[first_index:], 
                                    self.y_data[first_index:], 
                                    linewidth = 1,
                                    color = self.color, 
                                    linestyle = self.linestyle  )
        return _plot

    def call_lin_lin_plot(self):
        _plot, = self.ax.plot(  self.x_data, 
                                self.y_data, 
                                linewidth = 1,
                                color = self.color, 
                                linestyle = self.linestyle  )
        return _plot

    def call_log_log_plot(self, first_index=0):
        _plot, = self.ax.loglog(self.x_data[first_index:], 
                                self.y_data[first_index:], 
                                linewidth = 1,
                                color = self.color, 
                                linestyle = self.linestyle  )
        return _plot
    
    def get_plot_considering_invalid_log_values(self):
        if "log-log" in self.plot_type:
            if True in self.mask_y[1:] or True in self.mask_x[1:]:
                _plot = self.call_lin_lin_plot()
            else:
                _plot = self.call_log_log_plot(first_index=1)
        elif "log-x" in self.plot_type:
            if True in self.mask_x[1:]:
                _plot = self.call_lin_lin_plot()
            else:
                _plot = self.call_semilog_x_plot(first_index=1)
        elif "log-y" in self.plot_type:
            if True in self.mask_y[1:]:
                _plot = self.call_lin_lin_plot()
            else:
                _plot = self.call_semilog_y_plot(first_index=1)    
        else:
            _plot = self.call_lin_lin_plot()
        return _plot

    def call_cursor(self):

        show_cursor = not self.radioButton_disable_cursors.isChecked()
        show_legend = self.checkBox_cursor_legends.isChecked()
        
        if self.radioButton_harmonic_cursor.isChecked():
            number_vertLines = self.spinBox_vertical_lines.value()    
        else:
            number_vertLines = 1

        self.cursor = AdvancedCursor(   self.ax, 
                                        self.x_data, 
                                        self.y_data, 
                                        show_cursor,
                                        show_legend,
                                        number_vertLines = number_vertLines   )

        self.mouse_connection = self.fig.canvas.mpl_connect(s='motion_notify_event', func=self.cursor.mouse_move)

    def _set_data_to_plot(self, data):
        if isinstance(data, dict):
            self.data_to_plot = data
            self.plot_data_in_freq_domain()
            self.exec()