import numpy as np

from pulse.preprocessing.node import DOF_PER_NODE

# this is temporary, and will be changed a lot
def get_frf(mesh, solution, node, dof):
    position = mesh.nodes[node].global_index * DOF_PER_NODE + dof
    y = np.abs(solution[position])
    return y

def get_normal(mesh, solution, node):
    start_node = mesh.nodes[node]
    position = start_node.global_index * DOF_PER_NODE
    x = solution[position + 0]
    y = solution[position + 1]
    z = solution[position + 2]

    dx = (x + start_node.x)
    dy = (y + start_node.y)
    dz = (z + start_node.z)

    normal = np.sqrt(dx*dx + dy*dy + dz*dz)

    return normal