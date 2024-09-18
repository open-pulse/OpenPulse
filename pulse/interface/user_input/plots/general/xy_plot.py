# fmt: off

from PyQt5.QtWidgets import QToolButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters import icons

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# matplotlib.use('Qt5Agg')
plt.rcParams.update({'font.size': 10})


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=None, secondary_axis=False):
        fig = Figure()#(figsize=(width+5, height+5), dpi=dpi)
        self.ax_left = fig.add_subplot(111)
        if secondary_axis:
            self.ax_right = self.ax_left.twinx()
        fig.set_tight_layout(True)
        super(MplCanvas, self).__init__(fig)

class XYPlot(QWidget):

    def __init__(self, plot_config: dict):
        super().__init__()

        ui_path = UI_DIR / "plots/graphs/plot_xy_widget.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        app().main_window.theme_changed.connect(self.paint_toolbar_icons)

        self.number_of_plots = plot_config.get("number_of_plots", 1)
        self.x_label = plot_config.get("x_label", "")
        self.y_label = plot_config.get("y_label", "")
        self.title = plot_config.get("title", "")
        self.legends = plot_config.get("legends", list())
        self.colors = plot_config.get("colors", (0,0,1))
        self.line_styles = plot_config.get("line_styles", "-")
        self.markers = plot_config.get("markers", None)

        self._config_window()
        self._initialize_canvas()
        self._add_plots_to_widget()
        self._create_plots()
        self._configure_plots()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize_canvas(self):
        self.plots = list()
        self.results_plot = MplCanvas(self, width=8, height=6, dpi=110, secondary_axis=False)

    def _add_plots_to_widget(self):
        if self.layout() is None:
            toolbar = NavigationToolbar2QT(self.results_plot, self)
            self.paint_toolbar_for_current_mpl(toolbar, self.results_plot)
            #
            layout = QVBoxLayout()
            layout.addWidget(toolbar)
            layout.addWidget(self.results_plot)
            self.setLayout(layout)

    def _create_plots(self):

        for i in range(self.number_of_plots):
            plot_i, = self.results_plot.ax_left.plot(
                                                     [], 
                                                     [], 
                                                     color=self.colors[i], 
                                                     linewidth=1, 
                                                     linestyle=self.line_styles[i], 
                                                     marker=self.markers[i], 
                                                     markersize=5, 
                                                     markerfacecolor=self.colors[i]
                                                     )

            self.plots.append(plot_i)

        self.results_plot.ax_left.grid()
        self.results_plot.draw()

    def _configure_plots(self):
        self.results_plot.ax_left.set_xlabel(self.x_label)
        self.results_plot.ax_left.set_ylabel(self.y_label)
        self.results_plot.ax_left.set_title(self.title)
        self.results_plot.ax_left.legend(self.plots, self.legends, loc="upper right")

    def set_plot_data(self, x_data, y_data, plot_index, axes_limits):
        self.plots[plot_index].set_data(x_data, y_data)
        xlim, ylim = axes_limits
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

    #     from pulse.interface.user_input.plots.general.xy_plot import XYPlot

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

    #     self.xy_plot = XYPlot(plots_config)
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

# fmt: on