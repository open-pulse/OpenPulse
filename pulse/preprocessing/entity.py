# from pulse.preprocessing.material import Material

class Entity:
    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.nodes = []
        self.elements = []
        self.material = None
        self.fluid = None
        self.crossSection = None
        self.element_type = None
        self.additional_section_info = None
        self.capped_end = None
        self.length_correction = None
        self.internal_pressure = kwargs.get('internal_pressure', None)
        self.external_pressure = kwargs.get('external_pressure', None)
        self.internal_temperature = kwargs.get('internal_temperature', None)
        self.external_temperature = kwargs.get('external_temperature', None)

    def insertNode(self, node):
        self.nodes.append(node)

    def insertEdge(self, edge):
        self.elements.append(edge)
        
    def get_nodes(self):
        return self.nodes

    def get_elements(self):
        return self.elements

    def get_tag(self):
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
    
    def getcappedEnd(self):
        return self.capped_end
