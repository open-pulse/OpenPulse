from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkInteractorStyleClicker import vtkInteractorStyleClicker
from pulse.uix.vtk.vtkMeshClicker import vtkMeshClicker
from pulse.uix.vtk.actor.actorPoint import ActorPoint
from pulse.uix.vtk.actor.actorElement import ActorElement
import vtk

class RendererMesh(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkMeshClicker(self))
        self.project = project
        self.opv = opv 

        self._rendererPoints = vtk.vtkRenderer()
        self._rendererElements = vtk.vtkRenderer()
        self._rendererPoints.DrawOff()
        self._rendererElements.DrawOff()

    
    def getRendererPoints(self):
        return 
    
    def getRendererElements(self):
        return 
    
    def getListPickedPoints(self):
        return 
    
    def getListPickedElements(self):
        return
    
    def plot(self):
        self.reset()
        self.plotMain()
        self.plotPoints()
        self.plotElements()

    def reset(self):
        self._renderer.RemoveAllViewProps()
        self._rendererPoints.RemoveAllViewProps()
        self._rendererElements.RemoveAllViewProps()
        self._style.clear()
    
    def update(self):
        self.opv.update()

    def updateInfoText(self):
        numberPoints = len(self._style.getSelectedPoints())
        numberElements = len(self._style.getSelectedElements())
        text = f'{numberPoints} points \n{numberElements} elements'
        self.createInfoText(text)

    # 
    def plotMain(self):
        source = vtk.vtkAppendPolyData()
        mapper = vtk.vtkPolyDataMapper()
        actor = vtk.vtkActor()

        for key, node in self.project.get_nodes().items():
            sphere = vtk.vtkSphereSource()
            sphere.SetRadius(0.02)
            sphere.SetCenter(node.coordinates)
            source.AddInputConnection(sphere.GetOutputPort())

        for key, element in self.project.get_elements().items():
            plot = ActorElement(element, key)
            plot.build()
            source.AddInputData(plot.getActor().GetMapper().GetInput())
        
        mapper.SetInputConnection(source.GetOutputPort())
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0.6,0,0.4)
        actor.GetProperty().SetDiffuse(1)
        actor.GetProperty().SetSpecular(0)
        self._renderer.AddActor(actor)
    
    def plotPoints(self):
        for key, node in self.project.get_nodes().items():
            sphere = vtk.vtkSphereSource()
            mapper = vtk.vtkPolyDataMapper()
            actor = vtk.vtkActor()
            
            sphere.SetRadius(0.02)
            sphere.SetCenter(node.coordinates)
            mapper.SetInputConnection(sphere.GetOutputPort())
            actor.SetMapper(mapper)

            self._rendererPoints.AddActor(actor)
    
    def plotElements(self):
        for key, element in self.project.get_elements().items():
            plot = ActorElement(element, key)
            plot.build()
            self._rendererElements.AddActor(plot.getActor())
