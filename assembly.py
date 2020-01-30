import numpy as np
from scipy.sparse import coo_matrix


from node import Node
from tube import TubeCrossSection
from material import Material
from element import Element


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
                    material_list,
                    material_dictionary,
                    cross_section_list,
                    cross_section_dictionary,
                    element_type_dictionary):
        self.nodal_coordinates = nodal_coordinates
        self.connectivity = connectivity
        self.fixed_nodes = fixed_nodes
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
        return range( self.number_nodes() )
    
    def node_internal_to_user_index(self):
        """ Dictionary ."""
        return {i:self.nodes_user_index()[i] for i in self.nodes_internal_index()}
    
    def node_user_to_internal_index(self):
        """ Dictionary ."""
        return { j:i for i, j in self.node_internal_to_user_index().items() }

    def map_nodes(self):
        """ Nodes assembly in a list ordered by the internal indexing."""
        nodes_dictionary = self.node_internal_to_user_index()
        nodes_list = {}
        for i in self.nodes_internal_index():
            x = self.nodal_coordinates[i,1]
            y = self.nodal_coordinates[i,2]
            z = self.nodal_coordinates[i,3]
            user_index = nodes_dictionary[i]
            nodes_list.update( {i : Node(x, y, z, user_index, index = i)} )
        return nodes_list
    
    # #TODO: adapt this function to receive not all dof
    # def fixed_degree_freedom(self):
    #     fixed_degree_freedom = []

    #     for node in self.fixed_nodes:
    #         fixed_degree_freedom = np.concatenate(fixed_degree_freedom, node.global_dof())
    #     return fixed_degree_freedom
    
    #TODO: determinate the structure and type of material_list and material_dictionary.
    #TODO: determinate the structure and type of cross_section_list and cross_section_dictionary
    #TODO: determinate the structure and type of element_type_dictionary

    def number_elements(self):
        return self.connectivity.shape[0]
    
    def element_index(self):
        return self.connectivity[:,0].astype(int)
    
    def map_elements(self):
        elements_list = {}

        # Given a user index, it returns the internal index
        nodes_dictionary = self.node_user_to_internal_index()

        # Given the internal index, return respect node.
        map_nodes = self.map_nodes()

        # For each element index
        for i in range( self.number_elements() ):

            element_index, user_index_node_initial, user_index_node_final = self.connectivity[i,:]

            # Take the internal index from user index by dictionary
            index_node_initial = nodes_dictionary[ user_index_node_initial ]
            node_initial = map_nodes[ index_node_initial ]

            # Take the internal index from user index by dictionary
            index_node_final = nodes_dictionary[ user_index_node_final ]
            node_final = map_nodes[ index_node_final ]

            #TODO: define how to access the material and cross_section data.

            material = self.material_dictionary[ element_index ]
            cross_section = self.cross_section_dictionary[ element_index ]
            element_type = self.element_type_dictionary[ element_index ]

            elements_list.update( { element_index : Element(node_initial,node_final,material,cross_section,element_type,element_index)} )

        return elements_list
    
    @staticmethod
    def symmetrize(a):
        """ Take a matrix a and symmetrize it."""
        return a + a.T - np.diag(a.diagonal())
    
    def global_matrices(self):
        #TODO: Define a better way to pre alocated matrix.
        total_dof = 3 * Node.degree_freedom * ( self.number_nodes() - self.fixed_nodes.shape[0] )

        # Row, Collumn indeces to be used on Coo_matrix format
        I = np.zeros(total_dof * total_dof)
        J = np.zeros(total_dof * total_dof)

        # Data for the Coo_matrix format
        coo_K = np.zeros(total_dof * total_dof)
        coo_M = np.zeros(total_dof * total_dof)

        # For each element.
        for e in self.map_elements():
            element = self.map_elements()[e]

            # Elementar matrices on the global coordinate system
            Ke = element.stiffness_matrix_global()
            Me = element.mass_matrix_global()

            # Element global degree of freedom indeces
            #TODO: code is limited to all degree of freedom of a node fixed.
            global_dof, local_dof = element.global_degree_freedom( self.fixed_nodes )
            count = int(0)

            aux = len(global_dof)

            # Construct vectors row by row
            for i in range( aux ):
                row_index = int( global_dof[i] )

                I[count : count + aux]  = row_index * np.ones( aux, dtype=int )
                J[count : count + aux]  = np.array( global_dof, dtype= int )
                coo_K[count : count + aux] = Ke[i, local_dof]
                coo_M[count : count + aux] = Me[i, local_dof]

                # Each iteration update len( global_dof ) amount
                count += aux

        total_dof = Node.degree_freedom * ( self.number_nodes() )

        return I, J, coo_K, coo_M, total_dof

        # K = coo_matrix( (coo_K, (I, J)), shape = [total_dof, total_dof] )
        # M = coo_matrix( (coo_M, (I, J)), shape = [total_dof, total_dof] )
        
        # return K, M
    