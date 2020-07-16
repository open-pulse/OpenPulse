from time import time
import numpy as np
from scipy.sparse.linalg import eigs, spsolve
from pulse.processing.assembly_structural import AssemblyStructural
from pulse.utils import error

class SolutionStructural:

    def __init__(self, mesh, frequencies, **kwargs):

        self.acoustic_solution = kwargs.get("acoustic_solution", None)
        self.assembly = AssemblyStructural(mesh, frequencies, acoustic_solution=self.acoustic_solution)
        self.frequencies = frequencies

        self.K_lump, self.M_lump, self.C_lump, self.Kr_lump, self.Mr_lump, self.Cr_lump, self.flag_Clump = self.assembly.get_lumped_matrices()
        self.K, self.M, self.Kr, self.Mr = self.assembly.get_global_matrices()
        # self.Kadd_lump = self.K + self.K_lump
        # self.Madd_lump = self.M + self.M_lump

        self.prescribed_indexes = self.assembly.get_prescribed_indexes()
        self.prescribed_values = self.assembly.get_prescribed_values()
        self.unprescribed_indexes = self.assembly.get_unprescribed_indexes()
        self.flag_Modal_prescribed_NonNull_DOFs = False
        self.flag_ModeSup_prescribed_NonNull_DOFs = False
        self.warning_Clump = ""
        self.warning_ModeSup_prescribedDOFs = ""
        self.warning_Modal_prescribedDOFs = ""


    def _reinsert_prescribed_dofs(self, solution, modal_analysis=False):
        rows = solution.shape[0] + len(self.prescribed_indexes)
        cols = solution.shape[1]
        full_solution = np.zeros((rows, cols), dtype=complex)
        full_solution[self.unprescribed_indexes, :] = solution
        if modal_analysis:
            full_solution[self.prescribed_indexes, :] = np.zeros((len(self.prescribed_values),cols))
        else:
            full_solution[self.prescribed_indexes, :] = self.array_prescribed_values
        return full_solution


    def get_combined_loads(self, global_damping_values):

        F = self.assembly.get_global_loads()
        
        unprescribed_indexes = self.unprescribed_indexes
        prescribed_values = self.prescribed_values

        alphaH, betaH, alphaV, betaV = global_damping_values
        
        Kr = (self.Kr.toarray())[unprescribed_indexes, :]
        Mr = (self.Mr.toarray())[unprescribed_indexes, :]

        Kr_lump = [(Kr_lump.toarray())[unprescribed_indexes, :] for Kr_lump in self.Kr_lump]
        Mr_lump = [(Mr_lump.toarray())[unprescribed_indexes, :] for Mr_lump in self.Mr_lump]
        Cr_lump = [(Cr_lump.toarray())[unprescribed_indexes, :] for Cr_lump in self.Cr_lump]

        rows = Kr.shape[0]
        cols = len(self.frequencies)
        
        Kr_add = np.zeros((rows,cols), dtype=complex)
        Mr_add = np.zeros((rows,cols), dtype=complex)
        Kr_add_lump = np.zeros((rows,cols), dtype=complex)
        Mr_add_lump = np.zeros((rows,cols), dtype=complex)
        Cr_add_lump = np.zeros((rows,cols), dtype=complex)

        F_eq = np.zeros((rows,cols), dtype=complex)

        aux_ones = np.ones(cols, dtype=complex)
        list_prescribed_dofs = []

        try:    
            for value in prescribed_values:
                if isinstance(value, complex):
                    list_prescribed_dofs.append(aux_ones*value)
                elif isinstance(value, np.ndarray):
                    list_prescribed_dofs.append(value)
            self.array_prescribed_values = np.array(list_prescribed_dofs)
        except Exception as e:
            error(str(e))
            return F_eq

        for i in range(cols):
        
            if list_prescribed_dofs != []:
                Kr_add[:,i] = np.sum(Kr*self.array_prescribed_values[:,i], axis=1)
                Mr_add[:,i] = np.sum(Mr*self.array_prescribed_values[:,i], axis=1)
            
                Kr_add_lump[:,i] = np.sum(Kr_lump[i]*self.array_prescribed_values[:,i], axis=1)
                Mr_add_lump[:,i] = np.sum(Mr_lump[i]*self.array_prescribed_values[:,i], axis=1)
                Cr_add_lump[:,i] = np.sum(Cr_lump[i]*self.array_prescribed_values[:,i], axis=1)

        for i, freq in enumerate(self.frequencies):

            omega = 2*np.pi*freq
            F_Kadd = Kr_add[:,i] + Kr_add_lump[:,i]
            F_Madd = (-(omega**2))*(Mr_add[:,i] + Mr_add_lump[:,i]) 
            F_Cadd = 1j*((betaH + omega*betaV)*Kr_add[:,i] + (alphaH + omega*alphaV)*Mr_add[:,i])

            F_Cadd_lump = 1j*omega*Cr_add_lump[:,i]

            F_eq[:, i] = F_Kadd + F_Madd + F_Cadd + F_Cadd_lump

        F_combined = F - F_eq
        
        return F_combined


    def modal_analysis(self, K=[], M=[], modes=20, which='LM', sigma=0.01, harmonic_analysis=False):

        if K==[] and M==[] and self.assembly.no_table:
            Kadd_lump = self.K + self.K_lump[0]
            Madd_lump = self.M + self.M_lump[0]
        else:
            Kadd_lump = K
            Madd_lump = M
        
        eigen_values, eigen_vectors = eigs(Kadd_lump, M=Madd_lump, k=modes, which=which, sigma=sigma)

        positive_real = np.absolute(np.real(eigen_values))
        natural_frequencies = np.sqrt(positive_real)/(2*np.pi)
        modal_shape = np.real(eigen_vectors)

        index_order = np.argsort(natural_frequencies)
        natural_frequencies = natural_frequencies[index_order]
        modal_shape = modal_shape[:, index_order]

        if not harmonic_analysis:
            modal_shape = self._reinsert_prescribed_dofs(modal_shape, modal_analysis=True)
            for value in self.prescribed_values:
                if value is not None:
                    if (isinstance(value, complex) and value != complex(0)) or (isinstance(value, np.ndarray) and sum(value) != complex(0)):
                        self.flag_Modal_prescribed_NonNull_DOFs = True
                        self.warning_Modal_prescribedDOFs = ["The Prescribed DOFs of non-zero values has been ignored in the modal analysis.\n"+
                                                            "The null value has been attributed to those DOFs with non-zero values."]

        return natural_frequencies, modal_shape


    def direct_method(self, global_damping_values=(0,0,0,0)):

        """ 
            Perform an harmonic analysis through direct method and returns the response of
            all nodes due the external or internal equivalent load. It has been implemented two
            different damping models: Viscous Proportional and Hysteretic Proportional
            Entries for Viscous Proportional Model Damping: (alpha_v, beta_v)
            Entries for Hyteretic Proportional Model Damping: (alpha_h, beta_h)
        """

        alphaH, betaH, alphaV, betaV = global_damping_values
        
        # t0 = time()
        F = self.get_combined_loads(global_damping_values)
        # dt = time() - t0
        # print("Time elapsed: {}[s]".format(dt))

        rows = self.K.shape[0]
        cols = len(self.frequencies)
        solution = np.zeros((rows, cols), dtype=complex)

        alphaH, betaH, alphaV, betaV = global_damping_values
    
        for i, freq in enumerate(self.frequencies):

            omega = 2*np.pi*freq
            
            F_K = (self.K + self.K_lump[i])
            F_M =  (-(omega**2))*(self.M + self.M_lump[i])
            F_C = 1j*(( betaH + omega*betaV )*self.K + ( alphaH + omega*alphaV )*self.M)

            F_Clump = 1j*omega*self.C_lump[i]
            
            A = F_K + F_M + F_C + F_Clump
            solution[:,i] = spsolve(A, F[:,i])

        self.solution = self._reinsert_prescribed_dofs(solution)

        return self.solution

    def mode_superposition(self, modes, F_loaded=None, global_damping_values=(0,0,0,0), fastest=True):
        
        """ 
            Perform an harmonic analysis through superposition method and returns the response of
            all nodes due the external or internal equivalent load. It has been implemented two
            different damping models: Viscous Proportional and Hysteretic Proportional
            Entries for Viscous Proportional Model Damping: (alpha_v, beta_v)
            Entries for Hyteretic Proportional Model Damping: (alpha_h, beta_h)
        """
        alphaH, betaH, alphaV, betaV = global_damping_values

        if np.sum(self.prescribed_values)>0:
            solution = self.direct_method(global_damping_values=global_damping_values)
            self.flag_ModeSup_prescribed_NonNull_DOFs = True
            self.warning_ModeSup_prescribedDOFs = "The Harmonic Analysis of prescribed DOF's problems \nhad been solved through the Direct Method!"
            return solution
        else:
            F = self.assembly.get_global_loads(loads_matrix3D=fastest)
            Kadd_lump = self.K + self.K_lump[0]
            Madd_lump = self.M + self.M_lump[0]

        if not self.assembly.no_table:
            return

        #TODO: in the future version implement lets F_loaded operational

        natural_frequencies, modal_shape = self.modal_analysis(K=Kadd_lump, M=Madd_lump, modes=modes, harmonic_analysis=True)
        rows = Kadd_lump.shape[0]
        cols = len(self.frequencies)

        if fastest:    
        
            number_modes = len(natural_frequencies)
            omega = 2*np.pi*self.frequencies.reshape(cols,1,1)
            omega_n = 2*np.pi*natural_frequencies
            F_kg = (omega_n**2)
            F_mg =  - (omega**2)
            F_cg = 1j*((betaH + betaV*omega)*(omega_n**2) + (alphaH + omega*alphaV)) 
            diag = np.divide(1, (F_kg + F_mg + F_cg))*np.eye(number_modes)
            F_aux = modal_shape.T @ F
            solution = modal_shape @ (diag @ F_aux)
            solution = solution.reshape(cols, rows).T
        
        else:
        
            solution = np.zeros((rows, cols), dtype=complex)
            F_aux = modal_shape.T @ F
            omega_n = 2*np.pi*natural_frequencies
            F_kg = (omega_n**2)

            for i, freq in enumerate(self.frequencies):

                omega = 2*np.pi*freq
                F_mg =  - (omega**2)
                F_cg = 1j*((betaH + betaV*omega)*(omega_n**2) + (alphaH + omega*alphaV)) 
                data = np.divide(1, (F_kg + F_mg + F_cg))
                diag = np.diag(data)
                solution[:,i] = modal_shape @ (diag @ F_aux[:,i])

        self.solution = self._reinsert_prescribed_dofs(solution)

        if self.flag_Clump:
            self.warning_Clump = ["There are external dampers connecting nodes to the ground. The damping,\n"+
                                    "treated as a viscous non-proportional model, will be ignored in mode \n"+
                                    "superposition. It's recommended to solve the harmonic analysis through \n"+
                                    "direct method if you want to get more accurate results!"]

        return self.solution

    def get_reactions_at_fixed_nodes(self, global_damping_values=(0,0,0,0)):

        ''' This method returns reaction forces/moments at fixed points.
            load_reactions = [lines=frequencies; columns=reactions_at_node]'''

        alphaH, betaH, alphaV, betaV = global_damping_values

        if not self.solution==[]:    

            if self.Kr == [] or self.Mr == []:

                Kr_U, Mr_U = 0, 0

            else:

                U = self.solution
                Kr = self.Kr.toarray()
                Mr = self.Mr.toarray()
                rows, cols = len(self.frequencies), Kr.shape[1] 
                            
                load_reactions = np.zeros( (rows, cols+1), dtype=complex )
                load_reactions[:,0] = self.frequencies
                U_t = U.T

                Kr_U = U_t@Kr
                Mr_U = U_t@Mr
            
            omega = 2*np.pi*self.frequencies
            omega = omega.reshape(rows,1)
            F_K = Kr_U
            F_M = -(omega**2)*Mr_U
            F_C = 1j*(betaH + omega*betaV)*Kr_U + (alphaH + omega*alphaV)*Mr_U
            load_reactions[:, 1:] = F_K + F_M + F_C

        else:
            load_reactions = []
        return load_reactions

    def get_reaction_at_springs_and_dampers(self):

        if not self.solution==[]:

            U = self.solution
            cols = self.frequencies

            global_dofs_of_springs = []
            global_dofs_of_dampers = []
            springs_stiffness = []
            dampers_dampings = []

            for node in self.assembly.nodes_with_lumped_stiffness:
                global_dofs_of_springs.append(node.global_dof)
                if node.loaded_table_for_lumped_stiffness:
                    springs_stiffness.append([np.zeros_like(self.frequencies) if value is None else value for value in node.lumped_stiffness])
                else:
                    springs_stiffness.append([np.zeros_like(self.frequencies) if value is None else np.ones_like(self.frequencies)*value for value in node.lumped_stiffness])

            for node in self.assembly.nodes_with_lumped_dampings:
                global_dofs_of_dampers.append(node.global_dof)
                if node.loaded_table_for_lumped_dampings:
                    dampers_dampings.append([np.zeros_like(self.frequencies) if value is None else value for value in node.lumped_dampings])
                else:
                    dampers_dampings.append([np.zeros_like(self.frequencies) if value is None else np.ones_like(self.frequencies)*value for value in node.lumped_dampings])

            global_dofs_of_springs = np.array(global_dofs_of_springs).flatten()
            global_dofs_of_dampers = np.array(global_dofs_of_dampers).flatten()
            springs_stiffness = np.array(springs_stiffness).reshape(-1,cols)
            dampers_dampings = np.array(dampers_dampings).reshape(-1,cols)

            reactions_at_springs = springs_stiffness*U[global_dofs_of_springs,:]
            reactions_at_dampers = dampers_dampings*U[global_dofs_of_dampers,:]

            return reactions_at_springs, reactions_at_dampers

                  


