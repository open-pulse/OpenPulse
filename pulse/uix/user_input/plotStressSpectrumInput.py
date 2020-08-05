from PyQt5.QtWidgets import QLineEdit, QDialog, QFileDialog, QWidget, QTreeWidget, QToolButton, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QLabel, QCheckBox, QPushButton, QSpinBox
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
import os
import matplotlib.pyplot as plt
import numpy as np

from pulse.postprocessing.plot_structural_data import get_structural_frf
from pulse.utils import error

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


class PlotStressSpectrumInput(QDialog):
    def __init__(self, mesh, analysisMethod, frequencies, solution, list_elements_ids, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/plotStressSpectrumInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)
        self.userPath = os.path.expanduser('~')
        self.save_path = ""

        self.mesh = mesh
        
        self.analysisMethod = analysisMethod
        self.frequencies = frequencies
        self.solution = solution
        self.nodeID = 0
        self.imported_data = None
        self.localDof = None

        self.writeElements(list_elements_ids)

        self.lineEdit_elementID = self.findChild(QLineEdit, 'lineEdit_nodeID')

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
        self.lineEdit_skiprows = self.findChild(QSpinBox, 'spinBox')

        self.checkBox_cursor = self.findChild(QCheckBox, 'checkBox_cursor')
        self.cursor = self.checkBox_cursor.isChecked()
        self.checkBox_cursor.clicked.connect(self.update_cursor)

        self.radioButton_normal_axial = self.findChild(QRadioButton, 'radioButton_normal_axial')
        self.radioButton_normal_bending_y = self.findChild(QRadioButton, 'radioButton_normal_bending_y')
        self.radioButton_normal_bending_z = self.findChild(QRadioButton, 'radioButton_normal_bending_z')
        self.radioButton_hoop = self.findChild(QRadioButton, 'radioButton_hoop')
        self.radioButton_transv_shear_xy = self.findChild(QRadioButton, 'radioButton_transv_shear_xy')
        self.radioButton_transv_shear_xz = self.findChild(QRadioButton, 'radioButton_transv_shear_xz')
        self.radioButton_torsional_shear = self.findChild(QRadioButton, 'radioButton_torsional_shear')

        self.radioButton_normal_axial.clicked.connect(self.radioButtonEvent)
        self.radioButton_normal_bending_y.clicked.connect(self.radioButtonEvent)
        self.radioButton_normal_bending_z.clicked.connect(self.radioButtonEvent)
        self.radioButton_hoop.clicked.connect(self.radioButtonEvent)
        self.radioButton_torsional_shear.clicked.connect(self.radioButtonEvent)
        self.radioButton_transv_shear_xy.clicked.connect(self.radioButtonEvent)
        self.radioButton_transv_shear_xz.clicked.connect(self.radioButtonEvent)

        self.flag_normal_axial = self.radioButton_normal_axial.isChecked()
        self.flag_normal_bending_y = self.radioButton_normal_bending_y.isChecked()
        self.flag_normal_bending_z = self.radioButton_normal_bending_z.isChecked()
        self.flag_hoop = self.radioButton_hoop.isChecked()
        self.flag_torsional_shear = self.radioButton_torsional_shear.isChecked()
        self.flag_transv_shear_xy = self.radioButton_transv_shear_xy.isChecked()
        self.flag_transv_shear_xz = self.radioButton_transv_shear_xz.isChecked()

        self.mask = [self.flag_normal_axial, self.flag_normal_bending_y, self.flag_normal_bending_z, self.flag_hoop,
                    self.flag_torsional_shear, self.flag_transv_shear_xy, self.flag_transv_shear_xz]

        self.radioButton_plotAbs = self.findChild(QRadioButton, 'radioButton_plotAbs')
        self.radioButton_plotReal = self.findChild(QRadioButton, 'radioButton_plotReal')
        self.radioButton_plotImag = self.findChild(QRadioButton, 'radioButton_plotImag')
        self.radioButton_plotAbs.clicked.connect(self.radioButtonEvent_YAxis)
        self.radioButton_plotReal.clicked.connect(self.radioButtonEvent_YAxis)
        self.radioButton_plotImag.clicked.connect(self.radioButtonEvent_YAxis)
        self.plotAbs = self.radioButton_plotAbs.isChecked()
        self.plotReal = self.radioButton_plotReal.isChecked()
        self.plotImag = self.radioButton_plotImag.isChecked()

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
        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.pushButton.clicked.connect(self.check)

        self.exec_()

    def update_cursor(self):
        self.cursor = self.checkBox_cursor.isChecked()

    def reset_imported_data(self):
        self.imported_data = None
        self.messages("The plot data has been reseted.")
    
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
        self.import_path, _ = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'Files (*.dat; *.csv)')
        self.import_name = basename(self.import_path)
        self.lineEdit_ImportResultsPath.setText(str(self.import_path))
    
    def ImportResults(self):
        try:
            skiprows = int(self.lineEdit_skiprows.text())
            self.imported_data = np.loadtxt(self.import_path, delimiter=",", skiprows=skiprows)
            self.legend_imported = "imported data: "+ basename(self.import_path).split(".")[0]
            self.tabWidget_plot_results.setCurrentWidget(self.tab_plot)
            self.messages("The results has been imported.")
        except Exception as e:
            message = [str(e) + " It is recommended to skip the header rows."] 
            error(message[0], title="ERROR WHILE LOADING TABLE")
            return

    def choose_path_export_results(self):
        self.save_path = QFileDialog.getExistingDirectory(None, 'Choose a folder to export the results', self.userPath)
        self.save_name = basename(self.save_path)
        self.lineEdit_SaveResultsPath.setText(str(self.save_path))

    def check(self, export=False):
        self.localDof = None
        try:
            tokens = self.lineEdit_elementID.text().strip().split(',')
            try:
                tokens.remove('')
            except:
                pass
            node_typed = list(map(int, tokens))
            if len(node_typed) == 1:
                try:
                    self.nodeID = self.mesh.nodes[node_typed[0]].external_index
                except:
                    error("Incorrect Node ID input!")
                    return
            elif len(node_typed) == 0:
                error("Please, enter a valid Node ID!")
                return
            else:
                error("Multiple Node IDs", "Error Node ID's")
                return
        except Exception:
            error("Wrong input for Node ID's!", "Error Node ID's")
            return

        if self.radioButton_ux.isChecked():
            self.localDof = 0
            self.localdof_label = "Ux"
            self.unit_label = "m"

        if self.radioButton_uy.isChecked():
            self.localDof = 1
            self.localdof_label = "Uy"
            self.unit_label = "m"

        if self.radioButton_uz.isChecked():
            self.localDof = 2
            self.localdof_label = "Uz"
            self.unit_label = "m"
 
        if self.radioButton_rx.isChecked():
            self.localDof = 3
            self.localdof_label = "Rx"
            self.unit_label = "rad"

        if self.radioButton_ry.isChecked():
            self.localDof = 4
            self.localdof_label = "Ry"
            self.unit_label = "rad"

        if self.radioButton_rz.isChecked():
            self.localDof = 5
            self.localdof_label = "Rz"
            self.unit_label = "rad"
        
        if not export:
            self.plot()

    def ExportResults(self):
        
        if self.lineEdit_FileName.text() != "":
            if self.save_path != "":
                self.export_path_folder = self.save_path + "/"
            else:
                error("Plese, choose a folder before trying export the results!")
                return
        else:
            error("Inform a file name before trying export the results!")
            return
        
        self.check(export=True)
        freq = self.frequencies
        self.export_path = self.export_path_folder + self.lineEdit_FileName.text() + ".dat"
        if self.save_Absolute:
            response = get_structural_frf(self.mesh, self.solution, self.nodeID, self.localDof)
            header = ("Frequency[Hz], Real part [{}], Imaginary part [{}], Absolute [{}]").format(self.unit_label, self.unit_label, self.unit_label)
            data_to_export = np.array([freq, np.real(response), np.imag(response), np.abs(response)]).T
        elif self.save_Real_Imaginary:
            response = get_structural_frf(self.mesh, self.solution, self.nodeID, self.localDof)
            header = ("Frequency[Hz], Real part [{}], Imaginary part [{}]").format(self.unit_label, self.unit_label)
            data_to_export = np.array([freq, np.real(response), np.imag(response)]).T        
            
        np.savetxt(self.export_path, data_to_export, delimiter=",", header=header)
        self.messages("The results has been exported.")

    def plot(self):

        fig = plt.figure(figsize=[12,7])
        ax = fig.add_subplot(1,1,1)

        frequencies = self.frequencies
        response = get_structural_frf(self.mesh, self.solution, self.nodeID, self.localDof, absolute=self.plotAbs, real=self.plotReal, imaginary=self.plotImag)

        if self.plotAbs:
            ax.set_ylabel(("Structural Response - Absolute [{}]").format(self.unit_label), fontsize = 14, fontweight = 'bold')
        elif self.plotReal:
            ax.set_ylabel(("Structural Response - Real [{}]").format(self.unit_label), fontsize = 14, fontweight = 'bold')
        elif self.plotImag:
            ax.set_ylabel(("Structural Response - Imaginary [{}]").format(self.unit_label), fontsize = 14, fontweight = 'bold')

        #cursor = Cursor(ax)
        cursor = SnaptoCursor(ax, frequencies, response, self.cursor)
        plt.connect('motion_notify_event', cursor.mouse_move)

        legend_label = "Response {} at node {}".format(self.localdof_label, self.nodeID)
        if self.imported_data is None:
                
            if any(value<=0 for value in response):
                first_plot, = plt.plot(frequencies, response, color=[1,0,0], linewidth=2, label=legend_label)
            else:    
                first_plot, = plt.semilogy(frequencies, response, color=[1,0,0], linewidth=2, label=legend_label)
                # second_plot, = plt.semilogy(data[:,0], np.abs(data[:,1]+1j*data[:,2]), color=[0,0,1], linewidth=1)
            _legends = plt.legend(handles=[first_plot], labels=[legend_label], loc='upper right')

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
            _legends = plt.legend(handles=[first_plot, second_plot], labels=[legend_label, self.legend_imported], loc='upper right')

        plt.gca().add_artist(_legends)

        ax.set_title(('Frequency Response: {} Method').format(self.analysisMethod), fontsize = 18, fontweight = 'bold')
        ax.set_xlabel(('Frequency [Hz]'), fontsize = 14, fontweight = 'bold')

        plt.show()