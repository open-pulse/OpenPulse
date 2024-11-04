from pulse import app, SYMBOLS_DIR
from pulse.interface.viewer_3d.actors.symbols_actor import SymbolsActorBase, SymbolTransform, loadSymbol
from pulse.utils.common_utils import transformation_matrix_3x3

import numpy as np
from scipy.spatial.transform import Rotation
from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vtkmodules.vtkFiltersSources import vtkLineSource, vtkSphereSource

from pulse import SYMBOLS_DIR
from pulse.interface.viewer_3d.actors.symbols_actor import (
    SymbolsActorBase,
    SymbolTransform,
    loadSymbol,
)
from pulse.utils.common_utils import transformation_matrix_3x3


class AcousticNodesSymbolsActor(SymbolsActorBase):
    def _createConnections(self):
        return [
            (
                self._get_acoustic_pressure_symbol(),
                loadSymbol(SYMBOLS_DIR / "acoustic/acoustic_pressure.obj"),
            ),
            (
                self._get_volume_velocity_symbol(),
                loadSymbol(SYMBOLS_DIR / "acoustic/volume_velocity.obj"),
            ),
            (
                self._get_specific_impedance_symbol(),
                loadSymbol(SYMBOLS_DIR / "acoustic/specific_impedance.obj"),
            ),
            (
                self._get_radiation_impedance_symbol(),
                loadSymbol(SYMBOLS_DIR / "acoustic/radiation_impedance.obj"),
            ),
            (
                self._get_compressor_suction_symbol(),
                loadSymbol(SYMBOLS_DIR / "acoustic/compressor_suction.obj"),
            ),
            (
                self._get_compressor_discharge_symbol(),
                loadSymbol(SYMBOLS_DIR / "acoustic/compressor_discharge.obj"),
            ),
        ]

    def source(self):
        super().source()
        self._create_psd_acoustic_links()
        self._create_acoustic_transfer_element()

    # def _createSequence(self):
    #     return self.project.get_nodes().values()

    def _create_psd_acoustic_links(self):

        linkedSymbols = vtkAppendPolyData()

        for (property, *args), data in app().project.model.properties.nodal_properties.items():
            if property == "psd_acoustic_link":

                coords_a = np.array(data["coords"][:3], dtype=float)
                coords_b = np.array(data["coords"][3:], dtype=float)

                # divide the value of the coordinates by the scale factor
                source = vtkLineSource()
                source.SetPoint1(coords_a / self.scale_factor) 
                source.SetPoint2(coords_b / self.scale_factor)
                source.Update()
                linkedSymbols.AddInputData(source.GetOutput())
        
        s = vtkSphereSource()
        s.SetRadius(0)

        linkedSymbols.AddInputData(s.GetOutput())
        linkedSymbols.Update()

        index = len(self._connections)
        self._mapper.SetSourceData(index, linkedSymbols.GetOutput())
        self._sources.InsertNextTuple1(index)
        self._positions.InsertNextPoint(0, 0, 0)
        self._rotations.InsertNextTuple3(0, 0, 0)
        self._scales.InsertNextTuple3(1, 1, 1)
        self._colors.InsertNextTuple3(0, 250, 250)

    def _create_acoustic_transfer_element(self):

        linkedSymbols = vtkAppendPolyData()

        for (property, *args), data in app().project.model.properties.nodal_properties.items():
            if property == "acoustic_transfer_element":

                coords_a = np.array(data["coords"][:3], dtype=float)
                coords_b = np.array(data["coords"][3:], dtype=float)

                # divide the value of the coordinates by the scale factor
                source = vtkLineSource()
                source.SetPoint1(coords_a / self.scale_factor) 
                source.SetPoint2(coords_b / self.scale_factor)
                source.Update()
                linkedSymbols.AddInputData(source.GetOutput())

        s = vtkSphereSource()
        s.SetRadius(0)

        linkedSymbols.AddInputData(s.GetOutput())
        linkedSymbols.Update()

        index = len(self._connections)
        self._mapper.SetSourceData(index, linkedSymbols.GetOutput())
        self._sources.InsertNextTuple1(index)
        self._positions.InsertNextPoint(0, 0, 0)
        self._rotations.InsertNextTuple3(0, 0, 0)
        self._scales.InsertNextTuple3(1, 1, 1)
        self._colors.InsertNextTuple3(230, 110, 230)

    def _get_acoustic_pressure_symbol(self):

        src = 9
        rot = (0, 0, 0)
        scl = (1, 1, 1)
        col = (150, 0, 210)  # violet

        symbols = list()
        for (property, *args), data in app().project.model.properties.nodal_properties.items():

            if property == "acoustic_pressure":
                pos = data["coords"]
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        return symbols

    def _get_volume_velocity_symbol(self):

        src = 10
        rot = (0, 0, 0)
        scl = (1, 1, 1)
        col = (255, 10, 10)

        symbols = list()
        for (property, *args), data in app().project.model.properties.nodal_properties.items():

            if property == "volume_velocity":
                pos = data["coords"]
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        return symbols

    def _get_specific_impedance_symbol(self):

        src = 11
        rot = (0, 0, 0)
        scl = (1, 1, 1)
        col = (100, 255, 100)

        symbols = list()
        for (property, *args), data in app().project.model.properties.nodal_properties.items():

            if property == "specific_impedance":
                pos = data["coords"]
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        return symbols

    def _get_radiation_impedance_symbol(self):

        src = 12
        rot = (0, 0, 0)
        scl = (1, 1, 1)
        col = (224, 0, 75)

        symbols = list()
        for (property, *args), data in app().project.model.properties.nodal_properties.items():

            if property == "radiation_impedance":
                pos = data["coords"]
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        return symbols

    def _get_compressor_suction_symbol(self):

        src = 13
        rot = (0, 0, 0)
        scl = (1, 1, 1)
        col = (10, 10, 255)

        symbols = list()
        for (property, *args), data in app().project.model.properties.nodal_properties.items():

            if property == "compressor_excitation":

                if data["connection_type"] == "suction":

                    pos = data["coords"]
                    node_id = args[0]
                    node = app().project.preprocessor.nodes[node_id]

                    _elements = app().project.preprocessor.structural_elements_connected_to_node[node_id]

                    if len(_elements) == 1:
                        element = _elements[0]
                        rot = self.get_compressor_symbol_rotation(element, node)

                        if element.cross_section is not None:
                            diameter = element.cross_section.outer_diameter
                            factor = (diameter + 0.06) / self.scale_factor
                            scl = (factor, factor, factor)
                            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        return symbols  

    def _get_compressor_discharge_symbol(self):

        src = 14
        scl = (1, 1, 1)
        col = (255, 10, 10)

        symbols = list()
        for (property, *args), data in app().project.model.properties.nodal_properties.items():

            if property == "compressor_excitation":

                if data["connection_type"] == "discharge":

                    pos = data["coords"]
                    node_id = args[0]
                    node = app().project.preprocessor.nodes[node_id]
                    _elements = app().project.preprocessor.structural_elements_connected_to_node[node_id]

                    if len(_elements) == 1:
                        element = _elements[0]
                        rot = self.get_compressor_symbol_rotation(element, node)

                        if element.cross_section is not None:
                            diameter = element.cross_section.outer_diameter
                            factor = (diameter + 0.06) / self.scale_factor
                            scl = (factor, factor, factor)
                            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        return symbols  

    def get_compressor_symbol_rotation(self, element, node):
        if element.first_node == node:
            return element.section_rotation_xyz_undeformed

        else:
            rot_1 = transformation_matrix_3x3(-1, 0, 0)
            rot_2 = transformation_matrix_3x3(
                element.delta_x, element.delta_y, element.delta_z
            )
            mat_rot = rot_1 @ rot_2
            r = Rotation.from_matrix(mat_rot)
            rotations = -r.as_euler("zxy", degrees=True)
            rotations_xyz = np.array([rotations[1], rotations[2], rotations[0]]).T
            return rotations_xyz


class AcousticElementsSymbolsActor(SymbolsActorBase):

    def _createConnections(self):
        return [
            (
                self._get_perforated_plate_symbol(),
                loadSymbol(SYMBOLS_DIR / "acoustic/perforated_plate.obj"),
            )
        ]

    def _get_perforated_plate_symbol(self):

        src = 14
        col = (255, 0, 0)

        symbols = list()
        for (property, element_id), data in app().project.model.properties.element_properties.items():

            if property == "perforated_plate":

                if element_id in app().project.preprocessor.structural_elements.keys():
                    element = app().project.preprocessor.structural_elements[element_id]
                else:
                    return list()
            
                pos = element.center_coordinates
                rot = element.section_rotation_xyz_undeformed
    
                if element.valve_data:
                    d_in = element.valve_data["valve_effective_diameter"]
                    factor_yz = ((d_in / 2) / 0.1) / self.scale_factor
                else:
                    factor_yz = (element.cross_section.inner_diameter/0.1) / self.scale_factor

                factor_x = (element.perforated_plate.thickness/0.01) / self.scale_factor
                scl = (factor_x, factor_yz, factor_yz)

                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        return symbols
