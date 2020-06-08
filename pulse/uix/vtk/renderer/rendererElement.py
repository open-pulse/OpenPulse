from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkInteractorBase import vtkInteractorBase
from pulse.uix.vtk.actor.actorElement import ActorElement
import vtk

class RendererElement(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkInteractorBase(self))
        self.project = project
        self.opv = opv
        self.actors = {}

    def updateInfoText(self):
        self.update()

    def reset(self):
        for actor in self._renderer.GetActors():
            self._renderer.RemoveActor(actor)
        self.actors = {}
        self._style.clear()

    def plot(self):
        self.reset()
        for key, element in self.project.get_elements().items():
            plot = ActorElement(element, key)
            plot.build()
            self.actors[plot.getActor()] = key
            self._renderer.AddActor(plot.getActor())

    def update(self):
        self.opv.update()

    def getListPickedElements(self):
        return self._style.getListPickedActors()