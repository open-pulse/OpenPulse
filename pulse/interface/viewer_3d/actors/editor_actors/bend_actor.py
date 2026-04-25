from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkFiltersSources import vtkArcSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from pulse.editor.structures import Bend
from pulse.utils.cell_utils import paint_data
# from pulse.utils.cross_section_sources import apply_transform
from pulse.utils.rotations import transformation_matrix_3x3

import numpy as np


class BendActor(vtkActor):
    def __init__(self, bend: Bend):
        self.bend = bend
        self.create_geometry()

    def create_geometry(self):
        outer_radius = self.bend.diameter / 2
        offset_y = self.bend.offset_y 
        offset_z = self.bend.offset_z 
        
        # the offsets will be enabled in future updates
        offsets = 0 * np.array([0, offset_y, offset_z], dtype=float)

        #TODO: compute the unity normal vector of the cross-section at 
        # the start point and use this vector to rotate the offsets
        normal_vector = (1, 0, 0)

        # compute the transformation matrix
        rot_matrix = transformation_matrix_3x3( 
            normal_vector[0],
            normal_vector[1],
            normal_vector[2],
            gamma = 0.,
            )

        shift = rot_matrix.T @ offsets

        start = self.bend.start.coords() + shift
        end = self.bend.end.coords() + shift
        center = self.bend.center.coords() + shift

        #TODO: the shifted end point coordinates should update the 
        # start point of the next pipe structure

        arc_points = 10
        arc_source = vtkArcSource()
        arc_source.SetPoint1(start)
        arc_source.SetPoint2(end)
        arc_source.SetCenter(center)
        arc_source.SetResolution(arc_points - 1)
        arc_source.Update()

        external_faces = vtkTubeFilter()
        external_faces.SetInputData(arc_source.GetOutput())
        external_faces.SetNumberOfSides(20)
        external_faces.SetRadius(outer_radius)
        external_faces.CappingOn()
        external_faces.Update()

        data = external_faces.GetOutput()
        paint_data(data, self.bend.color.to_rgb())

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
