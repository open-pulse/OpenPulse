from abc import ABC, abstractmethod 
import vtk

class vtkRendererBase(ABC):
    def __init__(self, style):
        super().__init__()

        self._renderer = vtk.vtkRenderer()
        self._renderer.SetBackground((0,0,0))

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
        # self.textProperty.BoldOn()
        # self.textProperty.SetItalic(1)
        
        self._logo_pulse = vtk.vtkLogoRepresentation()
        self._logo_mopt = vtk.vtkLogoRepresentation()
        self._imageReader_pulse = vtk.vtkPNGReader()
        self._imageReader_mopt = vtk.vtkPNGReader()

        self._createConfigLogos()
        # self._addLogosToRender(OpenPulse=self.opv.add_OpenPulse_logo, MOPT=self.opv.add_MOPT_logo)

    def _createConfigLogos(self):
        
        self._imageReader_pulse.SetFileName('data\\icons\\OpenPulse_logo3.png')
        self._imageReader_mopt.SetFileName('data\\icons\\mopt_logo2.png')
        self._imageReader_pulse.Update()
        self._imageReader_mopt.Update()
        
        self._logo_pulse_input = self._imageReader_pulse.GetOutput()
        self._logo_pulse.SetImage(self._logo_pulse_input)
        self._logo_pulse.ProportionalResizeOn()

        self._logo_mopt_input = self._imageReader_mopt.GetOutput()
        self._logo_mopt.SetImage(self._logo_mopt_input)
        self._logo_mopt.ProportionalResizeOn()
        
        self._logo_pulse.SetPosition(0.865, 0.88)
        self._logo_pulse.SetPosition2(0.14, 0.14)
     
        self._logo_pulse.GetImageProperty().SetOpacity(0.8)
        self._logo_pulse.GetImageProperty().SetDisplayLocationToBackground()

        self._logo_mopt.SetPosition(0, -0.01)
        self._logo_mopt.SetPosition2(0.1, 0.1)
     
        self._logo_mopt.GetImageProperty().SetOpacity(0.8)
        self._logo_mopt.GetImageProperty().SetDisplayLocationToBackground()  

        # self.logoWidget = vtk.vtkLogoWidget()
        # self.logoWidget.SetRepresentation(self._logo_pulse)
        # self.logoWidget.On()
        # self.logoWidget.SetEnabled(True)

    def _addLogosToRender(self, OpenPulse=True, MOPT=True):

        self._renderer.RemoveViewProp(self._logo_pulse)
        self._renderer.RemoveViewProp(self._logo_mopt)

        if OpenPulse:   
            self._renderer.AddViewProp(self._logo_pulse)
            self._logo_pulse.SetRenderer(self._renderer)
        
        if MOPT:
            self._renderer.AddViewProp(self._logo_mopt)
            self._logo_mopt.SetRenderer(self._renderer)

    def changeBackgroundColor(self, color):
        self._renderer.SetBackground(color)
    
    def changeFontColor(self, color):
        self.textProperty.SetColor(color)

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