import vtk
from pulse.interface.symbolsActor import SymbolsActorBase, SymbolTransform, loadSymbol

class StructuralNodesSymbolsActor(SymbolsActorBase):
    def _createConnections(self):
        return [
            (self._getPrescribedPositionSymbols , loadSymbol('data/symbols/prescribedPosition.obj')),
            (self._getPrescribedRotationSymbols , loadSymbol('data/symbols/prescribedRotation.obj')),
            (self._getNodalLoadForce            , loadSymbol('data/symbols/nodalLoadPosition.obj')), 
            (self._getNodalLoadMoment           , loadSymbol('data/symbols/nodalLoadRotation.obj')),
            (self._getLumpedMass                , loadSymbol('data/symbols/lumpedMass.obj')),
            (self._getSpring                    , loadSymbol('data/symbols/spring.obj')),
            (self._getDamper                    , loadSymbol('data/symbols/damper.obj')),
        ]

    def _createSequence(self):
        return self.project.get_nodes().values()

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

    def _getPrescribedPositionSymbols(self, node):
        offset = 0 * self.scaleFactor
        x,y,z = self._getCoords(node)
        src = 1
        scl = (1,1,1)
        col = (0,255,0)

        symbols = []
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

    def _getPrescribedRotationSymbols(self, node):
        offset = 0 * self.scaleFactor
        x,y,z = self._getCoords(node)
        src = 2
        scl = (1,1,1)
        col = (0,200,200)

        symbols = []
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

    def _getNodalLoadForce(self, node):
        offset = 0.05 * self.scaleFactor
        x,y,z = self._getCoords(node)
        src = 3
        scl = (1,1,1)
        col = (255,0,0)

        symbols = []
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

    def _getNodalLoadMoment(self, node):
        offset = 0.05 * self.scaleFactor
        x,y,z = self._getCoords(node)
        src = 4
        scl = (1,1,1)
        col = (0,0,255)

        symbols = []
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

    def _getLumpedMass(self, node):
        src = 11
        pos = node.coordinates
        rot = (0,0,0)
        scl = (1,1,1)
        col = (7,156,231)
        symbols = []

        if any(node.lumped_masses):
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols

    def _getSpring(self, node):
        offset = 0.62 * self.scaleFactor
        x,y,z = self._getCoords(node)
        src = 6
        scl = (1,1,1)
        col = (242,121,0)

        symbols = []
        # mask = node.get_lumped_stiffness()[:3]
        mask = [(i is not None) for i in node.get_lumped_stiffness()[:3]]

        if mask[0]:
            pos = (x-offset, y, z)
            rot = (180,0,90)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        if mask[1]:
            pos = (x, y-offset, z)
            rot = (0,0,0)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        if mask[2]:
            pos = (x, y, z-offset)
            rot = (90,0,0)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        
        return symbols

    def _getDamper(self, node):
        offset = 0.62 * self.scaleFactor
        x,y,z = self._getCoords(node)
        src = 5
        scl = (1,1,1)
        col = (255,0,100)

        symbols = []
        # mask = node.get_lumped_dampings()[:3]
        mask = [(i is not None) for i in node.get_lumped_dampings()[:3]]

        if mask[0]:
            pos = (x-offset, y, z)
            rot = (180,0,90)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        if mask[1]:
            pos = (x, y-offset, z)
            rot = (0,0,0)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        if mask[2]:
            pos = (x, y, z-offset)
            rot = (90,0,0)
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
    # I think we dont have nothing to see here, but I will let it here because who knows
    def _createConnections(self):
        return []

    def _createSequence(self):
        return []


    def _getValve(self, element):
        src = 11
        pos = element.element_center_coordinates
        rot = (0,0,0)
        scl = (1,1,1)
        col = (7,156,231)
        symbols = []

        if any(element.valve_data):
            rot = element.section_rotation_xyz_undeformed
            rotation = Rotation.from_euler('xyz', rot, degrees=True)
            rot_matrix = rotation.as_matrix()
            vector = [round(value, 5) for value in rot_matrix[:,1]]
            if vector[1] < 0:
                rot[0] += 180
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols        
