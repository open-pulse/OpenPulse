from time import time
import numpy as np
from math import pi
from scipy.sparse.linalg import eigs, spsolve
from pulse.processing.assembly_structural import AssemblyStructural
from pulse.utils import error

class SolutionStructural:

    def __init__(self, mesh, frequencies, **kwargs):

        self.acoustic_solution = kwargs.get("acoustic_solution", None)
        self.assembly = AssemblyStructural(mesh, frequencies, acoustic_solution=self.acoustic_solution)
        self.mesh = mesh
        self.frequencies = frequencies
        
        self.K_lump, self.M_lump, self.C_lump, self.Kr_lump, self.Mr_lump, self.Cr_lump, self.flag_Clump = self.assembly.get_lumped_matrices()
        self.K, self.M, self.Kr, self.Mr = self.assembly.get_global_matrices()

        self.nodes_connected_to_springs = self.assembly.nodes_connected_to_springs
        self.nodes_with_lumped_masses = self.assembly.nodes_with_lumped_masses
        self.nodes_connected_to_dampers = self.assembly.nodes_connected_to_dampers

        self.prescribed_indexes = self.assembly.get_prescribed_indexes()
        self.prescribed_values, self.array_prescribed_values = self.assembly.get_prescribed_values()
        self.unprescribed_indexes = self.assembly.get_unprescribed_indexes()

        self.flag_Modal_prescribed_NonNull_DOFs = False
        self.flag_ModeSup_prescribed_NonNull_DOFs = False
        self.warning_Clump = ""
        self.warning_ModeSup_prescribedDOFs = ""
        self.warning_Modal_prescribedDOFs = ""
        self.solution = None

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


    def get_combined_loads(self, global_damping):
        # t0 = time()
        alphaV, betaV, alphaH, betaH = global_damping

        F = self.assembly.get_global_loads()
        unprescribed_indexes = self.unprescribed_indexes

        rows = len(unprescribed_indexes)
        cols = len(self.frequencies)
        F_eq = np.zeros((rows,cols), dtype=complex)
        
        if np.sum(self.array_prescribed_values) != 0:
            
            Kr_add_lump = complex(0)
            Mr_add_lump = complex(0)
            Cr_add_lump = complex(0)
            
            Kr = (self.Kr.toarray())[unprescribed_indexes, :]
            Mr = (self.Mr.toarray())[unprescribed_indexes, :]
            
            for i, freq in enumerate(self.frequencies):
                
                Kr_lump_i = (self.Kr_lump[i].toarray())[unprescribed_indexes, :]
                Mr_lump_i = (self.Mr_lump[i].toarray())[unprescribed_indexes, :]
                Cr_lump_i = (self.Cr_lump[i].toarray())[unprescribed_indexes, :]

                Kr_add = np.sum(Kr*self.array_prescribed_values[:,i], axis=1)
                Mr_add = np.sum(Mr*self.array_prescribed_values[:,i], axis=1)
                
                if self.nodes_connected_to_springs != []:
                    Kr_add_lump = np.sum(Kr_lump_i*self.array_prescribed_values[:,i], axis=1)
                if self.nodes_with_lumped_masses != []:
                    Mr_add_lump = np.sum(Mr_lump_i*self.array_prescribed_values[:,i], axis=1)
                if self.nodes_connected_to_dampers != []:
                    Cr_add_lump = np.sum(Cr_lump_i*self.array_prescribed_values[:,i], axis=1)

                omega = 2*np.pi*freq
                F_Kadd = Kr_add + Kr_add_lump
                F_Madd = (-(omega**2))*(Mr_add + Mr_add_lump) 
                F_Cadd = 1j*((betaH + omega*betaV)*Kr_add + (alphaH + omega*alphaV)*Mr_add)
                F_Cadd_lump = 1j*omega*Cr_add_lump
                F_eq[:, i] = F_Kadd + F_Madd + F_Cadd + F_Cadd_lump

        # dt = time()-t0
        # print("Time elapsed: {}[s]".format(dt))

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


    def direct_method(self, global_damping):

        """ 
            Perform an harmonic analysis through direct method and returns the response of
            all nodes due the external or internal equivalent load. It has been implemented two
            different damping models: Viscous Proportional and Hysteretic Proportional
            Entries for Viscous Proportional Model Damping: (alpha_v, beta_v)
            Entries for Hyteretic Proportional Model Damping: (alpha_h, beta_h)
        """

        alphaV, betaV, alphaH, betaH = global_damping
        
        # t0 = time()
        F = self.get_combined_loads(global_damping)
        # dt = time() - t0
        # print("Time elapsed: {}[s]".format(dt))

        rows = self.K.shape[0]
        cols = len(self.frequencies)
        solution = np.zeros((rows, cols), dtype=complex)
    
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


    def mode_superposition(self, modes, global_damping, F_loaded=None, fastest=True):
        
        """ 
            Perform an harmonic analysis through superposition method and returns the response of
            all nodes due the external or internal equivalent load. It has been implemented two
            different damping models: Viscous Proportional and Hysteretic Proportional
            Entries for Viscous Proportional Model Damping: (alpha_v, beta_v)
            Entries for Hyteretic Proportional Model Damping: (alpha_h, beta_h)
        """
        alphaV, betaV, alphaH, betaH = global_damping

        if np.sum(self.prescribed_values)>0:
            solution = self.direct_method(global_damping)
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
            F_mg =  -(omega**2)
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
        load_reactions = {}
        if self.solution is not None:    

            if self.Kr == [] or self.Mr == []:
                return

            else:

                Ut = self.solution.T
                Kr = self.Kr.toarray()
                Mr = self.Mr.toarray()
                rows = len(self.frequencies)

                Ut_Kr = Ut@Kr
                Ut_Mr = Ut@Mr
            
            omega = 2*np.pi*self.frequencies
            omega = omega.reshape(rows,1)
            F_K = Ut_Kr
            F_M = -(omega**2)*Ut_Mr
            F_C = 1j*((betaH + omega*betaV)*Ut_Kr + (alphaH + omega*alphaV)*Ut_Mr)
            _reactions = F_K + F_M + F_C

            for i, prescribed_index in enumerate(self.prescribed_indexes):
                load_reactions[prescribed_index] =  _reactions[:,i]
            return load_reactions


    def get_reactions_at_springs_and_dampers(self):

        dict_reactions_at_springs = {}
        dict_reactions_at_dampers = {}

        if self.solution is not None: 

            omega = 2*np.pi*self.frequencies
            cols = len(self.frequencies)

            U = self.solution

            global_dofs_of_springs = []
            global_dofs_of_dampers = []
            springs_stiffness = []
            dampers_dampings = []

            for node in self.mesh.nodes_connected_to_springs:
                global_dofs_of_springs.append(node.global_dof)
                if node.loaded_table_for_lumped_stiffness:
                    springs_stiffness.append([np.zeros_like(self.frequencies) if value is None else value for value in node.lumped_stiffness])
                else:
                    springs_stiffness.append([np.zeros_like(self.frequencies) if value is None else np.ones_like(self.frequencies)*value for value in node.lumped_stiffness])

            for node in self.mesh.nodes_connected_to_dampers:
                global_dofs_of_dampers.append(node.global_dof)
                if node.loaded_table_for_lumped_dampings:
                    dampers_dampings.append([np.zeros_like(self.frequencies) if value is None else value for value in node.lumped_dampings])
                else:
                    dampers_dampings.append([np.zeros_like(self.frequencies) if value is None else np.ones_like(self.frequencies)*value for value in node.lumped_dampings])

            if springs_stiffness != []:
                global_dofs_of_springs = np.array(global_dofs_of_springs).flatten()
                springs_stiffness = np.array(springs_stiffness).reshape(-1,cols)
                reactions_at_springs = springs_stiffness*U[global_dofs_of_springs,:]

                for i, gdof in enumerate(global_dofs_of_springs):
                    dict_reactions_at_springs[gdof] = reactions_at_springs[i,:]

            if dampers_dampings != []:
                global_dofs_of_dampers = np.array(global_dofs_of_dampers).flatten()
                dampers_dampings = np.array(dampers_dampings).reshape(-1,cols)
                reactions_at_dampers = (1j*omega)*dampers_dampings*U[global_dofs_of_dampers,:]
            
                for i, gdof in enumerate(global_dofs_of_dampers):
                    dict_reactions_at_dampers[gdof] = reactions_at_dampers[i,:]

            return dict_reactions_at_springs, dict_reactions_at_dampers


    def stress_calculate(self, global_damping, pressure_external = 0, damping_flag = False):
        self.stress_field_dict = {}
        if damping_flag:
            _, betaH, _, betaV = global_damping
        else:
            betaH = betaV = 0
        elements = self.mesh.structural_elements.values()
        omega = 2 * pi * self.frequencies.reshape(1,-1)
        damping = np.ones([6,1]) @  (1 + 1j*( betaH + omega * betaV ))
        p0 = pressure_external

        for element in elements:
            # Internal Loads
            structural_dofs = np.r_[element.first_node.global_dof, element.last_node.global_dof]
            if self.solution is None:
                error("Strutural analysis must be performed to obtain the stress field.")
                return

            u = self.solution[structural_dofs, :]
            Dab = element._Dab
            Bab = element._Bab

            Dts = element._Dts
            Bts = element._Bts

            rot = element._rot
            T = element.cross_section.principal_axis_translation
            
            normal = Dab @ Bab @ T @ rot @ u
            shear = Dts @ Bts @ T @ rot @ u

            element.internal_load = np.multiply(np.r_[normal, shear],damping)
            # Stress
            do = element.cross_section.external_diameter
            di = element.cross_section.internal_diameter
            ro = do/2
            area = element.cross_section.area
            Iy = element.cross_section.second_moment_area_y
            Iz = element.cross_section.second_moment_area_z
            J = element.cross_section.polar_moment_area

            acoustic_dofs = np.r_[element.first_node.global_index, element.last_node.global_index]
            
            if self.acoustic_solution is not None:
                p = self.acoustic_solution[acoustic_dofs, :]
            else:
                p = np.zeros((2, len(self.frequencies)))
            pm = np.sum(p,axis=0)/2
            hoop_stress = (2*pm*di**2 - p0*(do**2 + di**2))/(do**2 - di**2)

            element.stress = np.c_[element.internal_load[0]/area,
                                   element.internal_load[2] * ro/Iy,
                                   element.internal_load[1] * ro/Iz,
                                   hoop_stress,
                                   element.internal_load[3] * ro/J,
                                   element.internal_load[4]/area,
                                   element.internal_load[5]/area].T

            self.stress_field_dict[element.index] = element.stress
            
        return self.stress_field_dict