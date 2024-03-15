from pulse.tools.utils import get_new_path

import os
import sys
import configparser
from pathlib import Path

class Config:
    def __init__(self):
        self.reset()

    def reset(self):
        self.recent_projects = dict()
        self.open_last_project = False
        self.recents_filename = Path().home() / ".open_pulse_config"
        self.load_config_file()
        self.load_args()

    def load_config_file(self):
        try:
            config = configparser.ConfigParser()
            config.read(self.recents_filename)
            if config.has_section('project'):
                for key, value in config.items('project'):
                    self.recent_projects[key] = value
        except:
            if self.recents_filename.exists():
                os.remove(self.recents_filename)

    def remove_path_from_config_file(self, dir_identifier):
        config = configparser.ConfigParser()
        config.read(self.recents_filename)

        if config.has_section('project'):
            config.remove_option(section='project', option=dir_identifier)

        self.write_data_in_file(self.recents_filename, config) 
        self.reset()

    def load_args(self):
        if "--last" in sys.argv:
            self.open_last_project = True

    def resetRecentProjectList(self):
        config = configparser.ConfigParser()
        config.read(self.recents_filename)   
        
        if config.has_section('project'):
            config.remove_section(section='project')
        
        self.write_data_in_file(self.recents_filename, config)        
        self.reset()

    def getMostRecentProjectDir(self):
        return self.recent_projects[list(self.recent_projects.keys())[-1]]

    def getRecentProjectByID(self, id_):
        return self.recent_projects[list(self.recent_projects.keys())[id_]]

    def haveRecentProjects(self):
        return self.recent_projectsSize() > 0

    def recentProjectsSize(self):
        return len(self.recent_projects)
    
    def get_last_project_folder(self):

        config = configparser.ConfigParser()
        config.read(self.recents_filename)

        if config.has_section("User preferences"):
            section = config["User preferences"]
            if "last project folder" in section.keys():
                return section["last project folder"]
        return None

    def get_last_geometry_folder(self):

        config = configparser.ConfigParser()
        config.read(self.recents_filename)

        if config.has_section("User preferences"):
            section = config["User preferences"]
            if "last geometry folder" in section.keys():
                return section["last geometry folder"]
        return None

    def write_recent_project(self, project_path):

        project_name = os.path.basename(os.path.dirname(project_path))
        project_name = project_name.lower()
   
        config = configparser.ConfigParser()
        config.read(self.recents_filename)

        local_path = os.path.dirname(os.path.dirname(project_path)) 
        if config.has_section('User preferences'):
                config["User preferences"]["last project folder"] = local_path
        else:
            config["User preferences"] = {"last project folder" : local_path}

        section_name = "project"
        if config.has_section(section_name):
            count = len(config.items(section_name)) - 10
            for pName, _ in config.items(section_name):
                if count < 0:
                    break
                else:
                    config.remove_option(section_name, pName)
                    self.recent_projects.pop(pName)
                    count -= 1
            config[section_name][project_name] = str(project_path)
        else:
            config[section_name] = {project_name: str(project_path)}

        self.recent_projects[project_name] = str(project_path)
        self.write_data_in_file(self.recents_filename, config) 

    def write_theme_in_file(self, theme : str):
        try:

            config = configparser.ConfigParser()
            config.read(self.recents_filename)

            if config.has_section('User preferences'):
                config["User preferences"]["interface theme"] = theme
                config["User preferences"]["background color"] = theme
            else:
                config["User preferences"] = {"interface theme" : theme,
                                              "background color" : theme}

        except:
            return

        self.write_data_in_file(self.recents_filename, config) 

    def write_last_geometry_folder_path_in_file(self, geometry_path : str):
        try:

            _path = os.path.dirname(geometry_path)
            config = configparser.ConfigParser()
            config.read(self.recents_filename)

            if config.has_section('User preferences'):
                config["User preferences"]["last geometry folder"] = _path
            else:
                config["User preferences"] = {"last geometry folder" : _path}

        except:
            return

        self.write_data_in_file(self.recents_filename, config) 

    def write_colormap_in_file(self, colormap : str):
        try:

            config = configparser.ConfigParser()
            config.read(self.recents_filename)

            if config.has_section('User preferences'):
                config["User preferences"]["colormap"] = colormap
            else:
                config["User preferences"] = {"colormap" : colormap}

        except:
            return

        self.write_data_in_file(self.recents_filename, config)

    def write_user_preferences_in_file(self, preferences):

        config = configparser.ConfigParser()
        config.read(self.recents_filename)

        config['User preferences'] = preferences
        
        self.write_data_in_file(self.recents_filename, config)

    def get_user_preferences(self):

        config = configparser.ConfigParser()
        config.read(self.recents_filename)

        user_preferences = dict()
        if config.has_section("User preferences"):
            
            section = config["User preferences"]

            try:

                if "last project folder" in section.keys():
                    user_preferences["last project folder"] = section["last project folder"]

                if "last geometry folder" in section.keys():
                    user_preferences["last geometry folder"] = section["last geometry folder"]

                if "interface theme" in section.keys():
                    user_preferences["interface theme"] = section["interface theme"]

                if "background color" in section.keys():
                    if section["background color"] in ["light", "dark"]:
                        user_preferences["background color"] = section["background color"]
                    else:
                        background_color = section["background color"][1:-1].split(",")
                        user_preferences["background color"] = tuple([float(val) for val in background_color])

                if "bottom font color" in section.keys():
                    font_color = section["bottom font color"][1:-1].split(",")
                    user_preferences["bottom font color"] = tuple([float(val) for val in font_color])

                if "nodes color" in section.keys():
                    nodes_color = section["nodes color"][1:-1].split(",")
                    user_preferences["nodes color"] = tuple([float(val) for val in nodes_color])

                if "lines color" in section.keys():
                    lines_color = section["lines color"][1:-1].split(",")
                    user_preferences["lines color"] = tuple([float(val) for val in lines_color])

                if "surfaces color" in section.keys():
                    surfaces_color = section["surfaces color"][1:-1].split(",")
                    user_preferences["surfaces color"] = tuple([float(val) for val in surfaces_color])

                if "transparency" in section.keys():
                    user_preferences["transparency"] = float(section["transparency"])

                if "openpulse logo" in section.keys():
                    user_preferences["openpulse logo"] = bool(int(section["openpulse logo"]))

                if "colormap" in section.keys():
                    user_preferences["colormap"] = section["colormap"]

                if "Reference scale" in section.keys():
                    user_preferences["Reference scale"] = bool(int(section["Reference scale"]))

            except:
                pass

        return user_preferences

    def write_data_in_file(self, path, config):
        with open(path, 'w') as config_file:
            config.write(config_file)