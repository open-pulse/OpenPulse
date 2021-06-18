from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QStyledItemDelegate, QFrame
from PyQt5.QtGui import QBrush, QColor, QFont, QIcon, QPixmap, QPainter, QPen, QLinearGradient
from PyQt5.QtCore import Qt, QSize, QRect
from data.user_input.project.printMessageInput import PrintMessageInput


class BorderItemDelegate(QStyledItemDelegate):
    def __init__(self, parent, borderRole):
        super(BorderItemDelegate, self).__init__(parent)
        self.borderRole = borderRole

    def sizeHint(self, option, index):        
        size = super(BorderItemDelegate, self).sizeHint(option, index)
        pen = index.data(self.borderRole)
        if pen is not None:        
            # Make some room for the border
            # When width is 0, it is a cosmetic pen which
            # will be 1 pixel anyways, so set it to 1
            width = max(pen.width(), 1)            
            size = size + QSize(2 * width, 2 * width)
        return size
    
    def size(self, item):
        separator_size = QSize()
        separator_size.setHeight(2)
        return item.setSizeHint(0, separator_size)

    def paint(self, painter, option, index):
        pen = index.data(self.borderRole)
        rect = QRect(option.rect)

        if pen is not None:
            width = max(pen.width(), 1)
            # ...and remove the extra room we added in sizeHint...
            option.rect.adjust(width, width, -width, -width)      

        super(BorderItemDelegate, self).paint(painter, option, index)

        if pen is not None:
            painter.save() # Saves previous status
            
            # Align rect 
            painter.setClipRect(rect, Qt.ReplaceClip);          
            pen.setWidth(2 * width)

            # Paint the borders
            painter.setPen(pen)
            painter.drawRect(rect)     
            
            painter.restore() # Recovers previous status


class MenuItems(QTreeWidget):
    """Menu Items

    This class is responsible for creating, configuring and building the items
    in the items menu, located on the left side of the interface.

    """
    def __init__(self, main_window):
        super().__init__()
        self.mainWindow = main_window
        self.project = main_window.getProject()
        
        self._createIcons()
        self._configItemSizes()
        self._createFonts()
        self._createColorsBrush()
        self._configTree()
        self._createItems()
        self._addItems()
        self._configItems()
        self._updateItems()

    def keyPressEvent(self, event):
        """This deals with key events that are directly linked with the menu."""
        if event.key() == Qt.Key_F5:
            self.mainWindow.getInputWidget().runAnalysis()
            self._updateItems()

    def _createIcons(self):
        """Create Icons objects that are placed on the right side of the item.
            Currently isn't used.
        """
        self.icon_child_set_material = QIcon()
        self.icon_child_set_material.addPixmap(QPixmap("data/icons/pulse.png"), QIcon.Active, QIcon.On)

    def _createFonts(self):
        """Create Font objects that configure the font of the items."""
        self.font_top = QFont()
        self.font_top.setFamily("Segoe UI")
        self.font_top.setPointSize(13)
        self.font_top.setBold(True)
        self.font_top.setItalic(False)
        self.font_top.setWeight(75)

        self.font_child = QFont()
        self.font_child.setFamily("Segoe UI")
        self.font_child.setPointSize(12)
        #self.font_child.setBold(False)
        #self.font_child.setItalic(True)
        #self.font_child.setWeight(75)

    def _createColorsBrush(self):
        """Create Color objects that define the color of the text and/or background of the items."""
        
        self.QLinearGradient_model = QLinearGradient(0,0,400,0)
        self.QLinearGradient_model.setColorAt(0, QColor(60, 60, 60, 150))
        self.QLinearGradient_model.setColorAt(1, QColor(220, 220, 220, 150))

        self.QLinearGradient_viewer = QLinearGradient(0,0,400,0)
        self.QLinearGradient_viewer.setColorAt(0, QColor(102, 204, 255, 100))
        self.QLinearGradient_viewer.setColorAt(1, QColor(240, 240, 240, 150))

        self.brush_top = QBrush(self.QLinearGradient_model)
        self.brush_top.setStyle(Qt.LinearGradientPattern)
        
        self.color_item_results_viewer = QBrush(self.QLinearGradient_viewer)
        self.color_item_results_viewer.setStyle(Qt.LinearGradientPattern)

    def _configItemSizes(self):
        self.separator_size = QSize()
        self.separator_size.setHeight(2)

    def _configTree(self):
        """Define the initial configuration of the TreeWidget."""
  
        self.setHeaderHidden(True)
        self.setTabKeyNavigation(True)
        self.setRootIsDecorated(True)
        self.setFrameShape(1)
        # self.setFrameShadow(3)
        self.setLineWidth(2)
        # self.setStyleSheet("QTreeWidget{alternate-background-color: red; background: black;}")

        # self.setAutoExpandDelay(0)
        # self.setTreePosition(-1)
        # self.setIndentation(20)
        # self.setColumnWidth(0, 50)
        self.itemClicked.connect(self.on_click_item)

    def _createItems(self):
        """Create all TreeWidgetItems."""
        self.item_top_generalSettings = QTreeWidgetItem(['General Settings'])
        self.item_child_setProjectAttributes = QTreeWidgetItem(['Set Project Attributes'])
        self.item_child_setGeometryFile = QTreeWidgetItem(['Set Geometry File'])
        self.item_child_setMeshProperties = QTreeWidgetItem(['Set Mesh Properties'])
        self.item_child_set_material = QTreeWidgetItem(['Set Material'])
        self.item_child_set_crossSection = QTreeWidgetItem(['Set Cross-Section'])
        #
        self.item_top_structuralModelSetup = QTreeWidgetItem(['Structural Mode Setup'])
        self.item_child_setStructuralElementType = QTreeWidgetItem(['Set Structural Element Type'])
        self.item_child_setBeamXaxisRotation = QTreeWidgetItem(['Set Beam X-axis Rotation'])
        self.item_child_setRotationDecoupling = QTreeWidgetItem(['Set Rotation Decoupling'])
        self.item_child_setPrescribedDofs = QTreeWidgetItem(['Set Prescribed DOFs'])
        self.item_child_setNodalLoads = QTreeWidgetItem(['Set Nodal Loads'])
        self.item_child_addMassSpringDamper = QTreeWidgetItem(['Add: Mass / Spring / Damper'])
        self.item_child_add_elastic_nodal_links = QTreeWidgetItem(['Add Elastic Nodal Links'])
        self.item_child_setcappedEnd = QTreeWidgetItem(['Set Capped End'])
        self.item_child_set_stress_stiffening = QTreeWidgetItem(['Set Stress Stiffening'])
        #
        self.item_top_acousticModelSetup = QTreeWidgetItem(['Acoustic Model Setup'])
        self.item_child_setAcousticElementType = QTreeWidgetItem(['Set Acoustic Element Type'])
        self.item_child_set_fluid = QTreeWidgetItem(['Set Fluid'])
        self.item_child_setAcousticPressure = QTreeWidgetItem(['Set Acoustic Pressure'])
        self.item_child_setVolumeVelocity = QTreeWidgetItem(['Set Volume Velocity'])
        self.item_child_setSpecificImpedance = QTreeWidgetItem(['Set Specific Impedance'])
        self.item_child_set_radiation_impedance = QTreeWidgetItem(['Set Radiation Impedance'])
        self.item_child_add_perforated_plate = QTreeWidgetItem(['Add Perforated Plate'])
        self.item_child_set_acoustic_element_length_correction = QTreeWidgetItem(['Set Element Length Correction'])
        self.item_child_add_compressor_excitation = QTreeWidgetItem(['Add Compressor Excitation'])
        #
        self.item_top_analysis = QTreeWidgetItem(['Analysis'])
        self.item_child_selectAnalysisType = QTreeWidgetItem(['Select Analysis Type'])
        self.item_child_analisysSetup = QTreeWidgetItem(['Analysis Setup'])
        self.item_child_runAnalysis = QTreeWidgetItem(['Run Analysis (F5)'])
        #
        self.item_top_resultsViewer_structural = QTreeWidgetItem(['Results Viewer - Structural'])
        self.item_child_plotStructuralModeShapes = QTreeWidgetItem(['Plot Structural Mode Shapes'])
        self.item_child_plotDisplacementField = QTreeWidgetItem(['Plot Displacement Field'])
        self.item_child_plotStructuralFrequencyResponse = QTreeWidgetItem(['Plot Structural Frequency Response'])
        self.item_child_plotReactionsFrequencyResponse = QTreeWidgetItem(['Plot Reactions Frequency Response'])
        self.item_child_plotStressField = QTreeWidgetItem(['Plot Stress Field'])
        self.item_child_plotStressFrequencyResponse = QTreeWidgetItem(['Plot Stress Frequency Response'])
        #
        self.item_top_resultsViewer_acoustic = QTreeWidgetItem(['Results Viewer - Acoustic'])
        self.item_child_plotAcousticModeShapes = QTreeWidgetItem(['Plot Acoustic Mode Shapes'])
        self.item_child_plotAcousticPressureField = QTreeWidgetItem(['Plot Acoustic Pressure Field'])
        self.item_child_plotAcousticFrequencyResponse = QTreeWidgetItem(['Plot Acoustic Frequency Response'])
        self.item_child_plot_TL_NR = QTreeWidgetItem(['Plot Transmission Loss or Attenuation'])
        #
        self.item_top_separator = QTreeWidgetItem([""])

    def _addItems(self):
        self.addTopLevelItem(self.item_top_generalSettings)
        self.item_top_generalSettings.addChild(self.item_child_setProjectAttributes)
        self.item_top_generalSettings.addChild(self.item_child_setMeshProperties)
        self.item_top_generalSettings.addChild(self.item_child_setGeometryFile)
        self.item_top_generalSettings.addChild(self.item_child_set_material)
        self.item_top_generalSettings.addChild(self.item_child_set_crossSection)
        
        self.addTopLevelItem(self.item_top_structuralModelSetup)
        self.item_top_structuralModelSetup.addChild(self.item_child_setStructuralElementType)
        self.item_top_structuralModelSetup.addChild(self.item_child_setBeamXaxisRotation)
        self.item_top_structuralModelSetup.addChild(self.item_child_setPrescribedDofs)
        self.item_top_structuralModelSetup.addChild(self.item_child_setRotationDecoupling)
        self.item_top_structuralModelSetup.addChild(self.item_child_setNodalLoads)
        self.item_top_structuralModelSetup.addChild(self.item_child_addMassSpringDamper)
        self.item_top_structuralModelSetup.addChild(self.item_child_add_elastic_nodal_links)
        self.item_top_structuralModelSetup.addChild(self.item_child_set_stress_stiffening)
        self.item_top_structuralModelSetup.addChild(self.item_child_setcappedEnd)
        
        self.addTopLevelItem(self.item_top_acousticModelSetup)
        self.item_top_acousticModelSetup.addChild(self.item_child_setAcousticElementType)    
        self.item_top_acousticModelSetup.addChild(self.item_child_set_fluid)             
        self.item_top_acousticModelSetup.addChild(self.item_child_setAcousticPressure) 
        self.item_top_acousticModelSetup.addChild(self.item_child_setVolumeVelocity)     
        self.item_top_acousticModelSetup.addChild(self.item_child_setSpecificImpedance)
        self.item_top_acousticModelSetup.addChild(self.item_child_set_radiation_impedance)     
        self.item_top_acousticModelSetup.addChild(self.item_child_add_perforated_plate) 
        self.item_top_acousticModelSetup.addChild(self.item_child_set_acoustic_element_length_correction) 
        self.item_top_acousticModelSetup.addChild(self.item_child_add_compressor_excitation) 
        
        self.addTopLevelItem(self.item_top_analysis)
        self.item_top_analysis.addChild(self.item_child_selectAnalysisType)
        self.item_top_analysis.addChild(self.item_child_analisysSetup)
        self.item_top_analysis.addChild(self.item_child_runAnalysis)
        
        self.addTopLevelItem(self.item_top_resultsViewer_structural)
        self.item_top_resultsViewer_structural.addChild(self.item_child_plotStructuralModeShapes)
        self.item_top_resultsViewer_structural.addChild(self.item_child_plotDisplacementField)
        self.item_top_resultsViewer_structural.addChild(self.item_child_plotStructuralFrequencyResponse)
        self.item_top_resultsViewer_structural.addChild(self.item_child_plotReactionsFrequencyResponse)
        self.item_top_resultsViewer_structural.addChild(self.item_child_plotStressField)
        self.item_top_resultsViewer_structural.addChild(self.item_child_plotStressFrequencyResponse)
        
        self.addTopLevelItem(self.item_top_resultsViewer_acoustic)
        self.item_top_resultsViewer_acoustic.addChild(self.item_child_plotAcousticModeShapes)
        self.item_top_resultsViewer_acoustic.addChild(self.item_child_plotAcousticPressureField)
        self.item_top_resultsViewer_acoustic.addChild(self.item_child_plotAcousticFrequencyResponse)
        self.item_top_resultsViewer_acoustic.addChild(self.item_child_plot_TL_NR)     

    def _configItems(self):
        """Configure all items."""   

        borderRole = Qt.UserRole + 1
        borderPen = QPen(QColor(0,0,0))
        borderPen.setWidth(1)

        textTopBrush = QBrush(QColor(0,0,0))
        configTopBrush = self.brush_top
        plotTopBrush = self.color_item_results_viewer
        topFont = self.font_top

        configTopItems = [self.item_top_generalSettings, self.item_top_structuralModelSetup, 
                          self.item_top_acousticModelSetup, self.item_top_analysis]

        plotTopItems = [self.item_top_resultsViewer_structural, self.item_top_resultsViewer_acoustic]

        for item in configTopItems:
            item.setFlags(Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
            item.setFont(0, topFont)
            item.setData(0, borderRole, borderPen)
            item.setTextAlignment(0, Qt.AlignHCenter)
            item.setForeground(0, textTopBrush)
            item.setBackground(0, configTopBrush)
            self.expandItem(item)

        for item in plotTopItems:
            item.setFlags(Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
            item.setFont(0, topFont)
            item.setData(0, borderRole, borderPen)
            item.setTextAlignment(0, Qt.AlignHCenter)
            item.setForeground(0, textTopBrush)
            item.setBackground(0, plotTopBrush)

        delegate = BorderItemDelegate(self, borderRole)
        self.setItemDelegate(delegate)

        self.item_child_setProjectAttributes.setFont(0, self.font_child)
        self.item_child_setMeshProperties.setFont(0, self.font_child)
        self.item_child_setGeometryFile.setFont(0, self.font_child)

        self.item_child_setStructuralElementType.setFont(0, self.font_child)
        self.item_child_setBeamXaxisRotation.setFont(0, self.font_child)
        self.item_child_setRotationDecoupling.setFont(0, self.font_child)
        self.item_child_set_material.setFont(0, self.font_child)
        self.item_child_set_crossSection.setFont(0, self.font_child)
        self.item_child_setPrescribedDofs.setFont(0, self.font_child)
        self.item_child_setNodalLoads.setFont(0, self.font_child)
        self.item_child_addMassSpringDamper.setFont(0, self.font_child)
        self.item_child_setcappedEnd.setFont(0, self.font_child)
        self.item_child_set_stress_stiffening.setFont(0, self.font_child)
        self.item_child_add_elastic_nodal_links.setFont(0, self.font_child)

        self.item_child_setAcousticElementType.setFont(0, self.font_child)
        self.item_child_set_fluid.setFont(0, self.font_child)
        self.item_child_setAcousticPressure.setFont(0, self.font_child)
        self.item_child_setVolumeVelocity.setFont(0, self.font_child)
        self.item_child_setSpecificImpedance.setFont(0, self.font_child)
        self.item_child_set_radiation_impedance.setFont(0, self.font_child)
        self.item_child_add_perforated_plate.setFont(0, self.font_child)
        self.item_child_set_acoustic_element_length_correction.setFont(0, self.font_child)
        self.item_child_add_compressor_excitation.setFont(0, self.font_child)

        self.item_child_selectAnalysisType.setFont(0, self.font_child)
        self.item_child_analisysSetup.setFont(0, self.font_child)
        self.item_child_runAnalysis.setFont(0, self.font_child)

        self.item_child_plotStructuralModeShapes.setFont(0, self.font_child)
        self.item_child_plotDisplacementField.setFont(0, self.font_child)
        self.item_child_plotStructuralFrequencyResponse.setFont(0, self.font_child)
        self.item_child_plotReactionsFrequencyResponse.setFont(0, self.font_child)
        self.item_child_plotStressField.setFont(0, self.font_child)
        self.item_child_plotStressFrequencyResponse.setFont(0, self.font_child)

        self.item_child_plotAcousticModeShapes.setFont(0, self.font_child)
        self.item_child_plotAcousticPressureField.setFont(0, self.font_child)
        self.item_child_plotAcousticFrequencyResponse.setFont(0, self.font_child)
        self.item_child_plot_TL_NR.setFont(0, self.font_child)

    def update_plot_mesh(self):
        if not self.mainWindow.opv_widget.change_plot_to_mesh:
            self.mainWindow.plot_mesh()

    def update_plot_entities(self):
        if not self.mainWindow.opv_widget.change_plot_to_entities:
            self.mainWindow.plot_entities()  

    def update_plot_entities_with_cross_section(self):
        if not self.mainWindow.opv_widget.change_plot_to_entities_with_cross_section:
            self.mainWindow.plot_entities_with_cross_section()      

    def update_childItems_visibility(self, item):
        toggle = lambda x: x.setExpanded(not x.isExpanded())

        expandable = [self.item_top_generalSettings, self.item_top_structuralModelSetup,
                      self.item_top_acousticModelSetup, self.item_top_resultsViewer_structural, 
                      self.item_top_analysis, self.item_top_resultsViewer_acoustic]

        if item in expandable:
            toggle(item)
            return True 

        return False

    def on_click_item(self, item, column):
        """This event is raised every time an item is clicked on the menu."""
        self.mainWindow.getInputWidget().beforeInput()

        if self.update_childItems_visibility(item):
            return

        if self.project.none_project_action:           
            self.empty_project_action_message()
        
        if item == self.item_child_setProjectAttributes:
            if not self.item_child_setProjectAttributes.isDisabled():
                self.mainWindow.getInputWidget().set_project_attributes()

        if item == self.item_child_setGeometryFile:
            if not self.item_child_setGeometryFile.isDisabled():
                self.mainWindow.getInputWidget().set_geometry_file()

        if item == self.item_child_setMeshProperties:
            if not self.item_child_setMeshProperties.isDisabled():
                self.mainWindow.getInputWidget().set_mesh_properties()

        elif item == self.item_child_setStructuralElementType:
            if not self.item_child_setStructuralElementType.isDisabled():
                self.update_plot_entities()
                self.mainWindow.getInputWidget().setStructuralElementType()

        elif item == self.item_child_setBeamXaxisRotation:
            if not self.item_child_setBeamXaxisRotation.isDisabled():
                self.update_plot_entities_with_cross_section()
                self.mainWindow.getInputWidget().set_beam_xaxis_rotation()

        elif item == self.item_child_set_material:
            if not self.item_child_set_material.isDisabled():
                self.update_plot_entities()
                self.mainWindow.getInputWidget().set_material()
                self.mainWindow.plot_entities()

        elif item == self.item_child_set_crossSection:
            if not self.item_child_set_crossSection.isDisabled():
                self.update_plot_entities()
                if self.mainWindow.getInputWidget().set_cross_section():
                    self.mainWindow.plot_entities_with_cross_section()

        elif item == self.item_child_setPrescribedDofs:
            if not self.item_child_setPrescribedDofs.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().setDOF()
                self.mainWindow.plot_mesh()

        elif item == self.item_child_setRotationDecoupling:
            if not self.item_child_setRotationDecoupling.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().setRotationDecoupling()
                self.mainWindow.plot_mesh()

        elif item == self.item_child_setNodalLoads:
            if not self.item_child_setNodalLoads.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().setNodalLoads()
                self.mainWindow.plot_mesh()

        elif item == self.item_child_addMassSpringDamper:
            if not self.item_child_addMassSpringDamper.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().addMassSpringDamper()
                self.mainWindow.plot_mesh()

        elif item == self.item_child_setcappedEnd:
             if not self.item_child_setcappedEnd.isDisabled():
                # self.update_plot_entities()
                self.mainWindow.getInputWidget().setcappedEnd()
                # self.mainWindow.plot_entities()

        elif item == self.item_child_set_stress_stiffening:
            if not self.item_child_set_stress_stiffening.isDisabled():
                # self.update_plot_entities()
                self.mainWindow.getInputWidget().set_stress_stress_stiffening()
                # self.mainWindow.plot_entities()
        
        elif item == self.item_child_add_elastic_nodal_links:
            if not self.item_child_add_elastic_nodal_links.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().add_elastic_nodal_links()
                self.mainWindow.plot_mesh()

        elif item == self.item_child_setAcousticElementType:
            if not self.item_child_setAcousticElementType.isDisabled():
                self.update_plot_entities()
                self.mainWindow.getInputWidget().set_acoustic_element_type()
                self.mainWindow.plot_entities()

        elif item == self.item_child_set_fluid:
            if not self.item_child_set_fluid.isDisabled(): 
                self.update_plot_entities()
                self.mainWindow.getInputWidget().set_fluid()
                self.mainWindow.plot_entities()

        elif item == self.item_child_setAcousticPressure:
            if not self.item_child_setAcousticPressure.isDisabled():
                self.update_plot_mesh()      
                self.mainWindow.getInputWidget().setAcousticPressure()
                self.mainWindow.plot_mesh()

        elif item == self.item_child_setVolumeVelocity:
            if not self.item_child_setVolumeVelocity.isDisabled(): 
                self.update_plot_mesh()  
                self.mainWindow.getInputWidget().setVolumeVelocity()
                self.mainWindow.plot_mesh()

        elif item == self.item_child_setSpecificImpedance:
            if not self.item_child_setSpecificImpedance.isDisabled():
                self.update_plot_mesh() 
                self.mainWindow.getInputWidget().setSpecificImpedance()
                self.mainWindow.plot_mesh()

        elif item == self.item_child_set_radiation_impedance:
            if not self.item_child_set_radiation_impedance.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().set_radiation_impedance()
                self.mainWindow.plot_mesh()

        elif item == self.item_child_add_perforated_plate:
            if not self.item_child_add_perforated_plate.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().add_perforated_plate()
                self.mainWindow.plot_mesh()

        elif item == self.item_child_set_acoustic_element_length_correction:
            if not self.item_child_set_acoustic_element_length_correction.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().set_acoustic_element_length_correction()
                self.mainWindow.plot_mesh()

        elif item == self.item_child_add_compressor_excitation:
            if not self.item_child_add_compressor_excitation.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().add_compressor_excitation()
                self.mainWindow.plot_mesh()

        elif item == self.item_child_selectAnalysisType:
            if not self.item_child_selectAnalysisType.isDisabled():
                self.mainWindow.getInputWidget().analysisTypeInput()
                self._updateItems()
            
        elif item == self.item_child_analisysSetup:
            if not self.item_child_analisysSetup.isDisabled():
                self.mainWindow.getInputWidget().analysisSetup()
                self._updateItems()

        elif item == self.item_child_runAnalysis:
            if not self.item_child_runAnalysis.isDisabled():
                self.mainWindow.getInputWidget().runAnalysis()
                self._updateItems()

        elif item == self.item_child_plotStructuralModeShapes:
            if not self.item_child_plotStructuralModeShapes.isDisabled():
                self.mainWindow.getInputWidget().plotStructuralModeShapes()

        elif item == self.item_child_plotDisplacementField:
            if not self.item_child_plotDisplacementField.isDisabled():
                self.mainWindow.getInputWidget().plotDisplacementField()

        elif item == self.item_child_plotStructuralFrequencyResponse:
            if not self.item_child_plotStructuralFrequencyResponse.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().plotStructuralFrequencyResponse()

        elif item == self.item_child_plotReactionsFrequencyResponse:
            if not self.item_child_plotReactionsFrequencyResponse.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().plotReactionsFrequencyResponse()

        elif item == self.item_child_plotStressField:
            if not self.item_child_plotStressField.isDisabled():
                self.mainWindow.getInputWidget().plotStressField()

        elif item == self.item_child_plotStressFrequencyResponse:
            if not self.item_child_plotStressFrequencyResponse.isDisabled():
                self.update_plot_mesh()  
                self.mainWindow.getInputWidget().plotStressFrequencyResponse()

        elif item == self.item_child_plotAcousticModeShapes:
            if not self.item_child_plotAcousticModeShapes.isDisabled():
                self.mainWindow.getInputWidget().plotAcousticModeShapes()

        elif item == self.item_child_plotAcousticPressureField:
            if not self.item_child_plotAcousticPressureField.isDisabled():
                self.mainWindow.getInputWidget().plotAcousticPressureField()
         
        elif item == self.item_child_plotAcousticFrequencyResponse:
            if not self.item_child_plotAcousticFrequencyResponse.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().plotAcousticFrequencyResponse()

        elif item == self.item_child_plot_TL_NR:
            if not self.item_child_plot_TL_NR.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().plot_TL_NR()

    def modify_model_setup_items_access(self, bool_key):
        #
        self.item_child_setProjectAttributes.setDisabled(bool_key)
        self.item_child_setGeometryFile.setDisabled(bool_key)
        self.item_child_setMeshProperties.setDisabled(bool_key)
        #
        self.item_child_setStructuralElementType.setDisabled(bool_key)
        self.item_child_set_material.setDisabled(bool_key)
        self.item_child_set_crossSection.setDisabled(bool_key)
        self.item_child_setBeamXaxisRotation.setDisabled(bool_key)
        self.item_child_setPrescribedDofs.setDisabled(bool_key)
        self.item_child_setRotationDecoupling.setDisabled(bool_key)
        self.item_child_setNodalLoads.setDisabled(bool_key)
        self.item_child_addMassSpringDamper.setDisabled(bool_key)
        self.item_child_setcappedEnd.setDisabled(bool_key)
        self.item_child_set_stress_stiffening.setDisabled(bool_key)
        self.item_child_add_elastic_nodal_links.setDisabled(bool_key)   
        #   
        self.item_child_setAcousticElementType.setDisabled(bool_key)
        self.item_child_set_fluid.setDisabled(bool_key)
        self.item_child_setAcousticPressure.setDisabled(bool_key)
        self.item_child_setVolumeVelocity.setDisabled(bool_key)
        self.item_child_setSpecificImpedance.setDisabled(bool_key)
        self.item_child_set_radiation_impedance.setDisabled(bool_key)
        self.item_child_add_perforated_plate.setDisabled(bool_key)
        self.item_child_set_acoustic_element_length_correction.setDisabled(bool_key)
        self.item_child_add_compressor_excitation.setDisabled(bool_key)
        #
        self.item_child_selectAnalysisType.setDisabled(bool_key)

    def _updateItems(self):
        """Enable and disable items on menu when some condictions are not satisfied."""
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

    def empty_project_action_message(self):
        title = 'EMPTY PROJECT'
        message = 'Please, you should create a new project or load an already existing one before start to set up the model.'
        message += "\n\nIt is recommended to use the 'New Project' or the 'Import Project' buttons to continue."
        window_title = 'ERROR'
        PrintMessageInput([title, message, window_title], opv=self.mainWindow.getOPVWidget())