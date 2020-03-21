import numpy as np
import time
from scipy.sparse import coo_matrix, csr_matrix, csc_matrix
from collections import deque

from pulse.engine.node import Node
from pulse.engine.element_288 import Element
# from pulse.engine.element_16 import Element

class Assembly:
    """ Assembly  

    Parameters
    ----------
    nodal_coordinates : 
        
    connectivity : 
        
    nodes_prescribed_dofs : 
        
    material_list : 

    cross_section_list : 
        
    element_type_list : pipe16, pipe288
        Element type identifier.
    """
    Nel_max = 500000

    def __init__(   self,
                    preprocessor ):

        self.preprocessor = preprocessor
        self.number_nodes = preprocessor.number_nodes()
        self.number_elements = preprocessor.number_elements()
        self.total_elements_dofs = Element.total_degree_freedom
        self.global_dofs_prescribed = preprocessor.prescbribed_dofs_info()[:,0].astype(int)
        self.map_elements = preprocessor.map_elements()

        if preprocessor.prescbribed_load_info().any():
            self.prescribed_load_info = preprocessor.prescbribed_load_info()
            self.external_load = preprocessor.external_load()
            self.flag = True
        else:
            self.flag = False

        if self.number_elements <= self.Nel_max:
            self.elementaries_matrices = preprocessor.all_elementaries_matrices_gcs()
      
    def global_matrices(self):
        
        start_time = time.time()
        # Defining variables for memory preallocating
        
        edof = self.total_elements_dofs
        entries_per_element = edof**2
        total_entries = entries_per_element * self.number_elements
        N = int(total_entries / edof)

        if self.flag:
            ext_ind = len(self.prescribed_load_info[:,0])
            data_Fe, I_fe = self.external_load
        else:
            ext_ind = 1
            data_Fe, I_fe = 0, 0
            print("Warning: There's no external load.")

        # MEMORY PREALLOCATING     

        # Row, Collumn indeces to be used on Csr_matrix format
        I = np.zeros(total_entries)
        J = np.zeros(total_entries)
        I_f = np.zeros(N + ext_ind )
        J_f = np.zeros(N + ext_ind)
        
        # Data for the Csr_matrix format
        data_K = np.zeros(total_entries)
        data_M = np.zeros(total_entries)
        data_F = np.zeros(N + ext_ind)

        if self.number_elements <= self.Nel_max:

            Me, Ke, Fe, mat_I, mat_J, mat_If = self.elementaries_matrices
            data_M, data_K, data_F[0:-ext_ind] = Me.flatten(), Ke.flatten(), Fe.flatten()
            I, J, I_f[0:-ext_ind] = mat_I.flatten(), mat_J.flatten(), mat_If.flatten()

        else:

            count = 0
            map_elements = self.map_elements
            for element in map_elements.values():

                # Elementar matrices on the global coordinate system
                Me_temp, Ke_temp, Fe_temp = element.matrices_gcs()

                # Element global degree of freedom indeces
                I_temp, J_temp, If_temp  = element.dofs()

                start_f  = count * edof
                end_f = start_f + edof

                I_f[start_f : end_f] = If_temp
                data_F[start_f : end_f] = Fe_temp

                start = count * entries_per_element
                end = start + entries_per_element

                I[start : end]  = I_temp
                J[start : end]  = J_temp
                data_K[start : end] = Ke_temp
                data_M[start : end] = Me_temp

                count += 1

        # Line and Column Elimination
        
        # global_dofs_presc = np.sort( self.global_dofs_prescribed() )
        global_dofs_presc = self.global_dofs_prescribed
                
        # total_dof = Node.degree_freedom * ( self.number_nodes() )
        total_dof = Node.degree_freedom *self.number_nodes 
        
        global_dofs_free = np.delete( np.arange(total_dof), global_dofs_presc )

        K = csr_matrix( (data_K, (I, J)), shape = [total_dof, total_dof] )
        M = csr_matrix( (data_M, (I, J)), shape = [total_dof, total_dof] )
        
        data_F[-ext_ind:] = data_Fe
        I_f[-ext_ind:] = I_fe

        F = csr_matrix( (data_F, (I_f, J_f)), shape = [total_dof, 1] )
                
        # Slice rows and all columns of not prescribed dofs
        Kr = K[ global_dofs_presc,: ]
        Mr = M[ global_dofs_presc,: ]

        # Slice all rows/columns from not prescribed dofs
        K = K[ global_dofs_free, : ][ :, global_dofs_free ]
        M = M[ global_dofs_free, : ][ :, global_dofs_free ]
        F = F[ global_dofs_free, : ].toarray().flatten()
        end_time = time.time()

        print('Time to assemble and process global matrices:', round(end_time-start_time,6))
        
        return K, M, F, Kr, Mr, data_K, data_M, data_F, I, J, I_f, global_dofs_free, global_dofs_presc, total_dof