
from pulse.model.model import Model
from pulse.processing.assembly_acoustic import AssemblyAcoustic

import numpy as np
from numpy.linalg import norm
from scipy.sparse import csr_matrix, bmat, eye, block_array
from scipy.sparse.linalg import eigs, eigsh, spsolve, inv

import logging

def relative_error(vect_1, vect_2):
    return norm((vect_2-vect_1)) / norm(vect_1)

class AcousticSolver:
    """ This class creates a Acoustic Solution object from input data.

    Parameters
    ----------
    model :Model object
        Acoustic finite element model.

    frequencies : array
        Frequencies of analysis.
    """

    def __init__(self, model: Model):

        self.model = model
        frequencies = model.frequencies

        if isinstance(frequencies, np.ndarray | list):
            if frequencies[0] == 0:
                frequencies[0] = float(1e-4)

        self.frequencies = frequencies

        self.all_dofs = len(model.preprocessor.nodes)
        self.assembly = AssemblyAcoustic(model)
        self.acoustic_elements = model.preprocessor.acoustic_elements

        self.prescribed_indexes = self.assembly.get_prescribed_indexes()
        self.prescribed_values = self.assembly.get_prescribed_values()
        # self.unprescribed_indexes = self.assembly.get_unprescribed_indexes()
        self.get_pipe_and_unprescribed_indexes = self.assembly.get_pipe_and_unprescribed_indexes()

        self.nl_pp_elements = self.check_non_linear_perforated_plate()

        self._initialize()

    def _initialize(self):

        self.solution = None
        self.modal_shapes = None
        self.natural_frequencies = None
        self.complex_natural_frequencies = None

        self.convergence_data_log = None

        self.relative_error = list()
        self.deltaP_errors = list()
        self.iterations = list()

        self.max_iter = 100
        self.target = 10 / 100

        self.warning_modal_prescribed_pressures = ""

    def check_non_linear_perforated_plate(self):

        elements = list()
        for (property, element_id) in self.model.properties.element_properties.keys():
            if property == "perforated_plate":
                element = self.acoustic_elements[element_id]
                if element.perforated_plate.nonlinear_effects:
                    elements.append(element)

        return elements

    def get_global_matrices(self):
        """
        This method updates the acoustic global matrices.
        """
        self.K, self.Kr = self.assembly.get_global_matrices()
        self.K_lump, self.Kr_lump = self.assembly.get_lumped_matrices()
        self.K_link, self.Kr_link = self.assembly.get_fetm_link_matrices()
        self.T_link, self.Tr_link = self.assembly.get_fetm_transfer_matrices()

        # self.Kadd_lump = [ self.K[i] + self.K_link[i] + self.K_lump[i] for i in range(len(self.frequencies))]
        self.Kadd_lump = [ self.K[i] + self.K_link[i] + self.K_lump[i] + self.T_link[i] for i in range(len(self.frequencies))]

    def _reinsert_prescribed_dofs(self, solution, modal_analysis = False):
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

        rows = self.all_dofs
        cols = solution.shape[1]
        full_solution = np.zeros((rows, cols), dtype=complex)
        full_solution[self.get_pipe_and_unprescribed_indexes, :] = solution

        if modal_analysis:
            full_solution[self.prescribed_indexes, :] = np.zeros((len(self.prescribed_values),cols))
        else:
            if len(self.prescribed_indexes) != 0:
                full_solution[self.prescribed_indexes, :] = self.array_prescribed_values
        
        return full_solution

    def get_combined_volume_velocity(self):
        """
        This method adds the effects of prescribed acoustic pressure into volume velocity global vector.

        Returns
        ----------
        array
            Volume velocity. Each column corresponds to a frequency of analysis.
        """

        volume_velocity = self.assembly.get_global_volume_velocity()
  
        Kr = [(sparse_matrix.toarray())[self.get_pipe_and_unprescribed_indexes, :] for sparse_matrix in self.Kr]
        Kr_link = [(sparse_matrix.toarray())[self.get_pipe_and_unprescribed_indexes, :] for sparse_matrix in self.Kr_link]
        Kr_lump = [(sparse_matrix.toarray())[self.get_pipe_and_unprescribed_indexes, :] for sparse_matrix in self.Kr_lump]
        Tr_link = [(sparse_matrix.toarray())[self.get_pipe_and_unprescribed_indexes, :] for sparse_matrix in self.Tr_link]

        rows = Kr[0].shape[0]  
        cols = len(self.frequencies)
 
        aux_ones = np.ones(cols, dtype=complex)
        volume_velocity_eq = np.zeros((rows,cols), dtype=complex)

        if len(self.prescribed_values) != 0:  
            prescribed_values = list()

            for value in self.prescribed_values:
                if isinstance(value, complex):
                    prescribed_values.append(aux_ones*value)
                elif isinstance(value, np.ndarray):
                    prescribed_values.append(value)

            self.array_prescribed_values = np.array(prescribed_values)
            for i in range(cols):
                # volume_velocity_eq[:, i] = np.sum((Kr[i] + Kr_link[i] + Kr_lump[i]) * self.array_prescribed_values[:,i], axis=1)
                volume_velocity_eq[:, i] = np.sum((Kr[i] + Kr_link[i] + Kr_lump[i] + Tr_link[i]) * self.array_prescribed_values[:,i], axis=1)

        volume_velocity_combined = volume_velocity.T - volume_velocity_eq

        return volume_velocity_combined

    def modal_analysis(self, **kwargs):
        """
        This method evaluate the FEM acoustic modal analysis. The FETM formulation is not suitable to performe modal analysis.

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
            Find eigenvalues near sigma (in (rad/s)^2) using shift-invert mode. 
            Default is 0.01.

        Returns
        ----------
        natural_frequencies : array
            Natural frequencies.

        modal_shapes : array
            Modal shapes
        """

        modes = kwargs.get("modes", 40)
        which = kwargs.get("which", "LM")
        sigma_factor = kwargs.get("sigma_factor", 1e-4)

        self.warning_modal_prescribed_pressures = ""

        K, M = self.assembly.get_global_matrices_modal()
        K_link, M_link = self.assembly.get_link_global_matrices_modal()
        C, _ = self.assembly.get_lumped_matrices_for_FEM()

        K_add = K + K_link
        M_add = M + M_link

        if np.sum(C[0]):

            ones = eye(self.assembly.total_dof, dtype=complex, format="csr")
            zeros = csr_matrix((self.assembly.total_dof, self.assembly.total_dof), dtype=complex)

            ## Reference - book
            # A = bmat([[ C[0], M_add], 
            #         [M_add,  None]], format="csr", dtype=complex)

            # B = bmat([[K_add,   None], 
            #         [ None, -M_add]], format="csr", dtype=complex)            

            ## As Ans-theory
            # A = bmat([  [ C[0], -M_add], 
            #             [ ones,  zeros]  ], format="csr", dtype=complex)

            # B = bmat([  [K_add, zeros], 
            #             [zeros,  ones]  ], format="csr", dtype=complex)

            # from scipy.linalg import eig
            # eigen_values, eigen_vectors = eig(B.toarray(), b=A.toarray())
            # eigen_values, eigen_vectors = eigs(B, M=A, k=modes, which=which, sigma=sigma_factor)

            inv_M = inv(M_add.tocsc()).tocsr()
            
            AA = bmat([ [zeros, ones],
                        [-inv_M@K_add, -inv_M@C[0]]])
    
            eigen_values, eigen_vectors = eigs(AA, k=modes, which=which, sigma=sigma_factor)

            N_dofs = int(eigen_vectors.shape[0] / 2)

            mask = np.imag(eigen_values) > 0
            _eigen_values = eigen_values[mask]
            _eigen_vectors = eigen_vectors[:, mask]

            Wn = np.abs(_eigen_values)
            natural_frequencies = Wn / (2 * np.pi)
            damping_ratio = -np.real(_eigen_values) / Wn

            index_order = np.argsort(natural_frequencies)

            damping_ratio = damping_ratio[index_order]
            natural_frequencies = natural_frequencies[index_order]
            complex_natural_frequencies = _eigen_values[index_order] / (2 * np.pi)
            modal_shapes = _eigen_vectors[:N_dofs, index_order]

            mask_dmp = np.round(np.abs(damping_ratio), 6) < 1

            damping_ratio = damping_ratio[mask_dmp]
            natural_frequencies = natural_frequencies[mask_dmp]
            modal_shapes = modal_shapes[:, mask_dmp]
            self.complex_natural_frequencies = complex_natural_frequencies[mask_dmp]

            # print(np.array([natural_frequencies, damping_ratio]).T[:10])
            # print(eigen_values[:10])

        else:

            eigen_values, eigen_vectors = eigs(K_add, M=M_add, k=modes, which=which, sigma=sigma_factor)

            Wn_2 = np.absolute(np.real(eigen_values))
            natural_frequencies = np.sqrt(Wn_2) / (2 * np.pi)

            index_order = np.argsort(natural_frequencies)
            modal_shapes = eigen_vectors[:, index_order]

        modal_shapes = self._reinsert_prescribed_dofs(modal_shapes, modal_analysis=True)

        for value in self.prescribed_values:
            if value is not None:
                if (isinstance(value, complex) and value != complex(0)) or (isinstance(value, np.ndarray) and sum(value) != complex(0)):
                    self.flag_Modal_prescribed_NonNull_DOFs = True
                    self.warning_modal_prescribed_pressures  = "The Prescribed Pressure values have been ignored in the modal analysis. "
                    self.warning_modal_prescribed_pressures += "The null value has been attributed to those DOFs."

        if self.stop_processing():
            return None, None

        self.natural_frequencies = natural_frequencies

        self.modal_shapes = modal_shapes
        # self.modal_shapes = np.real(modal_shapes)

        return natural_frequencies, modal_shapes

    def direct_method(self):
        """
        This method evaluate the FETM acoustic solution through direct method.

        Returns
        ----------
        array
            Solution. Each column corresponds to a frequency of analysis. Each row corresponds to a degree of freedom.
        """

        self.solution = None

        perforated_plate = False
        for (property, _) in self.model.properties.element_properties.keys():
            if property == "perforated_plate":
                perforated_plate = True
                break

        cond_1 = (not perforated_plate)
        cond_2 = (perforated_plate and not self.nl_pp_elements)

        if cond_1 or cond_2:

            self.get_global_matrices()
            volume_velocity = self.get_combined_volume_velocity()

            rows = self.K[0].shape[0]
            cols = len(self.frequencies)
            solution = np.zeros((rows, cols), dtype=complex)

            for i, freq in enumerate(self.frequencies):

                logging.info(f"Solution step {i+1} and frequency {freq} [{i}/{len(self.frequencies)}]")
                solution[:, i] = spsolve(self.Kadd_lump[i], volume_velocity[:, i])

                if self.stop_processing():
                    self.solution = None
                    return None, None

            self.solution = self._reinsert_prescribed_dofs(solution)
            return self.solution, None      

        else:

            self.direct_method_for_non_linear_perforated_plate()

    def direct_method_for_non_linear_perforated_plate(self):
        """
        This method evaluate the FETM acoustic solution through direct method.

        Returns
        ----------
        array
            Solution. Each column corresponds to a frequency of analysis. Each row corresponds to a degree of freedom.
        """

        for (property, element_id) in self.model.properties.element_properties.keys():
            if property == "perforated_plate":
                element = self.model.preprocessor.acoustic_elements[element_id]
                element.reset()

        self.get_global_matrices()
        volume_velocity = self.get_combined_volume_velocity()

        rows = self.K[0].shape[0]
        cols = len(self.frequencies)
        solution = np.zeros((rows, cols), dtype=complex)

        indexes = list(np.arange(cols, dtype=int))[1:]
        previous_solution = np.zeros((rows, cols), dtype=complex)

        pressure_residues = list()
        delta_residues = list()

        cache_delta_pressures = list()
        cache_delta = list()
        
        self.unstable_frequencies = dict()
        freq_indexes = dict()

        count = 0
        converged = False
        relative_difference = 1

        if self.nl_pp_elements:

            _criteria = 100*self.target
            self.update_xy_plot_data()

            while relative_difference > self.target or not converged:
                
                progress = 2 * (count + 1) + 50
                if progress > 96:
                    progress = 96

                if self.relative_error:
                    _last_residue = self.relative_error[-1]
                else:
                    _last_residue = 100
                
                log_message = f"Solving non-linear perforated plate - iteration {count+1} [{progress}%]\n\n"
                log_message += f"Last pressure residue: {_last_residue : .2f}\n"
                log_message += f" Convergence criteria: {_criteria : .2f}\n"

                logging.info(log_message)
                                                                                                        
                if self.stop_processing():
                    self.solution = None
                    return None, None

                for i, freq in enumerate(self.frequencies):
                    solution[:, i] = spsolve(self.Kadd_lump[i], volume_velocity[:, i])

                solution = self._reinsert_prescribed_dofs(solution)
                
                delta_pressures_list = list()
                cache_delta_residues = list()
                cache_pressure_residues = np.array([])

                for i, element in enumerate(self.nl_pp_elements):

                    first_index = element.first_node.global_index
                    last_index = element.last_node.global_index

                    pressure_first = solution[first_index, :]
                    pressure_last = solution[last_index, :]
                    pp_delta_pressure =  pressure_last - pressure_first
                    element.update_delta_pressure(pp_delta_pressure)

                    pressure_residue_first = relative_error(solution[first_index, indexes], previous_solution[first_index, indexes])
                    pressure_residue_last = relative_error(solution[last_index, indexes], previous_solution[last_index, indexes])
                    cache_pressure_residues = np.r_[ cache_pressure_residues, pressure_residue_first, pressure_residue_last ] 

                    index = np.argmax(np.abs(pp_delta_pressure[indexes]))
                    max_value = np.max(np.abs(pp_delta_pressure[indexes]))

                    if len(delta_pressures_list) == len(self.nl_pp_elements):
                        delta_pressures_list[i] = pp_delta_pressure[1:]
                        cache_delta_residues[i] = relative_error(delta_pressures_list[i], cache_delta_pressures[i])
                    else:
                        delta_pressures_list.append(pp_delta_pressure[1:])
                        cache_delta_pressures.append(np.zeros_like(pp_delta_pressure[1:], dtype=complex))
                        cache_delta_residues.append(relative_error(delta_pressures_list[i], cache_delta_pressures[i]))

                    if count >= 5:
                        if len(cache_delta) == len(self.nl_pp_elements):                                
                            if abs((cache_delta[i]-max_value)/cache_delta[i]) > 0.5:
                                if index in freq_indexes.keys():
                                    freq_indexes[index] += 1
                                else:
                                    freq_indexes[index] = 1
                            cache_delta[i] = max_value
                        else:
                            cache_delta.append(max_value)

                count += 1
                relative_difference = np.max(cache_pressure_residues)
                pressure_residues.append(100*relative_difference)
                delta_residues.append(100*max(cache_delta_residues))
                self.iterations.append(count)

                cache_delta_pressures = delta_pressures_list.copy()
                previous_solution = solution.copy()

                for ind, repetitions in freq_indexes.items():
                    if repetitions >= 4:
                        if ind not in self.unstable_frequencies:
                            _frequencies = self.frequencies[indexes]
                            freq = _frequencies[ind]
                            self.unstable_frequencies[ind] = freq
                            indexes.remove(freq)
                            message = f"The {freq}Hz frequency step produces unstable results, therefore "
                            message += "it will be excluded from the calculation of the residue convergence criteria.\n"
                            print(message)

                self.relative_error = pressure_residues
                self.deltaP_errors = delta_residues
                converged = self.check_convergence_criterias(pressure_residues, delta_residues)

                if converged:
                    self.xy_plot.show()
                    self.convergence_data_log = [self.iterations, pressure_residues, delta_residues, 100*self.target]
                    self.solution = previous_solution
                    return self.solution, self.convergence_data_log

                else:
                    self.update_xy_plot_data()
                    self.get_global_matrices()
                    solution = np.zeros((rows, cols), dtype=complex)

    def initialize_xy_plotter(self):

        from pulse.interface.user_input.plots.general.xy_plot import XYPlot

        legends = [f'Target: {self.target*100}%', "Pressure residues", "Delta pressure residues"]

        plots_config = {
                        "number_of_plots" : 3,
                        "x_label" : "Iterations [n]",
                        "y_label" : "Relative error [%]",
                        "colors" : [(0,0,0), (0,0,1), (1,0,0)],
                        "line_styles" : ["--", "-", "-"],
                        "markers" : [None, "o", "o"],
                        "legends" : legends,
                        "title" : "Perforated plate convergence plot"
                        }

        self.xy_plot = XYPlot(plots_config)
        # self.xy_plot.show()

    def update_xy_plot_data(self):
        if self.iterations:
            dy = 20
            xlim = (1, max(self.iterations))
            ylim = (0, (round(max(self.relative_error)/dy,0)+1)*dy)
            x_data = self.iterations
            self.xy_plot.set_plot_data(x_data, self.relative_error, 1, (xlim, ylim))
            if self.deltaP_errors:
                self.xy_plot.set_plot_data(x_data, self.deltaP_errors, 2, (xlim, ylim))

        else:
            criteria = 100* self.target
            self.initialize_xy_plotter()
            xlim = (1, 100)
            ylim = (0, 120)
            x_data = [0, 100]
            y_data = [criteria, criteria]
            self.xy_plot.set_plot_data(x_data, y_data, 0, (xlim, ylim))

    def check_convergence_criterias(self, pressure_residues, delta_residues, delta_residue_criteria=True):

        ordinal = {1:"st", 2:"nd", 3:"rd"}
        count = self.iterations[-1]
        # delta_residue_criteria = False

        # if count >= 10:
        #     if np.remainder(len(pressure_residues), 5) == 0:
        #         self.plot_convergence_graph(self.iterations, pressure_residues, delta_residues)
        
        if count == 1:
            _label =  "\n      ---------------------------------------------------------------\n"
            _label += "      ||>>>>>    PERFORATED PLATE: CONVERGENCE INFORMATION    <<<<<||"
            _label += "\n      ---------------------------------------------------------------\n"
            print(_label)
        
        if count in ordinal.keys():
            label = ordinal[count]
        else:
            label = "th"

        print(f"Evaluated pressure residue criteria: {round(pressure_residues[-1], 2)}[%] @ {count}{label} iteration")
        print(f"Evaluated delta pressure residue criteria: {round(delta_residues[-1], 2)}[%] @ {count}{label} iteration\n")

        if count >= self.max_iter:
            if pressure_residues[-1] < 100*self.target:

                final_log = f"The solution converged after {count} iterations with the following observations:"
                if len(self.unstable_frequencies):
                    list_freqs = str(list(self.unstable_frequencies.values()))[1:-1]
                    final_log += f"\nList of unstable frequencies: {list_freqs} [Hz]"  
                final_log += "\nPressure residues criteria: converged"
                final_log += "\nDelta pressure residues criteria: not converged\n"
                print(final_log)
                return True 

            else:

                final_log = f"The solution did not converge after {count} iterations."
                final_log += f"\nLast pressure residue criteria found: {round(pressure_residues[-1], 2)}[%]"
                final_log += f"\nLast delta pressure residue criteria found: {round(delta_residues[-1], 2)}[%]"
                final_log += f"\nTarget criteria: {round(100*self.target, 2)}[%]\n"
                
                if len(self.unstable_frequencies):
                    list_freqs = str(list(self.unstable_frequencies.values()))[1:-1]
                    final_log += f"\nList of unstable frequencies: {list_freqs} [Hz]"
                                        
                final_log += "\nPressure residues criteria: not converged"
                final_log += "\nDelta pressure residues criteria: not converged\n"
                print(final_log)
                # TODO: print warning message without any threading conflicts
                return True 

        elif delta_residue_criteria:
    
            if pressure_residues[-1] < 100*self.target:
                if len(delta_residues) >= 4:
                        if max(delta_residues[-5:]) <= 100*self.target:
                            # if (delta_residues[-5] >= delta_residues[-4] >= delta_residues[-3] >= delta_residues[-2] >= delta_residues[-1]):
                            if max(pressure_residues[-3:]) <= 10:
                                if pressure_residues[-3] >= pressure_residues[-2] >= pressure_residues[-1]: 
                                
                                    final_log = f"The solution converged after {count} iterations with the following observations:"
                                    if len(self.unstable_frequencies):
                                        list_freqs = str(list(self.unstable_frequencies.values()))[1:-1]
                                        final_log += f"\nList of unstable frequencies: {list_freqs} [Hz]"                   
                                    final_log += "\nPressure residues criteria: converged"
                                    final_log += "\nDelta pressure residues criteria: converged\n"
                                    print(final_log)
                                    return True
            
        else: 

            if max(pressure_residues[-5:]) <= 100*self.target:
                # if pressure_residues[-5] >= pressure_residues[-4] >= pressure_residues[-3] >= pressure_residues[-2] >= pressure_residues[-1]: 
                final_log = f"The solution converged after {count} iterations with the following observations:"
                if len(self.unstable_frequencies):
                    list_freqs = str(list(self.unstable_frequencies.values()))[1:-1]
                    final_log += f"\nList of unstable frequencies: {list_freqs} [Hz]"  
                final_log += "\nPressure residues criteria: converged"
                final_log += "\nDelta pressure residues criteria: not converged\n"
                print(final_log)
                return True

        return False

    def stop_processing(self):
        if self.model.preprocessor.stop_processing:
            print("\nProcessing interruption was requested by the user. \nSolution interruped.")
            return True