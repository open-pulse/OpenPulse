from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkTubeFilter
from vtkmodules.vtkFiltersSources import vtkArcSource, vtkDiskSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from pulse.utils.cell_utils import paint_data
from pulse.editor.structures import Bend


class BendActor(vtkActor):
    def __init__(self, bend: Bend):
        self.bend = bend
        self.create_geometry()

    def create_geometry(self):
        outer_radius = self.bend.diameter / 2
        inner_radius = (self.bend.diameter - self.bend.thickness) / 2

        arc_points = 50
        arc_source = vtkArcSource()
        arc_source.SetPoint1(self.bend.start.coords())
        arc_source.SetPoint2(self.bend.end.coords())
        arc_source.SetCenter(self.bend.center.coords())
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
