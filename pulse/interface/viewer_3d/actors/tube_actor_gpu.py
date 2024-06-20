import vtk
import numpy as np
from enum import Enum

from opps.interface.viewer_3d.utils import cross_section_sources 
from pulse.interface.viewer_3d.coloring.colorTable import ColorTable

class ColorMode(Enum):
    empty = 0
    material = 1
    fluid = 2


class TubeActorGPU(vtk.vtkActor):
    '''
    This is an implementation of the tube actor that shows every element separatedly.
    Because we usually hava a lot of elements, this actor need to be incredbly fast.

    To match this requirement the vtkGlyph3DMapper is used, so we don't need to create
    an actual mesh (that would need a lot of time).
    With vtkGlyph3DMapper we just need to create some arrays and very few meshes, and
    send it to the GPU, and the hard work is handled there (very fastly btw).
    '''
    def __init__(self, project, show_deformed=False, **kwargs) -> None:
        super().__init__()

        self.project = project
        self.preprocessor = project.preprocessor
        self.elements = project.get_structural_elements()
        self.hidden_elements = kwargs.get('hidden_elements', set())
        self.show_deformed = show_deformed
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
            if self.show_deformed:
                points.InsertNextPoint(*element.first_node.deformed_coordinates)
                rotations.InsertNextTuple(element.deformed_rotation_xyz)
            else:
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

        self.GetProperty().SetInterpolationToPhong()
        self.GetProperty().SetDiffuse(0.8)
        self.GetProperty().SetSpecular(1.5)
        self.GetProperty().SetSpecularPower(80)
        self.GetProperty().SetSpecularColor(1, 1, 1)

    def create_element_data(self, element):
        cross_section = element.cross_section
        if cross_section is None:
            return None

        if "Pipe section" in cross_section.section_label:
            d_out, t, *_ = cross_section.section_parameters
            return cross_section_sources.pipe_data(element.length, d_out, t, sides=30)

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

        for i, element in self.elements.items():
            index = self._key_index.get(i)
            if index is None:
                continue
            color = color_table.get_color(element)
            colors.SetTuple(index, color)

        data.GetPointData().SetScalars(colors)
        self.GetMapper().Update()

    def color_by_material(self):
        # This copy is needed, otherwise the mapper is not updated
        data: vtk.vtkPolyData = self.GetMapper().GetInput()
        colors = vtk.vtkUnsignedCharArray()
        colors.DeepCopy(data.GetPointData().GetScalars())

        for element in self.elements.values():
            index = self._key_index.get(element)
            if index is None:
                continue

            # get the element color and make it a bit brighter
            color = np.array(element.material.getColorRGB()) + 50
            color = tuple(np.clip(color, 0, 255))
            colors.SetTuple(index, color)

        data.GetPointData().SetScalars(colors)
        self.GetMapper().Update()

    def color_by_fluid(self):
        # This copy is needed, otherwise the mapper is not updated
        data: vtk.vtkPolyData = self.GetMapper().GetInput()
        colors = vtk.vtkUnsignedCharArray()
        colors.DeepCopy(data.GetPointData().GetScalars())

        for element in self.elements.values():
            index = self._key_index.get(element)
            if index is None:
                continue

            # get the element color and make it a bit brighter
            color = np.array(element.fluid.getColorRGB()) + 50
            color = tuple(np.clip(color, 0, 255))
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
        transform.RotateZ(-90)
        transform.RotateY(180)
        transform.Update()

        transform_filter = vtk.vtkTransformFilter()
        transform_filter.SetInputData(source)
        transform_filter.SetTransform(transform)
        transform_filter.Update()

        normals_filter = vtk.vtkPolyDataNormals()
        normals_filter.AddInputData(transform_filter.GetOutput())
        normals_filter.Update()

        return normals_filter.GetOutput()
