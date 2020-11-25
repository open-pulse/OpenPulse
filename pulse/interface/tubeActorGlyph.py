import vtk
import numpy as np 
from time import time
from collections import defaultdict

from pulse.uix.vtk.colorTable import ColorTable
from pulse.interface.vtkActorBase import vtkActorBase

class TubeActor(vtkActorBase):
    def __init__(self, elements, project, deform=True):
        super().__init__()

        self.elements = elements
        self.project = project
        self.deform = deform

        self.transparent = True

        self._data = vtk.vtkPolyData()
        self._mapper = vtk.vtkPolyDataMapper()

        self.__color = None
        self.__to_color = None

    def update(self):
        return 
        opacity = 0.03 if self.transparent else 1
        lightining = not self.transparent

        self._actor.GetProperty().SetOpacity(opacity)
        self._actor.GetProperty().SetLighting(lightining)

    def source(self):
        sections_elements = defaultdict(list)
        for element in self.elements.values():
            sections_elements[element.cross_section].append(element)

        appendData = vtk.vtkAppendPolyData()
        for section, elements in sections_elements.items():
            source = self.createTubeSection(sections_elements[section][0])
            data = self.createTubeGlyphs(elements, source)
            appendData.AddInputData(data)

        appendData.Update()
        self._data = appendData.GetOutput()

    def map(self):
        self._mapper.SetInputData(self._data)
        # self._mapper.SetColorModeToDirectScalars()

    def filter(self):
        pass
    
    def actor(self):
        self.update()
        self._actor.SetMapper(self._mapper)
        self._actor.GetProperty().BackfaceCullingOff()

    def createTubeGlyphs(self, elements, source):
        points = vtk.vtkPoints()
        data = vtk.vtkPolyData()
        glyph = vtk.vtkTensorGlyph()
        tensors = vtk.vtkDoubleArray()
        tensors.SetNumberOfComponents(9)
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(9)

        for element in elements:
            try:
                x,y,z = element.first_node.deformed_coordinates
                u,v,w = element.deformed_directional_vectors
            except:
                x,y,z = element.first_node.coordinates
                u,v,w = element.directional_vectors

            color = (0,0,0, 0,0,0, 0,0,0)
            tensor = np.concatenate((v,w,u))
            tensors.InsertNextTuple(tensor)
            colors.InsertNextTuple(color)
            points.InsertNextPoint(x,y,z)

        glyph.ClampScalingOn()

        data.SetPoints(points)
        data.GetPointData().SetTensors(tensors)
        data.GetPointData().SetScalars(colors)
        glyph.SetInputData(data)
        glyph.SetSourceData(source)
        glyph.ThreeGlyphsOff()
        glyph.ExtractEigenvaluesOff()
        glyph.ColorGlyphsOff()
        glyph.SetColorModeToScalars()
        glyph.Update()
        return glyph.GetOutput()        

    def setColor(self, color, keys=None):
        return 

    def setColorTable(self, colorTable):
        pass

    def createTubeSection(self, element):
        NUMBER_OF_SIDES = 20
        MINIMUM_RADIUS = 0.01
        extruderFilter = vtk.vtkLinearExtrusionFilter()

        if not element.cross_section:
            polygon = vtk.vtkRegularPolygonSource()
            polygon.SetRadius(MINIMUM_RADIUS)
        else:
            label, parameters, *args = element.cross_section.additional_section_info
            if label == "Pipe section":
                polygon = vtk.vtkRegularPolygonSource()
                polygon.SetNumberOfSides(NUMBER_OF_SIDES)
                polygon.SetRadius(element.cross_section.external_diameter / 2)
            else:
                polygon = self.createSectionPolygon(element)
        
        size = self.project.get_element_size()
        extruderFilter.SetInputConnection(polygon.GetOutputPort())
        extruderFilter.SetScaleFactor(size)
        extruderFilter.Update()
        return extruderFilter.GetOutput()

    def createSectionPolygon(self, element):
        points = vtk.vtkPoints()
        edges = vtk.vtkCellArray()
        polygon = vtk.vtkPolygon()
        polyData = vtk.vtkPolyData()
        triangleFilter = vtk.vtkTriangleFilter() # this prevents bugs on extruder

        Xs, Ys = self.project.get_mesh().get_cross_section_points(element.index)
        polygon.GetPointIds().SetNumberOfIds(len(Xs))
        
        for i, (x, y) in enumerate(zip(Xs, Ys)):
            points.InsertNextPoint(x, y, 0)
            polygon.GetPointIds().SetId(i,i)
        edges.InsertNextCell(polygon)

        polyData.SetPoints(points)
        polyData.SetPolys(edges)
        triangleFilter.AddInputData(polyData)
        return triangleFilter