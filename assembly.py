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
        
    fixed_degree_freedom : 
        
    material_list : 

    cross_section_list : 
        
    element_type_list : pipe16, pipe288
        Element type identifier.
    """
    def __init__(   self,
                    nodal_coordinates,
                    connectivity,
                    fixed_degree_freedom,
                    material_list,
                    material_dictionary,
                    cross_section_list,
                    cross_section_dictionary,
                    element_type_dictionary):
        self.nodal_coordinates = nodal_coordinates
        self.connectivity = connectivity
        self.fixed_degree_freedom = fixed_degree_freedom
        self.material_list = material_list 
        self.material_dictionary = material_dictionary 
        self.cross_section_list = cross_section_list
        self.cross_section_dictionary = cross_section_dictionary
        self.element_type_dictionary = element_type_dictionary

    def number_nodes(self):
        """ Total number of nodes on the mesh."""
        return self.nodal_coordinates.shape[0]
    
    def node_user_index(self):
        """ Array with all node user index."""
        return self.nodal_coordinates[:,0].astype(int)
    
    def node_internal_index(self):
        """ Array with all node internal index."""
        return range(self.number_nodes())
    
    def node_internal_to_user_index(self):
        """ Dictionary ."""
        return {i:self.node_user_index()[i] for i in self.node_internal_index()}
    
    def node_user_to_internal_index(self):
        """ Dictionary ."""
        return { j:i for i, j in self.node_internal_to_user_index().items() }

    def map_nodes(self):
        """ Nodes assembly in a list ordered by the internal indexing."""
        nodes_dictionary = self.node_internal_to_user_index()
        nodes_list = {}
        for i in self.node_internal_index():
            x = self.nodal_coordinates[i,1]
            y = self.nodal_coordinates[i,2]
            z = self.nodal_coordinates[i,3]
            user_index = nodes_dictionary[i]
            nodes_list.update( {i : Node(x, y, z, user_index, index = i)} )
        return nodes_list
    
    #TODO: determinate the structure and type of material_list and material_dictionary.
    #TODO: determinate the structure and type of cross_section_list and cross_section_dictionary
    #TODO: determinate the structure and type of element_type_dictionary

    def number_elements(self):
        return self.connectivity.shape[0]
    
    def element_user_index(self):
        return self.connectivity[:,0].astype(int)
    
    def map_elements(self):
        elements_list = {}
        nodes_dictionary = self.node_user_to_internal_index()
        map_nodes = self.map_nodes()
        for i in self.element_user_index():
            index_node_initial = nodes_dictionary[ self.connectivity[i,1] ]
            node_initial = map_nodes[ index_node_initial ]

            index_node_final = nodes_dictionary[ self.connectivity[i,2] ]
            node_final = map_nodes[ index_node_final ]

            material = self.material_dictionary[i]
            cross_section = self.cross_section_dictionary[i]
            element_type = self.element_type_dictionary[i]
            user_index = i
            elements_list.update( {i : Element(node_initial,node_final,material,cross_section,element_type,user_index)} )

        return elements_list
    
    @staticmethod
    def symmetrize(a):
        """ Take a matrix a and symmetrize it."""
        return a + a.T - np.diag(a.diagonal())
    
    def global_matrices(self):
        total_dof = Node.degree_freedom * self.number_nodes()

        # Row, Collumn indeces to be used on Coo_matrix format
        I = []
        J = []

        # Data for the Coo_matrix format
        coo_K = []
        coo_M = []

        # For each element.
        for e in self.map_elements():
            element = self.map_elements()[e]

            # Elementar matrices on the global coordinate system
            Ke = element.stiffness_matrix_global()
            Me = element.mass_matrix_global()

            # Element global degree of freedom indeces
            global_dof = element.global_degree_freedom()

            # Construct vectors row by row
            for i in range(global_dof.shape[0]):
                row_index = global_dof[i]
                I = np.concatenate(I, row_index * np.ones_like(global_dof))
                J = np.concatenate(J, global_dof)
                coo_K = np.concatenate(coo_K, Ke[i,:])
                coo_M = np.concatenate(coo_M, Me[i,:])
        
        K = coo_matrix( (coo_K, (I, J)), [shape=(total_dof, total_dof)] )
        M = coo_matrix( (coo_M, (I, J)), [shape=(total_dof, total_dof)] )
        
        return K, M
    