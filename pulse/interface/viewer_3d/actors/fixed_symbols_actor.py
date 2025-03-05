from itertools import chain
from typing import Iterator

import numpy as np
from molde.colors import color_names
from molde.utils import set_polydata_colors
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from pulse import app
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

            coords_a = np.array(data["coords"][:3], dtype=float)
            coords_b = np.array(data["coords"][3:], dtype=float)

            source = vtkLineSource()
            source.SetPoint1(coords_a)
            source.SetPoint2(coords_b)
            source.Update()

            output = source.GetOutput()
            set_polydata_colors(output, color_names.GREEN.to_rgb())
            yield output

    def create_psd_structural_links(self) -> Iterator[vtkPolyData]:
        nodal_properties = app().project.model.properties.nodal_properties

        for (property_name, *args), data in nodal_properties.items():
            if property_name != "psd_structural_links":
                continue

            coords_a = np.array(data["coords"][:3], dtype=float)
            coords_b = np.array(data["coords"][3:], dtype=float)

            source = vtkLineSource()
            source.SetPoint1(coords_a)
            source.SetPoint2(coords_b)
            source.Update()

            output = source.GetOutput()
            set_polydata_colors(output, color_names.GREEN.to_rgb())
            yield output

    def create_psd_acoustic_links(self) -> Iterator[vtkPolyData]:
        nodal_properties = app().project.model.properties.nodal_properties

        for (property_name, *args), data in nodal_properties.items():
            if property_name != "psd_acoustic_link":
                continue

            coords_a = np.array(data["coords"][:3], dtype=float)
            coords_b = np.array(data["coords"][3:], dtype=float)

            source = vtkLineSource()
            source.SetPoint1(coords_a)
            source.SetPoint2(coords_b)
            source.Update()

            output = source.GetOutput()
            set_polydata_colors(output, color_names.BLUE.to_rgb())
            yield output

    def create_acoustic_transfer_element(self) -> Iterator[vtkPolyData]:
        nodal_properties = app().project.model.properties.nodal_properties

        for (property_name, *args), data in nodal_properties.items():
            if property_name != "acoustic_transfer_element":
                continue

            coords_a = np.array(data["coords"][:3], dtype=float)
            coords_b = np.array(data["coords"][3:], dtype=float)

            source = vtkLineSource()
            source.SetPoint1(coords_a)
            source.SetPoint2(coords_b)
            source.Update()

            output = source.GetOutput()
            set_polydata_colors(output, color_names.BLUE.to_rgb())
            yield output

    def create_perforated_plates(self) -> Iterator[vtkPolyData]:
        return []

    def create_valves(self) -> Iterator[vtkPolyData]:
        line_properties = app().project.model.properties.line_properties

        for line_id, data in line_properties.items():
            if "valve_info" not in data.keys():
                continue

            coords_a = np.array(data["start_coords"], dtype=float)
            coords_b = np.array(data["end_coords"], dtype=float)
            vector = coords_b - coords_a
            length = np.linalg.norm(vector)

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

            data = align_vtk_geometry(source, coords_a, vector)
            set_polydata_colors(data, color_names.PINK_6.to_rgb())
            yield data

    def configure_appearance(self):
        mapper = self.GetMapper()
        mapper.SetResolveCoincidentTopologyToPolygonOffset()
        mapper.SetRelativeCoincidentTopologyLineOffsetParameters(0, -66000)
        mapper.SetRelativeCoincidentTopologyPointOffsetParameter(-66000)
        mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(-1, 0)
        mapper.Update()

        self.GetProperty().SetAmbient(0.5)
        self.PickableOff()
