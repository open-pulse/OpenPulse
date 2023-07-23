from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np
import matplotlib.pyplot as plt
from os.path import basename

from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf
from data.user_input.project.printMessageInput import PrintMessageInput

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"

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
    def __init__(self, project, opv, analysisMethod, solution, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui/plots_/results_/acoustic_/plotAcousticFrequencyResponseInput.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon) 
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)
        self.list_node_IDs = self.opv.getListPickedPoints()

        self.projec = project
        self.preprocessor = project.preprocessor
        self.before_run = project.get_pre_solution_model_checks()

        self.nodes = self.preprocessor.nodes
        self.analysisMethod = analysisMethod
        self.frequencies = project.frequencies
        self.solution = solution

        self.userPath = os.path.expanduser('~')
        self.save_path = ""
        self.node_ID = 0
        self.imported_data = None

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')
        self.radioButton_plotAbs = self.findChild(QRadioButton, 'radioButton_plotAbs')
        self.radioButton_plotReal = self.findChild(QRadioButton, 'radioButton_plotReal')
        self.radioButton_plotImag = self.findChild(QRadioButton, 'radioButton_plotImag')
        self.radioButton_plotAbs.clicked.connect(self.radioButtonEvent_YAxis)
        self.radioButton_plotReal.clicked.connect(self.radioButtonEvent_YAxis)
        self.radioButton_plotImag.clicked.connect(self.radioButtonEvent_YAxis)
        self.plotAbs = self.radioButton_plotAbs.isChecked()
        self.plotReal = self.radioButton_plotReal.isChecked()
        self.plotImag = self.radioButton_plotImag.isChecked()

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
        self.spinBox_skiprows = self.findChild(QSpinBox, 'spinBox')

        self.checkBox_cursor = self.findChild(QCheckBox, 'checkBox_cursor')
        self.use_cursor = self.checkBox_cursor.isChecked()
        self.checkBox_cursor.clicked.connect(self.update_cursor)

        self.radioButton_Absolute = self.findChild(QRadioButton, 'radioButton_Absolute')
        self.radioButton_Real_Imaginary = self.findChild(QRadioButton, 'radioButton_Real_Imaginary')
        self.radioButton_Absolute.clicked.connect(self.radioButtonEvent_save_data)
        self.radioButton_Real_Imaginary.clicked.connect(self.radioButtonEvent_save_data)
        self.save_Absolute = self.radioButton_Absolute.isChecked()
        self.save_Real_Imaginary = self.radioButton_Real_Imaginary.isChecked()

        self.tabWidget_plot_results = self.findChild(QTabWidget, "tabWidget_plot_results")
        self.tab_plot = self.tabWidget_plot_results.findChild(QWidget, "tab_plot")
        self.pushButton_AddImportedPlot = self.findChild(QPushButton, 'pushButton_AddImportedPlot')
        self.pushButton_AddImportedPlot.clicked.connect(self.ImportResults) 

        self.checkBox_dB = self.findChild(QCheckBox, 'checkBox_dB')
        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.pushButton.clicked.connect(self.check)

        self.writeNodes(self.list_node_IDs)
        self.exec()

    def update_cursor(self):
        self.use_cursor = self.checkBox_cursor.isChecked()

    def reset_imported_data(self):
        self.imported_data = None
        title = "Information"
        message = "The plot data has been reseted."
        PrintMessageInput([title, message, window_title2])
    
    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        self.lineEdit_nodeID.setText(text)

    def update(self):
        self.list_node_IDs = self.opv.getListPickedPoints()
        if self.list_node_IDs != []:
            self.writeNodes(self.list_node_IDs)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def radioButtonEvent_YAxis(self):
        self.plotAbs = self.radioButton_plotAbs.isChecked()
        self.plotReal = self.radioButton_plotReal.isChecked()
        self.plotImag = self.radioButton_plotImag.isChecked()

    def radioButtonEvent_save_data(self):
        self.save_Absolute = self.radioButton_Absolute.isChecked()
        self.save_Real_Imaginary = self.radioButton_Real_Imaginary.isChecked()

    def choose_path_import_results(self):
        self.import_path, _ = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'Files (*.csv; *.dat; *.txt)')
        self.import_name = basename(self.import_path)
        self.lineEdit_ImportResultsPath.setText(str(self.import_path))
    
    def ImportResults(self):
        try:
            message = ""
            run = True
            skiprows = int(self.spinBox_skiprows.text())
            maximum_lines_to_skip = 100
 
            while run:
                try:
                    self.imported_data = np.loadtxt(self.import_path, delimiter=",", skiprows=skiprows)
                    self.spinBox_skiprows.setValue(int(skiprows))
                    run = False
                except:
                    skiprows += 1
                    if skiprows>=maximum_lines_to_skip:
                        run = False
                        title = "Error while loading data from file"
                        message = "The maximum number of rows to skip has been reached and no valid data has "
                        message += "been found. Please, verify the data in the imported file to proceed."
                        message += "Maximum number of header rows: 100"

            if skiprows<maximum_lines_to_skip:
                self.legend_imported = "imported data: "+ basename(self.import_path).split(".")[0]
                self.tabWidget_plot_results.setCurrentWidget(self.tab_plot)
                title = "Information"
                message = "The results have been imported."
                PrintMessageInput([title, message, window_title2])
                return

        except Exception as log_error:
            title = "Error while loading data from file"
            message = str(log_error)
            return
        
        if message != "":
            PrintMessageInput([title, message, window_title1])

    def choose_path_export_results(self):
        self.save_path = QFileDialog.getExistingDirectory(None, 'Choose a folder to export the results', self.userPath)
        self.save_name = basename(self.save_path)
        self.lineEdit_SaveResultsPath.setText(str(self.save_path))

    def check(self, export=False):

        lineEdit_nodeID = self.lineEdit_nodeID.text()
        stop, self.node_ID = self.before_run.check_input_NodeID(lineEdit_nodeID, single_ID=True)
        if stop:
            return True
                
        if self.checkBox_dB.isChecked():
            self.scale_dB = True
        elif not self.checkBox_dB.isChecked():
            self.scale_dB = False
        
        if not export:
            self.plot()

    def ExportResults(self):

        if self.lineEdit_FileName.text() != "":
            if self.save_path != "":
                self.export_path_folder = self.save_path + "/"
            else:
                title = "None folder selected"
                message = "Plese, choose a folder before trying export the results."
                PrintMessageInput([title, message, window_title1])
                return
        else:
            title = "Empty file name"
            message = "Inform a file name before trying export the results."
            PrintMessageInput([title, message, window_title1])
            return

        if self.check(export=True):
            return

        freq = self.frequencies
        self.export_path = self.export_path_folder + self.lineEdit_FileName.text() + ".dat"
        if self.save_Absolute:
            response = get_acoustic_frf(self.preprocessor, self.solution, self.node_ID)
            header = "Frequency[Hz], Real part [Pa], Imaginary part [Pa], Absolute [Pa]"
            data_to_export = np.array([freq, np.real(response), np.imag(response), np.abs(response)]).T
        elif self.save_Real_Imaginary:
            response = get_acoustic_frf(self.preprocessor, self.solution, self.node_ID)
            header = "Frequency[Hz], Real part [Pa], Imaginary part [Pa]"
            data_to_export = np.array([freq, np.real(response), np.imag(response)]).T        
            
        np.savetxt(self.export_path, data_to_export, delimiter=",", header=header)
        title = "Information"
        message = "The results have been exported."
        PrintMessageInput([title, message, window_title2])

    def dB(self, data):
        p_ref = 20e-6 
        return 20*np.log10(data/p_ref)

    def plot(self):

        self.fig = plt.figure(figsize=[12,7])
        ax = self.fig.add_subplot(1,1,1)  

        frequencies = self.frequencies
        response = get_acoustic_frf(self.preprocessor, self.solution, self.node_ID, absolute=self.plotAbs, real=self.plotReal, imag=self.plotImag)

        if complex(0) in response:
            response += np.ones(len(response), dtype=float)*(1e-12)

        if self.scale_dB :
            if self.plotAbs:
                response = self.dB(response)
                ax.set_ylabel("Acoustic Response - Absolute [dB]", fontsize = 14, fontweight = 'bold')
            else:
                if self.plotReal:
                    ax.set_ylabel("Acoustic Response - Real [Pa]", fontsize = 14, fontweight = 'bold')
                elif self.plotImag:
                    ax.set_ylabel("Acoustic Response - Imaginary [Pa]", fontsize = 14, fontweight = 'bold')
                title = "Plot Information"
                message = "The dB scalling can only be applied with the absolute \nY-axis representation, therefore, it will be ignored."
                PrintMessageInput([title, message, window_title2])
        else:
            if self.plotAbs:
                ax.set_ylabel("Acoustic Response - Absolute [Pa]", fontsize = 14, fontweight = 'bold')
            elif self.plotReal:
                ax.set_ylabel("Acoustic Response - Real [Pa]", fontsize = 14, fontweight = 'bold')
            elif self.plotImag:
                ax.set_ylabel("Acoustic Response - Imaginary [Pa]", fontsize = 14, fontweight = 'bold')

        # mng = plt.get_current_fig_manager()
        # mng.window.state('zoomed')

        #cursor = Cursor(ax)
        self.cursor = SnaptoCursor(ax, frequencies, response, self.use_cursor)
        self.mouse_connection = self.fig.canvas.mpl_connect(s='motion_notify_event', func=self.cursor.mouse_move)

        legend_label = "Acoustic Pressure at node {}".format(self.node_ID)
        
        if self.imported_data is None:

            response += np.ones(len(response), dtype=float)*(1e-12)

            if self.plotAbs and not self.scale_dB and not complex(0) in response:
                first_plot, = plt.semilogy(frequencies, response, color=[1,0,0], linewidth=2, label=legend_label)
            else:
                first_plot, = plt.plot(frequencies, response, color=[1,0,0], linewidth=2, label=legend_label)
            _legends = plt.legend(handles=[first_plot], labels=[legend_label])#, loc='upper right')

        else:

            data = self.imported_data
            imported_Xvalues = data[:,0]
            
            if self.plotAbs:
                imported_Yvalues = np.abs(data[:,1] + 1j*data[:,2])
                if complex(0) in imported_Yvalues:
                    imported_Yvalues += np.ones(len(imported_Yvalues), dtype=float)*(1e-12)

                if self.scale_dB :
                    imported_Yvalues = self.dB(imported_Yvalues)
            elif self.plotReal:
                imported_Yvalues = data[:,1]
            elif self.plotImag:
                imported_Yvalues = data[:,2]

            if self.plotAbs and not self.scale_dB and not complex(0) in response:
                first_plot, = plt.semilogy(frequencies, response, color=[1,0,0], linewidth=2)
                second_plot, = plt.semilogy(imported_Xvalues, imported_Yvalues, color=[0,0,1], linewidth=1, linestyle="--")            
            else:
                first_plot, = plt.plot(frequencies, response, color=[1,0,0], linewidth=2)
                second_plot, = plt.plot(imported_Xvalues, imported_Yvalues, color=[0,0,1], linewidth=1, linestyle="--")

            _legends = plt.legend(handles=[first_plot, second_plot], labels=[legend_label, self.legend_imported])#, loc='upper right')

        plt.gca().add_artist(_legends)

        ax.set_title(('ACOUSTIC FREQUENCY RESPONSE - {}').format(self.analysisMethod.upper()), fontsize = 16, fontweight = 'bold')
        ax.set_xlabel(('Frequency [Hz]'), fontsize = 14, fontweight = 'bold')

        self.fig.show()