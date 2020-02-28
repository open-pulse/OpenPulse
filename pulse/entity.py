class Entity:
    def __init__(self, tag):
        self.tag = tag
        self.nodes = []
        self.edges = []

    def insertNode(self, node):
        self.nodes.append(node)

    def insertEdge(self, edge):
        self.edges.append(edge)

    def print_(self):
        print("=======================")
        print("TAG "+str(self.tag))
        print("NODES:")
        for i in self.nodes:
            print(i)
        print("EDGES:")
        for i in self.edges:
            print(i)
        