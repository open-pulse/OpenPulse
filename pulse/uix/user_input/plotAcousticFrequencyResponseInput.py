from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QTreeWidgetItem, QTabWidget, QLabel, QCheckBox, QPushButton
from pulse.utils import error
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf
import matplotlib.pyplot as plt
import numpy as np


class SnaptoCursor(object):
    def __init__(self, ax, x, y, show_cursor):

        self.ax = ax
        self.x = x
        self.y = y
        self.show_cursor = show_cursor

        if show_cursor:
                
            self.vl = self.ax.axvline(x=x[0], color='k', alpha=0.3, label='_nolegend_')  # the vertical line
            self.hl = self.ax.axhline(y=y[0], color='k', alpha=0.3, label='_nolegend_')  # the horizontal line 
            self.marker, = ax.plot(x[0], y[0], markersize=4, marker="s", color=[0,0,0], zorder=3)
            # self.marker.set_label("x: %1.2f // y: %4.2e" % (self.x[0], self.y[0]))
            # plt.legend(handles=[self.marker], loc='lower left', title=r'$\bf{Cursor}$ $\bf{coordinates:}$')

    def mouse_move(self, event):
        if self.show_cursor:   

            if not event.inaxes: return
            x, y = event.xdata, event.ydata
            if x>=np.max(self.x): return

            indx = np.searchsorted(self.x, [x])[0]
            
            x = self.x[indx]
            y = self.y[indx]
            self.vl.set_xdata(x)
            self.hl.set_ydata(y)
            self.marker.set_data([x],[y])
            self.marker.set_label("x: %1.2f // y: %1.2f" % (x, y))
            plt.legend(handles=[self.marker], loc='lower left', title=r'$\bf{Cursor}$ $\bf{coordinates:}$')
    
            self.ax.figure.canvas.draw_idle()


class PlotAcousticFrequencyResponseInput(QDialog):
    def __init__(self, mesh, analysisMethod, frequencies, solution, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/plotAcousticFrequencyResponseInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.mesh = mesh
        
        self.analysisMethod = analysisMethod
        self.frequencies = frequencies
        self.solution = solution
        self.nodeID = 0

        self.mag = False
        self.real = False

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')

        self.checkBox_mag = self.findChild(QCheckBox, 'checkBox_mag')
        self.checkBox_real = self.findChild(QCheckBox, 'checkBox_real')

        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.pushButton.clicked.connect(self.check)

        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def check(self):
        try:
            tokens = self.lineEdit_nodeID.text().strip().split(',')
            try:
                tokens.remove('')
            except:
                pass
            node_typed = list(map(int, tokens))
            if len(node_typed) == 1:
                try:
                    self.nodeID = self.mesh.nodes[node_typed[0]].external_index
                except:
                    message = [" The Node ID input values must be\n major than 1 and less than {}.".format(len(self.nodes))]
                    error(message[0], title = " INCORRECT NODE ID INPUT! ")
                    return
            elif len(node_typed) == 0:
                error("Please, enter a valid Node ID!")
                return
            else:
                error("Multiple Node IDs", title="Error Node ID's")
                return
        except Exception:
            error("Wrong input for Node ID's!", title="Error Node ID's")
            return
        
        if self.checkBox_real.isChecked() and self.checkBox_mag.isChecked() == True:
            error("You must check only one plot representation data option!", title = " WARNING ")
            return
        elif self.checkBox_mag.isChecked():
            self.mag = True
            self.real = False

        elif self.checkBox_real.isChecked():
            self.real = True
            self.mag = False
        
        self.plot()

    def dB(self, data):
        p_ref = 20e-6 
        return 20*np.log10(data/p_ref)

    def plot(self):
        dB = True

        if dB:
            unit_label = "dB"
        else:
            unit_label = "Pa"            

        frequencies = self.frequencies
        dof_response = get_acoustic_frf(self.mesh, self.solution, self.nodeID, absolute=self.mag, real=self.real, dB=dB)
        fig = plt.figure(figsize=[12,8])
        ax = fig.add_subplot(1,1,1)
        mng = plt.get_current_fig_manager()
        # mng.window.state('zoomed')

        #cursor = Cursor(ax)
        cursor = SnaptoCursor(ax, frequencies, dof_response, show_cursor=True)
        plt.connect('motion_notify_event', cursor.mouse_move)

        legend_label = "Acoustic Pressure at node {}".format(self.nodeID)

        if dof_response.all()==0:
            first_plot, = plt.plot(frequencies, dof_response, color=[1,0,0], linewidth=2, label=legend_label)
        else:    
            first_plot, = plt.plot(frequencies, dof_response, color=[1,0,0], linewidth=2, label=legend_label)
        
        first_legend = plt.legend(handles=[first_plot], loc='upper right')
        plt.gca().add_artist(first_legend)

        ax.set_title(('Frequency Response: {} Method').format(self.analysisMethod), fontsize = 18, fontweight = 'bold')
        ax.set_xlabel(('Frequency [Hz]'), fontsize = 16, fontweight = 'bold')
        if self.mag:
            ax.set_ylabel(("Pressure amplitude [{}]").format(unit_label), fontsize = 16, fontweight = 'bold')
        else:
            ax.set_ylabel(("Real part of Pressure Spectrum [{}]").format(unit_label), fontsize = 16, fontweight = 'bold')
        plt.show()