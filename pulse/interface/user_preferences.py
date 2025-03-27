from dataclasses import dataclass

from molde.colors import Color, color_names

@dataclass
class UserPreferences:
    interface_theme = "light"
    renderer_background_color_1: Color =  Color("#8092A6")
    renderer_background_color_2: Color = Color("#EEF2F3")
    nodes_points_color: Color = Color("#FFB432")
    lines_color: Color = Color("#5A5A5A")
    tubes_color: Color = color_names.WHITE
    renderer_font_color: Color = color_names.BLACK
    renderer_font_size: int  = 12
    show_open_pulse_logo : bool = True
    show_reference_scale_bar: bool = True
    compatibility_mode: bool = False   
    color_map = "jet"

    def set_light_theme(self):
        self.interface_theme = "light"
        self.renderer_background_color_1 = Color("#8092A6")
        self.renderer_background_color_2 = Color("#EEF2F3")
        self.renderer_font_color = Color("#111111")
        self.nodes_points_color = Color("#FFB432")
        self.lines_color = Color("#5A5A5A")
        self.tubes_color = color_names.WHITE
        self.renderer_font_color = color_names.BLACK
    
    def set_dark_theme(self):
        self.interface_theme = "dark"
        self.renderer_background_color_1 = Color("#0b0f17")
        self.renderer_background_color_2 = Color("#3e424d")
        self.renderer_font_color = Color("#CCCCCC")
        self.nodes_points_color = Color("#FFB432")
        self.lines_color = Color("#5A5A5A")
        self.tubes_color = color_names.WHITE
        self.renderer_font_color = color_names.WHITE

    def reset_font_size(self):
        self.renderer_font_size = 12
    
    def reset_open_pulse_logo(self):
        self.show_open_pulse_logo = True
    
    def reset_reference_scale_bar(self):
        self.show_reference_scale_bar = True