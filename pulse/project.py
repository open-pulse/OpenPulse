from pulse.preprocessing.mesh import Mesh
from pulse.processing.assembly import get_global_matrices

class Project:
    def __init__(self):
        self.mesh = Mesh()
        self.projectName = ""
        self.importPath = ""
        self.elementSize = 0

        self.K = self.M = self.Kr = self.Mr = None

        self.projectReady = False #True if the project was created or loaded
        self.projectAssembly = False #True if the project was assembled

    def newProject(self, project_name, import_path, element_size):
        self.mesh = Mesh()
        self.importPath = import_path
        self.projectName = project_name
        self.elementSize = element_size
        self.projectReady = True
        self.mesh.generate(self.importPath, self.elementSize)

    def getNodes(self):
        return self.mesh.nodes

    def getElements(self):
        return self.mesh.elements

    def getEntities(self):
        return self.mesh.entities

    def setMaterial_by_Entity(self, entity_id, material):
        self.mesh.set_material_by_line(entity_id, material)

    def setMaterial(self, material):
        self.mesh.set_material_by_element('all', material)

    def setCrossSection(self, cross_section):
        self.mesh.set_cross_section_by_element('all', cross_section)

    def isReady(self):
        return self.projectReady

    def getGlobalMatrices(self):
        self.projectAssembly = True
        self.K, self.M, self.Kr, self.Mr = get_global_matrices(self.mesh)