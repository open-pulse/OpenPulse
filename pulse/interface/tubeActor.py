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

        self.transparent = False

        self._data = vtk.vtkPolyData()
        self._mapper = vtk.vtkPolyDataMapper()
        self._colors = vtk.vtkUnsignedCharArray()
        self._colors.SetNumberOfComponents(3)

        self._cachePolygon = dict()
        self._colorSlices = dict()

    def update(self):
        opacity = 0.03 if self.transparent else 1
        lightining = not self.transparent
        
        self._actor.GetProperty().SetOpacity(opacity)
        self._actor.GetProperty().SetLighting(lightining)

    def source(self):
        indexes = list(self.elements.keys())
        sections = [self.createTubeSection(element) for element in self.elements.values()]
        matrices = self.createMatrices()

        s = time()
        self._data = self.getTubeData(indexes, sections, matrices.reshape(-1,16))       
        print('aaa', time()-s)

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
    
    def createMatrices(self):
        scale = self.createScaleMatrices()
        rotation = self.createRotationMatrices()
        translation = self.createTranslationMatrices()
        return (rotation + translation) * scale
    
    def createRotationMatrices(self, deform=False):
        # this is the uglyest thing i have done in my life
        # but it need to be very fast
        rotation = np.array([element.directional_vectors for element in self.elements.values()])
        rotation = rotation[:, [1,2,0]]
        rotation = np.transpose(rotation, axes=[0,2,1])
        rotation = np.insert(rotation, 3, values=0, axis=1) 
        rotation = np.insert(rotation, 3, values=0, axis=2)
        rotation[:,3,3] = 1
        return rotation

    def createTranslationMatrices(self, deform=False):
        size = (len(self.elements), 4, 4) 
        translation = np.zeros(size)
        translation[:, 0:3, 3] = [el.first_node.coordinates for el in self.elements.values()]
        return translation
    
    def createScaleMatrices(self, deform=False):
        size = (len(self.elements), 4, 4) 
        scale = np.ones(size)
        for i, element in enumerate(self.elements.values()):
            scale[i, :, 2] = element.length
        return scale

    def getTubeData(self, indexes, sections, matrices):
        transformation = vtk.vtkTransform()
        extruderFilter = vtk.vtkLinearExtrusionFilter()
        transformPolyDataFilter = vtk.vtkTransformPolyDataFilter()
        data = vtk.vtkPolyData()
        appendData = vtk.vtkAppendPolyData()
        cleanData = vtk.vtkCleanPolyData()   

        transformPolyDataFilter.SetInputConnection(extruderFilter.GetOutputPort())
        transformPolyDataFilter.SetTransform(transformation)
        cleanData.SetInputConnection(appendData.GetOutputPort())

        size = 0
        for index, section, matrix in zip(indexes, sections, matrices):
            extruderFilter.SetInputConnection(section.GetOutputPort())
            transformation.SetMatrix(matrix)
            transformPolyDataFilter.Update()

            data = vtk.vtkPolyData()
            data.ShallowCopy(transformPolyDataFilter.GetOutput())
            appendData.AddInputData(data)
            points = data.GetNumberOfPoints()
            self._colorSlices[index] = (size, size+points)
            size += points

        self._colors.SetNumberOfTuples(size)     

        cleanData.PointMergingOff()
        cleanData.PieceInvariantOn()
        cleanData.Update()
        data.DeepCopy(cleanData.GetOutput())
        return data


       