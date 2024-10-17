from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vtkmodules.vtkFiltersSources import vtkCubeSource, vtkCylinderSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper


class FixedPointActor(vtkActor):
    def __init__(self):
        super().__init__()
        self.create_geometry()

    def create_geometry(self):
        base = vtkCubeSource()
        cylinder = vtkCylinderSource()

        base.SetXLength(1)
        base.SetYLength(0.1)
        base.SetZLength(1)

        cylinder.SetHeight(1)
        cylinder.SetRadius(0.1)
        cylinder.SetCenter(0, 0.5, 0)

        base.Update()
        cylinder.Update()

        append_filter = vtkAppendPolyData()
        append_filter.AddInputData(base.GetOutput())
        append_filter.AddInputData(cylinder.GetOutput())
        append_filter.Update()

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(append_filter.GetOutput())
        self.SetMapper(mapper)
