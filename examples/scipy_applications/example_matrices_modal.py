
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigs


def load_global_matrices_data(path: str):
    data = np.loadtxt(path, delimiter=",")
    rows = data[:, 0].astype(int)
    cols = data[:, 1].astype(int)
    data = data[:, 2]
    return rows, cols, data


def process_modal_analysis(example_name: str):
    
    ## import global matrices data
    rows_K, cols_K, data_K = load_global_matrices_data(f"examples_modal/{example_name}/K_data.csv")
    rows_M, cols_M, data_M = load_global_matrices_data(f"examples_modal/{example_name}/M_data.csv")

    ## import prescribed and unprescribed dofs
    unprescribed_dofs = np.loadtxt(f"examples_modal/{example_name}/unprescribed_dofs.dat").astype(int)
    prescribed_dofs = np.loadtxt(f"examples_modal/{example_name}/unprescribed_dofs.dat").astype(int)

    ## calculate the total dofs
    total_dofs = len(unprescribed_dofs) + len(prescribed_dofs)

    ## assemble the global matrices
    K = csr_matrix((data_K, (rows_K, cols_K)), shape=(total_dofs, total_dofs))
    M = csr_matrix((data_M, (rows_M, cols_M)), shape=(total_dofs, total_dofs))

    ## dropping global matrices according to prescribed dofs
    K = K[unprescribed_dofs, :][:, unprescribed_dofs]
    M = M[unprescribed_dofs, :][:, unprescribed_dofs]

    ## set the number of modes to find
    n_modes = 40

    ## solve the eigenproblem
    eigen_values, eigen_vectors = eigs(K, k=n_modes,  M=M, sigma=1e-2, which="LM")

    ## post-processing obtained results
    positive_real = np.absolute(np.real(eigen_values))
    natural_frequencies = np.sqrt(positive_real) / (2 * np.pi)

    ## reordering the eigenvalues
    index_order = np.argsort(natural_frequencies)
    natural_frequencies = natural_frequencies[index_order]

    ## reordering the eigenvectors
    eigen_vectors = eigen_vectors[:, index_order]
    
    ## initialize the solution matrix
    rows = eigen_vectors.shape[0] + len(prescribed_dofs)
    cols = eigen_vectors.shape[1]
    full_solution = np.zeros((rows, cols), dtype=complex)

    ## recovering the solution from all dofs
    full_solution[unprescribed_dofs, :] = eigen_vectors

    print("Obtained results for natural frequencies:\n")
    for i, nat_freq in enumerate(natural_frequencies):
        print(f"Mode: {i+1} -> Natural frequency: {nat_freq : .4f} Hz")


if __name__ == "__main__":

    examples = ["viga_reta", "trave"]
    process_modal_analysis(examples[0])