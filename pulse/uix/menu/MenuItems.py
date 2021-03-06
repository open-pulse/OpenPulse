from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QBrush, QColor, QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt

class MenuItems(QTreeWidget):
    """Menu Items

    This class is responsible for creating, configuring and building the items
    in the items menu, located on the right side of the interface.

    """
    def __init__(self, main_window):
        super().__init__()
        self.mainWindow = main_window
        self.project = main_window.getProject()
        self._createNames()
        self._createIcons()
        self._createFonts()
        self._createColorsBrush()
        self._configTree()
        self._createItems()
        self._configItems()
        self._addItems()
        self._updateItems()

    def keyPressEvent(self, event):
        """This deals with key events that are directly linked with the menu."""
        if event.key() == Qt.Key_F5:
            self.mainWindow.getInputWidget().runAnalysis()
            self._updateItems()

    def _createNames(self):
        """Create some variables to define the name of the items in the menu"""
        self.name_top_structuralmodelSetup = "Structural Model Setup"
        self.name_child_setStructuralElementType = "Set Structural Element Type"
        self.name_child_setRotationDecoupling = "Set Rotation Decoupling (B2PX)"
        self.name_child_set_material = "Set Material"
        self.name_child_set_crossSection = "Set Cross-Section"
        self.name_child_setPrescribedDofs = "Set Prescribed DOFs"
        self.name_child_setNodalLoads = "Set Nodal Loads"
        self.name_child_addMassSpringDamper = "Add: Mass / Spring / Damper"
        self.name_child_setcappedEnd = "Set Capped End"
        self.name_child_set_stress_stiffening = "Set Stress Stiffening"
        self.name_child_add_elastic_nodal_links = "Add Elastic Nodal Links"

        self.name_top_acousticmodelSetup = "Acoustic Model Setup"
        self.name_child_setAcousticElementType = "Set Acoustic Element Type"
        self.name_child_set_fluid = "Set Fluid"
        self.name_child_setAcousticPressure = "Set Acoustic Pressure"
        self.name_child_setVolumeVelocity = "Set Volume Velocity"
        self.name_child_setSpecificImpedance = "Set Specific Impedance"
        self.name_child_set_radiation_impedance = "Set Radiation Impedance"
        self.name_child_add_perforated_plate = "Add Perforated Plate"
        self.name_child_set_acoustic_element_length_correction = "Set Element Length Correction"
        self.name_child_add_compressor_excitation = 'Add Compressor Excitation'
        
        self.name_top_analysis = "Analysis"
        self.name_child_selectAnalysisType = "Select Analysis Type"
        self.name_child_analisysSetup = "Analysis Setup"
        self.name_child_runAnalysis = "Run Analysis (F5)"

        self.name_top_resultsViewer_structural = "Results Viewer - Structural"
        self.name_child_plotStructuralModeShapes = "Plot Structural Mode Shapes"
        self.name_child_plotDisplacementField = "Plot Displacement Field"
        self.name_child_plotStructuralFrequencyResponse = "Plot Structural Frequency Response"
        self.name_child_plotStressField = "Plot Stress Field"
        self.name_child_plotStressFrequencyResponse = "Plot Stress Frequency Response"

        self.name_top_resultsViewer_acoustic = "Results Viewer - Acoustic"
        self.name_child_plotAcousticModeShapes = "Plot Acoustic Mode Shapes"
        self.name_child_plotAcousticPressureField = "Plot Acoustic Pressure Field"
        self.name_child_plotAcousticFrequencyResponse = "Plot Acoustic Frequency Response"
        self.name_child_plot_TL_NR = "Plot Transmission Loss or Attenuation"
        self.name_child_plotReactionsFrequencyResponse = "Plot Reactions Frequency Response"


    def _createIcons(self):
        """Create Icons objects that are placed on the right side of the item.
            Currently isn't used.
        """
        self.icon_child_set_material = QIcon()
        self.icon_child_set_material.addPixmap(QPixmap("pulse/data/icons/pulse.png"), QIcon.Active, QIcon.On)

    def _createFonts(self):
        """Create Font objects that configure the font of the items."""
        self.font_top = QFont()
        #self.font_child = QFont()

        self.font_top.setFamily("Segoe UI")
        self.font_top.setPointSize(12)
        self.font_top.setBold(True)
        self.font_top.setItalic(False)
        self.font_top.setWeight(75)

        self.font_internal = QFont()
        self.font_internal.setFamily("Segoe UI")
        self.font_internal.setPointSize(11)
        #self.font_internal.setBold(False)
        #self.font_internal.setItalic(True)
        #self.font_internal.setWeight(75)

    def _createColorsBrush(self):
        """Create Color objects that define the color of the text and/or background of the items."""
        color_top = QColor(178, 178, 178)
        self.brush_top = QBrush(color_top)
        self.brush_top.setStyle(Qt.SolidPattern)
        #
        color_results_viewer = QColor(102, 204, 255)
        self.color_item_results_viewer = QBrush(color_results_viewer)
        self.color_item_results_viewer.setStyle(Qt.SolidPattern)

    def _configTree(self):
        """Define the initial configuration of the TreeWidget."""
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setTabKeyNavigation(True)
        self.setIndentation(0)
        self.itemClicked.connect(self.on_click_item)

    def _createItems(self):
        """Create all TreeWidgetItems."""
        self.item_top_structuralmodelSetup = QTreeWidgetItem([self.name_top_structuralmodelSetup])
        self.item_child_setStructuralElementType = QTreeWidgetItem([self.name_child_setStructuralElementType])
        self.item_child_setRotationDecoupling = QTreeWidgetItem([self.name_child_setRotationDecoupling])
        self.item_child_set_material = QTreeWidgetItem([self.name_child_set_material])
        self.item_child_set_crossSection = QTreeWidgetItem([self.name_child_set_crossSection])
        self.item_child_setPrescribedDofs = QTreeWidgetItem([self.name_child_setPrescribedDofs])
        self.item_child_setNodalLoads = QTreeWidgetItem([self.name_child_setNodalLoads])
        self.item_child_addMassSpringDamper = QTreeWidgetItem([self.name_child_addMassSpringDamper])
        self.item_child_setcappedEnd = QTreeWidgetItem([self.name_child_setcappedEnd])
        self.item_child_set_stress_stiffening = QTreeWidgetItem([self.name_child_set_stress_stiffening])
        self.item_child_add_elastic_nodal_links = QTreeWidgetItem([self.name_child_add_elastic_nodal_links])

        self.item_top_acousticmodelSetup = QTreeWidgetItem([self.name_top_acousticmodelSetup])
        self.item_child_setAcousticElementType = QTreeWidgetItem([self.name_child_setAcousticElementType])
        self.item_child_set_fluid = QTreeWidgetItem([self.name_child_set_fluid])
        self.item_child_setAcousticPressure = QTreeWidgetItem([self.name_child_setAcousticPressure])
        self.item_child_setVolumeVelocity = QTreeWidgetItem([self.name_child_setVolumeVelocity])
        self.item_child_setSpecificImpedance = QTreeWidgetItem([self.name_child_setSpecificImpedance])
        self.item_child_set_radiation_impedance = QTreeWidgetItem([self.name_child_set_radiation_impedance])
        self.item_child_add_perforated_plate = QTreeWidgetItem([self.name_child_add_perforated_plate])
        self.item_child_set_acoustic_element_length_correction = QTreeWidgetItem([self.name_child_set_acoustic_element_length_correction])
        self.item_child_add_compressor_excitation = QTreeWidgetItem([self.name_child_add_compressor_excitation])
        
        self.item_top_analysis = QTreeWidgetItem([self.name_top_analysis])
        self.item_child_selectAnalysisType = QTreeWidgetItem([self.name_child_selectAnalysisType])
        self.item_child_analisysSetup = QTreeWidgetItem([self.name_child_analisysSetup])
        self.item_child_runAnalysis = QTreeWidgetItem([self.name_child_runAnalysis])

        self.item_top_resultsViewer_structural = QTreeWidgetItem([self.name_top_resultsViewer_structural])
        self.item_child_plotStructuralModeShapes = QTreeWidgetItem([self.name_child_plotStructuralModeShapes])
        self.item_child_plotDisplacementField = QTreeWidgetItem([self.name_child_plotDisplacementField])
        self.item_child_plotStructuralFrequencyResponse = QTreeWidgetItem([self.name_child_plotStructuralFrequencyResponse])
        self.item_child_plotReactionsFrequencyResponse = QTreeWidgetItem([self.name_child_plotReactionsFrequencyResponse])
        self.item_child_plotStressField = QTreeWidgetItem([self.name_child_plotStressField])
        self.item_child_plotStressFrequencyResponse = QTreeWidgetItem([self.name_child_plotStressFrequencyResponse])

        self.item_top_resultsViewer_acoustic = QTreeWidgetItem([self.name_top_resultsViewer_acoustic])
        self.item_child_plotAcousticModeShapes = QTreeWidgetItem([self.name_child_plotAcousticModeShapes])
        self.item_child_plotAcousticPressureField = QTreeWidgetItem([self.name_child_plotAcousticPressureField])
        self.item_child_plotAcousticFrequencyResponse = QTreeWidgetItem([self.name_child_plotAcousticFrequencyResponse])
        self.item_child_plot_TL_NR = QTreeWidgetItem([self.name_child_plot_TL_NR])


    def _configItems(self):
        """Configure all items."""
        # Font setup - top items

        self.item_top_structuralmodelSetup.setFlags(Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        self.item_top_structuralmodelSetup.setFont(0, self.font_top)
        self.item_top_structuralmodelSetup.setTextAlignment(0, Qt.AlignHCenter)
        self.item_top_structuralmodelSetup.setBackground(0, self.brush_top)

        self.item_top_acousticmodelSetup.setFlags(Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        self.item_top_acousticmodelSetup.setFont(0, self.font_top)
        self.item_top_acousticmodelSetup.setTextAlignment(0, Qt.AlignHCenter)
        self.item_top_acousticmodelSetup.setBackground(0, self.brush_top)

        self.item_top_analysis.setFlags(Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        self.item_top_analysis.setFont(0, self.font_top)
        self.item_top_analysis.setTextAlignment(0, Qt.AlignHCenter)
        self.item_top_analysis.setBackground(0, self.brush_top)

        self.item_top_resultsViewer_structural.setFlags(Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        self.item_top_resultsViewer_structural.setFont(0, self.font_top)
        self.item_top_resultsViewer_structural.setTextAlignment(0, Qt.AlignHCenter)
        self.item_top_resultsViewer_structural.setBackground(0, self.color_item_results_viewer)

        self.item_top_resultsViewer_acoustic.setFlags(Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        self.item_top_resultsViewer_acoustic.setFont(0, self.font_top)
        self.item_top_resultsViewer_acoustic.setTextAlignment(0, Qt.AlignHCenter)
        self.item_top_resultsViewer_acoustic.setBackground(0, self.color_item_results_viewer)

        # Font setup - internal items

        self.item_child_setStructuralElementType.setFont(0, self.font_internal)
        self.item_child_setRotationDecoupling.setFont(0, self.font_internal)
        self.item_child_set_material.setFont(0, self.font_internal)
        self.item_child_set_crossSection.setFont(0, self.font_internal)
        self.item_child_setPrescribedDofs.setFont(0, self.font_internal)
        self.item_child_setNodalLoads.setFont(0, self.font_internal)
        self.item_child_addMassSpringDamper.setFont(0, self.font_internal)
        self.item_child_setcappedEnd.setFont(0, self.font_internal)
        self.item_child_set_stress_stiffening.setFont(0, self.font_internal)
        self.item_child_add_elastic_nodal_links.setFont(0, self.font_internal)

        self.item_child_setAcousticElementType.setFont(0, self.font_internal)
        self.item_child_set_fluid.setFont(0, self.font_internal)
        self.item_child_setAcousticPressure.setFont(0, self.font_internal)
        self.item_child_setVolumeVelocity.setFont(0, self.font_internal)
        self.item_child_setSpecificImpedance.setFont(0, self.font_internal)
        self.item_child_set_radiation_impedance.setFont(0, self.font_internal)
        self.item_child_add_perforated_plate.setFont(0, self.font_internal)
        self.item_child_set_acoustic_element_length_correction.setFont(0, self.font_internal)
        self.item_child_add_compressor_excitation.setFont(0, self.font_internal)

        self.item_child_selectAnalysisType.setFont(0, self.font_internal)
        self.item_child_analisysSetup.setFont(0, self.font_internal)
        self.item_child_runAnalysis.setFont(0, self.font_internal)

        self.item_child_plotStructuralModeShapes.setFont(0, self.font_internal)
        self.item_child_plotDisplacementField.setFont(0, self.font_internal)
        self.item_child_plotStructuralFrequencyResponse.setFont(0, self.font_internal)
        self.item_child_plotReactionsFrequencyResponse.setFont(0, self.font_internal)
        self.item_child_plotStressField.setFont(0, self.font_internal)
        self.item_child_plotStressFrequencyResponse.setFont(0, self.font_internal)

        self.item_child_plotAcousticModeShapes.setFont(0, self.font_internal)
        self.item_child_plotAcousticPressureField.setFont(0, self.font_internal)
        self.item_child_plotAcousticFrequencyResponse.setFont(0, self.font_internal)
        self.item_child_plot_TL_NR.setFont(0, self.font_internal)

        # self.item_child_setStructuralElementType.setDisabled(True)
        #self.item_child_plotStressField.setDisabled(True)

    def _addItems(self):
        """Insert items on the TreeWidget."""
        self.addTopLevelItem(self.item_top_structuralmodelSetup)
        self.addTopLevelItem(self.item_child_setStructuralElementType)
        self.addTopLevelItem(self.item_child_set_material)
        self.addTopLevelItem(self.item_child_set_crossSection)
        self.addTopLevelItem(self.item_child_setPrescribedDofs)
        self.addTopLevelItem(self.item_child_setRotationDecoupling)
        self.addTopLevelItem(self.item_child_setNodalLoads)
        self.addTopLevelItem(self.item_child_addMassSpringDamper)
        self.addTopLevelItem(self.item_child_setcappedEnd)
        self.addTopLevelItem(self.item_child_set_stress_stiffening)
        self.addTopLevelItem(self.item_child_add_elastic_nodal_links)

        self.addTopLevelItem(self.item_top_acousticmodelSetup)  
        self.addTopLevelItem(self.item_child_setAcousticElementType)    
        self.addTopLevelItem(self.item_child_set_fluid)             
        self.addTopLevelItem(self.item_child_setAcousticPressure) 
        self.addTopLevelItem(self.item_child_setVolumeVelocity)     
        self.addTopLevelItem(self.item_child_setSpecificImpedance)
        self.addTopLevelItem(self.item_child_set_radiation_impedance)     
        self.addTopLevelItem(self.item_child_add_perforated_plate) 
        self.addTopLevelItem(self.item_child_set_acoustic_element_length_correction) 
        self.addTopLevelItem(self.item_child_add_compressor_excitation) 

        self.addTopLevelItem(self.item_top_analysis)
        self.addTopLevelItem(self.item_child_selectAnalysisType)
        self.addTopLevelItem(self.item_child_analisysSetup)
        self.addTopLevelItem(self.item_child_runAnalysis)

        self.addTopLevelItem(self.item_top_resultsViewer_structural)
        self.addTopLevelItem(self.item_child_plotStructuralModeShapes)
        self.addTopLevelItem(self.item_child_plotDisplacementField)
        self.addTopLevelItem(self.item_child_plotStructuralFrequencyResponse)
        self.addTopLevelItem(self.item_child_plotReactionsFrequencyResponse)
        self.addTopLevelItem(self.item_child_plotStressField)
        self.addTopLevelItem(self.item_child_plotStressFrequencyResponse)
        self.addTopLevelItem(self.item_top_resultsViewer_acoustic)
        self.addTopLevelItem(self.item_child_plotAcousticModeShapes)
        self.addTopLevelItem(self.item_child_plotAcousticPressureField)
        self.addTopLevelItem(self.item_child_plotAcousticFrequencyResponse)
        self.addTopLevelItem(self.item_child_plot_TL_NR)

        
    def on_click_item(self, item, column):
        """This event is raised every time an item is clicked on the menu."""
        self.mainWindow.getInputWidget().beforeInput()

        if item.text(0) == self.name_child_setStructuralElementType:
            self.mainWindow.getInputWidget().setStructuralElementType()

        elif item.text(0) == self.name_child_set_material:
            self.mainWindow.plot_entities()
            self.mainWindow.getInputWidget().set_material()

        elif item.text(0) == self.name_child_set_crossSection:
            self.mainWindow.getInputWidget().set_cross_section()
            self.mainWindow.plot_entities_radius()

        elif item.text(0) == self.name_child_setPrescribedDofs:
            self.mainWindow.plot_mesh()
            self.mainWindow.getInputWidget().setDOF()

        elif item.text(0) == self.name_child_setRotationDecoupling:
            self.mainWindow.plot_mesh()
            self.mainWindow.getInputWidget().setRotationDecoupling()

        elif item.text(0) == self.name_child_setNodalLoads:
            self.mainWindow.plot_mesh()
            self.mainWindow.getInputWidget().setNodalLoads()

        elif item.text(0) == self.name_child_addMassSpringDamper:
            self.mainWindow.plot_mesh()
            self.mainWindow.getInputWidget().addMassSpringDamper()

        elif item.text(0) == self.name_child_setcappedEnd:
            # self.mainWindow.plot_entities()
            self.mainWindow.getInputWidget().setcappedEnd()

        elif item.text(0) == self.name_child_set_stress_stiffening:
            # self.mainWindow.plot_entities()
            self.mainWindow.getInputWidget().set_stress_stress_stiffening()
        
        elif item.text(0) == self.name_child_add_elastic_nodal_links:
            self.mainWindow.plot_mesh()
            self.mainWindow.getInputWidget().add_elastic_nodal_links()

        elif item.text(0) == self.name_child_setAcousticElementType:
            self.mainWindow.plot_entities()
            self.mainWindow.getInputWidget().set_acoustic_element_type()

        elif item.text(0) == self.name_child_set_fluid: 
            self.mainWindow.plot_entities()
            self.mainWindow.getInputWidget().set_fluid()

        elif item.text(0) == self.name_child_setAcousticPressure:
            self.mainWindow.plot_mesh()
            self.mainWindow.getInputWidget().setAcousticPressure()

        elif item.text(0) == self.name_child_setVolumeVelocity: 
            self.mainWindow.plot_mesh()
            self.mainWindow.getInputWidget().setVolumeVelocity()

        elif item.text(0) == self.name_child_setSpecificImpedance:
            self.mainWindow.plot_mesh()
            self.mainWindow.getInputWidget().setSpecificImpedance()

        elif item.text(0) == self.name_child_set_radiation_impedance:
            self.mainWindow.plot_mesh()
            self.mainWindow.getInputWidget().set_radiation_impedance()

        elif item.text(0) == self.name_child_add_perforated_plate:
            self.mainWindow.plot_mesh()
            self.mainWindow.getInputWidget().add_perforated_plate()

        elif item.text(0) == self.name_child_set_acoustic_element_length_correction:
            self.mainWindow.plot_mesh()
            self.mainWindow.getInputWidget().set_acoustic_element_length_correction()

        elif item.text(0) == self.name_child_add_compressor_excitation:
            self.mainWindow.plot_mesh()
            self.mainWindow.getInputWidget().add_compressor_excitation()

        elif item.text(0) == self.name_child_selectAnalysisType:
            self.mainWindow.getInputWidget().analysisTypeInput()
            self._updateItems()
            
        elif item.text(0) == self.name_child_analisysSetup:
            if not self.item_child_analisysSetup.isDisabled():
                self.mainWindow.getInputWidget().analysisSetup()
                self._updateItems()

        elif item.text(0) == self.name_child_runAnalysis:
            if not self.item_child_runAnalysis.isDisabled():
                self.mainWindow.getInputWidget().runAnalysis()
                self._updateItems()

        elif item.text(0) == self.name_child_plotStructuralModeShapes:
            self.mainWindow.getInputWidget().plotStructuralModeShapes()

        elif item.text(0) == self.name_child_plotDisplacementField:
            self.mainWindow.getInputWidget().plotDisplacementField()

        elif item.text(0) == self.name_child_plotStructuralFrequencyResponse:
            self.mainWindow.getInputWidget().plotStructuralFrequencyResponse()

        elif item.text(0) == self.name_child_plotReactionsFrequencyResponse:
            self.mainWindow.getInputWidget().plotReactionsFrequencyResponse()

        elif item.text(0) == self.name_child_plotStressField:
            self.mainWindow.getInputWidget().plotStressField()

        elif item.text(0) == self.name_child_plotStressFrequencyResponse:
            self.mainWindow.getInputWidget().plotStressFrequencyResponse()

        elif item.text(0) == self.name_child_plotAcousticModeShapes:
            self.mainWindow.getInputWidget().plotAcousticModeShapes()

        elif item.text(0) == self.name_child_plotAcousticPressureField:
            self.mainWindow.getInputWidget().plotAcousticPressureField()
         
        elif item.text(0) == self.name_child_plotAcousticFrequencyResponse:
            self.mainWindow.getInputWidget().plotAcousticFrequencyResponse()

        elif item.text(0) == self.name_child_plot_TL_NR:
            self.mainWindow.getInputWidget().plot_TL_NR()


    def _updateItems(self):
        """Enable and disable items on menu when some condictions aren't satisfied."""
        if True:
            self.item_child_plotStructuralModeShapes.setDisabled(True)
            self.item_child_plotDisplacementField.setDisabled(True)
            self.item_child_plotStructuralFrequencyResponse.setDisabled(True)
            self.item_child_plotStressField.setDisabled(True)
            self.item_child_plotStressFrequencyResponse.setDisabled(True)
            self.item_child_plotAcousticModeShapes.setDisabled(True)
            self.item_child_plotAcousticFrequencyResponse.setDisabled(True)
            self.item_child_plotAcousticPressureField.setDisabled(True)
            self.item_child_plot_TL_NR.setDisabled(True)
            self.item_child_plotReactionsFrequencyResponse.setDisabled(True)
            self.item_child_analisysSetup.setDisabled(True)
            self.item_child_runAnalysis.setDisabled(True)
        
        if self.project.analysis_ID in [None, 2,4]:
            self.item_child_analisysSetup.setDisabled(True)
        else:
            self.item_child_analisysSetup.setDisabled(False)
        
        if self.project.analysis_ID not in [None] and self.project.setup_analysis_complete:
            self.item_child_runAnalysis.setDisabled(False)
        
        if self.project.get_structural_solution() is not None or self.project.get_acoustic_solution() is not None:
        
            if self.project.analysis_ID == 0 or self.project.analysis_ID == 1:
                self.item_child_plotStructuralFrequencyResponse.setDisabled(False)
                self.item_child_plotDisplacementField.setDisabled(False)
                self.item_child_plotReactionsFrequencyResponse.setDisabled(False)
                self.item_child_plotStressField.setDisabled(False)
                self.item_child_plotStressFrequencyResponse.setDisabled(False)
            elif self.project.analysis_ID == 2:
                self.item_child_plotStructuralModeShapes.setDisabled(False)
            elif self.project.analysis_ID == 4:
                self.item_child_plotAcousticModeShapes.setDisabled(False)
            elif self.project.analysis_ID == 3:
                self.item_child_plotAcousticFrequencyResponse.setDisabled(False)
                self.item_child_plotAcousticPressureField.setDisabled(False)
                self.item_child_plot_TL_NR.setDisabled(False)
            elif self.project.analysis_ID in [5,6]:
                self.item_child_plotStructuralFrequencyResponse.setDisabled(False)
                self.item_child_plotAcousticFrequencyResponse.setDisabled(False)
                self.item_child_plotStressField.setDisabled(False)
                self.item_child_plotStressFrequencyResponse.setDisabled(False)
                self.item_child_plotDisplacementField.setDisabled(False)
                self.item_child_plotAcousticPressureField.setDisabled(False)
                self.item_child_plot_TL_NR.setDisabled(False)
                self.item_child_plotReactionsFrequencyResponse.setDisabled(False)  