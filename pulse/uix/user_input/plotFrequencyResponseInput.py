from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QLabel, QCheckBox, QPushButton
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from pulse.postprocessing.plot_data import get_frf
import matplotlib.pyplot as plt
import numpy as np


class SnaptoCursor(object):
    def __init__(self, ax, x, y):
        self.ax = ax
        self.ly = ax.axvline( x=np.min(x),  ymin=np.min(y), color='k', alpha=0.3)  # the vert line
        self.lx = ax.axhline(color='k', alpha=0.3)  # the vert line
        self.marker, = ax.plot(np.min(x), np.min(y), marker="o", color=[0,0,0], zorder=3) 
        self.x = x
        self.y = y
        self.txt = ax.text(np.min(x), np.min(y), '')
        self.df = (x[1]-x[0])/2
        self.dH = 0#(np.max(y) - np.min(y))/len(y)

    def mouse_move(self, event):
        if not event.inaxes: 
            return
        x, y = event.xdata, event.ydata
        if x>=np.max(self.x): 
            return
        indx = np.searchsorted(self.x, [x])[0]
        dx = self.df
        
        x = self.x[indx]
        y = self.y[indx]
        self.ly.set_xdata(x)
        self.lx.set_ydata(y)
        self.marker.set_data([x],[y])
        self.txt.set_text('x=%1.2f, y=%4.2e' % (x, y))
        self.txt.set_position((x+dx,y))
        self.ax.figure.canvas.draw_idle()


class PlotFrequencyResponseInput(QDialog):
    def __init__(self, mesh, analyseMethod, frequencies, solution, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/plotFrequencyResponseInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.mesh = mesh
        self.analyseMethod = analyseMethod
        self.frequencies = frequencies
        self.solution = solution
        self.nodeID = 0

        self.localDof = 0

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
        try:
            tokens = self.lineEdit_nodeID.text().strip().split(',')
            try:
                tokens.remove('')
            except:
                pass
            nodes = list(map(int, tokens))
            if len(nodes) == 1:
                self.nodeID = nodes[0]
            else:
                self.error("Multiple Node IDs", "Error Node ID's")
                return
        except Exception:
            self.error("Wrong input for Node ID's!", "Error Node ID's")
            return


        self.localDof = 0
        if self.checkBox_ux.isChecked():
            self.localDof = 0
            self.localdof_label = "Ux"
            self.unit_label = "m"

        if self.checkBox_uy.isChecked():
            if self.localDof != 0:
                self.error("Multiple Selections (Max 1)")
                return
            else:
                self.localDof = 1
                self.localdof_label = "Uy"
                self.unit_label = "m"
        
        if self.checkBox_uz.isChecked():
            if self.localDof != 0:
                self.error("Multiple Selections (Max 1)")
                return
            else:
                self.localDof = 2
                self.localdof_label = "Uz"
                self.unit_label = "m"

        if self.checkBox_rx.isChecked():
            if self.localDof != 0:
                self.error("Multiple Selections (Max 1)")
                return
            else:
                self.localDof = 3
                self.localdof_label = "Rx"
                self.unit_label = "rad"

        if self.checkBox_ry.isChecked():
            if self.localDof != 0:
                self.error("Multiple Selections (Max 1)")
                return
            else:
                self.localDof = 4
                self.localdof_label = "Ry"
                self.unit_label = "rad"

        if self.checkBox_rz.isChecked():
            if self.localDof != 0:
                self.error("Multiple Selections (Max 1)")
                return
            else:
                self.localDof = 5
                self.localdof_label = "Rz"
                self.unit_label = "rad"
        
        self.plot()

    def plot(self):
        frequencies = self.frequencies
        dof_response = get_frf(self.mesh, self.solution, self.nodeID, self.localDof)
       
        fig = plt.figure(figsize=[10,6])
        ax = fig.add_subplot(1,1,1)

        #cursor = Cursor(ax)
        cursor = SnaptoCursor(ax, frequencies, dof_response)
        plt.connect('motion_notify_event', cursor.mouse_move)

        if dof_response.all()==0:
            plt.plot(frequencies, dof_response, color = [1,0,0], linewidth=2)
        else:    
            plt.semilogy(frequencies, dof_response, color = [1,0,0], linewidth=2)
        
        ax.set_title(('Frequency Response Function: {} Method').format(self.analyseMethod), fontsize = 18, fontweight = 'bold')
        ax.set_xlabel(('Frequency [Hz]'), fontsize = 16, fontweight = 'bold')
        ax.set_ylabel(("FRF's magnitude [{}]").format(self.unit_label), fontsize = 16, fontweight = 'bold')
        legend_label = "Response {} at node {}".format(self.localdof_label, self.nodeID)
        ax.legend([legend_label])
        # plt.axis([np.min(frequencies), np.max(frequencies), np.min(dof_response), np.max(dof_response)])
        plt.show()