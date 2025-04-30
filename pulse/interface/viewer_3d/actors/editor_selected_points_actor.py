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
        if not app().main_window.config.user_preferences.compatibility_mode:
            self.GetProperty().RenderPointsAsSpheresOn()

        user_preferences = app().config.user_preferences
        selection_color = user_preferences.selection_color.apply_factor(1.2).to_rgb()

        self.GetProperty().SetColor([i / 255 for i in selection_color])
        self.GetProperty().LightingOff()
        self.make_ghost()
