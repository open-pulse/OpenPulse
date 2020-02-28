from pulse.mesh import Mesh

class Project:
    def __init__(self):
        self.mesh = Mesh()

    def newProject(self, import_path):
        self.mesh.path = import_path
        self.mesh.generate(1,1)