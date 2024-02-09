from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon, QFont, QPixmap, QColor, QLinearGradient, QBrush, QPen
from PyQt5.QtCore import Qt, QSize, QRect
from pathlib import Path

from pulse.interface.menu.border_item_delegate import BorderItemDelegate
from data.user_input.project.printMessageInput import PrintMessageInput

class ResultsViewerItems(QTreeWidget):
    """Menu Items

    This class is responsible for creating, configuring and building the items
    in the items menu, located on the left side of the interface.

    """
    def __init__(self, main_window):
        super().__init__()
        self.mainWindow = main_window
        self.project = main_window.getProject()

        self.setObjectName("results_viewer_items")
        
        # self._createIcons()
        # self._configItemSizes()
        self._createFonts()
        self._createColorsBrush()
        self._configTree()
        self._createItems()
        self._addItems()
        self._configItems()
        # self._updateItems()

    # def keyPressEvent(self, event):
    #     """This deals with key events that are directly linked with the menu."""
    #     if event.key() == Qt.Key_F5:
    #         self.mainWindow.getInputWidget().run_analysis()
    #         self._updateItems()

    # def _createIcons(self):
    #     """Create Icons objects that are placed on the right side of the item.
    #         Currently isn't used.
    #     """
    #     path = str(Path('data/icons/pulse.png'))
    #     self.icon_child_set_material = QIcon()
    #     self.icon_child_set_material.addPixmap(QPixmap(path), QIcon.Active, QIcon.On)

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
        #
        self.list_top_items = []
        self.list_child_items = []
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
        self.item_child_plotAcousticFrequencyResponseFunction = QTreeWidgetItem(['Plot Acoustic Frequency Response Function'])
        self.item_child_plotAcousticDeltaPressures = QTreeWidgetItem(['Plot Acoustic Delta Pressures'])
        self.item_child_plot_TL_NR = QTreeWidgetItem(['Plot Transmission Loss or Attenuation'])
        self.item_child_plot_perforated_plate_convergence_data = QTreeWidgetItem(['Plot perforated plate convergence data'])
        self.item_child_check_pulsation_criteria = QTreeWidgetItem(['Check Pulsation Criteria'])
        #
        self.list_top_items.append(self.item_top_resultsViewer_acoustic)
        self.list_child_items.append(self.item_child_plotAcousticModeShapes)
        self.list_child_items.append(self.item_child_plotAcousticPressureField)
        self.list_child_items.append(self.item_child_plotAcousticFrequencyResponse)
        self.list_child_items.append(self.item_child_plotAcousticFrequencyResponseFunction)
        self.list_child_items.append(self.item_child_plotAcousticDeltaPressures)
        self.list_child_items.append(self.item_child_plot_TL_NR)
        self.list_child_items.append(self.item_child_plot_perforated_plate_convergence_data)
        self.list_child_items.append(self.item_child_check_pulsation_criteria)
        #

    def _addItems(self):
        """Adds the Top Level Items and the Child Levels Items at the TreeWidget."""
        #
        self.addTopLevelItem(self.item_top_resultsViewer_structural)
        self.item_top_resultsViewer_structural.addChild(self.item_child_plotStructuralModeShapes)
        self.item_top_resultsViewer_structural.addChild(self.item_child_plotDisplacementField)
        self.item_top_resultsViewer_structural.addChild(self.item_child_plotStructuralFrequencyResponse)
        self.item_top_resultsViewer_structural.addChild(self.item_child_plotReactionsFrequencyResponse)
        self.item_top_resultsViewer_structural.addChild(self.item_child_plotStressField)
        self.item_top_resultsViewer_structural.addChild(self.item_child_plotStressFrequencyResponse)
        #
        self.addTopLevelItem(self.item_top_resultsViewer_acoustic)
        self.item_top_resultsViewer_acoustic.addChild(self.item_child_plotAcousticModeShapes)
        self.item_top_resultsViewer_acoustic.addChild(self.item_child_plotAcousticPressureField)
        self.item_top_resultsViewer_acoustic.addChild(self.item_child_plotAcousticFrequencyResponse)
        self.item_top_resultsViewer_acoustic.addChild(self.item_child_plotAcousticFrequencyResponseFunction)
        self.item_top_resultsViewer_acoustic.addChild(self.item_child_plotAcousticDeltaPressures) 
        self.item_top_resultsViewer_acoustic.addChild(self.item_child_plot_TL_NR)   
        self.item_top_resultsViewer_acoustic.addChild(self.item_child_plot_perforated_plate_convergence_data)
        self.item_top_resultsViewer_acoustic.addChild(self.item_child_check_pulsation_criteria) 

    def _configItems(self):
        """Configure all items."""   

        borderRole = Qt.UserRole + 1
        borderPen = QPen(QColor(0,0,0))
        borderPen.setWidth(1)

        textTopBrush = QBrush(QColor(0,0,0))
        # configTopBrush = self.brush_upper_items
        plotTopBrush = self.brush_lower_items

        for top_item in self.list_top_items:
            top_item.setFlags(Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
            top_item.setFont(0, self.font_top_Items)
            top_item.setData(0, borderRole, borderPen)
            top_item.setTextAlignment(0, Qt.AlignHCenter | Qt.AlignVCenter)
            top_item.setForeground(0, textTopBrush)
            # top_item.setSizeHint(0, self.top_items_size)

            # if top_item in configTopItems: 
            #     top_item.setBackground(0, configTopBrush)
            #     self.expandItem(top_item)
            # else:
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

        if item == self.item_child_check_pulsation_criteria:
            if not self.item_child_check_pulsation_criteria.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().check_pulsation_criteria()
                self.mainWindow.plot_mesh()

        elif item == self.item_child_plotStructuralModeShapes:
            return
            if not self.item_child_plotStructuralModeShapes.isDisabled():
                self.mainWindow.getInputWidget().plot_structural_mode_shapes()

        elif item == self.item_child_plotDisplacementField:
            return
            if not self.item_child_plotDisplacementField.isDisabled():
                self.mainWindow.getInputWidget().plot_displacement_field()

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
            return
            if not self.item_child_plotAcousticModeShapes.isDisabled():
                self.mainWindow.getInputWidget().plot_acoustic_mode_shapes()

        elif item == self.item_child_plotAcousticPressureField:
            return
            if not self.item_child_plotAcousticPressureField.isDisabled():
                self.mainWindow.getInputWidget().plot_acoustic_pressure_field()
         
        elif item == self.item_child_plotAcousticFrequencyResponse:
            if not self.item_child_plotAcousticFrequencyResponse.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().plotAcousticFrequencyResponse()
         
        elif item == self.item_child_plotAcousticFrequencyResponseFunction:
            if not self.item_child_plotAcousticFrequencyResponseFunction.isDisabled():
                self.update_plot_mesh()
                self.mainWindow.getInputWidget().plotAcousticFrequencyResponseFunction()

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

    def _updateItems(self):
        """Enables and disables the Child Items on the menu after the solution is done."""

        if True:
            # self.item_top_analysis.setHidden(True)
            self.item_top_resultsViewer_structural.setHidden(True)
            self.item_top_resultsViewer_acoustic.setHidden(True)
            self.item_child_plotStructuralModeShapes.setDisabled(True)
            self.item_child_plotDisplacementField.setDisabled(True)
            self.item_child_plotStructuralFrequencyResponse.setDisabled(True)
            self.item_child_plotStressField.setDisabled(True)
            self.item_child_plotStressFrequencyResponse.setDisabled(True)
            self.item_child_plotAcousticModeShapes.setDisabled(True)
            self.item_child_plotAcousticFrequencyResponse.setDisabled(True)
            self.item_child_plotAcousticFrequencyResponseFunction.setDisabled(True)
            self.item_child_plotAcousticPressureField.setDisabled(True)
            self.item_child_plotAcousticDeltaPressures.setDisabled(True)
            self.item_child_check_pulsation_criteria.setDisabled(True)
            self.item_child_plot_TL_NR.setDisabled(True)
            self.item_child_plot_perforated_plate_convergence_data.setDisabled(True)
            self.item_child_plotReactionsFrequencyResponse.setDisabled(True)
                            
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
                self.item_child_plotAcousticFrequencyResponseFunction.setDisabled(False)
                self.item_child_plotAcousticPressureField.setDisabled(False)
                self.item_child_plotAcousticDeltaPressures.setDisabled(False)
                self.item_child_plot_TL_NR.setDisabled(False)
                if self.project.preprocessor.nodes_with_compressor_excitation != []:
                    self.item_child_check_pulsation_criteria.setDisabled(False)
            
            elif self.project.analysis_ID in [5, 6]:
                if self.project.perforated_plate_dataLog:
                    self.item_child_plot_perforated_plate_convergence_data.setDisabled(False)

                self.item_child_plotDisplacementField.setDisabled(False)
                self.item_child_plotStructuralFrequencyResponse.setDisabled(False)
                self.item_child_plotStressField.setDisabled(False)
                self.item_child_plotStressFrequencyResponse.setDisabled(False)
                self.item_child_plotReactionsFrequencyResponse.setDisabled(False)  

                self.item_child_plotAcousticFrequencyResponse.setDisabled(False)
                self.item_child_plotAcousticFrequencyResponseFunction.setDisabled(False)
                self.item_child_plotAcousticPressureField.setDisabled(False)
                self.item_child_plotAcousticDeltaPressures.setDisabled(False)
                self.item_child_plot_TL_NR.setDisabled(False)

                if self.project.preprocessor.nodes_with_compressor_excitation != []:
                    self.item_child_check_pulsation_criteria.setDisabled(False)
            
            elif self.project.analysis_ID == 7:
                self.item_child_plotDisplacementField.setDisabled(False)
                self.item_child_plotStressField.setDisabled(False)
                self.item_child_plotStructuralFrequencyResponse.setDisabled(False)
                self.item_child_plotReactionsFrequencyResponse.setDisabled(False)
                self.item_child_plotStressFrequencyResponse.setDisabled(False)

            self.modify_item_names_according_to_analysis()
            # self.update_TreeVisibility_after_solution()
            
    def update_TreeVisibility_after_solution(self):
        """Expands and collapses the Top Level Items ont the menu after the solution is done.
        
        """
        # self.collapseItem(self.item_top_generalSettings)
        # self.collapseItem(self.item_top_structuralModelSetup)
        # self.collapseItem(self.item_top_acousticModelSetup)

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

    def empty_project_action_message(self):
        title = 'EMPTY PROJECT'
        message = 'Please, you should create a new project or load an already existing one before start to set up the model.'
        message += "\n\nIt is recommended to use the 'New Project' or the 'Import Project' \nbuttons to continue."
        window_title = 'ERROR'
        PrintMessageInput([title, message, window_title], opv=self.mainWindow.getOPVWidget())