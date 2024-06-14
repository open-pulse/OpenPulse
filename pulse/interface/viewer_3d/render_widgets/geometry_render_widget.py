import vtk
from opps.interface.viewer_3d.render_widgets.editor_render_widget import EditorRenderWidget
from pulse import app, ICON_DIR


class GeometryRenderWidget(EditorRenderWidget):
    def __init__(self, parent=None):
        super().__init__(app().project.pipeline, parent)

        self.open_pulse_logo = None
        self.create_logos()
        self.set_theme("light")

    def create_logos(self, theme="light"):
        self.renderer.RemoveViewProp(self.open_pulse_logo)
        self.open_pulse_logo = self.create_logo(ICON_DIR/ 'logos/OpenPulse_logo_gray.png')
        self.open_pulse_logo.SetPosition(0.845, 0.89)
        self.open_pulse_logo.SetPosition2(0.15, 0.15)
