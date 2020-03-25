class Entity:
    def __init__(self, tag):
        self.tag = tag
        self.nodes = []
        self.edges = []

    def insertNode(self, node):
        self.nodes.append(node)

    def insertEdge(self, edge):
        self.edges.append(edge)
        