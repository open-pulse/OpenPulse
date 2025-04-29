from vtkmodules.vtkRenderingCore import vtkPolyDataMapper

from molde.poly_data import VerticesData
from molde.actors import GhostActor

from pulse import app


class EditorPointsActor(GhostActor):
    def __init__(self):
        super().__init__()
        self.points = app().project.pipeline.points
        self.user_preferences = app().main_window.config.user_preferences
        self.build()

    def build(self):
        coords = [p.coords() for p in self.points]
        data = VerticesData(coords)
        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        self.SetMapper(mapper)

        points_size = app().config.user_preferences.points_size
        self.GetProperty().SetPointSize(points_size)

        if not app().main_window.config.user_preferences.compatibility_mode:
            self.GetProperty().RenderPointsAsSpheresOn()
        editor_points_color = self.user_preferences.nodes_points_color.to_rgb()
        self.GetProperty().SetColor([i / 255 for i in editor_points_color])
        self.GetProperty().LightingOff()
        self.make_ghost()
