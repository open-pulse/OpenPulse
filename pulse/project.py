from pulse.mesh import Mesh

class Project:
    def __init__(self):
        self.mesh = Mesh()

    def newProject(self, import_path):
        self.mesh = Mesh()
        self.mesh.path = import_path
        self.mesh.generate(1,1)

    def getEntities(self):
        return self.mesh.entities

    def getNodes(self):
        return self.mesh.nodes

    def getElements(self):
        return self.mesh.edges