from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtCore import Qt

from pulse import app
from pulse.interface.ui_generated.plots.graphs.plot_2d_dialog_ui import Plot2dDialog_UI
from pulse.interface.user_input.plots.general.custom_navigation_toolbar import CustomNavigationToolbar
from pulse.interface.user_input.plots.general.mpl_canvas import MplCanvas

import matplotlib.ticker as ticker
import numpy as np


class Plot2DSimplified(Plot2dDialog_UI):

    def __init__(
        self,
        title: str = "",
        x_label: str = "",
        y_label: str = "",
    ):

        super().__init__()
        app().main_window.set_input_widget(self)

        self._title = title
        self._x_label = x_label
        self._y_label = y_label
        self._toolbar: CustomNavigationToolbar = None
        self._has_legend = False

        self._config_window()
        self._create_connections()
        self._add_plots_to_widget()
        self._configure_plots()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _create_connections(self):
        self.pushButton_exit.clicked.connect(self.close)

    def _add_plots_to_widget(self):
        self.results_plot = MplCanvas(self, width=8, height=6, dpi=110)

        if self.plot_2d_widget.layout() is None:
            self._toolbar = CustomNavigationToolbar(self.results_plot, self)
            layout = QVBoxLayout()
            layout.addWidget(self._toolbar)
            layout.addWidget(self.results_plot)
            self.plot_2d_widget.setLayout(layout)

        self.results_plot.ax_left.grid(which="both")
        self.results_plot.draw()

    def _configure_plots(self):
        ax = self.results_plot.ax_left
        ax.set_xlabel(self._x_label)
        ax.set_ylabel(self._y_label)
        ax.set_title(self._title)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(self._format_axes_tick))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(self._format_axes_tick))

    @staticmethod
    def _format_axes_tick(x, _):
        if x == 0:
            return "0"

        mantissa_str, exp_str = f"{x:.2e}".split("e")
        exponent = int(exp_str)

        if abs(exponent) <= 2:
            return f"{x:g}"

        mantissa = float(mantissa_str)
        return f"{mantissa:.1f}e{exponent}"

    def set_plot_data(
        self,
        x_data: np.ndarray,
        y_data: np.ndarray,
        label: str = None,
        line_style: str = "-",
        line_width: float = 1.5,
        color: tuple = (0, 0, 1),
        marker: str = None,
        marker_size: int = 5,
        absolute_value: bool = False,
    ):

        if absolute_value:
            y_data = np.abs(y_data)

        self.results_plot.ax_left.plot(
            x_data,
            y_data,
            label=label,
            linestyle=line_style,
            linewidth=line_width,
            color=color,
            marker=marker,
            markersize=marker_size,
            markerfacecolor=color,
        )

        if label is not None:
            self._has_legend = True
            self.results_plot.ax_left.legend(loc="upper right")

        self.results_plot.draw()

    def closeEvent(self, a0):
        return super().closeEvent(a0)
