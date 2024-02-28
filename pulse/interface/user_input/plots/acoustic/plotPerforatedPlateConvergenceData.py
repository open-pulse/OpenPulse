from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

import matplotlib
import matplotlib.pyplot as plt

from pulse.processing.solution_acoustic import relative_error
from pulse.interface.user_input.project.printMessageInput import PrintMessageInput

from pulse import app

class PlotPerforatedPlateConvergenceData(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.project = project

        main_window = app().main_window
        self.project = main_window.project
        data_log = self.project.perforated_plate_data_log

        [iterations, pressure_residues, delta_residues, target] = data_log
        self.plot_convergence_graph(iterations, pressure_residues, delta_residues, target)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            plt.close()
            self.close()

    def plot_convergence_graph(self, iterations, pressure_residues, delta_residues, target):
        
        plt.close()
        self.fig = plt.figure(figsize=[8,6])
        self.ax = self.fig.add_subplot(1,1,1)
        
        x, y = 500, 100
        backend = matplotlib.get_backend()
        mngr = plt.get_current_fig_manager()

        if backend == 'TkAgg':
            mngr.window.wm_geometry("+%d+%d" % (x, y))
        elif backend == 'WXAgg':
            mngr.window.SetPosition((x, y))
        else:
            mngr.window.move(x, y)
        
        first_plot, = plt.plot(iterations, pressure_residues, color=[1,0,0], linewidth=2, marker='s', markersize=6, markerfacecolor=[0,0,1])
        second_plot, = plt.plot([1, max(iterations)], [target, target], color=[0,0,0], linewidth=2, linestyle="--")
        if delta_residues:
            third_plot, = plt.plot(iterations, delta_residues, color=[0,0,1], linewidth=2, marker='s', markersize=6, markerfacecolor=[1,0,0])

        first_plot_label = "Pressure residues"
        third_plot_label = "Delta pressure residues"
        second_plot_label = f'Target: {target}%'
        if delta_residues:
            _legends = plt.legend(handles=[first_plot, third_plot, second_plot], labels=[first_plot_label, third_plot_label, second_plot_label])#, loc='upper right')
        else:
            _legends = plt.legend(handles=[first_plot, second_plot], labels=[first_plot_label, second_plot_label])#, loc='upper right')
        plt.gca().add_artist(_legends)

        self.ax.set_title('PERFORATED PLATE: CONVERGENCE PLOT', fontsize = 16, fontweight = 'bold')
        self.ax.set_xlabel('Iteration [n]', fontsize = 14, fontweight = 'bold')
        self.ax.set_ylabel("Relative error [%]", fontsize = 14, fontweight = 'bold')

        # plt.xlim(1, max(iterations))
        plt.show()
        # plt.pause(0.001)