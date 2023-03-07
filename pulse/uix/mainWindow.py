from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QAction, QToolBar, QSplitter, QFileDialog, QMessageBox, QMainWindow, QMenu, QWidget, QCheckBox, QRadioButton, QLabel, QStatusBar, QSizeGrip

from pulse.uix.menu.Menu import Menu
from pulse.uix.inputUi import InputUi
from pulse.uix.opvUi import OPVUi
from pulse.project import Project
from pulse.uix.config import Config
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput

import sys
from os.path import expanduser, basename, exists, dirname
from pathlib import Path
import numpy as np

from pulse.uix.menu import *
# from pulse.uix.menu.widgets import *

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
        self._createProjectToolBar()
        self._createAnimationToolBar()
        self._createHideShowToolBar()
        self.set_enable_menuBar(False)
        self._createStatusBar()
        self.show()
        self.loadRecentProject()

    # Let this method be operational in some way!
    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_H:
    #         self.hide_selection()
    #     elif event.key() == Qt.Key_U:
    #         self.unhide_selection()

    def _loadIcons(self):
        icons_path = 'data\\icons\\'
        self.pulse_icon = QIcon(icons_path + 'pulse.png')
        self.new_icon = QIcon(icons_path + 'add.png')
        self.open_icon = QIcon(icons_path + 'upload.png')
        self.reset_icon = QIcon(icons_path + 'refresh.png')
        self.saveImage_icon = QIcon(icons_path + 'save_image.png')
        self.exit_icon = QIcon(icons_path + 'exit.png')
        self.playpause_icon = QIcon(icons_path + 'play_pause.png')
        self.element_and_lines_with_cross_sections_icon = QIcon(icons_path + 'cross_section_representation.png')
        self.lines_only_icon = QIcon(icons_path + 'lines_only.png')
        self.elements_and_nodes_icon = QIcon(icons_path + 'elements_and_nodes.png')
        self.elements_only_icon = QIcon(icons_path + 'elements_only.png')
        self.nodes_only_icon = QIcon(icons_path + 'nodes_only.png')
        
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
 
        self.about_action = QAction(self.pulse_icon, '&About OpenPulse', self)   
        self.about_action.setStatusTip('About OpenPulse')
        # self.about_action.setShortcut('F8')
        self.about_action.triggered.connect(self.getInputWidget().about_OpenPulse)

        # Graphics
        self.entities_action = QAction('&Plot Lines', self)        
        self.entities_action.setShortcut('Ctrl+1')
        self.entities_action.setStatusTip('Plot Lines')
        self.entities_action.triggered.connect(self.plot_entities)

        self.entities_action_radius = QAction('&Plot Lines with Cross-section', self)        
        self.entities_action_radius.setShortcut('Ctrl+2')
        self.entities_action_radius.setStatusTip('Plot Lines with Cross-section')
        self.entities_action_radius.triggered.connect(self.plot_entities_with_cross_section)

        self.mesh_action = QAction('&Plot Mesh', self)        
        self.mesh_action.setShortcut('Ctrl+3')
        self.mesh_action.setStatusTip('Plot Mesh')
        self.mesh_action.triggered.connect(self.plot_mesh)

        self.section_action = QAction('&Plot Cross-section', self)
        self.section_action.setShortcut('Ctrl+4')
        self.section_action.setStatusTip('Plot Cross-section')
        self.section_action.triggered.connect(self.getInputWidget().plot_cross_section)

        self.plot_material_action = QAction('&Plot Material', self)
        self.plot_material_action.setShortcut('Ctrl+5')
        self.plot_material_action.setStatusTip('Plot Material')
        # self.plot_material_action.triggered.connect(self.getInputWidget().plot_material)

        self.plot_fluid_action = QAction('&Plot Fluid', self)
        self.plot_fluid_action.setShortcut('Ctrl+6')
        self.plot_fluid_action.setStatusTip('Plot Fluid')
        # self.plot_fluid_action.triggered.connect(self.getInputWidget().plot_fluid)

        self.mesh_setup_visibility_action = QAction('&User preferences', self)
        self.mesh_setup_visibility_action.setShortcut('Ctrl+7')
        self.mesh_setup_visibility_action.setStatusTip('User preferences')
        self.mesh_setup_visibility_action.triggered.connect(self.getInputWidget().mesh_setup_visibility)

        # General Settings
        self.setProjectAtributtes_action = QAction('&Set Project Attributes', self) 
        self.setProjectAtributtes_action.setShortcut('Alt+1')
        self.setProjectAtributtes_action.setStatusTip('Set Project Attributes')
        self.setProjectAtributtes_action.triggered.connect(self.getInputWidget().set_project_attributes)

        self.geometryDesigner_action = QAction('&Geometry Designer', self) 
        self.geometryDesigner_action.setShortcut('Alt+2')
        self.geometryDesigner_action.setStatusTip('Geometry Designer')
        self.geometryDesigner_action.triggered.connect(self.getInputWidget().call_geometry_designer)

        self.setMeshProperties_action = QAction('&Set Mesh Properties', self) 
        self.setMeshProperties_action.setShortcut('Alt+3')
        self.setMeshProperties_action.setStatusTip('Set Mesh Properties')
        self.setMeshProperties_action.triggered.connect(self.getInputWidget().set_mesh_properties)

        self.setGeometryFile_action = QAction('&Set Geometry File', self) 
        self.setGeometryFile_action.setShortcut('Alt+4')
        self.setGeometryFile_action.setStatusTip('Set Geometry File')
        self.setGeometryFile_action.triggered.connect(self.getInputWidget().set_geometry_file)

        self.setMaterial_action = QAction('&Set Material', self)        
        self.setMaterial_action.setShortcut('Alt+5')
        self.setMaterial_action.setStatusTip('Set Material')
        self.setMaterial_action.triggered.connect(self.getInputWidget().set_material)

        self.set_fluid_action = QAction('&Set Fluid', self)        
        self.set_fluid_action.setShortcut('Alt+6')
        self.set_fluid_action.setStatusTip('Set Fluid')
        self.set_fluid_action.triggered.connect(self.getInputWidget().set_fluid)

        self.set_crossSection_action = QAction('&Set Cross-Section', self)        
        self.set_crossSection_action.setShortcut('Alt+7')
        self.set_crossSection_action.setStatusTip('Set Cross-Section')
        self.set_crossSection_action.triggered.connect(self.getInputWidget().set_cross_section)

        # Structural Model Setup
        self.setStructuralElementType_action = QAction('&Set Structural Element Type', self)        
        # self.setStructuralElementType_action.setShortcut('')
        self.setStructuralElementType_action.setStatusTip('Set Structural Element Type')
        self.setStructuralElementType_action.triggered.connect(self.getInputWidget().setStructuralElementType)

        self.addFlanges_action = QAction('&Add Connecting Flanges', self)
        # self.addFlanges_action.setShortcut('')
        self.addFlanges_action.setStatusTip('Add Connecting Flanges')
        self.addFlanges_action.triggered.connect(self.getInputWidget().add_flanges)

        self.setDOF_action = QAction('&Set Prescribed DOFs', self)        
        # self.setDOF_action.setShortcut('')
        self.setDOF_action.setStatusTip('Set Prescribed DOFs')
        self.setDOF_action.triggered.connect(self.getInputWidget().setDOF)

        self.setForce_action = QAction('&Set Nodal Loads', self)        
        # self.setForce_action.setShortcut('')
        self.setForce_action.setStatusTip('Set Nodal Loads')
        self.setForce_action.triggered.connect(self.getInputWidget().setNodalLoads)

        self.setMass_action = QAction('&Add: Mass / Spring / Damper', self)        
        # self.setMass_action.setShortcut('')
        self.setMass_action.setStatusTip('Add: Mass / Spring / Damper')
        self.setMass_action.triggered.connect(self.getInputWidget().addMassSpringDamper)

        self.setcappedEnd_action = QAction('&Set Capped End', self)        
        # self.setcappedEnd_action.setShortcut('')
        self.setcappedEnd_action.setStatusTip('Set Capped End')
        self.setcappedEnd_action.triggered.connect(self.getInputWidget().setcappedEnd)

        self.stressStiffening_action = QAction('&Set Strees Stiffening', self)        
        # self.stressStiffening_action.setShortcut('')
        self.stressStiffening_action.setStatusTip('Set Strees Stiffening')
        self.stressStiffening_action.triggered.connect(self.getInputWidget().set_stress_stress_stiffening)

        self.nodalLinks_action = QAction('&Add Elastic Nodal Links', self)        
        # self.nodalLinks_action.setShortcut('')
        self.nodalLinks_action.setStatusTip('Add Elastic Nodal Links')
        self.nodalLinks_action.triggered.connect(self.getInputWidget().add_elastic_nodal_links)

        # Acoustic Model Setup
        self.setAcousticElementType_action = QAction('&Set Acoustic Element Type', self)        
        # self.setAcousticElementType_action.setShortcut('')
        self.setAcousticElementType_action.setStatusTip('Set Acoustic Element Type')
        self.setAcousticElementType_action.triggered.connect(self.getInputWidget().set_acoustic_element_type)

        self.setAcousticPressure_action = QAction('&Set Acoustic Pressure', self)        
        # self.setAcousticPressure_action.setShortcut('')
        self.setAcousticPressure_action.setStatusTip('Set Acoustic Pressure')
        self.setAcousticPressure_action.triggered.connect(self.getInputWidget().setAcousticPressure)

        self.setVolumeVelocity_action = QAction('&Set Volume Velocity', self)        
        # self.setVolumeVelocity_action.setShortcut('')
        self.setVolumeVelocity_action.setStatusTip('Set Volume Velocity')
        self.setVolumeVelocity_action.triggered.connect(self.getInputWidget().setVolumeVelocity)

        self.setSpecificImpedance_action = QAction('&Set Specific Impedance', self)        
        # self.setSpecificImpedance_action.setShortcut('')
        self.setSpecificImpedance_action.setStatusTip('Set Specific Impedance')
        self.setSpecificImpedance_action.triggered.connect(self.getInputWidget().setSpecificImpedance)

        self.set_radiation_impedance_action = QAction('&Set Radiation Impedance', self)        
        # self.set_radiation_impedance_action.setShortcut('')
        self.set_radiation_impedance_action.setStatusTip('Set Radiation Impedance')
        self.set_radiation_impedance_action.triggered.connect(self.getInputWidget().set_radiation_impedance)

        self.add_perforated_plate_action = QAction('&Add Perforated Plate', self)        
        # self.add_perforated_plate_action.setShortcut('')
        self.add_perforated_plate_action.setStatusTip('Add Perforated Plate')
        self.add_perforated_plate_action.triggered.connect(self.getInputWidget().add_perforated_plate)

        self.set_acoustic_element_length_correction_action = QAction('&Set Acoustic Element Length Correction', self)        
        # self.set_acoustic_element_length_correction_action.setShortcut('')
        self.set_acoustic_element_length_correction_action.setStatusTip('Set Acoustic Element Length Correction')
        self.set_acoustic_element_length_correction_action.triggered.connect(self.getInputWidget().set_acoustic_element_length_correction)

        self.add_compressor_excitation_action = QAction('&Add Compressor Excitation', self)        
        # self.add_compressor_excitation_action.setShortcut('')
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
        self.runAnalysis_action.setShortcut('F5')
        self.runAnalysis_action.setStatusTip('Run Analysis')
        self.runAnalysis_action.triggered.connect(self.getInputWidget().runAnalysis)
 
        # Results Viewer
        self.plotStructuralModeShapes_action = QAction('&Plot Structural Mode Shapes', self)        
        # self.plotStructuralModeShapes_action.setShortcut('')
        self.plotStructuralModeShapes_action.setStatusTip('Plot Structural Mode Shapes')
        self.plotStructuralModeShapes_action.triggered.connect(self.getInputWidget().plotStructuralModeShapes)

        self.plotDisplacementField_action = QAction('&Plot Displacement Field', self)        
        # self.plotDisplacementField_action.setShortcut('')
        self.plotDisplacementField_action.setStatusTip('Plot Displacement Field')
        self.plotDisplacementField_action.triggered.connect(self.getInputWidget().plotDisplacementField)

        self.plotStructuralFrequencyResponse = QAction('&Plot Structural Frequency Response', self)        
        # self.plotStructuralFrequencyResponse.setShortcut('')
        self.plotStructuralFrequencyResponse.setStatusTip('Plot Structural Frequency Response')
        self.plotStructuralFrequencyResponse.triggered.connect(self.getInputWidget().plotStructuralFrequencyResponse)

        self.plotReactionsFrequencyResponse = QAction('&Plot Reactions Frequency Response', self)        
        # self.plotReactionsFrequencyResponse.setShortcut('')
        self.plotReactionsFrequencyResponse.setStatusTip('Plot Reactions Frequency Response')
        self.plotReactionsFrequencyResponse.triggered.connect(self.getInputWidget().plotReactionsFrequencyResponse)

        self.plotSressField_action = QAction('&Plot Stress Field', self)        
        # self.plotSressField_action.setShortcut('')
        self.plotSressField_action.setStatusTip('Plot Stress Field')
        self.plotSressField_action.triggered.connect(self.getInputWidget().plotStressField)

        self.plotSressFrequencyResponse_action = QAction('&Plot Stress Frequency Response', self)        
        # self.plotSressFrequencyResponse_action.setShortcut('')
        self.plotSressFrequencyResponse_action.setStatusTip('Plot Stress Frequency Response')
        self.plotSressFrequencyResponse_action.triggered.connect(self.getInputWidget().plotStressFrequencyResponse)

        self.plotPressureField_action = QAction('&Plot Acoustic Pressure Field', self)        
        # self.plotPressureField_action.setShortcut('')
        self.plotPressureField_action.setStatusTip('Plot Acoustic Pressure Field')
        self.plotPressureField_action.triggered.connect(self.getInputWidget().plotAcousticPressureField)

        self.plotAcousticFrequencyResponse = QAction('&Plot Acoustic Frequency Response', self)        
        # self.plotAcousticFrequencyResponse.setShortcut('')
        self.plotAcousticFrequencyResponse.setStatusTip('Plot Acoustic Frequency Response')
        self.plotAcousticFrequencyResponse.triggered.connect(self.getInputWidget().plotAcousticFrequencyResponse)

        self.plotAcousticDeltaPressures = QAction('&Plot Acoustic Delta Pressures', self)        
        # self.plotAcousticDeltaPressures.setShortcut('')
        self.plotAcousticDeltaPressures.setStatusTip('Plot Acoustic Delta Pressures')
        self.plotAcousticDeltaPressures.triggered.connect(self.getInputWidget().plot_TL_NR)

        self.plot_TL_NR = QAction('&Plot Transmission Loss or Attenuation', self)        
        self.plot_TL_NR.setStatusTip('Plot Transmission Loss or Attenuation')
        # self.plot_TL_NR.setShortcut('')
        self.plot_TL_NR.triggered.connect(self.getInputWidget().plot_TL_NR)

        self.playPauseAnimaton_action = QAction(self.playpause_icon, '&Play/Pause Animation', self)
        self.playPauseAnimaton_action.setStatusTip('Play/Pause Animation')
        self.playPauseAnimaton_action.setShortcut('Space')
        self.playPauseAnimaton_action.triggered.connect(self.opv_widget.opvAnalysisRenderer.tooglePlayPauseAnimation)

        self.animationSettings_action = QAction('&Animation Settings', self)
        self.animationSettings_action.setStatusTip('Animation Settings')
        self.animationSettings_action.triggered.connect(self.getInputWidget().animationSettings)

        self.show_lines_action = QAction(self.lines_only_icon, '&Hide/Show lines', self)
        # self.show_lines_action.setShortcut('')
        self.show_lines_action.setStatusTip('Hide/Show lines')
        self.show_lines_action.triggered.connect(self.hide_show_lines)

        self.show_elements_and_nodes_action = QAction(self.elements_and_nodes_icon, '&Hide/Show elements and nodes', self)
        # self.show_elements_and_nodes_action.setShortcut('')
        self.show_elements_and_nodes_action.setStatusTip('Hide/Show elements and nodes')
        self.show_elements_and_nodes_action.triggered.connect(self.hide_show_elements_and_nodes)

        self.show_elements_action = QAction(self.elements_only_icon, '&Hide/Show elements', self)
        # self.show_elements_action.setShortcut('')
        self.show_elements_action.setStatusTip('Hide/Show elements')
        self.show_elements_action.triggered.connect(self.hide_show_elements)

        self.show_nodes_action = QAction(self.nodes_only_icon, '&Hide/Show nodes', self)
        # self.show_nodes_action.setShortcut('')
        self.show_nodes_action.setStatusTip('Hide/Show nodes')
        self.show_nodes_action.triggered.connect(self.hide_show_nodes)

        # Views
        self.cameraTop_action = QAction('&Top View', self)
        self.cameraTop_action.setShortcut('Ctrl+Shift+1')
        self.cameraTop_action.triggered.connect(self.cameraTop_call)

        self.cameraBottom_action = QAction('&Bottom View', self)
        self.cameraBottom_action.setShortcut('Ctrl+Shift+2')
        self.cameraBottom_action.triggered.connect(self.cameraBottom_call)

        self.cameraLeft_action = QAction('&Left View', self)
        self.cameraLeft_action.setShortcut('Ctrl+Shift+3')
        self.cameraLeft_action.triggered.connect(self.cameraLeft_call)

        self.cameraRight_action = QAction('&Right View', self)
        self.cameraRight_action.setShortcut('Ctrl+Shift+4')
        self.cameraRight_action.triggered.connect(self.cameraRight_call)

        self.cameraFront_action = QAction('&Front View', self)
        self.cameraFront_action.setShortcut('Ctrl+Shift+5')
        self.cameraFront_action.triggered.connect(self.cameraFront_call)

        self.cameraBack_action = QAction('&Back View', self)
        self.cameraBack_action.setShortcut('Ctrl+Shift+6')
        self.cameraBack_action.triggered.connect(self.cameraBack_call)

        self.cameraIsometric_action = QAction('&Isometric View', self)
        self.cameraIsometric_action.setShortcut('Ctrl+Shift+7')
        self.cameraIsometric_action.triggered.connect(self.cameraIsometric_call)

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
        self.graphicMenu.addAction(self.entities_action)
        self.graphicMenu.addAction(self.entities_action_radius)
        self.graphicMenu.addAction(self.mesh_action)
        self.graphicMenu.addAction(self.section_action)
        self.graphicMenu.addAction(self.plot_material_action)
        self.graphicMenu.addAction(self.plot_fluid_action)
        self.graphicMenu.addAction(self.mesh_setup_visibility_action)

    def _loadGeneralSettingsMenu(self):
        self.generalSettingsMenu.addAction(self.setProjectAtributtes_action)
        self.generalSettingsMenu.addAction(self.setMeshProperties_action)
        self.generalSettingsMenu.addAction(self.setGeometryFile_action)        
        self.generalSettingsMenu.addAction(self.setMaterial_action)
        self.generalSettingsMenu.addAction(self.set_fluid_action)
        self.generalSettingsMenu.addAction(self.set_crossSection_action)
        
    def _loadModelSetupMenu(self):
        #Structural model setup
        self.structuralModelSetupMenu.addAction(self.setStructuralElementType_action)
        self.structuralModelSetupMenu.addAction(self.addFlanges_action)
        self.structuralModelSetupMenu.addAction(self.setDOF_action)
        self.structuralModelSetupMenu.addAction(self.setForce_action)
        self.structuralModelSetupMenu.addAction(self.setMass_action)
        self.structuralModelSetupMenu.addAction(self.setcappedEnd_action)
        self.structuralModelSetupMenu.addAction(self.stressStiffening_action)
        self.structuralModelSetupMenu.addAction(self.nodalLinks_action)
        #Acoustic model setup
        self.acousticModelSetupMenu.addAction(self.setAcousticElementType_action)
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
        #structural
        self.resultsViewerMenu.addAction(self.plotStructuralModeShapes_action)
        self.resultsViewerMenu.addAction(self.plotDisplacementField_action)
        self.resultsViewerMenu.addAction(self.plotStructuralFrequencyResponse)
        self.resultsViewerMenu.addAction(self.plotReactionsFrequencyResponse)
        self.resultsViewerMenu.addAction(self.plotSressField_action)
        self.resultsViewerMenu.addAction(self.plotSressFrequencyResponse_action)
        #acoustic
        self.resultsViewerMenu.addAction(self.plotPressureField_action)
        self.resultsViewerMenu.addAction(self.plotAcousticFrequencyResponse)
        self.resultsViewerMenu.addAction(self.plotAcousticDeltaPressures)
        self.resultsViewerMenu.addAction(self.plot_TL_NR)
        #animation
        self.resultsViewerMenu.addAction(self.playPauseAnimaton_action)
        self.resultsViewerMenu.addAction(self.animationSettings_action)
    
    def _loadCameraMenu(self):
        self.viewsMenu.addAction(self.cameraTop_action)
        self.viewsMenu.addAction(self.cameraBottom_action)
        self.viewsMenu.addAction(self.cameraLeft_action)
        self.viewsMenu.addAction(self.cameraRight_action)
        self.viewsMenu.addAction(self.cameraFront_action)
        self.viewsMenu.addAction(self.cameraBack_action)
        self.viewsMenu.addAction(self.cameraIsometric_action)

    def _loadHelpMenu(self):
        self.helpMenu.addAction(self.help_action)
        self.helpMenu.addAction(self.about_action)

    def _createMenuBar(self):
        menuBar = self.menuBar()

        self.projectMenu = menuBar.addMenu('&Project')
        self.graphicMenu = menuBar.addMenu('&Graphic')
        self.generalSettingsMenu = menuBar.addMenu('&General Settings')
        self.structuralModelSetupMenu = menuBar.addMenu('&Structural Model Setup')
        self.acousticModelSetupMenu = menuBar.addMenu('&Acoustic Model Setup')
        
        self.modelInfoMenu = menuBar.addMenu('&Model Info')
        self.analysisMenu = menuBar.addMenu('&Analysis')
        self.resultsViewerMenu = menuBar.addMenu('&Results Viewer')
        self.viewsMenu = menuBar.addMenu('&Views')
        self.helpMenu = menuBar.addMenu("&Help")

        self._loadProjectMenu()
        self._loadGraphicMenu()
        self._loadGeneralSettingsMenu()
        self._loadModelSetupMenu()
        self._loadModelInfoMenu()
        self._loadAnalysisMenu()
        self._loadResultsViewerMenu()
        self._loadCameraMenu()
        self._loadHelpMenu()

    def set_enable_menuBar(self, _bool):
        #
        self.graphicMenu.setEnabled(_bool)
        self.generalSettingsMenu.setEnabled(_bool)
        self.structuralModelSetupMenu.setEnabled(_bool)
        self.acousticModelSetupMenu.setEnabled(_bool)
        self.modelInfoMenu.setEnabled(_bool)
        self.analysisMenu.setEnabled(_bool)
        self.resultsViewerMenu.setEnabled(_bool)
        self.viewsMenu.setEnabled(_bool)
        #
        self.saveAsPng_action.setEnabled(_bool) 
        self.reset_action.setEnabled(_bool) 
        #
        self.toolbar_animation.setEnabled(_bool)
        self.toolbar_hide_show.setEnabled(_bool)

    def _getFont(self, fontSize, bold=False, italic=False, family_type="Arial"):
        font = QFont()
        font.setFamily(family_type)
        font.setPointSize(fontSize)
        font.setBold(bold)
        font.setItalic(italic)
        font.setWeight(75)  
        return font

    def _createProjectToolBar(self):
        self.toolbar = QToolBar("Project toolbar")
        self.toolbar.setIconSize(QSize(28,28))
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.new_action)
        self.toolbar.addAction(self.import_action)
        self.toolbar.addAction(self.reset_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.saveAsPng_action)

    def _createStatusBar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        #
        label_font = self._getFont(10, bold=True, italic=False, family_type="Arial")
        self.label_geometry_state = QLabel("", self)
        self.label_geometry_state.setFont(label_font)
        self.status_bar.addPermanentWidget(self.label_geometry_state)
        #
        self.label_mesh_state = QLabel("", self)
        self.label_mesh_state.setFont(label_font)
        self.status_bar.addPermanentWidget(self.label_mesh_state)

    def _updateGeometryState(self, label):
        _state = ""
        if label != "":
            _state = f" Geometry: {label} "            
        self.label_geometry_state.setText(_state)

    def _updateMeshState(self, label):
        _state = ""
        if label != "":
            _state = f" Mesh: {label} "           
        self.label_mesh_state.setText(_state)

    def _updateStatusBar(self):
        # Check and update geometry state
        if self.project.empty_geometry:
            self._updateGeometryState("pending")
        else:
            self._updateGeometryState("ok")
        # Check and update mesh state
        if len(self.project.preprocessor.structural_elements) == 0:
            if self.project.check_mesh_setup():
                self._updateMeshState("setup complete but not generated")
            else:
                self._updateMeshState("pending")
        else:
            self._updateMeshState("ok")

    def _createHideShowToolBar(self):

        label_font = self._getFont(10, bold=True, italic=False, family_type="Arial")
        radioButton_font = self._getFont(9, bold=True, italic=True, family_type="Arial")

        self.toolbar_hide_show = QToolBar("Hide/Show toolbar")
        self.toolbar_hide_show.setIconSize(QSize(30,30))
        self.toolbar_hide_show.setMovable(True)
        self.addToolBar(self.toolbar_hide_show)

        self.hide_selection_action = QAction('&Hide \nselection', self)
        self.hide_selection_action.setFont(radioButton_font)
        self.hide_selection_action.setShortcut('H')
        self.hide_selection_action.triggered.connect(self.hide_selection)
        
        # you need to add the action to the main window to make the shortcut work 
        # without creating a button
        self.addAction(self.hide_selection_action)

        self.show_all_action = QAction('&Show \nall', self)
        self.show_all_action.setFont(radioButton_font)
        self.show_all_action.setShortcut('U')
        self.show_all_action.triggered.connect(self.unhide_selection)

        self.acoustic_symbols_action = QAction('&Acoustic \nsymbols', self)
        self.acoustic_symbols_action.setFont(radioButton_font)
        # self.acoustic_symbols_action.setShortcut('U')
        self.acoustic_symbols_action.triggered.connect(self.hide_show_acoustic_symbols)

        self.structural_symbols_action = QAction('&Structural \nsymbols', self)
        self.structural_symbols_action.setFont(radioButton_font)
        # self.structural_symbols_action.setShortcut('U')
        self.structural_symbols_action.triggered.connect(self.hide_show_structural_symbols)
        
        self.label_hide_show_controls = QLabel(' Hide/Show controls:  ', self)
        self.label_hide_show_controls.setFont(label_font)

        self.radioButton_hide = QRadioButton("Hide ", self)
        self.radioButton_show = QRadioButton("Show ", self)
        self.radioButton_hide.setChecked(True)
        self.radioButton_hide.setFont(radioButton_font)
        self.radioButton_show.setFont(radioButton_font)

        # self.toolbar_hide_show.addAction("")
        self.toolbar_hide_show.addWidget(self.label_hide_show_controls)
        self.toolbar_hide_show.addWidget(self.radioButton_hide)
        self.toolbar_hide_show.addWidget(self.radioButton_show)

        self.toolbar_hide_show.addSeparator()
        self.toolbar_hide_show.addAction(self.show_lines_action)
        self.toolbar_hide_show.addAction(self.show_elements_and_nodes_action)
        self.toolbar_hide_show.addAction(self.show_elements_action)
        self.toolbar_hide_show.addAction(self.show_nodes_action)
        self.toolbar_hide_show.addAction(self.show_all_action)
        self.toolbar_hide_show.addAction(self.acoustic_symbols_action)
        self.toolbar_hide_show.addAction(self.structural_symbols_action)

        # widget_hide_selection = self.toolbar_hide_show.widgetForAction(self.hide_selection_action)
        widget_show_all = self.toolbar_hide_show.widgetForAction(self.show_all_action)
        widget_acoustic_symbols = self.toolbar_hide_show.widgetForAction(self.acoustic_symbols_action)
        widget_structural_symbols = self.toolbar_hide_show.widgetForAction(self.structural_symbols_action)

        # widget_hide_selection.setStyleSheet("QWidget { border: 1px solid rgb(200,200,200); }")
        widget_show_all.setStyleSheet("QWidget { border: 1px solid rgb(200,200,200); }")
        widget_acoustic_symbols.setStyleSheet("QWidget { border: 1px solid rgb(200,200,200); }")
        widget_structural_symbols.setStyleSheet("QWidget { border: 1px solid rgb(200,200,200); }")

        # widths = []
        # widths.append(widget_hide_selection.width())
        # widths.append(widget_show_all.width())
        # widths.append(widget_acoustic_symbols.width())
        # widths.append(widget_structural_symbols.width())
        # _width = max(widths)+10

        # widget_hide_selection.resize(_width, widget_hide_selection.height())
        # widget_show_all.resize(_width, widget_show_all.height())
        # widget_acoustic_symbols.resize(_width, widget_acoustic_symbols.height())
        # widget_structural_symbols.resize(_width, widget_structural_symbols.height())

    def _createAnimationToolBar(self):

        label_font = self._getFont(10, bold=True, italic=False, family_type="Arial")
        # radioButton_font = self._getFont(9, bold=True, italic=True, family_type="Arial")

        self.toolbar_animation = QToolBar("Animation toolbar")
        self.toolbar_animation.setIconSize(QSize(30,30))
        self.toolbar_animation.setMovable(True)
        self.addToolBar(self.toolbar_animation)

        self.label_animation_controls = QLabel(' Animation controls:  ', self)
        self.label_animation_controls.setFont(label_font)

        # self.toolbar_animation.addSeparator()
        self.toolbar_animation.addWidget(self.label_animation_controls)
        self.toolbar_animation.addAction(self.playPauseAnimaton_action)

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
            self.changeWindowTitle(self.project.file._project_name)
            self.draw()

    def importProject_call(self, path=None):
        if self.inputWidget.loadProject(self.config, path):
            self._loadProjectMenu()
            self.changeWindowTitle(self.project.file._project_name)
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
                self.changeWindowTitle(self.project.file._project_name)
                self.draw()

    def savePNG_call(self):
        project_path = self.project.file._project_path
        if not exists(project_path):
            project_path = ""
        path, _type = QFileDialog.getSaveFileName(None, 'Save file', project_path, 'PNG (*.png)')
        if path != "":
            self.getOPVWidget().savePNG(path)

    def cameraIsometric_call(self):
        self.opv_widget.setCameraView(0)

    def cameraTop_call(self):
        self.opv_widget.setCameraView(1)

    def cameraBottom_call(self):
        self.opv_widget.setCameraView(2)

    def cameraLeft_call(self):
        self.opv_widget.setCameraView(3)

    def cameraRight_call(self):
        self.opv_widget.setCameraView(4)

    def cameraFront_call(self):
        self.opv_widget.setCameraView(5)

    def cameraBack_call(self):
        self.opv_widget.setCameraView(6)

    def hide_selection(self):
        self.opv_widget.opvRenderer.hide_selection()

    def unhide_selection(self):
        self.opv_widget.opvRenderer.unhide_all()

    def hide_show_lines(self):
        self.opv_widget.opvRenderer.hide_show_lines(self.radioButton_show.isChecked())

    def hide_show_elements_and_nodes(self):
        self.opv_widget.opvRenderer.hide_show_elements_and_nodes(self.radioButton_show.isChecked())

    def hide_show_elements(self):
        self.opv_widget.opvRenderer.hide_show_elements(self.radioButton_show.isChecked())
            
    def hide_show_nodes(self):
        self.opv_widget.opvRenderer.hide_show_nodes(self.radioButton_show.isChecked())

    def hide_show_acoustic_symbols(self):
        self.opv_widget.opvRenderer.hide_show_acoustic_symbols()

    def hide_show_structural_symbols(self):
        self.opv_widget.opvRenderer.hide_show_structural_symbols()

    def plot_entities(self):
        self.opv_widget.changePlotToEntities()

    def plot_entities_with_cross_section(self):
        self.opv_widget.changePlotToEntitiesWithCrossSection()

    def plot_mesh(self):
        self.opv_widget.changePlotToMesh()

    def draw(self):
        self.opv_widget.updatePlots()
        self.plot_entities_with_cross_section()
        self.opv_widget.setCameraView(5)

    def closeEvent(self, event):
        title = "OpenPulse stop execution requested"
        message = "Do you really want to stop the OpenPulse processing and close \nthe current project setup?\n\n\n"
        message += "Note: The current project setup progress has already \nbeen saved in the project files."
        read = CallDoubleConfirmationInput(title, message, leftButton_label="No", rightButton_label="Yes")

        if read._stop:
            event.ignore()
            return

        if read._continue:
            sys.exit()
          
    def getInputWidget(self):
        return self.inputWidget

    def getMenuWidget(self):
        return self.menuWidget

    def getOPVWidget(self):
        return self.opv_widget

    def getProject(self):
        return self.project