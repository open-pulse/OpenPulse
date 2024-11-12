from dataclasses import dataclass

from molde.colors import Color, color_names

@dataclass
class UserPreferences:
    renderer_background_color_1: Color = color_names.WHITE
    renderer_background_color_2: Color = color_names.WHITE
    points_color: Color = color_names.WHITE
    nodes_color: Color = color_names.WHITE
    lines_color: Color = color_names.WHITE
    tubes_color: Color = color_names.WHITE
    renderer_font_color: Color = color_names.WHITE
    renderer_font_size: int  = 16
    interface_font_size: int = 16

    def set_light_theme(self):
        self.renderer_background_color_1 = Color("#8092A6")
        self.renderer_background_color_2 = Color("#EEF2F3")
        self.renderer_font_color = Color("#111111")
    
    def set_dark_theme(self):
        self.renderer_background_color_1 = Color("#0b0f17")
        self.renderer_background_color_2 = Color("#3e424d")
        self.renderer_font_color = Color("#CCCCCC")

    def set_preferences_to_default(self):
        pass
