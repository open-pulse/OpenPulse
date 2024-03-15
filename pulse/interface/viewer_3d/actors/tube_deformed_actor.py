import vtk
import numpy as np 
from time import time
from scipy.spatial.transform import Rotation
from time import time

from pulse.interface.tubeActor import TubeActor
from pulse.interface.viewer_3d.coloring.colorTable import ColorTable

class TubeDeformedActor(TubeActor):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(project, opv, *args, **kwargs)
        self.transparent = False

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
        for element in visible_elements.values():
                        
            radius = None
            max_min = None
            
            x,y,z = element.first_node.deformed_coordinates
            points.InsertNextPoint(x,y,z)
            section_rotation_xyz = element.deformed_rotation_xyz

            rotations.InsertNextTuple(section_rotation_xyz)
            self._colors.InsertNextTuple((255,255,255))
            
            if element.valve_parameters:
                radius = element.valve_diameters[element.index][0]/2
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
        # print(f"tubeDeformedActor - elapsed time: {dt}s")
        self._data.SetPoints(points)
        self._data.GetPointData().AddArray(sources)
        self._data.GetPointData().AddArray(rotations)