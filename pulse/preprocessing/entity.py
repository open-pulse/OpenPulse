class Entity:
    def __init__(self, tag):
        self.tag = tag
        self.nodes = []
        self.elements = []

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