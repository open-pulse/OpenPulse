import numpy as np

from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkTubeFilter
from vtkmodules.vtkFiltersSources import vtkArcSource, vtkDiskSource
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

        # Vtk needs the center of the arc to draw it.
        # If the center is aligned to the other points he 
        # can not draw it, because the arc is ambiguous.
        # Our solution is to draw two arcs that are not aligned

        if self.bend.center is not None:
            arc_points = 50
            arc_source_0 = vtkArcSource()
            arc_source_0.SetPoint1(self.bend.start.coords())
            arc_source_0.SetPoint2(self.bend.mid.coords())
            arc_source_0.SetCenter(self.bend.center.coords())
            arc_source_0.SetResolution(arc_points // 2 - 1)
            arc_source_0.Update()

            arc_source_1 = vtkArcSource()
            arc_source_1.SetPoint1(self.bend.mid.coords())
            arc_source_1.SetPoint2(self.bend.end.coords())
            arc_source_1.SetCenter(self.bend.center.coords())
            arc_source_1.SetResolution(arc_points // 2 - 1)
            arc_source_1.Update()

            external_faces_0 = vtkTubeFilter()
            external_faces_0.SetInputData(arc_source_0.GetOutput())
            external_faces_0.SetNumberOfSides(20)
            external_faces_0.SetRadius(outer_radius)
            external_faces_0.CappingOn()
            external_faces_0.Update()

            external_faces_1 = vtkTubeFilter()
            external_faces_1.SetInputData(arc_source_1.GetOutput())
            external_faces_1.SetNumberOfSides(20)
            external_faces_1.SetRadius(outer_radius)
            external_faces_1.CappingOn()
            external_faces_1.Update()

            append_polydata = vtkAppendPolyData()
            append_polydata.AddInputData(external_faces_0.GetOutput())
            append_polydata.AddInputData(external_faces_1.GetOutput())
            append_polydata.Update()
            data = append_polydata.GetOutput()

        else:
            vector = self.bend.end.coords() - self.bend.start.coords()
            length = np.linalg.norm(vector)
            source = closed_pipe_data(length, self.bend.diameter)
            data = align_vtk_geometry(source, self.bend.start.coords(), vector)

        paint_data(data, self.bend.color.to_rgb())
        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
