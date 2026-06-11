from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from pulse.utils.cell_utils import paint_data
from pulse.editor.structures.rigid_element import RigidElement


class RigidElementActor(vtkActor):
    def __init__(self, rigid: RigidElement):
        self.rigid = rigid
        self.create_geometry()

    def create_geometry(self):
        start = self.rigid.start.coords()
        end = self.rigid.end.coords()

        source = vtkLineSource()
        source.SetPoint1(*start)
        source.SetPoint2(*end)
        source.Update()

        data = source.GetOutput()
        paint_data(data, self.rigid.color.to_rgb())

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
        self.GetProperty().SetLineWidth(4)
