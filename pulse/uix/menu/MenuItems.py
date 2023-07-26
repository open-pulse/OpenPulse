from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pathlib import Path

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
        
        # self._createIcons()
        # self._configItemSizes()
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
        path = str(Path('data/icons/pulse.png'))
        self.icon_child_set_material = QIcon()
        self.icon_child_set_material.addPixmap(QPixmap(path), QIcon.Active, QIcon.On)

    def _createFonts(self):
        """Create Font objects that configure the font of the items."""
        self.font_top_Items = QFont()
        # self.font_top_Items.setFamily("Segoe UI")
        self.font_top_Items.setPointSize(12)
        # self.font_top_Items.setBold(False)
        # self.font_top_Items.setItalic(False)
        self.font_top_Items.setWeight(60)

        self.font_child_Items = QFont()
        # self.font_child_Items.setFamily("Segoe UI")
        self.font_child_Items.setPointSize(11)
        #self.font_child_Items.setBold(False)
        #self.font_child_Items.setItalic(True)
        self.font_child_Items.setWeight(50)

    def _createColorsBrush(self):
        """Create Color objects that define the color of the text and/or background of the items."""
        
        self.QLinearGradient_upper = QLinearGradient(0,0,400,0)
        self.QLinearGradient_upper.setColorAt(1, QColor(60, 60, 60, 150))
        self.QLinearGradient_upper.setColorAt(0, QColor(220, 220, 220, 150))

        self.QLinearGradient_lower = QLinearGradient(0,0,400,0)
        self.QLinearGradient_lower.setColorAt(1, QColor(102, 204, 255, 100))
        self.QLinearGradient_lower.setColorAt(0, QColor(240, 240, 240, 150))

        self.brush_upper_items = QBrush(self.QLinearGradient_upper)
        self.brush_upper_items.setStyle(Qt.LinearGradientPattern)
        
        self.brush_lower_items = QBrush(self.QLinearGradient_lower)
        self.brush_lower_items.setStyle(Qt.LinearGradientPattern)

    def _configItemSizes(self):
        """Creates a control to the items height size."""
        self.top_items_size = QSize()
        self.top_items_size.setHeight(35)
        self.child_items_size = QSize()
        self.child_items_size.setHeight(20)

    def _configTree(self):
        """Define the initial configuration of the TreeWidget."""
        self.setHeaderHidden(True)
        self.setTabKeyNavigation(True)
        self.setRootIsDecorated(True)
        self.setFrameShape(1)
        # self.setFrameShadow(3)
        self.setLineWidth(2)
        # self.setStyleSheet("QTreeWidget{alternate-background-color: red; background: black;}")
        # self.setIndentation(20)
        # self.setColumnWidth(0, 50)
        self.itemClicked.connect(self.on_click_item)

    def _createItems(self):
        """Creates all TreeWidgetItems."""
        self.list_top_items = []
        self.list_child_items = []
        self.item_top_generalSettings = QTreeWidgetItem(['General Settings'])
        self.item_child_createGeometry = QTreeWidgetItem(['Create/Edit Geometry'])
        self.item_child_editGeometry = QTreeWidgetItem(['Edit Geometry (GMSH GUI)'])
        self.item_child_setProjectAttributes = QTreeWidgetItem(['Set Project Attributes'])
        self.item_child_setGeometryFile = QTreeWidgetItem(['Set Geometry File'])
        self.item_child_setMeshProperties = QTreeWidgetItem(['Set Mesh Properties'])
        self.item_child_set_material = QTreeWidgetItem(['Set Material'])
        self.item_child_set_fluid = QTreeWidgetItem(['Set Fluid'])
        self.item_child_set_crossSection = QTreeWidgetItem(['Set Cross-Section'])
        #
        self.list_top_items.append(self.item_top_generalSettings)
        self.list_child_items.append(self.item_child_createGeometry)
        self.list_child_items.append(self.item_child_editGeometry)
        self.list_child_items.append(self.item_child_setProjectAttributes)
        self.list_child_items.append(self.item_child_setGeometryFile)
        self.list_child_items.append(self.item_child_setGeometryFile)
        self.list_child_items.append(self.item_child_setMeshProperties)
        self.list_child_items.append(self.item_child_set_material)
        self.list_child_items.append(self.item_child_set_fluid)
        self.list_child_items.append(self.item_child_set_crossSection)
        #
        self.item_top_structuralModelSetup = QTreeWidgetItem(['Structural Model Setup'])
        self.item_child_setStructuralElementType = QTreeWidgetItem(['Set Structural Element Type'])
        self.item_child_setPrescribedDofs = QTreeWidgetItem(['Set Prescribed DOFs'])
        self.item_child_setNodalLoads = QTreeWidgetItem(['Set Nodal Loads'])
        self.item_child_addMassSpringDamper = QTreeWidgetItem(['Add: Mass / Spring / Damper'])
        self.item_child_add_elastic_nodal_links = QTreeWidgetItem(['Add Elastic Nodal Links'])
        self.item_child_set_inertial_loads = QTreeWidgetItem(['Set Inertial Loads'])
        self.item_child_set_stress_stiffening = QTreeWidgetItem(['Set Stress Stiffening'])
        self.item_child_setcappedEnd = QTreeWidgetItem(['Set Capped End'])
        self.item_child_add_valve = QTreeWidgetItem(['Add Valve'])
        self.item_child_addFlanges = QTreeWidgetItem(['Add Connecting Flanges'])
        self.item_child_add_expansion_joint = QTreeWidgetItem(['Add Expansion Joint'])
        self.item_child_setBeamXaxisRotation = QTreeWidgetItem(['Set Beam X-axis Rotation'])
        self.item_child_setRotationDecoupling = QTreeWidgetItem(['Set Rotation Decoupling'])
        #
        self.list_top_items.append(self.item_top_structuralModelSetup)
        self.list_child_items.append(self.item_child_setStructuralElementType)
        self.list_child_items.append(self.item_child_setPrescribedDofs)
        self.list_child_items.append(self.item_child_setNodalLoads)
        self.list_child_items.append(self.item_child_addMassSpringDamper)
        self.list_child_items.append(self.item_child_add_elastic_nodal_links)
        self.list_child_items.append(self.item_child_set_inertial_loads)
        self.list_child_items.append(self.item_child_set_stress_stiffening)
        self.list_child_items.append(self.item_child_setcappedEnd)        
        self.list_child_items.append(self.item_child_add_valve)
        self.list_child_items.append(self.item_child_addFlanges)
        self.list_child_items.append(self.item_child_add_expansion_joint)
        self.list_child_items.append(self.item_child_setBeamXaxisRotation)
        self.list_child_items.append(self.item_child_setRotationDecoupling)
        #
        self.item_top_acousticModelSetup = QTreeWidgetItem(['Acoustic Model Setup'])
        self.item_child_setAcousticElementType = QTreeWidgetItem(['Set Acoustic Element Type'])
        self.item_child_setAcousticPressure = QTreeWidgetItem(['Set Acoustic Pressure'])
        self.item_child_setVolumeVelocity = QTreeWidgetItem(['Set Volume Velocity'])
        self.item_child_setSpecificImpedance = QTreeWidgetItem(['Set Specific Impedance'])
        self.item_child_set_radiation_impedance = QTreeWidgetItem(['Set Radiation Impedance'])
        self.item_child_add_perforated_plate = QTreeWidgetItem(['Add Perforated Plate'])
        self.item_child_set_acoustic_element_length_correction = QTreeWidgetItem(['Set Element Length Correction'])
        self.item_child_add_compressor_excitation = QTreeWidgetItem(['Add Compressor Excitation'])
        #
        self.list_top_items.append(self.item_top_acousticModelSetup)
        self.list_child_items.append(self.item_child_setAcousticElementType)
        self.list_child_items.append(self.item_child_setAcousticPressure)
        self.list_child_items.append(self.item_child_setVolumeVelocity)
        self.list_child_items.append(self.item_child_setSpecificImpedance)
        self.list_child_items.append(self.item_child_set_radiation_impedance)
        self.list_child_items.append(self.item_child_add_perforated_plate)
        self.list_child_items.append(self.item_child_set_acoustic_element_length_correction)
        self.list_child_items.append(self.item_child_add_compressor_excitation)
        #
        self.item_top_analysis = QTreeWidgetItem(['Analysis'])
        self.item_child_selectAnalysisType = QTreeWidgetItem(['Select Analysis Type'])
        self.item_child_analisysSetup = QTreeWidgetItem(['Analysis Setup'])
        self.item_child_runAnalysis = QTreeWidgetItem(['Run Analysis (F5)'])
        #
        self.list_top_items.append(self.item_top_analysis)
        self.list_child_items.append(self.item_child_selectAnalysisType)
        self.list_child_items.append(self.item_child_analisysSetup)
        self.list_child_items.append(self.item_child_runAnalysis)
        #
        self.item_top_resultsViewer_structural = QTreeWidgetItem(['Results Viewer - Structural'])
        self.item_child_plotStructuralModeShapes = QTreeWidgetItem(['Plot Structural Mode Shapes'])
        self.item_child_plotDisplacementField = QTreeWidgetItem(['Plot Displacement Field'])
        self.item_child_plotStructuralFrequencyResponse = QTreeWidgetItem(['Plot Structural Frequency Response'])
        self.item_child_plotReactionsFrequencyResponse = QTreeWidgetItem(['Plot Reactions Frequency Response'])
        self.item_child_plotStressField = QTreeWidgetItem(['Plot Stress Field'])
        self.item_child_plotStressFrequencyResponse = QTreeWidgetItem(['Plot Stress Frequency Response'])
        #
        self.list_top_items.append(self.item_top_resultsViewer_structural)
        self.list_child_items.append(self.item_child_plotStructuralModeShapes)
        self.list_child_items.append(self.item_child_plotDisplacementField)
        self.list_child_items.append(self.item_child_plotStructuralFrequencyResponse)
        self.list_child_items.append(self.item_child_plotReactionsFrequencyResponse)
        self.list_child_items.append(self.item_child_plotStressField)
        self.list_child_items.append(self.item_child_plotStressFrequencyResponse)
        #
        self.item_top_resultsViewer_acoustic = QTreeWidgetItem(['Results Viewer - Acoustic'])
        self.item_child_plotAcousticModeShapes = QTreeWidgetItem(['Plot Acoustic Mode Shapes'])
        self.item_child_plotAcousticPressureField = QTreeWidgetItem(['Plot Acoustic Pressure Field'])
        self.item_child_plotAcousticFrequencyResponse = QTreeWidgetItem(['Plot Acoustic Frequency Response'])
        self.item_child_plotAcousticDeltaPressures = QTreeWidgetItem(['Plot Acoustic Delta Pressures'])
        self.item_child_plot_TL_NR = QTreeWidgetItem(['Plot Transmission Loss or Attenuation'])
        self.item_child_plot_perforated_plate_convergence_data = QTreeWidgetItem(['Plot perforated plate convergence data'])
        #
        self.list_top_items.append(self.item_top_resultsViewer_acoustic)
        self.list_child_items.append(self.item_child_plotAcousticModeShapes)
        self.list_child_items.append(self.item_child_plotAcousticPressureField)
        self.list_child_items.append(self.item_child_plotAcousticFrequencyResponse)
        self.list_child_items.append(self.item_child_plotAcousticDeltaPressures)
        self.list_child_items.append(self.item_child_plot_TL_NR)
        self.list_child_items.append(self.item_child_plot_perforated_plate_convergence_data)
        #

    def _addItems(self):
        """Adds the Top Level Items and the Child Levels Items at the TreeWidget."""
        self.addTopLevelItem(self.item_top_generalSettings)
        self.item_top_generalSettings.addChild(self.item_child_createGeometry)
        self.item_top_generalSettings.addChild(self.item_child_editGeometry)
        self.item_top_generalSettings.addChild(self.item_child_setProjectAttributes)
        self.item_top_generalSettings.addChild(self.item_child_setMeshProperties)
        self.item_top_generalSettings.addChild(self.item_child_setGeometryFile)
        self.item_top_generalSettings.addChild(self.item_child_set_material)
        self.item_top_generalSettings.addChild(self.item_child_set_fluid)
        self.item_top_generalSettings.addChild(self.item_child_set_crossSection)
        
        self.addTopLevelItem(self.item_top_structuralModelSetup)
        self.item_top_structuralModelSetup.addChild(self.item_child_setStructuralElementType)
        self.item_top_structuralModelSetup.addChild(self.item_child_setPrescribedDofs)
        self.item_top_structuralModelSetup.addChild(self.item_child_setNodalLoads)
        self.item_top_structuralModelSetup.addChild(self.item_child_addMassSpringDamper)
        self.item_top_structuralModelSetup.addChild(self.item_child_add_elastic_nodal_links)
        self.item_top_structuralModelSetup.addChild(self.item_child_set_inertial_loads)
        self.item_top_structuralModelSetup.addChild(self.item_child_set_stress_stiffening)
        self.item_top_structuralModelSetup.addChild(self.item_child_setcappedEnd)
        self.item_top_structuralModelSetup.addChild(self.item_child_add_valve)
        self.item_top_structuralModelSetup.addChild(self.item_child_addFlanges)
        self.item_top_structuralModelSetup.addChild(self.item_child_add_expansion_joint)
        self.item_top_structuralModelSetup.addChild(self.item_child_setBeamXaxisRotation)
        self.item_top_structuralModelSetup.addChild(self.item_child_setRotationDecoupling)

        self.addTopLevelItem(self.item_top_acousticModelSetup)
        self.item_top_acousticModelSetup.addChild(self.item_child_setAcousticElementType)    
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
        self.item_top_resultsViewer_acoustic.addChild(self.item_child_plotAcousticDeltaPressures) 
        self.item_top_resultsViewer_acoustic.addChild(self.item_child_plot_TL_NR)   
        self.item_top_resultsViewer_acoustic.addChild(self.item_child_plot_perforated_plate_convergence_data)  

    def _configItems(self):
        """Configure all items."""   

        borderRole = Qt.UserRole + 1
        borderPen = QPen(QColor(0,0,0))
        borderPen.setWidth(1)

        textTopBrush = QBrush(QColor(0,0,0))
        configTopBrush = self.brush_upper_items
        plotTopBrush = self.brush_lower_items

        configTopItems = [  self.item_top_generalSettings, 
                            self.item_top_structuralModelSetup, 
                            self.item_top_acousticModelSetup    ]

        for top_item in self.list_top_items:
            top_item.setFlags(Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
            top_item.setFont(0, self.font_top_Items)
            top_item.setData(0, borderRole, borderPen)
            top_item.setTextAlignment(0, Qt.AlignHCenter | Qt.AlignVCenter)
            top_item.setForeground(0, textTopBrush)
            # top_item.setSizeHint(0, self.top_items_size)

            if top_item in configTopItems: 
                top_item.setBackground(0, configTopBrush)
                self.expandItem(top_item)
            else:
                top_item.setBackground(0, plotTopBrush)

        delegate = BorderItemDelegate(self, borderRole)
        self.setItemDelegate(delegate)

        for child_item in self.list_child_items:
            child_item.setFont(0, self.font_child_Items)
            # child_item.setSizeHint(0, self.top_items_size)

    def update_plot_mesh(self):
        if not self.mainWindow.opv_widget.change_plot_to_mesh:
            self.mainWindow.plot_mesh()

    def update_plot_entities(self):
        if not (self.mainWindow.opv_widget.change_plot_to_entities or self.mainWindow.opv_widget.change_plot_to_entities_with_cross_section):
            self.mainWindow.plot_entities()  

    def update_plot_entities_with_cross_section(self):
        if not self.mainWindow.opv_widget.change_plot_to_entities_with_cross_section:
            self.mainWindow.plot_entities_with_cross_section()   

    # def create_plot_convergence_data(self):
    #     self.item_top_resultsViewer_acoustic.addChild(self.item_child_plot_perforated_plate_convergence_data)

    def update_childItems_visibility(self, item):
        toggle = lambda x: x.setExpanded(not x.isExpanded())
        if item in self.list_top_items:
            toggle(item)
            return True 
        return False

    def on_click_item(self, item, column):
        """This event is raised every time an item is clicked on the menu."""
        # self.mainWindow.getInputWidget().beforeInput()

        if self.update_childItems_visibility(item):
            return

        if self.project.none_project_action:           
            self.empty_project_action_message()
        
        if item == self.item_child_setProjectAttributes:
            if not self.item_child_setProjectAttributes.isDisabled():
                self.mainWindow.getInputWidget().set_project_attributes()
        
        elif item == self.item_child_createGeometry:
            if not self.item_child_createGeometry.isDisabled():
                read = self.mainWindow.getInputWidget().call_geometry_designer()
                self.mainWindow._updateStatusBar()
                if read is None:
                    self.modify_general_settings_items_access(False)
                elif read:
                    self.modify_model_setup_items_access(False)
                    self.mainWindow.set_enable_menuBar(True)

        elif item == self.item_child_editGeometry:
            if not self.item_child_editGeometry.isDisabled():
                read = self.mainWindow.getInputWidget().edit_an_imported_geometry()

        elif item == self.item_child_setGeometryFile:
            if not self.item_child_setGeometryFile.isDisabled():
                self.mainWindow.getInputWidget().set_geometry_file()

        elif item == self.item_child_setMeshProperties:
            if not self.item_child_setMeshProperties.isDisabled():
                if self.mainWindow.getInputWidget().set_mesh_properties():
                    self._updateItems()
                    self.mainWindow.set_enable_menuBar(True)
                    self.mainWindow._updateStatusBar()

        elif item == self.item_child_set_material:
            if not self.item_child_set_material.isDisabled():
                self.update_plot_entities()
                self.mainWindow.getInputWidget().set_material()
                self.mainWindow.plot_entities()

        elif item == self.item_child_set_fluid:
            if not self.item_child_set_fluid.isDisabled(): 
                self.update_plot_entities()
                self.mainWindow.getInputWidget().set_fluid()
                self.mainWindow.plot_entities()

        elif item == self.item_child_set_crossSection:
            if not self.item_child_set_crossSection.isDisabled():
                if self.mainWindow.getInputWidget().set_cross_section():
                    self.mainWindow.plot_entities_with_cross_section()

        elif item == self.item_child_setStructuralElementType:
            if not self.item_child_setStructuralElementType.isDisabled():
                self.update_plot_entities()
                self.mainWindow.getInputWidget().setStructuralElementType()

        elif item == self.item_child_setPrescribedDofs:
            if not self.item_child_setPrescribedDofs.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().setDOF()
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

        elif item == self.item_child_add_elastic_nodal_links:
            if not self.item_child_add_elastic_nodal_links.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().add_elastic_nodal_links()
                self.mainWindow.plot_mesh()
        
        elif item == self.item_child_set_inertial_loads:
            if not self.item_child_set_inertial_loads.isDisabled():
                obj = self.mainWindow.getInputWidget().set_inertial_load()
                if obj.complete:
                    self.mainWindow.plot_mesh()

        elif item == self.item_child_set_stress_stiffening:
            if not self.item_child_set_stress_stiffening.isDisabled():
                self.mainWindow.getInputWidget().set_stress_stress_stiffening()
                # self.mainWindow.plot_entities()

        elif item == self.item_child_setcappedEnd:
             if not self.item_child_setcappedEnd.isDisabled():
                self.mainWindow.getInputWidget().setcappedEnd()
                # self.mainWindow.plot_entities()

        elif item == self.item_child_add_valve:
            if not self.item_child_add_valve.isDisabled():
                read = self.mainWindow.getInputWidget().add_valve()
                if read.complete:
                    self.mainWindow.plot_mesh()
                # self.mainWindow.plot_entities_with_cross_section()

        elif item == self.item_child_addFlanges:
            if not self.item_child_addFlanges.isDisabled():
                self.mainWindow.getInputWidget().add_flanges()

        elif item == self.item_child_add_expansion_joint:
            if not self.item_child_add_expansion_joint.isDisabled():
                self.mainWindow.getInputWidget().add_expansion_joint()
                # self.mainWindow.plot_entities_with_cross_section()

        elif item == self.item_child_setBeamXaxisRotation:
            if not self.item_child_setBeamXaxisRotation.isDisabled():
                self.update_plot_entities_with_cross_section()
                self.mainWindow.getInputWidget().set_beam_xaxis_rotation()

        elif item == self.item_child_setRotationDecoupling:
            if not self.item_child_setRotationDecoupling.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().setRotationDecoupling()
                self.mainWindow.plot_mesh()

        elif item == self.item_child_setAcousticElementType:
            if not self.item_child_setAcousticElementType.isDisabled():
                self.update_plot_entities()
                self.mainWindow.getInputWidget().set_acoustic_element_type()
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
                self.mainWindow.getInputWidget().plot_stress_field()

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

        elif item == self.item_child_plotAcousticDeltaPressures:
            if not self.item_child_plotAcousticDeltaPressures.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().plotAcousticDeltaPressures()

        elif item == self.item_child_plot_TL_NR:
            if not self.item_child_plot_TL_NR.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().plot_TL_NR()
        
        elif item == self.item_child_plot_perforated_plate_convergence_data:
            if not self.item_child_plot_perforated_plate_convergence_data.isDisabled():
                self.mainWindow.getInputWidget().plotPerforatedPlateConvergenceDataLog()

    def modify_geometry_item_access(self, bool_key):
        self.item_child_createGeometry.setDisabled(bool_key)
        self.item_child_setMeshProperties.setDisabled(bool_key)
        self.item_child_editGeometry.setHidden(True)

    def modify_general_settings_items_access(self, bool_key):
        #
        self.item_child_setProjectAttributes.setDisabled(bool_key)
        self.item_child_createGeometry.setDisabled(bool_key)
        self.item_child_setGeometryFile.setDisabled(bool_key)
        self.item_child_setMeshProperties.setDisabled(bool_key)
        self.item_child_editGeometry.setHidden(True)
        # self.item_child_set_material.setDisabled(bool_key)
        # self.item_child_set_fluid.setDisabled(bool_key)
        # self.item_child_set_crossSection.setDisabled(bool_key)

    def modify_model_setup_items_access(self, bool_key):
        #
        self.item_child_setProjectAttributes.setDisabled(bool_key)
        self.item_child_editGeometry.setDisabled(bool_key)
        self.item_child_createGeometry.setDisabled(bool_key)
        self.item_child_setGeometryFile.setDisabled(bool_key)
        self.item_child_setMeshProperties.setDisabled(bool_key)
        self.item_child_set_material.setDisabled(bool_key)
        self.item_child_set_fluid.setDisabled(bool_key)
        self.item_child_set_crossSection.setDisabled(bool_key)
        self.item_child_editGeometry.setHidden(False)
        #
        self.item_child_setStructuralElementType.setDisabled(bool_key) 
        self.item_child_setPrescribedDofs.setDisabled(bool_key)
        self.item_child_setNodalLoads.setDisabled(bool_key)
        self.item_child_addMassSpringDamper.setDisabled(bool_key)
        self.item_child_set_inertial_loads.setDisabled(bool_key)
        self.item_child_add_elastic_nodal_links.setDisabled(bool_key)
        self.item_child_set_stress_stiffening.setDisabled(bool_key)
        self.item_child_setcappedEnd.setDisabled(bool_key)
        self.item_child_add_valve.setDisabled(bool_key) 
        self.item_child_addFlanges.setDisabled(bool_key) 
        self.item_child_add_expansion_joint.setDisabled(bool_key)  
        self.item_child_setBeamXaxisRotation.setDisabled(bool_key)
        self.item_child_setRotationDecoupling.setDisabled(bool_key)
        #   
        self.item_child_setAcousticElementType.setDisabled(bool_key)
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
        """Enables and disables the Child Items on the menu after the solution is done."""
        self.modify_model_setup_items_access(False)

        if True:
            self.item_child_plotStructuralModeShapes.setDisabled(True)
            self.item_child_plotDisplacementField.setDisabled(True)
            self.item_child_plotStructuralFrequencyResponse.setDisabled(True)
            self.item_child_plotStressField.setDisabled(True)
            self.item_child_plotStressFrequencyResponse.setDisabled(True)
            self.item_child_plotAcousticModeShapes.setDisabled(True)
            self.item_child_plotAcousticFrequencyResponse.setDisabled(True)
            self.item_child_plotAcousticPressureField.setDisabled(True)
            self.item_child_plotAcousticDeltaPressures.setDisabled(True)
            self.item_child_plot_TL_NR.setDisabled(True)
            self.item_child_plot_perforated_plate_convergence_data.setDisabled(True)
            self.item_child_plotReactionsFrequencyResponse.setDisabled(True)
            self.item_child_analisysSetup.setDisabled(True)
            self.item_child_runAnalysis.setDisabled(True)
            # self.item_top_analysis.setHidden(True)
            self.item_top_resultsViewer_structural.setHidden(True)
            self.item_top_resultsViewer_acoustic.setHidden(True)
        
        if self.project.analysis_ID in [None, 2, 4]:
            self.item_child_analisysSetup.setDisabled(True)
        else:
            self.item_child_analisysSetup.setDisabled(False)
        
        if self.project.analysis_ID is not None and self.project.setup_analysis_complete:
            self.item_child_runAnalysis.setDisabled(False)
        
        if self.project.get_structural_solution() is not None or self.project.get_acoustic_solution() is not None:

            if self.project.analysis_ID in [0, 1, 2, 7]:
                self.item_top_resultsViewer_structural.setHidden(False)
            
            elif self.project.analysis_ID in [3, 4]:
                self.item_top_resultsViewer_acoustic.setHidden(False)
            
            elif self.project.analysis_ID in [5, 6]:    
                self.item_top_resultsViewer_acoustic.setHidden(False)
                self.item_top_resultsViewer_structural.setHidden(False)

            if self.project.analysis_ID in [0, 1]:
                self.item_child_plotStructuralFrequencyResponse.setDisabled(False)
                self.item_child_plotDisplacementField.setDisabled(False)
                self.item_child_plotReactionsFrequencyResponse.setDisabled(False)
                self.item_child_plotStressField.setDisabled(False)
                self.item_child_plotStressFrequencyResponse.setDisabled(False)
            
            elif self.project.analysis_ID == 2:
                self.item_child_plotStructuralModeShapes.setDisabled(False)
                if self.project.get_acoustic_solution() is not None:
                    self.item_child_plotAcousticModeShapes.setDisabled(False)    
            
            elif self.project.analysis_ID == 4:
                self.item_child_plotAcousticModeShapes.setDisabled(False)
                if self.project.get_structural_solution() is not None:
                    self.item_child_plotStructuralModeShapes.setDisabled(False)  
            
            elif self.project.analysis_ID == 3:
                if self.project.perforated_plate_dataLog:
                    self.item_child_plot_perforated_plate_convergence_data.setDisabled(False)
                self.item_child_plotAcousticFrequencyResponse.setDisabled(False)
                self.item_child_plotAcousticPressureField.setDisabled(False)
                self.item_child_plotAcousticDeltaPressures.setDisabled(False)
                self.item_child_plot_TL_NR.setDisabled(False)
            
            elif self.project.analysis_ID in [5, 6]:
                if self.project.perforated_plate_dataLog:
                    self.item_child_plot_perforated_plate_convergence_data.setDisabled(False)
                self.item_child_plotStructuralFrequencyResponse.setDisabled(False)
                self.item_child_plotAcousticFrequencyResponse.setDisabled(False)
                self.item_child_plotStressField.setDisabled(False)
                self.item_child_plotStressFrequencyResponse.setDisabled(False)
                self.item_child_plotDisplacementField.setDisabled(False)
                self.item_child_plotAcousticPressureField.setDisabled(False)
                self.item_child_plotAcousticDeltaPressures.setDisabled(False)
                self.item_child_plot_TL_NR.setDisabled(False)
                self.item_child_plotReactionsFrequencyResponse.setDisabled(False)  
            
            elif self.project.analysis_ID == 7:
                self.item_child_plotDisplacementField.setDisabled(False)
                self.item_child_plotStressField.setDisabled(False)
                self.item_child_plotStructuralFrequencyResponse.setDisabled(False)
                self.item_child_plotReactionsFrequencyResponse.setDisabled(False)
                self.item_child_plotStressFrequencyResponse.setDisabled(False)

            self.modify_item_names_according_to_analysis()
            self.update_TreeVisibility_after_solution()
            
    def update_TreeVisibility_after_solution(self):
        """Expands and collapses the Top Level Items ont the menu after the solution is done.
        
        """
        self.collapseItem(self.item_top_generalSettings)
        self.collapseItem(self.item_top_structuralModelSetup)
        self.collapseItem(self.item_top_acousticModelSetup)

        if self.project.analysis_ID in [0, 1, 2, 7]:
            self.item_top_resultsViewer_structural.setHidden(False)
            self.expandItem(self.item_top_resultsViewer_structural)
            # self.expandItem(self.item_top_structuralModelSetup)            
        elif self.project.analysis_ID in [3,4]:
            self.item_top_resultsViewer_acoustic.setHidden(False)
            self.expandItem(self.item_top_resultsViewer_acoustic)
            # self.expandItem(self.item_top_acousticModelSetup)
        elif self.project.analysis_ID in [5, 6]:
            self.item_top_resultsViewer_structural.setHidden(False)
            self.item_top_resultsViewer_acoustic.setHidden(False)
            self.expandItem(self.item_top_resultsViewer_structural)
            self.expandItem(self.item_top_resultsViewer_acoustic)

    def modify_item_names_according_to_analysis(self):
        if self.project.analysis_ID == 7:
            self.item_child_plotStructuralFrequencyResponse.setText(0, 'Plot Nodal Response')
            self.item_child_plotReactionsFrequencyResponse.setText(0, 'Plot Reactions')
            self.item_child_plotStressFrequencyResponse.setText(0, 'Plot Stresses')
        else:
            self.item_child_plotStructuralFrequencyResponse.setText(0, 'Plot Structural Frequency Response')
            self.item_child_plotReactionsFrequencyResponse.setText(0, 'Plot Reactions Frequency Response')
            self.item_child_plotStressFrequencyResponse.setText(0, 'Plot Stress Frequency Response')


    def update_structural_analysis_visibility_items(self):
        self.item_top_structuralModelSetup.setHidden(False)
        self.item_top_acousticModelSetup.setHidden(True)
        
    def update_acoustic_analysis_visibility_items(self):
        self.item_top_structuralModelSetup.setHidden(True)
        self.item_top_acousticModelSetup.setHidden(False)

    def update_coupled_analysis_visibility_items(self):
        self.item_top_structuralModelSetup.setHidden(False)
        self.item_top_acousticModelSetup.setHidden(False)

    def empty_project_action_message(self):
        title = 'EMPTY PROJECT'
        message = 'Please, you should create a new project or load an already existing one before start to set up the model.'
        message += "\n\nIt is recommended to use the 'New Project' or the 'Import Project' \nbuttons to continue."
        window_title = 'ERROR'
        PrintMessageInput([title, message, window_title], opv=self.mainWindow.getOPVWidget())