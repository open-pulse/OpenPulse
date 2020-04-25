import numpy as np
from time import time
from scipy.sparse import coo_matrix, csr_matrix, csc_matrix

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
                    preprocessor, Element  ):

        self.preprocessor = preprocessor
        self.Element = Element
        self.number_nodes = preprocessor.number_nodes()
        self.number_elements = preprocessor.number_elements()
        self.total_elements_dofs = self.Element.total_degree_freedom
        self.total_dofs = preprocessor.number_dofs() 
        self.global_dofs_prescribed = preprocessor.prescbribed_dofs_info()[:,0].astype(int)
        self.global_dofs_free = np.delete( np.arange(self.total_dofs), self.global_dofs_prescribed )
        self.global_dofs_values = preprocessor.prescbribed_dofs_info()[:,2]
        self.map_elements = preprocessor.map_elements()

        self.lump_stiffness = preprocessor.lumped_stiffness_info()
        self.lump_mass = preprocessor.lumped_mass_info()
        self.lump_viscous_damping = preprocessor.lumped_viscous_damping_info()
       
        if preprocessor.prescbribed_load_info().any():
            self.prescribed_load_info = preprocessor.prescbribed_load_info()
            self.external_load = preprocessor.external_load()
            self.flag = True
        else:
            self.flag = False

        if self.number_elements <= self.Nel_max:
            self.elementaries_matrices = preprocessor.all_elementaries_matrices_gcs()
      
    def global_matrices(self):
        
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

        # Row, Collumn indeces to be used on Csc_matrix format
        I = np.zeros(total_entries)
        J = np.zeros(total_entries)
        I_f = np.zeros(N + ext_ind )
        J_f = np.zeros(N + ext_ind)
        
        # Data for the Csc_matrix format
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

                # Element global degree of freedom indices
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

        # Get global matrices/vector through csc_matrix function
        K = csc_matrix( (data_K, (I, J)), shape = [self.total_dofs, self.total_dofs] )
        M = csc_matrix( (data_M, (I, J)), shape = [self.total_dofs, self.total_dofs] )
        
        # Add elements due the nodal load
        data_F[-ext_ind:] = data_Fe
        I_f[-ext_ind:] = I_fe
       
        F = csc_matrix( (data_F, (I_f, J_f)), shape = [self.total_dofs, 1] )
                                
        return K, M, F, data_K, data_M, data_F, I, J, I_f
    
    def lumped_matrices(self):

        infoK_lump = self.lump_stiffness
        infoM_lump = self.lump_mass
        infoC_lump = self.lump_viscous_damping
        dofs = self.total_dofs

        if not infoK_lump == []:
            I_k, data_Kl = infoK_lump[:,0], infoK_lump[:,2]
            K_lump = csc_matrix( (data_Kl, (I_k, I_k)), shape = [dofs, dofs] )
            flag_K = True
        else:
            K_lump = 0
            flag_K = False
        
        if not infoM_lump == []:
            I_m, data_Ml = infoM_lump[:,0], infoM_lump[:,2]
            M_lump = csc_matrix( (data_Ml, (I_m, I_m)), shape = [dofs, dofs] )
            flag_M = True
        else:
            M_lump = 0
            flag_M = False
        
        if not infoC_lump == []:
            I_c, data_Cl = infoC_lump[:,0], infoC_lump[:,2]
            C_lump = csc_matrix( (data_Cl, (I_c, I_c)), shape = [dofs, dofs] )
            flag_C = True
        else:
            C_lump = 0
            flag_C = False 
                
        return K_lump, M_lump, C_lump, flag_K, flag_M, flag_C

    def rows_columns_drops(self, timing=True):

        start_time = time()

        K, M, F, _, _, _, _, _, _, = self.global_matrices()
  
        # Slice columns of prescribed dofs
        Kr = K[ :, self.global_dofs_prescribed ]
        Mr = M[ :, self.global_dofs_prescribed ]

        # Slice all rows/columns from not prescribed dofs
        K = K[ self.global_dofs_free, : ][ :, self.global_dofs_free ]
        M = M[ self.global_dofs_free, : ][ :, self.global_dofs_free ]
        F = F[ self.global_dofs_free, : ].toarray().flatten()

        end_time = time()

        if timing:
            print('Time to assemble and process global matrices:', round(end_time-start_time,6))
        
        return K, M, F, Kr, Mr

    def rows_columns_drops_lumped(self):

        K_lump, M_lump, C_lump, flag_K, flag_M, flag_C = self.lumped_matrices()

        if flag_K:

            Kr_lump = K_lump[ :, self.global_dofs_prescribed ]
            K_lump = K_lump[ self.global_dofs_free, : ][ :, self.global_dofs_free ]
        else:
            Kr_lump = 0
        
        if flag_M:

            Mr_lump = M_lump[ :, self.global_dofs_prescribed ]
            M_lump = M_lump[ self.global_dofs_free, : ][ :, self.global_dofs_free ]
        else:
            Mr_lump = 0

        if flag_C:

            Cr_lump = C_lump[ :, self.global_dofs_prescribed ]
            C_lump = C_lump[ self.global_dofs_free, : ][ :, self.global_dofs_free ]       
        else:
            Cr_lump = 0

        return K_lump, M_lump, C_lump, Kr_lump, Mr_lump, Cr_lump, flag_K, flag_M, flag_C  

    def add_lumped_matrices(self):
        
        K, M, _, _, _ = self.rows_columns_drops(timing=False)
        K_lump, M_lump, _, _, _, _, _, _, _ = self.rows_columns_drops_lumped()
        
        Kadd_lump = K + K_lump
        Madd_lump = M + M_lump

        return Kadd_lump, Madd_lump
    
    def is_there_lumped_info(self):

        if list(self.lump_stiffness) == []:
            flagK = False
        elif (self.lump_stiffness[:,2]).any():
            flagK = True
        else:
            flagK = False

        if list(self.lump_mass) == []:
            flagM = False
        elif (self.lump_mass[:,2]).any():
            flagM = True
        else:
            flagM = False

        if flagK or flagM:
            flag = True
        else:
            flag = False

        return flag

    def solution_dofs_info(self):
        return self.global_dofs_free, self.global_dofs_prescribed, self.global_dofs_values

    def matrices_data_to_save(self):
        _, _, _, data_K, data_M, data_F, I, J, I_f = self.global_matrices()
        return data_K, data_M, data_F, I, J, I_f, self.global_dofs_free, self.global_dofs_prescribed, self.total_dofs