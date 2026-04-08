from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtCore import Qt

from pulse import app
# from pulse.interface.ui_generated.plots.graphs.plot_2d_widget_ui import PlotXyWidget_UI
from pulse.interface.ui_generated.plots.graphs.plot_2d_dialog_ui import Plot2dDialog_UI
from pulse.interface.user_input.plots.general.custom_navigation_toolbar import CustomNavigationToolbar
from pulse.interface.user_input.plots.general.mpl_canvas import MplCanvas

# import matplotlib
# matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from dataclasses import dataclass, field
from matplotlib.lines import Line2D

plt.rcParams.update({'font.size': 10})


@dataclass
class PlotSettings:
    title : str = ""
    x_label : str = ""
    y_label : str = ""

class Plot2DSimplified(Plot2dDialog_UI):

    def __init__(
        self, 
        title: str = "", 
        x_label: str = "", 
        y_label: str = "",
        **kwargs
    ):
        
        super().__init__()
        app().main_window.set_input_widget(self)

        self.plot_settings = PlotSettings(title, x_label, y_label)
        self._toolbar: CustomNavigationToolbar = None
        self._plot_index = 0

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
            #
            layout = QVBoxLayout()
            layout.addWidget(self._toolbar)
            layout.addWidget(self.results_plot)
            self.plot_2d_widget.setLayout(layout)

        self.results_plot.ax_left.grid()
        self.results_plot.draw()

    def _configure_plots(self):
        self.results_plot.ax_left.set_xlabel(self.plot_settings.x_label)
        self.results_plot.ax_left.set_ylabel(self.plot_settings.y_label)
        self.results_plot.ax_left.set_title(self.plot_settings.title)
        # self.results_plot.ax_left.legend(self.plots, self.plot_settings.legends, loc="upper right")
        self.results_plot.ax_left.xaxis.set_major_formatter(
            ticker.FuncFormatter(self._format_axes_tick)
        )
        self.results_plot.ax_left.yaxis.set_major_formatter(
            ticker.FuncFormatter(self._format_axes_tick)
        )
        # self.results_plot.ax_left.ticklabel_format(style="sci", axis="x", scilimits=(-2, 2))

    @staticmethod
    def _format_axes_tick(x, _):
        mantissa, exp = f"{x:.2e}".split("e")
        sign = "-" if exp[0] == "-" else ""
 
        if int(exp[1:]) <= 2:
            return f"{x:g}"

        return f"{mantissa[:3]}e{sign}{int(exp[1:])}"

    def set_plot_data(
        self, 
        x_data: np.ndarray, 
        y_data: np.ndarray,
        label: str = None,
        line_style: str = "-",
        line_width: int = 1.5,
        color: tuple = (1, 0, 0),
        marker: str = None,
        marker_size: int = 5,
        axes_limits: (list | tuple | str) = "auto",
    ):
    
        self.results_plot.axes.plot(
            x_data,
            y_data,
            label=label,
            linestyle=line_style,
            linewidth=line_width,
            color=color,
            marker=marker,
            markersize=marker_size,
            markerfacecolor=color
        )

        if label is not None:
            self.results_plot.axes.legend(loc="upper right")
        
        self.results_plot.draw()
    
    def closeEvent(self, a0):
        return super().closeEvent(a0)

    # def create_convergence_plots(self):

    #     fig = plt.figure(figsize=[8,6])
    #     self.ax  = fig.add_subplot(1,1,1)

    #     xlim = (1, 10)
    #     ylim = (0, 120)
    #     self.ax.set_xlim(*xlim)
    #     self.ax.set_ylim(*ylim)
    #     perc_criteria = self.target*100

    #     self.first_plot, = plt.plot([], [], color=[1,0,0], linewidth=1, marker='s', markersize=6, markerfacecolor=[0,0,1])
    #     self.second_plot, = plt.plot(xlim, [perc_criteria, perc_criteria], color=[0,0,0], linewidth=1, linestyle="--")
    #     self.third_plot, = plt.plot([], [], color=[0,0,1], linewidth=1, marker='s', markersize=6, markerfacecolor=[1,0,0])

    #     first_plot_label = "Pressure residues"
    #     third_plot_label = "Delta pressure residues"
    #     second_plot_label = f'Target: {perc_criteria}%'
        
    #     _legends = plt.legend(handles=[self.first_plot, self.third_plot, self.second_plot], labels=[first_plot_label, third_plot_label, second_plot_label])

    #     plt.gca().add_artist(_legends)
    #     plt.grid()

    #     self.ax.set_title('Perforated plate convergence plot', fontsize = 11)
    #     self.ax.set_xlabel('Iteration [n]', fontsize = 10)
    #     self.ax.set_ylabel("Relative error [%]", fontsize = 10)

    #     plt.ion()
    #     plt.show()

    # def initialize_xy_plotter(self):

    #     from pulse.interface.user_input.plots.general.xy_plot import Plot2DSimplified

    #     legends = [f'Target: {self.target*100}%', "Pressure residues", "Delta pressure residues"]

    #     plots_config = {
    #                     "number_of_plots" : 3,
    #                     "x_label" : "Iterations [n]",
    #                     "y_label" : "Relative error [%]",
    #                     "colors" : [(0,0,0), (0,0,1), (1,0,0)],
    #                     "line_styles" : ["--", "-", "-"],
    #                     "legends" : legends,
    #                     "title" : "Perforated plate convergence plot"
    #                     }

    #     self.xy_plot = Plot2DSimplified(plots_config)
    #     self.xy_plot.show()

    # def create_convergence_plots(self):

    #     fig = self.plt.figure(figsize=[8,6])
    #     self.ax  = fig.add_subplot(1,1,1)

    #     xlim = (1, 10)
    #     ylim = (0, 120)
    #     self.ax.set_xlim(*xlim)
    #     self.ax.set_ylim(*ylim)
    #     perc_criteria = self.target*100

    #     self.first_plot, = self.plt.plot([], [], color=[1,0,0], linewidth=1, marker='s', markersize=6, markerfacecolor=[0,0,1])
    #     self.second_plot, = self.plt.plot(xlim, [perc_criteria, perc_criteria], color=[0,0,0], linewidth=1, linestyle="--")
    #     self.third_plot, = self.plt.plot([], [], color=[0,0,1], linewidth=1, marker='s', markersize=6, markerfacecolor=[1,0,0])

    #     first_plot_label = "Pressure residues"
    #     third_plot_label = "Delta pressure residues"
    #     second_plot_label = f'Target: {perc_criteria}%'
        
    #     _legends = self.plt.legend(handles=[self.first_plot, self.third_plot, self.second_plot], labels=[first_plot_label, third_plot_label, second_plot_label])

    #     self.plt.gca().add_artist(_legends)
    #     self.plt.grid()

    #     self.ax.set_title('Perforated plate convergence plot', fontsize = 11)
    #     self.ax.set_xlabel('Iteration [n]', fontsize = 10)
    #     self.ax.set_ylabel("Relative error [%]", fontsize = 10)

    #     self.plt.ion()
    #     self.plt.show()

    # def update_convergence_plots(self):

    #     if (len(self.iterations) < 2) or (len(self.relative_error) < 2):
    #         xlim = (1, 10)
    #         ylim = (0, 120)
    #     else:
    #         dy = 20
    #         xlim = (1, max(self.iterations))
    #         ylim = (0, (round(max(self.relative_error)/dy,0)+1)*dy)

    #     self.ax.set_xlim(*xlim)
    #     self.ax.set_ylim(*ylim)

    #     self.first_plot.set_xdata(self.iterations)
    #     self.first_plot.set_ydata(self.relative_error)

    #     if self.deltaP_errors:
    #         self.third_plot.set_xdata(self.iterations)
    #         self.third_plot.set_ydata(self.deltaP_errors)

    #     self.plt.draw()