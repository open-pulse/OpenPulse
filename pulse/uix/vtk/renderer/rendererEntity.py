from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkInteractorBase import vtkInteractorBase
from pulse.uix.vtk.actor.actorLine import ActorLine
from pulse.uix.vtk.actor.actorSquare2D import ActorSquare2D
from pulse.uix.vtk.vtkInteractorStyleClicker import vtkInteractorStyleClicker
import vtk

class RendererEntity(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkInteractorStyleClicker(self))
        self.project = project
        self.opv = opv
        self.actors = {}
        self.squarePickerActor = ActorSquare2D((0,0), (0,0))
        self.plotRadius = False

    def updateInfoText(self):
        listActorsIDs = self.getListPickedEntities()
        text = ""
        if len(listActorsIDs) == 0:
            text = ""
        elif len(listActorsIDs) == 1:
            entity = self.project.get_entity(listActorsIDs[0])
            material_name = "Undefined"
            diam_ext = "Undefined"
            thickness = "Undefined"
            offset_y = "Undefined"
            offset_z = "Undefined"
            if entity.getMaterial() is not None:
                material_name = entity.getMaterial().getName()
            if entity.getCrossSection() is not None:
                diam_ext = entity.getCrossSection().getExternalDiameter()
                thickness = entity.getCrossSection().getThickness()
                offset_y = entity.getCrossSection().offset_y
                offset_z = entity.getCrossSection().offset_z
            text = "Line ID  {}\nMaterial:  {}\nExternal Diameter:  {} [m]\nThickness:  {} [m]\nOffset y: {} [m]\nOffset z: {} [m]".format(listActorsIDs[0], material_name, diam_ext, thickness, offset_y, offset_z)
        else:
            text = "Selected Lines:\n"
            i = 0
            for ids in listActorsIDs:
                if i == 30:
                    text += "..."
                    break
                if i == 10 or i == 20:
                    text += "{}\n".format(ids)
                else:
                    text += "{}  ".format(ids)
                i+=1
        self.createInfoText(text)

    def reset(self):
        for actor in self._renderer.GetActors():
            self._renderer.RemoveActor(actor)
        self.actors = {}
        self._style.clear()

    def plot(self):
        self.reset()
        for entity in self.project.get_entities():
            plot = ActorLine(entity, self.plotRadius)
            plot.build()
            self.actors[plot.getActor()] = entity.get_tag()
            self._renderer.AddActor(plot.getActor())

    def changeColorEntities(self, entity_id, color):
        self._style.clear()
        actors = [key  for (key, value) in self.actors.items() if value in entity_id]
        for actor in actors:
            actor.GetProperty().SetColor(color)
        self.updateInfoText()

    def getListPickedEntities(self):
        return self._style.getListPickedActors()

    def update(self):
        self.opv.update()

    def setPlotRadius(self, value):
        self.plotRadius = value

    def getPlotRadius(self):
        return self.plotRadius