from pulse.interface.symbolsActor import SymbolsActorBase, SymbolTransform, loadSymbol


class AcousticNodesSymbolsActor(SymbolsActorBase):
    def _createConnections(self):
        return [
            (self._getAcousticPressure()    ,   loadSymbol('data/symbols/acousticPressure.obj')),
            (self._getVolumeVelocity()      ,   loadSymbol('data/symbols/volumeVelocity.obj')),
            (self._getSpecificImpedance()   ,   loadSymbol('data/symbols/specificImpedance.obj')),
            (self._getRadiationImpedance()  ,   loadSymbol('data/symbols/radiationImpedance.obj')),
            (self._getCompressor()          ,   loadSymbol('data/symbols/compressor_head.obj')),
        ]
    
    # def _createSequence(self):
    #     return self.project.get_nodes().values()

    def _getAcousticPressure(self):
        src = 9
        rot = (0,0,0)
        scl = (1,1,1)
        col = (150,0,210) #violet
        
        symbols = []
        for node in self.preprocessor.nodes_with_acoustic_pressure:
            pos = node.coordinates
            if node.acoustic_pressure is not None:
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols
    
    def _getVolumeVelocity(self):
        src = 10
        rot = (0,0,0)
        scl = (1,1,1)
        col = (255,10,10)

        symbols = []
        for node in self.preprocessor.nodes_with_volume_velocity:
            pos = node.coordinates 
            if (node.volume_velocity is not None) and (node.compressor_excitation_table_names == []):
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols

    def _getSpecificImpedance(self):
        src = 11
        rot = (0,0,0)
        scl = (1,1,1)
        col = (100,255,100)

        symbols = []
        for node in self.preprocessor.nodes_with_specific_impedance:
            pos = node.coordinates 
            if node.specific_impedance is not None:
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols
    
    def _getRadiationImpedance(self):
        src = 12
        rot = (0,0,0)
        scl = (1,1,1)
        col = (224,0,75)

        symbols = []
        for node in self.preprocessor.nodes_with_radiation_impedance:
            pos = node.coordinates 
            if node.radiation_impedance_type in [0,1,2]:
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols
        
    def _getCompressor(self):
        src = 13
        rot = (0,0,0)
        scl = (1,1,1)
        # col = (255,10,10)

        symbols = []
        for node in self.preprocessor.nodes_with_compressor_excitation:
            pos = node.coordinates
            if (node.volume_velocity is not None) and (node.compressor_excitation_table_names != []):
                element = self.project.preprocessor.elements_connected_to_node[node]
                # pos = element[0].element_center_coordinates
                rot = element[0].section_rotation_xyz_undeformed
                diameter = element[0].cross_section.outer_diameter
                factor = (diameter + 0.06) / self.scaleFactor
                scl = (factor, factor, factor)
                for connection_type in node.dict_index_to_compressor_connection_info.values():
                    if connection_type == "suction":
                        col = (10,10,255)
                    else:
                        col = (255,10,10) 
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols    


class AcousticElementsSymbolsActor(SymbolsActorBase):
    
    def _createConnections(self):
        return [
            (self._getPerforatedPlate(), loadSymbol('data/symbols/perforated_plate.obj'))
        ]
    
    # def _createSequence(self):
    #     return self.preprocessor.elements_with_perforated_plate
        # return self.project.get_structural_elements().values()

    def _getPerforatedPlate(self):
        src = 14
        col = (255,0,0)

        symbols = []
        for element in self.preprocessor.elements_with_perforated_plate:
            if element.perforated_plate:
            
                pos = element.element_center_coordinates
                rot = element.section_rotation_xyz_undeformed
    
                factor_x = (element.perforated_plate.thickness/0.01) / self.scaleFactor
                if element.valve_parameters:
                    outer_diameter = element.cross_section.outer_diameter
                    thickness = element.cross_section.thickness
                    inner_diameter = outer_diameter - 4*thickness                
                    factor_yz = ((inner_diameter/2)/0.1) / self.scaleFactor
                else:
                    factor_yz = (element.cross_section.inner_diameter/0.1) / self.scaleFactor
                
                scl = (factor_x, factor_yz, factor_yz)

                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        return symbols