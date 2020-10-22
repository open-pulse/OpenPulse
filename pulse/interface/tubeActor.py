import vtk
import numpy as np 

from pulse.interface.vtkActorBase import vtkActorBase

class TubeActor(vtkActorBase):
    def __init__(self, elements, project):
        super().__init__()

        self.elements = elements
        self.project = project

        self._appendData = vtk.vtkAppendPolyData()
        self._mapper = vtk.vtkPolyDataMapper()

        self._cacheSection = dict()
        self._cacheMatrix = dict()
    
    def source(self):
        for element in self.elements:
            tubeSection = self.createTubeSection(element)
            transformation = self.createElementTransformation(element)
            tubeSection.SetTransform(transformation)
            tubeSection.Update()
          
            copyData = vtk.vtkPolyData()
            copyData.DeepCopy(tubeSection.GetOutput())

            self._appendData.AddInputData(copyData)
    
    def filter(self):
        pass
    
    def map(self):
        # Use this if you need performance, but loading time will be much longer
        # self._appendData.Update()
        # self._mapper.SetInputData(self._appendData.GetOutput())
        self._mapper.SetInputConnection(self._appendData.GetOutputPort())
    
    def actor(self):
        self._actor.SetMapper(self._mapper)
        self._actor.GetProperty().BackfaceCullingOff()
        self._actor.GetProperty().ShadingOff()

    def createTubeSection(self, element):
        if element.cross_section in self._cacheSection:
            return self._cacheSection[element.cross_section]

        extruderFilter = vtk.vtkLinearExtrusionFilter()
        transformPolyDataFilter = vtk.vtkTransformPolyDataFilter()

        polygon = vtk.vtkRegularPolygonSource()
        polygon.SetNumberOfSides(20)

        if not element.cross_section:
            polygon.SetRadius(0.01)
        else:
            label, parameters, *args = element.cross_section.additional_section_info
            if label == "Pipe section":
                polygon.SetRadius(element.cross_section.external_diameter / 2)
            else:
                polygon = self.createSectionPolygon(element)

        extruderFilter.SetInputConnection(polygon.GetOutputPort())
        transformPolyDataFilter.SetInputConnection(extruderFilter.GetOutputPort())

        self._cacheSection[element.cross_section] = transformPolyDataFilter
        return transformPolyDataFilter

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
    
    def createElementTransformation(self, element):
        start = element.first_node.coordinates
        end = element.last_node.coordinates
        size = element.length

        vector = tuple(end-start)
        if vector not in self._cacheMatrix:
            _, directionalVectors = element.get_local_coordinate_system_info()
            u, v, w = directionalVectors
            matrix = vtk.vtkMatrix4x4()
            matrix.Identity()
            for i in range(3):
                matrix.SetElement(i, 0, v[i])
                matrix.SetElement(i, 1, w[i])
                matrix.SetElement(i, 2, u[i]) 
            self._cacheMatrix[vector] = matrix
        else:
            matrix = self._cacheMatrix[vector]

        transformation = vtk.vtkTransform()
        transformation.Translate(start)
        transformation.Concatenate(matrix)
        transformation.Scale(1,1,size)

        return transformation