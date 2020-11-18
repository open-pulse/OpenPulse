from time import time
import numpy as np
from scipy.sparse.linalg import eigs, spsolve

from pulse.processing.assembly_acoustic import AssemblyAcoustic

class SolutionAcoustic:

    def __init__(self, mesh, frequencies):

        if frequencies is None:
            pass
        elif frequencies[0]==0:
            frequencies[0] = float(1e-4)
        self.all_dofs = len(mesh.nodes)
        self.assembly = AssemblyAcoustic(mesh, frequencies)
        self.frequencies = frequencies

        self.prescribed_indexes = self.assembly.get_prescribed_indexes()
        self.prescribed_values = self.assembly.get_prescribed_values()
        # self.unprescribed_indexes = self.assembly.get_unprescribed_indexes()
        self.get_pipe_and_unprescribed_indexes = self.assembly.get_pipe_and_unprescribed_indexes()

    def get_global_matrices(self):
        self.K, self.Kr = self.assembly.get_global_matrices()
        self.K_lump, self.Kr_lump = self.assembly.get_lumped_matrices()
        self.Kadd_lump = [ self.K[i] + self.K_lump[i] for i in range(len(self.frequencies))]

    def _reinsert_prescribed_dofs(self, solution, modal_analysis = False):

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
        """
        self.get_global_matrices()
        volume_velocity = self.get_combined_volume_velocity()

        rows = self.K[0].shape[0]
        cols = len(self.frequencies)
        solution = np.zeros((rows, cols), dtype=complex)

        for i in range(cols):
            solution[:,i] = spsolve(self.Kadd_lump[i],volume_velocity[:, i])

        solution = self._reinsert_prescribed_dofs(solution)

        return solution

    def modal_analysis(self, modes=20, which='LM', sigma=0.01):

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