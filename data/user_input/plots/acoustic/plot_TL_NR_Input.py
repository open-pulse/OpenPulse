from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np
import matplotlib.pyplot as plt

from pulse.tools.advanced_cursor import AdvancedCursor
from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf
from data.user_input.project.printMessageInput import PrintMessageInput

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"


class Plot_TL_NR_Input(QDialog):
    def __init__(self, project, opv, analysisMethod, solution, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui_files/plots_/results_/acoustic_/plot_TL_NR_Input.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)

        self.projec = project
        self.preprocessor = project.preprocessor
        self.before_run = project.get_pre_solution_model_checks()

        self.elements = self.preprocessor.acoustic_elements
        self.dict_elements_diameter = self.preprocessor.neighbor_elements_diameter()
        self.nodes = project.preprocessor.nodes
        
        self.userPath = os.path.expanduser('~')
        self.path = ""
        self.save_path = ""
        
        self.analysisMethod = analysisMethod
        self.frequencies = project.frequencies
        self.solution = solution

        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.writeNodes(self.opv.getListPickedPoints())
        self.exec()
    

    def _reset_variables(self):
        self.mag = False
        self.real = False
        self.imag = False
        self.flagTL = False
        self.flagNR = False
        self.input_node_ID = None
        self.output_node_ID = None
        self.imported_data = None


    def _define_qt_variables(self):
        # QCheckBox
        self.checkBox_legends = self.findChild(QCheckBox, 'checkBox_legends')
        # QLineEdit
        self.lineEdit_inputNodeID = self.findChild(QLineEdit, 'lineEdit_inputNodeID')   
        self.lineEdit_outputNodeID = self.findChild(QLineEdit, 'lineEdit_outputNodeID')
        self.lineEdit_FileName = self.findChild(QLineEdit, 'lineEdit_FileName')
        self.lineEdit_ImportResultsPath = self.findChild(QLineEdit, 'lineEdit_ImportResultsPath')
        self.lineEdit_SaveResultsPath = self.findChild(QLineEdit, 'lineEdit_SaveResultsPath')
        # QPushButton
        self.pushButton_ChooseFolderImport = self.findChild(QPushButton, 'pushButton_ChooseFolderImport')
        self.pushButton_ChooseFolderExport = self.findChild(QPushButton, 'pushButton_ChooseFolderExport')
        self.pushButton_ExportResults = self.findChild(QPushButton, 'pushButton_ExportResults')
        self.pushButton_ResetPlot = self.findChild(QPushButton, 'pushButton_ResetPlot')
        self.pushButton_AddImportedPlot = self.findChild(QPushButton, 'pushButton_AddImportedPlot')
        self.pushButton_plot = self.findChild(QPushButton, 'pushButton_plot')
        self.pushButton_flipNodes = self.findChild(QPushButton, 'pushButton_flipNodes')
        # QRadioButton
        self.radioButton_TL = self.findChild(QRadioButton, 'radioButton_TL')
        self.radioButton_NR = self.findChild(QRadioButton, 'radioButton_NR')
        self.radioButton_disable_cursors = self.findChild(QRadioButton, 'radioButton_disable_cursors')
        self.radioButton_cross_cursor = self.findChild(QRadioButton, 'radioButton_cross_cursor')
        self.radioButton_harmonic_cursor = self.findChild(QRadioButton, 'radioButton_harmonic_cursor')
        self.flagTL = self.radioButton_TL.isChecked()
        self.flagNR = self.radioButton_NR.isChecked()
        # QSpinBox
        self.spinBox_skiprows = self.findChild(QSpinBox, 'spinBox')
        # QTabWidget
        self.tabWidget_plot_results = self.findChild(QTabWidget, "tabWidget_plot_results")
        # QWidget
        self.tab_plot = self.tabWidget_plot_results.findChild(QWidget, "tab_plot")


    def _create_connections(self):
        #
        self.radioButton_TL.toggled.connect(self.radioButtonEvent_TL_NR)
        self.radioButton_NR.toggled.connect(self.radioButtonEvent_TL_NR)
        self.radioButton_disable_cursors.clicked.connect(self.update_cursor_controls)
        self.radioButton_cross_cursor.clicked.connect(self.update_cursor_controls)
        self.radioButton_harmonic_cursor.clicked.connect(self.update_cursor_controls)
        self.update_cursor_controls()
        #
        self.pushButton_AddImportedPlot.clicked.connect(self.ImportResults)
        self.pushButton_plot.clicked.connect(self.check)
        self.pushButton_flipNodes.clicked.connect(self.flip_nodes)
        self.pushButton_ResetPlot.clicked.connect(self.reset_imported_data)
        self.pushButton_ExportResults.clicked.connect(self.ExportResults)
        self.pushButton_ChooseFolderExport.clicked.connect(self.choose_path_export_results)
        self.pushButton_ChooseFolderImport.clicked.connect(self.choose_path_import_results)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()


    def writeNodes(self, list_node_ids):
        if len(list_node_ids) == 2:
            self.lineEdit_inputNodeID.setText(str(list_node_ids[-2]))
            self.lineEdit_outputNodeID.setText(str(list_node_ids[-1]))
        elif len(list_node_ids) == 1:
            self.lineEdit_inputNodeID.setText(str(list_node_ids[-1]))
            self.lineEdit_outputNodeID.setText("")


    def flip_nodes(self):
        temp_text_input = self.lineEdit_inputNodeID.text()
        temp_text_output = self.lineEdit_outputNodeID.text()
        self.lineEdit_inputNodeID.setText(temp_text_output)
        self.lineEdit_outputNodeID.setText(temp_text_input)   


    def update(self):
        self.writeNodes(self.opv.getListPickedPoints())


    def check_node(self, node_string):
        try:
            tokens = node_string.text().strip().split(',')
            try:
                tokens.remove('')
            except:
                pass
            node_typed = list(map(int, tokens))

        except Exception:
            title = "INVALID NODE ID"
            message = "Wrong input for Node ID."
            PrintMessageInput([title, message, window_title1])
            return None, False

        if len(node_typed) == 1:
            try:
                self.preprocessor.nodes[node_typed[0]].external_index
            except:
                title = "INVALID NODE ID"
                message = " The Node ID input values must be\n greater than 1 and less than {}.".format(len(self.nodes))
                PrintMessageInput([title, message, window_title1])
                return None, False

        elif len(node_typed) == 0:
            title = "INVALID NODE ID"
            message = "Please, enter a valid Node ID."
            PrintMessageInput([title, message, window_title1])
            return None, False

        else:
            title = "MULTIPLE NODE IDs"
            message = "Please, type or select only one Node ID."
            PrintMessageInput([title, message, window_title1])
            return None, False

        return node_typed[0], True


    def reset_imported_data(self):
        self.imported_data = None
        title = "Information"
        message = "The plot data has been reseted."
        PrintMessageInput([title, message, window_title2])


    def radioButtonEvent_TL_NR(self):
        self.flagTL = self.radioButton_TL.isChecked()
        self.flagNR = self.radioButton_NR.isChecked()


    def update_cursor_controls(self):
        if self.radioButton_disable_cursors.isChecked():
            self.checkBox_legends.setChecked(False)
            self.checkBox_legends.setDisabled(True)
        else:
            self.checkBox_legends.setDisabled(False)


    def check(self, export=False):

        lineEdit_input = self.lineEdit_inputNodeID.text()
        stop, self.input_node_ID = self.before_run.check_input_NodeID(lineEdit_input, single_ID=True)
        if stop:
            return True

        lineEdit_output = self.lineEdit_outputNodeID.text()
        stop, self.output_node_ID = self.before_run.check_input_NodeID(lineEdit_output, single_ID=True)
        if stop:
            return True

        if export:
            return
        else:
            self.plot()


    def choose_path_import_results(self):
        self.import_path, _ = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'Files (*.csv; *.dat; *.txt)')
        self.import_name = os.basename(self.import_path)
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
                self.legend_imported = "imported data: "+ os.basename(self.import_path).split(".")[0]
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
        self.save_name = os.basename(self.save_path)
        self.lineEdit_SaveResultsPath.setText(str(self.save_path))


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
        data = self.get_TL_NR()

        if self.stop:
            return

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
                title = "File name recheck"
                message = "Please, it's recommended to check the file name before export the results!"
                PrintMessageInput([title, message, window_title2])
                return            
            header = "Frequency[Hz], TL - Magnitude [dB]"    
        else:
            if True in check_name_NR:
                title = "File name recheck"
                message = "Please, it's recommended to check the file name before export the results!"
                PrintMessageInput([title, message, window_title2])
                return
            header = "Frequency[Hz], NR - Magnitude [dB]"

        self.export_path = self.export_path_folder + self.lineEdit_FileName.text() + ".dat"
        data_to_export = np.array([freq, data]).T    
        np.savetxt(self.export_path, data_to_export, delimiter=",", header=header)
            
        title = "Information"
        message = "The results have been exported."
        PrintMessageInput([title, message, window_title2])

    def get_minor_outer_diameter_from_node(self, node):
        data = self.dict_elements_diameter[node]
        inner_diameter = []
        density = []
        speed_of_sound = []
        for (index, _, int_dia) in data:
            inner_diameter.append(int_dia)
            density.append(self.elements[index].fluid.density)
            speed_of_sound.append(self.elements[index].speed_of_sound_corrected())
        ind = inner_diameter.index(min(inner_diameter))
        return inner_diameter[ind], density[ind], speed_of_sound[ind]

    def get_TL_NR(self):
        
        self.stop = False

        noise = 1e-10

        P_input = get_acoustic_frf(self.preprocessor, self.solution, self.input_node_ID)
        P_output = get_acoustic_frf(self.preprocessor, self.solution, self.output_node_ID)
        
        P_input2 = 0.5*np.real(P_input*np.conjugate(P_input)) + noise
        P_output2 = 0.5*np.real(P_output*np.conjugate(P_output)) + noise

        d_in, rho_in, c0_in = self.get_minor_outer_diameter_from_node(self.input_node_ID)
        d_out, rho_out, c0_out = self.get_minor_outer_diameter_from_node(self.output_node_ID)
               
        # if 0 not in P_input2 and 0 not in P_output2:
        
        if self.flagTL:
            alpha_T = (P_output2*rho_out*c0_out)/(P_input2*rho_in*c0_in)
            TL = -10*np.log10(alpha_T)
            return TL
            
        if self.flagNR:
            delta =  (P_output2*rho_out*c0_out*(d_out**2))/(P_input2*rho_in*c0_in*(d_in**2))
            NR = 10*np.log10(delta)
            return NR

        # else:
        #     self.stop = True
        #     return None

    def plot(self):
        """
        """
        plt.ion()
        plt.close()
        self.fig = plt.figure(figsize=[12,7])
        ax = self.fig.add_subplot(1,1,1)

        frequencies = self.frequencies
        results = self.get_TL_NR()
        
        # if self.stop:
        #     title = "Invalid pressure values"
        #     message = "The input pressure must be different from zero value!"
        #     PrintMessageInput([title, message, window_title1])
        #     return

        if self.flagTL:
            analysis_label = "TRANSMISSION LOSS"
        else:
            analysis_label = "ATTENUATION"
         
        # mng = plt.get_current_fig_manager()
        # mng.window.state('zoomed')

        unit_label = "dB"
        legend_label = "Input Node ID: {} || Output Node ID: {}".format(self.input_node_ID, self.output_node_ID)

        if self.imported_data is None:
            first_plot, = plt.plot(frequencies, results, color=[1,0,0], linewidth=2, label=legend_label)
            _legends = plt.legend(handles=[first_plot], labels=[legend_label])#, loc='upper right')
        else:    
            first_plot, = plt.plot(frequencies, results, color=[1,0,0], linewidth=2)
            second_plot, = plt.plot(self.imported_data[:,0], self.imported_data[:,1], color=[0,0,1], linewidth=2, linestyle="--")
            _legends = plt.legend(handles=[first_plot, second_plot], labels=[legend_label, self.legend_imported])#, loc='upper right')
        
        plt.gca().add_artist(_legends)

        ax.set_title(('FREQUENCY PLOT OF {}').format(analysis_label.upper()), fontsize = 18, fontweight = 'bold')
        ax.set_xlabel(('Frequency [Hz]'), fontsize = 14, fontweight = 'bold')
        if self.flagTL:
            ax.set_ylabel(("Transmission Loss [{}]").format(unit_label), fontsize = 14, fontweight = 'bold')
        elif self.flagNR:
            ax.set_ylabel(("Attenuation [{}]").format(unit_label), fontsize = 14, fontweight = 'bold')

        if not self.radioButton_disable_cursors.isChecked():
            show_legend = self.checkBox_legends.isChecked()
            if self.radioButton_harmonic_cursor.isChecked():
                self.cursor = AdvancedCursor(ax, frequencies, results, False, number_vertLines=12, show_legend=show_legend)
            else:
                self.cursor = AdvancedCursor(ax, frequencies, results, False, number_vertLines=1 , show_legend=show_legend)

            self.mouse_connection = self.fig.canvas.mpl_connect(s='motion_notify_event', func=self.cursor.mouse_move)

        self.fig.show()