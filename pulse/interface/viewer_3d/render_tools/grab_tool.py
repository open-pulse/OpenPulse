from pulse.interface.viewer_3d.render_tools.render_tool import RenderTool


class GrabTool(RenderTool):

    def __init__(self):
        super().__init__()

        self.update_mouse_cursor_in_render_widgets(self.pan_cursor_path)
        self.default_cursor = self.pan_cursor_path
    
    def left_button_press_event(self, obj, event):
        super().start_panning()
    
    def left_button_release_event(self, obj, event):
        super().stop_panning()
        self.update_mouse_cursor_in_render_widgets(self.pan_cursor_path)
