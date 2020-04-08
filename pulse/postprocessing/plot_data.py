import numpy as np

from pulse.preprocessing.node import DOF_PER_NODE

# this is temporary, and will be changed a lot
def get_frf(mesh, solution, node, dof):
    position = mesh.nodes[node].global_index * DOF_PER_NODE + dof
    y = np.abs(solution[position])
    return y
