import logging

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigs, spsolve

from pulse.interface import error_title
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.model.model import Model
from pulse.processing.assembly_structural import AssemblyStructural
# from pulse.model.elements.elements_builder import build_structural_element


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

    def __init__(self, model: Model, acoustic_solution: np.ndarray | None = None):

        self.model = model
        self.frequencies = model.frequencies

        self.acoustic_solution = acoustic_solution
        self.assembly = AssemblyStructural(model, acoustic_solution=acoustic_solution)

        self.K, self.M, self.Kr, self.Mr = self.assembly.get_global_matrices()       
        self.K_lump, self.M_lump, self.C_lump, self.Kr_lump, self.Mr_lump, self.Cr_lump, self.flag_Clump = self.assembly.get_lumped_matrices()       
        self.K_exp_joint, self.M_exp_joint, self.Kr_exp_joint, self.Mr_exp_joint = self.assembly.get_expansion_joint_global_matrices()

        self.prescribed_indexes = self.assembly.get_prescribed_indexes()
        self.prescribed_values, self.array_prescribed_values = self.assembly.get_prescribed_values()
        self.unprescribed_indexes = self.assembly.get_unprescribed_indexes()

        self.reset_variables()

    def reset_variables(self):
        
        self.natural_frequencies = None
        self.modal_shapes = None
        self.solution = None

        self.reset_stress_stiffening = False

        self.warning_Clump = ""
        self.warning_modal_prescribed_dofs = ""
        self.warning_mode_sup_prescribed_dofs = ""

        self.reactions_at_constrained_dofs = dict()
        self.reactions_at_springs = dict()
        self.reactions_at_dampers = dict()

    def update_global_matrices(self):
        self.K, self.M, self.Kr, self.Mr = self.assembly.get_global_matrices()

    def _reinsert_prescribed_dofs(self, solution, modal_analysis=False):
        """
        This method reinsert the value of the prescribed degree of freedom in the solution. If modal analysis is performed, the values are zeros.

        Parameters
        ----------
        solution : array
            Solution data from the direct method, modal superposition or modal shapes from modal analysis.

        modal_analysis : bool, optional
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
        alpha, beta, eta = self.model.global_damping

        F = self.assembly.get_global_loads(static_analysis=static_analysis)

        if static_analysis:
            _frequencies = np.array([0.], dtype=float)
        else:
            _frequencies = self.frequencies

        cols = len(_frequencies)
        rows = len(unprescribed_indexes)
        F_eq = np.zeros((rows,cols), dtype=complex)
        
        if np.sum(self.array_prescribed_values):
            
            Kr_add_lump = complex(0)
            Mr_add_lump = complex(0)
            Cr_add_lump = complex(0)

            lumped_masses = False
            lumped_stiffness = False
            lumped_dampings = False

            for (_property, *args) in self.model.properties.nodal_properties.items():
                
                if _property == "lumped_masses":
                    lumped_masses = True
                    continue

                if _property == "lumped_stiffness":
                    lumped_stiffness = True
                    continue

                if _property == "lumped_dampings":
                    lumped_dampings = True
            
            Kr = (self.Kr.toarray())[unprescribed_indexes, :]
            _Mr = (self.Mr.toarray())[unprescribed_indexes, :] + (self.Mr_exp_joint.toarray())[unprescribed_indexes, :]
            
            for i, freq in enumerate(_frequencies):
                
                _Kr = Kr + (self.Kr_exp_joint[i].toarray())[unprescribed_indexes, :]
                Kr_add = np.sum(_Kr*self.array_prescribed_values[:,i], axis=1)
                Mr_add = np.sum(_Mr*self.array_prescribed_values[:,i], axis=1)
                                
                if lumped_stiffness:
                    Kr_lump_i = (self.Kr_lump[i].toarray())[unprescribed_indexes, :]
                    Kr_add_lump = np.sum(Kr_lump_i*self.array_prescribed_values[:,i], axis=1)

                if lumped_masses:
                    Mr_lump_i = (self.Mr_lump[i].toarray())[unprescribed_indexes, :]
                    Mr_add_lump = np.sum(Mr_lump_i*self.array_prescribed_values[:,i], axis=1)

                if lumped_dampings:
                    Cr_lump_i = (self.Cr_lump[i].toarray())[unprescribed_indexes, :]
                    Cr_add_lump = np.sum(Cr_lump_i*self.array_prescribed_values[:,i], axis=1)

                omega = 2*np.pi*freq
                F_Kadd = Kr_add + Kr_add_lump
                F_Madd = (-(omega**2)) * (Mr_add + Mr_add_lump)
                F_Cadd = 1j * ((eta + omega * beta) * Kr_add + (omega * alpha) * Mr_add)
                F_Cadd_lump = 1j * omega * Cr_add_lump
                F_eq[:, i] = F_Kadd + F_Madd + F_Cadd + F_Cadd_lump

        F_combined = F - F_eq

        return F_combined


    def modal_analysis(
            self, 
            K: csr_matrix | None = None, 
            M: csr_matrix | None = None,
            number_of_modes : int = 40,
            which : str = "LM",
            sigma_factor : float = 0.01,
            harmonic_analysis : bool = False,
            ):
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

        harmonic_analysis : bool, optional
            True when the modal analysis is used to perform mode superposition. False otherwise.
            Default is False.

        Returns
        ----------
        natural_frequencies : array
            Natural frequencies.

        modal_shapes : array
            Modal shapes
        """

        self.warning_modal_prescribed_dofs = ""

        if not (isinstance(K, csr_matrix) and isinstance(M, csr_matrix)):

            if self.model.preprocessor.stress_stiffening_enabled:
                static_solution = self.static_analysis()
                self.model.preprocessor.update_nodal_solution_info(np.real(static_solution))
                self.update_global_matrices()
  
            # NOTE: stiffness and mass/moment of inertia parameters imported from tables  
            # are not considered in modal analysis, only single values are allowable

            K = self.K + self.K_exp_joint[0] + self.K_lump[0]
            M = self.M + self.M_exp_joint + self.M_lump[0]

        eigen_values, eigen_vectors = eigs(K, M=M, k=number_of_modes, which=which, sigma=sigma_factor)

        positive_real = np.absolute(np.real(eigen_values))
        natural_frequencies = np.sqrt(positive_real) / (2 * np.pi)
        # modal_shapes = np.real(eigen_vectors)

        index_order = np.argsort(natural_frequencies)
        natural_frequencies = natural_frequencies[index_order]
        modal_shapes = eigen_vectors[:, index_order]

        if not harmonic_analysis:
            modal_shapes = self._reinsert_prescribed_dofs(modal_shapes, modal_analysis=True)
            for value in self.prescribed_values:
                if value is not None:
                    if (isinstance(value, complex) and value != complex(0)) or (isinstance(value, np.ndarray) and sum(value) != complex(0)):
                        self.warning_modal_prescribed_dofs  = "The Prescribed DOFs of non-zero values have been ignored in the modal analysis. "
                        self.warning_modal_prescribed_dofs += "The null value has been attributed to those DOFs with non-zero values."

        if self.stop_processing():
            self.modal_shapes = None
            self.natural_frequencies = list()
            return None, None

        self.natural_frequencies = natural_frequencies
        self.modal_shapes = np.real(modal_shapes)

        return natural_frequencies, modal_shapes


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

        alpha, beta, eta = self.model.global_damping

        if self.model.preprocessor.stress_stiffening_enabled:
            static_solution = self.static_analysis()
            self.model.preprocessor.update_nodal_solution_info(np.real(static_solution))
            self.update_global_matrices()

        rows = self.K.shape[0]
        cols = len(self.frequencies)

        F = self.get_combined_loads()
        solution = np.zeros((rows, cols), dtype=complex)
        
        #TODO: remember to remove these lines
        # np.savetxt("loads.csv", F, delimiter=",", fmt="%.12e")
        # np.savetxt("frequencies.dat", self.frequencies)

        for i, freq in enumerate(self.frequencies):

            logging.info(f"Solution step {i+1} and frequency {freq : .3f} Hz [{i+1}/{len(self.frequencies)}]")

            omega = 2*np.pi*freq

            # F_K = (self.K + self.K_lump[i])
            # F_M =  (-(omega**2))*(self.M + self.M_lump[i])
            # F_C = 1j*(( beta_h + omega*beta_v )*self.K + ( alpha_h + omega*alpha_v )*self.M)

            F_K = (self.K + self.K_exp_joint[i] + self.K_lump[i])
            F_M =  (-(omega**2)) * (self.M + self.M_exp_joint + self.M_lump[i])
            F_C = 1j * ((eta + omega * beta) * (self.K + self.K_exp_joint[i]) + (omega * alpha) * (self.M + self.M_exp_joint))

            F_Clump = 1j * omega * self.C_lump[i]
            
            A = F_K + F_M + F_C + F_Clump
            solution[:, i] = spsolve(A, F[:, i])

            if self.stop_processing():
                return None

        self.solution = self._reinsert_prescribed_dofs(solution)

        return self.solution


    def mode_superposition(self, fastest: bool=True):
        """
        This method evaluates the harmonic analysis through mode superposition method. It is suitable for Viscous 
        Proportional and Hysteretic Proportional damping models.

        Parameters
        ----------
        fastest : bool, optional.
            True if 3D matrix solution procedure must be used. False otherwise.
            Default True.

        Returns
        ----------
        array
            Solution. Each column corresponds to a frequency of analysis. Each row corresponds to a degree of freedom.
        """
        number_of_modes = self.model.number_of_modes
        global_damping = self.model.global_damping
        alpha, beta, eta = global_damping

        self.warning_mode_sup_prescribed_dofs = ""

        if np.sum(self.prescribed_values) > 0:
            solution = self.direct_method(global_damping)
            self.warning_mode_sup_prescribed_dofs = "The Harmonic Analysis of prescribed DOF's problems "
            self.warning_mode_sup_prescribed_dofs += "had been solved through the Direct Method."
            return solution

        else:
            F = self.assembly.get_global_loads(loads_matrix3D=fastest)
            if self.model.preprocessor.stress_stiffening_enabled:
                static_solution = self.static_analysis()
                self.model.preprocessor.update_nodal_solution_info(np.real(static_solution))
                self.update_global_matrices()
            
            Kadd_lump = self.K + self.K_exp_joint[0] + self.K_lump[0]
            Madd_lump = self.M + self.M_exp_joint + self.M_lump[0]

        if not self.assembly.no_table:
            return

        #TODO: in the future version implement lets F_loaded operational

        natural_frequencies, modal_shape = self.modal_analysis(
            K = Kadd_lump,
            M = Madd_lump,
            number_of_modes = number_of_modes,
            harmonic_analysis = True,
            )

        rows = Kadd_lump.shape[0]
        cols = len(self.frequencies)

        if fastest:

            number_modes = len(natural_frequencies)
            omega = 2 * np.pi * self.frequencies.reshape(cols, 1, 1)
            omega_n = 2 * np.pi * natural_frequencies

            F_kg = (omega_n**2)
            F_mg =  -(omega**2)
            F_cg = 1j * ((eta + beta * omega) * (omega_n**2) + (omega * alpha))

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
                F_cg = 1j * ((eta + beta * omega) * (omega_n**2) + (omega * alpha)) 
                data = np.divide(1, (F_kg + F_mg + F_cg))
                diag = np.diag(data)
                solution[:, i] = modal_shape @ (diag @ F_aux[:,i])

                if self.stop_processing():
                    return None

        self.solution = self._reinsert_prescribed_dofs(solution)

        if self.flag_Clump:
            self.warning_Clump  = "There are external dampers connecting nodes to the ground. The damping, "
            self.warning_Clump += "treated as a viscous non-proportional model, will be ignored in mode "
            self.warning_Clump += "superposition. It's recommended to solve the harmonic analysis through "
            self.warning_Clump += "direct method if you want to get more accurate results!"

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

        alpha, beta, eta = self.model.global_damping
        # F = self.assembly.get_global_loads_for_static_analysis()
        F = self.get_combined_loads(static_analysis=True)

        rows = self.K.shape[0]
        cols = 1
        solution = np.zeros((rows, cols), dtype=complex)
        
        omega = 0

        F_K = (self.K + self.K_exp_joint[0] + self.K_lump[0])
        F_M =  (-(omega**2))*(self.M + self.M_exp_joint + self.M_lump[0])
        F_C = 1j * ((eta + omega * beta) * (self.K + self.K_exp_joint[0]) + 
                  (omega * alpha) * (self.M + self.M_exp_joint))

        F_Clump = 1j*omega*self.C_lump[0]
        A = F_K + F_M + F_C + F_Clump

        solution[:, 0] = spsolve(A, F[:, 0])
        self.solution = self._reinsert_prescribed_dofs(solution)

        return self.solution


    def get_reactions_at_constrained_dofs(self, static_analysis=False):
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

        alpha, beta, eta = self.model.global_damping

        if self.solution is None:
            return None

        if self.Kr.size == 0 or self.Mr.size == 0:
            return None
        
        if static_analysis:
            rows = 1
            _frequencies = np.array([0.])
        else:
            rows = len(self.frequencies)
            _frequencies = self.frequencies

        cols = len(self.prescribed_indexes)
        _reactions = np.zeros((rows, cols), dtype=complex)

        Ut = self.solution.T
        Kr = self.Kr.toarray()
        Mr = self.Mr.toarray() + self.Mr_exp_joint.toarray()
        Ut_Mr = Ut @ Mr

        n_freq = len(_frequencies)
        self.reactions_at_constrained_dofs.clear()

        for j, freq in enumerate(_frequencies):

            logging.info(f"Evaluating the structural reactions for constrained dofs [{j+1}/{n_freq}]")

            omega = 2*np.pi*freq
            Ut_Kr = Ut[j,:] @ (Kr + self.Kr_exp_joint[j].toarray())

            F_K = Ut_Kr
            F_M = -(omega**2) * Ut_Mr[j, :]
            F_C = 1j * ((eta + omega * beta) * Ut_Kr + (omega * alpha) * Ut_Mr[j, :])

            _reactions[j, :] = F_K + F_M + F_C

        for i, prescribed_index in enumerate(self.prescribed_indexes):
            self.reactions_at_constrained_dofs[prescribed_index] =  _reactions[:,i]


    def get_reactions_at_springs_and_dampers(self, static_analysis=False):
        """
        This method evaluates reaction forces and moments at lumped springs and dampers connected the structure and the ground.

        Returns
        ----------
        array
            Reactions. Each column corresponds to a frequency of analysis. Each row corresponds to a spring and damper.
        """

        reactions_at_springs = dict()
        reactions_at_dampers = dict()

        if self.solution is None:
            return

        U = self.solution

        if static_analysis:
            cols = 1
            _frequencies = np.array([0.])
        else:
            cols = len(self.frequencies)
            _frequencies = self.frequencies

        omega = 2*np.pi*_frequencies

        _springs_stiffness = list()
        _dampers_dampings = list()
        _global_dofs_springs = list()
        _global_dofs_dampers = list()

        self.reactions_at_springs.clear()
        self.reactions_at_dampers.clear()
        
        for (property, *args), data in self.model.properties.nodal_properties.items():
            if property == "lumped_stiffness":

                data: dict
                node_id = args[0]
                node = self.model.preprocessor.nodes[node_id]
                _global_dofs_springs.append(node.structural_global_dof)
                values = data["values"]

                if "table_names" in data.keys():
                    _springs_stiffness.append([np.zeros_like(self.frequencies) if value is None else value for value in values])
                else:
                    _springs_stiffness.append([np.zeros_like(self.frequencies) if value is None else np.ones_like(self.frequencies)*value for value in values])

            elif property == "lumped_dampings":

                node_id = args[0]
                node = self.model.preprocessor.nodes[node_id]
                _global_dofs_dampers.append(node.structural_global_dof)
                values = data["values"]

                if "table_names" in data.keys():
                    _dampers_dampings.append([np.zeros_like(self.frequencies) if value is None else value for value in values])
                else:
                    _dampers_dampings.append([np.zeros_like(self.frequencies) if value is None else np.ones_like(self.frequencies)*value for value in values])

        if _springs_stiffness:
            global_dofs_springs = np.array(_global_dofs_springs).flatten()
            springs_stiffness = np.array(_springs_stiffness).reshape(-1, cols)
            reactions_at_springs = springs_stiffness*U[global_dofs_springs,:]

            for i, gdof in enumerate(global_dofs_springs):
                self.reactions_at_springs[gdof] = reactions_at_springs[i, :]

        if _dampers_dampings:
            global_dofs_dampers = np.array(_global_dofs_dampers).flatten()
            dampers_dampings = np.array(_dampers_dampings).reshape(-1, cols)
            reactions_at_dampers = (1j*omega) * dampers_dampings * U[global_dofs_dampers,:]

            for i, gdof in enumerate(global_dofs_dampers):
                self.reactions_at_dampers[gdof] = reactions_at_dampers[i,:]

    def stress_calculate(self, external_pressure: float = 0., damping: bool = False, static_analysis: bool = False):
        """
        This method evaluates the nodal stresses of the structure.

        Parameters
        ----------
        external_pressure : float, optional
            Static pressure difference between atmosphere and the fluid in the pipeline.
            Default is 0.
            
        damping : bool, optional.
            True if the damping must be considered when evaluating the stresses. False otherwise.
            Default is False

        static_analysis : bool, optional.
            True if the structural analysis is static, False otherwise.
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


        # TODO: review the damping effect on the stress evaluation

        if damping:
            (_, beta, eta) = self.model.global_damping
            # _, beta_h, _, beta_v = self.model.global_damping
        else:
            beta = eta = 0

        if static_analysis:
            _frequencies = np.array([0], dtype=float)
        else:
            _frequencies = self.frequencies

        omega = 2 * np.pi * _frequencies.reshape(1, -1)

        damping = np.ones([6, 1]) @  (1 + 1j*(eta + omega * beta))
        # damping = np.ones([6,1]) @  (1 + 1j*( beta_h + omega * beta_v ))

        p0 = external_pressure

        n_elem = len(self.model.preprocessor.elements_attributes)
        nodal_stresses = np.zeros((n_elem, 7, len(_frequencies)), dtype=complex)

        for index, element_attributes in self.model.preprocessor.elements_attributes.items():
            # element = build_structural_element(element_attributes)

            if element_attributes.structural_element_type in ["beam_1", "expansion_joint", "valve"]:
                continue

            if element_attributes.structural_element_type != "pipe_1":
                continue

            Dab = element_attributes.matrices_for_stresses_recover.Dab
            Bab = element_attributes.matrices_for_stresses_recover.Bab
            Dts = element_attributes.matrices_for_stresses_recover.Dts
            Bts = element_attributes.matrices_for_stresses_recover.Bts

            rot = element_attributes.element_rotation_matrix

            cross_section = element_attributes.cross_section
            material = element_attributes.material
            wall_formulation = element_attributes.wall_formulation

            T = cross_section.principal_axis_translation

            first_node = element_attributes.first_node
            last_node = element_attributes.last_node

            # Internal Loads
            structural_dofs = np.r_[first_node.structural_global_dof, last_node.structural_global_dof]

            if self.solution is None:
                title = "Empty solution"
                message = "A strutural analysis must be performed to obtain the stress field."
                PrintMessageInput([error_title, title, message])
                return np.zeros((n_elem, 7, len(_frequencies)), dtype=complex)

            u = self.solution[structural_dofs, :]

            normal = Dab @ Bab @ T @ rot @ u
            shear = Dts @ Bts @ T @ rot @ u

            internal_load = np.multiply(np.r_[normal, shear], damping)

            # Stress
            do = cross_section.outer_diameter
            di = cross_section.inner_diameter
            ro = do / 2
            area = cross_section.area
            Iy = cross_section.second_moment_area_y
            Iz = cross_section.second_moment_area_z
            J = cross_section.polar_moment_area
            nu = material.poisson_ratio

            acoustic_dofs = np.r_[first_node.acoustic_global_dof, last_node.acoustic_global_dof]

            if self.acoustic_solution is not None:
                p = self.acoustic_solution[acoustic_dofs, :]
            else:
                p = np.zeros((2, len(_frequencies)))

            pm = np.sum(p, axis=0) / 2

            if wall_formulation == "thick_wall":
                hoop_stress = (2 * pm * di**2 - p0 * (do**2 + di**2)) / (do**2 - di**2)
                radial_stress = -2 * nu * (pm * di**2 - p0 * do**2) / (do**2 - di**2)

            if wall_formulation == "thin_wall":
                hoop_stress = pm
                radial_stress = -nu * np.pi * (do / (do - di) - 1)

            nodal_stresses[index, :, :] = np.c_[
                internal_load[0] / area - radial_stress,
                internal_load[1] * ro / Iy,
                internal_load[2] * ro / Iz,
                hoop_stress,
                internal_load[3] * ro / J,
                internal_load[4] / area,
                internal_load[5] / area,
            ].T

        return nodal_stresses

    def stop_processing(self):
        if self.model.preprocessor.stop_processing:
            print("\nProcessing interruption was requested by the user. \nSolution interruped.")
            return True