import vtk
import numpy as np

class ColorTable(vtk.vtkLookupTable):
    def __init__(self, project, matriz):
        super().__init__()
        self.project = project
        self.matriz = matriz
        self.meshNodes = self.project.getNodes()
        self.normal = {}
        self.min_value = 0
        self.max_value = 0
        try:
            for i in range(len(matriz)):
                node1 = self.matriz[i]
                node_id = node1[0]
                nodex = node1[1]
                nodey = node1[2]
                nodez = node1[3]
                cord1 = np.array([nodex, nodey, nodez])
                node2 = self.meshNodes[node_id]
                cord2 = node2.coordinates
                dist = self.distance_to(cord1, cord2)
                self.normal[node_id] = dist


            # for key, node in self.project.getNodesColor().items():
            #     calc = (node.x**2 + node.y**2 + node.z**2)**(1/2)
            #     self.normal[key] = calc

            self.max_value = max(self.normal.values())
            for index, value in self.normal.items():
                self.normal[index] = self.normal[index]/self.max_value

            self.min_value = min(self.normal.values())
            self.max_value = max(self.normal.values())
        except Exception as e:
            print("{}".format(e))
        
        self.SetTableRange(self.min_value,self.max_value)
        self.SetHueRange(self.min_value*2, self.max_value)
        self.ForceBuild()

    def is_empty(self):
        return len(self.normal) == 0

    def distance_to(self, cord1, cord2):
        return np.linalg.norm(cord1 - cord2)

    def get_color_by_id(self, key):
        if self.is_empty():
            return [255,255,255]
        
        color_temp = [0,0,0]
        self.GetColor(self.normal[key], color_temp)
        
        for i in range(3):
            color_temp[i] = int(color_temp[i]*255)
        
        #color_temp[0], color_temp[2] = color_temp[2], color_temp[0]

        return color_temp
