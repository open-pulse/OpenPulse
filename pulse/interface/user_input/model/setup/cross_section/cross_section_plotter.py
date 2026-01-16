import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from molde import load_ui
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QDialog, QToolButton, QVBoxLayout, QWidget

from pulse import UI_DIR, app
from pulse.interface.formatters import icons


class CrossSectionPlotter(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "plots/model/cross_section_plotter.ui"
        load_ui(ui_path, self, UI_DIR)

        app().main_window.set_input_widget(self)

        self._config_window()
        self._initialize()
        self._define_qt_variables()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("Cross section plotter")

    def _initialize(self):
        app().main_window.theme_changed.connect(self.paint_toolbar_icons)

    def _define_qt_variables(self):
        self.widget_plot: QWidget

    def paint_toolbar_icons(self, *args, **kwargs):
        from pulse.interface.user_input.plots.general.custom_navigation_toolbar import (
            CustomNavigationToolbar,
        )

        toolbar = self.findChild(CustomNavigationToolbar)
        if toolbar is None:
            return

        if app().main_window.interface_theme == "dark":
            color = QColor("#5f9af4")
        else:
            color = QColor("#1a73e8")

        icons.change_icon_color_for_widgets(toolbar.findChildren(QToolButton), color)

    def plot_cross_section(self, points, section_type_label, section_type):
        if len(points) == 6:
            Yp, Zp, Yp_ins, Zp_ins, Yc, Zc = points
        elif len(points) == 4:
            Yp, Zp, Yc, Zc = points
            Yp_ins = Zp_ins = None
        else:
            raise NotImplementedError()

        layout = self.widget_plot.layout()
        if layout is None:
            layout = QVBoxLayout()
            self.widget_plot.setLayout(layout)

        fig = Figure(figsize=(8, 8))
        ax = fig.add_subplot(1, 1, 1)
        canvas = FigureCanvasQTAgg(fig)
        layout.addWidget(canvas)

        _max = np.max(np.abs(np.array([Yp, Zp])))

        first_plot = ax.fill(
            Yp,
            Zp,
            color=[0.2, 0.2, 0.2],
            linewidth=2,
            zorder=2,
        )
        second_plot = ax.scatter(
            Yc,
            Zc,
            marker="+",
            linewidth=2,
            zorder=3,
            color=[1, 0, 0],
            s=150,
            label=f"y: {Yc:7.5e} // z: {Zc:7.5e}",
        )
        third_plot = ax.scatter(
            0,
            0,
            marker="+",
            linewidth=1.5,
            zorder=4,
            color=[0, 0, 1],
            s=120,
        )

        if section_type_label in ["pipe", "reducer"] and Yp_ins is not None:
            filled = ax.fill(Yp_ins, Zp_ins, color=[0.5, 1, 1], linewidth=2, zorder=5)[
                0
            ]
            filled.set_label("Insulation material")

            _max = np.max(np.abs(np.array([Zp_ins, Yp_ins]))) * 1.2
            ax.legend(
                handles=[second_plot, filled],
                framealpha=1,
                facecolor=[1, 1, 1],
                loc="upper right",
                title=r"$\bf{Centroid}$ $\bf{coordinates:}$",
            )
        else:
            ax.legend(
                handles=[second_plot],
                framealpha=1,
                facecolor=[1, 1, 1],
                loc="upper right",
                title=r"$\bf{Centroid}$ $\bf{coordinates:}$",
            )

        ax.set_title("CROSS-SECTION PLOT", fontsize=18, fontweight="bold")
        ax.set_xlabel("y [m]", fontsize=16, fontweight="bold")
        ax.set_ylabel("z [m]", fontsize=16, fontweight="bold")

        f = 1.25
        if section_type == 3:
            ax.set_xlim(-(1 / 2) * _max, (3 / 2) * _max)
        else:
            ax.set_xlim(-_max * f, _max * f)

        ax.set_ylim(-_max * f, _max * f)
        ax.grid(True)

        canvas.draw()
