import sys
from functools import partial
from os.path import expanduser, basename, exists, dirname

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QAction, QToolBar, QSplitter, QFileDialog, QMessageBox, QMainWindow, QMenu, QPushButton

from pulse.project import Project
from pulse.uix.opvUi import OPVUi
from pulse.uix.infoUi import InfoUi
from pulse.uix.config import Config
from pulse.uix.inputUi import InputUi

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.config = Config()
        self.project = Project()
        
        self._loadIcons()
        self._config()
        self._createBasicLayout()
        self._createActions()
        self._createMenuBar()
        self._createToolBar()
        self.show()
        self.loadRecentProject()

    def changeWindowTitle(self, msg = ""):
        title = ('OpenPulse - ' + msg) if msg else 'OpenPulse'
        self.setWindowTitle(title)

    def _loadIcons(self):
        icons_path = 'pulse\\interface\\icons\\'

        self.pulseIcon = QIcon(icons_path + 'pulse.png')
        self.newProjectIcon = QIcon(icons_path + 'new_file.png')
        self.loadProjectIcon = QIcon(icons_path + 'load_file.png')
        self.saveProjectIcon = QIcon(icons_path + 'save_classic.png')
        self.saveProjectAsIcon = QIcon(icons_path + 'save_as_classic.png')
        self.saveImageIcon = QIcon(icons_path + 'save_image.png')
        self.exitIcon = QIcon(icons_path + 'save_as_modern.png')

        self.plotEntityIcon = QIcon(icons_path + 'show_entities.png')
        self.plotSectionsIcon = QIcon(icons_path + 'show_sections.png')
        self.plotMeshIcon = QIcon(icons_path + 'show_mesh.png')

    def _config(self):
        self.setMinimumSize(QSize(800, 600))
        self.showMaximized()
        self.setWindowIcon(self.pulseIcon)
        self.changeWindowTitle()

    def _createBasicLayout(self):
        self.infoUi = InfoUi(self)
        self.opvUi = OPVUi(self.project, self)
        self.inputUi = InputUi(self.project, self)

        working_area = QSplitter(Qt.Horizontal)
        working_area.addWidget(self.infoUi)
        working_area.addWidget(self.opvUi)
        working_area.setSizes([100,400])
        self.setCentralWidget(working_area)

    def _createActions(self):
        self._createProjectActions()
        self._createGraphicActions()
        # self._createModelSetupActions()
        # self._createModelInfoActions()
        # self._createAnalysisActions()
        # self._createResultsViewerActions()
        self._createHelpActions()

    def _createMenuBar(self):
        self._createProjectMenu()
        self._createGraphicMenu()
        # self._createModelSetupMenu()
        # self._createModelInfoMenu()
        # self._createAnalysisMenu()
        # self._createResultsViewerMenu()
        self._createHelpMenu()

    def _createToolBar(self):
        self.toolbar = QToolBar("Enable Toolbar")
        self.toolbar.setIconSize(QSize(26,26))
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.newProjectAction)
        self.toolbar.addAction(self.loadProjectAction)
        self.toolbar.addAction(self.saveProjectAction)
        self.toolbar.addAction(self.saveProjectAsAction)
        self.toolbar.addAction(self.saveImageAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.plotEntityAction)
        self.toolbar.addAction(self.plotSectionsAction)
        self.toolbar.addAction(self.plotMeshAction)

    # ACTIONS
    def _createProjectActions(self):
        self.newProjectAction = QAction(self.newProjectIcon, 'New Project', self)        
        self.newProjectAction.setShortcut('Ctrl + N')
        self.newProjectAction.triggered.connect(self.newProjectFunc)

        self.loadProjectAction = QAction(self.loadProjectIcon, 'Load Project', self)       
        self.loadProjectAction.setShortcut('Ctrl + O')
        self.loadProjectAction.triggered.connect(self.loadProjectFunc)

        self.saveProjectAction = QAction(self.saveProjectIcon, 'Save Project', self)       
        self.saveProjectAction.setShortcut('Ctrl + S')
        self.saveProjectAction.triggered.connect(self.saveProjectFunc)

        self.saveProjectAsAction = QAction(self.saveProjectAsIcon, 'Save Project As', self)       
        self.saveProjectAsAction.setShortcut('Ctrl + Shift + S')
        self.saveProjectAsAction.triggered.connect(self.saveProjectAsFunc)

        self.saveImageAction = QAction(self.saveImageIcon, 'Save Image', self)
        self.saveImageAction.setShortcut('Ctrl + E')
        self.saveImageAction.triggered.connect(self.saveImageFunc)

        self.exitAction = QAction(self.exitIcon, 'Exit', self)        
        self.exitAction.setShortcut('Ctrl + Q')
        self.exitAction.triggered.connect(self.close)
    
    def _createGraphicActions(self):
        self.plotEntityAction = QAction(self.plotEntityIcon, 'Plot Entity')
        self.plotEntityAction.setShortcut('Ctrl + 1')
        self.plotEntityAction.triggered.connect(self.plotEntityFunc)

        self.plotSectionsAction = QAction(self.plotSectionsIcon, 'Plot Entity With Sections')
        self.plotSectionsAction.setShortcut('Ctrl + 2')
        self.plotSectionsAction.triggered.connect(self.plotSectionsFunc)

        self.plotMeshAction = QAction(self.plotMeshIcon, 'Plot Mesh')
        self.plotMeshAction.setShortcut('Ctrl + 3')
        self.plotMeshAction.triggered.connect(self.plotMeshFunc)

    def _createModelSetupActions(self):
        self.setMaterialAction = QAction('Set Material', self)        
        self.setMaterialAction.setShortcut('Alt + 1')
        self.setMaterialAction.triggered.connect(self.getInputWidget().set_material)

        self.setCrossSectionAction = QAction('Set Cross-Section', self)        
        self.setCrossSectionAction.setShortcut('Alt + 2')
        self.setCrossSectionAction.triggered.connect(self.getInputWidget().set_cross_section)

        self.setElementTypeAction = QAction('Set Element Type', self)        
        self.setElementTypeAction.setShortcut('Alt + 3')
        self.setElementTypeAction.triggered.connect(self.getInputWidget().setElementType)

        self.setDOFAction = QAction('Set Prescribed DOFs', self)        
        self.setDOFAction.setShortcut('Alt + 4')
        self.setDOFAction.triggered.connect(self.getInputWidget().setDOF)

        self.setForceAction = QAction('Set Nodal Loads', self)        
        self.setForceAction.setShortcut('Alt + 5')
        self.setForceAction.triggered.connect(self.getInputWidget().setNodalLoads)

        self.setMassAction = QAction('Add: Mass / Spring / Damper', self)        
        self.setMassAction.setShortcut('Alt + 6')
        self.setMassAction.triggered.connect(self.getInputWidget().addMassSpringDamper)

        self.setcappedEndAction = QAction('Set capped End', self)        
        self.setcappedEndAction.setShortcut('Alt + 7')
        self.setcappedEndAction.triggered.connect(self.getInputWidget().setcappedEnd)

        self.setFluidAction = QAction('Set Fluid', self)        
        self.setFluidAction.setShortcut('Ctrl + Alt + 1')
        self.setFluidAction.triggered.connect(self.getInputWidget().set_fluid)

        self.setAcousticPressureAction = QAction('Set Acoustic Pressure', self)        
        self.setAcousticPressureAction.setShortcut('Ctrl + Alt + 2')
        self.setAcousticPressureAction.triggered.connect(self.getInputWidget().setAcousticPressure)

        self.setVolumeVelocityAction = QAction('Set Volume Velocity', self)        
        self.setVolumeVelocityAction.setShortcut('Ctrl + Alt + 3')
        self.setVolumeVelocityAction.triggered.connect(self.getInputWidget().setVolumeVelocity)

        self.setSpecificImpedanceAction = QAction('Set Specific Impedance', self)        
        self.setSpecificImpedanceAction.setShortcut('Ctrl + Alt + 4')
        self.setSpecificImpedanceAction.triggered.connect(self.getInputWidget().setSpecificImpedance)

        self.setRadiationImpedanceAction = QAction('Set Radiation Impedance', self)        
        self.setRadiationImpedanceAction.setShortcut('Ctrl + Alt + 5')
        self.setRadiationImpedanceAction.triggered.connect(self.getInputWidget().set_radiation_impedance)

        self.addPerforatedPlateAction = QAction('Add perforated plate', self)        
        self.addPerforatedPlateAction.setShortcut('Ctrl + Alt + 6')
        self.addPerforatedPlateAction.triggered.connect(self.getInputWidget().add_perforated_plate)

        self.setAcousticElementLengthCorrectionAction = QAction('Set Acoustic Element Length Correction', self)        
        self.setAcousticElementLengthCorrectionAction.setShortcut('Ctrl + Alt + 7')
        self.setAcousticElementLengthCorrectionAction.triggered.connect(self.getInputWidget().set_acoustic_element_length_correction)
    
    def _createModelInfoActions(self):
        self.structuralModelInfoAction = QAction('Structural Model Info', self)    
        self.structuralModelInfoAction.setShortcut('F3')
        self.structuralModelInfoAction.triggered.connect(self.getInputWidget().structural_model_info)

        self.acousticModelInfoAction = QAction('Acoustic Model Info', self)      
        self.acousticModelInfoAction.setShortcut('F4')
        self.acousticModelInfoAction.triggered.connect(self.getInputWidget().acoustic_model_info)
    
    def _createAnalysisActions(self):
        self.selectAnalysisTypeAction = QAction('Select Analysis Type', self)        
        self.selectAnalysisTypeAction.setShortcut('Alt + Q')
        self.selectAnalysisTypeAction.triggered.connect(self.getInputWidget().analysisTypeInput)
        
        self.analysisSetupAction = QAction('Analysis Setup', self)        
        self.analysisSetupAction.setShortcut('Alt + W')
        self.analysisSetupAction.triggered.connect(self.getInputWidget().analysisSetup)

        self.runAnalysisAction = QAction('Run Analysis', self)
        self.runAnalysisAction.triggered.connect(self.getInputWidget().runAnalysis)
    
    def _createResultsViewerActions(self):
        self.plotStructuralModeShapesAction = QAction('Plot Structural Mode Shapes', self)
        self.plotStructuralModeShapesAction.triggered.connect(self.getInputWidget().plotStructuralModeShapes)

        self.plotDisplacementFieldAction = QAction('Plot Displacement Field', self) 
        self.plotDisplacementFieldAction.triggered.connect(self.getInputWidget().plotDisplacementField)

        self.plotStructuralFrequencyResponse = QAction('Plot Structural Frequency Response', self) 
        self.plotStructuralFrequencyResponse.triggered.connect(self.getInputWidget().plotStructuralFrequencyResponse)

        self.plotReactionsFrequencyResponse = QAction('&Plot Reactions Frequency Response', self)   
        self.plotReactionsFrequencyResponse.triggered.connect(self.getInputWidget().plotReactionsFrequencyResponse)

        self.plotSressFieldAction = QAction('Plot Stress Field', self)
        self.plotSressFieldAction.triggered.connect(self.getInputWidget().plotStressField)

        self.plotSressFrequencyResponseAction = QAction('Plot Stress Frequency Response', self)     
        self.plotSressFrequencyResponseAction.triggered.connect(self.getInputWidget().plotStressFrequencyResponse)

        self.plotPressureFieldAction = QAction('Plot Acoustic Pressure Field', self)
        self.plotPressureFieldAction.triggered.connect(self.getInputWidget().plotAcousticPressureField)

        self.plotAcousticFrequencyResponse = QAction('Plot Acoustic Frequency Response', self)
        self.plotAcousticFrequencyResponse.triggered.connect(self.getInputWidget().plotAcousticFrequencyResponse)

        self.plotTransmitionLossAttenuation = QAction('Plot Transmission Loss or Attenuation', self)
        self.plotTransmitionLossAttenuation.triggered.connect(self.getInputWidget().plotTransmitionLossAttenuation)
    
    def _createHelpActions(self):
        self.helpAction = QAction('Help', self)
        self.helpAction.setShortcut('F1')
        self.helpAction.triggered.connect(self.helpFunc)

        self.aboutAction = QAction('About Us')
        self.aboutAction.triggered.connect(self.aboutFunc)

        self.autorsAction = QAction('Autors', self)
        self.autorsAction.triggered.connect(self.autorsFunc)

        self.licenceAction = QAction('Licence', self)
        self.licenceAction.triggered.connect(self.licenceFunc)
    # END ACTIONS
    

    # MENUS
    def _createProjectMenu(self):
        self.projectMenu = self.menuBar().addMenu('Project')
        self._createRecentProjectsMenu()
        self.projectMenu.addAction(self.newProjectAction)
        self.projectMenu.addAction(self.loadProjectAction)
        self.projectMenu.addMenu(self.recentProjectsMenu)
        self.projectMenu.addAction(self.saveProjectAction)
        self.projectMenu.addAction(self.saveProjectAsAction)
        self.projectMenu.addSeparator()
        self.projectMenu.addAction(self.saveImageAction)
        self.projectMenu.addSeparator()
        self.projectMenu.addAction(self.exitAction)
    
    def _createGraphicMenu(self):
        self.graphicMenu = self.menuBar().addMenu('Graphic')
        self.graphicMenu.addAction(self.plotEntityAction)
        self.graphicMenu.addAction(self.plotSectionsAction)
        self.graphicMenu.addAction(self.plotMeshAction)
    
    def _createModelSetupMenu(self):
        self.modelSetupMenu = self.menuBar().addMenu('Model Setup')
        self.modelSetupMenu.addAction(self.setElementTypeAction)
        self.modelSetupMenu.addAction(self.setMaterialAction)
        self.modelSetupMenu.addAction(self.setCrossSectionAction)
        self.modelSetupMenu.addAction(self.setDOFAction)
        self.modelSetupMenu.addAction(self.setForceAction)
        self.modelSetupMenu.addAction(self.setMassAction)
        self.modelSetupMenu.addAction(self.setcappedEndAction)
        self.modelSetupMenu.addSeparator()
        self.modelSetupMenu.addAction(self.setFluidAction)
        self.modelSetupMenu.addAction(self.setAcousticPressureAction)
        self.modelSetupMenu.addAction(self.setVolumeVelocityAction)
        self.modelSetupMenu.addAction(self.setSpecificImpedanceAction)
        self.modelSetupMenu.addAction(self.setRadiationImpedanceAction)
        self.modelSetupMenu.addAction(self.addPerforatedPlateAction)
        self.modelSetupMenu.addAction(self.setAcousticElementLengthCorrectionAction)
    
    def _createModelInfoMenu(self):
        self.modelInfoMenu = self.menuBar().addMenu('Model Info')
        self.modelInfoMenu.addAction(self.structuralModelInfoAction)
        self.modelInfoMenu.addAction(self.acousticModelInfoAction)
    
    def _createAnalysisMenu(self):
        self.analysisMenu = self.menuBar().addMenu('Analysis')
        self.analysisMenu.addAction(self.selectAnalysisTypeAction)
        self.analysisMenu.addAction(self.analysisSetupAction)
        self.analysisMenu.addAction(self.runAnalysisAction)

    def _createResultsViewerMenu(self):
        self.resultsViewerMenu = self.menuBar().addMenu('Results Viewer')
        self.resultsViewerMenu.addAction(self.plotStructuralModeShapesAction)
        self.resultsViewerMenu.addAction(self.plotDisplacementFieldAction)
        self.resultsViewerMenu.addAction(self.plotStructuralFrequencyResponse)
        self.resultsViewerMenu.addAction(self.plotReactionsFrequencyResponse)
        self.resultsViewerMenu.addAction(self.plotSressFieldAction)
        self.resultsViewerMenu.addAction(self.plotSressFrequencyResponseAction)
        self.resultsViewerMenu.addSeparator()
        self.resultsViewerMenu.addAction(self.plotPressureField_action)
        self.resultsViewerMenu.addAction(self.plotAcousticFrequencyResponse)
        self.resultsViewerMenu.addAction(self.plotTransmitionLossAttenuation)
    
    def _createHelpMenu(self):
        self.helpMenu = self.menuBar().addMenu('Help')
        self.helpMenu.addAction(self.helpAction)
        self.helpMenu.addAction(self.aboutAction)
        self.helpMenu.addAction(self.autorsAction)
        self.helpMenu.addAction(self.licenceAction)

    def _createRecentProjectsMenu(self):
        self.recentProjectsMenu = QMenu("Recents Projects", parent=self)
        self.actions = []
        for name, path in self.config.recentProjects.items():
            if len(self.actions) > 10:
                break
            func = partial(print, path)
            action = QAction(name + '  -  ' + path)
            action.triggered.connect(func)
            self.actions.append(action)
            self.recentProjectsMenu.addAction(action)
    # END MENUS


    # CONNECTION FUNCTIONS 
    def newProjectFunc(self):
        if self.inputUi.new_project(self.config):
            self._createProjectMenu()
            self.changeWindowTitle(self.project.get_project_name())
            self.draw()

    def loadProjectFunc(self, path=None):
        if self.inputUi.loadProject(self.config, path):
            self._createProjectMenu()
            self.changeWindowTitle(self.project.get_project_name())
            self.draw()

    def loadRecentProject(self):
        if self.config.openLastProject and self.config.haveRecentProjects():
            self.importProject_call(self.config.getMostRecentProjectDir())
        else:
            if self.inputUi.getStarted(self.config):
                self._createProjectMenu()
                self.changeWindowTitle(self.project.get_project_name())
                self.draw()

    def saveProjectFunc(self):
        print('Save Project Is Not Implemented')    

    def saveProjectAsFunc(self):
        print('Save Project As Is Not Implemented')

    def saveImageFunc(self):
        userPath = expanduser('~')
        project_path = "{}\\OpenPulse\\Projects".format(userPath)
        if not exists(project_path):
            project_path = ""
        path, _type = QFileDialog.getSaveFileName(None, 'Save file', project_path, 'PNG (*.png)')
        if path != "":
            self.getOPVWidget().savePNG(path)
    
    # Graphic 
    def plotEntityFunc(self):
        # self.opvUi.plotEntities(False)
        self.opvUi.changePlotToEntities()

    def plotSectionsFunc(self):
        # self.opvUi.plotEntities(True)
        self.opvUi.changePlotToEntities()
    
    def plotMeshFunc(self):
        self.opvUi.changePlotToMesh()
    
    # Help
    def helpFunc(self):
        print('Help')
        
    def aboutFunc(self):
        print('About Us')

    def autorsFunc(self):
        print('Autors')
    
    def licenceFunc(self):
        print('MIT Licence')

    def draw(self):
        self.opvUi.plotEntities()
        self.opvUi.changePlotToMesh()
        self.plotEntityFunc()

    def closeEvent(self, event):
        save = QMessageBox.Save
        cancel = QMessageBox.Cancel
        discard = QMessageBox.Discard

        question = QMessageBox.question(
            self,
            'SAVE CHANGES',
            'Save changes before closing?',
            save | cancel | discard
        )

        if question == save:
            print('saving')
        elif question == cancel:
            event.ignore()
        elif question == discard:
            print('discarding')

    def getInputWidget(self):
        return self.inputUi

    def getInfoWidget(self):
        return self.infoUi

    def getOPVWidget(self):
        return self.opvUi

    def getProject(self):
        return self.project

# a big step for a man, a bigger step for code readability