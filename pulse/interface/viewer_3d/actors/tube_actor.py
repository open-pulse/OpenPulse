import logging

import numpy as np
from vtkmodules.util.numpy_support import numpy_to_vtk
from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkIntArray, vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkPlane, vtkPolyData
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkRenderingCore import vtkActor, vtkGlyph3DMapper

from pulse import app
from pulse.interface.viewer_3d.coloring.color_table import ColorTable
from pulse.model.cross_section import CrossSection
from pulse.model.elements.element_attributes import ElementAttributes
from pulse.utils import cross_section_sources
from pulse.utils.interface_utils import ColorMode


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
        self.user_preferences = app().main_window.config.user_preferences
        self.elements_attributes = app().project.model.preprocessor.elements_attributes
        self.deformed_coordinates = app().project.model.preprocessor.deformed_coordinates
        self.build()

    @property
    def model(self):
        return app().project.model

    @property
    def preprocessor(self):
        return app().project.model.preprocessor

    def build(self):
        all_elements = np.array(list(self.elements_attributes.keys()), dtype=int)
        self._key_index = {j: i for i, j in enumerate(all_elements)}

        data = vtkPolyData()
        mapper = vtkGlyph3DMapper()

        self.element_start_points = vtkPoints()
        self.element_start_points.SetNumberOfPoints(len(all_elements))

        self.element_rotations = vtkDoubleArray()
        self.element_rotations.SetNumberOfComponents(3)
        self.element_rotations.SetName("rotations")

        sources = vtkIntArray()
        sources.SetName("sources")

        colors = vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetNumberOfTuples(len(all_elements))
        colors.Fill(255)
        colors.SetName("colors")

        hashes = [id(el.cross_section) for el in self.elements_attributes.values()]
        unique_hashes, first_occurrences, remapped_indexes = np.unique(hashes, return_index=True, return_inverse=True)
        new_ids = np.arange(len(unique_hashes))

        sources.DeepCopy(numpy_to_vtk(remapped_indexes))
        sources.SetName("sources")

        for new_id, unique_hash, element_index in zip(new_ids, unique_hashes, first_occurrences):
            element_attributes = self.elements_attributes.get(element_index)
            source = self.create_element_data(element_attributes)
            source = self._fixed_section(source)
            mapper.SetSourceData(new_id, source)

        data.SetPoints(self.element_start_points)
        data.GetPointData().AddArray(sources)
        data.GetPointData().AddArray(self.element_rotations)
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

        self.update_element_coordinates_and_rotations()
        self.clear_colors()

    def get_all_elements_coordinates(self) -> np.ndarray:
        mesh = self.model.mesh
        return mesh.nodal_coordinates[mesh.lines_connectivity[:, 4], 1:]

    def get_all_elements_rotations(self):
        return self.preprocessor.undeformed_section_rotations

    def update_element_coordinates_and_rotations(self):
        coordinates = self.get_all_elements_coordinates()
        rotations = self.get_all_elements_rotations()

        mapper = self.GetMapper()
        if mapper is None:
            return

        data: vtkPolyData | None = mapper.GetInput()
        if data is None:
            return

        points: vtkPoints | None = data.GetPoints()
        if points is None:
            return
        
        point_data = data.GetPointData()
        if point_data is None:
            return
        
        rotations_array = point_data.GetArray("rotations")
        if rotations_array is None:
            return
        
        points.SetData(numpy_to_vtk(coordinates))
        rotations_array.DeepCopy(numpy_to_vtk(rotations))
        rotations_array.SetName("rotations")

    def create_element_data(self, element_attributes: ElementAttributes):
        cross_section = element_attributes.cross_section
        length = element_attributes.length
        section_parameters_render = element_attributes.section_parameters_render

        if not isinstance(cross_section, CrossSection):
            return vtkPolyData()

        tube_sides = self._get_tube_sides()

        if cross_section.section_type_label in ["pipe", "bend", "arc_bend", "reducer"]:
            if section_parameters_render is None:
                d_out, t, offset_y, offset_z, *_ = np.round(cross_section.section_parameters, 5)
            else:
                d_out, t, offset_y, offset_z, *_ = np.round(section_parameters_render, 5)

            return cross_section_sources.pipe_data(length, d_out, t, offset_y, offset_z, sides=tube_sides)

        elif cross_section.section_type_label == "rectangular_beam":
            b, h, b_in, h_in, offset_y, offset_z, *_ = np.round(cross_section.section_parameters, 5)
            return cross_section_sources.rectangular_beam_data(length, b, h, b_in, h_in, offset_y=offset_y, offset_z=offset_z)

        elif cross_section.section_type_label == "circular_beam":
            d_out, t, offset_y, offset_z, *_ = np.round(cross_section.section_parameters, 5)
            return cross_section_sources.circular_beam_data(length, d_out, t, offset_y=offset_y, offset_z=offset_z)

        elif cross_section.section_type_label == "c_beam":
            h, w1, t1, w2, t2, tw, offset_y, offset_z, *_ = np.round(cross_section.section_parameters, 5)
            return cross_section_sources.c_beam_data(length, h, w1, w2, t1, t2, tw, offset_y=offset_y, offset_z=offset_z)

        elif cross_section.section_type_label == "i_beam":
            h, w1, t1, w2, t2, tw, offset_y, offset_z, *_ = np.round(cross_section.section_parameters, 5)
            return cross_section_sources.i_beam_data(length, h, w1, w2, t1, t2, tw, offset_y=offset_y, offset_z=offset_z)

        elif cross_section.section_type_label == "t_beam":
            h, w1, t1, tw, offset_y, offset_z, *_ = np.round(cross_section.section_parameters, 5)
            return cross_section_sources.t_beam_data(length, h, w1, t1, tw, offset_y=offset_y, offset_z=offset_z)

        elif cross_section.section_type_label == "expansion_joint":
            d_eff, offset_y, offset_z, plot_key = np.round(section_parameters_render, 5)

            if plot_key == "major":
                d_out = d_eff * 1.25
            elif plot_key == "minor":
                d_out = d_eff * 1.1
            else:
                d_out = d_eff * 1.4

            t = (d_out - d_eff) / 2
            # if args:
            #     d_in = args[0]
            #     t = (d_out - d_in) / 2
            # else:
            #     t = (d_out - d_eff) / 2

            return cross_section_sources.pipe_data(length, d_out, t, offset_y=offset_y, offset_z=offset_z, sides=tube_sides)

        elif cross_section.section_type_label == "valve":
            d_out, t, offset_y, offset_z, *_ = np.round(section_parameters_render, 5)
            return cross_section_sources.pipe_data(length, d_out, t, offset_y=offset_y, offset_z=offset_z, sides=tube_sides)

        else:
            logging.warn(f"Representation not found for section {cross_section.section_type_label}")

        return None

    def _get_tube_sides(self):
        if len(self.elements_attributes) > 100_000:
            return 10
        elif len(self.elements_attributes) > 10_000:
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
            tubes_color = self.user_preferences.tubes_color.to_rgb()
            self.set_color(tubes_color)

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

        for elem_id in elements:
            index = self._key_index.get(elem_id)
            colors.SetTuple(index, color)

        data.GetPointData().SetScalars(colors)
        self.GetMapper().Update()

    def set_color_table(self, color_table: ColorTable):
        # This copy is needed, otherwise the mapper is not updated
        data: vtkPolyData = self.GetMapper().GetInput()
        colors = vtkUnsignedCharArray()
        colors.DeepCopy(data.GetPointData().GetScalars())

        for elem_id, element_attributes in self.elements_attributes.items():
            index = self._key_index.get(elem_id)
            if index is None:
                continue

            color = color_table.get_element_color(element_attributes)
            colors.SetTuple(index, color)

        data.GetPointData().SetScalars(colors)
        self.GetMapper().Update()

    def color_by_material(self):
        # This copy is needed, otherwise the mapper is not updated
        data: vtkPolyData = self.GetMapper().GetInput()
        colors = vtkUnsignedCharArray()
        colors.DeepCopy(data.GetPointData().GetScalars())

        for elem_id, element_attributes in self.elements_attributes.items():
            index = self._key_index.get(elem_id)
            if index is None:
                continue

            material = element_attributes.material
            if material is None:
                colors.SetTuple(index, (255, 255, 255))
                continue

            # get the element color and make it a bit brighter
            # color = np.array(element.material.getColorRGB()) + 50
            color = np.array(material.color) + 50

            color = tuple(np.clip(color, 0, 255))
            colors.SetTuple(index, color)

        data.GetPointData().SetScalars(colors)
        self.GetMapper().Update()

    def color_by_fluid(self):
        # This copy is needed, otherwise the mapper is not updated
        data: vtkPolyData = self.GetMapper().GetInput()
        colors = vtkUnsignedCharArray()
        colors.DeepCopy(data.GetPointData().GetScalars())

        for elem_id, element_attributes in self.elements_attributes.items():
            index = self._key_index.get(elem_id)
            if index is None:
                continue

            fluid = element_attributes.fluid
            if fluid is None:
                colors.SetTuple(index, (255, 255, 255))
                continue

            # get the element color and make it a bit brighter
            # color = np.array(element.fluid.getColorRGB()) + 50
            color = np.array(fluid.color) + 50

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

    def _hash_element_section(self, element_attributes: ElementAttributes):

        cross_section = element_attributes.cross_section
        if cross_section is None:
            return 0

        section_parameters = element_attributes.section_parameters_render
        if section_parameters is None:
            section_parameters = cross_section.section_parameters

        # if section_parameters is not None:
        #     section_parameters = tuple(section_parameters)

        length_rounded = round(element_attributes.length, 5)
        section_label = cross_section.section_type_label

        return hash((length_rounded, section_label, tuple(section_parameters)))

    def _fixed_section(self, source):
        if source is None:
            return vtkPolyData()

        normals_filter = vtkPolyDataNormals()
        normals_filter.AddInputData(source)
        normals_filter.Update()

        return normals_filter.GetOutput()
