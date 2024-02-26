import vtk
import numpy as np 
from time import time
from scipy.spatial.transform import Rotation

from pulse.interface.viewer_3d.actors.actor_base import ActorBase


class TubeClippableActor(ActorBase):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__()

        self.project = project
        self.preprocessor = project.preprocessor
        self.elements = project.get_structural_elements()
        self.opv = opv
        
        self.hidden_elements = kwargs.get('hidden_elements', set())
        self.pressure_plot = kwargs.get('pressure_plot', False)
        
        # self._key_index = {j:i for i,j in enumerate(self.elements.keys())}
        self._key_indexes = dict()

        self.transparent = True
        self.bff = 1  # bug fix factor 

        self._data = vtk.vtkPolyData()
        self.point_data = vtk.vtkPolyData()
        self._mapper = vtk.vtkPolyDataMapper()
        self.colorTable = None
        self._colors = vtk.vtkUnsignedCharArray()
        self._colors.SetNumberOfComponents(3)
        self._colors.Allocate(len(self.elements) * 60)


    @property
    def transparent(self):
        return self.__transparent

    @transparent.setter
    def transparent(self, value):
        if value:
            opacity = 1 - self.opv.opvRenderer.elements_transparency
            if self.preprocessor.number_structural_elements > 2e5:
                self._actor.GetProperty().SetOpacity(0)
                self._actor.GetProperty().SetLighting(True)
            else:
                # self._actor.GetProperty().SetOpacity(0.15)
                self._actor.GetProperty().SetOpacity(opacity)
                self._actor.GetProperty().SetLighting(False)
        else:
            self._actor.GetProperty().SetOpacity(1)
            self._actor.GetProperty().SetLighting(True)
        self.__transparent = value

    def source(self):
        visible_elements = {i:e for i, e in self.elements.items() if (i not in self.hidden_elements)}
        # self._key_index  = {j:i for i,j in enumerate(visible_elements)}
        self._key_indexes.clear()

        total_points_appended = 0 
        append_polydata = vtk.vtkAppendPolyData()
        for i, element in visible_elements.items():            
            x,y,z = element.first_node.coordinates
            section_rotation_xyz = element.section_rotation_xyz_undeformed

            source = self.createTubeSection(element)
            self._key_indexes[i] = range(total_points_appended, total_points_appended + source.GetNumberOfPoints())
            total_points_appended += source.GetNumberOfPoints()

            for _ in range(source.GetNumberOfPoints()):
                self._colors.InsertNextTuple((255,255,255))

            transform = vtk.vtkTransform()
            transform.Translate((x,y,z))
            transform.RotateX(section_rotation_xyz[0])
            transform.RotateZ(section_rotation_xyz[2])
            transform.RotateY(section_rotation_xyz[1])
            transform.Update()

            transform_filter = vtk.vtkTransformFilter()
            transform_filter.SetInputData(source)
            transform_filter.SetTransform(transform)
            transform_filter.Update()

            append_polydata.AddInputData(transform_filter.GetOutput())
        
        append_polydata.Update()
        self._data = append_polydata.GetOutput()


    def map(self):
        self._mapper.SetInputData(self._data)

        # self._mapper.SetInputData(self._data)
        # self._mapper.SourceIndexingOn()
        # self._mapper.SetSourceIndexArray('sources')
        # self._mapper.SetOrientationArray('rotations')
        # self._mapper.SetScaleFactor(1 / self.bff)
        # self._mapper.SetOrientationModeToRotation()
        # self._mapper.Update()

    def filter(self):
        pass
    
    def actor(self):
        self._actor.SetMapper(self._mapper)
        # self._actor.GetProperty().BackfaceCullingOff()
        # self._actor.GetProperty().VertexVisibilityOn()
        # self._actor.GetProperty().SetPointSize(6)

    def setColor(self, color, keys=None):
        c = vtk.vtkUnsignedCharArray()
        c.DeepCopy(self._colors)
        keys = keys if keys else self.elements.keys()

        all_indexes = []
        if keys is not None:
            for key in keys:
                indexes = self._key_indexes.get(key, list())
                all_indexes.extend(list(indexes))

        for index in all_indexes:
            c.SetTuple(index, color)

        # for key in keys:
        #     index = self._key_index.get(key)
        #     if index is not None:
        #         c.SetTuple(index, color)

        # for key in keys:
        #     index = self._key_index[key]
        #     c.SetTuple(index, color)

        self._data.GetPointData().SetScalars(c)
        self._colors = c
        self._mapper.Update()
    
    def setColorTable(self, colorTable):
        self.colorTable = colorTable

        for key, element in self.elements.items():
            color = self.colorTable.get_color(element)
            self.setColor(color, keys=[key])

    def updateBff(self):
        '''
        This is actually not needed anymore in this class.
        But this function probably is called in a lot of places,
        so i think it is a bit safer to keep constant bff = 1.
        '''
        self.bff = 1

    def createTubeSection(self, element) -> vtk.vtkPolyData:
        extruderFilter = vtk.vtkLinearExtrusionFilter()
        polygon = self.createSectionPolygon(element)
        size = element.length
        extruderFilter.SetInputConnection(polygon.GetOutputPort())
        extruderFilter.SetExtrusionTypeToVectorExtrusion()
        extruderFilter.SetVector(1,0,0)
        extruderFilter.SetScaleFactor(size * self.bff)
        extruderFilter.Update()
        return extruderFilter.GetOutput()

    def createSectionPolygon(self, element):
        if None in [element.cross_section, element.cross_section_points]:
            poly = vtk.vtkRegularPolygonSource()
            poly.SetNumberOfSides(3)
            poly.SetNormal(1,0,0)
            poly.SetRadius(1e-6)
            return poly
        
        if self.pressure_plot:
            if element.element_type in ['beam_1']:
                poly = vtk.vtkRegularPolygonSource()
                poly.SetNumberOfSides(3)
                poly.SetNormal(1,0,0)
                poly.SetRadius(1e-6)
                return poly
            elif element.valve_parameters:
                r = (element.valve_diameters[element.index][1]/2) * self.bff
            elif element.perforated_plate:
                r = (element.perforated_plate.hole_diameter/2) * self.bff
            else:
                r = (element.cross_section.inner_diameter/2) * self.bff

            poly = vtk.vtkRegularPolygonSource()
            poly.SetNumberOfSides(36)
            poly.SetNormal(1,0,0)
            poly.SetRadius(r)
            return poly

        outer_points, inner_points, _ = element.cross_section_points
        number_inner_points = len(inner_points)
        number_outer_points = len(outer_points)
        
        # definitions
        points = vtk.vtkPoints()
        outerData = vtk.vtkPolyData()    
        innerPolygon = vtk.vtkPolygon()
        innerCell = vtk.vtkCellArray()
        innerData = vtk.vtkPolyData()
        delaunay = vtk.vtkDelaunay2D()
        
        outerPolygon = vtk.vtkPolygon()
        edges = vtk.vtkCellArray()
        source = vtk.vtkTriangleFilter()

        # create points       
        for y, z in inner_points:
            y *= self.bff
            z *= self.bff
            points.InsertNextPoint(0, y, z)

        for y, z in outer_points:
            y *= self.bff
            z *= self.bff
            points.InsertNextPoint(0, y, z)

        # create external polygon
        outerData.SetPoints(points)

        #TODO: clean-up the structure below
        if number_inner_points >= 3:
            
            delaunay.SetProjectionPlaneMode(2)
            delaunay.SetInputData(outerData)

            # remove inner area for holed sections
            for i in range(number_inner_points):
                innerPolygon.GetPointIds().InsertNextId(i)

            innerCell.InsertNextCell(innerPolygon)
            innerData.SetPoints(points)
            innerData.SetPolys(innerCell) 
            delaunay.SetSourceData(innerData)
            delaunay.Update()

            return delaunay

        else:
            # prevents bugs on the outer section
            for i in range(number_outer_points):
                outerPolygon.GetPointIds().InsertNextId(i)
            edges.InsertNextCell(outerPolygon)
            
            outerData.SetPolys(edges)
            source.AddInputData(outerData)
            return source
 
    def apply_cut(self, origin, normal):
        if self._data is None:
            return

        plane = vtk.vtkPlane()
        plane.SetOrigin(origin)
        plane.SetNormal(normal)

        clipper = vtk.vtkClipPolyData()
        clipper.SetInputData(self._data)
        clipper.SetClipFunction(plane)
        clipper.Update()
        self.clipped_data = clipper.GetOutput()

        mapper = self._mapper
        mapper.InterpolateScalarsBeforeMappingOn()
        mapper.SetInputData(self.clipped_data)
        mapper.Modified()

    def disable_cut(self):
        if self._data is None:
            return
        self.clipped_data = self._data
        mapper = self._mapper
        mapper.SetInputData(self._data)
        mapper.Modified()
