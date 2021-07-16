import vtk
import numpy as np

class ColorTable(vtk.vtkLookupTable):
    def __init__(self, project, data, stress_field_plot=False, pressure_field_plot=False):
        super().__init__()

        self.project = project

        if isinstance(data, dict):
            self.valueVector = list(data.values())
            self.dictData = data
        else:
            self.valueVector = data

        self.stress_field_plot = stress_field_plot
        self.pressure_field_plot = pressure_field_plot

        self.structural_elements = project.preprocessor.structural_elements

        self.min_value = min(self.valueVector)
        self.max_value = max(self.valueVector)
                
        self.SetTableRange(self.min_value,self.max_value)
        self.SetHueRange( 2/3, 0 )
        self.ForceBuild()

    def is_empty(self):
        return len(self.valueVector) == 0

    def distance_to(self, cord1, cord2):
        return np.linalg.norm(cord1 - cord2)

    def get_color(self, element):

        key1 = element.first_node.global_index
        key2 = element.last_node.global_index

        if self.is_empty():
            return [255,255,255]

        color_temp = [0,0,0]
        if self.stress_field_plot and element.element_type == 'expansion_joint':
            return [255,255,255]
        elif (self.stress_field_plot or self.pressure_field_plot) and element.element_type == 'beam_1':
            return [255,255,255]
        elif self.pressure_field_plot:
            value = (self.valueVector[key1] + self.valueVector[key2])/2
        elif self.stress_field_plot:
            value = np.real(self.dictData[element.index])
        else:
            value = (self.valueVector[key1] + self.valueVector[key2])/2
        
        self.GetColor(value, color_temp)
        color_temp = [  int(color_temp[0]*255), int(color_temp[1]*255), int(color_temp[2]*255)  ]
                
        return color_temp
        
