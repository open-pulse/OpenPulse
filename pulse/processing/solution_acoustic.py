from time import time
import numpy as np
from numpy.linalg import norm
from scipy.sparse.linalg import eigs, spsolve

from pulse.processing.assembly_acoustic import AssemblyAcoustic


def relative_error(p1,p2):
    return norm(p1-p2)/norm(p1)
class SolutionAcoustic:
    """ This class creates a Acoustic Solution object from input data.

    Parameters
    ----------
    preprocessor : Preprocessor object
        Acoustic finite element preprocessor.

    frequencies : array
        Frequencies of analysis.
    """

    def __init__(self, preprocessor, frequencies):

        if frequencies is None:
            pass
        elif frequencies[0]==0:
            frequencies[0] = float(1e-4)
        self.all_dofs = len(preprocessor.nodes)
        self.assembly = AssemblyAcoustic(preprocessor, frequencies)
        self.acoustic_elements = preprocessor.acoustic_elements
        self.frequencies = frequencies

        self.elements_with_perforated_plate = preprocessor.group_elements_with_perforated_plate
        self.solution_nm1 = None

        self.prescribed_indexes = self.assembly.get_prescribed_indexes()
        self.prescribed_values = self.assembly.get_prescribed_values()
        # self.unprescribed_indexes = self.assembly.get_unprescribed_indexes()
        self.get_pipe_and_unprescribed_indexes = self.assembly.get_pipe_and_unprescribed_indexes()

    def get_global_matrices(self):
        """
        This method updates the acoustic global matrices.
        """
        self.K, self.Kr = self.assembly.get_global_matrices()
        self.K_lump, self.Kr_lump = self.assembly.get_lumped_matrices()
        self.Kadd_lump = [ self.K[i] + self.K_lump[i] for i in range(len(self.frequencies))]

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

        Kr_lump = [(sparse_matrix.toarray())[self.get_pipe_and_unprescribed_indexes, :] for sparse_matrix in self.Kr_lump]

        rows = Kr[0].shape[0]  
        cols = len(self.frequencies)
 
        aux_ones = np.ones(cols, dtype=complex)
        volume_velocity_eq = np.zeros((rows,cols), dtype=complex)

        if len(self.prescribed_values) != 0:  
            list_prescribed_values = []

            for value in self.prescribed_values:
                if isinstance(value, complex):
                    list_prescribed_values.append(aux_ones*value)
                elif isinstance(value, np.ndarray):
                    list_prescribed_values.append(value)
      
            self.array_prescribed_values = np.array(list_prescribed_values)
            for i in range(cols):
                volume_velocity_eq[:, i] = np.sum((Kr[i] + Kr_lump[i]) * self.array_prescribed_values[:,i], axis=1)
        
        volume_velocity_combined = volume_velocity.T - volume_velocity_eq
        
        return volume_velocity_combined

    def direct_method(self):
        """
        This method evaluate the FETM acoustic solution through direct method.

        Returns
        ----------
        array
            Solution. Each column corresponds to a frequency of analysis. Each row corresponds to a degree of freedom.
        """
        self.get_global_matrices()
        volume_velocity = self.get_combined_volume_velocity()

        rows = self.K[0].shape[0]
        cols = len(self.frequencies)
        solution = np.zeros((rows, cols), dtype=complex)

        if bool(self.elements_with_perforated_plate):
            values = list(dict.values(self.elements_with_perforated_plate))
            elements = [self.acoustic_elements[j] for [_,i] in values for j in i ]
            count = 0
            crit = 1
            self.solution_nm1 = np.zeros((rows, cols), dtype=complex)

            while count < 100 and crit > 1e-2:
                self.get_global_matrices()

                for i in range(cols):
                    solution[:,i] = spsolve(self.Kadd_lump[i],volume_velocity[:, i])

                solution = self._reinsert_prescribed_dofs(solution)

                Crit = np.array([])
                for el in elements:
                    el.update_pressure(solution)
                    first = el.first_node.global_index
                    last = el.last_node.global_index
                    Crit = np.r_[Crit, relative_error(solution[first,:], self.solution_nm1[first,:]), relative_error(solution[last,:], self.solution_nm1[last,:]) ]
                crit = np.max(Crit)
                # TODO: create a plot showing the iteration convergence.
                # print(crit) 
                
                count += 1
                self.solution_nm1 = solution
                solution = np.zeros((rows, cols), dtype=complex)

            if crit < 1e-2:
                return self.solution_nm1
            elif count > 100:
                # TODO: print warning message

                # title = "ITERATIVE PROCESS HAS NOT CONVERGED"
                # message = "The perforated plate solver has not converged."
                # message += "\n\nActual relative error: {}\n".format(str(crit.shape).replace(",", ""))
                # PrintMessageInput([title, message, "WARNING"])
                return self.solution_nm1
        else:
            for i in range(cols):
                solution[:,i] = spsolve(self.Kadd_lump[i],volume_velocity[:, i])

            solution = self._reinsert_prescribed_dofs(solution)

            return solution

        return solution

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
        
        eigen_values, eigen_vectors = eigs(K, M=M, k=modes, which=which, sigma=sigma)

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
        return natural_frequencies, modal_shape