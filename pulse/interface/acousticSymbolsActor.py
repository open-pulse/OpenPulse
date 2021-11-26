from pulse.interface.symbolsActor import SymbolsActorBase, SymbolTransform, loadSymbol


class AcousticNodesSymbolsActor(SymbolsActorBase):
    def _createConnections(self):
        return [
            (self._getAcousticPressure    ,   loadSymbol('data/symbols/acousticPressure.obj')),
            (self._getVolumeVelocity      ,   loadSymbol('data/symbols/volumeVelocity.obj')),
            (self._getSpecificImpedance   ,   loadSymbol('data/symbols/specificImpedance.obj')),
            (self._getRadiationImpedance  ,   loadSymbol('data/symbols/radiationImpedance.obj')),
            (self._getCompressor          ,   loadSymbol('data/symbols/compressor.obj')),
        ]
    
    def _createSequence(self):
        return self.project.get_nodes().values()

    def _getAcousticPressure(self, node):
        src = 9
        pos = node.coordinates
        rot = (0,0,0)
        scl = (1,1,1)
        col = (150,0,210) #violet
        symbols = []

        if node.acoustic_pressure is not None:
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols
    
    def _getVolumeVelocity(self, node):
        src = 10
        pos = node.coordinates
        rot = (0,0,0)
        scl = (1,1,1)
        col = (255,10,10)
        symbols = []

        if (node.volume_velocity is not None) and (node.compressor_excitation_table_names == []):
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols

    def _getSpecificImpedance(self, node):
        src = 11
        pos = node.coordinates
        rot = (0,0,0)
        scl = (1,1,1)
        col = (100,255,100)
        symbols = []

        if node.specific_impedance is not None:
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols
    
    def _getRadiationImpedance(self, node):
        src = 12
        pos = node.coordinates
        rot = (0,0,0)
        scl = (1,1,1)
        col = (224,0,75)
        symbols = []

        if node.radiation_impedance_type in [0,1,2]:
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols
        
    def _getCompressor(self, node):
        src = 13
        pos = node.coordinates
        rot = (0,0,0)
        scl = (1,1,1)
        col = (255,10,10)
        symbols = []

        if (node.volume_velocity is not None) and (node.compressor_excitation_table_names != []):
            element = self.project.preprocessor.elements_connected_to_node[node]
            pos = element[0].element_center_coordinates
            rot = element[0].section_rotation_xyz_undeformed
            scl = (0.5,0.5,0.5)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols    


class AcousticElementsSymbolsActor(SymbolsActorBase):
    def _createConnections(self):
        return [
            (self._getPerforatedPlate, loadSymbol('data/symbols/perforated_plate.obj'))
        ]
    
    def _createSequence(self):
        return self.project.get_structural_elements().values()

    def _getPerforatedPlate(self, element):
        src = 14
        col = (255,0,0)
        symbols = []

        if element.perforated_plate:
        
            pos = element.element_center_coordinates
            rot = element.section_rotation_xyz_undeformed
   
            factor_x = (element.perforated_plate.thickness/0.01) / self.scaleFactor
            factor_yz = (element.cross_section.inner_diameter/0.1) / self.scaleFactor
            scl = (factor_x, factor_yz, factor_yz)

            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        return symbols