import vtk
import numpy as np

class ColorTable(vtk.vtkLookupTable):
    def __init__(self):
        super().__init__()
        self.structure = None
        self.normal = {}
        self.min_value = 0
        self.max_value = 0
        
        

        try:
            if self.structure is not None:
                for id_, value in self.structure.nodes.items():
                    calc = (value.x**2 + value.y**2 + value.z**2)**(1/2)
                    self.normal[id_] = calc

                self.max_value = max(self.normal.values())
                
                for index, value in self.normal.items():
                    self.normal[index] = self.normal[index]*0.4/self.max_value

                self.min_value = min(self.normal.values())
                self.max_value = max(self.normal.values())
        except:
            pass
        
        self.SetTableRange(self.min_value,self.max_value)
        self.SetHueRange(self.max_value*2, self.max_value)
        self.ForceBuild()

    def is_empty(self):
        return len(self.normal) == 0

    def get_color_by_id(self, _id):
        if self.is_empty():
            return
        
        color_temp = [0,0,0]
        self.GetColor(self.normal[_id], color_temp)
        
        for i in range(3):
            color_temp[i] = int(color_temp[i]*255)
        
        #color_temp[0], color_temp[2] = color_temp[2], color_temp[0]

        return color_temp
