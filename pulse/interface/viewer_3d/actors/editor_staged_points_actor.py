from vtkmodules.vtkRenderingCore import vtkPolyDataMapper

from molde.actors import GhostActor
from molde.poly_data import VerticesData
from molde.utils import set_polydata_colors

from pulse import app


class EditorStagedPointsActor(GhostActor):
    def __init__(self):
        super().__init__()
        self.points = app().project.pipeline.staged_points
        self.user_preferences = app().main_window.config.user_preferences
        self.build()

    def build(self):
        coords = [p.coords() for p in self.points]
        data = VerticesData(coords)
        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        self.SetMapper(mapper)

        staged_points_color = self.user_preferences.nodes_points_color.to_rgb()
        set_polydata_colors(data, staged_points_color)
        self.make_ghost()
        self.GetProperty().SetPointSize(8)
