import sys
from os.path import expanduser, basename, exists, dirname
from pathlib import Path

import numpy as np

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QAction, QToolBar, QSplitter, QFileDialog, QMessageBox, QMainWindow

from pulse.uix.infoUi import InfoUi
from pulse.uix.opvUi import OPVUi
from pulse.project import Project
from pulse.uix.inputUi import InputUi

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.project = Project()
        self._load_icons()
        self._config()
        self._create_basic_layout()
        self._create_actions()
        self._create_menu_bar()
        self._create_tool_bar()
        self.show()

    def _load_icons(self):
        icons_path = 'pulse\\data\\icons\\'
        self.pulse_icon = QIcon(icons_path + 'pulse.png')
        self.new_icon = QIcon(icons_path + 'add.png')
        self.open_icon = QIcon(icons_path + 'upload.png')
        self.saveImage_icon = QIcon(icons_path + 'save_image.png')
        self.exit_icon = QIcon(icons_path + 'exit.png')

    def _config(self):
        self.setMinimumSize(QSize(800, 600))
        self.showMaximized()
        self.setWindowIcon(self.pulse_icon)
        self._change_window_title()

    def _change_window_title(self, msg = ""):
        title = "OpenPulse"
        if (msg != ""):
            title += " - " + msg
        self.setWindowTitle(title)

    def _create_actions(self):
        #File
        self.new_action = QAction(self.new_icon, '&New Project', self)        
        self.new_action.setShortcut('Ctrl+N')
        self.new_action.setStatusTip('New Project')
        self.new_action.triggered.connect(self.new_call)

        self.import_action = QAction(self.open_icon, '&Import Project', self)       
        self.import_action.setShortcut('Ctrl+O')
        self.import_action.setStatusTip('Import Project')
        self.import_action.triggered.connect(self.import_call)

        self.saveAsPng_action = QAction(self.saveImage_icon, '&Save as PNG', self)       
        self.saveAsPng_action.setShortcut('Ctrl+S')
        self.saveAsPng_action.setStatusTip('Save as PNG')
        self.saveAsPng_action.triggered.connect(self.savePNG_call)

        self.exit_action = QAction(self.exit_icon, '&Exit', self)        
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setStatusTip('Exit application')
        self.exit_action.triggered.connect(self.close)

        #Help
        self.help_action = QAction('&Help', self)        
        self.help_action.setStatusTip('Help')

        #Graphics
        self.entities_action = QAction('&Entity', self)        
        self.entities_action.setShortcut('Ctrl+1')
        self.entities_action.setStatusTip('Plot Entities')
        self.entities_action.triggered.connect(self.plot_entities)

        self.elements_action = QAction('&Elements', self)        
        self.elements_action.setShortcut('Ctrl+2')
        self.elements_action.setStatusTip('Plot Elements')
        self.elements_action.triggered.connect(self.plot_elements)

        self.points_action = QAction('&Points', self)        
        self.points_action.setShortcut('Ctrl+3')
        self.points_action.setStatusTip('Plot Points')
        self.points_action.triggered.connect(self.plot_points)

        #Structural Model Setup
        self.setMaterial_action = QAction('&Set Material', self)        
        self.setMaterial_action.setShortcut('Alt+1')
        self.setMaterial_action.setStatusTip('Set Material')
        self.setMaterial_action.triggered.connect(self.getInputWidget().setMaterial)

        self.setCrossSection_action = QAction('&Set Cross-Section', self)        
        self.setCrossSection_action.setShortcut('Alt+2')
        self.setCrossSection_action.setStatusTip('Set Cross-Section')
        self.setCrossSection_action.triggered.connect(self.getInputWidget().setCrossSection)

        self.setElementType_action = QAction('&Set Element Type', self)        
        self.setElementType_action.setShortcut('Alt+3')
        self.setElementType_action.setStatusTip('Set Element Type')
        self.setElementType_action.triggered.connect(self.getInputWidget().setElementType)

        self.setDOF_action = QAction('&Set Prescribed DOFs', self)        
        self.setDOF_action.setShortcut('Alt+4')
        self.setDOF_action.setStatusTip('Set Prescribed DOFs')
        self.setDOF_action.triggered.connect(self.getInputWidget().setDOF)

        self.setForce_action = QAction('&Set Nodal Loads', self)        
        self.setForce_action.setShortcut('Alt+5')
        self.setForce_action.setStatusTip('Set Nodal Loads')
        self.setForce_action.triggered.connect(self.getInputWidget().setNodalLoads)

        self.setMass_action = QAction('&Add: Mass / Spring / Damper', self)        
        self.setMass_action.setShortcut('Alt+6')
        self.setMass_action.setStatusTip('Add: Mass / Spring / Damper')
        self.setMass_action.triggered.connect(self.getInputWidget().addMassSpringDamper)

        #Structural Model Setup
        self.setFluid_action = QAction('&Set Fluid', self)        
        self.setFluid_action.setShortcut('Ctrl+Alt+1')
        self.setFluid_action.setStatusTip('Set Fluid')
        self.setFluid_action.triggered.connect(self.getInputWidget().setFluid)

        self.setAcousticPressure_action = QAction('&Set Fluid', self)        
        self.setAcousticPressure_action.setShortcut('Ctrl+Alt+2')
        self.setAcousticPressure_action.setStatusTip('Set Acoustic Pressure')
        self.setAcousticPressure_action.triggered.connect(self.getInputWidget().setFluid)

        self.setVolumeVelocity_action = QAction('&Set Fluid', self)        
        self.setVolumeVelocity_action.setShortcut('Ctrl+Alt+3')
        self.setVolumeVelocity_action.setStatusTip('Set Volume Velocity')
        self.setVolumeVelocity_action.triggered.connect(self.getInputWidget().setFluid)

        self.setSpecificImpedance_action = QAction('&Set Fluid', self)        
        self.setSpecificImpedance_action.setShortcut('Ctrl+Alt+4')
        self.setSpecificImpedance_action.setStatusTip('Set Specific Impedance')
        self.setSpecificImpedance_action.triggered.connect(self.getInputWidget().setFluid)

        #Analysis
        self.selectAnalysisType_action = QAction('&Select Analysis Type', self)        
        self.selectAnalysisType_action.setShortcut('Alt+Q')
        self.selectAnalysisType_action.setStatusTip('Select Analysis Type')
        self.selectAnalysisType_action.triggered.connect(self.getInputWidget().analyseTypeInput)
        
        self.analysisSetup_action = QAction('&Analysis Setup', self)        
        self.analysisSetup_action.setShortcut('Alt+W')
        self.analysisSetup_action.setStatusTip('Analysis Setup')
        self.analysisSetup_action.triggered.connect(self.getInputWidget().analyseSetup)

        self.selectOutput_action = QAction('&Select the Outputs Results', self)        
        self.selectOutput_action.setShortcut('Alt+E')
        self.selectOutput_action.setStatusTip('Select the Outputs Results')
        self.selectOutput_action.triggered.connect(self.getInputWidget().analyseOutputResults)

        self.runAnalysis_action = QAction('&Run Analysis', self)        
        self.runAnalysis_action.setShortcut('Alt+R')
        self.runAnalysis_action.setStatusTip('Run Analysis')
        self.runAnalysis_action.triggered.connect(self.getInputWidget().runAnalyse)

        #Results Viewer
        self.plotModeShapes_action = QAction('&Plot Mode Shapes', self)        
        self.plotModeShapes_action.setShortcut('Ctrl+Q')
        self.plotModeShapes_action.setStatusTip('Plot Mode Shapes')
        self.plotModeShapes_action.triggered.connect(self.getInputWidget().plotModeShapes)

        self.plotHarmonicResponse_action = QAction('&Plot Harmonic Response', self)        
        self.plotHarmonicResponse_action.setShortcut('Ctrl+W')
        self.plotHarmonicResponse_action.setStatusTip('Plot Harmonic Response')
        self.plotHarmonicResponse_action.triggered.connect(self.getInputWidget().plotHarmonicResponse)

        self.plotPressureField_action = QAction('&Plot Pressure Field', self)        
        self.plotPressureField_action.setShortcut('Ctrl+E')
        self.plotPressureField_action.setStatusTip('Plot Pressure Field')
        self.plotPressureField_action.triggered.connect(self.getInputWidget().plotPressureField)

        self.plotSressField_action = QAction('&Plot Stress Field', self)        
        self.plotSressField_action.setShortcut('Ctrl+R')
        self.plotSressField_action.setStatusTip('Plot Stress Field')
        self.plotSressField_action.triggered.connect(self.getInputWidget().plotStressField)

        self.plotFrequencyResponse_action = QAction('&Plot Frequency Response', self)        
        self.plotFrequencyResponse_action.setShortcut('Ctrl+T')
        self.plotFrequencyResponse_action.setStatusTip('Plot Frequency Response')
        self.plotFrequencyResponse_action.triggered.connect(self.getInputWidget().plotFrequencyResponse)


    def _create_menu_bar(self):
        menuBar = self.menuBar()

        projectMenu = menuBar.addMenu('&Project')
        graphicMenu = menuBar.addMenu('&Graphic')
        modelSetup = menuBar.addMenu('&Model Setup')
        analysisMenu = menuBar.addMenu('&Analysis')
        resultsViewerMenu = menuBar.addMenu('&Results Viewer')
        helpMenu = menuBar.addMenu("&Help")

        projectMenu.addAction(self.new_action)
        projectMenu.addAction(self.import_action)
        projectMenu.addAction(self.saveAsPng_action)
        projectMenu.addAction(self.exit_action)

        graphicMenu.addAction(self.entities_action)
        graphicMenu.addAction(self.elements_action)
        graphicMenu.addAction(self.points_action)

        modelSetup.addAction(self.setMaterial_action)
        modelSetup.addAction(self.setCrossSection_action)
        modelSetup.addAction(self.setElementType_action)
        modelSetup.addAction(self.setDOF_action)
        modelSetup.addAction(self.setForce_action)
        modelSetup.addAction(self.setMass_action)

        modelSetup.addAction(self.setFluid_action)
        modelSetup.addAction(self.setAcousticPressure_action)
        modelSetup.addAction(self.setVolumeVelocity_action)
        modelSetup.addAction(self.setSpecificImpedance_action)

        analysisMenu.addAction(self.selectAnalysisType_action)
        analysisMenu.addAction(self.analysisSetup_action)
        analysisMenu.addAction(self.selectOutput_action)
        analysisMenu.addAction(self.runAnalysis_action)

        resultsViewerMenu.addAction(self.plotModeShapes_action)
        resultsViewerMenu.addAction(self.plotHarmonicResponse_action)
        resultsViewerMenu.addAction(self.plotPressureField_action)
        resultsViewerMenu.addAction(self.plotSressField_action)
        resultsViewerMenu.addAction(self.plotFrequencyResponse_action)

        helpMenu.addAction(self.help_action)

    def _create_tool_bar(self):
        self.toolbar = QToolBar("Enable Toolbar")
        self.toolbar.setIconSize(QSize(26,26))
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.new_action)
        self.toolbar.addAction(self.import_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.saveAsPng_action)

    def _create_basic_layout(self):
        self.info_widget = InfoUi(self)
        self.opv_widget = OPVUi(self.project, self)
        self.inputWidget = InputUi(self.project, self)

        working_area = QSplitter(Qt.Horizontal)
        self.setCentralWidget(working_area)

        working_area.addWidget(self.info_widget)
        working_area.addWidget(self.opv_widget)
        working_area.setSizes([100,300])

    def new_call(self):
        if self.inputWidget.newProject():
            self.resetInfo()
            self._change_window_title(self.project.getProjectName())
            self.draw()

    def import_call(self):
        userPath = expanduser('~')
        projectPath = "{}\\OpenPulse\\Projects".format(userPath)
        if not exists(projectPath):
            projectPath = ""
        path, _type = QFileDialog.getOpenFileName(None, 'Open file', projectPath, 'OpenPulse Project (*.ini)')
        if path != "":
            self.resetInfo()
            self.project.loadProject(path)
            self._change_window_title(self.project.getProjectName())
            self.draw()

    def savePNG_call(self):
        userPath = expanduser('~')
        projectPath = "{}\\OpenPulse\\Projects".format(userPath)
        if not exists(projectPath):
            projectPath = ""
        path, _type = QFileDialog.getSaveFileName(None, 'Save file', projectPath, 'PNG (*.png)')
        if path != "":
            self.getOPVWidget().savePNG(path)

    def resetInfo(self):
        self.opv_widget.resetInfo()

    def plot_entities(self):
        self.opv_widget.change_to_entities()

    def plot_elements(self):
        self.opv_widget.change_to_elements()

    def plot_points(self):
        self.opv_widget.change_to_points()

    def draw(self):
        self.opv_widget.plot_entities()
        self.opv_widget.plot_points()
        self.opv_widget.plot_elements()
        self.plot_entities()

    def closeEvent(self, event):
        close = QMessageBox.question(
            self,
            "QUIT",
            "Are you sure want to stop process?",
            QMessageBox.No | QMessageBox.Yes)
        
        if close == QMessageBox.Yes:
            sys.exit()
        else:
            event.ignore()

    def getInputWidget(self):
        return self.inputWidget

    def getInfoWidget(self):
        return self.info_widget

    def getOPVWidget(self):
        return self.opv_widget

    def getProject(self):
        return self.project