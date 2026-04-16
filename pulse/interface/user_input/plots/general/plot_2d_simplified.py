from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtCore import Qt

from pulse import app
from pulse.interface.ui_generated.plots.graphs.plot_2d_dialog_ui import Plot2dDialog_UI
from pulse.interface.user_input.plots.general.custom_navigation_toolbar import CustomNavigationToolbar
from pulse.interface.user_input.plots.general.mpl_canvas import MplCanvas

import matplotlib.ticker as ticker
import numpy as np
from matplotlib.axes import Axes


class Plot2DSimplified(Plot2dDialog_UI):

    def __init__(
        self,
        title: str = "",
        x_label: str = "",
        y_left_label: str = "",
        y_right_label: str = ""
    ) -> None:

        super().__init__()
        app().main_window.set_input_widget(self)

        self._title = title
        self._x_label = x_label
        self._y_left_label = y_left_label
        self._y_right_label = y_right_label
        self._toolbar: CustomNavigationToolbar = None

        self._config_window()
        self._create_connections()
        self._add_plots_to_widget()
        self._configure_plots()

    def _config_window(self) -> None:
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _create_connections(self) -> None:
        self.pushButton_exit.clicked.connect(self.close)

    def _add_plots_to_widget(self) -> None:
        self.results_plot = MplCanvas(self, width=8, height=6, dpi=110)

        self.left_ax = self.results_plot.ax_left
        self.right_ax = None

        if self.plot_2d_widget.layout() is None:
            self._toolbar = CustomNavigationToolbar(self.results_plot, self)
            layout = QVBoxLayout()
            layout.addWidget(self._toolbar)
            layout.addWidget(self.results_plot)
            self.plot_2d_widget.setLayout(layout)

        self.left_ax.grid(which="both")
        self.results_plot.draw()

    def _configure_plots(self) -> None:
        self.left_ax.set_xlabel(self._x_label)
        self.left_ax.set_ylabel(self._y_left_label)
        self.left_ax.set_title(self._title)
        self.left_ax.xaxis.set_major_formatter(ticker.FuncFormatter(self._format_axes_tick))
        self.left_ax.yaxis.set_major_formatter(ticker.FuncFormatter(self._format_axes_tick))

    def _ensure_right_ax(self) -> Axes:
        if self.right_ax is None:
            self.right_ax = self.left_ax.twinx()
            self.right_ax.set_ylabel(self._y_right_label)
            self.right_ax.grid(which="both")
            self.right_ax.yaxis.set_major_formatter(ticker.FuncFormatter(self._format_axes_tick))
            
        return self.right_ax

    @staticmethod
    def _format_axes_tick(x: float, _) -> str:
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
        y_label_position: str = "left"
    ) -> None:

        if absolute_value:
            y_data = np.abs(y_data)

        if y_label_position == "left":
            ax = self.left_ax
        else:
            ax = self._ensure_right_ax()
        
        ax.plot(
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
        
        self.results_plot.draw()
    
    def show(self) -> None:
        handles_l, labels_l = self.left_ax.get_legend_handles_labels()
        handles_r, labels_r = self.right_ax.get_legend_handles_labels() if self.right_ax is not None else ([], [])
        handles = handles_l + handles_r

        if handles:
            legend_ax = self.right_ax if self.right_ax is not None else self.left_ax
            legend_ax.legend(handles, labels_l + labels_r, loc="upper right")

        super().show()

    def closeEvent(self, a0) -> None:
        return super().closeEvent(a0)
