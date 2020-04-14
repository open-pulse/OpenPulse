import vtk
import numpy as np

class ColorTable(vtk.vtkLookupTable):
    def __init__(self, project, r_def):
        super().__init__()
        self.project = project
        self.r_def = r_def
        # self.matriz = matriz
        # self.normal = {}
        self.min_value = min(self.r_def)
        self.max_value = max(self.r_def)
        # try:
        #     for i in range(len(matriz)):
        #         node1 = self.matriz[i]
        #         node_id = node1[0]
        #         nodex = node1[1]
        #         nodey = node1[2]
        #         nodez = node1[3]
        #         calc = (nodex**2 + nodey**2 + nodez**2)**(1/2)
        #         self.normal[node_id] = calc

        #     # self.max_value = max(self.normal.values())
        #     # for index, value in self.normal.items():
        #     #     self.normal[index] = self.normal[index]/self.max_value

        #     self.min_value = min(self.normal.values())
        #     self.max_value = max(self.normal.values())
        # except Exception as e:
        #     print("{}".format(e))
        
        self.SetTableRange(self.min_value,self.max_value)
        self.SetHueRange( 2/3, 0 )
        #self.SetHueRange(self.min_value, self.max_value/1.5)
        self.ForceBuild()

    def is_empty(self):
        return len(self.r_def) == 0

    def distance_to(self, cord1, cord2):
        return np.linalg.norm(cord1 - cord2)

    def get_color_by_id(self, key):
        if self.is_empty():
            return [255,255,255]
        
        color_temp = [0,0,0]
        self.GetColor(self.r_def[key], color_temp)
        
        for i in range(3):
            color_temp[i] = int(color_temp[i]*255)
        
        #color_temp[0], color_temp[2] = color_temp[2], color_temp[0]
        return color_temp
