from vtk import vtkAppendPolyData, vtkLineSource, vtkTubeFilter, vtkPolyDataMapper, vtkSphereSource
from vtkmodules.vtkRenderingCore import vtkActor

from molde.render_widgets import CommonRenderWidget

from pulse import ICON_DIR, app
from pulse.editor.pulsation_damper import PulsationDamper

class DamperPreviewRenderWidget(CommonRenderWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_window = app().main_window

        # It is better for an editor to have parallel projection
        self.renderer.GetActiveCamera().SetParallelProjection(True)
        self.renderer.RemoveAllLights()

        self.create_axes()
        self.create_camera_light(0.1, 0.1)

    
        self.update_plot()

    def update_plot(self):
        self.update()

    def build_device_preview(self, device_data):
        device = PulsationDamper(device_data)
