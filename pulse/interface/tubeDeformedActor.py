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
   
        self.updateBff()
        cache = dict()
        counter = 0
        
        for element in self.elements.values():
            x,y,z = element.first_node.deformed_coordinates
            points.InsertNextPoint(x,y,z)
            section_rotation_xyz = element.deformed_rotation_xyz

            rotations.InsertNextTuple(section_rotation_xyz)

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
