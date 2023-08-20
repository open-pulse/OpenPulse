from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from pathlib import Path
import configparser
import os
from os.path import basename
import matplotlib.pyplot as plt
import numpy as np

from pulse.tools.advanced_cursor import AdvancedCursor
from pulse.postprocessing.plot_structural_data import get_stress_spectrum_data
from data.user_input.project.printMessageInput import PrintMessageInput


error_title = "ERROR"
warning_title = "WARNING"

class PlotStressFrequencyResponseInput(QDialog):
    def __init__(self, project, opv, analysisMethod, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui/plots_/results_/structural_/plot_stress_frequency_response_input.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.userPath = os.path.expanduser('~')
        self.save_path = ""

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)

        self.project = project
        self.preprocessor = project.preprocessor
        self.before_run = project.get_pre_solution_model_checks()
        self.frequencies = project.frequencies
        self.solve = self.project.structural_solve 
        self.analysisMethod = analysisMethod

        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.writeElements(self.opv.getListPickedElements())
        self.exec()


    def _reset_variables(self):
        self.elementID = None
        self.imported_data = None
        self.keys = np.arange(7)
        self.labels = np.array(["Normal axial", 
                                "Normal bending y", 
                                "Normal bending z", 
                                "Hoop", 
                                "Torsional shear", 
                                "Transversal shear xy", 
                                "Transversal shear xz"])
        self.stress_data = []
        self.unit_label = "Pa"


    def _define_qt_variables(self):
        # QCheckBox
        self.checkBox_damping_effect = self.findChild(QCheckBox, 'checkBox_damping_effect')
        self.checkBox_legends = self.findChild(QCheckBox, 'checkBox_legends')
        self.flag_damping_effect = self.checkBox_damping_effect.isChecked()
        # QLineEdit
        self.lineEdit_elementID = self.findChild(QLineEdit, 'lineEdit_elementID')
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
        # QRadioButton
        self.radioButton_normal_axial = self.findChild(QRadioButton, 'radioButton_normal_axial')
        self.radioButton_normal_bending_y = self.findChild(QRadioButton, 'radioButton_normal_bending_y')
        self.radioButton_normal_bending_z = self.findChild(QRadioButton, 'radioButton_normal_bending_z')
        self.radioButton_hoop = self.findChild(QRadioButton, 'radioButton_hoop')
        self.radioButton_transv_shear_xy = self.findChild(QRadioButton, 'radioButton_transv_shear_xy')
        self.radioButton_transv_shear_xz = self.findChild(QRadioButton, 'radioButton_transv_shear_xz')
        self.radioButton_torsional_shear = self.findChild(QRadioButton, 'radioButton_torsional_shear')
        self.radioButton_plotAbs = self.findChild(QRadioButton, 'radioButton_plotAbs')
        self.radioButton_plotReal = self.findChild(QRadioButton, 'radioButton_plotReal')
        self.radioButton_plotImag = self.findChild(QRadioButton, 'radioButton_plotImag')
        self.radioButton_Absolute = self.findChild(QRadioButton, 'radioButton_Absolute')
        self.radioButton_Real_Imaginary = self.findChild(QRadioButton, 'radioButton_Real_Imaginary')
        self.radioButton_disable_cursors = self.findChild(QRadioButton, 'radioButton_disable_cursors')
        self.radioButton_cross_cursor = self.findChild(QRadioButton, 'radioButton_cross_cursor')
        self.radioButton_harmonic_cursor = self.findChild(QRadioButton, 'radioButton_harmonic_cursor')
        self.radioButtonEvent()
        self.radioButtonEvent_YAxis()
        self.radioButtonEvent_save_data()
        # QSpinBox
        self.spinBox_skiprows = self.findChild(QSpinBox, 'spinBox_skiprows')
        self.spinBox_vertical_lines = self.findChild(QSpinBox, 'spinBox_vertical_lines')
        # QTabWidget
        self.tabWidget_plot_results = self.findChild(QTabWidget, "tabWidget_plot_results")
        # QWidget
        self.tab_plot = self.tabWidget_plot_results.findChild(QWidget, "tab_plot")


    def _create_connections(self):
        #
        self.checkBox_damping_effect.clicked.connect(self._update_damping_effect)
        #
        self.pushButton_ChooseFolderImport.clicked.connect(self.choose_path_import_results)
        self.pushButton_ChooseFolderExport.clicked.connect(self.choose_path_export_results)
        self.pushButton_ExportResults.clicked.connect(self.ExportResults)
        self.pushButton_ResetPlot.clicked.connect(self.reset_imported_data)
        self.pushButton_AddImportedPlot.clicked.connect(self.ImportResults)  
        self.pushButton_plot.clicked.connect(self.check)
        #
        self.radioButton_normal_axial.clicked.connect(self.radioButtonEvent)
        self.radioButton_normal_bending_y.clicked.connect(self.radioButtonEvent)
        self.radioButton_normal_bending_z.clicked.connect(self.radioButtonEvent)
        self.radioButton_hoop.clicked.connect(self.radioButtonEvent)
        self.radioButton_torsional_shear.clicked.connect(self.radioButtonEvent)
        self.radioButton_transv_shear_xy.clicked.connect(self.radioButtonEvent)
        self.radioButton_transv_shear_xz.clicked.connect(self.radioButtonEvent)
        self.radioButton_plotAbs.clicked.connect(self.radioButtonEvent_YAxis)
        self.radioButton_plotReal.clicked.connect(self.radioButtonEvent_YAxis)
        self.radioButton_plotImag.clicked.connect(self.radioButtonEvent_YAxis)
        self.radioButton_Absolute.clicked.connect(self.radioButtonEvent_save_data)
        self.radioButton_Real_Imaginary.clicked.connect(self.radioButtonEvent_save_data)
        self.radioButton_disable_cursors.clicked.connect(self.update_cursor_controls)
        self.radioButton_cross_cursor.clicked.connect(self.update_cursor_controls)
        self.radioButton_harmonic_cursor.clicked.connect(self.update_cursor_controls)
        self.update_cursor_controls()


    def update_cursor_controls(self):
        if self.radioButton_disable_cursors.isChecked():
            self.checkBox_legends.setChecked(False)
            self.checkBox_legends.setDisabled(True)
            self.frame_vertical_lines.setDisabled(True)
        else:
            self.checkBox_legends.setDisabled(False)
            if self.radioButton_harmonic_cursor.isChecked():
                self.frame_vertical_lines.setDisabled(False)


    def _update_damping_effect(self):
        self.flag_damping_effect = self.checkBox_damping_effect.isChecked()
        self.update_damping = True


    def update(self):
        self.writeElements(self.opv.getListPickedElements())


    def reset_imported_data(self):
        self.imported_data = None
        title = "Information"
        message = "The plot data has been reseted."
        PrintMessageInput([title, message, warning_title])


    def writeElements(self, list_elements_ids):
        text = ""
        for node in list_elements_ids:
            text += "{}, ".format(node)
        self.lineEdit_elementID.setText(text)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()


    def radioButtonEvent(self):
        self.flag_normal_axial = self.radioButton_normal_axial.isChecked()
        self.flag_normal_bending_y = self.radioButton_normal_bending_y.isChecked()
        self.flag_normal_bending_z = self.radioButton_normal_bending_z.isChecked()
        self.flag_hoop = self.radioButton_hoop.isChecked()
        self.flag_torsional_shear = self.radioButton_torsional_shear.isChecked()
        self.flag_transv_shear_xy = self.radioButton_transv_shear_xy.isChecked()
        self.flag_transv_shear_xz = self.radioButton_transv_shear_xz.isChecked()

        self.mask = [self.flag_normal_axial, self.flag_normal_bending_y, self.flag_normal_bending_z, self.flag_hoop,
                    self.flag_torsional_shear, self.flag_transv_shear_xy, self.flag_transv_shear_xz]


    def radioButtonEvent_YAxis(self):
        self.plotAbs = self.radioButton_plotAbs.isChecked()
        self.plotReal = self.radioButton_plotReal.isChecked()
        self.plotImag = self.radioButton_plotImag.isChecked()


    def radioButtonEvent_save_data(self):
        self.save_Absolute = self.radioButton_Absolute.isChecked()
        self.save_Real_Imaginary = self.radioButton_Real_Imaginary.isChecked()


    def messages(self, msg, title = " Information "):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(msg)
        msg_box.setWindowTitle(title)
        msg_box.exec_()


    def choose_path_import_results(self):
        self.import_path, _ = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'Files (*.csv; *.dat; *.txt)')
        self.import_name = basename(self.import_path)
        self.lineEdit_ImportResultsPath.setText(str(self.import_path))


    def ImportResults(self):
        try:
            skiprows = self.spinBox_skiprows.value()
            self.imported_data = np.loadtxt(self.import_path, delimiter=",", skiprows=skiprows)
            self.legend_imported = "imported data: "+ basename(self.import_path).split(".")[0]
            self.tabWidget_plot_results.setCurrentWidget(self.tab_plot)
            title = "Information"
            message = "The results has been imported."
            PrintMessageInput([title, message, warning_title])
        except Exception as log_error:
            title = "Error while loading table"
            message = str(log_error) + " It is recommended to skip the header rows."
            PrintMessageInput([title, message, error_title])
            return


    def choose_path_export_results(self):
        self.save_path = QFileDialog.getExistingDirectory(None, 'Choose a folder to export the results', self.userPath)
        self.save_name = basename(self.save_path)
        self.lineEdit_SaveResultsPath.setText(str(self.save_path))


    def check(self, export=False):

        lineEdit = self.lineEdit_elementID.text()
        stop, self.elementID = self.before_run.check_input_ElementID(lineEdit, single_ID=True)
        
        if stop:
            return True
        
        self.get_stress_data()

        if not export:
            self.plot()


    def ExportResults(self):
        
        if self.lineEdit_FileName.text() != "":
            if self.save_path != "":
                self.export_path_folder = self.save_path + "/"
            else:
                title = "Empty folder input field detected"
                message = "Plese, choose a folder before trying export the results!"
                PrintMessageInput([title, message, warning_title])
                return
        else:
            title = "Empty file name input field"
            message = "Inform a file name before trying export the results!"  
            PrintMessageInput([title, message, warning_title])
            return
        
        if self.check(export=True):
            return

        freq = self.frequencies
        self.export_path = self.export_path_folder + self.lineEdit_FileName.text() + ".dat"
        response = get_stress_spectrum_data(self.stress_data, self.elementID, self.stress_key)

        if self.save_Absolute:
            header = ("Frequency[Hz], Real part [{}], Imaginary part [{}], Absolute [{}]").format(self.unit_label, self.unit_label, self.unit_label)
            data_to_export = np.array([freq, np.real(response), np.imag(response), np.abs(response)]).T
        elif self.save_Real_Imaginary:
            header = ("Frequency[Hz], Real part [{}], Imaginary part [{}]").format(self.unit_label, self.unit_label)
            data_to_export = np.array([freq, np.real(response), np.imag(response)]).T        
            
        np.savetxt(self.export_path, data_to_export, delimiter=",", header=header)
        title = "Information"
        message = "The results have been exported."
        PrintMessageInput([title, message, warning_title])


    def get_stress_data(self):
        
        self.stress_label = self.labels[self.mask][0]
        self.stress_key = self.keys[self.mask][0]

        if self.stress_data == [] or self.update_damping:
            self.stress_data = self.solve.stress_calculate(pressure_external = 0, damping_flag = self.flag_damping_effect)
            self.update_damping = False


    def plot(self):
        """
        """
        plt.ion()
        self.fig = plt.figure(figsize=[12,7])
        ax = self.fig.add_subplot(1,1,1)

        frequencies = self.frequencies
        response = get_stress_spectrum_data(self.stress_data, 
                                            self.elementID, 
                                            self.stress_key, 
                                            absolute=self.plotAbs, 
                                            real=self.plotReal, 
                                            imaginary=self.plotImag)

        if self.plotAbs:
            ax.set_ylabel(("Stress - Absolute [{}]").format(self.unit_label), fontsize = 14, fontweight = 'bold')
        elif self.plotReal:
            ax.set_ylabel(("Stress - Real [{}]").format(self.unit_label), fontsize = 14, fontweight = 'bold')
        elif self.plotImag:
            ax.set_ylabel(("Stress - Imaginary [{}]").format(self.unit_label), fontsize = 14, fontweight = 'bold')

        legend_label = "{} stress at element {}".format(self.stress_label, self.elementID)
        if self.imported_data is None:
                
            if any(value<=0 for value in response):
                first_plot, = plt.plot(frequencies, response, color=[1,0,0], linewidth=2, label=legend_label)
            else:    
                first_plot, = plt.semilogy(frequencies, response, color=[1,0,0], linewidth=2, label=legend_label)
                # second_plot, = plt.semilogy(data[:,0], np.abs(data[:,1]+1j*data[:,2]), color=[0,0,1], linewidth=1)
            _legends = plt.legend(handles=[first_plot], labels=[legend_label])#, loc='upper right')

        else:

            data = self.imported_data
            imported_Xvalues = data[:,0]

            if self.plotAbs:
                imported_Yvalues = np.abs(data[:,1] + 1j*data[:,2])  
            elif self.plotReal:
                imported_Yvalues = data[:,1]
            elif self.plotImag:
                imported_Yvalues = data[:,2]

            if any(value<=0 for value in response) or any(value<=0 for value in imported_Yvalues):
                first_plot, = plt.plot(frequencies, response, color=[1,0,0], linewidth=2)
                second_plot, = plt.plot(imported_Xvalues, imported_Yvalues, color=[0,0,1], linewidth=1, linestyle="--")
            else:    
                first_plot, = plt.semilogy(frequencies, response, color=[1,0,0], linewidth=2, label=legend_label)
                second_plot, = plt.semilogy(imported_Xvalues, imported_Yvalues, color=[0,0,1], linewidth=1, linestyle="--")
            _legends = plt.legend(handles=[first_plot, second_plot], labels=[legend_label, self.legend_imported])#, loc='upper right')

        plt.gca().add_artist(_legends)

        if self.analysisMethod is None:
            title = f"{self.stress_label.upper()} STRESS FREQUENCY RESPONSE"
        else:
            title = f"{self.stress_label.upper()} STRESS FREQUENCY RESPONSE - {self.analysisMethod.upper()}"

        ax.set_title(title, fontsize = 12, fontweight = 'bold')
        ax.set_xlabel('Frequency [Hz]', fontsize = 12, fontweight = 'bold')

        if not self.radioButton_disable_cursors.isChecked():
            show_legend = self.checkBox_legends.isChecked()
            number_vertLines = self.spinBox_vertical_lines.value()
            if self.radioButton_harmonic_cursor.isChecked():
                self.cursor = AdvancedCursor(   ax, 
                                                frequencies, 
                                                response, 
                                                False, 
                                                number_vertLines=number_vertLines, 
                                                show_legend=show_legend   )
            else:
                self.cursor = AdvancedCursor(   ax, 
                                                frequencies, 
                                                response, 
                                                False, 
                                                number_vertLines=1, 
                                                show_legend=show_legend   )

            self.mouse_connection = self.fig.canvas.mpl_connect(s='motion_notify_event', func=self.cursor.mouse_move)

        self.fig.show()