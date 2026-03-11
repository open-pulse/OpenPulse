from molde.interactor_styles.arcball_camera_style import ArcballCameraInteractorStyle

from pulse import ICON_DIR
from pathlib import Path


class RenderTool(ArcballCameraInteractorStyle):

    def __init__(self):
        super().__init__()

        self.pan_cursor_path = ICON_DIR/"cursors/pan_cursor.png"
        self.zoom_cursor_path = ICON_DIR/"cursors/zoom_cursor.png"
        self.rotation_cursor_path = ICON_DIR/"cursors/rotation_cursor.png"

        self.current_cursor = "default"
        self.default_cursor = "default"
    
    def update_mouse_cursor_in_render_widgets(self, path: str | Path):
        self.current_cursor = path
        self.InvokeEvent("CursorChangedEvent")

    def start_rotating(self):
        if self.is_panning or self.is_zooming:
            return
        
        super().start_rotating()
        self.update_mouse_cursor_in_render_widgets(self.rotation_cursor_path)

    def stop_rotating(self):
        self.stop_all_actions()

    def start_panning(self):
        if self.is_rotating or self.is_zooming:
            return

        super().start_panning()
        self.update_mouse_cursor_in_render_widgets(self.pan_cursor_path)
    
    def stop_panning(self):
        self.stop_all_actions()
    
    def start_zooming(self):
        if self.is_rotating or self.is_panning:
            return

        super().start_zooming()
        self.update_mouse_cursor_in_render_widgets(self.zoom_cursor_path)
    
    def stop_zooming(self):
        self.stop_all_actions()
    
    def left_button_release_event(self, obj, event):
        self.stop_all_actions()
    
    def stop_all_actions(self):
        super().stop_zooming()
        super().stop_panning()
        super().stop_rotating()
        self.update_mouse_cursor_in_render_widgets(self.default_cursor)