import numpy as np
from pulse.preprocessing.node import DOF_PER_NODE_ACOUSTIC

def get_acoustic_frf(mesh, solution, node, absolute=True, real=False, dB=True):
    position = mesh.nodes[node].global_index * DOF_PER_NODE_ACOUSTIC
    if absolute:
        results = np.abs(solution[position])
    if real:
        results = np.real(solution[position])
    if dB:
        p_ref = 20e-6
        results = 20*np.log10(np.abs(results/p_ref))
    return results

def get_acoustic_response(mesh, solution, column):
    data = np.real(solution.T)
    rows = int(solution.shape[0])
    pressure = np.zeros((rows, 2))
    pressure[:,0] = np.arange( 0, rows, 1 )
    pressure[:,1] = data[column]
    
    r_def = data[column]

    coord = mesh.nodal_coordinates_matrix
    connect = mesh.connectivity_matrix
        
    return pressure, connect, coord, r_def