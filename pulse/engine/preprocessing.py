import numpy as np
import time

from pulse.engine.node import Node
from pulse.engine.section_fem import TubeCrossSection
from pulse.engine.material import Material
# from pulse.engine.element_16 import Element
from pulse.engine.element_288a import Element
# from pulse.engine.element_288b import Element
# from pulse.engine.element_288c import Element
                                
class PreProcessing:

    def __init__ (  self, 
                    nodal_coordinates, 
                    connectivity,
                    material_dictionary,
                    cross_section_dictionary,
                    load_dictionary,
                    element_type_dictionary,
                    # nodes_prescribed_dofs,
                    # local_dofs_prescribed,
                    # prescribed_dofs_values,
                    # nodes_prescribed_load,
                    # local_dofs_prescribed_load,
                    # prescribed_load_values,
                    # nodes_response,
                    # local_dofs_response,
                    # nodes_lumped_stiffness,
                    # local_lumped_stiffness,
                    # lumped_stiffness_values,
                    # nodes_lumped_mass,
                    # local_lumped_mass,
                    # lumped_mass_values,
                    # nodes_lumped_damping,
                    # local_lumped_damping,
                    # lumped_damping_values, 
                    **kwargs  ):

        self.nodal_coordinates = nodal_coordinates
        self.connectivity = connectivity
        self.material_dictionary = material_dictionary 
        self.cross_section_dictionary = cross_section_dictionary
        self.load_dictionary = load_dictionary
        self.element_type_dictionary = element_type_dictionary

        self.nodes_prescribed_dofs = kwargs.get("nodes_prescribed_dofs", [])
        self.local_dofs_prescribed = kwargs.get("local_dofs_prescribed", [[]])
        self.prescribed_dofs_values = kwargs.get("prescribed_dofs_values", [[]])

        self.nodes_prescribed_load = kwargs.get("nodes_prescribed_load", [])
        self.local_dofs_prescribed_load = kwargs.get("local_dofs_prescribed_load", [[]])
        self.prescribed_load_values = kwargs.get("prescribed_load_values", [[]])

        self.nodes_response = kwargs.get("nodes_response",[1])
        self.local_dofs_response = kwargs.get("local_dofs_response",[[0]])

        self.nodes_lumped_stiffness = kwargs.get("nodes_lumped_stiffness",[])
        self.local_lumped_stiffness = kwargs.get("local_lumped_stiffness",[[]])
        self.lumped_stiffness_values = kwargs.get("lumped_stiffness_values",[[]])

        self.nodes_lumped_mass = kwargs.get("nodes_lumped_mass",[])
        self.local_lumped_mass = kwargs.get("local_lumped_mass",[[]])
        self.lumped_mass_values = kwargs.get("lumped_mass_values",[[]])
        
        self.nodes_lumped_damping = kwargs.get("nodes_lumped_damping",[])
        self.local_lumped_damping = kwargs.get("local_lumped_damping",[[]])
        self.lumped_damping_values = kwargs.get("lumped_damping_values",[[]])

    
    def number_nodes(self):
        ''' Gets the total number of nodes '''
        return len(self.nodal_coordinates[:,0])
    
    def number_dofs(self):
        ''' Gets the total number of degrees of freedom '''
        return int(self.number_nodes()*Node.degree_freedom)

    def map_index_nodes(self):
        '''' Maps internal index in relation to external index of nodes 
             dictioanary = {external_node_index : internal_node_index} '''
        nodes_in = np.array(self.nodal_coordinates[:,0], dtype=int)
        ord_nodes = np.arange(len(nodes_in), dtype=int)
        return dict(zip(nodes_in, ord_nodes))

    def connectivity_remaped(self):
        ''' Reconstruction of initial connectivity array considering the nodes_ID changes '''
        
        connectivity_remaped = np.zeros(self.connectivity.shape, dtype=int)
        connectivity_remaped[:,0] = np.arange(1, self.connectivity.shape[0]+1, 1, dtype=int)
        mapping = self.map_index_nodes()

        for i in range(self.connectivity.shape[0]):
            for j in range(self.connectivity.shape[1]-1):
                connectivity_remaped[ i , 1 + j ] = mapping[ self.connectivity[ i , 1 + j ] ] 
        return connectivity_remaped

    def nodal_coordinates_remaped(self):
        ''' Reconstruction of initial nodal_coordinates array considering nodes_ID changes '''
        
        temp_coord = self.nodal_coordinates.copy()
        mapping = self.map_index_nodes()
        
        for i in range(len(self.nodal_coordinates[:,0])):
            temp_coord[ i , 0 ] = int(mapping[ self.nodal_coordinates[ i , 0 ]])
        return temp_coord

    def get_input_info(self, nodes_p, local_dofs_p, values_p):
        ''' This method correlates user inputs and maps this to internal dofs '''

        if nodes_p == []:

            input_info = []

        else:

            number_of_dofs_per_node = np.zeros((2, len(nodes_p)),dtype=int)
            number_of_dofs_per_node[0,:] = nodes_p

            for i in range(len(nodes_p)):
                number_of_dofs_per_node[1,i] = len(local_dofs_p[i])

            if values_p != None:
                input_info = np.zeros(( np.sum(number_of_dofs_per_node[1,:]), 3))
            else:
                input_info = np.zeros(( np.sum(number_of_dofs_per_node[1,:]), 2))
            
            start, end = 0, 0
            mapping = self.map_index_nodes()

            for j, value in enumerate(nodes_p):
                end += number_of_dofs_per_node[1,j]
                input_info[ start:end, 0] = mapping[value]*Node.degree_freedom + local_dofs_p[j]
                input_info[ start:end, 1] = local_dofs_p[j]
                if values_p != None:
                    input_info[ start:end, 2] = values_p[j]
                start = end

            ind = np.argsort(input_info[:, 0])
            input_info = input_info[ind, :]
    
        return input_info
    
    def prescbribed_dofs_info (self):
        ''' Returns prescribed info of external load in the format:
            [global_dofs, local_dofs, values_prescribed] '''
        return self.get_input_info(self.nodes_prescribed_dofs, self.local_dofs_prescribed, self.prescribed_dofs_values)

    def prescbribed_load_info (self):
        ''' Returns prescribed dofs info in the format:
            [global_dofs, local_dofs, values_prescribed] '''
        return self.get_input_info( self.nodes_prescribed_load, self.local_dofs_prescribed_load, self.prescribed_load_values )

    def response_info (self):
        ''' Returns prescribed dofs info in the format:
            [global_dofs, local_dofs, values_prescribed] '''
        return self.get_input_info( self.nodes_response, self.local_dofs_response, None )

    def lumped_stiffness_info (self):
        ''' Returns prescribed dofs info in the format:
            [global_dofs, local_dofs, values_prescribed] '''
        return self.get_input_info( self.nodes_lumped_stiffness, self.local_lumped_stiffness, self.lumped_stiffness_values )

    def lumped_mass_info (self):
        ''' Returns prescribed dofs info in the format:
            [global_dofs, local_dofs, values_prescribed] '''
        return self.get_input_info( self.nodes_lumped_mass, self.local_lumped_mass, self.lumped_mass_values )

    def lumped_viscous_damping_info (self):
        ''' Returns prescribed dofs info in the format:
            [global_dofs, local_dofs, values_prescribed] '''
        return self.get_input_info( self.nodes_lumped_damping, self.local_lumped_damping, self.lumped_damping_values )

    def free_dofs(self):

        total_dof = Node.degree_freedom *self.number_nodes()
        aux = np.arange(total_dof)
        free_dofs = np.delete(aux, self.prescbribed_dofs_info()[:,0])

        return free_dofs

    def map_nodes(self):
        """ Nodes assembly in a list ordered by the user indexing."""
        user_index = self.nodal_coordinates[:,0].astype(int)
        map_nodes = {}
        nodes_internal = self.nodal_coordinates_remaped()[:,0].astype(int)
        for i in nodes_internal:
            x = self.nodal_coordinates[i,1]
            y = self.nodal_coordinates[i,2]
            z = self.nodal_coordinates[i,3]
            map_nodes.update( {user_index[i] : Node(x, y, z, user_index, index = i)} )
        return map_nodes

    def total_element_dofs(self):
        return Element.total_degree_freedom

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
            cross_section_properties = self.cross_section_dictionary[ element_index ]
            load = self.load_dictionary[ element_index ]
            element_type = self.element_type_dictionary[ element_index ]

            map_elements.update( { element_index : Element(node_initial,node_final,material,cross_section_properties,load,element_type,element_index)} )

        return map_elements
        
    def all_elementaries_matrices_gcs(self):

        Nel = self.number_elements()           
        edof = Element.total_degree_freedom

        Ke_t    = np.ones(shape=[ Nel, edof**2 ], dtype=float)
        Me_t    = np.ones(shape=[ Nel, edof**2 ], dtype=float)
        Fe_t    = np.ones(shape=[ Nel, edof    ], dtype=float)
        mat_It  = np.ones(shape=[ Nel, edof**2 ], dtype=float)
        mat_Jt  = np.ones(shape=[ Nel, edof**2 ], dtype=float)
        mat_Ift = np.ones(shape=[ Nel, edof    ], dtype=float)

        map_elements = self.map_elements()

        for i, element in enumerate(map_elements.values()): 
            Me_t[i,:], Ke_t[i,:], Fe_t[i,:] = element.matrices_gcs()
            mat_It[i,:], mat_Jt[i,:], mat_Ift[i,:] = element.dofs()
        return Me_t, Ke_t, Fe_t, mat_It, mat_Jt, mat_Ift

    def external_load(self):
        
        load_info = self.prescbribed_load_info() 
        Element.total_degree_freedom

        if load_info.any() and not load_info == []:
            
            F_ext = load_info[:,2]
            I_fe = load_info[:,0]
        else:
            F_ext, I_fe = 0, 0

        return F_ext, I_fe