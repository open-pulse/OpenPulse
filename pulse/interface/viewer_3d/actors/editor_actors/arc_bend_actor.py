import numpy as np

from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkTubeFilter
from vtkmodules.vtkFiltersSources import vtkArcSource, vtkLineSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from pulse.utils.cell_utils import paint_data
from pulse.utils.rotations import align_vtk_geometry
from pulse.editor.structures import ArcBend
from pulse.utils.cross_section_sources import closed_pipe_data



class ArcBendActor(vtkActor):
    def __init__(self, bend: ArcBend):
        self.bend = bend
        self.create_geometry()

    def create_geometry(self):
        outer_radius = self.bend.diameter / 2
        arc_points = 50
        tube_sides = 20
        center = self.bend.center

        if center is None:
            arc_source = vtkLineSource()
            arc_source.SetPoint1(self.bend.start.coords())
            arc_source.SetPoint2(self.bend.end.coords())
            arc_source.Update()

        else:
            polar_vector = self.bend.start.coords() - center.coords()
            arc_source = vtkArcSource()
            arc_source.UseNormalAndAngleOn()
            arc_source.SetPolarVector(polar_vector)
            arc_source.SetCenter(center.coords())
            arc_source.SetNormal(self.bend.normal())
            arc_source.SetAngle(np.degrees(self.bend.angle()))
            arc_source.SetResolution(arc_points // 2 - 1)
            arc_source.Update()

        external_faces = vtkTubeFilter()
        external_faces.SetInputData(arc_source.GetOutput())
        external_faces.SetNumberOfSides(tube_sides)
        external_faces.SetRadius(outer_radius)
        external_faces.CappingOn()
        external_faces.Update()
        data = external_faces.GetOutput()

        paint_data(data, self.bend.color.to_rgb())
        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
