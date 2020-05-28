from time import time
import numpy as np
from scipy.sparse.linalg import eigs, spsolve

from pulse.processing.assembly_structural import AssemblyStructural

class SolutionStructural:

    def __init__(self, mesh, **kwargs):

        self.acoustic_solution = kwargs.get("acoustic_solution", None)
        self.assembly = AssemblyStructural(mesh, acoustic_solution=self.acoustic_solution)

        self.K_lump, self.M_lump, self.C_lump, self.Kr_lump, self.Mr_lump, self.Cr_lump, self.flag_Clump = self.assembly.get_lumped_matrices()
        self.K, self.M, self.Kr, self.Mr = self.assembly.get_global_matrices()
        self.Kadd_lump = self.K + self.K_lump
        self.Madd_lump = self.M + self.M_lump

        self.prescribed_indexes = self.assembly.get_prescribed_indexes()
        self.prescribed_values = self.assembly.get_prescribed_values()
        self.unprescribed_indexes = self.assembly.get_unprescribed_indexes()
        self.flag_Modal_prescribed_NonNull_DOFs = False
        self.flag_ModeSup_prescribed_NonNull_DOFs = False
        self.warning_Clump = ""
        self.warning_ModeSup_prescribedDOFs = ""
        self.warning_Modal_prescribedDOFs = ""


    def _reinsert_prescribed_dofs(self, solution, prescribed_indexes, prescribed_values):
        rows = solution.shape[0] + len(prescribed_indexes)
        cols = solution.shape[1]
        unprescribed_indexes = np.delete(np.arange(rows), prescribed_indexes)

        full_solution = np.zeros((rows, cols), dtype=complex)
        full_solution[unprescribed_indexes, :] = solution
        full_solution[prescribed_indexes, :] = np.ones(cols)*np.array(prescribed_values).reshape(-1, 1)

        return full_solution


    def get_combined_loads(self, frequencies, global_damping_values, lump_damping_values, is_viscous_lumped):

        F = self.assembly.get_global_loads(frequencies)
        
        unprescribed_indexes = self.unprescribed_indexes
        prescribed_values = self.prescribed_values

        alphaH_lump, betaH_lump, alphaV_lump, betaV_lump = lump_damping_values 
        alphaH, betaH, alphaV, betaV = global_damping_values

        if is_viscous_lumped:
            proportional_damping_lumped = False
        else:
            proportional_damping_lumped = True
        
        Kr = (self.Kr.toarray())[unprescribed_indexes, :]
        Mr = (self.Mr.toarray())[unprescribed_indexes, :]

        Kr_lump = (self.Kr_lump.toarray())[unprescribed_indexes, :]
        Mr_lump = (self.Mr_lump.toarray())[unprescribed_indexes, :]
        Cr_lump = (self.Cr_lump.toarray())[unprescribed_indexes, :]

        if Kr == [] or Mr == []:
            Kr_add = 0
            Mr_add = 0
        else:
            Kr_add = np.sum(Kr*prescribed_values, axis=1)
            Mr_add = np.sum(Mr*prescribed_values, axis=1)
        
        Kr_add_lump = np.sum(Kr_lump*prescribed_values, axis=1)
        Mr_add_lump = np.sum(Mr_lump*prescribed_values, axis=1)
        Cr_add_lump = np.sum(Cr_lump*prescribed_values, axis=1)

        rows = len(Kr_add)
        cols = len(frequencies)
        F_eq = np.zeros((rows,cols), dtype=complex)

        for i, freq in enumerate(frequencies):

            omega = 2*np.pi*freq

            F_Kadd = Kr_add + Kr_add_lump
            F_Madd = (-(omega**2))*(Mr_add + Mr_add_lump) 
            F_Cadd = 1j*((betaH + omega*betaV)*Kr_add + (alphaH + omega*alphaV)*Mr_add)

            if proportional_damping_lumped:
                F_Cadd_lump = 1j*((betaH_lump + omega*betaV_lump)*Kr_add_lump + (alphaH_lump + omega*alphaV_lump)*Mr_add_lump)
            else:
                F_Cadd_lump = 1j*omega*Cr_add_lump

            F_eq[:, i] = F_Kadd + F_Madd + F_Cadd + F_Cadd_lump

        F_combined = F - F_eq
        
        return F_combined


    def modal_analysis(self, K=[], M=[], modes=20, which='LM', sigma=0.01, harmonic_analysis=False):

        if K==[] and M==[]:
            Kadd_lump = self.Kadd_lump
            Madd_lump = self.Madd_lump 
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

            modal_shape = self._reinsert_prescribed_dofs( modal_shape, self.prescribed_indexes, np.zeros_like(self.prescribed_values) )

            if sum(self.prescribed_values)>0:
                self.flag_Modal_prescribed_NonNull_DOFs = True
                self.warning_Modal_prescribedDOFs = ["The Prescribed DOFs of non-zero values has been ignored in the modal analysis.\n"+
                                                      "The null value has been attributed to those DOFs with non-zero values."]

        return natural_frequencies, modal_shape


    def direct_method(self, frequencies, global_damping_values=(0,0,0,0), lump_damping_values=(0,0,0,0), is_viscous_lumped=False):

        """ 
            Perform an harmonic analysis through direct method and returns the response of
            all nodes due the external or internal equivalent load. It has been implemented two
            different damping models: Viscous Proportional and Hysteretic Proportional
            Entries for Viscous Proportional Model Damping: (alpha_v, beta_v)
            Entries for Hyteretic Proportional Model Damping: (alpha_h, beta_h)
        """

        alphaH, betaH, alphaV, betaV = global_damping_values
        alphaH_lump, betaH_lump, alphaV_lump, betaV_lump = lump_damping_values

        if is_viscous_lumped:
            proportional_damping_lumped = False
        else:
            proportional_damping_lumped = True
        
        Kadd_lump, Madd_lump, K, M, K_lump, M_lump, C_lump = self.Kadd_lump, self.Madd_lump, self.K, self.M, self.K_lump, self.M_lump, self.C_lump 
        
        F = self.get_combined_loads(frequencies, global_damping_values, lump_damping_values, is_viscous_lumped)

        rows = Kadd_lump.shape[0]
        cols = len(frequencies)
        solution = np.zeros((rows, cols), dtype=complex)

        alphaH, betaH, alphaV, betaV = global_damping_values
    
        for i, freq in enumerate(frequencies):

            omega = 2*np.pi*freq
            
            F_K = Kadd_lump
            F_M =  (-(omega**2))*Madd_lump
            F_C = 1j*(( betaH + omega*betaV )*K + ( alphaH + omega*alphaV )*M)

            if is_viscous_lumped:
                F_Clump = 1j*omega*C_lump
            
            if proportional_damping_lumped:
                F_Clump = 1j*(( betaH_lump + omega*betaV_lump )*K_lump + ( alphaH_lump + omega*alphaV_lump )*M_lump)

            A = F_K + F_M + F_C + F_Clump
            solution[:,i] = spsolve(A, F[:,i])

        solution = self._reinsert_prescribed_dofs(solution, self.prescribed_indexes, self.prescribed_values)

        return solution

    def mode_superposition(self, frequencies, modes, F_loaded=None, global_damping_values=(0,0,0,0), lump_damping_values=(0,0,0,0), fastest=True):
        
        """ 
            Perform an harmonic analysis through superposition method and returns the response of
            all nodes due the external or internal equivalent load. It has been implemented two
            different damping models: Viscous Proportional and Hysteretic Proportional
            Entries for Viscous Proportional Model Damping: (alpha_v, beta_v)
            Entries for Hyteretic Proportional Model Damping: (alpha_h, beta_h)
        """
        alphaH, betaH, alphaV, betaV = global_damping_values

        if np.sum(self.prescribed_values)>0:
            solution = self.direct_method(frequencies, global_damping_values=global_damping_values, lump_damping_values=lump_damping_values)
            self.flag_ModeSup_prescribed_NonNull_DOFs = True
            self.warning_ModeSup_prescribedDOFs = "The Harmonic Analysis of prescribed DOF's problems \nhad been solved through the Direct Method!"
            return solution
        else:
            F = self.assembly.get_global_loads( frequencies, loads_matrix3D=fastest)
            Kadd_lump = self.Kadd_lump
            Madd_lump = self.Madd_lump

        #TODO: in the future version implement lets F_loaded operational

        natural_frequencies, modal_shape = self.modal_analysis(K=Kadd_lump, M=Madd_lump, modes=modes, harmonic_analysis=True)
        rows = Kadd_lump.shape[0]
        cols = len(frequencies)

        if fastest:    
        
            number_modes = len(natural_frequencies)
            omega = 2*np.pi*frequencies.reshape(cols,1,1)
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

            for i, freq in enumerate(frequencies):

                omega = 2*np.pi*freq
                F_mg =  - (omega**2)
                F_cg = 1j*((betaH + betaV*omega)*(omega_n**2) + (alphaH + omega*alphaV)) 
                data = np.divide(1, (F_kg + F_mg + F_cg))
                diag = np.diag(data)
                solution[:,i] = modal_shape @ (diag @ F_aux[:,i])

        solution = self._reinsert_prescribed_dofs(solution, self.prescribed_indexes, self.prescribed_values)

        if self.flag_Clump:
            self.warning_Clump = ["There are external dampers connecting nodes to the ground. The damping,\n"+
                                    "treated as a viscous non-proportional model, will be ignored in mode \n"+
                                    "superposition. It's recommended to solve the harmonic analysis through \n"+
                                    "direct method if you want to get more accurate results!"]

        return solution

    def get_reactions_at_fixed_nodes(self, frequencies, U, global_damping_values=(0,0,0,0)):

        ''' This method returns reaction forces/moments at fixed points.
            load_reactions = [lines=frequencies; columns=reactions_at_node]'''

        alphaH, betaH, alphaV, betaV = global_damping_values

        if not U==[]:    

            if self.Kr == [] or self.Mr == []:

                Kr_U, Mr_U = 0, 0

            else:

                Kr = self.Kr.toarray()
                Mr = self.Mr.toarray()
                rows, cols = len(frequencies), Kr.shape[1] 
                            
                load_reactions = np.zeros( (rows, cols+1), dtype=complex )
                load_reactions[:,0] = frequencies
                U_t = U.T

                Kr_U = U_t@Kr
                Mr_U = U_t@Mr
            
            omega = 2*np.pi*frequencies
            omega = omega.reshape(rows,1)
            F_K = Kr_U
            F_M = -(omega**2)*Mr_U
            F_C = 1j*(betaH + omega*betaV)*Kr_U + (alphaH + omega*alphaV)*Mr_U
            load_reactions[:, 1:] = F_K + F_M + F_C

        else:
            load_reactions = []
        return load_reactions