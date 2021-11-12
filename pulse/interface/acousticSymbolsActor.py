from pulse.interface.symbolsActor import SymbolsActorBase, SymbolTransform, loadSymbol

class AcousticNodesSymbolsActor(SymbolsActorBase):
    def _createConnections(self):
        return [
            (self._getAcousticPressure    ,   loadSymbol('data/symbols/prescribedPosition.obj')),
            (self._getVolumeVelocity      ,   loadSymbol('data/symbols/prescribedPosition.obj')),
            (self._getSpecificImpedance   ,   loadSymbol('data/symbols/prescribedPosition.obj')),
            (self._getRadiationImpedance  ,   loadSymbol('data/symbols/prescribedPosition.obj')),
            (self._getCompressor          ,   loadSymbol('data/symbols/prescribedPosition.obj')),
        ]
    
    def _createSequence(self):
        return self.project.get_nodes().values()

    def _getAcousticPressure(self, node):
        src = 8
        pos = node.coordinates
        rot = (0,0,0)
        scl = (1,1,1)
        col = (150,0,210) #violet
        symbols = []

        if node.acoustic_pressure is not None:
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols
    
    def _getVolumeVelocity(self, node):
        src = 7
        pos = node.coordinates
        rot = (0,0,0)
        scl = (1,1,1)
        col = (255,10,10)
        symbols = []

        if (node.volume_velocity is not None) and (node.compressor_excitation_table_names == []):
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols

    def _getSpecificImpedance(self, node):
        src = 9
        pos = node.coordinates
        rot = (0,0,0)
        scl = (1,1,1)
        col = (100,255,100)
        symbols = []

        if node.specific_impedance is not None:
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols
    
    def _getRadiationImpedance(self, node):
        src = 10
        pos = node.coordinates
        rot = (0,0,0)
        scl = (1,1,1)
        col = (224,0,75)
        symbols = []

        if node.radiation_impedance_type in [0,1,2]:
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols
        
    def _getCompressor(self, node):
        src = 12
        pos = node.coordinates
        rot = (0,0,0)
        scl = (1,1,1)
        col = (255,10,10)
        symbols = []

        if (node.volume_velocity is not None) and (node.compressor_excitation_table_names != []):
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols
    

class AcousticElementsSymbolsActor(SymbolsActorBase):
    def _createConnections(self):
        return [
            (self._getPerforatedPlate, loadSymbol('data/symbols/perforatedPlate.obj'))
        ]
    
    def _createSequence(self):
        return self.project.get_structural_elements().values()

    def _getPerforatedPlate(self, element):
        rad = 1
        acoustic = self.project.get_acoustic_element(element.index)

        if element.cross_section:
            if element.element_type in ['pipe_1', 'pipe_2']:
                rad = element.cross_section.inner_diameter / self.scaleFactor
                if rad == 0:
                    rad = 1

        src = 13
        pos = element.element_center_coordinates
        rot = element.section_rotation_xyz_undeformed
        scl = (1,rad,rad)
        col = (255,0,0)
        symbols = []

        if (acoustic.perforated_plate is not None):
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols
