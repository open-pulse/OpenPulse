from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QLabel, QCheckBox, QPushButton
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from pulse.postprocessing.plot_structural_data import get_structural_frf
import matplotlib.pyplot as plt
import numpy as np


class SnaptoCursor(object):
    def __init__(self, ax, x, y, show_cursor):

        self.ax = ax
        self.x = x
        self.y = y
        self.show_cursor = show_cursor

        if show_cursor:
                
            self.vl = self.ax.axvline(x=np.min(x), ymin=np.min(y), color='k', alpha=0.3, label='_nolegend_')  # the vertical line
            self.hl = self.ax.axhline(color='k', alpha=0.3, label='_nolegend_')  # the horizontal line 
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
            self.marker.set_label("x: %1.2f // y: %4.2e" % (x, y))
            plt.legend(handles=[self.marker], loc='lower left', title=r'$\bf{Cursor}$ $\bf{coordinates:}$')
    
            self.ax.figure.canvas.draw_idle()


class PlotStructuralFrequencyResponseFunctionInput(QDialog):
    def __init__(self, mesh, analysisMethod, frequencies, solution, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/plotStructuralFrequencyResponseFunctionInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.mesh = mesh
        
        self.analysisMethod = analysisMethod
        self.frequencies = frequencies
        self.solution = solution
        self.nodeID = 0

        self.localDof = None

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')

        self.checkBox_ux = self.findChild(QCheckBox, 'checkBox_ux')
        self.checkBox_uy = self.findChild(QCheckBox, 'checkBox_uy')
        self.checkBox_uz = self.findChild(QCheckBox, 'checkBox_uz')
        self.checkBox_rx = self.findChild(QCheckBox, 'checkBox_rx')
        self.checkBox_ry = self.findChild(QCheckBox, 'checkBox_ry')
        self.checkBox_rz = self.findChild(QCheckBox, 'checkBox_rz')

        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.pushButton.clicked.connect(self.check)

        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def error(self, msg, title = "Error"):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(msg)
        msg_box.setWindowTitle(title)
        msg_box.exec_()

    def check(self):
        self.localDof = None
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
                    self.error("Incorrect Node ID input!")
                    return
            elif len(node_typed) == 0:
                self.error("Please, enter a valid Node ID!")
                return
            else:
                self.error("Multiple Node IDs", "Error Node ID's")
                return
        except Exception:
            self.error("Wrong input for Node ID's!", "Error Node ID's")
            return

        if self.checkBox_ux.isChecked():
            self.localDof = 0
            self.localdof_label = "Ux"
            self.unit_label = "m"

        if self.checkBox_uy.isChecked():
            if self.localDof == None:
                self.localDof = 1
                self.localdof_label = "Uy"
                self.unit_label = "m"
            else:
                self.error("Multiple Selections (Max 1)")
                return
        if self.checkBox_uz.isChecked():
            if self.localDof == None:
                self.localDof = 2
                self.localdof_label = "Uz"
                self.unit_label = "m"
            else:
                self.error("Multiple Selections (Max 1)")
                return

        if self.checkBox_rx.isChecked():
            if self.localDof == None:
                self.localDof = 3
                self.localdof_label = "Rx"
                self.unit_label = "rad"
            else:
                self.error("Multiple Selections (Max 1)")
                return

        if self.checkBox_ry.isChecked():
            if self.localDof == None:
                self.localDof = 4
                self.localdof_label = "Ry"
                self.unit_label = "rad"
            else:
                self.error("Multiple Selections (Max 1)")
                return
        if self.checkBox_rz.isChecked():
            if self.localDof == None:
                self.localDof = 5
                self.localdof_label = "Rz"
                self.unit_label = "rad"
            else:
                self.error("Multiple Selections (Max 1)")
                return
          
        if self.localDof==None:
            self.error("Please, it's necessary to select one DOF to plot the frequency response.")
            return

        self.plot()

    def plot(self):

        frequencies = self.frequencies
        dof_response = get_structural_frf(self.mesh, self.solution, self.nodeID, self.localDof)
        fig = plt.figure(figsize=[10,6])
        ax = fig.add_subplot(1,1,1)

        #cursor = Cursor(ax)
        cursor = SnaptoCursor(ax, frequencies, dof_response, show_cursor=True)
        plt.connect('motion_notify_event', cursor.mouse_move)

        legend_label = "Response {} at node {}".format(self.localdof_label, self.nodeID)

        if dof_response.all()==0:
            first_plot, = plt.plot(frequencies, dof_response, color=[1,0,0], linewidth=2, label=legend_label)
        else:    
            first_plot, = plt.semilogy(frequencies, dof_response, color=[1,0,0], linewidth=2, label=legend_label)
        
        first_legend = plt.legend(handles=[first_plot], loc='upper right')
        plt.gca().add_artist(first_legend)

        ax.set_title(('Frequency Response Function: {} Method').format(self.analysisMethod), fontsize = 18, fontweight = 'bold')
        ax.set_xlabel(('Frequency [Hz]'), fontsize = 16, fontweight = 'bold')
        ax.set_ylabel(("FRF's magnitude [{}]").format(self.unit_label), fontsize = 16, fontweight = 'bold')
        
        # plt.axis([np.min(frequencies), np.max(frequencies), np.min(dof_response), np.max(dof_response)])
        plt.show()