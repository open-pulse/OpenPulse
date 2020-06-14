from PyQt5.QtWidgets import QMessageBox, QLineEdit, QDialog, QFileDialog, QWidget, QTreeWidget, QRadioButton, QTreeWidgetItem, QTabWidget, QLabel, QCheckBox, QPushButton, QToolButton
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
        self.path = ""
        
        self.analysisMethod = analysisMethod
        self.frequencies = frequencies
        self.solution = solution

        self.mag = False
        self.real = False
        self.imag = False
        self.flagTL = False
        self.flagNR = False
        self.input_node = None
        self.output_node = None
        self.imported_data = None
        self.elements = self.mesh.acoustic_elements
        self.dict_elements_diameter = self.mesh.neighbour_elements_diameter()
    
        self.lineEdit_inputNodeID = self.findChild(QLineEdit, 'lineEdit_inputNodeID')   
        self.lineEdit_outputNodeID = self.findChild(QLineEdit, 'lineEdit_outputNodeID')
        self.lineEdit_FileName = self.findChild(QLineEdit, 'lineEdit_FileName')
        self.lineEdit_ImportResultsPath = self.findChild(QLineEdit, 'lineEdit_ImportResultsPath')
        self.lineEdit_SaveResultsPath = self.findChild(QLineEdit, 'lineEdit_SaveResultsPath')

        self.toolButton_ChooseFolderImport = self.findChild(QToolButton, 'toolButton_ChooseFolderImport')
        self.toolButton_ChooseFolderImport.clicked.connect(self.choose_path_import_results)
        self.toolButton_ChooseFolderExport = self.findChild(QToolButton, 'toolButton_ChooseFolderExport')
        self.toolButton_ChooseFolderExport.clicked.connect(self.choose_path_export_results)
        self.toolButton_ExportResults = self.findChild(QToolButton, 'toolButton_ExportResults')
        self.toolButton_ExportResults.clicked.connect(self.ExportResults)
        self.toolButton_ResetPlot = self.findChild(QToolButton, 'toolButton_ResetPlot')
        self.toolButton_ResetPlot.clicked.connect(self.reset_imported_data)

        self.tabWidget_plot_results = self.findChild(QTabWidget, "tabWidget_plot_results")
        self.tab_plot = self.tabWidget_plot_results.findChild(QWidget, "tab_plot")

        self.radioButton_TL = self.findChild(QRadioButton, 'radioButton_TL')
        self.radioButton_NR = self.findChild(QRadioButton, 'radioButton_NR')
        self.radioButton_TL.toggled.connect(self.radioButtonEvent_TL_NR)
        self.radioButton_NR.toggled.connect(self.radioButtonEvent_TL_NR)
        self.flagTL = self.radioButton_TL.isChecked()
        self.flagNR = self.radioButton_NR.isChecked()

        self.pushButton_AddImportedPlot = self.findChild(QPushButton, 'pushButton_AddImportedPlot')
        self.pushButton_AddImportedPlot.clicked.connect(self.ImportResults)

        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.pushButton.clicked.connect(self.check)

        self.exec_()

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
        
        return node_typed[0], True
    
    def messages(self, msg, title = " Information "):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(msg)
        msg_box.setWindowTitle(title)
        msg_box.exec_()

    def reset_imported_data(self):
        self.imported_data = None
        self.messages("The plot data has been reseted.")

    def radioButtonEvent_TL_NR(self):
        self.flagTL = self.radioButton_TL.isChecked()
        self.flagNR = self.radioButton_NR.isChecked()

    def check(self, export=False):
        self.input_node, input_ok = self.check_node(self.lineEdit_inputNodeID)
        self.output_node, output_ok = self.check_node(self.lineEdit_outputNodeID)
        if input_ok and output_ok and not export:
            self.plot()
        else:
            return

    def choose_path_import_results(self):
        self.import_path, _ = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'Dat Files (*.dat)')
        self.import_name = basename(self.import_path)
        self.lineEdit_ImportResultsPath.setText(str(self.import_path))
    
    def ImportResults(self):
        self.imported_data = np.loadtxt(self.import_path, delimiter=",")
        self.legend_imported = "imported data: "+ basename(self.import_path).split(".")[0]
        self.tabWidget_plot_results.setCurrentWidget(self.tab_plot)
        self.messages("The results has been imported.")

    def choose_path_export_results(self):
        self.save_path = QFileDialog.getExistingDirectory(None, 'Choose a folder to export the results', self.userPath)
        self.save_name = basename(self.save_path)
        self.lineEdit_SaveResultsPath.setText(str(self.save_path))
        if self.lineEdit_FileName.text() != "":
            self.export_path_folder = self.save_path + "/" 
        else:
            error("Inform a file name before trying export the results!")
            return
    
    def ExportResults(self):
        self.check(export=True)
        TL, NR = self.get_TL_NR()
        freq = self.frequencies

        check_name_TL = []
        check_name_NR = []
        for a in ["NR", "Nr", "nr", "attenuation", "Attenuation", "ATTENUATION"]:
            if a in self.lineEdit_FileName.text():
                check_name_TL.append(True)
            else:
                check_name_TL.append(False)

        for a in ["TL", "Tl","tl", "tranmission", "loss", "Transmission", "Loss", "TRANSMISSION", "LOSS"]:
            if a in self.lineEdit_FileName.text():
                check_name_NR.append(True)
            else:
                check_name_NR.append(False)

        if self.flagTL:
            if True in check_name_TL:
                self.messages("Please, it's recommended to check the file name before export the results!", title=" Warning ")
                return
            self.export_path = self.export_path_folder + self.lineEdit_FileName.text() + ".dat"
            data_to_export = np.array([freq, TL]).T
            header = "Frequency[Hz], TL - Magnitude [dB]"
            np.savetxt(self.export_path, data_to_export, delimiter=",", header=header)
        else:
            if True in check_name_NR:
                self.messages("Please, it's recommended to check the file name before export the results!", title=" Warning ")
                return
            self.export_path = self.export_path_folder + self.lineEdit_FileName.text() + ".dat"
            data_to_export = np.array([freq, NR]).T
            header = "Frequency[Hz], NR - Magnitude [dB]"
            np.savetxt(self.export_path, data_to_export, delimiter=",", header=header)
        self.messages("The results has been exported.")

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

    def get_TL_NR(self):
        P_input = get_acoustic_frf(self.mesh, self.solution, self.input_node)
        P_output = get_acoustic_frf(self.mesh, self.solution, self.output_node)
        
        P_input2 = 0.5*np.real(P_input*np.conjugate(P_input))
        P_output2 = 0.5*np.real(P_output*np.conjugate(P_output))

        d_in, rho_in, c0_in = self.get_minor_external_diameter_from_node(self.input_node)
        d_out, rho_out, c0_out = self.get_minor_external_diameter_from_node(self.output_node)

        if P_input2.all()!=0:
            alpha_T = (P_output2*rho_out*c0_out)/(P_input2*rho_in*c0_in)
            TL = -10*np.log10(alpha_T)
            delta =  (P_output2*rho_out*c0_out*(d_out**2))/(P_input2*rho_in*c0_in*(d_in**2))
            NR = 10*np.log10(delta)
        else:
            message = "The input pressure must be different from zero value!"
            error(message, title=" Input pressure value Error ")
        return TL, NR

    def plot(self):

        fig = plt.figure(figsize=[12,7])
        ax = fig.add_subplot(1,1,1)

        frequencies = self.frequencies
        TL, NR = self.get_TL_NR()

        if self.flagTL:
            results = TL
            analysis_label = "TRANSMISSION LOSS"
        else:
            results = NR
            analysis_label = "ATTENUATION"
         
        # mng = plt.get_current_fig_manager()
        # mng.window.state('zoomed')

        #cursor = Cursor(ax)
        cursor = SnaptoCursor(ax, frequencies, results, show_cursor=True)
        plt.connect('motion_notify_event', cursor.mouse_move)
        unit_label = "dB"
        legend_label = "Input Node ID: {} || Output Node ID: {}".format(self.input_node, self.output_node)

        if self.imported_data is None:
            first_plot, = plt.plot(frequencies, results, color=[1,0,0], linewidth=2, label=legend_label)
            _legends = plt.legend(handles=[first_plot], labels=[legend_label], loc='upper right')
        else:    
            first_plot, = plt.plot(frequencies, results, color=[1,0,0], linewidth=2)
            second_plot, = plt.plot(self.imported_data[:,0], self.imported_data[:,1], color=[0,0,1], linewidth=2, linestyle="--")
            _legends = plt.legend(handles=[first_plot, second_plot], labels=[legend_label, self.legend_imported], loc='upper right')
        
        plt.gca().add_artist(_legends)

        ax.set_title(('SPECTRUM OF THE {}').format(analysis_label), fontsize = 18, fontweight = 'bold')
        ax.set_xlabel(('Frequency [Hz]'), fontsize = 14, fontweight = 'bold')
        if self.flagTL:
            ax.set_ylabel(("Transmission Loss [{}]").format(unit_label), fontsize = 14, fontweight = 'bold')
        elif self.flagNR:
            ax.set_ylabel(("Attenuation [{}]").format(unit_label), fontsize = 14, fontweight = 'bold')
        plt.show()