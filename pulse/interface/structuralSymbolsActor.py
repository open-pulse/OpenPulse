import vtk
from pulse.interface.symbolsActor import SymbolsActorBase, SymbolTransform, loadSymbol
import numpy as np
from scipy.spatial.transform import Rotation

class StructuralNodesSymbolsActor(SymbolsActorBase):
    def _createConnections(self):
        return [
            (self._getPrescribedPositionSymbols() , loadSymbol('data/symbols/prescribedPosition.obj')),
            (self._getPrescribedRotationSymbols() , loadSymbol('data/symbols/prescribedRotation.obj')),
            (self._getNodalLoadForce()            , loadSymbol('data/symbols/nodalLoadPosition.obj')), 
            (self._getNodalLoadMoment()           , loadSymbol('data/symbols/nodalLoadRotation.obj')),
            (self._getLumpedMass()                , loadSymbol('data/symbols/lumpedMass.obj')),
            (self._getSpring()                    , loadSymbol('data/symbols/_spring.obj')),
            (self._getDamper()                    , loadSymbol('data/symbols/_damper.obj')),
        ]

    # def _createSequence(self):
    #     return self.project.get_nodes().values()

    def source(self):
        super().source()
        self._createNodalLinks()    # a very special case

    def _createNodalLinks(self):
        linkedNodes = set()
        linkedSymbols = vtk.vtkAppendPolyData()

        allnodes = self.project.get_nodes()

        # extract from string values that shoud be avaliable
        # create a set without useless repetitions 
        for node in allnodes.values():
            stif = tuple(node.elastic_nodal_link_stiffness.keys())
            damp = tuple(node.elastic_nodal_link_dampings.keys())
            if stif:
                nodes = sorted(int(i) for i in stif[0].split('-'))
            elif damp:
                nodes = sorted(int(i) for i in damp[0].split('-'))
            else:
                continue 
            linkedNodes.add(tuple(nodes))

        for a, b in linkedNodes:
            # divide the value of the coordinates by the scale factor
            source = vtk.vtkLineSource()
            source.SetPoint1(allnodes[a].coordinates / self.scaleFactor) 
            source.SetPoint2(allnodes[b].coordinates / self.scaleFactor)
            source.Update()
            linkedSymbols.AddInputData(source.GetOutput())
        
        s = vtk.vtkSphereSource()
        s.SetRadius(0)

        linkedSymbols.AddInputData(s.GetOutput())
        linkedSymbols.Update()

        index = len(self._connections)
        self._mapper.SetSourceData(index, linkedSymbols.GetOutput())
        self._sources.InsertNextTuple1(index)
        self._positions.InsertNextPoint(0,0,0)
        self._rotations.InsertNextTuple3(0,0,0)
        self._scales.InsertNextTuple3(1,1,1)
        self._colors.InsertNextTuple3(16,222,129)

    def _getPrescribedPositionSymbols(self):
        
        src = 1
        scl = (1,1,1)
        col = (0,255,0)
        offset = 0 * self.scaleFactor

        symbols = []
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

    def _getPrescribedRotationSymbols(self):
        
        src = 2
        scl = (1,1,1)
        col = (0,200,200)
        offset = 0 * self.scaleFactor

        symbols = []
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

    def _getNodalLoadForce(self):
        
        src = 3
        scl = (1,1,1)
        col = (255,0,0)
        offset = 0.05 * self.scaleFactor

        symbols = []
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

    def _getNodalLoadMoment(self):
        
        src = 4
        scl = (1,1,1)
        col = (0,0,255)
        offset = 0.05 * self.scaleFactor

        symbols = []
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

    def _getLumpedMass(self):

        src = 5
        rot = (0,0,0)
        scl = (1,1,1)
        col = (7,156,231)

        symbols = []
        for node in self.preprocessor.nodes_with_masses:
            pos = node.coordinates
            if any(node.lumped_masses):
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols

    def _getSpring(self):
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

        symbols = []
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

    def _getDamper(self):
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

        symbols = []
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
        elif np.real(value)>=0:
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
            (self._getValve(), loadSymbol('data/symbols/valve_symbol.obj'))
        ]
    
    # def _createSequence(self):
    #     return self.preprocessor.elements_with_valve
        # return self.project.get_structural_elements().values()
    
    def _getValve(self):
        src = 8
        col = (0,10,255)

        symbols = []
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

                    pos = center_coordinates
                    rot = element.section_rotation_xyz_undeformed
                    rotation = Rotation.from_euler('xyz', rot, degrees=True)
                    rot_matrix = rotation.as_matrix()
                    vector = [round(value, 5) for value in rot_matrix[:,1]]
                    if vector[1] < 0:
                        rot[0] += 180
                    factor_x = (element.valve_parameters["valve_length"]/0.247)/self.scaleFactor
                    factor_yz = (element.valve_parameters["valve_section_parameters"]["outer_diameter"]/0.130)/self.scaleFactor
                    # factor_yz = 1
                    scl = (factor_x, factor_yz, factor_yz)
                    symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        return symbols  