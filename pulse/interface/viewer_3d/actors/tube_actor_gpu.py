import vtk
from enum import Enum

from .tube_actor import TubeActor
from pulse.interface.viewer_3d.coloring.colorTable import ColorTable

class ColorMode(Enum):
    empty = 0
    material = 1
    fluid = 2


class TubeActorGPU(TubeActor):
    '''
    This is an implementation of the tube actor that shows every element separatedly.
    Because we usually hava a lot of elements, this actor need to be incredbly fast.

    To match this requirement the vtkGlyph3DMapper is used, so we don't need to create
    an actual mesh (that would need a lot of time).
    With vtkGlyph3DMapper we just need to create some arrays and very few meshes, and
    send it to the GPU, and the hard work is handled there (very fastly btw).
    '''
    def __init__(self, project, **kwargs) -> None:
        super().__init__(project, **kwargs)

        self.project = project
        self.preprocessor = project.preprocessor
        self.elements = project.get_structural_elements()
        self.hidden_elements = kwargs.get('hidden_elements', set())
        self.color_mode = ColorMode.empty

        self.build()

    def build(self):
        visible_elements = {i:e for i, e in self.elements.items() if (i not in self.hidden_elements)}
        self._key_index  = {j:i for i,j in enumerate(visible_elements.keys())}

        data = vtk.vtkPolyData()
        mapper = vtk.vtkGlyph3DMapper()

        points = vtk.vtkPoints()
        sources = vtk.vtkIntArray()
        sources.SetName('sources')

        rotations = vtk.vtkDoubleArray()
        rotations.SetNumberOfComponents(3)
        rotations.SetName('rotations')

        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetNumberOfTuples(len(visible_elements))
        colors.Fill(255)
        colors.SetName('colors')

        section_index = dict()
        for element in visible_elements.values():
            points.InsertNextPoint(*element.first_node.coordinates)
            rotations.InsertNextTuple(element.section_rotation_xyz_undeformed)

            key = self._hash_element_section(element)
            if key not in section_index:
                section_index[key] = len(section_index)
                source = self.create_element_data(element)
                source = self._fixed_section(source)
                mapper.SetSourceData(section_index[key], source)
            sources.InsertNextTuple1(section_index[key])

        data.SetPoints(points)
        data.GetPointData().AddArray(sources)
        data.GetPointData().AddArray(rotations)
        data.GetPointData().SetScalars(colors)

        mapper.SetInputData(data)
        mapper.SourceIndexingOn()
        mapper.SetSourceIndexArray('sources')
        mapper.SetOrientationArray('rotations')
        mapper.SetScaleFactor(1)
        mapper.SetOrientationModeToRotation()
        mapper.SetScalarModeToUsePointData()
        mapper.ScalarVisibilityOn()
        mapper.Update()

        self.SetMapper(mapper)

    def clear_colors(self):
        if self.color_mode == ColorMode.empty:
            self.set_color((255, 255, 255))

        elif self.color_mode == ColorMode.material:
            self.color_by_material()

        elif self.color_mode == ColorMode.fluid:
            self.color_by_fluid()

    def set_color(self, color, elements=None, entities=None):
        # This copy is needed, otherwise the mapper is not updated
        data: vtk.vtkPolyData = self.GetMapper().GetInput()
        colors = vtk.vtkUnsignedCharArray()
        colors.DeepCopy(data.GetPointData().GetScalars())

        if (elements is None) and (entities is None):
            for component, value in enumerate(color):
                colors.FillComponent(component, value)
            data.GetPointData().SetScalars(colors)
            self.GetMapper().Update()
            return

        if elements is None:
            elements = set()

        # Get the elements inside every entity to paint them
        line_to_elements = self.project.preprocessor.line_to_elements
        for entity in entities:
            entity_elements = line_to_elements[entity]
            elements |= set(entity_elements)

        for element in elements:
            index = self._key_index.get(element)
            colors.SetTuple(index, color)

        data.GetPointData().SetScalars(colors)
        self.GetMapper().Update()

    def set_color_table(self, color_table: ColorTable):
        # This copy is needed, otherwise the mapper is not updated
        data: vtk.vtkPolyData = self.GetMapper().GetInput()
        colors = vtk.vtkUnsignedCharArray()
        colors.DeepCopy(data.GetPointData().GetScalars())

        for element in self.elements.values():
            color = color_table.get_color(element)
            index = self._key_index.get(element)
            colors.SetTuple(index, color)

        data.GetPointData().SetScalars(colors)
        self.GetMapper().Update()

    def apply_cut(self, origin, normal):
        self.plane = vtk.vtkPlane()
        self.plane.SetOrigin(origin)
        self.plane.SetNormal(normal)
        self.GetMapper().AddClippingPlane(self.plane)

    def disable_cut(self):
        self.GetMapper().RemoveAllClippingPlanes()

    def _hash_element_section(self, element):
        return hash((
            round(element.length, 5),
            element.cross_section.section_label,
            tuple(element.cross_section.section_parameters),
        ))

    def _fixed_section(self, source):
        transform = vtk.vtkTransform()
        transform.RotateY(180)
        transform.RotateZ(-90)
        transform.Update()

        transform_filter = vtk.vtkTransformFilter()
        transform_filter.SetInputData(source)
        transform_filter.SetTransform(transform)
        transform_filter.Update()

        normals_filter = vtk.vtkPolyDataNormals()
        normals_filter.AddInputData(transform_filter.GetOutput())
        normals_filter.Update()

        return normals_filter.GetOutput()
