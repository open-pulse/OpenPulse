from enum import IntEnum

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QDialog, QLineEdit, QVBoxLayout

from pulse import app
from pulse.interface import error_title
from pulse.interface.ui_generated.plots.results.general.frequency_response_plotter_ui import FrequencyResponsePlotter_UI
from pulse.interface.formatters.icons import Icon
from pulse.interface.user_input.data_handler.export_model_results import ExportModelResults
from pulse.interface.user_input.data_handler.data_import_assistant import DataImportAssistant
from pulse.interface.user_input.plots.general.advanced_cursor import AdvancedCursor
from pulse.interface.user_input.project.print_message import PrintMessageInput


class DataFormat(IntEnum):
    ABSOLUTE = 0
    REAL = 1
    IMAGINARY = 2
    DECIBEL_SCALE = 3


class PlotType(IntEnum):
    LOG_Y = 0
    LOG_X = 1
    LIN_LIN = 2
    LOG_LOG = 3


class DisplayHarmonicLines(IntEnum):
    DISABLED = 0
    ENABLED = 1


class Differentiate(IntEnum):
    NONE = 0
    SINGLE = 1
    DOUBLE = 2


class CursorIndex(IntEnum):
    DISABLED = 0
    CROSS = 1
    HARMONIC = 2


class FrequencyResponsePlotter(FrequencyResponsePlotter_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()

        app().main_window.set_input_widget(self)

        self._config_window()
        self._initialize()
        self._initialize_canvas()
        self._create_connections()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("Frequency response plotter")

    def _initialize(self):

        self.keep_window_open = True
        self.decibel_data = False
        self._layout = None
        self.x_data = None
        self.y_data = None
        self.f_cut = None

        self.importer = None
        self.exporter = None

        self.model_results_data = dict()
        self.imported_results_data = dict()

        self.title = ""
        self.font_weight = "normal"

        self.colors = [ 
            [0,0,1],
            [0,0,0],
            [1,0,0],
            [0,1,1],
            [0.75,0.75,0.75],
            [0.5, 0.5, 0.5],
            [0.25, 0.25, 0.25],
            ]

    def _create_connections(self):
        #
        self.checkBox_grid.stateChanged.connect(self.plot_data_in_freq_domain)
        self.checkBox_legends.stateChanged.connect(self.plot_data_in_freq_domain)
        self.checkBox_cursor_legends.stateChanged.connect(self.plot_data_in_freq_domain)
        #
        self.comboBox_plot_type.currentIndexChanged.connect(self.plot_type_changed_callback)
        self.comboBox_differentiate_data.currentIndexChanged.connect(self.plot_data_in_freq_domain)
        self.comboBox_harmonic_lines_control.currentIndexChanged.connect(self.plot_harmonic_lines_callback)
        self.comboBox_data_format.currentIndexChanged.connect(self.data_format_changed_callback)
        self.comboBox_cursor_control.currentIndexChanged.connect(self.cursor_controls_changed_callback)
        #
        self.lineEdit_harmonic_lines_1st_freq.textChanged.connect(self.plot_harmonic_lines_callback)
        self.lineEdit_harmonic_lines_1st_freq.returnPressed.connect(self.plot_harmonic_lines_callback)
        #
        self.pushButton_import_data.clicked.connect(self.import_file)
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_display_hfrequencies.clicked.connect(self.update_harmonic_lines_legend_icon)
        #
        self.spinBox_harmonic_lines_number.valueChanged.connect(self.plot_harmonic_lines_callback)
        # 
        #
        self._initial_config()
        self.plot_harmonic_lines_callback()

    def update_harmonic_lines_legend_icon(self):

        if "Display" in self.pushButton_display_hfrequencies.toolTip():
            icon = Icon(":/icons/common/visibility_off.png")
            tool_tip = "Remove harmonic line frequencies"

        else:
            icon = Icon(":/icons/common/visibility.png")
            tool_tip = "Display harmonic line frequencies"

        self.pushButton_display_hfrequencies.setIcon(icon)
        self.pushButton_display_hfrequencies.setToolTip(tool_tip)

        self.plot_harmonic_lines_callback()

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
            self.importer = DataImportAssistant(self)
            self.importer.exec()

    def _initial_config(self):
        self.linear_plot = False
        self.plot_type_index = self.comboBox_plot_type.currentIndex()
        self.checkBox_cursor_legends.setChecked(False)
        self.checkBox_cursor_legends.setDisabled(True)
        self.frame_vertical_lines.setDisabled(True)

    def data_format_changed_callback(self):

        self.cache_plot_type = self.comboBox_plot_type.currentIndex()
        self.linear_plot = self.comboBox_data_format.currentIndex() != DataFormat.ABSOLUTE
        self.comboBox_plot_type.setDisabled(self.linear_plot)

        if self.linear_plot:
            self.comboBox_plot_type.setCurrentIndex(PlotType.LIN_LIN)
        else:
            self.comboBox_plot_type.setCurrentIndex(PlotType.LOG_Y)

        if self.plot_type_index == self.cache_plot_type:
            self.plot_data_in_freq_domain()

    def plot_type_changed_callback(self):
        self.plot_type_index = self.comboBox_plot_type.currentIndex()
        self.plot_data_in_freq_domain()

    def cursor_controls_changed_callback(self):
        cursor_disabled = self.comboBox_cursor_control.currentIndex() == CursorIndex.DISABLED
        self.checkBox_cursor_legends.setDisabled(cursor_disabled)
        self.frame_vertical_lines.setDisabled(cursor_disabled)

        if cursor_disabled:
            self.checkBox_cursor_legends.setChecked(False)

        self.plot_data_in_freq_domain()

    def _initialize_canvas(self):
        from pulse.interface.user_input.plots.general.mpl_canvas import MplCanvas
        self.mpl_canvas_frequency_plot = MplCanvas(self, width=8, height=6, dpi=110)
        self.ax = self.mpl_canvas_frequency_plot.axes
        self.fig = self.mpl_canvas_frequency_plot.fig

    def export_data_callback(self):
        self.hide()
        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results_data)

    def plot_harmonic_lines(
        self,
        fundamental_freq: float,
        n_harmonics: int,
        display_hfrequencies: bool,
        remove_all: bool,
    ):
        if self.x_data is None:
            return
        
        plotted_lines = [line for line in self.ax.lines if getattr(line, "is_harmonic_line", False)]
        for line in plotted_lines:
            line.remove()
        
        plotted_texts = [text for text in self.ax.texts if getattr(text, "is_harmonic_label", False)]
        for text in plotted_texts:
            text.remove()

        if not remove_all:
            x_min, x_max = self.ax.get_xlim()

            for i in range(n_harmonics):
                frequency = float((i + 1) * fundamental_freq)

                if x_min <= frequency <= x_max:
                    line = self.ax.axvline(x=frequency, color=(214/255, 126/255, 44/255), linestyle="--", alpha=0.8, label="_nolegend_")
                    line.is_harmonic_line = True

                    legend = f" {i + 1}x"
                    newline = "\n"

                    if display_hfrequencies:
                        legend += f"{newline} ({round(frequency, 3)} Hz)"

                    if legend != "":
                        txt = self.ax.text(
                            frequency,
                            0.95,
                            legend,
                            transform=self.ax.get_xaxis_transform(),
                            fontsize=6,
                            verticalalignment="bottom",
                            horizontalalignment="left",
                        )
                        txt.is_harmonic_label = True

        self.mpl_canvas_frequency_plot.draw()

    def check_inputs(
        self, 
        line_edit: QLineEdit, 
        ):

        message = ""
        title = "Invalid value typed"
        input_value = line_edit.text().replace(",", ".").strip()

        if input_value == "":
            return None

        try:
            output_value = float(input_value)

            if output_value <= 0:
                message = "Enter a positive non-zero value in the 'Frequency (1x)' input field."

        except Exception as error_log:
            message = "You have typed an invalid value in the 'Frequency (1x)' input field.\n\n"
            message += str(error_log)

        if message != "":
            self.hide()
            line_edit.setFocus()
            PrintMessageInput([error_title, title, message])
            return None

        return output_value

    def plot_harmonic_lines_callback(self):

        plot_hlines = self.comboBox_harmonic_lines_control.currentIndex() == DisplayHarmonicLines.ENABLED

        self.lineEdit_harmonic_lines_1st_freq.setEnabled(plot_hlines)
        self.spinBox_harmonic_lines_number.setEnabled(plot_hlines)
        self.pushButton_display_hfrequencies.setEnabled(plot_hlines)

        if not plot_hlines:
            self.plot_harmonic_lines(0, 0, False, True)
            return

        value = self.check_inputs(self.lineEdit_harmonic_lines_1st_freq)
        if value is None:
            return

        number_of_lines = self.spinBox_harmonic_lines_number.value()
        display_hfrequencies = "Remove" in self.pushButton_display_hfrequencies.toolTip()

        self.plot_harmonic_lines(
            value,
            number_of_lines,
            display_hfrequencies,
            False,
        )

    def imported_real_data(self, decibel_data: bool=False):
        self.decibel_data = decibel_data

        self.comboBox_plot_type.setDisabled(True)
        self.comboBox_data_format.setDisabled(True)
        self.comboBox_differentiate_data.setDisabled(True)

        self.comboBox_plot_type.setCurrentIndex(PlotType.LIN_LIN)
        if decibel_data:
            self.comboBox_data_format.setCurrentIndex(DataFormat.DECIBEL_SCALE)
        else:
            self.comboBox_data_format.setCurrentIndex(DataFormat.REAL)

    def load_data_to_plot(self, data: dict):

        if data.get("type") != "imported_data":
            self.x_label = data.get("x_label")
            self.unit = data.get("unit", "?")
            self.y_label = self.get_y_axis_label(data.get("y_label"))

        self.x_data = data.get("x_data")
        self.y_data = self.get_y_axis_data(data.get("y_data"))

        self.color = data.get("color")
        self.title = data.get("title")
        self.legend = data.get("legend")
        self.linestyle = data.get("linestyle")

    def get_scaled_data(self, data: np.ndarray):
        if self.comboBox_data_format.currentIndex() != DataFormat.DECIBEL_SCALE:
            return data

        shift = 0
        if self.comboBox_differentiate_data.currentIndex() != Differentiate.NONE:
            shift = 1
            
        self.x_data = self.x_data[shift:]
        data2 = np.real(data[shift:]*np.conjugate(data[shift:]))

        if self.unit == "Pa":
            return 10*np.log10(data2/((2e-5)**2))

        return 10*np.log10(data2)

    def get_y_axis_data(self, data: np.ndarray | None):
        if data is None:
            return None

        if self.decibel_data:
            return data

        dif_data = self.process_differentiation(data)
        data_format_index = self.comboBox_data_format.currentIndex()

        if data_format_index == DataFormat.REAL:
            return np.real(dif_data)

        elif data_format_index == DataFormat.IMAGINARY:
            return np.imag(dif_data)

        elif data_format_index == DataFormat.ABSOLUTE:
            return np.abs(dif_data)

        else:
            return self.get_scaled_data(dif_data)

    def get_y_axis_label(self, label: str):
        
        data_format_index = self.comboBox_data_format.currentIndex()
        if data_format_index == DataFormat.REAL:
            type_label = "real"

        elif data_format_index == DataFormat.IMAGINARY:
            type_label = "imaginary"

        else:
            type_label = "absolute"

        if self.decibel_data:
            return f"{label} [dB]"

        unit = self.get_unit_considering_differentiation()
        if data_format_index == DataFormat.DECIBEL_SCALE:
            return f"{label} - {type_label} [dB]"

        return f"{label} - {type_label} [{unit}]"

    def process_differentiation(self, data: np.ndarray):
        frequencies = self.x_data
        n = self.comboBox_differentiate_data.currentIndex()

        return data*((1j*2*np.pi*frequencies)**n)

    def get_unit_considering_differentiation(self):
        index = self.comboBox_differentiate_data.currentIndex()
        if index == 0:
            return self.unit
        elif index == 1:
            return self.unit + "/s"
        else:
            return self.unit + "/s²"

    def plot_data_in_freq_domain(self):

        self.ax.cla()
        self.legends = list()
        self.plots = list()

        if self._layout is None:

            from pulse.interface.user_input.plots.general.custom_navigation_toolbar import CustomNavigationToolbar

            toolbar = CustomNavigationToolbar(self.mpl_canvas_frequency_plot, self)

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

                    has_single_point = len(self.x_data) == 1

                    if self.linear_plot:
                        _plot = self.call_lin_lin_plot()

                    # elif True in (self.mask_x + self.mask_y):
                    #     _plot = self.get_plot_considering_invalid_log_values()

                    elif self.plot_type_index == PlotType.LOG_LOG:
                        _plot = self.call_log_log_plot()

                    elif self.plot_type_index == PlotType.LOG_Y:
                        _plot = self.call_semilog_y_plot()

                    elif self.plot_type_index == PlotType.LOG_X:
                        _plot = self.call_semilog_x_plot()

                    else:
                        _plot = self.call_lin_lin_plot()

                    if has_single_point:
                        _plot.set_marker('o')
                        _plot.set_markersize(8)
                
                    self.legends.append(self.legend)
                    self.plots.append(_plot)

        if self.plots:
               
            self.call_cursor()
            self.ax.set_xlabel(self.x_label, fontsize = 10, fontweight = self.font_weight)
            self.ax.set_ylabel(self.y_label, fontsize = 10, fontweight = self.font_weight)
            
            if self.title != "":
                self.ax.set_title(self.title, fontsize = 11, fontweight = self.font_weight)

            if self.checkBox_grid.isChecked():
                self.ax.grid()

            if isinstance(self.f_cut, float):
                f_cut = round(self.f_cut, 4)
                _plot = self.ax.axvline(x=f_cut, color=(0.9, 0.4, 0), visible=True, linestyle="--", linewidth=1)
                self.plots.append(_plot)
                self.legends.append(f'Pipe cut-off frequency $f_c$ = {f_cut} [Hz]')

            if self.checkBox_legends.isChecked():
                self.ax.legend(handles=self.plots, labels=self.legends, fontsize=9)

            self.mpl_canvas_frequency_plot.draw()

            if self.comboBox_harmonic_lines_control.currentIndex() == DisplayHarmonicLines.ENABLED:
                self.plot_harmonic_lines_callback()

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

        if self.comboBox_plot_type.currentIndex() != PlotType.LIN_LIN:
            self.comboBox_plot_type.blockSignals(True)
            self.comboBox_plot_type.setCurrentIndex(PlotType.LIN_LIN)
            self.comboBox_plot_type.blockSignals(False)

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

        if self.plot_type_index == PlotType.LOG_LOG:
            if True in self.mask_y[1:] or True in self.mask_x[1:]:
                _plot = self.call_lin_lin_plot()
            else:
                if self.mask_x[0] or self.mask_y[0]:
                    _plot = self.call_log_log_plot(first_index=1)
                else:
                    _plot = self.call_log_log_plot(first_index=0)

        elif self.plot_type_index == PlotType.LOG_X:
            if True in self.mask_x[1:]:
                _plot = self.call_lin_lin_plot()
            else:
                if self.mask_x[0]:
                    _plot = self.call_semilog_x_plot(first_index=1)
                else:
                    _plot = self.call_semilog_x_plot(first_index=0)

        elif self.plot_type_index == PlotType.LOG_Y:
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

        show_cursor = self.comboBox_cursor_control.currentIndex() != CursorIndex.DISABLED
        show_legend = self.checkBox_cursor_legends.isChecked()
        
        number_vlines = 1
        if self.comboBox_cursor_control.currentIndex() == CursorIndex.HARMONIC:
            number_vlines = self.spinBox_vertical_lines.value()

        self.cursor = AdvancedCursor(   
            self.ax, 
            self.x_data, 
            self.y_data, 
            show_cursor,
            show_legend,
            number_vlines = number_vlines,
            )

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
        
    def reset_imported_results_data_to_plot(self):
        self.imported_results_data = dict()
        self.plot_data_in_freq_domain()

    def set_cutoff_frequency(self, f_cut: float):
        self.f_cut = f_cut

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        if self.exporter is not None:
            self.exporter.close()

        if isinstance(self.importer, QDialog):
            if self.importer.isVisible():
                self.importer.close()
            self.importer = None

        self.keep_window_open = False
        return super().closeEvent(a0)