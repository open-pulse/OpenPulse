from dataclasses import dataclass

from molde.colors import Color

@dataclass
class UserPreferences:
    renderer_background_color_1: Color
    renderer_background_color_2: Color
    point_color: Color
    line_color: Color
    tube_color: Color
    renderer_font_color: Color
    renderer_font_size: int 
    font_size: int 

    def set_light_theme(self):
        self.renderer_background_color_1 = Color("#8092A6")
        self.renderer_background_color_2 = Color("#EEF2F3")
        self.renderer_font_color = Color("#111111")
    
    def set_dark_theme(self):
        self.renderer_background_color_1 = Color("#0b0f17")
        self.renderer_background_color_2 = Color("#3e424d")
        self.renderer_font_color = Color("#CCCCCC")
