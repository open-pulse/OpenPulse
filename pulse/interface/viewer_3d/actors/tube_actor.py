import vtk
from collections import defaultdict
import numpy as np
from enum import Enum

from vtkat.utils import set_polydata_property, set_polydata_colors
from opps.interface.viewer_3d.utils import cross_section_sources 
from pulse.interface.viewer_3d.coloring.color_table import ColorTable


class ColorMode(Enum):
    empty = 0
    material = 1
    fluid = 2


class TubeActor(vtk.vtkActor):
    def __init__(self, project, **kwargs) -> None:
        super().__init__()

        self.project = project
        self.preprocessor = project.preprocessor
        self.elements = project.get_structural_elements()
        self.hidden_elements = kwargs.get('hidden_elements', set())
        self.color_mode = ColorMode.empty

        self.build()

    def build(self):
        visible_elements = {i:e for i, e in self.elements.items() if (i not in self.hidden_elements)}
        # self._key_index  = {j:i for i,j in enumerate(visible_elements)}
        self._key_indexes = dict()

        mapper = vtk.vtkPolyDataMapper()
        append_polydata = vtk.vtkAppendPolyData()

        total_points_appended = 0 
        for i, element in visible_elements.items():            
            x,y,z = element.first_node.coordinates
            section_rotation_xyz = element.section_rotation_xyz_undeformed

            source: vtk.vtkPolyData = self.create_element_data(element)
            if source is None:
                continue

            entity = self.preprocessor.elements_to_line[i]
            set_polydata_property(source, i, "element_index")
            set_polydata_property(source, entity, "entity_index")

            self._key_indexes[i] = range(total_points_appended, total_points_appended + source.GetNumberOfPoints())
            total_points_appended += source.GetNumberOfPoints()

            transform = vtk.vtkTransform()
            transform.Translate((element.length/2, 0, 0))
            transform.Translate((x,y,z))
            transform.RotateX(section_rotation_xyz[0])
            transform.RotateZ(section_rotation_xyz[2])
            transform.RotateY(section_rotation_xyz[1])
            transform.RotateY(180)
            transform.RotateZ(-90)
            transform.Update()

            transform_filter = vtk.vtkTransformFilter()
            transform_filter.SetInputData(source)
            transform_filter.SetTransform(transform)
            transform_filter.Update()

            append_polydata.AddInputData(transform_filter.GetOutput())
        
        if visible_elements:
            append_polydata.Update()
            appended_data = append_polydata.GetOutput()
        else:
            appended_data = vtk.vtkPolyData()

        normals_filter = vtk.vtkPolyDataNormals()
        normals_filter.AddInputData(appended_data)
        normals_filter.Update()

        data: vtk.vtkPolyData = normals_filter.GetOutput()

        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)

        self.clear_colors()

    def create_element_data(self, element):
        cross_section = element.cross_section
        if cross_section is None:
            return None

        if "Pipe section" in cross_section.section_label:
            d_out = cross_section.outer_diameter
            t = cross_section.thickness
            return cross_section_sources.pipe_data(element.length, d_out, t)

        elif cross_section.section_label == "Rectangular section":
            b, h, t, *_ = cross_section.section_parameters
            return cross_section_sources.rectangular_beam_data(element.length, b, h, t)

        elif cross_section.section_label == "Circular section":
            d_out, t, *_ = cross_section.section_parameters
            return cross_section_sources.circular_beam_data(element.length, d_out, t)

        elif cross_section.section_label == "C-section":
            h, w1, t1, w2, t2, tw, *_ = cross_section.section_parameters
            return cross_section_sources.c_beam_data(element.length, h, w1, w2, t1, t2, tw)

        elif cross_section.section_label == "I-section":

            h, w1, t1, w2, t2, tw, *_ = cross_section.section_parameters
            return cross_section_sources.i_beam_data(element.length, h, w1, w2, t1, t2, tw)

        elif cross_section.section_label == "T-section":
            h, w1, t1, tw, *_ = cross_section.section_parameters
            return cross_section_sources.t_beam_data(element.length, h, w1, t1, tw)

        return None

    def clear_colors(self):
        data = self.GetMapper().GetInput()
        set_polydata_colors(data, (255,255,255))

        if self.color_mode == ColorMode.material:
            self.color_by_material()

        elif self.color_mode == ColorMode.fluid:
            self.color_by_fluid()
    
    def color_by_material(self):
        grouped_by_color = defaultdict(list)
        elements = self.project.get_structural_elements()
        for i, e in elements.items():
            if i in self.hidden_elements:
                continue
            color = (0,0,0)
            if (e.material is not None) and e.material.color:
                # get the color and make it a bit brighter
                color = np.array(e.material.getColorRGB()) + 50
                color = tuple(np.clip(color, 0, 255))
            grouped_by_color[color].append(i)
        
        for color, elements in grouped_by_color.items():
            self.set_color(color, elements)

    def color_by_fluid(self):
        grouped_by_color = defaultdict(list)
        elements = self.project.get_structural_elements()
        for i, e in elements.items():
            if i in self.hidden_elements:
                continue
            color = (0,0,0)
            if (e.fluid is not None) and e.fluid.color:
                # get the color and make it a bit brighter
                color = np.array(e.fluid.getColorRGB()) + 50
                color = tuple(np.clip(color, 0, 255))
            grouped_by_color[color].append(i)
        
        for color, elements in grouped_by_color.items():
            self.set_color(color, elements)

    def set_color(self, color, elements=None, entities=None):
        if len(color) != 3:
            return

        data = self.GetMapper().GetInput()
        if (elements is None) and (entities is None):
            set_polydata_colors(data, color)
            self.GetMapper().SetScalarModeToUseCellData()
            self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
            self.GetMapper().ScalarVisibilityOn()
            return
        
        elements = set(elements) if elements else set()
        entities = set(entities) if entities else set()

        n_cells = data.GetNumberOfCells()
        element_indexes: vtk.vtkIntArray = data.GetCellData().GetArray("element_index")
        entity_indexes: vtk.vtkIntArray = data.GetCellData().GetArray("entity_index")
        colors: vtk.vtkCharArray = data.GetCellData().GetArray("colors")

        for i in range(n_cells):
            element = element_indexes.GetValue(i)
            entity = entity_indexes.GetValue(i)
            if (entity in entities) or (element in elements):
                colors.SetTuple(i, color)
        
        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def set_color_table(self, color_table: ColorTable):
        data = self.GetMapper().GetInput()
        element_indexes: vtk.vtkIntArray = data.GetCellData().GetArray("element_index")
        colors: vtk.vtkCharArray = data.GetCellData().GetArray("colors")

        element_colors = dict()
        for i, element in self.elements.items():
            element_colors[i] = color_table.get_color(element)

        n_cells = data.GetNumberOfCells()
        for i in range(n_cells):
            element_index = element_indexes.GetValue(i)
            color = element_colors[element_index]
            colors.SetTuple(i, color)

        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()
    
    def get_cell_element(self, cell):
        data = self.GetMapper().GetInput()
        element_indexes: vtk.vtkIntArray = data.GetCellData().GetArray("element_index")
        return element_indexes.GetValue(cell)

    def get_cell_entity(self, cell):
        data = self.GetMapper().GetInput()
        entity_indexes: vtk.vtkIntArray = data.GetCellData().GetArray("entity_index")
        return entity_indexes.GetValue(cell)
