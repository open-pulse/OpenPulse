import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100, secondary_axis=False):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.ax_left = self.fig.add_subplot(111)
        self.ax_right = None
        if secondary_axis:
            self.ax_right = self.ax_left.twinx()
        self.fig.set_layout_engine("tight")
        super().__init__(self.fig)