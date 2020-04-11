import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from pulse.processing.assembly import get_global_matrices
from pulse.processing.solution import direct_method, modal_superposition
from pulse.postprocessing.plot_data import get_frf

import numpy as np


class FRF(FigureCanvasQTAgg):
    def __init__(self, project, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.project = project
        self.axes = fig.add_subplot(111)
        super(FRF, self).__init__(fig)
        self.setWindowTitle("FRF")
        try:
            frequencies = np.arange(0, 1401, 7)
            modes = 140
            direct = direct_method(self.project.getMesh(), frequencies)
            modal = modal_superposition(self.project.getMesh(), frequencies, modes)

            # GETTING FRF
            node = 96
            local_dof = 1
            x = frequencies
            yd = get_frf(self.project.getMesh(), direct, node, local_dof)
            ym = get_frf(self.project.getMesh(), modal, node, local_dof)

            # PLOTTING RESULTS
            self.axes.semilogy(x, yd)
            self.axes.semilogy(x, ym)
        except Exception as e:
            print("Erro frf {}".format(e))