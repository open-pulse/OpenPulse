from itertools import chain
from typing import Iterator

import numpy as np
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from pulse import app
from molde.utils import set_polydata_colors
from molde.colors import color_names


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

            coords = data["coords"]
            start = np.array(coords[:3], dtype=float)
            end = np.array(coords[3:], dtype=float)

            source = vtkLineSource()
            source.SetPoint1(start)
            source.SetPoint2(end)
            source.Update()

            output = source.GetOutput()
            set_polydata_colors(output, color_names.GREEN.to_rgb())
            yield output

    def create_psd_structural_links(self) -> Iterator[vtkPolyData]:
        return []

    def create_perforated_plates(self) -> Iterator[vtkPolyData]:
        return []

    def create_valves(self) -> Iterator[vtkPolyData]:
        return []

    def configure_appearance(self):
        self.set_zbuffer_offsets(1, -66000)
        self.GetProperty().SetAmbient(0.5)
        self.PickableOff()

    def set_zbuffer_offsets(self, factor: float, units: float):
        """
        This functions is usefull to make a object appear in front of the others.
        If the object should never be hidden, the parameters should be set to
        factor = 1 and offset = -66000.
        """
        mapper = self.GetMapper()
        mapper.SetResolveCoincidentTopologyToPolygonOffset()
        mapper.SetRelativeCoincidentTopologyLineOffsetParameters(factor, units)
        mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(factor, units)
        mapper.SetRelativeCoincidentTopologyPointOffsetParameter(units)
        mapper.Update()
