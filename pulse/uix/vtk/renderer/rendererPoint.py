from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkInteractorBase import vtkInteractorBase
from pulse.uix.vtk.actor.actorLine import ActorLine
from pulse.uix.vtk.actor.actorPoint import ActorPoint
from pulse.uix.vtk.vtkInteractorStyleClicker import vtkInteractorStyleClicker
import vtk
import numpy as np

class RendererPoint(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkInteractorStyleClicker(self))
        self.project = project
        self.opv = opv
        self.actors = {}

    def updateInfoText(self):
        listActorsIDs = self.getListPickedPoints()
        text = ""
        if len(listActorsIDs) == 0:
            text = ""
            vertical_position_adjust = None
        elif len(listActorsIDs) == 1:
            node = self.project.get_node(int(listActorsIDs[0]))
            values = node.get_prescribed_dofs()
            text = "Node ID  {}\nCoordinates:  ({:.3f}, {:.3f}, {:.3f})\nDisplacement:  ({}, {}, {})\nRotation:  ({}, {}, {})".format(listActorsIDs[0], node.x, node.y, node.z, values[0], values[1], values[2], values[3], values[4], values[5])
            vertical_position_adjust = (1-0.915)*960
        else:
            text = "{} nodes in selection:\n\n".format(len(listActorsIDs))
            i = 0
            correction = 1
            for ids in listActorsIDs:
                if i == 30:
                    text += "..."
                    factor = 1.02
                    break
                elif i == 19: 
                    text += "{}\n".format(ids)
                    factor = 1.02  
                    correction = factor/1.06            
                elif i == 9:
                    text += "{}\n".format(ids)
                    factor = 1.04
                    correction = factor/1.06
                else:
                    text += "{}  ".format(ids)
                    factor = 1.06*correction
                i+=1
            vertical_position_adjust = (1-0.88*factor)*960
        
        self.createInfoText(text, vertical_position_adjust)

    def plot(self):
        self.reset()
        for entity in self.project.get_entities():
            plot = ActorLine(entity)
            plot.setRadius(0.001)
            plot.build()
            self._renderer.AddActor(plot.getActor())
            self.actors[plot.getActor()] = -1

        for key, node in self.project.get_nodes().items():
            plot = ActorPoint(node, key)
            plot.build()
            self.actors[plot.getActor()] = key
            self._renderer.AddActor(plot.getActor())

    def changeColorPoints(self, points_id, color):
        actors = [key  for (key, value) in self.actors.items() if value in points_id]
        for actor in actors:
            actor.GetProperty().SetColor(color)

    def transformPointsToSphere(self, points_id):
        actors = [key  for (key, value) in self.actors.items() if value in points_id]
        for actor in actors:
            sphere = vtk.vtkSphereSource()
            sphere.SetRadius(0.03)
            pos = actor.GetCenter()
            sphere.SetCenter(pos[0], pos[1], pos[2])
            sphere.SetPhiResolution(11)
            sphere.SetThetaResolution(21)
            actor.GetMapper().SetInputConnection(sphere.GetOutputPort())

    def transformPointsToCube(self, points_id):
        actors = [key  for (key, value) in self.actors.items() if value in points_id]
        for actor in actors:
            cube = vtk.vtkCubeSource()
            pos = actor.GetCenter()
            cube.SetXLength(0.01)
            cube.SetYLength(0.01)
            cube.SetZLength(0.01)
            cube.SetCenter(pos[0], pos[1], pos[2])
            actor.GetMapper().SetInputConnection(cube.GetOutputPort())

    def transformPoints(self, points_id):
        self._style.clear()
        nodeAll = []
        nodeBC = []
        nodeF = []
        nodeND = []
        for node_id in points_id:
            node = self.project.get_node(node_id)

            if node.there_are_prescribed_dofs and node.there_are_nodal_loads:
                nodeAll.append(node_id)

            elif node.there_are_prescribed_dofs:
                nodeBC.append(node_id)
                if True in [True if isinstance(value, np.ndarray) else False for value in node.prescribed_dofs]:
                    colorBC = [1,1,1]
                elif sum([value if value is not None else complex(0) for value in node.prescribed_dofs]) != complex(0):
                    colorBC = [1,1,1]
                else:
                    colorBC = [0,0,0]
                self.changeColorPoints(nodeBC, colorBC)

            elif node.there_are_nodal_loads:
                nodeF.append(node_id)
                colorF = [1,1,0]
                self.changeColorPoints(nodeF, colorF)
            else:
                nodeND.append(node_id)

        colorAll = [0,1,0]
        colorND = [0,0,1]
        self.changeColorPoints(nodeAll, colorAll)
        self.changeColorPoints(nodeND, colorND)

        self.transformPointsToCube(nodeND)
        self.transformPointsToSphere(nodeAll)
        self.transformPointsToSphere(nodeBC)
        self.transformPointsToSphere(nodeF)

        self.updateInfoText()

    def getListPickedPoints(self):
        return self._style.getListPickedActors()

    def reset(self):
        for actor in self._renderer.GetActors():
            self._renderer.RemoveActor(actor)
        self.actors = {}
        self._style.clear()

    def update(self):
        self.opv.update()