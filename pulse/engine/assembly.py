import numpy as np
import time
from scipy.sparse import coo_matrix, csr_matrix, csc_matrix
from collections import deque

from pulse.engine.node import Node
from pulse.engine.tube import TubeCrossSection
from pulse.engine.material import Material
from pulse.engine.element import Element

class Assembly:
    """ Assembly  

    Parameters
    ----------
    nodal_coordinates : 
        
    connectivity : 
        
    fixed_nodes : 
        
    material_list : 

    cross_section_list : 
        
    element_type_list : pipe16, pipe288
        Element type identifier.
    """
    def __init__(   self,
                    nodal_coordinates,
                    connectivity,
                    fixed_nodes,
                    dofs_fixed_node,
                    dofs_fixed_value,
                    material_list,
                    material_dictionary,
                    cross_section_list,
                    cross_section_dictionary,
                    element_type_dictionary):
        self.nodal_coordinates = nodal_coordinates
        self.connectivity = connectivity
        self.fixed_nodes = fixed_nodes
        self.dofs_fixed_node = dofs_fixed_node   
        self.dofs_fixed_value = dofs_fixed_value            
        self.material_list = material_list 
        self.material_dictionary = material_dictionary 
        self.cross_section_list = cross_section_list
        self.cross_section_dictionary = cross_section_dictionary
        self.element_type_dictionary = element_type_dictionary

    def number_nodes(self):
        """ Total number of nodes on the mesh."""
        return self.nodal_coordinates.shape[0]
    
    def nodes_user_index(self):
        """ Array with all node user index."""
        return self.nodal_coordinates[:,0].astype(int)
    
    def nodes_internal_index(self):
        """ Array with all node internal index."""
        return np.arange( self.number_nodes() )
    
    def node_internal_to_user_index(self):
        """ Dictionary ."""
        return {i:self.nodes_user_index()[i] for i in self.nodes_internal_index()}
    
    def node_user_to_internal_index(self):
        """ Dictionary ."""
        return { j:i for i, j in self.node_internal_to_user_index().items() }
       
    def dofs_fixed(self):
        """ Global index of every fixed degree of freedom."""
        dictionary = self.node_user_to_internal_index()
        dofs_fixed = deque()

        for i, user_index in enumerate(self.fixed_nodes):
            index = dictionary[user_index]
            dofs_fixed.extend( index * Node.degree_freedom + self.dofs_fixed_node[i] )

        return dofs_fixed
        
    def dofs_prescribed_values(self):
        """ Dictionary ."""
        count = 0
        dofs_presc = self.dofs_fixed()
        dofs_prescribed_values = {}
        for i in range(self.fixed_nodes.shape[0]):
            for j in range(len(self.dofs_fixed_value[i])):
                dofs_prescribed_values.update({ dofs_presc[j+count] : self.dofs_fixed_value[i][j] })
            count += len(self.dofs_fixed_value[i])
        return dofs_prescribed_values

    def map_nodes(self):
        """ Nodes assembly in a list ordered by the user indexing."""
        nodes_dictionary = self.node_internal_to_user_index()
        map_nodes = {}
        nodes_internal = self.nodes_internal_index()
        for i in nodes_internal:
            x = self.nodal_coordinates[i,1]
            y = self.nodal_coordinates[i,2]
            z = self.nodal_coordinates[i,3]
            user_index = nodes_dictionary[i]
            map_nodes.update( {user_index : Node(x, y, z, user_index, index = i)} )
        return map_nodes
    
    #TODO: determinate the structure and type of material_list and material_dictionary.
    #TODO: determinate the structure and type of cross_section_list and cross_section_dictionary
    #TODO: determinate the structure and type of element_type_dictionary

    def number_elements(self):
        return len(self.connectivity)
    
    def element_index(self):
        return self.connectivity[:,0].astype(int)

    def map_elements(self):
        map_elements = {}

        map_nodes = self.map_nodes()
        # For each element index
        for line in self.connectivity:

            element_index, user_index_node_initial, user_index_node_final = line

            # Take the internal index from user index by dictionary
            node_initial = map_nodes[ user_index_node_initial ]

            # Take the internal index from user index by dictionary
            node_final = map_nodes[ user_index_node_final ]
            
            #TODO: define how to access the material and cross_section data.
            material = self.material_dictionary[ element_index ]
            cross_section = self.cross_section_dictionary[ element_index ]
            element_type = self.element_type_dictionary[ element_index ]

            map_elements.update( { element_index : Element(node_initial,node_final,material,cross_section,element_type,element_index)} )

        return map_elements
        
    def global_matrices(self):
        start_time = time.time()
        # Prealocate
        entries_per_element = Element.total_degree_freedom**2
        total_entries = entries_per_element * self.number_elements()
               
        # Row, Collumn indeces to be used on Csr_matrix format
        I = np.zeros(total_entries)
        J = np.zeros(total_entries)
        
        # Data for the Csr_matrix format
        data_K = np.zeros(total_entries)
        data_M = np.zeros(total_entries)

        map_elements = self.map_elements()
        
        count = 0

        # For each element.
        for _, element in map_elements.items():

            # Elementar matrices on the global coordinate system
            Ke = element.stiffness_matrix_gcs()
            Me = element.mass_matrix_gcs()

            # Element global degree of freedom indeces
            mat_I, mat_J = element.dofs()

            start = count*entries_per_element
            end = start + entries_per_element
            count += 1

            I[start : end]  = mat_I.flatten()
            J[start : end]  = mat_J.flatten()
            data_K[start : end] = Ke.flatten()
            data_M[start : end] = Me.flatten()

        # Line and Column Elimination
        
        global_dofs_presc = np.sort( self.dofs_fixed() )
                
        total_dof = Node.degree_freedom * ( self.number_nodes() )
        global_dofs_free = np.delete( np.arange(total_dof), global_dofs_presc )

        K = csr_matrix( (data_K, (I, J)), shape = [total_dof, total_dof] )
        M = csr_matrix( (data_M, (I, J)), shape = [total_dof, total_dof] )
        
        # Slice rows and all columns of not prescribed dofs
        Kr = K[ global_dofs_presc,: ]
        Mr = K[ global_dofs_presc,: ]

        # Slice all rows/columns from not prescribed dofs
        K = K[ global_dofs_free, : ][ :, global_dofs_free ]
        M = M[ global_dofs_free, : ][ :, global_dofs_free ]
        end_time = time.time()

        print('Time to assemble and process global matrices:', round(end_time-start_time,6))

        return K, M, Kr, Mr, data_K, data_M, I, J, global_dofs_free, global_dofs_presc, total_dof