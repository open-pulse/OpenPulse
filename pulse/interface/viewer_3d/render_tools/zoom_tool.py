from pulse.interface.viewer_3d.render_tools.render_tool import RenderTool


class ZoomTool(RenderTool):

    def __init__(self):
        super().__init__()

        self.update_mouse_cursor_in_render_widgets(self.zoom_cursor_path)
        self.default_cursor = self.zoom_cursor_path
    
    def left_button_press_event(self, obj, event):
        super().start_zooming()
    
    def left_button_release_event(self, obj, event):
        super().stop_zooming()
        self.update_mouse_cursor_in_render_widgets(self.zoom_cursor_path)
    
    
    def key_release_event(self, obj, event):
        pass

        