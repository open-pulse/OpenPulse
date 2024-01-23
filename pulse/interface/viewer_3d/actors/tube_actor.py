import vtk
from vtkat.utils import set_polydata_property, set_polydata_colors

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
        data = append_polydata.GetOutput()
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
            return self.pipe_data(element.length, d_out, t)

        elif cross_section.section_label == "Rectangular section":
            b, h, *_ = cross_section.section_parameters
            return self.rectangular_beam_data(element.length, b, h)

        elif cross_section.section_label == "Circular section":
            d_out, t, *_ = cross_section.section_parameters
            return self.circular_beam_data(element.length, d_out, t)

        elif cross_section.section_label == "C-section":
            h, w1, t1, w2, t2, tw, *_ = cross_section.section_parameters
            return self.c_beam_data(element.length, h, w1, w2, t1, t2, tw)

        elif cross_section.section_label == "I-section":

            h, w1, t1, w2, t2, tw, *_ = cross_section.section_parameters
            return self.i_beam_data(element.length, h, w1, w2, t1, t2, tw)

        elif cross_section.section_label == "T-section":
            h, w1, t1, tw, *_ = cross_section.section_parameters
            return self.t_beam_data(element.length, h, w1, t1, tw)

        return None

    def clear_colors(self):
        data = self.GetMapper().GetInput()
        set_polydata_colors(data, (255,255,255))

    def set_color(self, color, elements=None, entities=None):
        data = self.GetMapper().GetInput()
        if (elements is None) and (entities is None):
            set_polydata_colors(data, color)
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
            if entity in entities or element in elements:
                colors.SetTuple3(i, *color)

    def set_color_table(self, color_table):
        pass

    # 
    def pipe_data(self, length, outside_diameter, thickness):
        if thickness == 0:
            return self.closed_pipe_data(length, outside_diameter)
        cilinder = vtk.vtkCylinderSource()
        cilinder.SetResolution(20)
        cilinder.SetRadius(outside_diameter / 2)
        cilinder.SetHeight(length)
        cilinder.CappingOff()
        cilinder.Update()
        return cilinder.GetOutput()

    def closed_pipe_data(self, length, outside_diameter):
        cilinder = vtk.vtkCylinderSource()
        cilinder.SetResolution(20)
        cilinder.SetRadius(outside_diameter / 2)
        cilinder.SetHeight(length)
        cilinder.CappingOn()
        cilinder.Update()
        return cilinder.GetOutput()

    def circular_beam_data(self, length, outside_diameter, thickness):
        return self.pipe_data(length, outside_diameter, thickness)

    def rectangular_beam_data(self, length, b, h, t):
        if t == 0:
            return self.closed_rectangular_beam_data(length, b, h)

        rectangular_top = vtk.vtkCubeSource()
        rectangular_left = vtk.vtkCubeSource()
        rectangular_right = vtk.vtkCubeSource()
        rectangular_bottom = vtk.vtkCubeSource()

        rectangular_top.SetYLength(length)
        rectangular_top.SetZLength(t)
        rectangular_top.SetXLength(b)
        rectangular_top.SetCenter(0, 0, -h/2 + t/2)

        rectangular_left.SetYLength(length)
        rectangular_left.SetZLength(h)
        rectangular_left.SetXLength(t)
        rectangular_left.SetCenter(-b/2 + t/2, 0, 0)

        rectangular_right.SetYLength(length)
        rectangular_right.SetZLength(h)
        rectangular_right.SetXLength(t)
        rectangular_right.SetCenter(b/2 - t/2, 0, 0)

        rectangular_bottom.SetYLength(length)
        rectangular_bottom.SetZLength(t)
        rectangular_bottom.SetXLength(b)
        rectangular_bottom.SetCenter(0, 0, h/2 - t/2)

        rectangular_top.Update()
        rectangular_left.Update()
        rectangular_right.Update()
        rectangular_bottom.Update()

        append_polydata = vtk.vtkAppendPolyData()
        append_polydata.AddInputData(rectangular_top.GetOutput())
        append_polydata.AddInputData(rectangular_left.GetOutput())
        append_polydata.AddInputData(rectangular_right.GetOutput())
        append_polydata.AddInputData(rectangular_bottom.GetOutput())
        append_polydata.Update()

        return append_polydata.GetOutput()

    def closed_rectangular_beam_data(self, length, b, h):
        rectangular = vtk.vtkCubeSource()
        rectangular.SetYLength(length)
        rectangular.SetXLength(b)
        rectangular.SetZLength(h)
        rectangular.Update()
        return rectangular.GetOutput()

    def c_beam_data(self, length, h, w1, w2, t1, t2, tw):
        rectangular_top = vtk.vtkCubeSource()
        rectangular_left = vtk.vtkCubeSource()
        rectangular_bottom = vtk.vtkCubeSource()

        rectangular_top.SetYLength(length)
        rectangular_top.SetZLength(t1)
        rectangular_top.SetXLength(w1)
        rectangular_top.SetCenter(w1/2 - max(w1, w2)/2, 0, -h/2 + t1/2)

        rectangular_left.SetYLength(length)
        rectangular_left.SetZLength(h)
        rectangular_left.SetXLength(tw)
        rectangular_left.SetCenter(-max(w1, w2)/2 + tw/2, 0, 0)

        rectangular_bottom.SetYLength(length)
        rectangular_bottom.SetZLength(t2)
        rectangular_bottom.SetXLength(w2)
        rectangular_bottom.SetCenter(w2/2 - max(w1, w2)/2, 0, h/2 - t2/2)

        rectangular_top.Update()
        rectangular_left.Update()
        rectangular_bottom.Update()

        append_polydata = vtk.vtkAppendPolyData()
        append_polydata.AddInputData(rectangular_top.GetOutput())
        append_polydata.AddInputData(rectangular_left.GetOutput())
        append_polydata.AddInputData(rectangular_bottom.GetOutput())
        append_polydata.Update()

        return append_polydata.GetOutput()

    def i_beam_data(self, length, h, w1, w2, t1, t2, tw):
        rectangular_top = vtk.vtkCubeSource()
        rectangular_center = vtk.vtkCubeSource()
        rectangular_bottom = vtk.vtkCubeSource()

        rectangular_top.SetYLength(length)
        rectangular_top.SetZLength(t1)
        rectangular_top.SetXLength(w1)
        rectangular_top.SetCenter(0, 0, -h/2 + t1/2)

        rectangular_center.SetYLength(length)
        rectangular_center.SetZLength(h)
        rectangular_center.SetXLength(tw)

        rectangular_bottom.SetYLength(length)
        rectangular_bottom.SetZLength(t2)
        rectangular_bottom.SetXLength(w2)
        rectangular_bottom.SetCenter(0, 0, h/2 - t2/2)

        rectangular_top.Update()
        rectangular_center.Update()
        rectangular_bottom.Update()

        append_polydata = vtk.vtkAppendPolyData()
        append_polydata.AddInputData(rectangular_top.GetOutput())
        append_polydata.AddInputData(rectangular_center.GetOutput())
        append_polydata.AddInputData(rectangular_bottom.GetOutput())
        append_polydata.Update()

        return append_polydata.GetOutput()

    def t_beam_data(self, length, h, w1, t1, tw):
        rectangular_top = vtk.vtkCubeSource()
        rectangular_center = vtk.vtkCubeSource()

        rectangular_top.SetYLength(length)
        rectangular_top.SetZLength(t1)
        rectangular_top.SetXLength(w1)
        rectangular_top.SetCenter(0, 0, -h/2 + t1/2)

        rectangular_center.SetYLength(length)
        rectangular_center.SetZLength(h)
        rectangular_center.SetXLength(tw)

        rectangular_top.Update()
        rectangular_center.Update()

        append_polydata = vtk.vtkAppendPolyData()
        append_polydata.AddInputData(rectangular_top.GetOutput())
        append_polydata.AddInputData(rectangular_center.GetOutput())
        append_polydata.Update()

        return append_polydata.GetOutput()
