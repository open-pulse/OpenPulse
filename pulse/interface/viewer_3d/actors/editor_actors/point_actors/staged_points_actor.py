from molde.poly_data import VerticesData
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper


class StagedPointsActor(vtkActor):
    def __init__(self, points):
        super().__init__()
        self.points = points
        self.build()

    def build(self):
        coords = [p.coords() for p in self.points]
        data = VerticesData(coords)
        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        self.SetMapper(mapper)

        self.GetProperty().SetPointSize(10)
        self.GetProperty().SetColor([i / 255 for i in (255, 180, 50)])
        self.GetProperty().LightingOff()

        offset = -66000
        mapper.SetResolveCoincidentTopologyToPolygonOffset()
        mapper.SetRelativeCoincidentTopologyLineOffsetParameters(0, offset)
        mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(0, offset)
        mapper.SetRelativeCoincidentTopologyPointOffsetParameter(offset)
