import numpy as np

from pulse.preprocessing.node import DOF_PER_NODE

# this is temporary, and will be changed a lot
def get_frf(mesh, solution, node, dof):
    position = mesh.nodes[node].global_index * DOF_PER_NODE + dof
    y = np.abs(solution[position])
    return y

def get_displacement_matrix(mesh, solution, frequency):
    displacement = []
    
    for i, node in mesh.nodes.items():
        pos = node.global_index * DOF_PER_NODE
        x = np.real(solution[pos + 0, frequency])
        y = np.real(solution[pos + 1, frequency])
        z = np.real(solution[pos + 2, frequency])
        displacement.append([i,x,y,z])
        
    return displacement