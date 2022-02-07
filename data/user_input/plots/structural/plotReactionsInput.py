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

from pulse.postprocessing.plot_structural_data import get_reactions
from data.user_input.project.printMessageInput import PrintMessageInput

window_title_1 = "ERROR"
window_title_2 = "WARNING"
window_title_3 = "INFORMATION"

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

            if not event.inaxes: 
                return

            x, y = event.xdata, event.ydata
 
            if x>=np.max(self.x): 
                return

            indx = np.searchsorted(self.x, [x])[0]
            
            x = self.x[indx]
            y = self.y[indx]
            self.vl.set_xdata(x)
            self.hl.set_ydata(y)
            self.marker.set_data([x],[y])
            self.marker.set_label("x: %1.2f // y: %4.2e" % (x, y))
            plt.legend(handles=[self.marker], loc='lower left', title=r'$\bf{Cursor}$ $\bf{coordinates:}$')
    
            self.ax.figure.canvas.draw_idle()


class PlotReactionsInput(QDialog):
    def __init__(self, project, opv, analysisMethod, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Plots/Results/Structural/plotReactionsInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
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

        reactions = project.get_structural_reactions()
        self.dict_reactions_at_constrained_dofs, self.dict_reactions_at_springs, self.dict_reactions_at_dampers = reactions

        self.analysisMethod = analysisMethod
        self.frequencies = project.frequencies
        
        self.node_ID = 0
        self.imported_data = None
        self.localDof = None

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')

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

        self.radioButton_Fx = self.findChild(QRadioButton, 'radioButton_Fx')
        self.radioButton_Fy = self.findChild(QRadioButton, 'radioButton_Fy')
        self.radioButton_Fz = self.findChild(QRadioButton, 'radioButton_Fz')
        self.radioButton_Mx = self.findChild(QRadioButton, 'radioButton_Mx')
        self.radioButton_My = self.findChild(QRadioButton, 'radioButton_My')
        self.radioButton_Mz = self.findChild(QRadioButton, 'radioButton_Mz')
        self.Fx = self.radioButton_Fx.isChecked()
        self.Fy = self.radioButton_Fy.isChecked()
        self.Fz = self.radioButton_Fz.isChecked()
        self.Mx = self.radioButton_Mx.isChecked()
        self.My = self.radioButton_My.isChecked()
        self.Mz = self.radioButton_Mz.isChecked()

        self.list_radioButtons = [  self.radioButton_Fx, self.radioButton_Fy, self.radioButton_Fz,
                                    self.radioButton_Mx, self.radioButton_My, self.radioButton_Mz   ]

        self.checkBox_cursor = self.findChild(QCheckBox, 'checkBox_cursor')
        self.cursor = self.checkBox_cursor.isChecked()
        self.checkBox_cursor.clicked.connect(self.update_cursor)

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
        self.pushButton_plot_reactions_frequency_response = self.findChild(QPushButton, 'pushButton_plot_reactions_frequency_response')
        self.pushButton_plot_reactions_frequency_response.clicked.connect(self.check)

        self.treeWidget_reactions_at_springs = self.findChild(QTreeWidget, 'treeWidget_reactions_at_springs')
        self.treeWidget_reactions_at_springs.setColumnWidth(1, 20)
        self.treeWidget_reactions_at_springs.setColumnWidth(2, 80)
        self.treeWidget_reactions_at_springs.itemClicked.connect(self.on_click_item)
        self.treeWidget_reactions_at_springs.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.treeWidget_reactions_at_dampers = self.findChild(QTreeWidget, 'treeWidget_reactions_at_dampers')
        self.treeWidget_reactions_at_dampers.setColumnWidth(1, 20)
        self.treeWidget_reactions_at_dampers.setColumnWidth(2, 80)
        self.treeWidget_reactions_at_dampers.itemClicked.connect(self.on_click_item)
        self.treeWidget_reactions_at_dampers.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.treeWidget_reactions_at_constrained_dofs = self.findChild(QTreeWidget, 'treeWidget_reactions_at_constrained_dofs')
        self.treeWidget_reactions_at_constrained_dofs.setColumnWidth(1, 20)
        self.treeWidget_reactions_at_constrained_dofs.setColumnWidth(2, 80)
        self.treeWidget_reactions_at_constrained_dofs.itemClicked.connect(self.on_click_item)
        self.treeWidget_reactions_at_constrained_dofs.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.tabWidget_reactions = self.findChild(QTabWidget, "tabWidget_reactions")
        self.tab_constrained_dofs = self.tabWidget_plot_results.findChild(QWidget, "tab_constrained_dofs")
        self.tab_external_springs_dampers = self.tabWidget_plot_results.findChild(QWidget, "tab_external_springs_dampers")

        self.tabWidget_springs_dampers = self.findChild(QTabWidget, "tabWidget_springs_dampers")
        self.tab_nodes_with_springs = self.tabWidget_springs_dampers.findChild(QWidget, "tab_nodes_with_springs")
        self.tab_nodes_with_dampers = self.tabWidget_springs_dampers.findChild(QWidget, "tab_nodes_with_dampers")

        self.load_nodes_info()
        self.exec_()

    def update_cursor(self):
        self.cursor = self.checkBox_cursor.isChecked()

    def reset_imported_data(self):
        self.imported_data = None
        title = "Information"
        message = "The plot data has been reseted."
        PrintMessageInput([title, message, window_title_2])
    
    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        self.lineEdit_nodeID.setText(text)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def isInt(self, value):
        try:
            int(value)
            return True
        except:
            return False

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
            skiprows = int(self.lineEdit_skiprows.text())
            self.imported_data = np.loadtxt(self.import_path, delimiter=",",skiprows=skiprows)
            self.legend_imported = "imported data: "+ basename(self.import_path).split(".")[0]
            self.tabWidget_plot_results.setCurrentWidget(self.tab_plot)
            
            title = "Loading table"
            message = "The reactions data have been imported."
            PrintMessageInput([title, message, window_title_3])
        except Exception as _error:
            
            title = "Error reached while loading table"
            message = f"{str(_error)}\n It is recommended to skip the header rows." 
            PrintMessageInput([title, message, window_title_1])

    def choose_path_export_results(self):
        self.save_path = QFileDialog.getExistingDirectory(None, 'Choose a folder to export the results', self.userPath)
        self.save_name = basename(self.save_path)
        self.lineEdit_SaveResultsPath.setText(str(self.save_path))

    def text_label(self, mask):
        
        text = ""
        load_labels = np.array(['Fx','Fy','Fz','Mx','My','Mz'])
        temp = load_labels[mask]

        if list(mask).count(True) == 6:
            text = "[{}, {}, {}, {}, {}, {}]".format(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5])
        elif list(mask).count(True) == 5:
            text = "[{}, {}, {}, {}, {}]".format(temp[0], temp[1], temp[2], temp[3], temp[4])
        elif list(mask).count(True) == 4:
            text = "[{}, {}, {}, {}]".format(temp[0], temp[1], temp[2], temp[3])
        elif list(mask).count(True) == 3:
            text = "[{}, {}, {}]".format(temp[0], temp[1], temp[2])
        elif list(mask).count(True) == 2:
            text = "[{}, {}]".format(temp[0], temp[1])
        elif list(mask).count(True) == 1:
            text = "[{}]".format(temp[0])
        return text

    def load_nodes_info(self):
        
        for node in self.preprocessor.nodes_connected_to_springs:
            lumped_stiffness_mask = [False if bc is None else True for bc in node.lumped_stiffness]
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(lumped_stiffness_mask))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_reactions_at_springs.addTopLevelItem(new)

        for node in self.preprocessor.nodes_connected_to_dampers:
            lumped_dampings_mask = [False if bc is None else True for bc in node.lumped_dampings]
            new = QTreeWidgetItem([str(node.external_index), str(self.text_label(lumped_dampings_mask))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_reactions_at_dampers.addTopLevelItem(new)

        for node in self.preprocessor.nodes_with_constrained_dofs:
            constrained_dofs_mask = [False, False, False, False, False, False]
            for index, value in enumerate(node.prescribed_dofs):
                if isinstance(value, complex):
                    if value == complex(0):
                        constrained_dofs_mask[index] = True
                elif isinstance(value, np.ndarray):
                    constrained_dofs_mask[index] = False
            # constrained_dofs_mask = np.array(node.prescribed_dofs) == complex(0)
            if constrained_dofs_mask.count(False) != 6:         
                new = QTreeWidgetItem([str(node.external_index), str(self.text_label(constrained_dofs_mask))])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_reactions_at_constrained_dofs.addTopLevelItem(new)

    def disable_non_existing_reactions(self, node_id):

        node = self.preprocessor.nodes[int(node_id)]
        if self.tabWidget_reactions.currentIndex()==0:
            mask = [False, False, False, False, False, False]
            for index, value in enumerate(node.prescribed_dofs):
                if isinstance(value, complex):
                    if value == complex(0):
                        mask[index] = True
                elif isinstance(value, np.ndarray):
                    mask[index] = True

            # mask = np.array(node.prescribed_dofs) == complex(0)
            self.reactions = self.dict_reactions_at_constrained_dofs
            self.damper = False

        elif self.tabWidget_reactions.currentIndex()==1:
            if self.tabWidget_springs_dampers.currentIndex()==0:
                mask = [False if bc is None else True for bc in node.lumped_stiffness]
                self.reactions = self.dict_reactions_at_springs
                self.damper = False

            elif self.tabWidget_springs_dampers.currentIndex()==1:
                mask = [False if bc is None else True for bc in node.lumped_dampings]
                self.reactions = self.dict_reactions_at_dampers
                self.damper = True

        list_disabled_buttons = []
        for index, radioButton in enumerate(self.list_radioButtons):
            radioButton.setDisabled(not mask[index])
            if not radioButton.isEnabled():
                list_disabled_buttons.append(radioButton)

        if len(list_disabled_buttons) > 0:
            for radioButton in self.list_radioButtons:
                if radioButton.isEnabled():
                    radioButton.setChecked(True)
                    break

    def on_click_item(self, item):
        self.lineEdit_nodeID.setText(item.text(0))
        self.disable_non_existing_reactions(item.text(0))

    def on_doubleclick_item(self, item):
        self.lineEdit_nodeID.setText(item.text(0))
        self.check()

    def button(self):
        self.check()         

    def check(self, export=False):
        
        lineEdit_nodeID = self.lineEdit_nodeID.text()
        stop, self.node_ID = self.before_run.check_input_NodeID(lineEdit_nodeID, single_ID=True)
        if stop:
            return

        self.localDof = None
        if self.radioButton_Fx.isChecked():
            self.localDof = 0
            self.localdof_label = "Fx"
            self.unit_label = "N"
            self.reaction_label = "Force reactions"

        if self.radioButton_Fy.isChecked():
            self.localDof = 1
            self.localdof_label = "Fy"
            self.unit_label = "N"
            self.reaction_label = "Force reactions"

        if self.radioButton_Fz.isChecked():
            self.localDof = 2
            self.localdof_label = "Fz"
            self.unit_label = "N"
            self.reaction_label = "Force reactions"
 
        if self.radioButton_Mx.isChecked():
            self.localDof = 3
            self.localdof_label = "Mx"
            self.unit_label = "N.m"
            self.reaction_label = "Moment reactions"

        if self.radioButton_My.isChecked():
            self.localDof = 4
            self.localdof_label = "My"
            self.unit_label = "N.m"
            self.reaction_label = "Moment reactions"

        if self.radioButton_Mz.isChecked():
            self.localDof = 5
            self.localdof_label = "Mz"
            self.unit_label = "N.m"
            self.reaction_label = "Moment reactions"
        
        if not export:
            self.plot()

    def ExportResults(self):
        
        if self.lineEdit_FileName.text() != "":
            if self.save_path != "":
                self.export_path_folder = self.save_path + "/"
            else:
                
                title = "Additional action required"
                message = "Plese, choose a folder before trying export the results!"
                PrintMessageInput([title, message, window_title_2])
                return
        else:
            title = "Additional action required"
            message = "Inform a file name before trying export the results!"
            PrintMessageInput([title, message, window_title_2])
            return
        
        self.check(export=True)
        freq = self.frequencies
        self.export_path = self.export_path_folder + self.lineEdit_FileName.text() + ".dat"
        if self.save_Absolute:
            response = get_reactions(self.preprocessor, self.reactions, self.node_ID, self.localDof)
            header = ("Frequency[Hz], Real part [{}], Imaginary part [{}], Absolute [{}]").format(  self.unit_label, 
                                                                                                    self.unit_label, 
                                                                                                    self.unit_label )
            data_to_export = np.array([freq, np.real(response), np.imag(response), np.abs(response)]).T
        elif self.save_Real_Imaginary:
            response = get_reactions(self.preprocessor, self.reactions, self.node_ID, self.localDof)
            header = ("Frequency[Hz], Real part [{}], Imaginary part [{}]").format(self.unit_label, self.unit_label)
            data_to_export = np.array([freq, np.real(response), np.imag(response)]).T        
            
        np.savetxt(self.export_path, data_to_export, delimiter=",", header=header)
        title = "Information"
        message = "The results have been exported."
        PrintMessageInput([title, message, window_title_2])
 
    def plot(self):

        fig = plt.figure(figsize=[12,7])
        ax = fig.add_subplot(1,1,1)

        frequencies = self.frequencies
        response = get_reactions(   self.preprocessor, 
                                    self.reactions, 
                                    self.node_ID, 
                                    self.localDof, 
                                    absolute=self.plotAbs, 
                                    real=self.plotReal, 
                                    imaginary=self.plotImag )

        if self.damper and self.frequencies[0]==0:
            frequencies = self.frequencies[1:]
            response = response[1:]

        if self.plotAbs:
            ax.set_ylabel(("{} - Absolute [{}]").format(self.reaction_label, self.unit_label), fontsize = 14, fontweight = 'bold')
        elif self.plotReal:
            ax.set_ylabel(("{} - Real [{}]").format(self.reaction_label, self.unit_label), fontsize = 14, fontweight = 'bold')
        elif self.plotImag:
            ax.set_ylabel(("{} - Imaginary [{}]").format(self.reaction_label, self.unit_label), fontsize = 14, fontweight = 'bold')

        #cursor = Cursor(ax)
        cursor = SnaptoCursor(ax, frequencies, response, self.cursor)
        plt.connect('motion_notify_event', cursor.mouse_move)

        legend_label = "Reaction {} at node {}".format(self.localdof_label, self.node_ID)
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

        ax.set_title(('REACTIONS FREQUENCY RESPONSE - {}').format(self.analysisMethod.upper()), fontsize = 16, fontweight = 'bold')
        ax.set_xlabel(('Frequency [Hz]'), fontsize = 14, fontweight = 'bold')

        plt.show()