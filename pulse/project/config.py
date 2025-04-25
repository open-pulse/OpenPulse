from pathlib import Path
import json

from pulse.interface.user_preferences import UserPreferences
from molde.colors import Color

class Config:
    
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
                self.user_preferences.show_open_pulse_logo = user_preferences["show_open_pulse_logo"]
                self.user_preferences.show_reference_scale_bar = user_preferences["show_reference_scale_bar"]
                self.user_preferences.compatibility_mode = user_preferences["compatibility_mode"]
                self.user_preferences.color_map = user_preferences["color_map"]

        except:
            self._write_config_file()
    
    def _write_config_file(self):
        data = { 
        "interface_theme" : self.user_preferences.interface_theme,
        "renderer_background_color_1" : self.user_preferences.renderer_background_color_1.to_rgb(),
        "renderer_background_color_2" : self.user_preferences.renderer_background_color_2.to_rgb(),
        "nodes_points_color" : self.user_preferences.nodes_points_color.to_rgb(),
        "lines_color" : self.user_preferences.lines_color.to_rgb(),
        "tubes_color" : self.user_preferences.tubes_color.to_rgb(),
        "renderer_font_color" : self.user_preferences.renderer_font_color.to_rgb(),
        "renderer_font_size" : self.user_preferences.renderer_font_size,
        "show_open_pulse_logo" : self.user_preferences.show_open_pulse_logo,
        "show_reference_scale_bar" : self.user_preferences.show_reference_scale_bar,
        "compatibility_mode" : self.user_preferences.compatibility_mode,
        "color_map" : self.user_preferences.color_map
        }
        
        self.write_data_in_file(data)

    def update_config_file(self):
        data = self.get_config_data()

        data["interface_theme"] = self.user_preferences.interface_theme
        data["renderer_background_color_1"] = self.user_preferences.renderer_background_color_1.to_rgb()
        data["renderer_background_color_2"] = self.user_preferences.renderer_background_color_2.to_rgb()
        data["nodes_points_color"] = self.user_preferences.nodes_points_color.to_rgb()
        data["lines_color"] = self.user_preferences.lines_color.to_rgb()
        data["tubes_color"] = self.user_preferences.tubes_color.to_rgb()
        data["renderer_font_color"] = self.user_preferences.renderer_font_color.to_rgb()
        data["renderer_font_size"] = self.user_preferences.renderer_font_size
        data["show_open_pulse_logo"] = self.user_preferences.show_open_pulse_logo
        data["show_reference_scale_bar"] = self.user_preferences.show_reference_scale_bar
        data["compatibility_mode"] = self.user_preferences.compatibility_mode
        data["color_map"] = self.user_preferences.color_map

        self.write_data_in_file(data)

    def add_recent_file(self, recent_file: str | Path):
        recent_file = Path(recent_file)

        recent_files = self.get_recent_files()
        if (len(recent_files) == 5) and (recent_file not in recent_files):
            recent_files.pop()

        if recent_file in recent_files:
            recent_files.remove(recent_file)

        recent_files = [str(file) for file in recent_files]
        recent_files.insert(0, str(recent_file))

        data = self.get_config_data()
        data["recent_files"] = recent_files

        self.write_data_in_file(data)
        
    def get_recent_files(self) -> list[Path]:
        data = self.get_config_data()

        recent_files = list()
        if "recent_files" not in data.keys():
            return recent_files
        
        for file in data["recent_files"]:
            recent_files.append(Path(file))
        
        return recent_files

    def remove_path_from_config_file(self, path: str | Path):
        data = self.get_config_data()
        data["recent_files"].remove(str(path))

        self.write_data_in_file(data)
        
    def reset_recent_projects(self):
        data = self.get_config_data()
        data["recent_files"] = list()

        self.write_data_in_file(data)

    def write_last_folder_path_in_file(self, label: str, file_path: str):
        data = self.get_config_data()
        path = str(Path(file_path).parent)

        key = f"last_{label}"
        if "last_paths" in data.keys():
            data["last_paths"][key] = path
        else:
            data["last_paths"] = {key : path}
        
        self.write_data_in_file(data)
        
    def get_last_folder_for(self, label: str) -> str | None:
        data = self.get_config_data()

        if "last_paths" in data.keys():
            key = f"last_{label}"
            return data["last_paths"].get(key)
        
        return None
    
    def write_refprop_path_in_file(self, path: str):
        data = self.get_config_data()
        data["refprop_path"] = path

        self.write_data_in_file(data)

    def get_refprop_path_from_file(self) -> str | None:
        data = self.get_config_data()

        if "refprop_path" in data.keys():
            return data["refprop_path"]
    
        return None

    def get_config_data(self) -> dict:
        with open(self.config_path, "r") as file:
            return json.load(file)
    
    def write_data_in_file(self, data: dict):
        with open(self.config_path, "w") as file:
            json.dump(data, file, indent=2)
