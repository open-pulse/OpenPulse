
import numpy as np

from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
from matplotlib import pyplot as plt


def load_global_matrices_data(path: str):
    data = np.loadtxt(path, delimiter=",")
    rows = data[:, 0].astype(int)
    cols = data[:, 1].astype(int)
    data = data[:, 2]
    return rows, cols, data


def process_harmonic_analysis(example_name: str, export_results: bool=False):

    ## import the global matrices data
    rows_K, cols_K, data_K = load_global_matrices_data(f"examples_harmonic/{example_name}/K_data.csv")
    rows_M, cols_M, data_M = load_global_matrices_data(f"examples_harmonic/{example_name}/M_data.csv")

    ## import the load vector
    F = np.loadtxt(f"examples_harmonic/{example_name}/loads.csv", delimiter=",", dtype=complex)

    ## import the prescribed and unprescribed dofs
    unprescribed_dofs = np.loadtxt(f"examples_harmonic/{example_name}/unprescribed_dofs.dat", dtype=int)
    prescribed_dofs = np.loadtxt(f"examples_harmonic/{example_name}/unprescribed_dofs.dat", dtype=int)

    ## import the analysis frequencies
    frequencies = np.loadtxt(f"examples_harmonic/{example_name}/frequencies.dat", dtype=float)

    ## calculate the total dofs
    total_dofs = len(unprescribed_dofs) + len(prescribed_dofs)

    ## assemble the global matrices
    K = csr_matrix((data_K, (rows_K, cols_K)), shape=(total_dofs, total_dofs))
    M = csr_matrix((data_M, (rows_M, cols_M)), shape=(total_dofs, total_dofs))

    ## dropping global matrices according to prescribed dofs
    K = K[unprescribed_dofs, :][:, unprescribed_dofs]
    M = M[unprescribed_dofs, :][:, unprescribed_dofs]

    ## initialize the solution matrix
    rows = K.shape[0]
    cols = len(frequencies)
    solution = np.zeros((rows, cols), dtype=complex)

    ## define the damping matrix (proportional damping)
    alpha = 1e-3
    beta = 1e-6
    C = alpha*M + beta*K

    ## solve the harmonic analysis (direct method)
    for i, freq in enumerate(frequencies):
        w = 2 * np.pi * freq
        A = K + 1j*w*C - (w**2)*M
        solution[:, i] = spsolve(A, F[:, i])

    ## recovering the solution from all dofs
    rows = solution.shape[0] + len(prescribed_dofs)
    cols = solution.shape[1]

    full_solution = np.zeros((rows, cols), dtype=complex)
    full_solution[unprescribed_dofs, :] = solution

    if example_name == "trave":
        node_A, dof_A = 36, "Uy"
        node_B, dof_B = 86, "Ux"

        response_Uy_node_A = full_solution[2557, :]
        response_Ux_node_B = full_solution[5898, :]

    elif example_name == "viga_reta":
        node_A, dof_A = 32, "Uy"
        node_B, dof_B = 167, "Uy"
        response_Uy_node_A = full_solution[193, :]
        response_Ux_node_B = full_solution[1003, :]

    if export_results:
        out_data_Uy_node_A = np.array([frequencies, np.real(response_Uy_node_A), np.imag(response_Uy_node_A)]).T
        out_data_Ux_node_B = np.array([frequencies, np.real(response_Ux_node_B), np.imag(response_Ux_node_B)]).T

        header = "Frequency [Hz], Displacement - real [m], Displacement - imaginary [m]"
        np.savetxt(f"output_data_{dof_A}_{node_A}.dat", out_data_Uy_node_A, delimiter=",", header=header)
        np.savetxt(f"output_data_{dof_B}_{node_B}.dat", out_data_Ux_node_B, delimiter=",", header=header)

    ## Gatherering data to plot

    data_to_plot = dict()
    
    label_A = f"Displacement {dof_A} (node {node_A})"
    data_to_plot[label_A] = {
                                "x_data" : frequencies,
                                "y_data" : np.abs(response_Uy_node_A),
                                "linewidth" : 2,
                                "linestyle" : "-",
                                "color" : (0, 0, 0)
                                }

    label_B = f"Displacement {dof_B} (node {node_B})"
    data_to_plot[label_B] = {
                                "x_data" : frequencies,
                                "y_data" : np.abs(response_Ux_node_B),
                                "linewidth" : 2,
                                "linestyle" : "-",
                                "color" : (1, 0, 0)
                                }

    ## Plot the inlet pressure criteria
    x_label = "Frequency [Hz]"
    y_label = "Displacement - absolute [m]"
    title = "Results spectrum of harmonic analysis"

    plot_data(data_to_plot, x_label, y_label, title, absolute=True)


def plot_data(plot_data: dict, x_label: str, y_label: str, title: str, absolute=False):

    fig = plt.figure(figsize=[8, 6])
    ax = fig.add_subplot(1,1,1)

    if absolute:
        plot = ax.semilogy
    else:
        plot = ax.plot

    for i, (label, data) in enumerate(plot_data.items()):
        plot(
             data["x_data"], 
             data["y_data"], 
             color = data["color"], 
             linewidth = data["linewidth"], 
             linestyle = data["linestyle"], 
             label = label
             )

    ax.set_xlabel(x_label, fontsize = 11, fontweight = 'bold')
    ax.set_ylabel(y_label, fontsize = 11, fontweight = 'bold')
    ax.set_title(title, fontsize = 12, fontweight = 'bold')

    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":

    examples = ["viga_reta", "trave"]
    process_harmonic_analysis(examples[0])