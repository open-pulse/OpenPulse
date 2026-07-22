import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout

from pulse import app
from pulse.interface.ui_generated.plots.model.cross_section_plotter_ui import (
    CrossSectionPlotter_UI,
)

class CrossSectionPlotter(CrossSectionPlotter_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app().main_window.set_input_widget(self)

        self._config_window()
        self._create_connections()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("Cross section plotter")

    def _create_connections(self):
        self.close_button.clicked.connect(self.close)

    def plot_cross_section(self, plot_data: list, section_type_label: str):

        if len(plot_data) == 6:
            Zp, Yp, Zp_ins, Yp_ins, Zc, Yc = plot_data

        elif len(plot_data) == 4:
            Zp, Yp, Zc, Yc = plot_data
            Zp_ins = Yp_ins = None

        else:
            raise NotImplementedError()

        layout = self.widget_plot.layout()
        if layout is None:
            layout = QVBoxLayout()
            self.widget_plot.setLayout(layout)

        fig = Figure(figsize=(8, 8), tight_layout=True)
        ax = fig.add_subplot(1, 1, 1)
        ax.set_aspect("equal")

        canvas = FigureCanvasQTAgg(fig)
        layout.addWidget(canvas)

        _max = np.max(np.abs(np.array([Zp, Yp])))

        first_plot = ax.fill(
            Zp,
            Yp,
            color=[0.2, 0.2, 0.2],
            linewidth=2,
            zorder=2,
        )

        second_plot = ax.scatter(
            Zc,
            Yc,
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
            filled = ax.fill(Zp_ins, Yp_ins, color=[0.5, 1, 1], linewidth=2, zorder=5)[
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

        # ax.set_title("CROSS-SECTION PLOT", fontsize=12, fontweight="bold")
        ax.set_xlabel("z [m]", fontsize=12, fontweight="bold")
        ax.set_ylabel("y [m]", fontsize=12, fontweight="bold")

        f = 1.4
        if section_type_label == "c_beam":
            ax.set_xlim(-(1 / 2) * _max, (3 / 2) * _max)
        else:
            ax.set_xlim(-_max * f, _max * f)

        ax.set_ylim(-_max * f, _max * f)
        ax.grid(True)

        canvas.draw()