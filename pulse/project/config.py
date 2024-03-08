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

    def write_recent_project(self, project_path):
        
        project_name = os.path.basename(os.path.dirname(project_path))
        project_name = project_name.lower()
   
        section_name = 'project'
        config = configparser.ConfigParser()
        config.read(self.recents_filename)

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

        with open(self.recents_filename, 'w') as configfile:
            config.write(configfile)

    def remove_path_from_config_file(self, dir_identifier):
        config = configparser.ConfigParser()
        config.read(self.recents_filename)
        if config.has_section('project'):
            config.remove_option(section='project', option=dir_identifier)
        with open(self.recents_filename, 'w') as configfile:
            config.write(configfile)
        self.reset()

    def load_args(self):
        if "--last" in sys.argv:
            self.open_last_project = True

    def resetRecentProjectList(self):
        config = configparser.ConfigParser()
        config.read(self.recents_filename)   
        
        if config.has_section('project'):
            config.remove_section(section='project')
        
        with open(self.recents_filename, 'w') as configfile:
            config.write(configfile)
        
        self.reset()

    def getMostRecentProjectDir(self):
        return self.recent_projects[list(self.recent_projects.keys())[-1]]

    def getRecentProjectByID(self, id_):
        return self.recent_projects[list(self.recent_projects.keys())[id_]]

    def haveRecentProjects(self):
        return self.recent_projectsSize() > 0

    def recentProjectsSize(self):
        return len(self.recent_projects)