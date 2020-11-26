import vtk
import numpy as np 
from time import time
from scipy.spatial.transform import Rotation

from pulse.interface.tubeActor import TubeActor
from pulse.uix.vtk.colorTable import ColorTable

class TubeDeformedActor(TubeActor):
    def __init__(self, elements, project):
        super().__init__(elements, project)
        self.transparent = False

    def source(self):
        points = vtk.vtkPoints()
        sources = vtk.vtkIntArray()
        sources.SetName('sources')
        rotations = vtk.vtkDoubleArray()
        rotations.SetNumberOfComponents(3)
        rotations.SetName('rotations')

        cache = dict()
        counter = 0
        for element in self.elements.values():
            x,y,z = element.first_node.deformed_coordinates
            u,v,w = element.deformed_directional_vectors
            points.InsertNextPoint(x,y,z)
            r = Rotation.from_matrix(np.concatenate((u,v,w)).reshape(3,3))
            rotations.InsertNextTuple(r.as_euler('zxy', degrees=True))
            self._colors.InsertNextTuple((255,255,255))

            if element.cross_section not in cache:
                cache[element.cross_section] = counter
                source = self.createTubeSection(element)
                self._mapper.SetSourceData(counter, source)
                counter += 1
            sources.InsertNextTuple1(cache[element.cross_section])
        
        self._data.SetPoints(points)
        self._data.GetPointData().AddArray(sources)
        self._data.GetPointData().AddArray(rotations)
        self.setColorTable()

    def map(self):
        self._mapper.SetInputData(self._data)
        self._mapper.SourceIndexingOn()
        self._mapper.SetSourceIndexArray('sources')
        self._mapper.SetOrientationArray('rotations')
        self._mapper.SetOrientationModeToRotation()
        self._mapper.Update()

    def setColorTable(self):
        def get_deform(element):
            start = element.first_node.coordinates
            end = element.first_node.deformed_coordinates
            dist = np.linalg.norm(start - end)
            return dist

        deformations = np.array([get_deform(element) for element in self.elements.values()])
        Table = ColorTable(self.project, deformations)

        c = vtk.vtkUnsignedCharArray()
        c.DeepCopy(self._colors)
        for key, element in self.elements.items():
            index = self._key_index[key]
            color = Table.get_color_by_id(index)
            c.SetTuple(index, color)

        self._data.GetPointData().SetScalars(c)
        self._colors = c