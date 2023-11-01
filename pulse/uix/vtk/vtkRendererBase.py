import vtk

from abc import ABC, abstractmethod 
from pathlib import Path


class vtkRendererBase(ABC):
    def __init__(self, style):
        super().__init__()

        self.nodes_color = (255, 255, 63)
        self.lines_color = (255, 255, 255)
        self.surfaces_color = (255, 255, 255)
        self.elements_transparency = 0.8

        self.background_color = (0,0,0)
        self._renderer = vtk.vtkRenderer()
        self._renderer.SetBackground(self.background_color)

        self._style = style
        self._style.SetDefaultRenderer(self._renderer)

        self._textActor = vtk.vtkTextActor()
        self.textActorStress = vtk.vtkTextActor()
        self.actors = {}
        self._inUse = False
        self._usePicker = True
        self.textProperty = vtk.vtkTextProperty()
        self.textProperty.SetFontSize(17)
        self.textProperty.SetColor((1,1,1))
        self.textProperty.BoldOn()
        # self.textProperty.SetItalic(1)
        
        self._logo_pulse = vtk.vtkLogoRepresentation()
        self._logo_mopt = vtk.vtkLogoRepresentation()
        self._imageReader_pulse = vtk.vtkPNGReader()
        self._imageReader_mopt = vtk.vtkPNGReader()

        self.changeLogosToGetBetterContrast()
        self._createConfigLogos()        

    def _createConfigLogos(self):
        
        self._imageReader_pulse.SetFileName(Path('data/icons/OpenPulse_logo_white.png'))
        self._imageReader_mopt.SetFileName(Path('data/icons/mopt_logo_white.png'))
        self._imageReader_pulse.Update()
        self._imageReader_mopt.Update()
        
        self._logo_pulse_input = self._imageReader_pulse.GetOutput()
        self._logo_pulse.SetImage(self._logo_pulse_input)
        self._logo_pulse.ProportionalResizeOn()

        self._logo_mopt_input = self._imageReader_mopt.GetOutput()
        self._logo_mopt.SetImage(self._logo_mopt_input)
        self._logo_mopt.ProportionalResizeOn()
        
        self._logo_pulse.SetPosition(0.845, 0.89)
        self._logo_pulse.SetPosition2(0.15, 0.15)   
     
        self._logo_pulse.GetImageProperty().SetOpacity(0.9)
        self._logo_pulse.GetImageProperty().SetDisplayLocationToBackground()

        self._logo_mopt.SetPosition(0.01, -0.015)
        self._logo_mopt.SetPosition2(0.07, 0.1)
     
        self._logo_mopt.GetImageProperty().SetOpacity(0.9)
        self._logo_mopt.GetImageProperty().SetDisplayLocationToBackground()  

    def _createLogos(self, OpenPulse=True, MOPT=True):

        self._renderer.RemoveViewProp(self._logo_pulse)
        self._renderer.RemoveViewProp(self._logo_mopt)

        if OpenPulse:   
            self._renderer.AddViewProp(self._logo_pulse)
            self._logo_pulse.SetRenderer(self._renderer)
        
        if MOPT:
            self._renderer.AddViewProp(self._logo_mopt)
            self._logo_mopt.SetRenderer(self._renderer)

    def changeBackgroundColor(self, color):
        self.background_color = color

        # I would preffer to use only two themes like
        # we do inside Vibra.
        # But this way is much more convenient and
        # probably good enought
        if self.background_color == (0,0,0):
            self._renderer.GradientBackgroundOn()
            self._renderer.SetBackground(0.06, 0.08, 0.12)
            self._renderer.SetBackground2(color)
        elif self.background_color == (1,1,1):
            self._renderer.GradientBackgroundOn()
            self._renderer.SetBackground(0.5, 0.5, 0.65)
            self._renderer.SetBackground2(color)
        else:
            self._renderer.GradientBackgroundOff()
            self._renderer.SetBackground(color)

        self.changeLogosToGetBetterContrast()

    def changeLogosToGetBetterContrast(self):
        if self.background_color == (0,0,0):
            self._imageReader_pulse.SetFileName(Path('data/icons/OpenPulse_logo_white.png'))
            self._imageReader_mopt.SetFileName(Path('data/icons/mopt_logo_white.png'))
        elif self.background_color == (0.25,0.25,0.25):
            self._imageReader_pulse.SetFileName(Path('data/icons/OpenPulse_logo_white.png'))
            self._imageReader_mopt.SetFileName(Path('data/icons/mopt_logo_white.png'))
        elif self.background_color == (0.7,0.7,0.7):
            self._imageReader_pulse.SetFileName(Path('data/icons/OpenPulse_logo_black.png'))
            self._imageReader_mopt.SetFileName(Path('data/icons/mopt_logo_black.png'))
        elif self.background_color == (1,1,1):
            self._imageReader_pulse.SetFileName(Path('data/icons/OpenPulse_logo_black.png'))
            self._imageReader_mopt.SetFileName(Path('data/icons/mopt_logo_black.png'))
        self._imageReader_pulse.Update()
        self._imageReader_mopt.Update()
        
    def changeNodesColor(self, color):
        self.nodes_color = color 
    
    def changeLinesColor(self, color):
        self.lines_color = color

    def changeSurfacesColor(self, color):
        self.surfaces_color = color
    
    def changeElementsTransparency(self, transparency):
        self.elements_transparency = transparency

    def changeFontColor(self, color):
        self.textProperty.SetColor(color)

    def changeSliderFontColor(self, color):
        self.SetColor(color)

    def changeColorbarFontColor(self, color):
        self.SetColor(color)

    def changeReferenceScaleFontColor(self, color):
        self.scaleBarTitleProperty.SetColor(color)
        self.scaleBarLabelProperty.SetColor(color)

    def _createScaleBar(self):
        
        self._renderer.RemoveActor(self.scaleBar)
        width, height = self.getSize()
        self.scaleBar = vtk.vtkLegendScaleActor()
        self.scaleBarTitleProperty = self.scaleBar.GetLegendTitleProperty()
        self.scaleBarLabelProperty = self.scaleBar.GetLegendLabelProperty()
        
        if self.opv.show_reference_scale:
            self.scaleBarTitleProperty.ShadowOff()
            self.scaleBarLabelProperty.ShadowOff()
            self.scaleBarTitleProperty.SetFontSize(16)
            self.scaleBarLabelProperty.SetFontSize(16)
            self.scaleBarTitleProperty.SetColor(self.opv.font_color)
            self.scaleBarLabelProperty.SetColor(self.opv.font_color)
            self.scaleBarTitleProperty.SetVerticalJustificationToTop()
            self.scaleBarTitleProperty.SetLineOffset(-40)
            self.scaleBarLabelProperty.SetLineOffset(-25)
            self.scaleBar.AllAxesOff()
            self._renderer.AddActor(self.scaleBar)
            # self.scaleBar.LegendVisibilityOff()
            # self.scaleBar.BottomAxisVisibilityOn()

    def _createColorBar(self):

        self.colorBarTitleProperty = vtk.vtkTextProperty()
        self.colorBarTitleProperty.SetFontSize(20)
        self.colorBarTitleProperty.ShadowOff()
        self.colorBarTitleProperty.BoldOn()
        # self.colorBarTitleProperty.SetItalic(1)
        self.colorBarTitleProperty.SetColor(self.opv.font_color)
        self.colorBarTitleProperty.SetJustificationToLeft()
        
        self.colorBarLabelProperty = vtk.vtkTextProperty()
        self.colorBarLabelProperty.SetFontSize(14)
        self.colorBarLabelProperty.ShadowOff()
        # self.colorBarLabelProperty.SetItalic(1)
        self.colorBarLabelProperty.SetColor(self.opv.font_color)
        self.colorBarLabelProperty.SetJustificationToLeft()   

        unit = self.project.get_unit()
        if unit:
            text = "None"
        text = "Unit: [{}]".format(unit)
        
        self._renderer.RemoveActor(self.colorbar)
        self.colorbar = vtk.vtkScalarBarActor()
        self.colorbar.SetLabelTextProperty(self.colorBarLabelProperty)
        self.colorbar.SetTitleTextProperty(self.colorBarTitleProperty)
        self.colorbar.SetMaximumNumberOfColors(400)
        self.colorbar.SetWidth(0.04)
        self.colorbar.SetTextPositionToPrecedeScalarBar()
        self.colorbar.SetPosition(0.94, 0.07)
        self.colorbar.SetLabelFormat("%1.0e ")
        self.colorbar.UnconstrainedFontSizeOn()   
        self.colorbar.VisibilityOn()
        self.colorbar.SetTitle(text)
        self.colorbar.SetVerticalTitleSeparation(20)

        self._renderer.AddActor(self.colorbar)

    def resetCamera(self):
        self._renderer.ResetCamera()

    def getRenderer(self):
        return self._renderer

    def getStyle(self):
        return self._style

    def getSize(self):
        return self._renderer.GetSize()

    def getInUse(self):
        return self._inUse

    def getUsePicker(self):
        return self._usePicker

    def setUsePicker(self, value):
        self._usePicker = value

    def setInUse(self, value):
        self._style.releaseButtons()
        self._inUse = value

    def createInfoText(self, text):
        #Remove the actor if it already exists
        self._renderer.RemoveActor2D(self._textActor)

        height = self._renderer.GetSize()[1] - 30
        width = 20
        
        self.textProperty.SetVerticalJustificationToTop()
        self.textProperty.SetJustificationToLeft()
        self._textActor.SetInput(text)
        self._textActor.SetTextProperty(self.textProperty)
        self._textActor.SetDisplayPosition(width, height)
        self._renderer.AddActor2D(self._textActor)

    @abstractmethod
    def updateInfoText(self):
        #It's necessary to call createInfoText with the text to plot.
        pass

    @abstractmethod
    def plot(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def update(self):
        pass