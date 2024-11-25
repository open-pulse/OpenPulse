from pathlib import Path
import json

from pulse import app

from pulse.interface.user_preferences import UserPreferences
from molde.colors import Color

class Config2:
    
    def __init__(self):
        self.config_path = Path().home() / "pulse_config.json"
        self.user_preferences = UserPreferences()

        self.load_config_file()

    def load_config_file(self):
        try:
            with open(self.config_path, "r") as file:
                user_preferences = json.load(file)

                self.user_preferences.interface_theme = user_preferences["interface_theme"]
                self.user_preferences.renderer_background_color_1 = Color(*user_preferences["renderer_background_color_1"])
                self.user_preferences.renderer_background_color_2 = Color(*user_preferences["renderer_background_color_2"])
                self.user_preferences.nodes_points_color = Color(*user_preferences["nodes_points_color"])
                self.user_preferences.lines_color = Color(*user_preferences["lines_color"])
                self.user_preferences.tubes_color = Color(*user_preferences["tubes_color"])
                self.user_preferences.renderer_font_color = Color(*user_preferences["renderer_font_color"])
                self.user_preferences.renderer_font_size = user_preferences["renderer_font_size"]
                self.user_preferences.interface_font_size = user_preferences["interface_font_size"]
                self.user_preferences.show_open_pulse_logo = user_preferences["show_open_pulse_logo"]
                self.user_preferences.show_reference_scale_bar = user_preferences["show_reference_scale_bar"]

        except FileNotFoundError:
            self.write_config_file()

    def write_config_file(self):
        data = {
            "interface_theme" : self.user_preferences.interface_theme,
            "renderer_background_color_1" : self.user_preferences.renderer_background_color_1.to_rgb(),
            "renderer_background_color_2" : self.user_preferences.renderer_background_color_2.to_rgb(),
            "nodes_points_color" : self.user_preferences.nodes_points_color.to_rgb(),
            "lines_color" : self.user_preferences.lines_color.to_rgb(),
            "tubes_color" : self.user_preferences.tubes_color.to_rgb(),
            "renderer_font_color" : self.user_preferences.renderer_font_color.to_rgb(),
            "renderer_font_size" : self.user_preferences.renderer_font_size,
            "interface_font_size" : self.user_preferences.interface_font_size,
            "show_open_pulse_logo" : self.user_preferences.show_open_pulse_logo,
            "show_reference_scale_bar" : self.user_preferences.show_reference_scale_bar
        }

        self.write_data_in_file(data)

    def add_recent_file(self, recent_file: str):
        data = self.get_config_data()

        recents_files = self.get_recents_files()
        recents_files.append(recent_file)

        data["recents_files"] = list()
        for file in recents_files:
            if file not in data["recents_files"]:
                data["recents_files"].append(file)
            else:
                data["recents_files"].remove(file)
                data["recents_files"].insert(0, file)
        self.write_data_in_file(data)
        
    def get_recents_files(self) -> list[str]:
        data = self.get_config_data()

        recents_files = list()
        if "recents_files" not in data.keys():
            return recents_files
        
        for file in data["recents_files"]:
            recents_files.append(file)
        
        return recents_files
    
    def get_most_recent_project(self) -> str:
        data = self.get_config_data()
        return data["recents_files"][0]
    
    def get_config_data(self) -> dict:
        with open(self.config_path, "r") as file:
            return json.load(file)
    
    def write_data_in_file(self, data: dict):
        with open(self.config_path, "w") as file:
            json.dump(data, file, indent=2)
