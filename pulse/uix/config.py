import os
import sys
import configparser

class Config:
    def __init__(self):
        self.reset()

    def reset(self):
        self.recentProjects = {}
        self.openLastProject = False
        self.configFileName = ".config"
        self.load_config_file()
        self.load_args()
    
    def load_config_file(self):
        config = configparser.ConfigParser()
        config.read(self.configFileName)
        if config.has_section('project'):
            for k, v in config.items('project'):
                self.recentProjects[k] = v

    def write_recent_project(self, project_path):
        
        project_name = os.path.basename(os.path.dirname(project_path))
        project_name = project_name.lower()
   
        section_name = 'project'
        config = configparser.ConfigParser()
        config.read(self.configFileName)

        if config.has_section(section_name):
            count = len(config.items(section_name)) - 10
            for pName, _ in config.items(section_name):
                if count < 0:
                    break
                else:
                    config.remove_option(section_name, pName)
                    self.recentProjects.pop(pName)
                    count -= 1
            config[section_name][project_name] = str(project_path)
        else:
            config[section_name] = {project_name: str(project_path)}

        self.recentProjects[project_name] = str(project_path)

        with open(self.configFileName, 'w') as configfile:
            config.write(configfile)

    def remove_path_from_config_file(self, dir_identifier):
        config = configparser.ConfigParser()
        config.read(self.configFileName)
        if config.has_section('project'):
            config.remove_option(section='project', option=dir_identifier)
        with open(self.configFileName, 'w') as configfile:
            config.write(configfile)
        self.reset()

    def load_args(self):
        if "--last" in sys.argv:
            self.openLastProject = True

    def resetRecentProjectList(self):
        config = configparser.ConfigParser()
        config.read(self.configFileName)   
        
        if config.has_section('project'):
            config.remove_section(section='project')
        
        with open(self.configFileName, 'w') as configfile:
            config.write(configfile)
        
        self.reset()

    def getMostRecentProjectDir(self):
        return self.recentProjects[list(self.recentProjects.keys())[-1]]

    def getRecentProjectByID(self, id_):
        return self.recentProjects[list(self.recentProjects.keys())[id_]]

    def haveRecentProjects(self):
        return self.recentProjectsSize() > 0

    def recentProjectsSize(self):
        return len(self.recentProjects)