from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkInteractorBase import vtkInteractorBase
from pulse.uix.vtk.actor.actorLine import ActorLine
from pulse.uix.vtk.vtkInteractorStyleClicker import vtkInteractorStyleClicker
import vtk

class RendererEntity(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkInteractorStyleClicker(self))
        self.project = project
        self.opv = opv
        self.actors = {}
        self.plotRadius = False

    def updateInfoText(self):
        listActorsIDs = self.getListPickedEntities()
        text = ''
        if len(listActorsIDs) == 0: 
            text = ''

        elif len(listActorsIDs) == 1:

            entity = self.project.get_entity(listActorsIDs[0])
            
            e_type = 'undefined'
            material_name = 'undefined'
            diam_ext, thickness = 'undefined', 'undefined'
            offset_y, offset_z = 'undefined', 'undefined'
            
            if entity.getMaterial() is not None:
                material_name = entity.getMaterial().getName()

            if entity.element_type is not None:
                e_type = entity.element_type.upper()

            if entity.tag in (self.project.lines_multiples_cross_sections or self.project.file.lines_multiples_cross_sections):

                if len(self.project.lines_multiples_cross_sections) != 0:
                    number_cross_sections = self.project.lines_multiples_cross_sections.count(entity.tag)
                    # print(self.project.lines_multiples_cross_sections)

                if len(self.project.file.lines_multiples_cross_sections) != 0:
                    number_cross_sections = self.project.file.lines_multiples_cross_sections.count(entity.tag)
                    # print(self.project.file.lines_multiples_cross_sections)

                if entity.element_type is not None and entity.element_type not in ['beam_1']:
                
                    diam_ext, thickness = 'multiples', 'multiples'
                    offset_y, offset_z = 'multiples', 'multiples'
                    insulation_thickness, insulation_density = 'multiples', 'multiples'

                    text = 'Line ID  {} ({} cross-sections)\n\n'.format(listActorsIDs[0], number_cross_sections)              
                    text += 'Material:  {}\n'.format(material_name)
                    text += 'Element type:  {}\n'.format(e_type)
                    text += 'External diameter: {} [m]\n'.format(diam_ext)
                    text += 'Thickness: {} [m]\n'.format(thickness)
                    if offset_y != 0 or offset_z != 0:
                        text += 'Offset y: {} [m]\nOffset z: {} [m]\n'.format(offset_y, offset_z)
                    if insulation_thickness != 0 or insulation_density != 0: 
                        text += 'Insulation thickness: {} [m]\nInsulation density: {} [kg/m³]'.format(insulation_thickness, int(insulation_density))

            else:

                if entity.getCrossSection() is not None:
                    if entity.element_type is not None and entity.element_type not in ['beam_1']:
                        text = ''
                        diam_ext = entity.getCrossSection().external_diameter
                        thickness = entity.getCrossSection().thickness
                        offset_y = entity.getCrossSection().offset_y
                        offset_z = entity.getCrossSection().offset_z
                        insulation_thickness = entity.crossSection.insulation_thickness
                        insulation_density = entity.crossSection.insulation_density

                        text += 'Line ID  {}\n\n'.format(listActorsIDs[0])
                        text += 'Material:  {}\n'.format(material_name)
                        text += 'Element type:  {}\n'.format(e_type)
                        text += 'External Diameter:  {} [m]\n'.format(diam_ext)
                        text += 'Thickness:  {} [m]\n'.format(thickness)
                        if offset_y != 0 or offset_z != 0:
                            text += 'Offset y: {} [m]\nOffset z: {} [m]\n'.format(offset_y, offset_z)
                        if insulation_thickness != 0 or insulation_density != 0: 
                            text += 'Insulation thickness: {} [m]\nInsulation density: {} [kg/m³]'.format(insulation_thickness, int(insulation_density))
            
                    elif entity.element_type is not None and entity.element_type in ['beam_1']:

                        text = ''
                        area = entity.getCrossSection().area
                        Iyy = entity.getCrossSection().second_moment_area_y
                        Izz = entity.getCrossSection().second_moment_area_z
                        Iyz = entity.getCrossSection().second_moment_area_yz
                        additional_section_info = entity.getCrossSection().additional_section_info

                        text += 'Line ID  {}\n\n'.format(listActorsIDs[0])
                        text += 'Material:  {}\n'.format(material_name)

                        if additional_section_info is not None:
                            text += 'Element type:  {} ({})\n'.format(e_type, additional_section_info[0].capitalize())
                        else:
                            text += 'Element type:  {} (-)\n'.format(e_type)

                        text += 'Area:  {} [m²]\n'.format(area)
                        text += 'Iyy:  {} [m^4]\n'.format(Iyy)
                        text += 'Izz:  {} [m^4]\n'.format(Izz)
                        text += 'Iyz:  {} [m^4]\n'.format(Iyz)

        else:

            text = '{} lines in selection:\n\n'.format(len(listActorsIDs))
            i = 0
            for ids in listActorsIDs:
                if i == 30:
                    text += '...'

                    break
                elif i == 19: 
                    text += '{}\n'.format(ids)
                elif i == 9:
                    text += '{}\n'.format(ids)
                else:
                    text += '{}  '.format(ids)
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
        self.opv.updateDialogs()

    def setPlotRadius(self, value):
        self.plotRadius = value

    def getPlotRadius(self):
        return self.plotRadius