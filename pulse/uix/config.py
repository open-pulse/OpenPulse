import sys
import configparser

class Config:
    def __init__(self):
        self.reset()

    def reset(self):
        self.recentProjects = {}
        self.openLastProject = False
        self.configFileName = ".config"
        self.loadConfigFile()
        self.LoadArgs()
    
    def loadConfigFile(self):
        config = configparser.ConfigParser()
        config.read(self.configFileName)
        if config.has_section('project'):
            for k, v in config.items('project'):
                self.recentProjects[k] = v

    def writeRecentProject(self, projectName, projectDir):
        projectName = projectName.lower()
        projectSectionName = 'project'
        config = configparser.ConfigParser()
        config.read(self.configFileName)
        if config.has_section(projectSectionName):
            count = len(config.items(projectSectionName)) - 10
            for pName, _ in config.items(projectSectionName):
                if count < 0:
                    break
                else:
                    config.remove_option(projectSectionName, pName)
                    self.recentProjects.pop(pName)
                    count -= 1
            config[projectSectionName][projectName] = projectDir
        else:
            config[projectSectionName] = {projectName: projectDir}

        self.recentProjects[projectName] = projectDir

        with open(self.configFileName, 'w') as configfile:
            config.write(configfile)

    def LoadArgs(self):
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