import numpy as np
import logging
from opps.interface.viewer_3d.utils import cross_section_sources
from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkIntArray,
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import vtkPlane, vtkPolyData
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersGeneral import vtkTransformFilter
from vtkmodules.vtkRenderingCore import vtkActor, vtkGlyph3DMapper

from pulse import app
from pulse.interface.utils import ColorMode
from pulse.interface.viewer_3d.coloring.color_table import ColorTable


class TubeActor(vtkActor):
    """
    This actor show the tubes as a set of element sections that compose it.

    They should appear "sectioned", it is not a bug, it is a feature, because
    the "sections" are correspondent to what is happening in the FEM.

    Usually a model have a lot of elements, and to make this actor render fast,
    this implementations uses vtkGlyph3DMapper, wich is not a traditional approach,
    but is a very fast approach.

    With vtkGlyph3DMapper we just need to create some arrays and very few meshes,
    send them to the GPU, and the hard work is handled there (very fastly btw).
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()

        self.project = app().project
        self.model = self.project.model
        self.preprocessor = self.project.preprocessor
        self.elements = self.project.get_structural_elements()
        self.hidden_elements = kwargs.get("hidden_elements", set())
        self.build()

    def build(self):
        visible_elements = {
            i: e for i, e in self.elements.items() if (i not in self.hidden_elements)
        }
        self._key_index = {j: i for i, j in enumerate(visible_elements.keys())}

        data = vtkPolyData()
        mapper = vtkGlyph3DMapper()

        points = vtkPoints()
        sources = vtkIntArray()
        sources.SetName("sources")

        rotations = vtkDoubleArray()
        rotations.SetNumberOfComponents(3)
        rotations.SetName("rotations")

        colors = vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetNumberOfTuples(len(visible_elements))
        colors.Fill(255)
        colors.SetName("colors")

        section_index = dict()
        for element in visible_elements.values():
            points.InsertNextPoint(self.get_element_coordinates(element))
            rotations.InsertNextTuple(self.get_element_rotations(element))

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
        mapper.SetSourceIndexArray("sources")
        mapper.SetOrientationArray("rotations")
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

    def get_element_coordinates(self, element) -> tuple[float, float, float]:
        return element.first_node.coordinates

    def get_element_rotations(self, element) -> tuple[float, float, float]:
        return element.section_rotation_xyz_undeformed

    def create_element_data(self, element):
        cross_section = element.cross_section
        if cross_section is None:
            return vtkPolyData()
        
        tube_sides = self._get_tube_sides()
        length = element.length

        if cross_section.section_type_label in ["Pipe", "Reducer"]:
            d_out, t, offset_y, offset_z, *_ = element.section_parameters_render
            return cross_section_sources.pipe_data(length, d_out, t, offset_y, offset_z, sides=tube_sides)

        elif cross_section.section_type_label == "Rectangular section":
            b, h, b_in, h_in, offset_y, offset_z, *_ = element.section_parameters_render
            t0 = (b - b_in) / 2
            t1 = (h - h_in) / 2
            return cross_section_sources.rectangular_beam_data(length, b, h, t0, t1, offset_y=offset_y, offset_z=offset_z)

        elif cross_section.section_type_label == "Circular section":
            d_out, t, offset_y, offset_z, *_ = element.section_parameters_render
            return cross_section_sources.circular_beam_data(length, d_out, t, offset_y=offset_y, offset_z=offset_z)

        elif cross_section.section_type_label == "C-section":
            h, w1, t1, w2, t2, tw, offset_y, offset_z, *_ = element.section_parameters_render
            return cross_section_sources.c_beam_data(length, h, w1, w2, t1, t2, tw, offset_y=offset_y, offset_z=offset_z)

        elif cross_section.section_type_label == "I-section":
            h, w1, t1, w2, t2, tw, offset_y, offset_z, *_ = element.section_parameters_render
            return cross_section_sources.i_beam_data(length, h, w1, w2, t1, t2, tw, offset_y=offset_y, offset_z=offset_z)

        elif cross_section.section_type_label == "T-section":
            h, w1, t1, tw, offset_y, offset_z, *_ = element.section_parameters_render
            return cross_section_sources.t_beam_data(length, h, w1, t1, tw, offset_y=offset_y, offset_z=offset_z)

        elif cross_section.section_type_label == "Expansion joint":

            plot_key, d_eff, *args = element.section_parameters_render

            if plot_key == "major":
                d_out = d_eff * 1.25
            elif plot_key == "minor":
                d_out = d_eff * 1.1            
            else:
                d_out = d_eff * 1.4

            if args:
                d_in = args[0]
                t = (d_out - d_in) / 2
            else:
                t = (d_out - d_eff) / 2

            return cross_section_sources.pipe_data(length, d_out, t, sides=tube_sides)

        elif cross_section.section_type_label == "Valve":
            d_out, t, *_ = element.section_parameters_render
            return cross_section_sources.pipe_data(length, d_out, t, sides=tube_sides)
        
        else:
            logging.warn(f"Representation not found for section {cross_section.section_type_label}")

        return None
    
    def _get_tube_sides(self):
        if len(self.elements) > 100_000:
            return 10
        elif len(self.elements) > 10_000:
            return 20
        else:
            return 30

    def clear_colors(self):
        color_mode = app().main_window.visualization_filter.color_mode

        if color_mode == ColorMode.MATERIAL:
            self.color_by_material()

        elif color_mode == ColorMode.FLUID:
            self.color_by_fluid()

        else:
            self.set_color((255, 255, 255))

    def set_color(self, color, elements=None, lines=None):
        # This copy is needed, otherwise the mapper is not updated
        data: vtkPolyData = self.GetMapper().GetInput()
        colors = vtkUnsignedCharArray()
        colors.DeepCopy(data.GetPointData().GetScalars())

        if (elements is None) and (lines is None):
            for component, value in enumerate(color):
                colors.FillComponent(component, value)
            data.GetPointData().SetScalars(colors)
            self.GetMapper().Update()
            return

        if elements is None:
            elements = set()
        else:
            elements = set(elements)

        # Get the elements inside every entity to paint them
        line_to_elements = self.model.mesh.elements_from_line
        for line in lines:
            line_elements = line_to_elements[line]
            elements |= set(line_elements)

        for element in elements:
            index = self._key_index.get(element)
            colors.SetTuple(index, color)

        data.GetPointData().SetScalars(colors)
        self.GetMapper().Update()

    def set_color_table(self, color_table: ColorTable):
        # This copy is needed, otherwise the mapper is not updated
        data: vtkPolyData = self.GetMapper().GetInput()
        colors = vtkUnsignedCharArray()
        colors.DeepCopy(data.GetPointData().GetScalars())

        for i, element in self.elements.items():
            index = self._key_index.get(i)
            if index is None:
                continue
            color = color_table.get_element_color(element)
            colors.SetTuple(index, color)

        data.GetPointData().SetScalars(colors)
        self.GetMapper().Update()

    def color_by_material(self):
        # This copy is needed, otherwise the mapper is not updated
        data: vtkPolyData = self.GetMapper().GetInput()
        colors = vtkUnsignedCharArray()
        colors.DeepCopy(data.GetPointData().GetScalars())

        for i, element in self.elements.items():
            index = self._key_index.get(i)
            if index is None:
                continue

            if element.material is None:
                colors.SetTuple(index, (255, 255, 255))
                continue

            # get the element color and make it a bit brighter
            # color = np.array(element.material.getColorRGB()) + 50
            color = np.array(element.material.color) + 50

            color = tuple(np.clip(color, 0, 255))
            colors.SetTuple(index, color)

        data.GetPointData().SetScalars(colors)
        self.GetMapper().Update()

    def color_by_fluid(self):
        # This copy is needed, otherwise the mapper is not updated
        data: vtkPolyData = self.GetMapper().GetInput()
        colors = vtkUnsignedCharArray()
        colors.DeepCopy(data.GetPointData().GetScalars())

        for i, element in self.elements.items():
            index = self._key_index.get(i)
            if index is None:
                continue

            if element.fluid is None:
                colors.SetTuple(index, (255, 255, 255))
                continue

            # get the element color and make it a bit brighter
            # color = np.array(element.fluid.getColorRGB()) + 50
            color = np.array(element.fluid.color) + 50

            color = tuple(np.clip(color, 0, 255))
            colors.SetTuple(index, color)

        data.GetPointData().SetScalars(colors)
        self.GetMapper().Update()

    def apply_cut(self, origin, normal):
        self.plane = vtkPlane()
        self.plane.SetOrigin(origin)
        self.plane.SetNormal(normal)
        self.GetMapper().RemoveAllClippingPlanes()
        self.GetMapper().AddClippingPlane(self.plane)

    def disable_cut(self):
        self.GetMapper().RemoveAllClippingPlanes()

    def _hash_element_section(self, element):

        if element.cross_section is None:
            return 0

        section_label = element.cross_section.section_type_label
        section_parameters = element.section_parameters_render

        if section_parameters is not None:
            section_parameters = tuple(section_parameters)

        return hash((
            round(element.length, 5),
            section_label,
            section_parameters,
        ))

    def _fixed_section(self, source):
        if source is None:
            return vtkPolyData()

        transform = vtkTransform()
        transform.RotateZ(-90)
        transform.RotateY(180)
        transform.Update()

        transform_filter = vtkTransformFilter()
        transform_filter.SetInputData(source)
        transform_filter.SetTransform(transform)
        transform_filter.Update()

        normals_filter = vtkPolyDataNormals()
        normals_filter.AddInputData(transform_filter.GetOutput())
        normals_filter.Update()

        return normals_filter.GetOutput()
