import vtk

from pulse import SYMBOLS_DIR
from pulse.interface.viewer_3d.actors.symbols_actor import SymbolsActorBase, SymbolTransform, loadSymbol

import numpy as np
from scipy.spatial.transform import Rotation

class StructuralNodesSymbolsActor(SymbolsActorBase):
    def _createConnections(self):
        return [(self._get_prescribed_displacement_symbol() , loadSymbol(SYMBOLS_DIR / 'structural/prescribed_displacement.obj')),
                (self._get_prescribed_rotation_symbol()     , loadSymbol(SYMBOLS_DIR / 'structural/prescribed_rotation.obj')),
                (self._get_nodal_force_symbol()             , loadSymbol(SYMBOLS_DIR / 'structural/nodal_force.obj')), 
                (self._get_nodal_moment_symbol()            , loadSymbol(SYMBOLS_DIR / 'structural/nodal_moment.obj')),
                (self._get_lumped_mass_symbol()             , loadSymbol(SYMBOLS_DIR / 'structural/lumped_mass.obj')),
                (self._get_lumped_spring_symbol()           , loadSymbol(SYMBOLS_DIR / 'structural/lumped_spring.obj')),
                (self._get_lumped_damper_symbol()           , loadSymbol(SYMBOLS_DIR / 'structural/lumped_damper.obj')),
                ]

    # def _createSequence(self):
    #     return self.project.get_nodes().values()

    def source(self):
        super().source()
        self._create_nodal_links()
        self._create_structural_links()

    def _create_nodal_links(self):

        linked_nodes = set()
        self.linked_symbols = vtk.vtkAppendPolyData()

        for key_s in self.project.preprocessor.nodes_with_elastic_link_stiffness.keys():
            node_ids = [int(node) for node in key_s.split("-")]
            linked_nodes.add(tuple(node_ids))

        for key_d in self.project.preprocessor.nodes_with_elastic_link_dampings.keys():
            node_ids = [int(node) for node in key_d.split("-")]
            linked_nodes.add(tuple(node_ids))

        nodes = self.project.preprocessor.nodes

        for a, b in linked_nodes:
            # divide the value of the coordinates by the scale factor
            source = vtk.vtkLineSource()
            source.SetPoint1(nodes[a].coordinates / self.scaleFactor) 
            source.SetPoint2(nodes[b].coordinates / self.scaleFactor)
            source.Update()
            self.linked_symbols.AddInputData(source.GetOutput())
        
        s = vtk.vtkSphereSource()
        s.SetRadius(0)

        self.linked_symbols.AddInputData(s.GetOutput())
        self.linked_symbols.Update()

        index = len(self._connections)
        self._mapper.SetSourceData(index, self.linked_symbols.GetOutput())
        self._sources.InsertNextTuple1(index)
        self._positions.InsertNextPoint(0,0,0)
        self._rotations.InsertNextTuple3(0,0,0)
        self._scales.InsertNextTuple3(1,1,1)
        self._colors.InsertNextTuple3(16,222,129)

    def _create_structural_links(self):

        nodes = self.preprocessor.nodes

        for (a, b) in self.preprocessor.nodes_with_structural_links.keys():
            # divide the value of the coordinates by the scale factor
            source = vtk.vtkLineSource()
            source.SetPoint1(nodes[a].coordinates / self.scaleFactor) 
            source.SetPoint2(nodes[b].coordinates / self.scaleFactor)
            source.Update()
            self.linked_symbols.AddInputData(source.GetOutput())

        s = vtk.vtkSphereSource()
        s.SetRadius(0)

        self.linked_symbols.AddInputData(s.GetOutput())
        self.linked_symbols.Update()

        index = len(self._connections)
        self._mapper.SetSourceData(index, self.linked_symbols.GetOutput())
        self._sources.InsertNextTuple1(index)
        self._positions.InsertNextPoint(0,0,0)
        self._rotations.InsertNextTuple3(0,0,0)
        self._scales.InsertNextTuple3(1,1,1)
        self._colors.InsertNextTuple3(10,0,10)

    def _get_prescribed_displacement_symbol(self):
        
        src = 1
        scl = (1,1,1)
        col = (0,255,0)
        offset = 0 * self.scaleFactor

        symbols = list()
        for node in self.preprocessor.nodes_with_prescribed_dofs:

            x,y,z = self._getCoords(node)
            mask = [(i is not None) for i in node.getStructuralBondaryCondition()[:3]]
            values = list(node.getStructuralBondaryCondition()[:3])

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
        scl = (1,1,1)
        col = (0,200,200)
        offset = 0 * self.scaleFactor

        symbols = list()
        for node in self.preprocessor.nodes_with_prescribed_dofs:

            x,y,z = self._getCoords(node)
            mask = [(i is not None) for i in node.getStructuralBondaryCondition()[3:]]
            values = list(node.getStructuralBondaryCondition()[3:])
            
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
                    rot = (90,0,0)
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        
        return symbols

    def _get_nodal_force_symbol(self):
        
        src = 3
        scl = (1,1,1)
        col = (255,0,0)
        offset = 0.05 * self.scaleFactor

        symbols = list()
        for node in self.preprocessor.nodes_with_nodal_loads:

            x,y,z = self._getCoords(node)
            mask = [(i is not None) for i in node.get_prescribed_loads()[:3]]
            values = list(node.get_prescribed_loads()[:3])
            
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
        scl = (1,1,1)
        col = (0,0,255)
        offset = 0.05 * self.scaleFactor

        symbols = list()
        for node in self.preprocessor.nodes_with_nodal_loads:

            x,y,z = self._getCoords(node)
            values = list(node.get_prescribed_loads()[:3])
            mask = [(i is not None) for i in node.get_prescribed_loads()[3:]]
            
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
                    rot = (90,0,0)
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        
        return symbols

    def _get_lumped_mass_symbol(self):

        src = 5
        rot = (0,0,0)
        scl = (1,1,1)
        col = (7,156,231)

        symbols = list()
        for node in self.preprocessor.nodes_with_masses:
            pos = node.coordinates
            if any(node.lumped_masses):
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols

    def _get_lumped_spring_symbol(self):

        e_size = self.project.file._element_size
        length = self.scaleFactor/2

        if self.scaleFactor/2 > 4*e_size:
            f = 2
        elif self.scaleFactor/2 > 2*e_size:
            f = 1
        elif self.scaleFactor/2 > e_size/2:
            f = 0.5
        else:
            f = 0.25

        delta_x = 0.14 + f*e_size*1.19/length
        offset = delta_x*length/1.19
        
        src = 6
        scale_x = (length/1.19)/self.scaleFactor
        scl = (scale_x, scale_x, scale_x)
        col = (242,121,0)

        symbols = list()
        for node in self.preprocessor.nodes_connected_to_springs:
            x,y,z = self._getCoords(node)
            mask = [(i is not None) for i in node.get_lumped_stiffness()[:3]]

            if mask[0]:
                pos = (x-offset, y, z)
                rot = (0,0,0)
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

            if mask[1]:
                pos = (x, y-offset, z)
                rot = (0,0,90)
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

            if mask[2]:
                pos = (x, y, z-offset)
                rot = (0,-90,0)
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        
        return symbols

    def _get_lumped_damper_symbol(self):

        e_size = self.project.file._element_size
        length = self.scaleFactor/2

        if self.scaleFactor/2 > 4*e_size:
            f = 2
        elif self.scaleFactor/2 > 2*e_size:
            f = 1
        elif self.scaleFactor/2 > e_size/2:
            f = 0.5
        else:
            f = 0.25

        delta_x = 0.14 + f*e_size*1.19/length
        offset = delta_x*length/1.19

        src = 7
        scale_x = (length/1.19)/self.scaleFactor
        scl = (scale_x, scale_x, scale_x)
        col = (255,0,100)

        symbols = list()
        for node in self.preprocessor.nodes_connected_to_dampers:
            x,y,z = self._getCoords(node)
            mask = [(i is not None) for i in node.get_lumped_dampings()[:3]]

            if mask[0]:
                pos = (x-offset, y, z)
                rot = (0,0,0)
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

            if mask[1]:
                pos = (x, y-offset, z)
                rot = (0,0,90)
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

            if mask[2]:
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
        return [(self._get_valve_symbol(), loadSymbol(SYMBOLS_DIR / 'structural/valve_symbol.obj'))]
    
    # def _createSequence(self):
    #     return self.preprocessor.elements_with_valve
        # return self.project.get_structural_elements().values()
    
    def _get_valve_symbol(self):

        src = 8
        col = (0,10,255)

        symbols = list()
        for element in self.preprocessor.elements_with_valve:
            if element.valve_parameters:

                center_coordinates = element.valve_parameters["valve_center_coordinates"]
                valve_elements = element.valve_parameters["valve_elements"]

                if np.remainder(len(valve_elements), 2) == 0:
                    index = int(len(valve_elements)/2)
                    center_element = valve_elements[index]
                else:
                    index = int((len(valve_elements)-1)/2) + 1
                    center_element = valve_elements[index]
                
                if center_element == element.index:

                    rot = element.section_rotation_xyz_undeformed
                    rotation = Rotation.from_euler('xyz', rot, degrees=True)
                    rot_matrix = rotation.as_matrix()
                    
                    vector = [round(value, 5) for value in rot_matrix[:, 1]]
                    if vector[1] < 0:
                        rot[0] += 180
                    
                    factor_x = (element.valve_parameters["valve_length"]/0.247)/self.scaleFactor
                    factor_yz = (element.valve_parameters["valve_section_parameters"][0]/0.130)/self.scaleFactor
                    
                    # factor_yz = 1
                    pos = center_coordinates
                    scl = (factor_x, factor_yz, factor_yz)
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        return symbols