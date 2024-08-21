from vtkmodules.vtkRenderingCore import vtkPolyDataMapper

from molde.poly_data import VerticesData
from molde.actors import GhostActor

from pulse import app


class EditorSelectedPointsActor(GhostActor):
    def __init__(self):
        super().__init__()
        self.points = app().project.pipeline.selected_points
        self.build()

    def build(self):
        coords = [p.coords() for p in self.points]
        data = VerticesData(coords)
        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        self.SetMapper(mapper)

        self.GetProperty().SetPointSize(15)
        self.GetProperty().RenderPointsAsSpheresOn()
        self.GetProperty().SetColor([i / 255 for i in (255, 50, 50)])
        self.GetProperty().LightingOff()
        self.make_ghost()
