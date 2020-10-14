from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkInteractorBase import vtkInteractorBase
from pulse.uix.vtk.actor.actorLine import ActorLine
from pulse.uix.vtk.vtkInteractorStyleClicker import vtkInteractorStyleClicker
import vtk
import numpy as np

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
        mesh = self.project.get_mesh()
        for entity in self.project.get_entities():
            elements = [mesh.structural_elements[i] for i in mesh.line_to_elements[entity.tag]]
            actor = self.createActorTubes(elements)
            self.actors[actor] = entity.get_tag()
            self._renderer.AddActor(actor)

            # plot = ActorLine(entity, self.plotRadius)
            # plot.build()
            # self.actors[plot.getActor()] = entity.get_tag()
            # self._renderer.AddActor(plot.getActor())

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




    # apaga por favor tá todo mundo pedindo pra apagar...
    def createActorTubes(self, elements):
        source = vtk.vtkAppendPolyData()
        mapper = vtk.vtkPolyDataMapper()
        actor = vtk.vtkActor()

        for element in elements:
            cross_section = element.cross_section
            if cross_section and self.plotRadius:
                label, parameters, *args = cross_section.additional_section_info
                if label == "Pipe section":
                    polygon = vtk.vtkRegularPolygonSource()
                    polygon.SetRadius(cross_section.external_diameter / 2)
                    polygon.SetNumberOfSides(20)
                else:
                    polygon = self.createSectionPolygon(element)
            else:
                polygon = vtk.vtkRegularPolygonSource()
                polygon.SetRadius(0.01)
                polygon.SetNumberOfSides(20)

            tube = self.generalSectionTube(element, polygon.GetOutputPort())
            source.AddInputData(tube.GetOutput())

        mapper.SetInputConnection(source.GetOutputPort())
        actor.SetMapper(mapper)
        return actor

    def createSectionPolygon(self, element):
        Yp, Zp, Yc, Zc, dict_lines_to_points = self.project.get_mesh().get_cross_section_points(element.index)
        points = vtk.vtkPoints()
        edges = vtk.vtkCellArray()
        data = vtk.vtkPolyData()
        poly = vtk.vtkPolygon()
        source = vtk.vtkTriangleFilter()

        for x, y in zip(Yp, Zp):
            points.InsertNextPoint(x-Yc, y-Zc, 0)    
        
        n = len(Yp)

        poly.GetPointIds().SetNumberOfIds(n)
        for i in range(n):
            poly.GetPointIds().SetId(i,i)
        edges.InsertNextCell(poly)
        
        data.SetPoints(points)
        data.SetPolys(edges)
        source.AddInputData(data)

        return source

    def generalSectionTube(self, element, section):
        start = element.last_node.coordinates
        end = element.first_node.coordinates
        size = element.length

        normalizedX = (end - start)
        normalizedX /= np.linalg.norm(normalizedX)

        normalizedZ = np.cross(normalizedX, [5,7,11]) # [5,7,11] is random
        normalizedZ /= np.linalg.norm(normalizedZ)

        normalizedY = np.cross(normalizedZ, normalizedX)

        matrix = vtk.vtkMatrix4x4()
        matrix.Identity()
        for i in range(3):
            matrix.SetElement(i, 0, normalizedZ[i])
            matrix.SetElement(i, 1, normalizedY[i])
            matrix.SetElement(i, 2, normalizedX[i])

        data = vtk.vtkTransformPolyDataFilter()
        extrusion = vtk.vtkLinearExtrusionFilter()
        transformation = vtk.vtkTransform()

        extrusion.SetScaleFactor(size)
        extrusion.SetInputConnection(section)
        transformation.Translate(start)
        transformation.Concatenate(matrix)
        data.SetTransform(transformation)
        data.SetInputConnection(extrusion.GetOutputPort())
        data.Update()
        return data