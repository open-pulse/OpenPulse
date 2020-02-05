import numpy as np
from scipy.sparse import coo_matrix
import time


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
            if dof_list == 'all':
                count += 6
            else:
                count += len(dof_list)
        return count

    def dofs_fixed(self):
        """ Global index of every fixed degree of freedom."""
        dictionary = self.node_user_to_internal_index()
        global_dofs_fixed = np.zeros( self.count_dofs_fixed() )
        count = 0
        for i in range( len(self.fixed_nodes) ):
            user_index = self.fixed_nodes[i]
            index = dictionary[user_index]

            if self.dofs_fixed_node[i] == 'all':
                global_dofs_fixed[count : count + Node.degree_freedom] = index * Node.degree_freedom + np.arange( Node.degree_freedom )
                count += Node.degree_freedom
            else:
                global_dofs_fixed[count : count + len(dof_list)] = index * Node.degree_freedom + self.dofs_fixed[i]
                count += len(dof_list)

        return global_dofs_fixed
    
    def nodes_boundary(self):
        """ Dictionary ."""
        boundary = {}
        dictionary = self.node_internal_to_user_index()
        nodes_internal = self.nodes_internal_index()
        for i in nodes_internal:
            user_index = dictionary[i]
            if user_index in self.fixed_nodes:
                if self.dofs_fixed_node[ list(self.fixed_nodes).index(user_index) ] == 'all':
                    boundary.update( {i : np.arange( Node.degree_freedom ) })
                else:
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
        
    def global_matrices(self, delete_rc = True ):
        entries_per_element = Element.total_degree_freedom**2
        total_entries = entries_per_element * self.number_elements()
        
        # Row, Collumn indeces to be used on Coo_matrix format
        I = np.zeros(total_entries)
        J = np.zeros(total_entries)
        
        # Data for the Coo_matrix format
        coo_K = np.zeros(total_entries)
        coo_M = np.zeros(total_entries)

        map_elements = self.map_elements()

        # For each element.
        for e in map_elements:
            element = map_elements[e]

            # Elementar matrices on the global coordinate system
            Ke = element.stiffness_matrix_gcs()
            Me = element.mass_matrix_gcs()

            # Element global degree of freedom indeces
            global_dof, local_dof = element.global_dof( delete_rc )

            aux = len(global_dof)

            # map_elements is counted initiating by 1 going up to number_elements
            #TODO: be carefull about element index.
            count = (e - 1) * entries_per_element
            
            
            # Construct vectors row by row
            ind = int(0)
            for i in local_dof:
                
                row_index = int( global_dof[ind] )

                I[count : count + aux]  = row_index * np.ones( aux, dtype=int )
                J[count : count + aux]  = np.array( global_dof, dtype= int )
                coo_K[count : count + aux] = Ke[i, local_dof]
                coo_M[count : count + aux] = Me[i, local_dof]

                # Each iteration update len( global_dof ) amount
                ind += 1
                count += aux 
        
        #TODO: consider write in another method
        # Line and Collumn Elimination

        # 
        count = int(0)

        if delete_rc:
            global_dofs_fixed = self.dofs_fixed()
            for dof_fixed in global_dofs_fixed:

                aux_I = np.where(I > dof_fixed - count )
                aux_J = np.where(J > dof_fixed - count )

                I[aux_I] = I[aux_I] - 1
                J[aux_J] = J[aux_J] - 1

                count += 1

        total_dof = Node.degree_freedom * ( self.number_nodes() ) - count

        K = coo_matrix( (coo_K, (I, J)), shape = [total_dof, total_dof] )
        M = coo_matrix( (coo_M, (I, J)), shape = [total_dof, total_dof] )
        
        return K, M, I, J, coo_K, coo_M, total_dof