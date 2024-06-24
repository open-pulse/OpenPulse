import vtk
import numpy as np 
from time import time
from scipy.spatial.transform import Rotation
from time import time

from pulse.interface.viewer_3d.actors.tube_clippable_actor import TubeClippableActor
from pulse.interface.viewer_3d.coloring.color_table import ColorTable

class TubeClippableDeformedActor(TubeClippableActor):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(project, opv, *args, **kwargs)
        self.transparent = False

    def source(self):
        visible_elements = {i:e for i, e in self.elements.items() if (i not in self.hidden_elements)}
        # self._key_index  = {j:i for i,j in enumerate(visible_elements)}
        self._key_indexes.clear()

        total_points_appended = 0 
        append_polydata = vtk.vtkAppendPolyData()
        for i, element in visible_elements.items():            
            x,y,z = element.first_node.deformed_coordinates
            section_rotation_xyz = element.deformed_rotation_xyz

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
        
        if visible_elements:
            append_polydata.Update()
            self._data = append_polydata.GetOutput()
        else:
            self._data = vtk.vtkPolyData()