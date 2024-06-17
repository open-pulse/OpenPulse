import vtk

from time import time

class TubeActorGPU(vtk.vtkActor):
    def __init__(self, project, **kwargs) -> None:
        super().__init__()

        self.project = project
        self.preprocessor = project.preprocessor
        self.elements = project.get_structural_elements()
        self.hidden_elements = kwargs.get('hidden_elements', set())

        self.build()

    def build(self):
        visible_elements = {i:e for i, e in self.elements.items() if (i not in self.hidden_elements)}
        self._key_index  = {j:i for i,j in enumerate(visible_elements)}

        data = vtk.vtkPolyData()
        mapper = vtk.vtkGlyph3DMapper()

        points = vtk.vtkPoints()
        sources = vtk.vtkIntArray()
        sources.SetName('sources')
        rotations = vtk.vtkDoubleArray()
        rotations.SetNumberOfComponents(3)
        rotations.SetName('rotations')

        for element in visible_elements.values():
            points.InsertNextPoint(*element.first_node.coordinates)
            rotations.InsertNextTuple(element.section_rotation_xyz_undeformed)
            sources.InsertNextTuple1(0)

            source = self.create_element_data(element)
            mapper.SetSourceData(0, source)

        data.SetPoints(points)
        data.GetPointData().AddArray(sources)
        data.GetPointData().AddArray(rotations)
        # data.GetPointData().SetScalars(self._colors)

        mapper.SetInputData(data)
        mapper.SourceIndexingOn()
        mapper.SetSourceIndexArray('sources')
        mapper.SetOrientationArray('rotations')
        mapper.SetScaleFactor(1)
        mapper.SetOrientationModeToRotation()
        mapper.Update()

        self.SetMapper(mapper)

        self.plane = vtk.vtkPlane()
        self.plane.SetOrigin((0.5, 0.5, 0.5))
        self.plane.SetNormal((1, 1, 0))
        mapper.AddClippingPlane(self.plane)

    def create_element_data(self, element):
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(0.1)
        sphere.Update()
        return sphere.GetOutput()

    def clear_colors(self, *args, **kwargs):
        pass

    def set_color(self, *args, **kwargs):
        pass

    def set_color_table(self, *args, **kwargs):
        pass