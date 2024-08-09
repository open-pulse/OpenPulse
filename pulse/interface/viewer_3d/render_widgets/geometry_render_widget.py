from opps.interface.viewer_3d.render_widgets.editor_render_widget import (
    EditorRenderWidget,
)

from pulse import ICON_DIR, app


class GeometryRenderWidget(EditorRenderWidget):
    def __init__(self, parent=None):
        super().__init__(app().project.pipeline, parent)

        app().main_window.visualization_changed.connect(
            self.visualization_changed_callback
        )

        self.open_pulse_logo = None
        self.create_logos()
        self.set_theme("light")

        self.renderer.RemoveAllLights()
        self.create_camera_light(0.1, 0.1)

    def create_logos(self, theme="light"):
        self.renderer.RemoveViewProp(self.open_pulse_logo)
        self.open_pulse_logo = self.create_logo(
            ICON_DIR / "logos/OpenPulse_logo_gray.png"
        )
        self.open_pulse_logo.SetPosition(0.845, 0.89)
        self.open_pulse_logo.SetPosition2(0.15, 0.15)

    def visualization_changed_callback(self):
        if not self._actor_exists():
            return

        visualization = app().main_window.visualization_filter
        self.control_points_actor.SetVisibility(visualization.points)
        self.staged_points_actor.SetVisibility(visualization.points)
        self.selected_points_actor.SetVisibility(visualization.points)
        self.pipeline_actor.SetVisibility(visualization.tubes)
        opacity = 0.9 if visualization.transparent else 1
        self.pipeline_actor.GetProperty().SetOpacity(opacity)
        self.update()

    def _actor_exists(self):
        actors = [
            self.control_points_actor,
            self.staged_points_actor,
            self.selected_points_actor,
            self.pipeline_actor,
        ]
        return all([actor is not None for actor in actors])
