from itertools import chain
from typing import Iterator

import numpy as np
from molde.colors import color_names
from molde.utils import set_polydata_colors, read_obj_file, transform_polydata

from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from pulse import app, SYMBOLS_DIR
from pulse.utils.cross_section_sources import valve_data
from pulse.utils.rotations import align_vtk_geometry


class FixedSymbolsActor(vtkActor):
    def __init__(self):
        super().__init__()
        self.build()
        self.configure_appearance()

    def build(self):
        mapper = vtkPolyDataMapper()
        source = vtkAppendPolyData()

        for symbol in chain(
            self.create_structural_links(),
            self.create_psd_structural_links(),
            self.create_perforated_plates(),
            self.create_valves(),
        ):
            source.AddInputData(symbol)

        source.Update()
        mapper.SetInputData(source.GetOutput())
        self.SetMapper(mapper)

    def create_structural_links(self) -> Iterator[vtkPolyData]:
        nodal_properties = app().project.model.properties.nodal_properties

        for (property_name, *args), data in nodal_properties.items():
            if property_name not in ["structural_stiffness_links", "structural_damping_links"]:
                continue

            yield self._create_line(
                data["coords"][:3],
                data["coords"][3:],
                color_names.GREEN,
            )

    def create_psd_structural_links(self) -> Iterator[vtkPolyData]:
        nodal_properties = app().project.model.properties.nodal_properties

        for (property_name, *args), data in nodal_properties.items():
            if property_name != "psd_structural_links":
                continue

            yield self._create_line(
                data["coords"][:3],
                data["coords"][3:],
                color_names.GREEN,
            )

    def create_psd_acoustic_links(self) -> Iterator[vtkPolyData]:
        nodal_properties = app().project.model.properties.nodal_properties

        for (property_name, *args), data in nodal_properties.items():
            if property_name != "psd_acoustic_link":
                continue

            yield self._create_line(
                data["coords"][:3],
                data["coords"][3:],
                color_names.BLUE,
            )

    def create_acoustic_transfer_element(self) -> Iterator[vtkPolyData]:
        nodal_properties = app().project.model.properties.nodal_properties

        for (property_name, *args), data in nodal_properties.items():
            if property_name != "acoustic_transfer_element":
                continue

            yield self._create_line(
                data["coords"][:3],
                data["coords"][3:],
                color_names.BLUE,
            )

    def create_perforated_plates(self) -> Iterator[vtkPolyData]:
        perforated_plate = read_obj_file(SYMBOLS_DIR / "acoustic/perforated_plate.obj")
        element_properties = app().project.model.properties.element_properties

        for (property_name, element_id), data in element_properties.items():
            if property_name != "perforated_plate":
                continue

            element = app().project.preprocessor.structural_elements.get(element_id)
            if element is None:
                continue

            # There must be a cleaner way, but I will just
            # copy this code from the previous version
            factor_x = element.perforated_plate.thickness / 0.01
            if element.valve_data:
                d_in = element.valve_data["valve_effective_diameter"]
                factor_yz = (d_in / 2) / 0.1
            else:
                factor_yz = element.cross_section.inner_diameter / 0.1
            factor_yz *= 1.5

            coord_a = element.first_node.coordinates
            coord_b = element.last_node.coordinates
            vector = coord_b - coord_a

            data = transform_polydata(
                perforated_plate,
                rotation=(0, 0, 90),
                scale=(factor_x, factor_yz, factor_yz),
            )
            data = align_vtk_geometry(data, coord_a, vector)
            set_polydata_colors(data, color_names.PINK_6.to_rgb())
            yield data

    def create_valves(self) -> Iterator[vtkPolyData]:
        line_properties = app().project.model.properties.line_properties

        for line_id, data in line_properties.items():
            if "valve_info" not in data.keys():
                continue

            coords_a = np.array(data["start_coords"], dtype=float)
            coords_b = np.array(data["end_coords"], dtype=float)
            vector = coords_b - coords_a
            length = np.linalg.norm(vector)

            # this makes the valve handle always point up
            angle = 0
            if vector[0] >= 0:
                angle = np.pi

            valve_info = data["valve_info"]
            outside_diameter, thickness, *_ = valve_info["body_section_parameters"]
            flange_outer_diameter, *_ = valve_info["flange_section_parameters"]
            flange_length = valve_info["flange_length"]

            source = valve_data(
                length,
                outside_diameter,
                thickness,
                flange_outer_diameter,
                flange_length,
            )

            data = align_vtk_geometry(source, coords_a, vector, angle)
            set_polydata_colors(data, color_names.PINK_6.to_rgb())
            yield data

    def configure_appearance(self):
        # This shows the points and lines over any other geometry
        # But the polygons get just a small priority to avoid
        # unexpected rendering
        mapper = self.GetMapper()
        mapper.SetResolveCoincidentTopologyToPolygonOffset()
        mapper.SetRelativeCoincidentTopologyLineOffsetParameters(0, -66000)
        mapper.SetRelativeCoincidentTopologyPointOffsetParameter(-66000)
        mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(-1, 0)
        mapper.Update()

        self.GetProperty().SetAmbient(0.5)
        self.PickableOff()

    def _create_line(self, coords_a, coords_b, color):
        coords_a = np.array(coords_a)
        coords_b = np.array(coords_a)

        source = vtkLineSource()
        source.SetPoint1(coords_a)
        source.SetPoint2(coords_b)
        source.Update()

        output = source.GetOutput()
        set_polydata_colors(output, color.to_rgb())
        return output
