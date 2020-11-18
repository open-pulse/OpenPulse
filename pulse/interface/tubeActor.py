import vtk
import numpy as np 
from time import time

from pulse.uix.vtk.colorTable import ColorTable
from pulse.interface.vtkActorBase import vtkActorBase

class TubeActor(vtkActorBase):
    def __init__(self, elements, project, deformation=None):
        super().__init__()

        self.elements = elements
        self.project = project
        self.deformation = deformation

        self.transparent = True

        self._data = vtk.vtkPolyData()
        self._mapper = vtk.vtkPolyDataMapper()
        self._colors = vtk.vtkUnsignedCharArray()
        self._colors.SetNumberOfComponents(3)

        self._cachePolygon = dict()
        self._cacheMatrix = dict()
        self._colorSlices = dict()

    def update(self):
        opacity = 0.03 if self.transparent else 1
        lightining = not self.transparent
        
        self._actor.GetProperty().SetOpacity(opacity)
        self._actor.GetProperty().SetLighting(lightining)

    def source(self):
        indexes = list(self.elements.keys())
        sections = [self.createTubeSection(element) for element in self.elements.values()]
        matrices = [self.createMatrix(element) for element in self.elements.values()]
        
        tubeData = self.getTubeData(indexes, sections, matrices)       
        self._data = self.mergeData(tubeData)
    
    def map(self):
        self._mapper.SetInputData(self._data)
        self._mapper.SetColorModeToDirectScalars()

    def filter(self):
        pass
    
    def actor(self):
        self.update()
        self._actor.SetMapper(self._mapper)
        self._actor.GetProperty().BackfaceCullingOff()

    def setColor(self, color, keys=None):
        c = vtk.vtkUnsignedCharArray()
        c.DeepCopy(self._colors)

        keys = keys if keys else self.elements.keys()
        for key in keys:
            start, end = self._colorSlices[key]
            for i in range(start, end):
                c.SetTuple(i, color)

        self._data.GetPointData().SetScalars(c)
        self._colors = c

    def setColorTable(self, colorTable):
        pass

    def createTubeSection(self, element):
        if element.cross_section in self._cachePolygon:
            return self._cachePolygon[element.cross_section]   
    
        NUMBER_OF_SIDES = 20
        MINIMUM_RADIUS = 0.01

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
        
        self._cachePolygon[element.cross_section] = polygon
        return polygon

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
    
    def createMatrix(self, element):
        vec = tuple(element.last_node.coordinates - element.first_node.coordinates)

        if vec in self._cacheMatrix:
            # this cache may not look so usefull here
            # but it acelerates self._appendData.Update() 
            scale, rotation = self._cacheMatrix[vec]
        else:
            scale = self.createScaleMatrix(element)
            rotation = self.createRotationMatrix(element)
            self._cacheMatrix[vec] = scale, rotation

        translation = self.createTranslationMatrix(element)
        final = (rotation + translation) * scale
        
        matrix = vtk.vtkMatrix4x4()
        matrix.DeepCopy(final.flatten()) # numpy to vtk
        return matrix

    def createRotationMatrix(self, element):
        u,v,w = element.inverse_sub_rotation_matrix.T # directional vectors
        matrix = np.identity(4)
        matrix[0:3, 0] = v
        matrix[0:3, 1] = w
        matrix[0:3, 2] = u 
        return matrix

    def createTranslationMatrix(self, element):
        start = element.first_node.coordinates
        matrix = np.zeros((4,4))
        matrix[0:3, 3] = start 
        return matrix
    
    def createScaleMatrix(self, element):
        size = element.length
        matrix = np.ones((4,4))
        matrix[:, 2] = size
        return matrix
    
    def getTubeData(self, indexes, sections, matrices):
        # this may be the most costly function and should be implemented in c++ 
        tubeData = dict()
        transformation = vtk.vtkTransform()
        extruderFilter = vtk.vtkLinearExtrusionFilter()
        transformPolyDataFilter = vtk.vtkTransformPolyDataFilter()
        transformPolyDataFilter.SetInputConnection(extruderFilter.GetOutputPort())
        transformPolyDataFilter.SetTransform(transformation)

        for index, section, matrix in zip(indexes, sections, matrices):
            extruderFilter.SetInputConnection(section.GetOutputPort())
            transformation.SetMatrix(matrix)
            transformPolyDataFilter.Update()

            data = vtk.vtkPolyData()
            data.ShallowCopy(transformPolyDataFilter.GetOutput())
            tubeData[index] = data

        return tubeData

    def mergeData(self, dataset):
        data = vtk.vtkPolyData()
        appendData = vtk.vtkAppendPolyData()
        cleanData = vtk.vtkCleanPolyData()

        size = 0
        for key, data in dataset.items():
            points = data.GetNumberOfPoints()
            appendData.AddInputData(data)
            self._colorSlices[key] = (size, size+points)
            size += points
        self._colors.SetNumberOfTuples(size)

        cleanData.SetInputConnection(appendData.GetOutputPort())
        cleanData.PointMergingOff()
        cleanData.Update()
        data.DeepCopy(cleanData.GetOutput())

        return data
