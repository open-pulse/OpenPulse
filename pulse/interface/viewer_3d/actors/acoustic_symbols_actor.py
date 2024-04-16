from pulse import SYMBOLS_DIR
from pulse.interface.viewer_3d.actors.symbols_actor import SymbolsActorBase, SymbolTransform, loadSymbol
from pulse.tools.utils import transformation_matrix_3x3

import numpy as np
from scipy.spatial.transform import Rotation

class AcousticNodesSymbolsActor(SymbolsActorBase):
    def _createConnections(self):
        return [(   self._get_acoustic_pressure_symbol(),   loadSymbol(SYMBOLS_DIR / 'acoustic/acoustic_pressure.obj')    ),
                (     self._get_volume_velocity_symbol(),   loadSymbol(SYMBOLS_DIR / 'acoustic/volume_velocity.obj')      ),
                (  self._get_specific_impedance_symbol(),   loadSymbol(SYMBOLS_DIR / 'acoustic/specific_impedance.obj')   ),
                ( self._get_radiation_impedance_symbol(),   loadSymbol(SYMBOLS_DIR / 'acoustic/radiation_impedance.obj')  ),
                (  self._get_compressor_suction_symbol(),   loadSymbol(SYMBOLS_DIR / 'acoustic/compressor_suction.obj')  ),
                (self._get_compressor_discharge_symbol(),   loadSymbol(SYMBOLS_DIR / 'acoustic/compressor_discharge.obj'))
            ]

    # def _createSequence(self):
    #     return self.project.get_nodes().values()

    def _get_acoustic_pressure_symbol(self):

        src = 9
        rot = (0,0,0)
        scl = (1,1,1)
        col = (150,0,210) #violet
        
        symbols = list()
        for node in self.preprocessor.nodes_with_acoustic_pressure:
            pos = node.coordinates
            if node.acoustic_pressure is not None:
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols
    
    def _get_volume_velocity_symbol(self):

        src = 10
        rot = (0,0,0)
        scl = (1,1,1)
        col = (255,10,10)

        symbols = list()
        for node in self.preprocessor.nodes_with_volume_velocity:
            pos = node.coordinates 
            if (node.volume_velocity is not None) and (node.compressor_excitation_table_names == list()):
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols

    def _get_specific_impedance_symbol(self):

        src = 11
        rot = (0,0,0)
        scl = (1,1,1)
        col = (100,255,100)

        symbols = list()
        for node in self.preprocessor.nodes_with_specific_impedance:
            pos = node.coordinates 
            if node.specific_impedance is not None:
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols
    
    def _get_radiation_impedance_symbol(self):

        src = 12
        rot = (0,0,0)
        scl = (1,1,1)
        col = (224,0,75)

        symbols = list()
        for node in self.preprocessor.nodes_with_radiation_impedance:
            pos = node.coordinates 
            if node.radiation_impedance_type in [0,1,2]:
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols
        
    def _get_compressor_suction_symbol(self):

        src = 13
        rot = (0,0,0)
        scl = (1,1,1)
        col = (10,10,255)

        symbols = list()
        for node in self.preprocessor.nodes_with_compressor_excitation:
            pos = node.coordinates
            if (node.volume_velocity is not None) and (node.compressor_excitation_table_names != list()):
                element = self.project.preprocessor.elements_connected_to_node[node]
                rot = self.get_compressor_symbol_rotation(element[0], node)
                if element[0].cross_section is not None:
                    diameter = element[0].cross_section.outer_diameter
                    factor = (diameter + 0.06) / self.scaleFactor
                    scl = (factor, factor, factor)
                    for connection_type in node.dict_index_to_compressor_connection_info.values():
                        if connection_type == "suction":
                            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols  

    def _get_compressor_discharge_symbol(self):

        src = 14
        scl = (1,1,1)
        col = (255,10,10)

        symbols = list()
        for node in self.preprocessor.nodes_with_compressor_excitation:
            pos = node.coordinates
            if (node.volume_velocity is not None) and (node.compressor_excitation_table_names != list()):
                element = self.project.preprocessor.elements_connected_to_node[node]
                rot = self.get_compressor_symbol_rotation(element[0], node)
                if element[0].cross_section is not None:
                    diameter = element[0].cross_section.outer_diameter
                    factor = (diameter + 0.06) / self.scaleFactor
                    scl = (factor, factor, factor)
                    for connection_type in node.dict_index_to_compressor_connection_info.values():
                        if connection_type == "discharge":
                            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols  

    def get_compressor_symbol_rotation(self, element, node):
        if element.first_node == node:
            return element.section_rotation_xyz_undeformed

        else:
            rot_1 = transformation_matrix_3x3(-1, 0, 0)
            rot_2 = transformation_matrix_3x3(element.delta_x, element.delta_y, element.delta_z)
            mat_rot = rot_1@rot_2
            r = Rotation.from_matrix(mat_rot)
            rotations = -r.as_euler('zxy', degrees=True)
            rotations_xyz = np.array([rotations[1], rotations[2], rotations[0]]).T
            return rotations_xyz


class AcousticElementsSymbolsActor(SymbolsActorBase):
    
    def _createConnections(self):
        return [(self._get_perforated_plate_symbol(), loadSymbol(SYMBOLS_DIR / 'acoustic/perforated_plate.obj'))]
    
    # def _createSequence(self):
    #     return self.preprocessor.elements_with_perforated_plate
        # return self.project.get_structural_elements().values()

    def _get_perforated_plate_symbol(self):

        src = 14
        col = (255,0,0)

        symbols = list()
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