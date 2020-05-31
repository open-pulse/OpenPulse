from abc import ABC, abstractmethod 
import vtk
from pulse.uix.vtk.actor.actorSquare2D import ActorSquare2D

class vtkRendererBase(ABC):
    def __init__(self, style):
        super().__init__()
        self._renderer = vtk.vtkRenderer()
        self._renderer.SetBackground(0.2,0.2,0.2)
        self._style = style
        self._style.SetDefaultRenderer(self._renderer)
        self._textActor = vtk.vtkTextActor()
        self.actors = {}
        self._inUse = False
        self.squarePickerActor = ActorSquare2D((0,0), (0,0))
        self._usePicker = True
        self.textProperty = vtk.vtkTextProperty()
        self.textProperty.SetFontSize(16)
        self.textProperty.SetItalic(1)

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
        self._inUse = value

    def createInfoText(self, text, width = -1, height = -1):
        #Remove the actor if it already exists
        self._renderer.RemoveActor2D(self._textActor)
        if width == -1 and height == -1:
            #Empiric values
            width, height = self._renderer.GetSize()
            height -= 140
            width = 20
            # width, height = self._renderer.GetSize()
            # height = 35
            # width -= 250
        self._textActor.SetInput(text)
        self._textActor.SetTextProperty(self.textProperty)
        self._textActor.SetDisplayPosition(width, height)
        self._renderer.AddActor2D(self._textActor)

    def updateAreaPicker(self, posA, posB):
        if not self._usePicker:
            return
        self._renderer.RemoveActor2D(self.squarePickerActor.getActor())
        self.squarePickerActor = ActorSquare2D(posA, posB)
        self.squarePickerActor.build()
        self._renderer.AddActor2D(self.squarePickerActor.getActor())
        self.update()

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