class Entity:
    def __init__(self, tag):
        self.tag = tag
        self.nodes = []
        self.elements = []
        self.material = None
        self.cross = None

    def insertNode(self, node):
        self.nodes.append(node)

    def insertEdge(self, edge):
        self.elements.append(edge)
        
    def getNodes(self):
        return self.nodes

    def getElements(self):
        return self.elements

    def getTag(self):
        return self.tag

    def getColor(self):
        if self.material is None:
            return [255,255,255]
        return self.material.getColorRGB()