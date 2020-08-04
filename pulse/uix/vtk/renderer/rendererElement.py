from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkInteractorBase import vtkInteractorBase
from pulse.uix.vtk.actor.actorElement import ActorElement
from pulse.uix.vtk.vtkInteractorStyleClicker import vtkInteractorStyleClicker
import vtk

class RendererElement(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkInteractorStyleClicker(self))
        self.project = project
        self.opv = opv
        self.actors = {}

    def updateInfoText(self):
        listActorsIDs = self.getListPickedElements()
        text = ""
        if len(listActorsIDs) == 0:
            text = ""
            vertical_position_adjust = None
        elif len(listActorsIDs) == 1:
            element = self.project.get_element(int(listActorsIDs[0]))
            # print(int(listActorsIDs[0]))
            text = "Element ID: {}\n".format(listActorsIDs[0])
            node = element.first_node
            text += "Node ID (first node): {} -- Coordinates: ({}, {}, {}) [m]\n".format(node.external_index, round(node.x,4), round(node.y,4), round(node.z,4))
            node = element.last_node
            text += "Node ID (last node): {} -- Coordinates: ({}, {}, {}) [m]\n".format(node.external_index, round(node.x,4), round(node.y,4), round(node.z,4))
            text += "Element type: {}\n".format(element.element_type.upper())
            
            if element.cross_section is None:
                text += "Diameter: {}\nThickness: {}\nOffset y: {}\nOffset z: {}\n".format("undefined", "undefined", "undefined", "undefined")
            else:
                external_diameter = element.cross_section.external_diameter
                thickness = element.cross_section.thickness
                offset_y = element.cross_section.offset_y
                offset_z = element.cross_section.offset_z
                text += "Diameter: {} [m]\nThickness: {} [m]\nOffset y: {} [m]\nOffset z: {} [m]\n".format(external_diameter, thickness, offset_y, offset_z)

            if element.material is None:
                text += "Material: {}\n".format("undefined")
            else:
                text += "Material: {}\n".format(element.material.name.upper())

            if element.fluid is None:
                text += "Fluid: {}\n".format("undefined")
            else:
                text += "Fluid: {}\n".format(element.fluid.name.upper())

            vertical_position_adjust = (1-0.79)*960
        else:
            text = "{} elements in selection:\n\n".format(len(listActorsIDs))
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

        self.createInfoText(text)

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