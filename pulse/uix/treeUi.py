from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QBrush, QColor, QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt

class TreeUi(QTreeWidget):
    def __init__(self, main_window):
        super().__init__()
        self.mainWindow = main_window
        self._createNames()
        self._createIcons()
        self._createFonts()
        self._createColorsBrush()
        self._configTree()
        self._createItems()
        self._configItems()
        self._addItems()
        self._updateItems()

    def _createNames(self):
        self.name_top_structuralmodelSetup = "Structural Model Setup"
        self.name_child_setMaterial = "Set Material"
        self.name_child_setCrossSection = "Set Cross-Section"
        self.name_child_setElementType = "Set Element Type"
        self.name_child_setPrescribedDofs = "Set Prescribed DOFs"
        self.name_child_setNodalLoads = "Set Nodal Loads"
        self.name_child_addMassSpringDamper = "Add: Mass / Spring / Damper"

        self.name_top_acousticmodelSetup = "Acoustic Model Setup"
        self.name_child_setFluid = "Set Fluid"
        self.name_child_setAcousticPressure = "Set Acoustic Pressure"
        self.name_child_setVolumeVelocity = "Set Volume Velocity"
        self.name_child_setSpecificImpedance = "Set Specific Impedance"
        self.name_child_setRadiationImpedance = "Set Radiation Impedance"
        
        self.name_top_analysis = "Analysis"
        self.name_child_selectAnalysisType = "Select Analysis Type"
        self.name_child_analisysSetup = "Analysis Setup"
        self.name_child_selectTheOutputResults = "Select the Outputs Results"
        self.name_child_runAnalysis = "Run Analysis"

        self.name_top_resultsViewer = "Results Viewer"
        self.name_child_plotModeShapes = "Plot Mode Shapes"
        self.name_child_plotHarmonicResponse = "Plot Harmonic Response"
        self.name_child_plotPressureField = "Plot Pressure Field"
        self.name_child_plotStressField = "Plot Stress Field"
        self.name_child_plotFrequencyResponse = "Plot Frequency Response"

    def _createIcons(self):
        self.icon_child_setMaterial = QIcon()
        self.icon_child_setMaterial.addPixmap(QPixmap("pulse/data/icons/pulse.png"), QIcon.Active, QIcon.On)

    def _createFonts(self):
        self.font_top = QFont()
        #self.font_child = QFont()

        self.font_top.setFamily("Segoe UI")
        self.font_top.setPointSize(10)
        self.font_top.setBold(True)
        self.font_top.setItalic(True)
        self.font_top.setWeight(75)

    def _createColorsBrush(self):
        #color_top = QColor(39, 180, 211)
        color_top = QColor(178, 178, 178)
        #color_child = QColor(0, 0, 0)
        self.brush_top = QBrush(color_top)
        self.brush_top.setStyle(Qt.SolidPattern)

    def _configTree(self):
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setTabKeyNavigation(True)
        self.setIndentation(0)
        self.itemClicked.connect(self.on_click_item)

    def _createItems(self):
        self.item_top_structuralmodelSetup = QTreeWidgetItem([self.name_top_structuralmodelSetup])
        self.item_child_setMaterial = QTreeWidgetItem([self.name_child_setMaterial])
        self.item_child_setCrossSection = QTreeWidgetItem([self.name_child_setCrossSection])
        self.item_child_setElementType = QTreeWidgetItem([self.name_child_setElementType])
        self.item_child_setPrescribedDofs = QTreeWidgetItem([self.name_child_setPrescribedDofs])
        self.item_child_setNodalLoads = QTreeWidgetItem([self.name_child_setNodalLoads])
        self.item_child_addMassSpringDamper = QTreeWidgetItem([self.name_child_addMassSpringDamper])

        self.item_top_acousticmodelSetup = QTreeWidgetItem([self.name_top_acousticmodelSetup])
        self.item_child_setFluid = QTreeWidgetItem([self.name_child_setFluid])
        self.item_child_setAcousticPressure = QTreeWidgetItem([self.name_child_setAcousticPressure])
        self.item_child_setVolumeVelocity = QTreeWidgetItem([self.name_child_setVolumeVelocity])
        self.item_child_setSpecificImpedance = QTreeWidgetItem([self.name_child_setSpecificImpedance])
        self.item_child_setRadiationImpedance = QTreeWidgetItem([self.name_child_setRadiationImpedance])

        self.item_top_analysis = QTreeWidgetItem([self.name_top_analysis])
        self.item_child_selectAnalysisType = QTreeWidgetItem([self.name_child_selectAnalysisType])
        self.item_child_analisysSetup = QTreeWidgetItem([self.name_child_analisysSetup])
        self.item_child_selectTheOutputResults = QTreeWidgetItem([self.name_child_selectTheOutputResults])
        self.item_child_runAnalysis = QTreeWidgetItem([self.name_child_runAnalysis])

        self.item_top_resultsViewer = QTreeWidgetItem([self.name_top_resultsViewer])
        self.item_child_plotModeShapes = QTreeWidgetItem([self.name_child_plotModeShapes])
        self.item_child_plotHarmonicResponse = QTreeWidgetItem([self.name_child_plotHarmonicResponse])
        self.item_child_plotPressureField = QTreeWidgetItem([self.name_child_plotPressureField])
        self.item_child_plotStressField = QTreeWidgetItem([self.name_child_plotStressField])
        self.item_child_plotFrequencyResponse = QTreeWidgetItem([self.name_child_plotFrequencyResponse])

    def _configItems(self):
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

        self.item_top_resultsViewer.setFlags(Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        self.item_top_resultsViewer.setFont(0, self.font_top)
        self.item_top_resultsViewer.setTextAlignment(0, Qt.AlignHCenter)
        self.item_top_resultsViewer.setBackground(0, self.brush_top)

        #self.item_child_setMaterial.setIcon(0, self.icon_child_setMaterial)

        self.item_child_setElementType.setDisabled(True)
        self.item_child_selectTheOutputResults.setDisabled(True)
        self.item_child_plotStressField.setDisabled(True)

    def _addItems(self):
        self.addTopLevelItem(self.item_top_structuralmodelSetup)
        self.addTopLevelItem(self.item_child_setMaterial)
        self.addTopLevelItem(self.item_child_setCrossSection)
        self.addTopLevelItem(self.item_child_setElementType)
        self.addTopLevelItem(self.item_child_setPrescribedDofs)
        self.addTopLevelItem(self.item_child_setNodalLoads)
        self.addTopLevelItem(self.item_child_addMassSpringDamper)

        self.addTopLevelItem(self.item_top_acousticmodelSetup)      
        self.addTopLevelItem(self.item_child_setFluid)             
        self.addTopLevelItem(self.item_child_setAcousticPressure) 
        self.addTopLevelItem(self.item_child_setVolumeVelocity)     
        self.addTopLevelItem(self.item_child_setSpecificImpedance)
        self.addTopLevelItem(self.item_child_setRadiationImpedance)     

        self.addTopLevelItem(self.item_top_analysis)
        self.addTopLevelItem(self.item_child_selectAnalysisType)
        self.addTopLevelItem(self.item_child_analisysSetup)
        self.addTopLevelItem(self.item_child_selectTheOutputResults)
        self.addTopLevelItem(self.item_child_runAnalysis)

        self.addTopLevelItem(self.item_top_resultsViewer)
        self.addTopLevelItem(self.item_child_plotModeShapes)
        self.addTopLevelItem(self.item_child_plotHarmonicResponse)
        self.addTopLevelItem(self.item_child_plotPressureField)
        self.addTopLevelItem(self.item_child_plotStressField)
        self.addTopLevelItem(self.item_child_plotFrequencyResponse)

    def on_click_item(self, item, column):
        if item.text(0) == self.name_child_setMaterial:
            self.mainWindow.getInputWidget().setMaterial()
        elif item.text(0) == self.name_child_setFluid: 
            self.mainWindow.getInputWidget().setFluid()
        elif item.text(0) == self.name_child_setAcousticPressure:
            self.mainWindow.getInputWidget().setAcousticPressure()
        elif item.text(0) == self.name_child_setVolumeVelocity: 
            self.mainWindow.getInputWidget().setVolumeVelocity()
        elif item.text(0) == self.name_child_setSpecificImpedance:
            self.mainWindow.getInputWidget().setSpecificImpedance()
        elif item.text(0) == self.name_child_setRadiationImpedance:
            self.mainWindow.getInputWidget().setRadiationImpedance()
        elif item.text(0) == self.name_child_setCrossSection:
            self.mainWindow.getInputWidget().setCrossSection()
        elif item.text(0) == self.name_child_setElementType:
            self.mainWindow.getInputWidget().setElementType()
        elif item.text(0) == self.name_child_setPrescribedDofs:
            self.mainWindow.getInputWidget().setDOF()
        elif item.text(0) == self.name_child_setNodalLoads:
            self.mainWindow.getInputWidget().setNodalLoads()
        elif item.text(0) == self.name_child_addMassSpringDamper:
            self.mainWindow.getInputWidget().addMassSpringDamper()
        elif item.text(0) == self.name_child_selectAnalysisType:
            self.mainWindow.getInputWidget().analyseTypeInput()
            self._updateItems()
        elif item.text(0) == self.name_child_analisysSetup:
            self.mainWindow.getInputWidget().analyseSetup()
        elif item.text(0) == self.name_child_selectTheOutputResults:
            self.mainWindow.getInputWidget().analyseOutputResults()
        elif item.text(0) == self.name_child_runAnalysis:
            self.mainWindow.getInputWidget().runAnalyse()
            self._updateItems()
        elif item.text(0) == self.name_child_plotModeShapes:
            self.mainWindow.getInputWidget().plotModeShapes()
        elif item.text(0) == self.name_child_plotHarmonicResponse:
            self.mainWindow.getInputWidget().plotHarmonicResponse()
        elif item.text(0) == self.name_child_plotPressureField:
            self.mainWindow.getInputWidget().plotPressureField()
        elif item.text(0) == self.name_child_plotStressField:
            self.mainWindow.getInputWidget().plotStressField()
        elif item.text(0) == self.name_child_plotFrequencyResponse:
            self.mainWindow.getInputWidget().plotFrequencyResponse()

    def _updateItems(self):
        project = self.mainWindow.getProject()

        if project.getStructuralSolution() is None:
            self.item_child_plotModeShapes.setDisabled(True)
            self.item_child_plotHarmonicResponse.setDisabled(True)
            self.item_child_plotFrequencyResponse.setDisabled(True)

        if project.getAcousticSolution() is None:
            self.item_child_plotModeShapes.setDisabled(True)
            self.item_child_plotHarmonicResponse.setDisabled(True)
            self.item_child_plotFrequencyResponse.setDisabled(True)
            self.item_child_plotPressureField.setDisabled(True)
        
        if project.getStructuralSolution() is not None or project.getAcousticSolution() is not None:
            analysisType = project.getAnalysisType()
            if analysisType == 'Harmonic Analysis - Structural':
                self.item_child_plotFrequencyResponse.setDisabled(False)
                self.item_child_plotHarmonicResponse.setDisabled(False)
            elif analysisType == 'Harmonic Analysis - Acoustic':
                self.item_child_plotFrequencyResponse.setDisabled(False)
                self.item_child_plotPressureField.setDisabled(False)
            elif analysisType == 'Modal Analysis - Structural':
                self.item_child_plotModeShapes.setDisabled(False) 