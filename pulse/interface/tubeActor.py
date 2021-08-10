import vtk
import numpy as np 
from time import time
from scipy.spatial.transform import Rotation

from pulse.interface.vtkActorBase import vtkActorBase


class TubeActor(vtkActorBase):
    def __init__(self, elements, project, **kwargs):
        super().__init__()

        self.elements = elements
        self.project = project
        self.pressure_plot = kwargs.get('pressure_plot', False)
        
        self._key_index = {j:i for i,j in enumerate(self.elements.keys())}

        self.transparent = True
        self.bff = 5  # bug fix factor 

        self._data = vtk.vtkPolyData()
        self._mapper = vtk.vtkGlyph3DMapper()
        self.colorTable = None
        self._colors = vtk.vtkUnsignedCharArray()
        self._colors.SetNumberOfComponents(3)
        self._colors.SetNumberOfTuples(len(self.elements))
        print("TubeActor", len(self.elements))


    @property
    def transparent(self):
        return self.__transparent

    @transparent.setter
    def transparent(self, value):
        if value:
            self._actor.GetProperty().SetOpacity(0.2)
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

        self.updateBff()
        cache = dict()
        counter = 0

        for element in self.elements.values():
            x,y,z = element.first_node.coordinates
            points.InsertNextPoint(x,y,z)
            section_rotation_xyz = element.section_rotation_xyz_undeformed

            rotations.InsertNextTuple(section_rotation_xyz)
            self._colors.InsertNextTuple((255,255,255))
            
            key = (element.cross_section, round(element.length, 4))
            if key not in cache:
                cache[key] = counter
                source = self.createTubeSection(element)
                self._mapper.SetSourceData(counter, source)
                counter += 1
            sources.InsertNextTuple1(cache[key])

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
            index = self._key_index[key]
            c.SetTuple(index, color)
        self._data.GetPointData().SetScalars(c)
        self._colors = c
        self._mapper.Update()
    
    def setColorTable(self, colorTable):
        self.colorTable = colorTable

        c = vtk.vtkUnsignedCharArray()
        c.DeepCopy(self._colors)
        for key, element in self.elements.items():
            index = self._key_index[key]
            color = self.colorTable.get_color(element)
            c.SetTuple(index, color)

        self._data.GetPointData().SetScalars(c)
        self._colors = c

    def updateBff(self):
        # At some stage of VTK creation of the Actor (and I can't properly say where),
        # the library destroys small or big structures. This factor is a random number, found 
        # empirically that strechs a lot the structure, and shrink it again when
        # everything is done. 

        # it starts in 1 to prevent division by 0
        # and the difference is negligible
        sums = 1
        items = 1

        for element in self.elements.values():
            try:
                sec = element.cross_section.outer_diameter / 2
                sums += sec 
                items += 1
            except:                
                pass # it doesn't need to be so precise

        self.bff = 0.5 / (sums / items)

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
        if (element.cross_section is None):
            poly = vtk.vtkRegularPolygonSource()
            poly.SetNumberOfSides(3)
            poly.SetNormal(1,0,0)
            poly.SetRadius(1e-6)
            return poly

        if self.pressure_plot and (element.element_type in ['beam_1']):
            poly = vtk.vtkRegularPolygonSource()
            poly.SetNumberOfSides(3)
            poly.SetNormal(1,0,0)
            poly.SetRadius(1e-6)
            return poly

        if self.pressure_plot and (element.element_type not in ['beam_1']):
            r = element.cross_section.inner_diameter/2 * self.bff
            poly = vtk.vtkRegularPolygonSource()
            poly.SetNumberOfSides(20)
            poly.SetNormal(1,0,0)
            poly.SetRadius(r)
            return poly

        outer_points, inner_points = element.cross_section.get_cross_section_points()
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