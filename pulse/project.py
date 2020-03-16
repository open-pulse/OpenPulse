from pulse.mesh import Mesh

class Project:
    def __init__(self):
        self.mesh = Mesh()
        self.entities = []

        self._flag_generate = False   #Do have generate mash?
        self._flag_elements = False   #
        self._flag_points = False     #
        self._flag_entities = False   #

    def newProject(self, import_path):
        self.mesh = Mesh()
        self.mesh.path = import_path
        self.mesh.generate(1,1)
        self.entities = self.mesh.entities
        self.set_flags_new_project()

    def getEntities(self):
        return self.entities

    def getNodes(self):
        return self.mesh.nodes

    def getElements(self):
        return self.mesh.edges

    def generate(self, min_size, max_size):
        self.set_flags_generate()
        self.mesh.generate(min_size,max_size)

    def set_flags_new_project(self):
        self._flag_generate = False
        self._flag_entities = True
        self._flag_elements = False
        self._flag_points = False

    def set_flags_generate(self):
        self._flag_generate = True
        self._flag_entities = True
        self._flag_elements = True
        self._flag_points = True

        