import vtk


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

            source = self.create_element_data(element)
            self._key_indexes[i] = range(total_points_appended, total_points_appended + source.GetNumberOfPoints())
            total_points_appended += source.GetNumberOfPoints()

            # for _ in range(source.GetNumberOfPoints()):
            #     self._colors.InsertNextTuple((255,255,255))

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
        mapper.SetInputData(append_polydata.GetOutput())
        self.SetMapper(mapper)

    def create_element_data(self, element):
        return self.pipe_data(element.length, 0.08, 0.001)
        # sphere = vtk.vtkSphereSource()
        # sphere.SetRadius(0.1)
        # sphere.Update()
        # return sphere.GetOutput()

    def pipe_data(self, length, outside_diameter, thickness):
        cilinder = vtk.vtkCylinderSource()
        cilinder.SetResolution(20)
        cilinder.SetRadius(outside_diameter / 2)
        cilinder.SetHeight(length)
        if thickness == 0:
            cilinder.CappingOn()
        else:
            cilinder.CappingOff()
        cilinder.Update()
        return cilinder.GetOutput()

    def circular_beam_data(self, length, outside_diameter, thickness):
        return self.pipe_data(length, )

    def square_beam_data(self, length, base, height, thickness):
        pass

    def c_beam_data(self, length, h, w1, w2, t1, t2, tw):
        pass

    def i_beam_data(self, length, h, w1, w2, t1, t2, tw):
        pass

    def t_section(self, length, h, w1, t1, tw):
        '''
        bottom:             top:
        0          1        8          9
        ┌──────────┐        ┌──────────┐
        │          │        │          │
       2└──┐    ┌──┘3     10└──┐    ┌──┘11
          4│    │5           12│    │13
           │    │              │    │
           │    │              │    │
           │    │              │    │
          6└────┘7           14└────┘15
        '''

        # data = vtk.vtkPolyData()
        # points = vtk.vtkPoints()
        # points.SetNumberOfPoints(16)

        # points.SetPoint(0, -w1/2, )