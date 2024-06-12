import vtk
from collections import defaultdict
import numpy as np
from enum import Enum

from .tube_actor import TubeActor
from vtkat.utils import set_polydata_property, set_polydata_colors
from opps.interface.viewer_3d.utils import cross_section_sources 

class ColorMode(Enum):
    empty = 0
    material = 1
    fluid = 2


class TubeActorDeformed(TubeActor):
    def build(self):
        visible_elements = {i:e for i, e in self.elements.items() if (i not in self.hidden_elements)}
        # self._key_index  = {j:i for i,j in enumerate(visible_elements)}
        self._key_indexes = dict()

        mapper = vtk.vtkPolyDataMapper()
        append_polydata = vtk.vtkAppendPolyData()

        total_points_appended = 0 
        for i, element in visible_elements.items():            
            x,y,z = element.first_node.deformed_coordinates
            section_rotation_xyz = element.section_rotation_xyz_deformed

            source: vtk.vtkPolyData = self.create_element_data(element)
            if source is None:
                continue

            entity = self.preprocessor.elements_to_line[i]
            set_polydata_property(source, i, "element_index")
            set_polydata_property(source, entity, "entity_index")

            self._key_indexes[i] = range(total_points_appended, total_points_appended + source.GetNumberOfPoints())
            total_points_appended += source.GetNumberOfPoints()

            transform = vtk.vtkTransform()
            transform.Translate((element.length/2, 0, 0))
            transform.Translate((x,y,z))
            transform.RotateX(section_rotation_xyz[0])
            transform.RotateZ(section_rotation_xyz[2])
            transform.RotateY(section_rotation_xyz[1])
            transform.RotateY(180)
            transform.RotateZ(-90)
            transform.Update()

            transform_filter = vtk.vtkTransformFilter()
            transform_filter.SetInputData(source)
            transform_filter.SetTransform(transform)
            transform_filter.Update()

            append_polydata.AddInputData(transform_filter.GetOutput())
        
        append_polydata.Update()
        data: vtk.vtkPolyData = append_polydata.GetOutput()

        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)

        self.clear_colors()
