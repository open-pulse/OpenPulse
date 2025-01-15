from vtkmodules.vtkRenderingCore import vtkActor

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication
from molde.interactor_styles import BoxSelectionInteractorStyle
from molde.pickers import CellAreaPicker, CellPropertyAreaPicker
from molde.render_widgets import CommonRenderWidget

from pulse.interface.viewer_3d.actors import EditorPointsActor, EditorStagedPointsActor, EditorSelectedPointsActor
from pulse import ICON_DIR, app
from pulse.interface.user_input.model.editor import pulsation_suppression_device_inputs


class PSDPreviewRenderWidget(CommonRenderWidget):

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

    def build_device_callback(self, data):
        