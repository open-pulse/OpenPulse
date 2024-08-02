import vtk
import numpy as np
from pulse.interface.viewer_3d.coloring.color_palettes import (
    grey_colors, jet_colors, 
    viridis_colors, inferno_colors, magma_colors, plasma_colors,
    bwr_colors, PiYG_colors, PRGn_colors, BrBG_colors, PuOR_colors,
)

class ColorTable(vtk.vtkLookupTable):
    def __init__(self, project, data, min_max_values, colormap, stress_field_plot=False, pressure_field_plot=False):
        super().__init__()

        self.project = project

        self.colormap = colormap

        if isinstance(data, dict):
            self.valueVector = list(data.values())
            self.dictData = data
        else:
            self.valueVector = data

        [self.min_value, self.max_value] = min_max_values

        self.stress_field_plot = stress_field_plot
        self.pressure_field_plot = pressure_field_plot

        self.structural_elements = project.preprocessor.structural_elements

        self.SetTableRange(self.min_value, self.max_value)
        self.set_colormap(self.colormap)

    def set_colormap(self, colormap:str):
        # just to make sure it has no uppercases or extra spaces
        colormap = colormap.strip().lower()

        if colormap == "grayscale":
            self.set_colors(grey_colors)
        elif colormap == "jet":
            self.set_colors(jet_colors)
        elif colormap == "viridis":
            self.set_colors(viridis_colors)
        elif colormap == "inferno":
            self.set_colors(inferno_colors)
        elif colormap == "magma":
            self.set_colors(magma_colors)
        elif colormap == "plasma":
            self.set_colors(plasma_colors)
        elif colormap == "bwr":
            self.set_colors(bwr_colors)
        elif colormap == "piyg":
            self.set_colors(PiYG_colors)
        elif colormap == "prgn":
            self.set_colors(PRGn_colors)            
        elif colormap == "brbg":
            self.set_colors(BrBG_colors)
        elif colormap == "puor":
            self.set_colors(PuOR_colors)
        else:
            print(f'Invalid colormap "{colormap}". Using "viridis" instead.')
            self.set_colors(viridis_colors)

        diverging_colormaps = ["bwr", "piyg", "prgn", "brbg", "puor"]
        if colormap in diverging_colormaps:
            # Center values on Zeros
            max_abs = max(abs(self.min_value), abs(self.max_value))
            self.SetTableRange(-max_abs, max_abs)
        else:
            self.SetTableRange(self.min_value, self.max_value)

    def set_colors(self, colors, shades=256):
        color_transfer = vtk.vtkColorTransferFunction()
        for i, color in enumerate(colors):
            color_transfer.AddRGBPoint(i/(len(colors) - 1), *color)

        self.SetNumberOfColors(shades)
        for i in range(shades):
            interpolated_color = color_transfer.GetColor(i / (shades - 1))
            normalized_color = [i/255 for i in interpolated_color]
            self.SetTableValue(i, *normalized_color)
        self.Build()

    def is_empty(self):
        return len(self.valueVector) == 0

    def distance_to(self, cord1, cord2):
        return np.linalg.norm(cord1 - cord2)
    
    def get_node_color(self, node):
        if self.is_empty():
            return [255, 255, 255]
        
        value = self.valueVector[node.global_index]
        color_temp = [255, 255, 255]
        self.GetColor(value, color_temp)
        color_temp = [int(i * 255) for i in color_temp]
        return

    def get_element_color(self, element):
        key1 = element.first_node.global_index
        key2 = element.last_node.global_index

        if self.is_empty():
            return [255, 255, 255]

        color_temp = [0,0,0]
        
        if self.stress_field_plot and element.element_type in ['beam_1', 'expansion_joint', 'valve']:
            return [255,255,255]
        elif self.pressure_field_plot and element.element_type == 'beam_1':
            return [255, 255, 255]
        elif self.pressure_field_plot:
            value = (self.valueVector[key1] + self.valueVector[key2])/2
        elif self.stress_field_plot:
            value = np.real(self.dictData[element.index])
        else:
            value = (self.valueVector[key1] + self.valueVector[key2])/2
        
        self.GetColor(value, color_temp)
        color_temp = [int(i * 255) for i in color_temp]
        return color_temp
