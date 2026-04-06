from PySide6.QtWidgets import QDialog, QToolButton, QVBoxLayout, QWidget
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

from pulse import app
# from pulse.interface.ui_generated.plots.graphs.plot_2d_widget_ui import PlotXyWidget_UI
from pulse.interface.ui_generated.plots.graphs.plot_2d_dialog_ui import Plot2dDialog_UI
from pulse.interface.formatters import icons

# import matplotlib
# matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass, field
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

plt.rcParams.update({'font.size': 10})


@dataclass
class PlotSettings:
    number_of_plots: int = 1
    legends : list = field(default_factory=[""])
    title : str = ""
    x_label : str = ""
    y_label : str = ""
    line_styles : list = field(default_factory=["-"])
    line_widths : list = field(default_factory=[2])
    colors : tuple = field(default_factory=(0,0,1))
    markers : list = field(default_factory=[None])
    marker_sizes : list = field(default_factory=[5])


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=None, secondary_axis=False):
        fig = Figure()#(figsize=(width+5, height+5), dpi=dpi)
        self.ax_left = fig.add_subplot(111)
        if secondary_axis:
            self.ax_right = self.ax_left.twinx()
        fig.set_tight_layout(True)
        super(MplCanvas, self).__init__(fig)


class Plot2DSimplified(Plot2dDialog_UI):

    def __init__(self, plot_config: PlotSettings, **kwargs):
        super().__init__()
        app().main_window.set_input_widget(self)
        app().main_window.theme_changed.connect(self.paint_toolbar_icons)

        self.plot_config = plot_config

        self._config_window()
        self._create_connections()
        self._add_plots_to_widget()
        self._create_plots()
        self._configure_plots()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")
    
    def _create_connections(self):
        self.pushButton_exit.clicked.connect(self.close)

    def _add_plots_to_widget(self):

        self.plots = list()
        self.results_plot = MplCanvas(self, width=8, height=6, dpi=110, secondary_axis=False)

        if self.plot_2d_widget.layout() is None:
            toolbar = NavigationToolbar2QT(self.results_plot, self)
            self.paint_toolbar_for_current_mpl(toolbar, self.results_plot)
            #
            layout = QVBoxLayout()
            layout.addWidget(toolbar)
            layout.addWidget(self.results_plot)
            self.plot_2d_widget.setLayout(layout)

    def _create_plots(self):

        self.plots: list[Line2D]

        for i in range(self.plot_config.number_of_plots):
            plot_i, = self.results_plot.ax_left.plot(
                [],
                [],
                color = self.plot_config.colors[i],
                linewidth = self.plot_config.line_widths[i],
                linestyle = self.plot_config.line_styles[i],
                marker = self.plot_config.markers[i],
                markersize = self.plot_config.marker_sizes[i], 
                markerfacecolor = self.plot_config.colors[i],
                )

            self.plots.append(plot_i)

        self.results_plot.ax_left.grid()
        self.results_plot.draw()

    def _configure_plots(self):
        self.results_plot.ax_left.set_xlabel(self.plot_config.x_label)
        self.results_plot.ax_left.set_ylabel(self.plot_config.y_label)
        self.results_plot.ax_left.set_title(self.plot_config.title)
        self.results_plot.ax_left.legend(self.plots, self.plot_config.legends, loc="upper right")

    def set_plot_data(
            self, 
            x_data: np.ndarray, 
            y_data: np.ndarray, 
            plot_index: int, 
            axes_limits: (list | tuple | str),
            ):

        self.plots[plot_index].set_data(x_data, y_data)

        # TODO: try to find a solution to better adjust the axes limits
        if isinstance(axes_limits, (list | tuple)):
            xlim, ylim = axes_limits

        else:
            xlim = (0.9 * min(x_data), 1.1 * max(x_data))
            ylim = (0.9 * min(y_data), 1.1 * max(y_data))

            # self.results_plot.ax_left.autoscale()
            # self.results_plot.ax_left.autoscale_view()

        if xlim[0] != xlim[1]:
            self.results_plot.ax_left.set_xlim(*xlim)
    
        if ylim[0] != ylim[1]:
            self.results_plot.ax_left.set_ylim(*ylim)

        self.results_plot.draw()

    def paint_toolbar_for_current_mpl(self, toolbar, mpl_plot):
        self.paint_toolbar_icons()
        for button in toolbar.findChildren(QToolButton):
            button.clicked.connect(self.paint_toolbar_icons)                    
        mpl_plot.mpl_connect("draw_event", self.paint_toolbar_icons)

    def paint_toolbar_icons(self, *args, **kwargs):

        if app().main_window.interface_theme == "dark":
            color = QColor("#5f9af4")
        else:
            color = QColor("#1a73e8")

        for toolbar in self.findChildren(NavigationToolbar2QT):
            buttons = toolbar.findChildren(QToolButton)
            icons.change_icon_color_for_widgets(buttons, color)

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