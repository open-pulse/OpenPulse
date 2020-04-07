from pulse.preprocessing.mesh import Mesh
from pulse.processing.assembly import get_global_matrices
from pulse.preprocessing.entity import Entity
from pulse.preprocessing.material import Material
from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.boundary_condition import BoundaryCondition
import configparser

class Project:
    def __init__(self):
        self.mesh = Mesh()
        self.path = ""
        self.projectName = ""
        self.materialListPath = ""
        self.geometryPath = ""
        self.elementSize = 0
        self.entityPath = ""
        self.nodePath = ""

        self.K = self.M = self.Kr = self.Mr = None

        self.projectReady = False #True if the project was created or loaded
        self.projectAssembly = False #True if the project was assembled

    def newProject(self, path, project_name, geometry_name, element_size, material_name):
        self.mesh = Mesh()
        self.path = path
        self.geometryPath = "{}//{}".format(path, geometry_name)
        self.materialListPath = "{}//{}".format(path, material_name)
        self.entityPath = "{}//{}".format(path, 'entity.dat')
        self.nodePath = "{}//{}".format(path, 'node.dat')
        self.projectName = project_name
        self.elementSize = float(element_size)
        self.projectReady = True
        self.mesh.generate(self.geometryPath, self.elementSize)
        self.createEntityFile()

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
        self.geometryPath = "{}//{}".format(folder_path, geometry_name)
        self.materialListPath = "{}//{}".format(folder_path, material_name)
        self.entityPath = "{}//{}".format(folder_path, 'entity.dat')
        self.nodePath = "{}//{}".format(folder_path, 'node.dat')
        self.elementSize = float(element_size)
        self.projectReady = True
        self.mesh = Mesh()
        self.mesh.generate(self.geometryPath, self.elementSize)
        self.loadEntityFile()
        self.loadNodeFile()

    def getNodes(self):
        return self.mesh.nodes

    def getElements(self):
        return self.mesh.elements

    def getEntities(self):
        return self.mesh.entities

    def getNode(self, node_id):
        return self.mesh.nodes[node_id]

    def getEntity(self, entity_id):
        for entity in self.mesh.entities:
            if entity.getTag() == entity_id:
                return entity

    def loadMaterial_by_Entity(self, entity_id, material):
        self.mesh.set_material_by_line(entity_id, material)
        self._setEntityMaterial(entity_id, material)

    def loadCrossSection_by_Entity(self, entity_id, cross_section):
        self.mesh.set_cross_section_by_line(entity_id, cross_section)
        self._setEntityCross(entity_id, cross_section)

    def loadBondaryCondition_by_Node(self, node_id, bc):
        self.mesh.set_boundary_condition_by_node(node_id, bc)

    def setMaterial_by_Entity(self, entity_id, material):
        self.mesh.set_material_by_line(entity_id, material)
        self._setEntityMaterial(entity_id, material)
        self.addMaterialInFile(entity_id, material.identifier)

    def setCrossSection_by_Entity(self, entity_id, cross_section):
        self.mesh.set_cross_section_by_line(entity_id, cross_section)
        self._setEntityCross(entity_id, cross_section)
        self.addCrossSectionInFile(entity_id, cross_section)

    def setMaterial(self, material):
        self.mesh.set_material_by_element('all', material)
        self._setAllEntityMaterial(material)
        for entity in self.mesh.entities:
            self.addMaterialInFile(entity.getTag(), material.identifier)

    def setCrossSection(self, cross_section):
        self.mesh.set_cross_section_by_element('all', cross_section)
        self._setAllEntityCross(cross_section)
        for entity in self.mesh.entities:
            self.addCrossSectionInFile(entity.getTag(), cross_section)

    def setBondaryCondition_by_Node(self, node_id, bc):
        self.mesh.set_boundary_condition_by_node(node_id, bc)
        self.addBondaryConditionInFile(node_id, bc)

    def isReady(self):
        return self.projectReady

    def getGlobalMatrices(self):
        self.projectAssembly = True
        self.K, self.M, self.Kr, self.Mr = get_global_matrices(self.mesh)

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

    def createEntityFile(self):
        config = configparser.ConfigParser()
        for entity in self.getEntities():
            config[str(entity.getTag())] = {
                'MaterialID': '',
                'External Diam': '',
                'Internal Diam': ''
            }
        with open(self.entityPath, 'w') as configfile:
            config.write(configfile)

    def addMaterialInFile(self, entity_id, material_id):
        config = configparser.ConfigParser()
        config.read(self.entityPath)
        config[str(entity_id)]['MaterialID'] = str(material_id)
        with open(self.entityPath, 'w') as configfile:
            config.write(configfile)

    def addBondaryConditionInFile(self, nodes_id, bc):
        config = configparser.ConfigParser()
        config.read(self.nodePath)
        for node_id in nodes_id:
            if str(node_id) in config.sections():
                config[str(node_id)]['displacement'] = str(bc.displacement)
                config[str(node_id)]['rotation'] = str(bc.rotation)
            else:
                config[str(node_id)] = {
                    'displacement': str(bc.displacement),
                    'rotation': str(bc.rotation)
                }
        with open(self.nodePath, 'w') as configfile:
            config.write(configfile)

    def addCrossSectionInFile(self, entity_id, cross_section):
        config = configparser.ConfigParser()
        config.read(self.entityPath)
        config[str(entity_id)]['external diam'] = str(cross_section.external_diameter)
        config[str(entity_id)]['internal diam'] = str(cross_section.internal_diameter)
        with open(self.entityPath, 'w') as configfile:
            config.write(configfile)

    def loadEntityFile(self):
        material_list = configparser.ConfigParser()
        material_list.read(self.materialListPath)

        entityFile = configparser.ConfigParser()
        entityFile.read(self.entityPath)

        for entity in entityFile.sections():
            material_id = entityFile[entity]['MaterialID']
            diam_ext = entityFile[entity]['external diam']
            diam_int = entityFile[entity]['internal diam']
            if material_id.isnumeric():
                material_id = int(material_id)
                for material in material_list.sections():
                    if int(material_list[material]['identifier']) == material_id:
                        name = str(material_list[material]['name'])
                        identifier = str(material_list[material]['identifier'])
                        density =  str(material_list[material]['density'])
                        youngmodulus =  str(material_list[material]['youngmodulus'])
                        poisson =  str(material_list[material]['poisson'])
                        color =  str(material_list[material]['color'])
                        temp_material = Material(name, float(density), identifier=identifier, young_modulus=float(youngmodulus), poisson_ratio=float(poisson), color=color)
                        self.loadMaterial_by_Entity(int(entity), temp_material)
            
            if self.isFloat(diam_ext) and self.isFloat(diam_int):
                diam_ext = float(diam_ext)
                diam_int = float(diam_int)
                cross = CrossSection(diam_ext, diam_int)
                self.loadCrossSection_by_Entity(int(entity), cross)

    def loadNodeFile(self):
        node_list = configparser.ConfigParser()
        node_list.read(self.nodePath)
        for node in node_list.sections():
            node_id = int(node)
            displacement = node_list[str(node)]['displacement']
            rotation = node_list[str(node)]['rotation']
            displacement = displacement[1:-1].split(',')
            rotation = rotation[1:-1].split(',')

            dx = dy = dz = rx = ry = rz = None
            if displacement[0].isnumeric():
                dx = int(displacement[0])
            if displacement[1].isnumeric():
                dy = int(displacement[1])
            if displacement[2].isnumeric():
                dz = int(displacement[2])

            if rotation[0].isnumeric():
                rx = int(rotation[0])
            if rotation[1].isnumeric():
                ry = int(rotation[1])
            if rotation[2].isnumeric():
                rz = int(rotation[2])

            bc = BoundaryCondition(dx,dy,dz,rx,ry,rz)
            self.loadBondaryCondition_by_Node(node_id, bc)

    def isFloat(self, number):
        try:
            float(number)
            return True
        except Exception:
            return False

    def getElementSize(self):
        return self.elementSize