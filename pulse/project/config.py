from pathlib import Path
from dataclasses import fields
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

        except:
            self.update_config_file()
            return
    
        for field in fields(UserPreferences):
            read_value = user_preferences.get(field.name)

            if read_value is None:
                continue

            if field.type is Color:
                read_value = Color(*read_value)

            setattr(self.user_preferences, field.name, read_value)

    def update_config_file(self):
        data = self.get_config_data()

        user_preferences_attr = self.user_preferences.get_attributes()
        for attr, value in user_preferences_attr.items():
            if isinstance(value, Color):
                value = value.to_rgb()
            
            data[attr] = value

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
