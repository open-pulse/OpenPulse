from pulse import app, SYMBOLS_DIR
from pulse.interface.viewer_3d.actors.symbols_actor import SymbolsActorBase, SymbolTransform, loadSymbol

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


class StructuralNodesSymbolsActor(SymbolsActorBase):
    def _createConnections(self):
        return [
            (
                self._get_prescribed_displacement_symbol(),
                loadSymbol(SYMBOLS_DIR / "structural/prescribed_displacement.obj"),
            ),
            (
                self._get_prescribed_rotation_symbol(),
                loadSymbol(SYMBOLS_DIR / "structural/prescribed_rotation.obj"),
            ),
            (
                self._get_nodal_force_symbol(),
                loadSymbol(SYMBOLS_DIR / "structural/nodal_force.obj"),
            ),
            (
                self._get_nodal_moment_symbol(),
                loadSymbol(SYMBOLS_DIR / "structural/nodal_moment.obj"),
            ),
            (
                self._get_lumped_mass_symbol(),
                loadSymbol(SYMBOLS_DIR / "structural/lumped_mass.obj"),
            ),
            (
                self._get_lumped_spring_symbol(),
                loadSymbol(SYMBOLS_DIR / "structural/lumped_spring.obj"),
            ),
            (
                self._get_lumped_damper_symbol(),
                loadSymbol(SYMBOLS_DIR / "structural/lumped_damper.obj"),
            ),
        ]

    # def _createSequence(self):
    #     return self.project.get_nodes().values()

    def source(self):
        super().source()
        self._create_psd_structural_links()
        self._create_structural_links()

    def _create_psd_structural_links(self):

        linked_nodes = set()
        self.linked_symbols = vtkAppendPolyData()

        for (_property, *args), data in app().project.model.properties.nodal_properties.items():

            if _property == "psd_structural_links":

                node_a, node_b = args
                linked_nodes.add((node_a, node_b))

                coords_a = np.array(data["coords"][:3], dtype=float)
                coords_b = np.array(data["coords"][3:], dtype=float)

                # divide the value of the coordinates by the scale factor
                source = vtkLineSource()
                source.SetPoint1(coords_a / self.scale_factor) 
                source.SetPoint2(coords_b / self.scale_factor)
                source.Update()
                self.linked_symbols.AddInputData(source.GetOutput())

        s = vtkSphereSource()
        s.SetRadius(0)

        self.linked_symbols.AddInputData(s.GetOutput())
        self.linked_symbols.Update()

        index = len(self._connections)
        self._mapper.SetSourceData(index, self.linked_symbols.GetOutput())
        self._sources.InsertNextTuple1(index)
        self._positions.InsertNextPoint(0, 0, 0)
        self._rotations.InsertNextTuple3(0, 0, 0)
        self._scales.InsertNextTuple3(1, 1, 1)
        self._colors.InsertNextTuple3(16, 222, 129)

    def _create_structural_links(self):

        for (_property, *args), data in app().project.model.properties.nodal_properties.items():

            if _property in ["structural_stiffness_links", "structural_damping_links"]:

                coords = data["coords"]
                coords_a = np.array(coords[:3], dtype=float)
                coords_b = np.array(coords[3:], dtype=float)

                # divide the value of the coordinates by the scale factor
                source = vtkLineSource()
                source.SetPoint1(coords_a / self.scale_factor) 
                source.SetPoint2(coords_b / self.scale_factor)
                source.Update()
                self.linked_symbols.AddInputData(source.GetOutput())

        s = vtkSphereSource()
        s.SetRadius(0)

        self.linked_symbols.AddInputData(s.GetOutput())
        self.linked_symbols.Update()

        index = len(self._connections)
        self._mapper.SetSourceData(index, self.linked_symbols.GetOutput())
        self._sources.InsertNextTuple1(index)
        self._positions.InsertNextPoint(0, 0, 0)
        self._rotations.InsertNextTuple3(0, 0, 0)
        self._scales.InsertNextTuple3(1, 1, 1)
        self._colors.InsertNextTuple3(10, 0, 10)

    def _get_prescribed_displacement_symbol(self):

        src = 1
        scl = (1, 1, 1)
        col = (0, 255, 0)
        offset = 0 * self.scale_factor

        symbols = list()
        for (property, *args), data in app().project.model.properties.nodal_properties.items():

            if property == "prescribed_dofs":

                x, y, z = data["coords"]
                values = data["values"]
                mask = [(i is not None) for i in values]

                if mask[0]:
                    pos = (x-offset, y, z)
                    rot = (0,0,90)
                    if self.is_value_negative(values[0]):
                        pos = (x-offset, y, z)
                        rot = (0,0,-90)
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

                if mask[1]:
                    pos = (x, y-offset, z)
                    rot = (180,90,0)
                    if self.is_value_negative(values[1]):
                        pos = (x, y+offset, z)
                        rot = (180,90,180)
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

                if mask[2]:
                    pos = (x, y, z-offset)
                    rot = (-90,0,0)
                    if self.is_value_negative(values[2]):
                        pos = (x, y, z+offset)
                        rot = (90,0,0)
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        
        return symbols

    def _get_prescribed_rotation_symbol(self):

        src = 2
        scl = (1, 1, 1)
        col = (0, 200, 200)
        offset = 0 * self.scale_factor

        symbols = list()
        for (property, *args), data in app().project.model.properties.nodal_properties.items():

            if property == "prescribed_dofs":

                x, y, z = data["coords"]
                values = data["values"]
                mask = [(i is not None) for i in values]

                if mask[3]:
                    pos = (x-offset, y, z)
                    rot = (0,0,90)
                    if self.is_value_negative(values[3]):
                        pos = (x+offset, y, z)
                        rot = (0,0,-90)
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

                if mask[4]:
                    pos = (x, y-offset, z)
                    rot = (180,90,0)
                    if self.is_value_negative(values[4]):
                        pos = (x, y+offset, z)
                        rot = (180,90,180)
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

                if mask[5]:
                    pos = (x, y, z-offset)
                    rot = (-90,0,0)
                    if self.is_value_negative(values[5]):
                        pos = (x, y, z+offset)
                        rot = (90,0,0)
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        return symbols

    def _get_nodal_force_symbol(self):

        src = 3
        scl = (1, 1, 1)
        col = (255, 0, 0)
        offset = 0.05 * self.scale_factor

        symbols = list()
        for (property, *args), data in app().project.model.properties.nodal_properties.items():

            if property == "nodal_loads":

                x, y, z = data["coords"]
                values = data["values"]
                mask = [(i is not None) for i in values]

                if mask[0]:
                    pos = (x-offset, y, z)
                    rot = (0,0,90)
                    if self.is_value_negative(values[0]):
                        pos = (x+offset, y, z)
                        rot = (0,0,-90)
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

                if mask[1]:
                    pos = (x, y-offset, z)
                    rot = (180,90,0)
                    if self.is_value_negative(values[1]):
                        pos = (x, y+offset, z)
                        rot = (180,90,180)
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

                if mask[2]:
                    pos = (x, y, z-offset)
                    rot = (-90,0,0)
                    if self.is_value_negative(values[2]):
                        pos = (x, y, z+offset)
                        rot = (90,90,0)
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        return symbols

    def _get_nodal_moment_symbol(self):

        src = 4
        scl = (1, 1, 1)
        col = (0, 0, 255)
        offset = 0.05 * self.scale_factor

        symbols = list()
        for (property, *args), data in app().project.model.properties.nodal_properties.items():

            if property == "nodal_loads":

                x, y, z = data["coords"]
                values = data["values"]
                mask = [(i is not None) for i in values]

                if mask[3]:
                    pos = (x-offset, y, z)
                    rot = (0,0,90)
                    if self.is_value_negative(values[3]):
                        pos = (x+offset, y, z)
                        rot = (0,0,-90)
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

                if mask[4]:
                    pos = (x, y-offset, z)
                    rot = (180,90,0)
                    if self.is_value_negative(values[4]):
                        pos = (x, y+offset, z)
                        rot = (180,90,180)
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

                if mask[5]:
                    pos = (x, y, z-offset)
                    rot = (-90,0,0)
                    if self.is_value_negative(values[5]):
                        pos = (x, y, z+offset)
                        rot = (90,0,0)
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        return symbols

    def _get_lumped_mass_symbol(self):

        src = 5
        rot = (0, 0, 0)
        scl = (1, 1, 1)
        col = (7, 156, 231)

        symbols = list()
        for (property, *args), data in app().project.model.properties.nodal_properties.items():

            if property == "lumped_masses":

                pos = data["coords"]
                values = data["values"]
                mask = [(i is not None) for i in values]

                if sum(mask):
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        return symbols

    def _get_lumped_spring_symbol(self):

        e_size = app().project.preprocessor.mesh.element_size
        length = self.scale_factor/2

        if self.scale_factor / 2 > 4 * e_size:
            f = 2
        elif self.scale_factor / 2 > 2 * e_size:
            f = 1
        elif self.scale_factor / 2 > e_size / 2:
            f = 0.5
        else:
            f = 0.25

        delta_x = 0.14 + f * e_size * 1.19 / length
        offset = delta_x * length / 1.19

        src = 6
        scale_x = (length / 1.19) / self.scale_factor
        scl = (scale_x, scale_x, scale_x)
        col = (242, 121, 0)

        symbols = list()
        for (property, *args), data in app().project.model.properties.nodal_properties.items():

            if property == "lumped_stiffness":

                x, y, z = data["coords"]
                values = data["values"]
                mask = [(i is not None) for i in values]

                if mask[0] or mask[3]:
                    pos = (x-offset, y, z)
                    rot = (0,0,0)
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

                if mask[1] or mask[4]:
                    pos = (x, y-offset, z)
                    rot = (0,0,90)
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

                if mask[2] or mask[5]:
                    pos = (x, y, z-offset)
                    rot = (0,-90,0)
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        return symbols

    def _get_lumped_damper_symbol(self):

        e_size = app().project.preprocessor.mesh.element_size
        length = self.scale_factor/2

        if self.scale_factor / 2 > 4 * e_size:
            f = 2
        elif self.scale_factor / 2 > 2 * e_size:
            f = 1
        elif self.scale_factor / 2 > e_size / 2:
            f = 0.5
        else:
            f = 0.25

        delta_x = 0.14 + f * e_size * 1.19 / length
        offset = delta_x * length / 1.19

        src = 7
        scale_x = (length / 1.19) / self.scale_factor
        scl = (scale_x, scale_x, scale_x)
        col = (255, 0, 100)

        symbols = list()
        for (property, *args), data in app().project.model.properties.nodal_properties.items():

            if property == "lumped_dampings":

                x, y, z = data["coords"]
                values = data["values"]
                mask = [(i is not None) for i in values]

                if mask[0] or mask[3]:
                    pos = (x-offset, y, z)
                    rot = (0,0,0)
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

                if mask[1] or mask[4]:
                    pos = (x, y-offset, z)
                    rot = (0,0,90)
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

                if mask[2] or mask[5]:
                    pos = (x, y, z-offset)
                    rot = (0,-90,0)
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        return symbols

    def is_value_negative(self, value):
        if isinstance(value, np.ndarray):
            return False
        elif np.real(value) >= 0:
            return False
        else:
            return True

    def _getCoords(self, node):
        if self.deformed:
            return node.deformed_coordinates
        else:
            return node.coordinates


class StructuralElementsSymbolsActor(SymbolsActorBase):

    def _createConnections(self):
        return [
            (
                self._get_valve_symbol(),
                loadSymbol(SYMBOLS_DIR / "structural/valve_symbol.obj"),
            )
        ]

    # def _createSequence(self):
    #     return self.preprocessor.elements_with_valve
    # return self.project.get_structural_elements().values()

    def _get_valve_symbol(self):

        src = 8
        col = (0, 10, 255)

        symbols = list()

        for line_id, data in app().project.model.properties.line_properties.items():

            start_coords = data["start_coords"]
            end_coords = data["end_coords"]

            if "valve_info" in data.keys():

                A = np.array(start_coords, dtype=float)
                B = np.array(end_coords, dtype=float) 

                valve_length = np.linalg.norm(B - A)
                center_coordinates = (B + A) / 2

                if line_id in app().project.model.mesh.line_to_elements.keys():
                    valve_elements = app().project.model.mesh.line_to_elements[line_id]
                else:
                    return list()

                diameter, *_ = data["valve_info"]["body_section_parameters"]

                if np.remainder(len(valve_elements), 2) == 0:
                    index = int(len(valve_elements) / 2)
                    element_id = valve_elements[index]
                else:
                    index = int((len(valve_elements) - 1) / 2) + 1
                    element_id = valve_elements[index]

                element = app().project.preprocessor.structural_elements[element_id]

                rot = element.section_rotation_xyz_undeformed
                rotation = Rotation.from_euler("xyz", rot, degrees=True)
                rot_matrix = rotation.as_matrix()

                vector = [round(value, 5) for value in rot_matrix[:, 1]]
                if vector[1] < 0:
                    rot[0] += 180

                factor_x = (valve_length / 0.247) / self.scale_factor
                factor_yz = (diameter / 0.130) / self.scale_factor

                # factor_yz = 1
                pos = center_coordinates
                scl = (factor_x, factor_yz, factor_yz)
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        return symbols