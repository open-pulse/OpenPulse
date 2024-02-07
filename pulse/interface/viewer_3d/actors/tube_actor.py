import vtk
from vtkat.utils import set_polydata_property, set_polydata_colors
from pulse.interface.viewer_3d.sources import cross_section_sources


class TubeActor(vtk.vtkActor):
    def __init__(self, project, **kwargs) -> None:
        super().__init__()

        self.project = project
        self.preprocessor = project.preprocessor
        self.elements = project.get_structural_elements()
        self.hidden_elements = kwargs.get('hidden_elements', set())

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
            transform.Translate((x,y,z))
            transform.RotateX(section_rotation_xyz[0])
            transform.RotateZ(section_rotation_xyz[2])
            transform.RotateY(section_rotation_xyz[1])
            transform.RotateZ(90)

            transform.Update()

            transform_filter = vtk.vtkTransformFilter()
            transform_filter.SetInputData(source)
            transform_filter.SetTransform(transform)
            transform_filter.Update()

            append_polydata.AddInputData(transform_filter.GetOutput())
        
        append_polydata.Update()
        data: vtk.vtkPolyData = append_polydata.GetOutput()
        set_polydata_colors(data, (255, 255, 255))

        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)

    def create_element_data(self, element):
        cross_section = element.cross_section
        if cross_section is None:
            return None

        if cross_section.section_label == "Pipe section":
            d_out = cross_section.outer_diameter
            t = cross_section.thickness
            return cross_section_sources.pipe_data(element.length, d_out, t)

        elif cross_section.section_label == "Rectangular section":
            b, h, *_ = cross_section.section_parameters
            return cross_section_sources.rectangular_beam_data(element.length, b, h)

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

    def set_color(self, color, elements=None, entities=None):
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
                colors.SetTuple3(i, *color)
        
        self.GetMapper().SetScalarModeToUseCellData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def set_color_table(self, color_table):
        pass
    
    def get_cell_element(self, cell):
        data = self.GetMapper().GetInput()
        element_indexes: vtk.vtkIntArray = data.GetCellData().GetArray("element_index")
        return element_indexes.GetValue(cell)

    def get_cell_entity(self, cell):
        data = self.GetMapper().GetInput()
        entity_indexes: vtk.vtkIntArray = data.GetCellData().GetArray("entity_index")
        return entity_indexes.GetValue(cell)
