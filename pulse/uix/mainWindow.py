import sys
from os.path import expanduser, basename, exists, dirname
from pathlib import Path

import numpy as np

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5 import QtCore
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

        self.entities_action_radius = QAction('&Entity with Cross-section', self)        
        self.entities_action_radius.setShortcut('Ctrl+2')
        self.entities_action_radius.setStatusTip('Plot Entities with Cross-section')
        self.entities_action_radius.triggered.connect(self.plot_entities_radius)

        self.points_action = QAction('&Nodes', self)        
        self.points_action.setShortcut('Ctrl+3')
        self.points_action.setStatusTip('Plot Nodes')
        self.points_action.triggered.connect(self.plot_points)

        self.elements_action = QAction('&Elements', self)        
        self.elements_action.setShortcut('Ctrl+4')
        self.elements_action.setStatusTip('Plot Elements')
        self.elements_action.triggered.connect(self.plot_elements)

        #Structural Model Setup
        self.set_material_action = QAction('&Set Material', self)        
        self.set_material_action.setShortcut('Alt+1')
        self.set_material_action.setStatusTip('Set Material')
        self.set_material_action.triggered.connect(self.getInputWidget().set_material)

        self.set_crossSection_action = QAction('&Set Cross-Section', self)        
        self.set_crossSection_action.setShortcut('Alt+2')
        self.set_crossSection_action.setStatusTip('Set Cross-Section')
        self.set_crossSection_action.triggered.connect(self.getInputWidget().set_cross_section)

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

        #Acoustic Model Setup
        self.set_fluid_action = QAction('&Set Fluid', self)        
        self.set_fluid_action.setShortcut('Ctrl+Alt+1')
        self.set_fluid_action.setStatusTip('Set Fluid')
        self.set_fluid_action.triggered.connect(self.getInputWidget().set_fluid)

        self.setAcousticPressure_action = QAction('&Set Acoustic Pressure', self)        
        self.setAcousticPressure_action.setShortcut('Ctrl+Alt+2')
        self.setAcousticPressure_action.setStatusTip('Set Acoustic Pressure')
        self.setAcousticPressure_action.triggered.connect(self.getInputWidget().setAcousticPressure)

        self.setVolumeVelocity_action = QAction('&Set Volume Velocity', self)        
        self.setVolumeVelocity_action.setShortcut('Ctrl+Alt+3')
        self.setVolumeVelocity_action.setStatusTip('Set Volume Velocity')
        self.setVolumeVelocity_action.triggered.connect(self.getInputWidget().setVolumeVelocity)

        self.setSpecificImpedance_action = QAction('&Set Specific Impedance', self)        
        self.setSpecificImpedance_action.setShortcut('Ctrl+Alt+4')
        self.setSpecificImpedance_action.setStatusTip('Set Specific Impedance')
        self.setSpecificImpedance_action.triggered.connect(self.getInputWidget().setSpecificImpedance)

        self.set_radiation_impedance_action = QAction('&Set Radiation Impedance', self)        
        self.set_radiation_impedance_action.setShortcut('Ctrl+Alt+5')
        self.set_radiation_impedance_action.setStatusTip('Set Radiation Impedance')
        self.set_radiation_impedance_action.triggered.connect(self.getInputWidget().set_radiation_impedance)

        self.add_perforated_plate_action = QAction('&Add perforated plate', self)        
        self.add_perforated_plate_action.setShortcut('Ctrl+Alt+6')
        self.add_perforated_plate_action.setStatusTip('Add perforated plate')
        self.add_perforated_plate_action.triggered.connect(self.getInputWidget().add_perforated_plate)

        self.set_acoustic_element_length_correction_action = QAction('&Set Acoustic Element Length Correction', self)        
        self.set_acoustic_element_length_correction_action.setShortcut('Ctrl+Alt+7')
        self.set_acoustic_element_length_correction_action.setStatusTip('Set Acoustic Element Length Correction')
        self.set_acoustic_element_length_correction_action.triggered.connect(self.getInputWidget().set_acoustic_element_length_correction)

        #Model Informations
        self.structural_model_info_action = QAction('&Structural Model Info', self)        
        self.structural_model_info_action.setStatusTip('Structural Model Info')
        self.structural_model_info_action.triggered.connect(self.getInputWidget().structural_model_info)

        self.acoustic_model_info_action = QAction('&Acoustic Model Info', self)        
        self.acoustic_model_info_action.setStatusTip('Acoustic Model Info')
        self.acoustic_model_info_action.triggered.connect(self.getInputWidget().acoustic_model_info)

        #Analysis
        self.selectAnalysisType_action = QAction('&Select Analysis Type', self)        
        self.selectAnalysisType_action.setShortcut('Alt+Q')
        self.selectAnalysisType_action.setStatusTip('Select Analysis Type')
        self.selectAnalysisType_action.triggered.connect(self.getInputWidget().analysisTypeInput)
        
        self.analysisSetup_action = QAction('&Analysis Setup', self)        
        self.analysisSetup_action.setShortcut('Alt+W')
        self.analysisSetup_action.setStatusTip('Analysis Setup')
        self.analysisSetup_action.triggered.connect(self.getInputWidget().analysisSetup)

        self.selectOutput_action = QAction('&Select the Outputs Results', self)        
        self.selectOutput_action.setShortcut('Alt+E')
        self.selectOutput_action.setStatusTip('Select the Outputs Results')
        self.selectOutput_action.triggered.connect(self.getInputWidget().analysisOutputResults)

        self.runAnalysis_action = QAction('&Run Analysis', self)        
        self.runAnalysis_action.setShortcut('F5')
        self.runAnalysis_action.setStatusTip('Run Analysis')
        self.runAnalysis_action.triggered.connect(self.getInputWidget().runAnalysis)

        #Results Viewer
        self.plotStructuralModeShapes_action = QAction('&Plot Structural Mode Shapes', self)        
        self.plotStructuralModeShapes_action.setShortcut('Ctrl+Q')
        self.plotStructuralModeShapes_action.setStatusTip('Plot Structural Mode Shapes')
        self.plotStructuralModeShapes_action.triggered.connect(self.getInputWidget().plotStructuralModeShapes)

        self.plotStructuralHarmonicResponse_action = QAction('&Plot Structural Harmonic Response', self)        
        self.plotStructuralHarmonicResponse_action.setShortcut('Ctrl+W')
        self.plotStructuralHarmonicResponse_action.setStatusTip('Plot Structural Harmonic Response')
        self.plotStructuralHarmonicResponse_action.triggered.connect(self.getInputWidget().plotStructuralHarmonicResponse)

        self.plotAcousticHarmonicResponse_action = QAction('&Plot Acoustic Harmonic Response', self)        
        self.plotAcousticHarmonicResponse_action.setShortcut('Ctrl+E')
        self.plotAcousticHarmonicResponse_action.setStatusTip('Plot Acoustic Harmonic Response')
        self.plotAcousticHarmonicResponse_action.triggered.connect(self.getInputWidget().plotAcousticHarmonicResponse)

        self.plotSressField_action = QAction('&Plot Stress Field', self)        
        self.plotSressField_action.setShortcut('Ctrl+R')
        self.plotSressField_action.setStatusTip('Plot Stress Field')
        self.plotSressField_action.triggered.connect(self.getInputWidget().plotStressField)

        self.plotStructuralFrequencyResponse = QAction('&Plot Structural Frequency Response', self)        
        self.plotStructuralFrequencyResponse.setShortcut('Ctrl+T')
        self.plotStructuralFrequencyResponse.setStatusTip('Plot Structural Frequency Response')
        self.plotStructuralFrequencyResponse.triggered.connect(self.getInputWidget().plotStructuralFrequencyResponse)

        self.plotAcousticFrequencyResponse = QAction('&Plot Acoustic Frequency Response', self)        
        self.plotAcousticFrequencyResponse.setShortcut('Ctrl+U')
        self.plotAcousticFrequencyResponse.setStatusTip('Plot Acoustic Frequency Response')
        self.plotAcousticFrequencyResponse.triggered.connect(self.getInputWidget().plotAcousticFrequencyResponse)

        self.plot_TL_NR = QAction('&Plot Transmission Loss or Attenuation', self)        
        self.plot_TL_NR.setShortcut('Ctrl+V')
        self.plot_TL_NR.setStatusTip('Plot Transmission Loss or Attenuation')
        self.plot_TL_NR.triggered.connect(self.getInputWidget().plot_TL_NR)

        self.plot_reactions = QAction('&Plot Reactions to the Fixed DOFs or Ground', self)        
        self.plot_reactions.setShortcut('Ctrl+W')
        self.plot_reactions.setStatusTip('Plot Reactions')
        self.plot_reactions.triggered.connect(self.getInputWidget().plot_reactions)

    def _create_menu_bar(self):
        menuBar = self.menuBar()

        projectMenu = menuBar.addMenu('&Project')
        graphicMenu = menuBar.addMenu('&Graphic')
        modelSetup = menuBar.addMenu('&Model Setup')
        model_info = menuBar.addMenu('&Model Info')
        analysisMenu = menuBar.addMenu('&Analysis')
        resultsViewerMenu = menuBar.addMenu('&Results Viewer')
        helpMenu = menuBar.addMenu("&Help")

        projectMenu.addAction(self.new_action)
        projectMenu.addAction(self.import_action)
        projectMenu.addAction(self.saveAsPng_action)
        projectMenu.addAction(self.exit_action)

        graphicMenu.addAction(self.entities_action)
        graphicMenu.addAction(self.entities_action_radius)
        graphicMenu.addAction(self.points_action)
        graphicMenu.addAction(self.elements_action)

        modelSetup.addAction(self.setElementType_action)
        modelSetup.addAction(self.set_material_action)
        modelSetup.addAction(self.set_crossSection_action)
        modelSetup.addAction(self.setDOF_action)
        modelSetup.addAction(self.setForce_action)
        modelSetup.addAction(self.setMass_action)

        modelSetup.addAction(self.set_fluid_action)
        modelSetup.addAction(self.setAcousticPressure_action)
        modelSetup.addAction(self.setVolumeVelocity_action)
        modelSetup.addAction(self.setSpecificImpedance_action)
        modelSetup.addAction(self.set_radiation_impedance_action)
        modelSetup.addAction(self.add_perforated_plate_action)
        modelSetup.addAction(self.set_acoustic_element_length_correction_action)

        model_info.addAction(self.structural_model_info_action)
        model_info.addAction(self.acoustic_model_info_action)

        analysisMenu.addAction(self.selectAnalysisType_action)
        analysisMenu.addAction(self.analysisSetup_action)
        analysisMenu.addAction(self.selectOutput_action)
        analysisMenu.addAction(self.runAnalysis_action)

        resultsViewerMenu.addAction(self.plotStructuralModeShapes_action)
        resultsViewerMenu.addAction(self.plotStructuralHarmonicResponse_action)
        resultsViewerMenu.addAction(self.plotAcousticHarmonicResponse_action)
        resultsViewerMenu.addAction(self.plotSressField_action)
        resultsViewerMenu.addAction(self.plotStructuralFrequencyResponse)
        resultsViewerMenu.addAction(self.plotAcousticFrequencyResponse)
        resultsViewerMenu.addAction(self.plot_TL_NR)
        resultsViewerMenu.addAction(self.plot_reactions)

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
        working_area.setSizes([100,400])

    def new_call(self):
        if self.inputWidget.new_project():
            self.reset_info()
            self._change_window_title(self.project.get_project_name())
            self.draw()

    def import_call(self):
        loaded = self.inputWidget.loadProject()
        if loaded:
            self._change_window_title(self.project.get_project_name())
            self.draw()

    def savePNG_call(self):
        userPath = expanduser('~')
        project_path = "{}\\OpenPulse\\Projects".format(userPath)
        if not exists(project_path):
            project_path = ""
        path, _type = QFileDialog.getSaveFileName(None, 'Save file', project_path, 'PNG (*.png)')
        if path != "":
            self.getOPVWidget().savePNG(path)

    def reset_info(self):
        return
        self.opv_widget.reset_info()

    def plot_entities(self):
        self.opv_widget.plotEntities()
        self.opv_widget.changePlotToEntities()

    def plot_entities_radius(self):
        self.opv_widget.plotEntities(True)
        self.opv_widget.changePlotToEntities()

    def plot_elements(self):
        self.opv_widget.changePlotToElements()

    def plot_points(self):
        self.opv_widget.changePlotToPoints()

    def draw(self):
        self.opv_widget.plotEntities()
        self.opv_widget.plotElements()
        self.opv_widget.plotPoints()
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