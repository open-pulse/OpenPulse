from functools import partial

import numpy as np
from molde.actors import CommonSymbolsActorFixedSize
from molde.colors import color_names
from molde.utils import read_obj_file, transform_polydata
from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkRenderingCore import vtkPolyDataMapper

from pulse import SYMBOLS_DIR, app
from pulse.utils.cross_section_sources import valve_data
from pulse.utils.rotations import align_vtk_geometry

from ..polydata import (
    create_compressor_discharge,
    create_compressor_suction,
    create_pump_discharge,
    create_pump_suction,
)


class FixedSymbolsActor(CommonSymbolsActorFixedSize):
    def __init__(self):
        super().__init__()
        self.build()
        self.configure_appearance()
        self.UseBoundsOff()

    def build(self):
        mapper = vtkPolyDataMapper()
        source = vtkAppendPolyData()

        self.create_compressor_symbol()
        self.create_reciprocating_pump_excitation()
        self.create_structural_links()
        self.create_psd_structural_links()
        self.create_acoustic_transfer_element()
        self.create_perforated_plates()
        self.create_valves()

        source.Update()
        mapper.SetInputData(source.GetOutput())
        self.SetMapper(mapper)

        return super().build()

    @property
    def preprocessor(self):
        return app().project.model.preprocessor

    @property
    def properties(self):
        return app().project.model.properties

    def create_compressor_symbol(self):
        for (property_name, *args), data in self.properties.nodal_properties.items():
            if property_name != "reciprocating_compressor_excitation":
                continue

            node_id = args[0]
            element_ids = self.preprocessor.elements_connected_to_node.get(node_id)

            if len(element_ids) != 1:
                continue

            node = self.preprocessor.nodes[node_id]
            element_attributes = self.preprocessor.elements_attributes.get(element_ids[0])
            orientation = element_attributes.last_node.coordinates - element_attributes.first_node.coordinates

            if node != element_attributes.first_node:
                orientation = -orientation

            node_id = int(*args)
            element_ids = self.preprocessor.elements_connected_to_node.get(node_id)
            cross_section = self.preprocessor.get_element_cross_section(element_ids[0])

            scale = cross_section.outer_diameter

            if data["connection_type"] == "discharge":
                self.add_symbol(create_compressor_discharge, data["coords"], orientation, color=color_names.RED_2, scale=scale)

            elif data["connection_type"] == "suction":
                self.add_symbol(create_compressor_suction, data["coords"], orientation, color=color_names.BLUE_2, scale=scale)

    def create_reciprocating_pump_excitation(self):
        for (property_name, *args), data in self.properties.nodal_properties.items():
            if property_name != "reciprocating_pump_excitation":
                continue

            node_id = args[0]
            element_ids = self.preprocessor.elements_connected_to_node.get(node_id)

            if len(element_ids) != 1:
                continue

            node = self.preprocessor.nodes[node_id]
            element_attributes = self.preprocessor.elements_attributes.get(element_ids[0])
            orientation = element_attributes.last_node.coordinates - element_attributes.first_node.coordinates

            if node != element_attributes.first_node:
                orientation = -orientation

            if data["connection_type"] == "discharge":
                self.add_symbol(create_pump_discharge, data["coords"], orientation, color=color_names.RED)

            elif data["connection_type"] == "suction":
                self.add_symbol(create_pump_suction, data["coords"], orientation, color=color_names.BLUE)

    def create_structural_links(self):
        for (property_name, *args), data in self.properties.nodal_properties.items():
            if property_name not in ["stiffness_nodal_links", "damping_nodal_links"]:
                continue

            func = partial(self._create_line, data["coords"][:3], data["coords"][3:])
            self.add_symbol(func, (0, 0, 0), (0, 0, 0), color_names.GREEN)

    def create_psd_structural_links(self):
        for (property_name, *args), data in self.properties.nodal_properties.items():
            if property_name != "psd_structural_links":
                continue

            creation_line_func = partial(self._create_line, data["coords"][:3], data["coords"][3:])
            self.add_symbol(creation_line_func, (0, 0, 0), (0, 0, 0), color_names.GREEN)

    def create_psd_acoustic_links(self):
        for (property_name, *args), data in self.properties.nodal_properties.items():
            if property_name != "psd_acoustic_link":
                continue

            creation_line_func = partial(self._create_line, data["coords"][:3], data["coords"][3:])
            self.add_symbol(creation_line_func, (0, 0, 0), (0, 0, 0), color_names.BLUE)

    def create_acoustic_transfer_element(self):
        for (property_name, *args), data in self.properties.nodal_properties.items():
            if property_name != "acoustic_transfer_element":
                continue

            creation_line_func = partial(self._create_line, data["coords"][:3], data["coords"][3:])
            self.add_symbol(creation_line_func, (0, 0, 0), (0, 0, 0), color_names.BLUE)

    def create_perforated_plates(self):
        pp_many_holes = read_obj_file(SYMBOLS_DIR / "acoustic/perforated_plate_many_holes.obj")
        pp_single_hole = read_obj_file(SYMBOLS_DIR / "acoustic/perforated_plate_single_hole.obj")

        for (property_name, element_id), data in self.properties.element_properties.items():
            if property_name != "perforated_plate":
                continue

            element_attributes = self.preprocessor.elements_attributes.get(element_id)
            if element_attributes is None:
                continue

            cross_section = element_attributes.cross_section

            # There must be a cleaner way, but I will just
            # copy this code from the previous version

            perforated_plate = element_attributes.perforated_plate_data
            pp_thickness = perforated_plate.plate_thickness
            if element_attributes.valve_data is not None:
                d_in = element_attributes.valve_data.effective_diameter
                diameter = d_in / 2

            else:
                diameter = cross_section.inner_diameter

            coord_a = element_attributes.first_node.coordinates
            coord_b = element_attributes.last_node.coordinates
            vector = coord_b - coord_a

            obj_data = pp_single_hole if perforated_plate.single_hole else pp_many_holes

            func = partial(
                transform_polydata,
                obj_data,
                rotation=(0, 0, 90),
                scale=(pp_thickness, diameter, diameter),
            )

            self.add_symbol(
                func,
                (coord_a + coord_b) / 2,
                vector,
                color_names.PINK_6,
            )

    def create_valves(self):
        line_properties = self.properties.line_properties

        for line_id, data in line_properties.items():
            if "valve_info" not in data.keys():
                continue

            coords_a = np.array(data["start_coords"], dtype=float)
            coords_b = np.array(data["end_coords"], dtype=float)
            vector = coords_b - coords_a
            length = np.linalg.norm(vector)

            # this makes the valve handle always point up
            angle = 0
            if vector[0] < 0:
                angle = -np.pi

            valve_info = data["valve_info"]
            outside_diameter, thickness, offset_y, offset_z, *_ = valve_info["body_section_parameters"]
            flange_outer_diameter, *_ = valve_info["flange_section_parameters"]
            flange_length = valve_info["flange_length"]

            source = valve_data(
                length,
                outside_diameter,
                thickness,
                flange_outer_diameter,
                flange_length,
                offset_y=offset_y,
                offset_z=offset_z,
            )

            # Every valve is different, thus we need a different function for each one.
            # Since the position and rotation are already handled by the function, we
            # pass the default values (0, 0, 0) and (1, 0, 0) for the add_symbol method.
            func = partial(
                align_vtk_geometry,
                source,
                coords_a,
                vector,
                angle,
            )

            self.add_symbol(
                func,
                (0, 0, 0),
                (1, 0, 0),
                color_names.PINK_6,
            )

    def configure_appearance(self):
        self.set_zbuffer_offsets(1, -6600)

        self.GetProperty().SetLineWidth(4)
        self.GetProperty().RenderLinesAsTubesOn()
        self.GetProperty().SetOpacity(0.7)
        self.GetProperty().SetAmbient(0.5)
        self.PickableOff()

    def set_zbuffer_offsets(self, factor: float, units: float):
        """
        This functions is usefull to make a object appear in front of the others.
        If the object should never be hidden, the parameters should be set to
        factor = 1 and offset = -6600.
        """
        mapper = self.GetMapper()
        mapper.SetResolveCoincidentTopologyToPolygonOffset()
        mapper.SetRelativeCoincidentTopologyLineOffsetParameters(factor, units)
        mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(factor, units)
        mapper.SetRelativeCoincidentTopologyPointOffsetParameter(units)
        mapper.Update()

    def _create_line(self, coords_a, coords_b):
        coords_a = np.array(coords_a)
        coords_b = np.array(coords_b)

        source = vtkLineSource()
        source.SetPoint1(coords_a)
        source.SetPoint2(coords_b)
        source.Update()

        return source.GetOutput()
