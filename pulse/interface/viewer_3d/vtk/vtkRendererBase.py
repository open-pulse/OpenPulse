import vtk

from abc import ABC, abstractmethod 
from pathlib import Path
from vtkat import VTKAT_DIR
from pulse import ICON_DIR

class vtkRendererBase(ABC):
    def __init__(self, style):
        super().__init__()

        self._logo_pulse = vtk.vtkLogoRepresentation()
        self._imageReader_pulse = vtk.vtkPNGReader()
        self._imageReader_mopt = vtk.vtkPNGReader()
        
        self._textActor = vtk.vtkTextActor()
        self.textActorStress = vtk.vtkTextActor()
        self.textProperty = vtk.vtkTextProperty()
        self._renderer = vtk.vtkRenderer()

        self.colorBarTitleProperty = vtk.vtkTextProperty()
        self.colorBarLabelProperty = vtk.vtkTextProperty()
        
        self.scaleBar = vtk.vtkLegendScaleActor()
        self.colorbar = vtk.vtkScalarBarActor()

        self._load_default_preferences()
        self._create_and_config_logos()

        self._style = style
        self._style.SetDefaultRenderer(self._renderer)

        self.actors = {}
        self._inUse = False
        self._usePicker = True

        font_file = VTKAT_DIR / "fonts/LiberationMono-Bold.ttf"
        self.textProperty.SetFontSize(14)
        self.textProperty.SetFontFamily(vtk.VTK_FONT_FILE)
        self.textProperty.SetFontFile(font_file)

        # self.textProperty.BoldOn()
        # self.textProperty.SetItalic(1)

    def _load_default_preferences(self):
        self.background_color = "light"
        self.bottom_font_color = (0, 0, 0)
        self.top_font_color = (0, 0, 0)
        self.nodes_color = (255, 255, 63)
        self.lines_color = (255, 255, 255)
        self.surfaces_color = (255, 255, 255)
        self.elements_transparency = 0.8
        self.colormap = "viridis"
        self.set_background_color("light")
        self.add_OpenPulse_logo = True
        self.show_reference_scale = True

    def _create_and_config_logos(self):
        
        # self._imageReader_pulse.SetFileName(Path('data/icons/logos/OpenPulse_logo_black.png'))
        self._imageReader_pulse.SetFileName(str(ICON_DIR / 'logos/OpenPulse_logo_gray.png'))
        self._imageReader_pulse.Update()
        
        self._logo_pulse_input = self._imageReader_pulse.GetOutput()
        self._logo_pulse.SetImage(self._logo_pulse_input)
        self._logo_pulse.ProportionalResizeOn()
        
        self._logo_pulse.SetPosition(0.845, 0.89)
        self._logo_pulse.SetPosition2(0.15, 0.15)   
     
        self._logo_pulse.GetImageProperty().SetOpacity(0.9)
        self._logo_pulse.GetImageProperty().SetDisplayLocationToBackground()

    def add_openpulse_logo(self):
        self._renderer.RemoveViewProp(self._logo_pulse)
        if self.add_OpenPulse_logo:
            self._renderer.AddViewProp(self._logo_pulse)
            self._logo_pulse.SetRenderer(self._renderer)

    def set_background_color(self, color):
        self.background_color = color
        if color == "dark":
            self._renderer.GradientBackgroundOn()
            self._renderer.SetBackground(0.06, 0.08, 0.12)
            self._renderer.SetBackground2(0.9,0.9,0.9)
        elif color == "light":
            self._renderer.GradientBackgroundOn()
            self._renderer.SetBackground(0.5, 0.5, 0.65)
            self._renderer.SetBackground2(1,1,1)
        else:
            self.background_color = [value/255 for value in color]
            self._renderer.GradientBackgroundOff()
            self._renderer.SetBackground(self.background_color)
        # self.update_logos_to_get_better_contrast()

    def update_logos_to_get_better_contrast(self):
        # Leave it disabled for now
        return

        if self.background_color in [(0,0,0), "dark"]:
            self._imageReader_pulse.SetFileName(Path('data/icons/logos/OpenPulse_logo_white.png'))

        elif self.background_color in [(0.25,0.25,0.25), "dark"]:
            self._imageReader_pulse.SetFileName(Path('data/icons/logos/OpenPulse_logo_white.png'))

        elif self.background_color in [(0.7,0.7,0.7), "light"]:
            self._imageReader_pulse.SetFileName(Path('data/icons/logos/OpenPulse_logo_black.png'))

        elif self.background_color in [(1,1,1), "light"]:
            self._imageReader_pulse.SetFileName(Path('data/icons/logos/OpenPulse_logo_black.png'))

        self._imageReader_pulse.Update()
        self._imageReader_mopt.Update()

    def set_colormap(self, colormap):
        self.colormap = colormap
        
    def changeNodesColor(self, color):
        self.nodes_color = color 
    
    def changeLinesColor(self, color):
        self.lines_color = color

    def changeSurfacesColor(self, color):
        self.surfaces_color = color
    
    def changeElementsTransparency(self, transparency):
        self.elements_transparency = transparency

    def change_font_color(self, color):
        #TODO: allow to change the top texts font color
        self.top_font_color = (0, 0, 0)
        self.textProperty.SetColor(self.top_font_color)
        self.bottom_font_color = [value/255 for value in color]
        self.colorBarTitleProperty.SetColor(self.bottom_font_color)
        self.colorBarLabelProperty.SetColor(self.bottom_font_color)
        self.scaleBarTitleProperty.SetColor(self.bottom_font_color)
        self.scaleBarLabelProperty.SetColor(self.bottom_font_color)

    def _createScaleBar(self):

        self._renderer.RemoveActor(self.scaleBar)
        width, height = self.getSize()
        self.scaleBar = vtk.vtkLegendScaleActor()
        self.scaleBarTitleProperty = self.scaleBar.GetLegendTitleProperty()
        self.scaleBarLabelProperty = self.scaleBar.GetLegendLabelProperty()
        self.scaleBarTitleProperty.SetColor(self.bottom_font_color)
        self.scaleBarLabelProperty.SetColor(self.bottom_font_color)
        
        if self.show_reference_scale:
            self.scaleBarTitleProperty.ShadowOff()
            self.scaleBarLabelProperty.ShadowOff()
            self.scaleBarTitleProperty.SetFontSize(14)
            self.scaleBarLabelProperty.SetFontSize(14)
            self.scaleBarTitleProperty.SetVerticalJustificationToTop()
            self.scaleBarTitleProperty.SetLineOffset(-40)
            self.scaleBarLabelProperty.SetLineOffset(-25)
            self.scaleBar.AllAxesOff()
            self._renderer.AddActor(self.scaleBar)
            # self.scaleBar.LegendVisibilityOff()
            # self.scaleBar.BottomAxisVisibilityOn()

    def _createColorBar(self):

        self.colorBarTitleProperty.SetFontSize(20)
        self.colorBarTitleProperty.ShadowOff()
        # self.colorBarTitleProperty.BoldOn()
        # self.colorBarTitleProperty.SetItalic(1)
        self.colorBarTitleProperty.SetJustificationToLeft()
        
        self.colorBarLabelProperty.SetFontSize(14)
        self.colorBarLabelProperty.ShadowOff()
        # self.colorBarLabelProperty.SetItalic(1)
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