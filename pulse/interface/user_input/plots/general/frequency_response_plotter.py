from PySide6.QtWidgets import QComboBox, QCheckBox, QDialog, QFrame, QPushButton, QRadioButton, QSpinBox, QVBoxLayout, QToolButton, QWidget
from PySide6.QtGui import QCloseEvent, QColor
from PySide6.QtCore import Qt

from pulse import app, UI_DIR
from pulse.interface.formatters import icons
from pulse.interface.user_input.data_handler.export_model_results import ExportModelResults
from pulse.interface.user_input.data_handler.import_data_to_compare import ImportDataToCompare
from pulse.interface.user_input.plots.general.advanced_cursor import AdvancedCursor

from molde import load_ui

import numpy as np


class FrequencyResponsePlotter(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/results/general/frequency_response_plot.ui"
        load_ui(ui_path, self, UI_DIR)

        app().main_window.set_input_widget(self)

        self._config_window()
        self._initialize()
        self._initialize_canvas()
        self._define_qt_variables()
        self._create_connections()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("Frequency response plotter")

    def _initialize(self):

        self.keep_window_open = True
        self.imported_dB = False
        self._layout = None
        self.x_data = None
        self.y_data = None

        self.importer = None
        self.exporter = None

        self.model_results_data = dict()
        self.imported_results_data = dict()

        self.title = ""
        self.font_weight = "normal"

        self.colors = [ [0,0,1],
                        [0,0,0],
                        [1,0,0],
                        [0,1,1],
                        [0.75,0.75,0.75],
                        [0.5, 0.5, 0.5],
                        [0.25, 0.25, 0.25] ]

    def _define_qt_variables(self):

        # QCheckBox
        self.checkBox_grid : QCheckBox
        self.checkBox_legends : QCheckBox
        self.checkBox_cursor_legends : QCheckBox

        # QComboBox
        self.comboBox_plot_type : QComboBox
        self.comboBox_differentiate_data : QComboBox

        # QFrame
        self.frame_vertical_lines : QFrame

        # QPushButton
        self.pushButton_import_data : QPushButton

        # QRadioButton
        self.radioButton_absolute : QRadioButton
        self.radioButton_real : QRadioButton
        self.radioButton_imaginary : QRadioButton
        self.radioButton_decibel_scale : QRadioButton
        self.radioButton_disable_cursors : QRadioButton
        self.radioButton_cross_cursor : QRadioButton
        self.radioButton_harmonic_cursor : QRadioButton
        self.pushButton_export_data : QPushButton

        # QSpinBox
        self.spinBox_vertical_lines : QSpinBox

        # QWidget
        self.widget_plot : QWidget

    def _create_connections(self):
        #
        self.checkBox_grid.stateChanged.connect(self.plot_data_in_freq_domain)
        self.checkBox_legends.stateChanged.connect(self.plot_data_in_freq_domain)
        self.checkBox_cursor_legends.stateChanged.connect(self.plot_data_in_freq_domain)
        #
        self.comboBox_plot_type.currentIndexChanged.connect(self._update_plot_type)
        self.comboBox_differentiate_data.currentIndexChanged.connect(self.plot_data_in_freq_domain)
        #
        self.radioButton_real.clicked.connect(self._update_comboBox)
        self.radioButton_imaginary.clicked.connect(self._update_comboBox)
        self.radioButton_absolute.clicked.connect(self._update_comboBox)
        self.radioButton_decibel_scale.clicked.connect(self._update_comboBox)
        self.radioButton_disable_cursors.clicked.connect(self.update_cursor_controls)
        self.radioButton_cross_cursor.clicked.connect(self.update_cursor_controls)
        self.radioButton_harmonic_cursor.clicked.connect(self.update_cursor_controls)
        #
        self.pushButton_import_data.clicked.connect(self.import_file)
        self.pushButton_export_data.clicked.connect(self.call_data_exporter)
        #
        app().main_window.theme_changed.connect(self.paint_toolbar_icons)
        self._initial_config()

    def import_file(self):

        if isinstance(self.importer, QDialog):
            if self.importer.isVisible():
                if self.importer.isMinimized():
                    self.importer.showNormal()
                self.importer.raise_()
            else:
                self.importer.exec()
            return

        elif self.importer is None:
            self.importer = ImportDataToCompare(self)
            self.importer.exec()
            app().main_window.set_input_widget(self)

    def _initial_config(self):
        self.aux_bool = False
        self.plot_type = self.comboBox_plot_type.currentText()        
        self.checkBox_cursor_legends.setChecked(False)
        self.checkBox_cursor_legends.setDisabled(True)
        self.frame_vertical_lines.setDisabled(True)

    def _update_comboBox(self):
        self.cache_plot_type = self.comboBox_plot_type.currentText()
        aux_real = self.radioButton_real.isChecked()
        aux_imag = self.radioButton_imaginary.isChecked()
        aux_decibel = self.radioButton_decibel_scale.isChecked()

        self.aux_bool = aux_real + aux_imag + aux_decibel
        if self.aux_bool:
            self.comboBox_plot_type.setDisabled(True)
            self.comboBox_plot_type.setCurrentIndex(2)
        else:
            self.comboBox_plot_type.setDisabled(False)
            self.comboBox_plot_type.setCurrentIndex(0)
        
        if self.plot_type == self.cache_plot_type:
            self.plot_data_in_freq_domain()
        
    def _update_plot_type(self):
        # if self.not_update:
        #     return
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
        from pulse.interface.user_input.plots.general.mpl_canvas import MplCanvas
        self.mpl_canvas_frequency_plot = MplCanvas(self, width=8, height=6, dpi=110)
        self.ax = self.mpl_canvas_frequency_plot.axes
        self.fig = self.mpl_canvas_frequency_plot.fig
    
    def call_data_exporter(self):
        self.hide()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results_data)

    def imported_dB_data(self):
        self.imported_dB = True
        self.comboBox_plot_type.setCurrentIndex(2)
        self.comboBox_plot_type.setDisabled(True)
        self.radioButton_absolute.setDisabled(True)
        self.radioButton_real.setDisabled(True)
        self.radioButton_real.setChecked(True)
        self.radioButton_imaginary.setDisabled(True)
        self.radioButton_decibel_scale.setDisabled(True)
        self.comboBox_differentiate_data.setDisabled(True)

    def load_data_to_plot(self, data: dict):

        if "x_data" in data.keys():
            self.x_data = data["x_data"]
        if "y_data" in data.keys():
            self.y_data = self.get_y_axis_data(data["y_data"])
        if "unit" in data.keys():
            if data["unit"] != "":
                self.unit = data["unit"]
                # if self.unit == "dB":
                #     self.imported_dB_data()
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

    def get_scaled_data(self, data):
        if self.radioButton_decibel_scale.isChecked():
            if self.comboBox_differentiate_data.currentIndex() != 0:
                shift = 1
            else:
                shift = 0
            self.x_data = self.x_data[shift:]
            data2 = np.real(data[shift:]*np.conjugate(data[shift:]))
            if "Pa" in self.unit:
                return 10*np.log10(data2/((2e-5)**2))
            else:
                return 10*np.log10(data2**2)
        else:
            return data

    def get_y_axis_data(self, data):
        dif_data = self.process_differentiation(data)
        if self.radioButton_real.isChecked():
            return np.real(dif_data)
        elif self.radioButton_imaginary.isChecked():
            return np.imag(dif_data)
        elif self.radioButton_absolute.isChecked():
            return np.abs(dif_data)
        else:
            return self.get_scaled_data(dif_data)

    def get_y_axis_label(self, label):
        
        if self.radioButton_real.isChecked():
            type_label = "real"
        elif self.radioButton_imaginary.isChecked():
            type_label = "imaginary"
        else:
            type_label = "absolute"

        if self.imported_dB:
            return f"{label} [dB]"

        unit = self.get_unit_considering_differentiation()
        if self.radioButton_decibel_scale.isChecked():
            return f"{label} - {type_label} [dB]"
        else:
            return f"{label} - {type_label} [{unit}]"

    def process_differentiation(self, data):
        frequencies = self.x_data
        index = self.comboBox_differentiate_data.currentIndex()
        if index == 0:
            output_data = data
        elif index == 1:
            output_data = data*(1j*2*np.pi)*frequencies
        else:
            output_data = data*((1j*2*np.pi*frequencies)**2)           
        return output_data
    
    def get_unit_considering_differentiation(self):
        index = self.comboBox_differentiate_data.currentIndex()
        if index == 0:
            return self.unit
        elif index == 1:
            return self.unit + "/s"
        else:
            return self.unit + "/s²"

    def paint_toolbar_icons(self, *args, **kwargs):
        from pulse.interface.user_input.plots.general.custom_navigation_toolbar import CustomNavigationToolbar
        toolbar = self.findChild(CustomNavigationToolbar)
        if toolbar is None:
            return

        if app().main_window.interface_theme == "dark":
            color = QColor("#5f9af4")
        else:
            color = QColor("#1a73e8")

        icons.change_icon_color_for_widgets(toolbar.findChildren(QToolButton), color)

    def plot_data_in_freq_domain(self):

        self.ax.cla()
        self.legends = []
        self.plots = []

        if self._layout is None:
            from pulse.interface.user_input.plots.general.custom_navigation_toolbar import CustomNavigationToolbar
            toolbar = CustomNavigationToolbar(self.mpl_canvas_frequency_plot, self)

            # Paint the toolbar icons and connect the buttons to paint
            # themselves after every click or draw events
            self.paint_toolbar_icons()
            for button in toolbar.findChildren(QToolButton):
                button.clicked.connect(self.paint_toolbar_icons)                    
            self.mpl_canvas_frequency_plot.mpl_connect("draw_event", self.paint_toolbar_icons)

            self._layout = QVBoxLayout()
            self._layout.addWidget(toolbar)
            self._layout.addWidget(self.mpl_canvas_frequency_plot)
            self._layout.setContentsMargins(2, 2, 2, 2)
            self.widget_plot.setLayout(self._layout)

        for current_data in [self.model_results_data, self.imported_results_data]:
            for _, data in current_data.items():

                self.load_data_to_plot(data)

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
                    elif "log-x" in self.plot_type:
                        _plot = self.call_semilog_x_plot()
                    else:
                        _plot = self.call_lin_lin_plot()

                    self.legends.append(self.legend)
                    self.plots.append(_plot)

        if self.plots:

            if self.checkBox_legends.isChecked():
                self.ax.legend(handles=self.plots, labels=self.legends)
                
            self.call_cursor()
            self.ax.set_xlabel(self.x_label, fontsize = 11, fontweight = self.font_weight)
            self.ax.set_ylabel(self.y_label, fontsize = 11, fontweight = self.font_weight)
            
            if self.title != "":
                self.ax.set_title(self.title, fontsize = 12, fontweight = self.font_weight)

            if self.checkBox_grid.isChecked():
                self.ax.grid()

            self.mpl_canvas_frequency_plot.draw()
            return

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
                if self.mask_x[0] or self.mask_y[0]:
                    _plot = self.call_log_log_plot(first_index=1)
                else:
                    _plot = self.call_log_log_plot(first_index=0)

        elif "log-x" in self.plot_type:
            
            if True in self.mask_x[1:]:
                _plot = self.call_lin_lin_plot()
            else:
                if self.mask_x[0]:
                    _plot = self.call_semilog_x_plot(first_index=1)
                else:
                    _plot = self.call_semilog_x_plot(first_index=0)
        
        elif "log-y" in self.plot_type:
        
            if True in self.mask_y[1:]:
                _plot = self.call_lin_lin_plot()
            else:
                if self.mask_y[0]:
                    _plot = self.call_semilog_y_plot(first_index=1)
                else:
                    _plot = self.call_semilog_y_plot(first_index=0)
        
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

    def _set_model_results_data_to_plot(self, data):
        if isinstance(data, dict):
            self.model_results_data = data
            self.plot_data_in_freq_domain()
            while self.keep_window_open:
                self.exec()

    def _set_imported_results_data_to_plot(self, data):
        if isinstance(data, dict):
            self.imported_results_data = data
            self.plot_data_in_freq_domain()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        if self.exporter is not None:
            self.exporter.close()

        if self.importer is not None:
            self.importer.close()

        self.keep_window_open = False
        return super().closeEvent(a0)