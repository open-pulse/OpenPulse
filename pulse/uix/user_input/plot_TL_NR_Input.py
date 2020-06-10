from PyQt5.QtWidgets import QLineEdit, QDialog, QFileDialog, QTreeWidget, QRadioButton, QTreeWidgetItem, QTabWidget, QLabel, QCheckBox, QPushButton, QToolButton
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
import os


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


class Plot_TL_NR_Input(QDialog):
    def __init__(self, mesh, analysisMethod, frequencies, solution, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/plot_TL_NR_Input.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.mesh = mesh
        self.userPath = os.path.expanduser('~')
        
        self.analysisMethod = analysisMethod
        self.frequencies = frequencies
        self.solution = solution
        self.nodeID = 0

        self.mag = False
        self.real = False
        self.imag = False
        self.flagTL = False
        self.flagNR = False
        self.input_node = None
        self.output_node = None
        self.elements = self.mesh.acoustic_elements
        self.dict_elements_diameter = self.mesh.neighbour_elements_diameter()
    
        self.lineEdit_inputNodeID = self.findChild(QLineEdit, 'lineEdit_inputNodeID')   
        self.lineEdit_outputNodeID = self.findChild(QLineEdit, 'lineEdit_outputNodeID')
        self.lineEdit_resultsPath = self.findChild(QLineEdit, 'lineEdit_resultsPath')

        self.toolButton_import_results = self.findChild(QToolButton, 'toolButton_Import')
        self.toolButton_import_results.clicked.connect(self.import_results)

        self.radioButton_TL = self.findChild(QRadioButton, 'radioButton_TL')
        self.radioButton_NR = self.findChild(QRadioButton, 'radioButton_NR')
        self.radioButton_TL.toggled.connect(self.radioButtonEvent_TL_NR)
        self.radioButton_NR.toggled.connect(self.radioButtonEvent_TL_NR)
        self.flagTL = self.radioButton_TL.isChecked()
        self.flagNR = self.radioButton_NR.isChecked()

        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.pushButton.clicked.connect(self.check)

        self.exec_()

    def import_results(self):
        self.path, _type = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'Dat Files (*.dat)')
        self.name = basename(self.path)
        self.lineEdit_resultsPath.setText(str(self.path))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def check_node(self, node_string):
        try:
            tokens = node_string.text().strip().split(',')
            try:
                tokens.remove('')
            except:
                pass
            node_typed = list(map(int, tokens))
            if len(node_typed) == 1:
                try:
                    self.mesh.nodes[node_typed[0]].external_index
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
        return node_typed[0]

    def radioButtonEvent_TL_NR(self):
        self.flagTL = self.radioButton_TL.isChecked()
        self.flagNR = self.radioButton_NR.isChecked()

    def check(self):
        self.input_node = self.check_node(self.lineEdit_inputNodeID)
        self.output_node = self.check_node(self.lineEdit_outputNodeID)
        print(self.input_node, self.output_node)
        self.plot()

    def dB(self, data):
        p_ref = 20e-6 
        return 20*np.log10(data/p_ref)

    def get_minor_external_diameter_from_node(self, node):
        data = self.dict_elements_diameter[node]
        internal_diameter = []
        density = []
        sound_velocity = []
        for (index, _, int_dia) in data:
            internal_diameter.append(int_dia)
            density.append(self.elements[index].fluid.density)
            sound_velocity.append(self.elements[index].sound_velocity_corrected())
        ind = internal_diameter.index(min(internal_diameter))
        return internal_diameter[ind], density[ind], sound_velocity[ind]

    def plot(self):

        frequencies = self.frequencies
        P_input = get_acoustic_frf(self.mesh, self.solution, self.input_node)
        P_output = get_acoustic_frf(self.mesh, self.solution, self.output_node)
        
        P_input2 = 0.5*np.real(P_input*np.conjugate(P_input))
        P_output2 = 0.5*np.real(P_output*np.conjugate(P_output))

        d_in, rho_in, c0_in = self.get_minor_external_diameter_from_node(self.input_node)
        d_out, rho_out, c0_out = self.get_minor_external_diameter_from_node(self.output_node)
                
        if self.flagTL:
            if P_input2.all()!=0:
                alpha_T = (P_output2*rho_out*c0_out)/(P_input2*rho_in*c0_in)
                TL = -10*np.log10(alpha_T)
                results = TL
                analysis_label = "TRANSMISSION LOSS"
            else:
                message = "The input pressure must be different from zero value!"
                error(message, title=" Input pressure value Error ")
        else:
            if P_input2.all()!=0:
                delta =  (P_output2*rho_out*c0_out*(d_out**2))/(P_input2*rho_in*c0_in*(d_in**2))
                NR = 10*np.log10(delta)
                results = NR
                analysis_label = "SOUND ATTENUATION"
            else:
                message = "The input pressure must be different from zero value!"
                error(message, title=" Input pressure value Error ")               

        fig = plt.figure(figsize=[12,8])
        ax = fig.add_subplot(1,1,1)
        # mng = plt.get_current_fig_manager()
        # mng.window.state('zoomed')

        #cursor = Cursor(ax)
        cursor = SnaptoCursor(ax, frequencies, results, show_cursor=True)
        plt.connect('motion_notify_event', cursor.mouse_move)

        legend_label = "Acoustic Pressure at node {}".format(self.nodeID)

        if results.all()==0:
            first_plot, = plt.plot(frequencies, results, color=[1,0,0], linewidth=2, label=legend_label)
        else:    
            first_plot, = plt.plot(frequencies, results, color=[1,0,0], linewidth=2, label=legend_label)
        
        first_legend = plt.legend(handles=[first_plot], loc='upper right')
        plt.gca().add_artist(first_legend)
        unit_label = "dB"
        ax.set_title(('SPECTRUM OF THE {}').format(analysis_label), fontsize = 18, fontweight = 'bold')
        ax.set_xlabel(('Frequency [Hz]'), fontsize = 14, fontweight = 'bold')
        if self.flagTL:
            ax.set_ylabel(("Transmission Loss [{}]").format(unit_label), fontsize = 14, fontweight = 'bold')
        elif self.flagNR:
            ax.set_ylabel(("Attenuation [{}]").format(unit_label), fontsize = 14, fontweight = 'bold')
        plt.show()