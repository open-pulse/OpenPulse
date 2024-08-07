from time import time
import numpy as np
from math import pi
from scipy.sparse.linalg import eigs, spsolve
from pulse.processing.assembly_structural import AssemblyStructural
from pulse.interface.user_input.project.print_message import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"

class StructuralSolver:
    """ This class creates a Structural Solution object from input data.

    Parameters
    ----------
    preprocessor : Preprocessor object
        Structural finite element preprocessor.

    frequencies : array
        Frequencies of analysis.

    acoustic_solution : array, optional
        Solution of the acoustic FETM model. This solution is need to solve the coupled problem.
        Default is None.
    """

    def __init__(self, preprocessor, frequencies, **kwargs):

        self.acoustic_solution = kwargs.get("acoustic_solution", None)
        self.assembly = AssemblyStructural(preprocessor, frequencies, acoustic_solution=self.acoustic_solution)
        self.preprocessor = preprocessor
        self.frequencies = frequencies
        
        self.K_lump, self.M_lump, self.C_lump, self.Kr_lump, self.Mr_lump, self.Cr_lump, self.flag_Clump = self.assembly.get_lumped_matrices()
        self.K, self.M, self.Kr, self.Mr = self.assembly.get_global_matrices()
        self.K_exp_joint, self.M_exp_joint, self.Kr_exp_joint, self.Mr_exp_joint = self.assembly.get_expansion_joint_global_matrices()

        self.cache_K = self.K.copy()

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
        self.reset_stress_stiffening = False

    def update_global_matrices(self):
        self.K, self.M, self.Kr, self.Mr = self.assembly.get_global_matrices()
        # print(np.max(np.abs(self.cache_K - self.K)))
        # print(np.max(np.abs(self.K)))

    def _reinsert_prescribed_dofs(self, solution, modal_analysis=False):
        """
        This method reinsert the value of the prescribed degree of freedom in the solution. If modal analysis is performed, the values are zeros.

        Parameters
        ----------
        solution : array
            Solution data from the direct method, modal superposition or modal shapes from modal analysis.

        modal_analysis : boll, optional
            True if the modal analysis was evaluated.

        Returns
        ----------
        array
            Solution of all the degrees of freedom.
        """
        rows = solution.shape[0] + len(self.prescribed_indexes)
        cols = solution.shape[1]
        full_solution = np.zeros((rows, cols), dtype=complex)
        full_solution[self.unprescribed_indexes, :] = solution

        if len(self.prescribed_indexes) > 0:
            if modal_analysis:
                full_solution[self.prescribed_indexes, :] = np.zeros((len(self.prescribed_values),cols))
            else:
                full_solution[self.prescribed_indexes, :] = self.array_prescribed_values[:, 0:cols]
        return full_solution


    def get_loads_for_stress_stiffening(self):
        """ This method returns the loads relative to internal pressure only for
            stress stiffening analysis.
        """
        return self.assembly.get_global_loads_for_stress_stiffening()


    def get_combined_loads(self, static_analysis=False):
        """
        This method adds the effects of prescribed displacement and rotation into global loads vector.

        Parameters
        ----------
        global_damping : list of floats.
            Damping coefficients alpha viscous, beta viscous, alpha histeretic, and beta histeretic.

        Returns
        ----------
        array
            Force and moment global loads. Each column corresponds to a frequency of analysis.
        """

        unprescribed_indexes = self.unprescribed_indexes
        alphaV, betaV, alphaH, betaH = self.preprocessor.global_damping

        F = self.assembly.get_global_loads(static_analysis=static_analysis)

        if static_analysis:
            _frequencies = np.array([0.], dtype=float)
        else:
            _frequencies = self.frequencies       

        cols = len(_frequencies)
        rows = len(unprescribed_indexes)
        F_eq = np.zeros((rows,cols), dtype=complex)
        
        if np.sum(self.array_prescribed_values) != 0:
            
            Kr_add_lump = complex(0)
            Mr_add_lump = complex(0)
            Cr_add_lump = complex(0)
            
            Kr = (self.Kr.toarray())[unprescribed_indexes, :]
            _Mr = (self.Mr.toarray())[unprescribed_indexes, :] + (self.Mr_exp_joint.toarray())[unprescribed_indexes, :]
            
            for i, freq in enumerate(_frequencies):
                
                _Kr = Kr + (self.Kr_exp_joint[i].toarray())[unprescribed_indexes, :]
                Kr_add = np.sum(_Kr*self.array_prescribed_values[:,i], axis=1)
                Mr_add = np.sum(_Mr*self.array_prescribed_values[:,i], axis=1)
                
                if self.nodes_connected_to_springs != []:
                    Kr_lump_i = (self.Kr_lump[i].toarray())[unprescribed_indexes, :]
                    Kr_add_lump = np.sum(Kr_lump_i*self.array_prescribed_values[:,i], axis=1)

                if self.nodes_with_lumped_masses != []:
                    Mr_lump_i = (self.Mr_lump[i].toarray())[unprescribed_indexes, :]
                    Mr_add_lump = np.sum(Mr_lump_i*self.array_prescribed_values[:,i], axis=1)

                if self.nodes_connected_to_dampers != []:
                    Cr_lump_i = (self.Cr_lump[i].toarray())[unprescribed_indexes, :]
                    Cr_add_lump = np.sum(Cr_lump_i*self.array_prescribed_values[:,i], axis=1)

                omega = 2*np.pi*freq
                F_Kadd = Kr_add + Kr_add_lump
                F_Madd = (-(omega**2))*(Mr_add + Mr_add_lump) 
                F_Cadd = 1j*((betaH + omega*betaV)*Kr_add + (alphaH + omega*alphaV)*Mr_add)
                F_Cadd_lump = 1j*omega*Cr_add_lump
                F_eq[:, i] = F_Kadd + F_Madd + F_Cadd + F_Cadd_lump

        F_combined = F - F_eq

        return F_combined


    def modal_analysis(self, K=[], M=[], modes=20, which='LM', sigma=0.01, harmonic_analysis=False):
        """
        This method evaluates the FEM acoustic modal analysis. The FETM formulation is not suitable to performe modal analysis.

        Parameters
        ----------
        modes : int, optional
            Number of acoustic modes to be evaluated.
            Default is 20.

        which : str, ['LM' | 'SM' | 'LR' | 'SR' | 'LI' | 'SI'], optional
            Which `k` eigenvectors and eigenvalues to find:
                'LM' : largest magnitude
                'SM' : smallest magnitude
                'LR' : largest real part
                'SR' : smallest real part
                'LI' : largest imaginary part
                'SI' : smallest imaginary part
            Default is 'LM'.

        sigma : float, optional
            Find eigenvalues near sigma in (rad/s)^2 using shift-invert mode. 

        harmonic_analysis : boll, optional
            True when the modal analysis is used to perform mode superposition. False otherwise.
            Default is False.

        Returns
        ----------
        natural_frequencies : array
            Natural frequencies.

        modal_shapes : array
            Modal shapes
        """

        if K==[] and M==[]:

            if self.preprocessor.stress_stiffening_enabled:
                static_solution = self.static_analysis()
                self.preprocessor.update_nodal_solution_info(np.real(static_solution))
                self.update_global_matrices()
  
            Kadd_lump = self.K + self.K_exp_joint[0] + self.K_lump[0]
            Madd_lump = self.M + self.M_exp_joint + self.M_lump[0]
            ##Note: stiffness and mass/moment of inertia parameters imported from tables are not considered in modal analysis, only single values are allowable.
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
                        self.warning_Modal_prescribedDOFs = ["The Prescribed DOFs of non-zero values have been ignored in the modal analysis.\n"+
                                                            "The null value has been attributed to those DOFs with non-zero values."]

        if self.stop_processing():
            return None, None        
        
        return natural_frequencies, modal_shape


    def direct_method(self):
        """
        This method evaluates the harmonic analysis through direct method. It is suitable for Viscous Proportional and Hysteretic Proportional damping models.

        Parameters
        ----------
        global_damping : list of floats.
            Damping coefficients alpha viscous, beta viscous, alpha histeretic, and beta histeretic.

        Returns
        ----------
        array
            Solution. Each column corresponds to a frequency of analysis. Each row corresponds to a degree of freedom.
        """

        alphaV, betaV, alphaH, betaH = self.preprocessor.global_damping

        if self.preprocessor.stress_stiffening_enabled:
            static_solution = self.static_analysis()
            self.preprocessor.update_nodal_solution_info(np.real(static_solution))
            self.update_global_matrices()

        rows = self.K.shape[0]
        cols = len(self.frequencies)

        F = self.get_combined_loads()
        solution = np.zeros((rows, cols), dtype=complex)
        
        for i, freq in enumerate(self.frequencies):

            omega = 2*np.pi*freq
            
            # F_K = (self.K + self.K_lump[i])
            # F_M =  (-(omega**2))*(self.M + self.M_lump[i])
            # F_C = 1j*(( betaH + omega*betaV )*self.K + ( alphaH + omega*alphaV )*self.M)

            F_K = (self.K + self.K_exp_joint[i] + self.K_lump[i])
            F_M =  (-(omega**2))*(self.M + self.M_exp_joint + self.M_lump[i])
            F_C = 1j*(( betaH + omega*betaV )*(self.K + self.K_exp_joint[i]) + ( alphaH + omega*alphaV )*(self.M + self.M_exp_joint))

            F_Clump = 1j*omega*self.C_lump[i]
            
            A = F_K + F_M + F_C + F_Clump
            solution[:,i] = spsolve(A, F[:,i])

            if self.stop_processing():
                return None

        self.solution = self._reinsert_prescribed_dofs(solution)

        return self.solution


    def mode_superposition(self, modes, fastest=True):
        """
        This method evaluates the harmonic analysis through mode superposition method. It is suitable for Viscous Proportional and Hysteretic Proportional damping models.

        Parameters
        ----------
        global_damping : list of floats.
            Damping coefficients alpha viscous, beta viscous, alpha histeretic, and beta histeretic.

        F_loaded : ,optional.
            
            Default None.

        fastest : boll, optional.
            True if 3D matrix solution procedure must be used. False otherwise.
            Default True.

        Returns
        ----------
        array
            Solution. Each column corresponds to a frequency of analysis. Each row corresponds to a degree of freedom.
        """
        global_damping = self.preprocessor.global_damping
        alphaV, betaV, alphaH, betaH = global_damping

        if np.sum(self.prescribed_values)>0:
            solution = self.direct_method(global_damping)
            self.flag_ModeSup_prescribed_NonNull_DOFs = True
            self.warning_ModeSup_prescribedDOFs = "The Harmonic Analysis of prescribed DOF's problems \nhad been solved through the Direct Method!"
            return solution
        else:
            F = self.assembly.get_global_loads(loads_matrix3D=fastest)
            if self.preprocessor.stress_stiffening_enabled:
                static_solution = self.static_analysis()
                self.preprocessor.update_nodal_solution_info(np.real(static_solution))
                self.update_global_matrices()
            
            # Kadd_lump = self.K + self.K_lump[0]
            # Madd_lump = self.M + self.M_lump[0]
            Kadd_lump = self.K + self.K_exp_joint[0] + self.K_lump[0]
            Madd_lump = self.M + self.M_exp_joint + self.M_lump[0]

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

            if self.stop_processing():
                return None
        
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

                if self.stop_processing():
                    return None

        self.solution = self._reinsert_prescribed_dofs(solution)

        if self.flag_Clump:
            self.warning_Clump = ["There are external dampers connecting nodes to the ground. The damping,\n"+
                                    "treated as a viscous non-proportional model, will be ignored in mode \n"+
                                    "superposition. It's recommended to solve the harmonic analysis through \n"+
                                    "direct method if you want to get more accurate results!"]

        return self.solution

    def static_analysis(self):
        """
        This method evaluates the static analysis through the direct method. This method is evaluated whenever stress stiffening effects are enabled.
        Parameters
        ----------
        global_damping : list of floats.
            Damping coefficients alpha viscous, beta viscous, alpha histeretic and beta histeretic.
        Returns
        ----------
        ????
            Gets the nodal results at the global coordinate system and updates the global matrices to get into account the stress stiffening effect. 
        """
       
        alphaV, betaV, alphaH, betaH = self.preprocessor.global_damping
        # F = self.assembly.get_global_loads_for_static_analysis()
        F = self.get_combined_loads(static_analysis=True)

        rows = self.K.shape[0]
        cols = 1
        solution = np.zeros((rows, cols), dtype=complex)
        
        omega = 0

        F_K = (self.K + self.K_exp_joint[0] + self.K_lump[0])
        F_M =  (-(omega**2))*(self.M + self.M_exp_joint + self.M_lump[0])
        F_C = 1j*(( betaH + omega*betaV )*(self.K + self.K_exp_joint[0]) + 
                  ( alphaH + omega*alphaV )*(self.M + self.M_exp_joint))
        
        F_Clump = 1j*omega*self.C_lump[0]
        A = F_K + F_M + F_C + F_Clump

        solution[:,0] = spsolve(A, F[:,0])
        self.solution = self._reinsert_prescribed_dofs(solution)

        return self.solution


    def get_reactions_at_fixed_nodes(self):
        """
        This method evaluates reaction forces and moments at fixed nodes.

        Parameters
        ----------
        global_damping : list of floats.
            Damping coefficients alpha viscous, beta viscous, alpha histeretic, and beta histeretic.

        Returns
        ----------
        array
            Reactions. Each column corresponds to a frequency of analysis. Each row corresponds to a fixed degree of freedom.
        """

        alphaH, betaH, alphaV, betaV = self.preprocessor.global_damping
        load_reactions = {}
        if self.solution is not None:    

            if self.Kr == [] or self.Mr == []:
                return None

            else:

                rows = len(self.frequencies)
                cols = len(self.prescribed_indexes)
                _reactions = np.zeros((rows, cols), dtype=complex)

                Ut = self.solution.T
                Kr = self.Kr.toarray()
                Mr = self.Mr.toarray() + self.Mr_exp_joint.toarray()
                Ut_Mr = Ut@Mr

                for j, freq in enumerate(self.frequencies):
                    
                    omega = 2*np.pi*freq
                    # Ut_Kr = Ut@(Kr+self.Kr_exp_joint[j].toarray())

                    # F_K = Ut_Kr[j,:]
                    # F_M = -(omega**2)*Ut_Mr[j,:]
                    # F_C = 1j*((betaH + omega*betaV)*Ut_Kr[j,:] + (alphaH + omega*alphaV)*Ut_Mr[j,:])

                    Ut_Kr = Ut[j,:]@(Kr+self.Kr_exp_joint[j].toarray())
                    F_K = Ut_Kr
                    F_M = -(omega**2)*Ut_Mr[j,:]
                    F_C = 1j*((betaH + omega*betaV)*Ut_Kr + (alphaH + omega*alphaV)*Ut_Mr[j,:])
                    _reactions[j,:] = F_K + F_M + F_C
                
                # Mr = self.Mr.toarray()
                # Ut_Kr = Ut@Kr
                # Ut_Mr = Ut@Mr
                
                # omega = 2*np.pi*self.frequencies
                # omega = omega.reshape(rows,1)
                    
                # F_K = Ut_Kr
                # F_M = -(omega**2)*Ut_Mr
                # F_C = 1j*((betaH + omega*betaV)*Ut_Kr + (alphaH + omega*alphaV)*Ut_Mr)
                # _reactions = F_K + F_M + F_C

                for i, prescribed_index in enumerate(self.prescribed_indexes):
                    load_reactions[prescribed_index] =  _reactions[:,i]
                return load_reactions


    def get_reactions_at_springs_and_dampers(self):
        """
        This method evaluates reaction forces and moments at lumped springs and dampers connected the structure and the ground.

        Returns
        ----------
        array
            Reactions. Each column corresponds to a frequency of analysis. Each row corresponds to a spring and damper.
        """

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

            for node in self.preprocessor.nodes_connected_to_springs:
                global_dofs_of_springs.append(node.global_dof)
                if node.loaded_table_for_lumped_stiffness:
                    springs_stiffness.append([np.zeros_like(self.frequencies) if value is None else value for value in node.lumped_stiffness])
                else:
                    springs_stiffness.append([np.zeros_like(self.frequencies) if value is None else np.ones_like(self.frequencies)*value for value in node.lumped_stiffness])

            for node in self.preprocessor.nodes_connected_to_dampers:
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


    def stress_calculate(self, pressure_external = 0, damping = False, _real_values=False):
        """
        This method evaluates reaction forces and moments at lumped springs and dampers connected the structure and the ground.

        Parameters
        ----------
        global_damping : list of floats.
            Damping coefficients alpha viscous, beta viscous, alpha histeretic, and beta histeretic.

        pressure_external : float, optional
            Static pressure difference between atmosphere and the fluid in the pipeline.
            Default is 0.
            
        damping : boll, optional.
            True if the damping must be considered when evaluating the stresses. False otherwise.
            Default is False

        Returns
        ----------
        array
            Stresses. Each column corresponds to a element. The rows corresponds to the:
                Normal axial stress
                Normal bending-y stress 
                Normal bending-z stress 
                Hoop stress
                Torsional shear
                Transversal-xy shear
                Transversal-xz shear
        """

        self.stress_field_dict = dict()

        if damping:
            _, betaH, _, betaV = self.preprocessor.global_damping
        else:
            betaH = betaV = 0

        elements = self.preprocessor.structural_elements.values()
        omega = 2 * pi * self.frequencies.reshape(1,-1)
        damping = np.ones([6,1]) @  (1 + 1j*( betaH + omega * betaV ))
        p0 = pressure_external

        for element in elements:

            if element.element_type in ['beam_1', 'expansion_joint', 'valve']:
                element.stress = np.zeros((7, len(self.frequencies)))
            
            elif element.element_type == 'pipe_1':
                # Internal Loads
                structural_dofs = np.r_[element.first_node.global_dof, element.last_node.global_dof]

                if self.solution is None:
                    title = "Empty solution"
                    message = "A strutural analysis must be performed to obtain the stress field."
                    PrintMessageInput([window_title_1, title, message])
                    return {}

                u = self.solution[structural_dofs, :]
                Dab = element._Dab
                Bab = element._Bab

                Dts = element._Dts
                Bts = element._Bts

                rot = element._rot
                T = element.cross_section.principal_axis_translation
                
                normal = Dab @ Bab @ T @ rot @ u
                shear = Dts @ Bts @ T @ rot @ u

                element.internal_load = np.multiply(np.r_[normal, shear], damping)
                # Stress
                do = element.cross_section.outer_diameter
                di = element.cross_section.inner_diameter
                ro = do/2
                area = element.cross_section.area
                Iy = element.cross_section.second_moment_area_y
                Iz = element.cross_section.second_moment_area_z
                J = element.cross_section.polar_moment_area
                nu = element.material.poisson_ratio

                acoustic_dofs = np.r_[element.first_node.global_index, element.last_node.global_index]
                
                if self.acoustic_solution is not None:
                    p = self.acoustic_solution[acoustic_dofs, :]
                else:
                    p = np.zeros((2, len(self.frequencies)))
                pm = np.sum(p,axis=0)/2

                if element.wall_formulation == "thick_wall":
                    hoop_stress = (2*pm*di**2 - p0*(do**2 + di**2))/(do**2 - di**2)
                    radial_stress =  -2*nu*(pm*di**2 - p0*do**2)/(do**2 - di**2)
                if element.wall_formulation == "thin_wall":
                    hoop_stress = pm
                    radial_stress = -nu*pi*(do/(do-di) - 1)
                   
                stress_data = np.c_[element.internal_load[0]/area - radial_stress,
                                    element.internal_load[1] * ro/Iy,
                                    element.internal_load[2] * ro/Iz,
                                    hoop_stress,
                                    element.internal_load[3] * ro/J,
                                    element.internal_load[4]/area,
                                    element.internal_load[5]/area   ].T
                
                if _real_values:
                    element.stress = np.real(stress_data)
                else:
                    element.stress = stress_data

            self.stress_field_dict[element.index] = element.stress
            
        return self.stress_field_dict

    def stop_processing(self):
        if self.preprocessor.stop_processing:
            print("\nProcessing interruption was requested by the user. \nSolution interruped.")
            return True