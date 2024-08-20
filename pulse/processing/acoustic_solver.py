
from pulse.model.model import Model
from pulse.processing.assembly_acoustic import AssemblyAcoustic

import numpy as np
from numpy.linalg import norm
from scipy.sparse.linalg import eigs, spsolve

def relative_error(vect_1, vect_2):
    return norm((vect_2-vect_1))/norm(vect_1)

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

        self.valve_elements = self.check_non_linear_valves()

        self.prescribed_indexes = self.assembly.get_prescribed_indexes()
        self.prescribed_values = self.assembly.get_prescribed_values()
        # self.unprescribed_indexes = self.assembly.get_unprescribed_indexes()
        self.get_pipe_and_unprescribed_indexes = self.assembly.get_pipe_and_unprescribed_indexes()

        self._initialize()

    def _initialize(self):

        self.solution_nm1 = None
        self.convergence_dataLog = None

        self.relative_error = list()
        self.deltaP_errors = list()
        self.iterations = list()

        self.max_iter = 100
        self.target = 10/100

    def check_non_linear_valves(self):

        elements = list()
        self.non_linear = False

        for (property, element_id) in self.model.properties.element_properties.keys():
            if property == "perforated_plate":
                element = self.acoustic_elements[element_id]
                if element.perforated_plate.nonlinear_effect:
                    elements.append(element)

        if elements:
            self.non_linear = True

        return elements

    def get_global_matrices(self):
        """
        This method updates the acoustic global matrices.
        """
        self.K, self.Kr = self.assembly.get_global_matrices()
        self.K_lump, self.Kr_lump = self.assembly.get_lumped_matrices()
        self.K_link, self.Kr_link = self.assembly.get_fetm_link_matrices()
        self.Kadd_lump = [ self.K[i] + self.K_link[i] + self.K_lump[i] for i in range(len(self.frequencies))]

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
                volume_velocity_eq[:, i] = np.sum((Kr[i] + Kr_link[i] + Kr_lump[i]) * self.array_prescribed_values[:,i], axis=1)

        volume_velocity_combined = volume_velocity.T - volume_velocity_eq

        return volume_velocity_combined

    def modal_analysis(self, modes=20, which='LM', sigma=0.01):
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

        K, M = self.assembly.get_global_matrices_modal()
        K_link, M_link = self.assembly.get_link_global_matrices_modal()

        K_add = K + K_link
        M_add = M + M_link

        eigen_values, eigen_vectors = eigs(K_add, M=M_add, k=modes, which=which, sigma=sigma)

        positive_real = np.absolute(np.real(eigen_values))
        natural_frequencies = np.sqrt(positive_real)/(2*np.pi)
        modal_shape = np.real(eigen_vectors)

        index_order = np.argsort(natural_frequencies)
        natural_frequencies = natural_frequencies[index_order]
        modal_shape = modal_shape[:, index_order]

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
        This method evaluate the FETM acoustic solution through direct method.

        Returns
        ----------
        array
            Solution. Each column corresponds to a frequency of analysis. Each row corresponds to a degree of freedom.
        """
        import matplotlib.pyplot as plt

        self.get_global_matrices()
        volume_velocity = self.get_combined_volume_velocity()

        rows = self.K[0].shape[0]
        cols = len(self.frequencies)
        solution = np.zeros((rows, cols), dtype=complex)

        for (property, _) in self.model.properties.element_properties.keys():
            if property == "perforated_plate":
    
                self.solution_nm1 = np.zeros((rows, cols), dtype=complex)
                vect_freqs = list(np.arange(cols, dtype=int))[1:]

                self.plt = plt

                # self.iterations = list()
                pressure_residues = list()
                delta_residues = list()

                cache_delta_pressures = list()
                cache_delta = list()
                
                self.unstable_frequencies = {}
                freq_indexes = {}

                count = 0
                relative_difference = 1
                converged = False

                if self.non_linear:
                    while relative_difference > self.target or not converged:

                        if self.stop_processing():
                            return None, None

                        self.get_global_matrices()

                        for i in range(cols):
                            solution[:,i] = spsolve(self.Kadd_lump[i], volume_velocity[:, i])

                        solution = self._reinsert_prescribed_dofs(solution)
                        
                        delta_pressures = []
                        cache_delta_residues = []
                        cache_pressure_residues = np.array([])

                        for i, element in enumerate(self.valve_elements):
                            element.update_pressure(solution)
                            first = element.first_node.global_index
                            last = element.last_node.global_index
                            pressure_residue_first = relative_error(solution[first, vect_freqs], self.solution_nm1[first, vect_freqs])
                            pressure_residue_last = relative_error(solution[last, vect_freqs], self.solution_nm1[last, vect_freqs])
                            cache_pressure_residues = np.r_[ cache_pressure_residues, pressure_residue_first, pressure_residue_last ] 
            
                            index = np.argmax(np.abs(element.delta_pressure[vect_freqs]))
                            max_value = np.max(np.abs(element.delta_pressure[vect_freqs]))

                            if len(delta_pressures) == len(self.valve_elements):
                                delta_pressures[i] = element.delta_pressure[1:]
                                cache_delta_residues[i] = relative_error(delta_pressures[i], cache_delta_pressures[i])
                            else:
                                delta_pressures.append(element.delta_pressure[1:])
                                cache_delta_pressures.append(np.zeros_like(element.delta_pressure[1:], dtype=complex))
                                cache_delta_residues.append(relative_error(delta_pressures[i], cache_delta_pressures[i]))
                                            
                            if count >= 5:
                                if len(cache_delta) == len(self.valve_elements):                                
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

                        cache_delta_pressures = delta_pressures.copy()
                        self.solution_nm1 = solution
                        solution = np.zeros((rows, cols), dtype=complex)

                        for ind, repetitions in freq_indexes.items():
                            if repetitions >= 4:
                                if ind not in self.unstable_frequencies:
                                    _frequencies = self.frequencies[vect_freqs]
                                    freq = _frequencies[ind]
                                    self.unstable_frequencies[ind] = freq
                                    vect_freqs.remove(freq)
                                    message = f"The {freq}Hz frequency step produces unstable results, therefore "
                                    message += "it will be excluded from the calculation of the residue convergence criteria.\n"
                                    print(message)  

                        self.relative_error = pressure_residues
                        self.deltaP_errors = delta_residues
                        converged = self.check_convergence_criterias(pressure_residues, delta_residues)

                        if converged:
                            self.convergence_dataLog = [self.iterations, pressure_residues, delta_residues, 100*self.target]
                            return self.solution_nm1, self.convergence_dataLog

                else:

                    for i in range(cols):
                        solution[:,i] = spsolve(self.Kadd_lump[i], volume_velocity[:, i])
                        if self.stop_processing():
                            return None, None
                    solution = self._reinsert_prescribed_dofs(solution)
                    return solution, self.convergence_dataLog                     

            else:

                for i in range(cols):
                    solution[:,i] = spsolve(self.Kadd_lump[i], volume_velocity[:, i])
                solution = self._reinsert_prescribed_dofs(solution)
                return solution, self.convergence_dataLog

    def graph_callback(self, interval, fig, ax):  
        import matplotlib.pyplot as plt

        if (len(self.iterations) < 2) or (len(self.relative_error) < 2):
            xlim = (1, 10)
            ylim = (0, 120)
        else:
            dy = 20
            xlim = (1, max(self.iterations))
            ylim = (0, (round(max(self.relative_error)/dy,0)+1)*dy)

        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        perc_criteria = self.target*100

        first_plot, = plt.plot(self.iterations, self.relative_error, color=[1,0,0], linewidth=2, marker='s', markersize=6, markerfacecolor=[0,0,1])
        second_plot, = plt.plot(xlim, [perc_criteria, perc_criteria], color=[0,0,0], linewidth=2, linestyle="--")
        
        if self.deltaP_errors:
            third_plot, = plt.plot(self.iterations, self.deltaP_errors, color=[0,0,1], linewidth=2, marker='s', markersize=6, markerfacecolor=[1,0,0])
        else:
            third_plot, = plt.plot([])
        
        first_plot_label = "Pressure residues"
        third_plot_label = "Delta pressure residues"
        second_plot_label = f'Target: {perc_criteria}%'
        
        if self.deltaP_errors:
            _legends = plt.legend(handles=[first_plot, third_plot, second_plot], labels=[first_plot_label, third_plot_label, second_plot_label])#, loc='upper right')
        else:
            _legends = plt.legend(handles=[first_plot, second_plot], labels=[first_plot_label, second_plot_label])#, loc='upper right')
        plt.gca().add_artist(_legends)
        # plt.grid()

        ax.set_title('PERFORATED PLATE: CONVERGENCE PLOT', fontsize = 16, fontweight = 'bold')
        ax.set_xlabel('Iteration [n]', fontsize = 14, fontweight = 'bold')
        ax.set_ylabel("Relative error [%]", fontsize = 14, fontweight = 'bold')

        return (first_plot, second_plot, third_plot)

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
            # self.plt.close()
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