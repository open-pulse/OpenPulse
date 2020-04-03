from pulse.preprocessing.mesh import Mesh
from pulse.processing.assembly import get_global_matrices
from pulse.preprocessing.entity import Entity
import configparser

class Project:
    def __init__(self):
        self.mesh = Mesh()
        self.path = ""
        self.projectName = ""
        self.materialPath = ""
        self.importPath = ""
        self.elementSize = 0

        self.K = self.M = self.Kr = self.Mr = None

        self.projectReady = False #True if the project was created or loaded
        self.projectAssembly = False #True if the project was assembled

    def newProject(self, path, project_name, geometry_name, element_size, material_name):
        self.mesh = Mesh()
        self.path = path
        self.importPath = "{}//{}".format(path, geometry_name)
        self.materialPath = "{}//{}".format(path, material_name)
        self.projectName = project_name
        self.elementSize = float(element_size)
        self.projectReady = True
        self.mesh.generate(self.importPath, self.elementSize)

    def openProject(self, path):
        folder_path = path.split('/')[-3:-1] #Get folder path
        folder_path = "{}//{}".format(folder_path[0], folder_path[1])
        config = configparser.ConfigParser()
        config.read(path)
        name = config['PROJECT']['name']
        geometry_name = config['PROJECT']['geometryfile']
        element_size = config['PROJECT']['elementsize']
        material_name = config['PROJECT']['materialfile']
        
        self.path = folder_path
        self.projectName = name
        self.importPath = "{}//{}".format(folder_path, geometry_name)
        self.materialPath = "{}//{}".format(folder_path, material_name)
        self.elementSize = float(element_size)
        self.projectReady = True
        self.mesh = Mesh()
        self.mesh.generate(self.importPath, self.elementSize)

    def getNodes(self):
        return self.mesh.nodes

    def getElements(self):
        return self.mesh.elements

    def getEntities(self):
        return self.mesh.entities

    def setMaterial_by_Entity(self, entity_id, material):
        self.mesh.set_material_by_line(entity_id, material)
        self._setEntityMaterial(entity_id, material)

    def setCrossSection_by_Entity(self, entity_id, cross_section):
        self.mesh.set_cross_section_by_line(entity_id, cross_section)
        self._setEntityCross(entity_id, cross_section)

    def setMaterial(self, material):
        self.mesh.set_material_by_element('all', material)
        self._setAllEntityMaterial(material)

    def setCrossSection(self, cross_section):
        self.mesh.set_cross_section_by_element('all', cross_section)
        self._setAllEntityCross(cross_section)

    def setBondaryCondition_by_Node(self, node_id, bc):
        self.mesh.set_boundary_condition_by_node(node_id, bc)

    def isReady(self):
        return self.projectReady

    def getGlobalMatrices(self):
        self.projectAssembly = True
        self.K, self.M, self.Kr, self.Mr = get_global_matrices(self.mesh)
        print(self.K)
        print(self.M)
        print(self.Kr)
        print(self.Mr)

    def _setEntityMaterial(self, entity_id, material):
        for entity in self.mesh.entities:
            if entity.tag == entity_id:
                entity.material = material
                return

    def _setEntityCross(self, entity_id, cross):
        for entity in self.mesh.entities:
            if entity.tag == entity_id:
                entity.cross = cross
                return

    def _setAllEntityMaterial(self, material):
        for entity in self.mesh.entities:
            entity.material = material

    def _setAllEntityCross(self, cross):
        for entity in self.mesh.entities:
            entity.cross = cross