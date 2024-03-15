import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
matplotlib.use('Qt5Agg')

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # fig = Figure(figsize=(width+5, height+5), dpi=dpi)
        self.fig = Figure()#(dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.fig.set_tight_layout(True)
        super(MplCanvas, self).__init__(self.fig)