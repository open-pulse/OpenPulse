from vtkmodules.vtkRenderingCore import vtkPolyDataMapper

from molde.actors import GhostActor
from molde.poly_data import VerticesData
from molde.utils import set_polydata_colors

from pulse import app


class EditorStagedPointsActor(GhostActor):
    def __init__(self):
        super().__init__()
        self.points = app().project.pipeline.staged_points
        self.build()

    def build(self):
        coords = [p.coords() for p in self.points]
        data = VerticesData(coords)
        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        self.SetMapper(mapper)

        set_polydata_colors(data, (255, 180, 50))
        self.make_ghost()
        self.GetProperty().SetPointSize(8)
