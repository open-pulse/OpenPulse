import vtk

from pulse.postprocessing.plot_structural_data import get_structural_response
from pulse.postprocessing.plot_acoustic_data import get_acoustic_response

from pulse.uix.vtk.colorTable import ColorTable
from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkMeshClicker import vtkMeshClicker
from pulse.interface.tubeActor import TubeActor
from pulse.interface.tubeDeformedActor import TubeDeformedActor



class opvAnalisysRenderer(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkMeshClicker(self))

        self.project = project
        self.opv = opv
        self.setUsePicker(False)

        self._magnificationFactor = 1
        self._currentFrequency = 0
        self._currentPlot = None
        self.colorbar = None 
        self.scaleBar = None

        # just ignore it 
        self.nodesBounds = dict()
        self.elementsBounds = dict()
        self.entitiesBounds = dict()

        self.opvDeformedTubes = None
        self.opvPressureTubes = None
        self.slider = None
        self._createSlider()

    def plot(self):
        self.reset()

        self.opvDeformedTubes = TubeDeformedActor(self.project.get_elements(), self.project)
        self.opvPressureTubes = TubeActor(self.project.get_elements(), self.project)

        self.opvPressureTubes.transparent = False

        self._createSlider()
        plt = lambda x: self._renderer.AddActor(x.getActor())
        plt(self.opvDeformedTubes)
        plt(self.opvPressureTubes)

    def reset(self):
        self._renderer.RemoveAllViewProps()
        self._style.clear()
    
    def update(self):
        self.opv.updateDialogs()
        renWin = self._renderer.GetRenderWindow()
        if renWin: renWin.Render()

    def updateHud(self):
        self._createSlider()
        self._createColorBar()
        self._createScaleBar()

    def showStressField(self, frequency, gain=1):
        
        mesh = self.project.get_mesh()
        solution = self.project.get_structural_solution()
        self._currentPlot = self.showStressField
        self._currentFrequency = frequency

        _, _, u_def, self._magnificationFactor = get_structural_response(mesh, solution, frequency, gain=gain)
        self.opvDeformedTubes.build()

        colorTable = ColorTable(self.project, u_def, stress_field_plot=True)
        self.opvDeformedTubes.setColorTable(colorTable)
        self.colorbar.SetLookupTable(colorTable)
        
        self.slider.SetEnabled(True)
        self.opvDeformedTubes.getActor().SetVisibility(True)
        self.opvPressureTubes.getActor().SetVisibility(False)

        self.updateInfoText()
        self._renderer.ResetCameraClippingRange()
        self.opv.update()
        self.update()

    def showDisplacement(self, frequency, gain=1):
        mesh = self.project.get_mesh()
        solution = self.project.get_structural_solution()
        self._currentPlot = self.showDisplacement
        self._currentFrequency = frequency

        _, _, u_def, self._magnificationFactor = get_structural_response(mesh, solution, frequency, gain=gain)
        self.opvDeformedTubes.build()

        colorTable = ColorTable(self.project, u_def, stress_field_plot=False)
        self.opvDeformedTubes.setColorTable(colorTable)
        self.colorbar.SetLookupTable(colorTable)
        
        self.slider.SetEnabled(True)
        self.opvDeformedTubes.getActor().SetVisibility(True)
        self.opvPressureTubes.getActor().SetVisibility(False)

        self.updateInfoText()
        self._renderer.ResetCameraClippingRange()
        self.opv.update()
        self.update()

    def showPressureField(self, frequency, real_part=True):
        mesh = self.project.get_mesh()
        solution = self.project.get_acoustic_solution()
        self._currentFrequency = frequency
        self._colorScalling = 'real part' if real_part else 'absolute'

        *args, u_def = get_acoustic_response(mesh, solution, frequency, real_part)
        self.opvPressureTubes.build()

        colorTable = ColorTable(self.project, u_def, pressure_field_plot=True)
        self.opvPressureTubes.setColorTable(colorTable)
        self.colorbar.SetLookupTable(colorTable)
        
        self.slider.SetEnabled(False)
        self.opvDeformedTubes.getActor().SetVisibility(False)
        self.opvPressureTubes.getActor().SetVisibility(True)

        self.updateInfoText()
        self._renderer.ResetCameraClippingRange()
        self.opv.update()
        self.update()

    def _createSlider(self):
        self.slider = vtk.vtkSliderWidget()
        
        sld = vtk.vtkSliderRepresentation2D()
        sld.SetMinimumValue(-1)
        sld.SetMaximumValue(1)
        sld.SetValue(1)

        sld.GetSelectedProperty().SetColor(1, 0, 0)
        sld.GetTubeProperty().SetColor(0.5, 0.5, 0.5)
        sld.GetCapProperty().SetColor(0.8, 0.8, 0.8)
        
        sld.SetSliderLength(0.01)
        sld.SetSliderWidth(0.02)
        sld.SetTubeWidth(0.02)

        sld.SetEndCapWidth(0.02)
        sld.SetEndCapLength(0.005)

        sld.SetTitleHeight(0.015)
        sld.SetLabelHeight(0.015)

        width, height = self.getSize()
        sld.GetPoint1Coordinate().SetCoordinateSystemToDisplay()
        sld.GetPoint2Coordinate().SetCoordinateSystemToDisplay()
        sld.GetPoint1Coordinate().SetValue(20, height-150)
        sld.GetPoint2Coordinate().SetValue(220, height-150)

        self.slider.SetInteractor(self.opv)
        self.slider.SetRepresentation(sld)
        self.slider.AddObserver(vtk.vtkCommand.EndInteractionEvent, self._sliderCallback)

    def _sliderCallback(self, slider, b):
        if self._currentPlot is None:
            return 
        
        sliderValue = slider.GetRepresentation().GetValue()
        sliderValue = round(sliderValue, 1)
        slider.GetRepresentation().SetValue(sliderValue)
        
        # call the last plot function related to the slider
        self._currentPlot(self._currentFrequency, sliderValue)

    def _createColorBar(self):
        textProperty = vtk.vtkTextProperty()
        textProperty.SetFontSize(14)
        textProperty.SetItalic(1)
        unit = self.project.get_unit(stress=False)
        text = "Unit: [{}]".format(unit)

        self._renderer.RemoveActor(self.colorbar)
        self.colorbar = vtk.vtkScalarBarActor()
        self.colorbar.SetLabelTextProperty(textProperty)
        self.colorbar.SetMaximumNumberOfColors(400)
        self.colorbar.SetWidth(0.04)
        self.colorbar.SetTextPositionToPrecedeScalarBar()
        self.colorbar.SetPosition(0.94, 0.1)
        self.colorbar.SetLabelFormat("%1.0e ")
        self.colorbar.UnconstrainedFontSizeOn()   
        self.colorbar.VisibilityOn()
        self.colorbar.SetTitle(text)
        self.colorbar.SetVerticalTitleSeparation(20)
        self.colorbar.GetTitleTextProperty().SetFontSize(20)
        self.colorbar.GetTitleTextProperty().SetJustificationToLeft()
        self._renderer.AddActor(self.colorbar)

    def _createScaleBar(self):
        width, height = self.getSize()
        self._renderer.RemoveActor(self.scaleBar)
        self.scaleBar = vtk.vtkLegendScaleActor()
        self.scaleBar.AllAxesOff()
        self._renderer.AddActor(self.scaleBar)


    # info text
    def updateInfoText(self, *args, **kwargs):
        mode = self._currentFrequency + 14
        magnif = abs(self.slider.GetRepresentation().GetValue())
        frequencies = self.project.get_frequencies()
        text = self.project.analysis_type_label + "\n"
        if self.project.analysis_ID not in [2,4]:
            text += self.project.analysis_method_label + "\n"
            text += "Frequency: {:.2f} [Hz]\n".format(frequencies[self._currentFrequency])
        elif self.project.analysis_ID == 2:
            frequencies = self.project.get_structural_natural_frequencies()
            text += "Mode: {}\n".format(mode)
            text += "Natural Frequency: {:.2f} [Hz]\n".format(frequencies[self._currentFrequency])
        elif self.project.analysis_ID == 4:
            frequencies = self.project.get_acoustic_natural_frequencies()
            text += "Mode: {}\n".format(mode)
            text += "Natural Frequency: {:.2f} [Hz]\n".format(frequencies[self._currentFrequency])
            text += "Color scalling: {}".format(self._colorScalling)
        if not self.project.plot_pressure_field:
            text += "\nMagnification factor {:.2f}x\n".format(self._magnificationFactor)
        # vertical_position_adjust = None
        self.createInfoText(text)

    # functions to be removed but currently break the execution
    def getElementsInfoText(self, *args, **kwargs):
        pass
    
    def getEntityInfoText(self, *args, **kwargs):
        pass 

    def getPlotRadius(self, *args, **kwargs):
        return 
    
    def changeColorEntities(self, *args, **kwargs):
        return 

    def setPlotRadius(self, plt):
        pass