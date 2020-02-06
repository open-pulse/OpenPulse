import numpy as np
from scipy.sparse import coo_matrix
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
                    material_list,
                    material_dictionary,
                    cross_section_list,
                    cross_section_dictionary,
                    element_type_dictionary):
        self.nodal_coordinates = nodal_coordinates
        self.connectivity = connectivity
        self.fixed_nodes = fixed_nodes
        self.dofs_fixed_node = dofs_fixed_node               
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
    
    def count_dofs_fixed(self):
        "Number of dofs fixed"
        count = 0
        for dof_list in self.dofs_fixed_node:
            count += len(dof_list)
        return count
    
    def count_empty_entries(self):
        "Number of dofs fixed"
        count = 0
        for i in range( len (self.fixed_nodes )):
            count += 2 * len(self.dofs_fixed_node[i])**2
        return count

    def dofs_fixed(self):
        """ Global index of every fixed degree of freedom."""
        dictionary = self.node_user_to_internal_index()
        global_dofs_fixed = deque()

        for i, user_index in enumerate(self.fixed_nodes):
            index = dictionary[user_index]
            global_dofs_fixed.extend( index * Node.degree_freedom + self.dofs_fixed_node[i] )

        return global_dofs_fixed
    
    def nodes_boundary(self):
        """ Dictionary ."""
        boundary = {}
        dictionary = self.node_internal_to_user_index()
        for i, user_index in dictionary.items():
            if user_index in self.fixed_nodes:
                boundary.update({i : self.dofs_fixed_node[ list(self.fixed_nodes).index(user_index) ] })
            else:
                boundary.update({i: []})
        return boundary
    
    def map_nodes(self):
        """ Nodes assembly in a list ordered by the internal indexing."""
        nodes_dictionary = self.node_internal_to_user_index()
        nodes_list = {}
        nodes_boundary = self.nodes_boundary()
        nodes_internal = self.nodes_internal_index()
        for i in nodes_internal:
            x = self.nodal_coordinates[i,1]
            y = self.nodal_coordinates[i,2]
            z = self.nodal_coordinates[i,3]
            user_index = nodes_dictionary[i]
            boundary = nodes_boundary[i]
            nodes_list.update( {i : Node(x, y, z, user_index, index = i, boundary = boundary)} )
        return nodes_list
    
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
        
    def global_matrices(self):
        # Prealocate
        entries_per_element = Element.total_degree_freedom**2
        empty_entries = self.count_empty_entries() 
        total_entries = entries_per_element * self.number_elements() - empty_entries
               
        # Row, Collumn indeces to be used on Coo_matrix format
        I = np.zeros(total_entries)
        J = np.zeros(total_entries)
        
        # Data for the Coo_matrix format
        coo_K = np.zeros(total_entries)
        coo_M = np.zeros(total_entries)

        # Row, Collumn indeces to be used on Coo_matrix format
        Ib = np.zeros(empty_entries)
        Jb = np.zeros(empty_entries)
        
        # Data for the Coo_matrix format
        coo_Kb = np.zeros(empty_entries)
        coo_Mb = np.zeros(empty_entries)

        map_elements = self.map_elements()

        count = int(0)
        count_b = int(0)
        line_restored = int(0)
        # For each element.
        for _, element in map_elements.items():

            # Elementar matrices on the global coordinate system
            Ke = element.stiffness_matrix_gcs()
            Me = element.mass_matrix_gcs()

            # Element global degree of freedom indeces
            global_dof, local_dof, global_boundary, boundary = element.dofs()

            # Construct non precribed matriz
            aux = len(global_dof)            
            for i, line_dof in enumerate(local_dof):

                I[count : count + aux]  = global_dof[i] * np.ones( aux, dtype=int )
                J[count : count + aux]  = np.array( global_dof, dtype= int )
                coo_K[count : count + aux] = Ke[line_dof, local_dof]
                coo_M[count : count + aux] = Me[line_dof, local_dof]

                count += aux
            
             
            # Construct auxiliar vectors row by row for the BOUNDARY degree of freedom
            for _, line_dof in enumerate(boundary):

                aux_b = len(global_boundary) 

                Ib[count_b : count_b + aux_b]  = line_restored * np.ones( aux_b, dtype=int )
                Jb[count_b : count_b + aux_b]  = np.array( global_boundary, dtype= int )
                coo_Kb[count_b : count_b + aux_b] = Ke[line_dof, boundary]
                coo_Mb[count_b : count_b + aux_b] = Me[line_dof, boundary]

                count_b += aux_b

                aux_b = len(global_dof) 
                Ib[count_b : count_b + aux_b]  = line_restored * np.ones( aux_b, dtype=int )
                Jb[count_b : count_b + aux_b]  = np.array( global_dof, dtype= int )
                coo_Kb[count_b : count_b + aux_b] = Ke[line_dof, local_dof]
                coo_Mb[count_b : count_b + aux_b] = Me[line_dof, local_dof]

                count_b += aux_b
                line_restored +=1
                
        
        # Line and Collumn Elimination
        count = int(0)
        global_dofs_fixed = np.sort( self.dofs_fixed() )
        for dof_fixed in global_dofs_fixed:

            aux_I = np.where(I > dof_fixed - count )
            aux_J = np.where(J > dof_fixed - count )

            I[aux_I] = I[aux_I] - 1
            J[aux_J] = J[aux_J] - 1

            count += 1
        
        total_dof = Node.degree_freedom * ( self.number_nodes() )

        K = coo_matrix( (coo_K, (I, J)), shape = [total_dof - line_restored, total_dof - line_restored] )
        M = coo_matrix( (coo_M, (I, J)), shape = [total_dof - line_restored, total_dof - line_restored] )

        Kb = coo_matrix( (coo_Kb, (Ib, Jb)), shape = [line_restored, total_dof] )
        Mb = coo_matrix( (coo_Mb, (Ib, Jb)), shape = [line_restored, total_dof] )

        return K, M, Kb, Mb, total_dof - line_restored, Ib, Jb