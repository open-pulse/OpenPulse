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
        open_pulse_path = str(ICON_DIR/ 'logos/OpenPulse_logo_gray.png')

        self.open_pulse_logo = self._load_vtk_logo(open_pulse_path)
        self.open_pulse_logo.SetPosition(0.845, 0.89)
        self.open_pulse_logo.SetPosition2(0.15, 0.15)
        self.renderer.AddViewProp(self.open_pulse_logo)
        self.open_pulse_logo.SetRenderer(self.renderer)

    def _load_vtk_logo(self, path):
        image_reader = vtk.vtkPNGReader()
        image_reader.SetFileName(path)
        image_reader.Update()

        logo = vtk.vtkLogoRepresentation()
        logo.SetImage(image_reader.GetOutput())
        logo.ProportionalResizeOn()
        logo.GetImageProperty().SetOpacity(0.9)
        logo.GetImageProperty().SetDisplayLocationToBackground()
        return logo
