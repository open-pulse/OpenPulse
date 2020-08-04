from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkInteractorBase import vtkInteractorBase
from pulse.uix.vtk.actor.actorLine import ActorLine
from pulse.uix.vtk.actor.actorPoint import ActorPoint
from pulse.uix.vtk.actor.actorElement import ActorElement
from pulse.uix.vtk.actor.actorEntityPoints import ActorEntityPoints
from pulse.uix.vtk.actor.actorEntityElements import ActorEntityElements
from pulse.uix.vtk.vtkInteractorStyleClickerMesh import vtkInteractorStyleClickerMesh
import vtk
import numpy as np

class RendererMesh(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkInteractorStyleClickerMesh(self))
        self.project = project
        self.opv = opv
        self.linePointsActors = {}
        self.lineElementsActors = {}
        self.pointsActors = {}
        self.elementsActors = {}
        self.axes = {}
        self.removedActorsPoints = []
        self.removedActorsElements = []

    def updateInfoText(self):
        listPointsIDs = self.getListPickedPoints()
        listElementsIDs = self.getListPickedElements()

        text = ""
        vertical_position_adjust = None
            
        if listPointsIDs != [] and listElementsIDs == []:
            textPoints = ""
            if len(listPointsIDs) == 0:
                textPoints = ""
                vertical_position_adjust = None
            elif len(listPointsIDs) == 1:
                node = self.project.get_node(int(listPointsIDs[0]))
                values = node.get_prescribed_dofs()
                textPoints = "Node ID  {}\nCoordinates:  ({:.3f}, {:.3f}, {:.3f})\nDisplacement:  ({}, {}, {})\nRotation:  ({}, {}, {})".format(listPointsIDs[0], node.x, node.y, node.z, values[0], values[1], values[2], values[3], values[4], values[5])
                vertical_position_adjust = (1-0.915)*960
            else:
                textPoints = "{} nodes in selection:\n\n".format(len(listPointsIDs))
                i = 0
                correction = 1
                for ids in listPointsIDs:
                    if i == 30:
                        textPoints += "..."
                        factor = 1.02
                        break
                    elif i == 19: 
                        textPoints += "{}\n".format(ids)
                        factor = 1.02  
                        correction = factor/1.06            
                    elif i == 9:
                        textPoints += "{}\n".format(ids)
                        factor = 1.04
                        correction = factor/1.06
                    else:
                        textPoints += "{}  ".format(ids)
                        factor = 1.06*correction
                    i+=1
                vertical_position_adjust = (1-0.88*factor)*960
            
            text = textPoints

        if listPointsIDs == [] and listElementsIDs != []:    
            textElements = ""
            if len(listElementsIDs) == 0:
                textElements = ""
                vertical_position_adjust = None
            elif len(listElementsIDs) == 1:
                element = self.project.get_element(int(listElementsIDs[0]))

                textElements = "Element ID: {}\n".format(listElementsIDs[0])
                node = element.first_node
                textElements += "Node ID (first node): {} -- Coordinates: ({:.3f}, {:.3f}, {:.3f}) [m]\n".format(node.external_index, node.x, node.y, node.z)
                node = element.last_node
                textElements += "Node ID (last node): {} -- Coordinates: ({:.3f}, {:.3f}, {:.3f}) [m]\n".format(node.external_index, node.x, node.y, node.z)
                textElements += "Element type: {}\n".format(element.element_type.upper())
                
                if element.cross_section is None:
                    textElements += "Diameter: {}\nThickness: {}\nOffset y: {}\nOffset z: {}\n".format("undefined", "undefined", "undefined", "undefined")
                else:
                    external_diameter = element.cross_section.external_diameter
                    thickness = element.cross_section.thickness
                    offset_y = element.cross_section.offset_y
                    offset_z = element.cross_section.offset_z
                    textElements += "Diameter: {} [m]\nThickness: {} [m]\nOffset y: {} [m]\nOffset z: {} [m]\n".format(external_diameter, thickness, offset_y, offset_z)

                if element.material is None:
                    textElements += "Material: {}\n".format("undefined")
                else:
                    textElements += "Material: {}\n".format(element.material.name.upper())

                if element.fluid is None:
                    textElements += "Fluid: {}\n".format("undefined")
                else:
                    textElements += "Fluid: {}\n".format(element.fluid.name.upper())

                vertical_position_adjust = (1-0.79)*960
            else:
                textElements = "{} elements in selection:\n\n".format(len(listElementsIDs))
                i = 0
                correction = 1
                for ids in listElementsIDs:
                    if i == 30:
                        textElements += "..."
                        factor = 1.02
                        break
                    elif i == 19: 
                        textElements += "{}\n".format(ids)
                        factor = 1.02  
                        correction = factor/1.06            
                    elif i == 9:
                        textElements += "{}\n".format(ids)
                        factor = 1.04
                        correction = factor/1.06
                    else:
                        textElements += "{}  ".format(ids)
                        factor = 1.06*correction
                    i+=1
                vertical_position_adjust = (1-0.88*factor)*960
            text = textElements

        self.createInfoText(text, vertical_position_adjust)

    def getSize(self):
        return self.project.get_element_size()*0.7

    def resetPlot(self):
        self.resetPoints()
        self.resetElements()
        self.removedActorsElements = []
        self.removedActorsPoints = []
        self.pointsActors = {}
        self.elementsActors = {}

    def resetPoints(self):
        actors = [key  for (key, value) in self.pointsActors.items()]
        for actor in actors:
            self._renderer.RemoveActor(actor)

        size = self.getSize()
        map_node = self.project.get_map_nodes()
        for entity in self.project.get_entities():
            if entity.tag not in self.removedActorsPoints:
                continue
            nodes = []
            for node in entity.nodes:
                try:
                    n = self.project.get_node(map_node[node[0]])
                    nodes.append(n)
                    self.plotAxes(n, map_node[node[0]])
                except Exception:
                    continue
            plot = ActorEntityPoints(nodes, size, entity.tag)
            plot.build()
            self.linePointsActors[plot.getActor()] = entity.tag
            self._renderer.AddActor(plot.getActor())

    def resetElements(self):
        actors = [key  for (key, value) in self.elementsActors.items()]
        for actor in actors:
            self._renderer.RemoveActor(actor)

        map_element = self.project.get_map_elements()
        for entity in self.project.get_entities():
            if entity.tag not in self.removedActorsElements:
                continue
            elements = []
            for element in entity.elements:
                try:
                    e = self.project.get_element(map_element[element[0]])
                    elements.append(e)
                except Exception:
                    continue
            
            plot = ActorEntityElements(elements, map_element[element[0]])
            plot.build()
            self.lineElementsActors[plot.getActor()] = entity.tag
            self._renderer.AddActor(plot.getActor())

    def plot(self):
        self.reset()
        self.plotLinesElements()
        self.plotLinesPoints()

    def plotLinesElements(self):
        map_element = self.project.get_map_elements()
        for entity in self.project.get_entities():
            elements = []
            for element in entity.elements:
                try:
                    e = self.project.get_element(map_element[element[0]])
                    elements.append(e)
                except Exception:
                    continue
            
            plot = ActorEntityElements(elements, map_element[element[0]])
            plot.build()
            self.lineElementsActors[plot.getActor()] = entity.tag
            self._renderer.AddActor(plot.getActor())
    
    def plotLinesPoints(self):
        size = self.getSize()
        map_node = self.project.get_map_nodes()
        for entity in self.project.get_entities():
            nodes = []
            for node in entity.nodes:
                try:
                    n = self.project.get_node(map_node[node[0]])
                    nodes.append(n)
                    self.plotAxes(n, map_node[node[0]])
                except Exception:
                    continue
            plot = ActorEntityPoints(nodes, size, entity.tag)
            plot.build()
            self.linePointsActors[plot.getActor()] = entity.tag
            self._renderer.AddActor(plot.getActor())

    def plotPoints(self, actorID):
        actor = [key  for (key, value) in self.linePointsActors.items() if value == actorID]
        self.removedActorsPoints.append(actorID)
        self._renderer.RemoveActor(actor[0])
        map_node = self.project.get_map_nodes()
        size = self.getSize()
        for node in self.project.get_entity(actorID).nodes:
            try:
                n = self.project.get_node(map_node[node[0]])
            except Exception:
                continue
            plot = ActorPoint(n, size=size, enableTransformation=False)
            plot.build()
            self.pointsActors[plot.getActor()] = map_node[node[0]]
            self._renderer.AddActor(plot.getActor())

    def plotElements(self, actorID):
        actor = [key  for (key, value) in self.lineElementsActors.items() if value == actorID]
        self.removedActorsElements.append(actorID)
        self._renderer.RemoveActor(actor[0])
        map_elements = self.project.get_map_elements()
        for element in self.project.get_entity(actorID).elements:
            try:
                n = self.project.get_element(map_elements[element[0]])
            except Exception:
                continue
            plot = ActorElement(n, size=0.003)
            plot.build()
            self.elementsActors[plot.getActor()] = map_elements[element[0]]
            self._renderer.AddActor(plot.getActor())

    def transformPoints(self, points_id):
        self._style.clear()
        for point in points_id:
            try:
                n = self.project.get_node(point)
                self.plotAxes(n, point)
            except Exception as e:
                print(e)

    def plotAxes(self, node, key_id):
        self.removeAxes(key_id)
        self.axes[key_id] = []
        self.plotForceAxes(node, key_id)
        self.plotBcAxes(node, key_id)
        self.plotRotationAxes(node, key_id)
        self.plotMomentoAxes(node, key_id)
        self.updateInfoText()

    def removeAxes(self, key):
        if self.axes.get(key) is not None:
            for actor in self.axes[key]:
                self._renderer.RemoveActor(actor)
            self.axes.pop(key)

    def transformAxe(self, node, negative_axe):
        transform = vtk.vtkTransform()
        transform.Translate(node.x, node.y, node.z)
        if negative_axe[0] == 1:
            transform.RotateZ(90)
            if negative_axe[1] == 1:
                transform.RotateY(270)
                if negative_axe[2] == 1:
                    transform.RotateY(-90)
                #Z +
            else:
                #Y +
                if negative_axe[2] == 1:
                    transform.RotateY(90)
        else:
            #X +
            if negative_axe[1] == 1:
                transform.RotateX(180)
                transform.RotateY(90)
                if negative_axe[2] == 1:
                    transform.RotateZ(90)
                #Z +
            else:
                #Y +
                if negative_axe[2] == 1:
                    transform.RotateZ(90)
                    transform.RotateX(180)
        return transform

    def getPosAxe(self, negative_axe, have_axe):
        if negative_axe[0] == 1:
            pos_axes = [1,0,2]
            if negative_axe[1] == 1:
                if negative_axe[2] == 1:
                    pos_axes = [1,0,2]
                else:
                    pos_axes = [1,2,0]
            else:
                if negative_axe[2] == 1:
                    pos_axes = [1,2,0]
                else:
                    pos_axes = [1,0,2]
        else:
            pos_axes = [0,1,2]
            if negative_axe[1] == 1:
                if negative_axe[2] == 1:
                    pos_axes = [2,0,1]
                else:
                    pos_axes = [2,1,0]
            else:
                if negative_axe[2] == 1:
                    pos_axes = [1,0,2]
                else:
                    pos_axes = [0,1,2]

        temp = [0,0,0]
        temp[pos_axes[0]] = have_axe[0]
        temp[pos_axes[1]] = have_axe[1]
        temp[pos_axes[2]] = have_axe[2]
        return temp

    def getReal(self, vector):
        new_vector = vector.copy()
        for i in range(len(vector)):
            if type(vector[i]) == complex:
                new_vector[i] = vector[i].real
        return new_vector

    def plotBcAxes(self, node, key_id):
        bc = self.getReal(node.getStructuralBondaryCondition())
        have_bc = [0,0,0]
        negative_bc = [0,0,0]
        for i in range(0,3):
            if bc[i] is not None:
                have_bc[i] = 1
            if bc[i] is not None and bc[i] < 0:
                negative_bc[i] = 1

        if have_bc.count(0) == 3:
            return
        
        transform = self.transformAxe(node, negative_bc)
        have_bc = self.getPosAxe(negative_bc, have_bc)
        
        axe = vtk.vtkAxesActor()
        axe.AxisLabelsOff()
        axe.SetTotalLength(0.02*have_bc[0],0.02*have_bc[1],0.02*have_bc[2])
        axe.SetShaftTypeToLine()
        axe.SetNormalizedTipLength(0.8*have_bc[0],0.8*have_bc[1],0.8*have_bc[2])
        axe.SetUserTransform(transform)
        axe.GetXAxisShaftProperty().SetColor(0,1,0)
        axe.GetYAxisShaftProperty().SetColor(0,1,0)
        axe.GetZAxisShaftProperty().SetColor(0,1,0)

        axe.GetXAxisTipProperty().SetColor(0,1,0)
        axe.GetYAxisTipProperty().SetColor(0,1,0)
        axe.GetZAxisTipProperty().SetColor(0,1,0)
        self.axes[key_id].append(axe)
        self._renderer.AddActor(axe)

    def plotRotationAxes(self, node, key_id):
        rotation = self.getReal(node.getStructuralBondaryCondition())
        have_rotation = [0,0,0]
        negative_rotation = [0,0,0]
        for i in range(3,6):
            if rotation[i] is not None and rotation[i] != 0:
                have_rotation[i-3] = 1
            if rotation[i] is not None and rotation[i] < 0:
                negative_rotation[i-3] = 1

        if have_rotation.count(0) == 3:
            return
        
        transform = self.transformAxe(node, negative_rotation)
        have_rotation = self.getPosAxe(negative_rotation, have_rotation)
        
        axe = vtk.vtkAxesActor()
        axe.AxisLabelsOff()
        axe.SetTotalLength(0.03*have_rotation[0],0.03*have_rotation[1],0.03*have_rotation[2])
        axe.SetShaftTypeToLine()
        axe.SetNormalizedTipLength(0.5*have_rotation[0],0.5*have_rotation[1],0.5*have_rotation[2])
        axe.SetUserTransform(transform)
        axe.GetXAxisShaftProperty().SetColor(1,0.64,0)
        axe.GetYAxisShaftProperty().SetColor(1,0.64,0)
        axe.GetZAxisShaftProperty().SetColor(1,0.64,0)

        axe.GetXAxisTipProperty().SetColor(1,0.64,0)
        axe.GetYAxisTipProperty().SetColor(1,0.64,0)
        axe.GetZAxisTipProperty().SetColor(1,0.64,0)
        self.axes[key_id].append(axe)
        self._renderer.AddActor(axe)

    def plotMomentoAxes(self, node, key_id):
        momento = self.getReal(node.get_prescribed_loads())
        have_momento = [0,0,0]
        negative_momento = [0,0,0]
        for i in range(3,6):
            if momento[i] is not None and momento[i] != 0:
                have_momento[i-3] = 1
            if momento[i] is not None and momento[i] < 0:
                negative_momento[i-3] = 1

        if have_momento.count(0) == 3:
            return

        transform = self.transformAxe(node, negative_momento)
        have_momento = self.getPosAxe(negative_momento, have_momento)
        
        axe = vtk.vtkAxesActor()
        axe.AxisLabelsOff()
        axe.SetTotalLength(0.15*have_momento[0], 0.15*have_momento[1], 0.15*have_momento[2])
        axe.SetShaftTypeToLine()
        axe.SetShaftTypeToCylinder()
        axe.SetCylinderRadius(self.getSize()*2)
        axe.SetNormalizedTipLength(0.2*have_momento[0], 0.2*have_momento[1], 0.2*have_momento[2])
        axe.SetUserTransform(transform)

        axe.GetXAxisShaftProperty().SetColor(0,0,1)
        axe.GetYAxisShaftProperty().SetColor(0,0,1)
        axe.GetZAxisShaftProperty().SetColor(0,0,1)

        axe.GetXAxisTipProperty().SetColor(0,0,1)
        axe.GetYAxisTipProperty().SetColor(0,0,1)
        axe.GetZAxisTipProperty().SetColor(0,0,1)

        axe2 = vtk.vtkAxesActor()
        axe2.AxisLabelsOff()
        axe2.SetTotalLength(0.18*have_momento[0], 0.18*have_momento[1], 0.18*have_momento[2])
        axe2.SetShaftTypeToLine()
        axe2.SetNormalizedTipLength(0.2*have_momento[0], 0.2*have_momento[1], 0.2*have_momento[2])
        axe2.SetUserTransform(transform)

        axe2.GetXAxisShaftProperty().SetColor(0,0,1)
        axe2.GetYAxisShaftProperty().SetColor(0,0,1)
        axe2.GetZAxisShaftProperty().SetColor(0,0,1)

        axe2.GetXAxisTipProperty().SetColor(0,0,1)
        axe2.GetYAxisTipProperty().SetColor(0,0,1)
        axe2.GetZAxisTipProperty().SetColor(0,0,1)

        self.axes[key_id].append(axe)
        self.axes[key_id].append(axe2)

        self._renderer.AddActor(axe)
        self._renderer.AddActor(axe2)

    def plotForceAxes(self, node, key_id):
        force = self.getReal(node.get_prescribed_loads())
        have_force = [0,0,0]
        negative_force = [0,0,0]
        for i in range(0,3):
            if force[i] is not None and force[i] != 0:
                have_force[i] = 1
            if force[i] is not None and force[i] < 0:
                negative_force[i] = 1

        if have_force.count(0) == 3:
            return

        transform = self.transformAxe(node, negative_force)
        have_force = self.getPosAxe(negative_force, have_force)
        
        axe = vtk.vtkAxesActor()
        axe.AxisLabelsOff()
        axe.SetTotalLength(0.15*have_force[0], 0.15*have_force[1], 0.15*have_force[2])
        axe.SetShaftTypeToLine()
        axe.SetShaftTypeToCylinder()
        axe.SetCylinderRadius(self.getSize()*2)
        axe.SetNormalizedTipLength(0.2*have_force[0], 0.2*have_force[1], 0.2*have_force[2])
        axe.SetUserTransform(transform)

        axe.GetXAxisShaftProperty().SetColor(1,0,0)
        axe.GetYAxisShaftProperty().SetColor(1,0,0)
        axe.GetZAxisShaftProperty().SetColor(1,0,0)

        axe.GetXAxisTipProperty().SetColor(1,0,0)
        axe.GetYAxisTipProperty().SetColor(1,0,0)
        axe.GetZAxisTipProperty().SetColor(1,0,0)

        self.axes[key_id].append(axe)
        self._renderer.AddActor(axe)

    def getListPickedPoints(self):
        return self._style.getListPickedActorsPoints()

    def getListPickedElements(self):
        return self._style.getListPickedActorsElements()

    def reset(self):
        for actor in self._renderer.GetActors():
            self._renderer.RemoveActor(actor)
        self.linePointsActors = {}
        self.lineElementsActors = {}
        self.pointsActors = {}
        self.elementsActors = {}
        self.axes = {}
        self.removedActorsPoints = []
        self.removedActorsElements = []
        self._style.clear()

    def update(self):
        self.opv.update()