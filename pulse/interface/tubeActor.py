import vtk
import numpy as np 
from time import time
from scipy.spatial.transform import Rotation

from pulse.interface.viewer_3d.actors.actor_base import ActorBase


class TubeActor(ActorBase):
    def __init__(self, project, *args, **kwargs):
        super().__init__()

        self.project = project
        self.preprocessor = project.preprocessor
        self.elements = project.get_structural_elements()
        
        self.hidden_elements = kwargs.get('hidden_elements', set())
        self.pressure_plot = kwargs.get('pressure_plot', False)
        
        self._key_index = {j:i for i,j in enumerate(self.elements.keys())}

        self.transparent = False
        self.bff = 5  # bug fix factor 

        self._data = vtk.vtkPolyData()
        self._mapper = vtk.vtkGlyph3DMapper()
        self.colorTable = None
        self._colors = vtk.vtkUnsignedCharArray()
        self._colors.SetNumberOfComponents(3)
        self._colors.SetNumberOfTuples(len(self.elements))


    @property
    def transparent(self):
        return self.__transparent

    @transparent.setter
    def transparent(self, value):
        if value:
            # opacity = 1 - self.opv.opvRenderer.elements_transparency
            opacity = 1
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

        points = vtk.vtkPoints()
        sources = vtk.vtkIntArray()
        sources.SetName('sources')
        rotations = vtk.vtkDoubleArray()
        rotations.SetNumberOfComponents(3)
        rotations.SetName('rotations')

        visible_elements = {i:e for i, e in self.elements.items() if (i not in self.hidden_elements)}
        self._key_index  = {j:i for i,j in enumerate(visible_elements)}

        self.updateBff()
        cache = dict()
        counter = 0
        # t0 = time()

        for i, element in visible_elements.items():
            
            radius = None
            max_min = None
            
            x,y,z = element.first_node.coordinates
            points.InsertNextPoint(x,y,z)
            section_rotation_xyz = element.section_rotation_xyz_undeformed

            rotations.InsertNextTuple(section_rotation_xyz)
            self._colors.InsertNextTuple((255,255,255))

            if element.valve_parameters:
                radius = element.valve_diameters[element.index][1]/2
            elif element.perforated_plate:
                radius = element.perforated_plate.hole_diameter/2        
            
            if element.cross_section_points:
                max_min = element.cross_section_points[2]

            key = (radius, max_min)
            if key not in cache:
                cache[key] = counter
                source = self.createTubeSection(element)
                self._mapper.SetSourceData(counter, source)
                counter += 1
            sources.InsertNextTuple1(cache[key])
        # dt = time() - t0  
        # print(f"tubeActor - elapsed time: {dt}s")
        self._data.SetPoints(points)
        self._data.GetPointData().AddArray(sources)
        self._data.GetPointData().AddArray(rotations)
        self._data.GetPointData().SetScalars(self._colors)

    def map(self):
        self._mapper.SetInputData(self._data)
        self._mapper.SourceIndexingOn()
        self._mapper.SetSourceIndexArray('sources')
        self._mapper.SetOrientationArray('rotations')
        self._mapper.SetScaleFactor(1 / self.bff)
        self._mapper.SetOrientationModeToRotation()
        self._mapper.Update()

    def filter(self):
        pass
    
    def actor(self):
        self._actor.SetMapper(self._mapper)
        self._actor.GetProperty().BackfaceCullingOff()

    def setColor(self, color, keys=None):
        c = vtk.vtkUnsignedCharArray()
        c.DeepCopy(self._colors)
        keys = keys if keys else self.elements.keys()
        
        for key in keys:
            index = self._key_index.get(key)
            if index is not None:
                c.SetTuple(index, color)

        self._data.GetPointData().SetScalars(c)
        self._colors = c
        self._mapper.Update()
    
    def setColorTable(self, colorTable):
        self.colorTable = colorTable

        c = vtk.vtkUnsignedCharArray()
        c.DeepCopy(self._colors)
        for key, element in self.elements.items():
            index = self._key_index.get(key, None)
            if index is None:
                continue
            color = self.colorTable.get_element_color(element)
            c.SetTuple(index, color)

        self._data.GetPointData().SetScalars(c)
        self._colors = c

    def updateBff(self):
        # At some stage of VTK creation of the Actor (and I can't properly say where),
        # the library destroys small or big structures. This factor is a random number, found 
        # empirically that strechs a lot the structure, and shrink it again when
        # everything is done. 

        # max representable: outer_diameter = 22
        # min representable: outer_diameter = 0.02

        min_ = 0
        max_ = 0        

        for element in self.elements.values():
            if element.cross_section is None:
                continue
            rad = element.cross_section.outer_diameter / 2
            min_ = min(rad, min_) if min_ else rad
            max_ = max(rad, max_)
                        
        avg = (min_ + max_) / 2
        self.bff = (5 / avg / 2) if avg else 5

    def createTubeSection(self, element):
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