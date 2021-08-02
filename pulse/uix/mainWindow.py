from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5 import QtCore
from PyQt5.QtWidgets import QAction, QToolBar, QSplitter, QFileDialog, QMessageBox, QMainWindow, QMenu

from pulse.uix.menu.Menu import Menu
from pulse.uix.inputUi import InputUi
from pulse.uix.opvUi import OPVUi
from pulse.project import Project
from pulse.uix.config import Config
from pulse.interface.opvRenderer import ViewOptions, SelectOptions

import sys
from os.path import expanduser, basename, exists, dirname
from pathlib import Path
import numpy as np

from pulse.uix.menu import *


class CustomQMenu(QMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mouseReleaseFunc = kwargs.get("mouseReleaseFunc", lambda *args, **kwargs:())

    def mouseReleaseEvent(self, *args, **kwargs):
        super().mouseReleaseEvent(*args, **kwargs)
        self.mouseReleaseFunc()


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)

        self.config = Config()
        self.project = Project()
        self.menuWidget = Menu(self)

        self._loadIcons()
        self._config()
        self._createBasicLayout()
        self._createActions()
        self._createMenuBar()
        self._createToolBar()
        self.show()
        self.loadRecentProject()

    def _loadIcons(self):
        icons_path = 'data\\icons\\'
        self.pulse_icon = QIcon(icons_path + 'pulse.png')
        self.new_icon = QIcon(icons_path + 'add.png')
        self.open_icon = QIcon(icons_path + 'upload.png')
        self.reset_icon = QIcon(icons_path + 'refresh.png')
        self.saveImage_icon = QIcon(icons_path + 'save_image.png')
        self.exit_icon = QIcon(icons_path + 'exit.png')
        
    def _config(self):
        self.setMinimumSize(QSize(800, 600))
        self.showMaximized()
        self.setWindowIcon(self.pulse_icon)
        self.changeWindowTitle()

    def changeWindowTitle(self, msg = ""):
        title = "OpenPulse"
        if (msg != ""):
            title += " - " + msg
        self.setWindowTitle(title)

    def _createActions(self):
        # File
        self.new_action = QAction(self.new_icon, '&New Project', self)        
        self.new_action.setShortcut('Ctrl+N')
        self.new_action.setStatusTip('New Project')
        self.new_action.triggered.connect(self.newProject_call)

        self.import_action = QAction(self.open_icon, '&Import Project', self)       
        self.import_action.setShortcut('Ctrl+O')
        self.import_action.setStatusTip('Import Project')
        self.import_action.triggered.connect(lambda: self.importProject_call())

        self.saveAsPng_action = QAction(self.saveImage_icon, '&Save as PNG', self)       
        self.saveAsPng_action.setShortcut('Ctrl+S')
        self.saveAsPng_action.setStatusTip('Save as PNG')
        self.saveAsPng_action.triggered.connect(self.savePNG_call)

        self.reset_action = QAction(self.reset_icon, '&Reset Project', self)       
        self.reset_action.setShortcut('Ctrl+Sift+R')
        self.reset_action.setStatusTip('Reset Project')
        self.reset_action.triggered.connect(lambda: self.resetProject_call())

        self.exit_action = QAction(self.exit_icon, '&Exit', self)        
        self.exit_action.setShortcut('Ctrl+Shift+Q')
        self.exit_action.setStatusTip('Exit application')
        self.exit_action.triggered.connect(self.close)

        # Help
        self.help_action = QAction('&Help', self)        
        self.help_action.setStatusTip('Help')
        self.help_action.setShortcut('F1')

        # Graphics
        self.entities_action = QAction('&Entity', self)        
        self.entities_action.setShortcut('Ctrl+1')
        self.entities_action.setStatusTip('Plot Entities')
        self.entities_action.triggered.connect(self.plot_entities)

        self.entities_action_radius = QAction('&Entity with Cross-section', self)        
        self.entities_action_radius.setShortcut('Ctrl+2')
        self.entities_action_radius.setStatusTip('Plot Entities with Cross-section')
        self.entities_action_radius.triggered.connect(self.plot_entities_with_cross_section)

        self.mesh_action = QAction('&Mesh', self)        
        self.mesh_action.setShortcut('Ctrl+3')
        self.mesh_action.setStatusTip('Plot Mesh')
        self.mesh_action.triggered.connect(self.plot_mesh)

        self.section_action = QAction('&Plot Cross-section', self)
        self.section_action.setShortcut('Ctrl+4')
        self.section_action.setStatusTip('Plot Cross-section')
        self.section_action.triggered.connect(self.getInputWidget().plot_cross_section)

        # Structural Model Setup
        self.set_material_action = QAction('&Set Material', self)        
        self.set_material_action.setShortcut('Alt+1')
        self.set_material_action.setStatusTip('Set Material')
        self.set_material_action.triggered.connect(self.getInputWidget().set_material)

        self.set_crossSection_action = QAction('&Set Cross-Section', self)        
        self.set_crossSection_action.setShortcut('Alt+2')
        self.set_crossSection_action.setStatusTip('Set Cross-Section')
        self.set_crossSection_action.triggered.connect(self.getInputWidget().set_cross_section)

        self.setStructuralElementType_action = QAction('&Set Structural Element Type', self)        
        self.setStructuralElementType_action.setShortcut('Alt+3')
        self.setStructuralElementType_action.setStatusTip('Set Structural Element Type')
        self.setStructuralElementType_action.triggered.connect(self.getInputWidget().setStructuralElementType)

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

        self.setcappedEnd_action = QAction('&Set Capped End', self)        
        self.setcappedEnd_action.setShortcut('Alt+7')
        self.setcappedEnd_action.setStatusTip('Set Capped End')
        self.setcappedEnd_action.triggered.connect(self.getInputWidget().setcappedEnd)

        self.stressStiffening_action = QAction('&Set Strees Stiffening', self)        
        # self.stressStiffening_action.setShortcut('Alt+7')
        self.stressStiffening_action.setStatusTip('Set Strees Stiffening')
        self.stressStiffening_action.triggered.connect(self.getInputWidget().set_stress_stress_stiffening)

        self.nodalLinks_action = QAction('&Add Elastic Nodal Links', self)        
        # self.nodalLinks_action.setShortcut('Alt+7')
        self.nodalLinks_action.setStatusTip('Add Elastic Nodal Links')
        self.nodalLinks_action.triggered.connect(self.getInputWidget().add_elastic_nodal_links)

        # Acoustic Model Setup
        self.setAcousticElementType_action = QAction('&Set Acoustic Element Type', self)        
        self.setAcousticElementType_action.setShortcut('Ctrl+Alt+1')
        self.setAcousticElementType_action.setStatusTip('Set Acoustic Element Type')
        self.setAcousticElementType_action.triggered.connect(self.getInputWidget().set_acoustic_element_type)

        self.set_fluid_action = QAction('&Set Fluid', self)        
        self.set_fluid_action.setShortcut('Ctrl+Alt+2')
        self.set_fluid_action.setStatusTip('Set Fluid')
        self.set_fluid_action.triggered.connect(self.getInputWidget().set_fluid)

        self.setAcousticPressure_action = QAction('&Set Acoustic Pressure', self)        
        self.setAcousticPressure_action.setShortcut('Ctrl+Alt+3')
        self.setAcousticPressure_action.setStatusTip('Set Acoustic Pressure')
        self.setAcousticPressure_action.triggered.connect(self.getInputWidget().setAcousticPressure)

        self.setVolumeVelocity_action = QAction('&Set Volume Velocity', self)        
        self.setVolumeVelocity_action.setShortcut('Ctrl+Alt+4')
        self.setVolumeVelocity_action.setStatusTip('Set Volume Velocity')
        self.setVolumeVelocity_action.triggered.connect(self.getInputWidget().setVolumeVelocity)

        self.setSpecificImpedance_action = QAction('&Set Specific Impedance', self)        
        self.setSpecificImpedance_action.setShortcut('Ctrl+Alt+5')
        self.setSpecificImpedance_action.setStatusTip('Set Specific Impedance')
        self.setSpecificImpedance_action.triggered.connect(self.getInputWidget().setSpecificImpedance)

        self.set_radiation_impedance_action = QAction('&Set Radiation Impedance', self)        
        self.set_radiation_impedance_action.setShortcut('Ctrl+Alt+6')
        self.set_radiation_impedance_action.setStatusTip('Set Radiation Impedance')
        self.set_radiation_impedance_action.triggered.connect(self.getInputWidget().set_radiation_impedance)

        self.add_perforated_plate_action = QAction('&Add Perforated Plate', self)        
        self.add_perforated_plate_action.setShortcut('Ctrl+Alt+7')
        self.add_perforated_plate_action.setStatusTip('Add Perforated Plate')
        self.add_perforated_plate_action.triggered.connect(self.getInputWidget().add_perforated_plate)

        self.set_acoustic_element_length_correction_action = QAction('&Set Acoustic Element Length Correction', self)        
        self.set_acoustic_element_length_correction_action.setShortcut('Ctrl+Alt+8')
        self.set_acoustic_element_length_correction_action.setStatusTip('Set Acoustic Element Length Correction')
        self.set_acoustic_element_length_correction_action.triggered.connect(self.getInputWidget().set_acoustic_element_length_correction)

        self.add_compressor_excitation_action = QAction('&Add Compressor Excitation', self)        
        # self.add_compressor_excitation_action.setShortcut('Ctrl+Alt+9')
        self.add_compressor_excitation_action.setStatusTip('Add Compressor Excitation')
        self.add_compressor_excitation_action.triggered.connect(self.getInputWidget().add_compressor_excitation)

        # Structural and Acoustic Model Informations
        self.structural_model_info_action = QAction('&Structural Model Info', self)    
        self.structural_model_info_action.setShortcut('F3')    
        self.structural_model_info_action.setStatusTip('Structural Model Info')
        self.structural_model_info_action.triggered.connect(self.getInputWidget().structural_model_info)

        self.acoustic_model_info_action = QAction('&Acoustic Model Info', self)      
        self.acoustic_model_info_action.setShortcut('F4')  
        self.acoustic_model_info_action.setStatusTip('Acoustic Model Info')
        self.acoustic_model_info_action.triggered.connect(self.getInputWidget().acoustic_model_info)

        # Analysis
        self.selectAnalysisType_action = QAction('&Select Analysis Type', self)        
        self.selectAnalysisType_action.setShortcut('Alt+Q')
        self.selectAnalysisType_action.setStatusTip('Select Analysis Type')
        self.selectAnalysisType_action.triggered.connect(self.getInputWidget().analysisTypeInput)
        
        self.analysisSetup_action = QAction('&Analysis Setup', self)        
        self.analysisSetup_action.setShortcut('Alt+W')
        self.analysisSetup_action.setStatusTip('Analysis Setup')
        self.analysisSetup_action.triggered.connect(self.getInputWidget().analysisSetup)

        self.runAnalysis_action = QAction('&Run Analysis', self)        
        # self.runAnalysis_action.setShortcut('F5')
        self.runAnalysis_action.setStatusTip('Run Analysis')
        self.runAnalysis_action.triggered.connect(self.getInputWidget().runAnalysis)
 
        # Results Viewer
        self.playPauseAnimaton_action = QAction('&Play/Pause Animation', self)
        self.playPauseAnimaton_action.setShortcut('Space')
        self.playPauseAnimaton_action.setStatusTip('Play/Pause Animation')
        self.playPauseAnimaton_action.triggered.connect(self.opv_widget.opvAnalisysRenderer.tooglePlayPauseAnimation)

        self.plotStructuralModeShapes_action = QAction('&Plot Structural Mode Shapes', self)        
        self.plotStructuralModeShapes_action.setShortcut('Ctrl+Q')
        self.plotStructuralModeShapes_action.setStatusTip('Plot Structural Mode Shapes')
        self.plotStructuralModeShapes_action.triggered.connect(self.getInputWidget().plotStructuralModeShapes)

        self.plotDisplacementField_action = QAction('&Plot Displacement Field', self)        
        self.plotDisplacementField_action.setShortcut('Ctrl+W')
        self.plotDisplacementField_action.setStatusTip('Plot Displacement Field')
        self.plotDisplacementField_action.triggered.connect(self.getInputWidget().plotDisplacementField)

        self.plotStructuralFrequencyResponse = QAction('&Plot Structural Frequency Response', self)        
        self.plotStructuralFrequencyResponse.setShortcut('Ctrl+T')
        self.plotStructuralFrequencyResponse.setStatusTip('Plot Structural Frequency Response')
        self.plotStructuralFrequencyResponse.triggered.connect(self.getInputWidget().plotStructuralFrequencyResponse)

        self.plotReactionsFrequencyResponse = QAction('&Plot Reactions Frequency Response', self)        
        self.plotReactionsFrequencyResponse.setShortcut('Ctrl+W')
        self.plotReactionsFrequencyResponse.setStatusTip('Plot Reactions Frequency Response')
        self.plotReactionsFrequencyResponse.triggered.connect(self.getInputWidget().plotReactionsFrequencyResponse)

        self.plotSressField_action = QAction('&Plot Stress Field', self)        
        # self.plotSressField_action.setShortcut('Ctrl+R')
        self.plotSressField_action.setStatusTip('Plot Stress Field')
        self.plotSressField_action.triggered.connect(self.getInputWidget().plotStressField)

        self.plotSressFrequencyResponse_action = QAction('&Plot Stress Frequency Response', self)        
        # self.plotSressFrequencyResponse_action.setShortcut('Ctrl+R')
        self.plotSressFrequencyResponse_action.setStatusTip('Plot Stress Frequency Response')
        self.plotSressFrequencyResponse_action.triggered.connect(self.getInputWidget().plotStressFrequencyResponse)

        self.plotPressureField_action = QAction('&Plot Acoustic Pressure Field', self)        
        self.plotPressureField_action.setShortcut('Ctrl+E')
        self.plotPressureField_action.setStatusTip('Plot Acoustic Pressure Field')
        self.plotPressureField_action.triggered.connect(self.getInputWidget().plotAcousticPressureField)

        self.plotAcousticFrequencyResponse = QAction('&Plot Acoustic Frequency Response', self)        
        self.plotAcousticFrequencyResponse.setShortcut('Ctrl+U')
        self.plotAcousticFrequencyResponse.setStatusTip('Plot Acoustic Frequency Response')
        self.plotAcousticFrequencyResponse.triggered.connect(self.getInputWidget().plotAcousticFrequencyResponse)

        self.plot_TL_NR = QAction('&Plot Transmission Loss or Attenuation', self)        
        self.plot_TL_NR.setShortcut('Ctrl+V')
        self.plot_TL_NR.setStatusTip('Plot Transmission Loss or Attenuation')
        self.plot_TL_NR.triggered.connect(self.getInputWidget().plot_TL_NR)

    def _createRecentProjectsActions(self):
        self.importRecent_action = {}
        for value in self.config.recentProjects:
            import_action = QAction('&'+str(value) + "     "+str(self.config.recentProjects[value]), self)       
            import_action.setStatusTip(value)
            self.importRecent_action[value] = import_action
        try:
            temp = list(self.config.recentProjects.items())
            self.importRecent_action[temp[0][0]].triggered.connect(lambda: self.importRecentProject_call(temp[0][1]))
            self.importRecent_action[temp[1][0]].triggered.connect(lambda: self.importRecentProject_call(temp[1][1]))
            self.importRecent_action[temp[2][0]].triggered.connect(lambda: self.importRecentProject_call(temp[2][1]))
            self.importRecent_action[temp[3][0]].triggered.connect(lambda: self.importRecentProject_call(temp[3][1]))
            self.importRecent_action[temp[4][0]].triggered.connect(lambda: self.importRecentProject_call(temp[4][1]))
            self.importRecent_action[temp[5][0]].triggered.connect(lambda: self.importRecentProject_call(temp[5][1]))
            self.importRecent_action[temp[6][0]].triggered.connect(lambda: self.importRecentProject_call(temp[6][1]))
            self.importRecent_action[temp[7][0]].triggered.connect(lambda: self.importRecentProject_call(temp[7][1]))
            self.importRecent_action[temp[8][0]].triggered.connect(lambda: self.importRecentProject_call(temp[8][1]))
            self.importRecent_action[temp[9][0]].triggered.connect(lambda: self.importRecentProject_call(temp[9][1]))
        except Exception:
            pass

    def _createMenuRecentProjects(self):
        self.recentProjectsMenu = QMenu("Recents Projects", parent=self)
        for i in self.importRecent_action:
            self.recentProjectsMenu.addAction(self.importRecent_action[i])
    
    def _loadProjectMenu(self):
        self._createRecentProjectsActions()
        self._createMenuRecentProjects()
        self.projectMenu.clear()
        self.projectMenu.addAction(self.new_action)
        self.projectMenu.addAction(self.import_action)
        self.projectMenu.addMenu(self.recentProjectsMenu)
        self.projectMenu.addAction(self.saveAsPng_action)
        self.projectMenu.addAction(self.reset_action)
        self.projectMenu.addAction(self.exit_action)

    def _loadGraphicMenu(self):
        self.createCustomPlotMenu()

        self.graphicMenu.addAction(self.entities_action)
        self.graphicMenu.addAction(self.entities_action_radius)
        self.graphicMenu.addAction(self.mesh_action)
        self.graphicMenu.addMenu(self.customPlotMenu)
        self.graphicMenu.addAction(self.section_action)

    def _loadModelSetupMenu(self):
        self.structuralModelSetupMenu.addAction(self.setStructuralElementType_action)
        self.structuralModelSetupMenu.addAction(self.set_material_action)
        self.structuralModelSetupMenu.addAction(self.set_crossSection_action)
        self.structuralModelSetupMenu.addAction(self.setDOF_action)
        self.structuralModelSetupMenu.addAction(self.setForce_action)
        self.structuralModelSetupMenu.addAction(self.setMass_action)
        self.structuralModelSetupMenu.addAction(self.setcappedEnd_action)
        self.structuralModelSetupMenu.addAction(self.stressStiffening_action)
        self.structuralModelSetupMenu.addAction(self.nodalLinks_action)

        self.acousticModelSetupMenu.addAction(self.setAcousticElementType_action)
        self.acousticModelSetupMenu.addAction(self.set_fluid_action)
        self.acousticModelSetupMenu.addAction(self.setAcousticPressure_action)
        self.acousticModelSetupMenu.addAction(self.setVolumeVelocity_action)
        self.acousticModelSetupMenu.addAction(self.setSpecificImpedance_action)
        self.acousticModelSetupMenu.addAction(self.set_radiation_impedance_action)
        self.acousticModelSetupMenu.addAction(self.add_perforated_plate_action)
        self.acousticModelSetupMenu.addAction(self.set_acoustic_element_length_correction_action)
        self.acousticModelSetupMenu.addAction(self.add_compressor_excitation_action)

    def _loadModelInfoMenu(self):
        self.modelInfoMenu.addAction(self.structural_model_info_action)
        self.modelInfoMenu.addAction(self.acoustic_model_info_action)

    def _loadAnalysisMenu(self):
        self.analysisMenu.addAction(self.selectAnalysisType_action)
        self.analysisMenu.addAction(self.analysisSetup_action)
        self.analysisMenu.addAction(self.runAnalysis_action)

    def _loadResultsViewerMenu(self):
        self.resultsViewerMenu.addAction(self.plotStructuralModeShapes_action)
        self.resultsViewerMenu.addAction(self.plotDisplacementField_action)
        self.resultsViewerMenu.addAction(self.plotStructuralFrequencyResponse)
        self.resultsViewerMenu.addAction(self.plotReactionsFrequencyResponse)
        self.resultsViewerMenu.addAction(self.plotSressField_action)
        self.resultsViewerMenu.addAction(self.plotSressFrequencyResponse_action)
        self.resultsViewerMenu.addAction(self.playPauseAnimaton_action)

        self.resultsViewerMenu.addAction(self.plotPressureField_action)
        self.resultsViewerMenu.addAction(self.plotAcousticFrequencyResponse)
        self.resultsViewerMenu.addAction(self.plot_TL_NR)

    def _loadHelpMenu(self):
        self.helpMenu.addAction(self.help_action)

    def createCustomPlotMenu(self):
        self.customPlotMenu = CustomQMenu('Custom Menu', parent=self)
        self.customPlotMenu.mouseReleaseFunc = self.custom_plot_parameters

        self.customPlotNodes = QAction('Plot Nodes', self, checkable=True)
        self.customPlotTubes = QAction('Plot Tubes', self, checkable=True)
        self.customPlotSymbols = QAction('Plot Symbols', self, checkable=True)

        self.customPlotMenu.addAction(self.customPlotNodes)
        self.customPlotMenu.addAction(self.customPlotTubes)
        self.customPlotMenu.addAction(self.customPlotSymbols)

    def _createMenuBar(self):
        menuBar = self.menuBar()

        self.projectMenu = menuBar.addMenu('&Project')
        self.graphicMenu = menuBar.addMenu('&Graphic')
        self.structuralModelSetupMenu = menuBar.addMenu('&Structural Model Setup')
        self.acousticModelSetupMenu = menuBar.addMenu('&Acoustic Model Setup')
        
        self.modelInfoMenu = menuBar.addMenu('&Model Info')
        self.analysisMenu = menuBar.addMenu('&Analysis')
        self.resultsViewerMenu = menuBar.addMenu('&Results Viewer')
        self.helpMenu = menuBar.addMenu("&Help")

        self._loadProjectMenu()
        self._loadGraphicMenu()
        self._loadModelSetupMenu()
        self._loadModelInfoMenu()
        self._loadAnalysisMenu()
        self._loadResultsViewerMenu()
        self._loadHelpMenu()

    def set_enable_menuBar(self, _bool):
        #
        self.graphicMenu.setEnabled(_bool)
        self.structuralModelSetupMenu.setEnabled(_bool)
        self.acousticModelSetupMenu.setEnabled(_bool)
        self.modelInfoMenu.setEnabled(_bool)
        self.analysisMenu.setEnabled(_bool)
        self.resultsViewerMenu.setEnabled(_bool)
        #
        self.saveAsPng_action.setEnabled(_bool) 
        self.reset_action.setEnabled(_bool) 

    def _createToolBar(self):
        self.toolbar = QToolBar("Enable Toolbar")
        self.toolbar.setIconSize(QSize(26,26))
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.new_action)
        self.toolbar.addAction(self.import_action)
        self.toolbar.addAction(self.reset_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.saveAsPng_action)

    def _createBasicLayout(self):
        self.menuWidget = Menu(self)
        self.opv_widget = OPVUi(self.project, self)
        self.inputWidget = InputUi(self.project, self)

        working_area = QSplitter(Qt.Horizontal)
        self.setCentralWidget(working_area)

        working_area.addWidget(self.menuWidget)
        working_area.addWidget(self.opv_widget)
        working_area.setSizes([100,400])

    def newProject_call(self):
        if self.inputWidget.new_project(self.config):
            self._loadProjectMenu()
            self.changeWindowTitle(self.project.get_project_name())
            self.draw()

    def importProject_call(self, path=None):
        if self.inputWidget.loadProject(self.config, path):
            self._loadProjectMenu()
            self.changeWindowTitle(self.project.get_project_name())
            self.draw()
    
    def resetProject_call(self):
        self.inputWidget.reset_project()
        return

    def importRecentProject_call(self, dir):
        self.importProject_call(dir)

    def loadRecentProject(self):
        if self.config.openLastProject and self.config.haveRecentProjects():
            self.importProject_call(self.config.getMostRecentProjectDir())
        else:
            if self.inputWidget.getStarted(self.config):
                self._loadProjectMenu()
                self.changeWindowTitle(self.project.get_project_name())
                self.draw()

    def savePNG_call(self):
        userPath = expanduser('~')
        project_path = "{}\\OpenPulse\\Projects".format(userPath)
        if not exists(project_path):
            project_path = ""
        path, _type = QFileDialog.getSaveFileName(None, 'Save file', project_path, 'PNG (*.png)')
        if path != "":
            self.getOPVWidget().savePNG(path)

    def plot_entities(self):
        self.opv_widget.changePlotToEntities()

    def plot_entities_with_cross_section(self):
        self.opv_widget.changePlotToEntitiesWithCrossSection()

    def plot_mesh(self):
        self.opv_widget.changePlotToMesh()
    
    def custom_plot_parameters(self, *args, **kwargs):
        transparent = self.customPlotNodes.isChecked() and self.customPlotTubes.isChecked()
        select_nodes = self.customPlotNodes.isChecked()

        viewOpt  = (ViewOptions.SHOW_LINES)
        viewOpt |= (ViewOptions.SHOW_NODES) if self.customPlotNodes.isChecked() else 0
        viewOpt |= (ViewOptions.SHOW_TUBES) if self.customPlotTubes.isChecked() else 0
        viewOpt |= (ViewOptions.SHOW_TRANSP) if transparent else 0

        if select_nodes:
            selectOpt = SelectOptions.SELECT_NODES | SelectOptions.SELECT_ELEMENTS
        else:
            selectOpt = SelectOptions.SELECT_ENTITIES

        self.opv_widget.changePlotToCustom(viewOpt, selectOpt)

    def draw(self):
        self.opv_widget.updatePlots()
        self.plot_entities_with_cross_section()

    def closeEvent(self, event):
        close = QMessageBox.question(
            self,
            "QUIT",
            "Are you sure you want to stop process?",
            QMessageBox.No | QMessageBox.Yes)
               
        if close == QMessageBox.Yes:
            sys.exit()
        else:
            event.ignore()

    def getInputWidget(self):
        return self.inputWidget

    def getMenuWidget(self):
        return self.menuWidget

    def getOPVWidget(self):
        return self.opv_widget

    def getProject(self):
        return self.project