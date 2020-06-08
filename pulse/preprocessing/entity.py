# from pulse.preprocessing.material import Material

class Entity:
    def __init__(self, tag):
        self.tag = tag
        self.nodes = []
        self.elements = []
        self.material = None
        self.fluid = None
        self.crossSection = None
        self.element_type = None

    def insertNode(self, node):
        self.nodes.append(node)

    def insertEdge(self, edge):
        self.elements.append(edge)
        
    def get_nodes(self):
        return self.nodes

    def get_elements(self):
        return self.elements

    def getTag(self):
        return self.tag

    def getColor(self):
        if self.material is None:
            return [255,255,255]
        return self.material.getColorRGB()

    def getNormalizedColor(self):
        if self.material is None:
            return [1,1,1]
        return self.material.getNormalizedColorRGB()

    def getCrossSection(self):
        return self.crossSection
    
    def getElementType(self):
        return self.element_type

    def getMaterial(self):
        return self.material
        
    def getFluid(self):
        return self.fluid
