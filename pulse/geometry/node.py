import numpy as np

from pulse.setup.boundary_condition import BoundaryCondition

DOF_PER_NODE = 6


def distance(a, b):
    return np.linalg.norm(a.coordinates - b.coordinates)


class Node:
    def __init__(self, x, y, z, global_index=None):
        self.x = x
        self.y = y
        self.z = z
        self.boundary_condition = BoundaryCondition()
        self.global_index = global_index

    @property
    def coordinates(self):
        return np.array([self.x, self.y, self.z])

    @property
    def local_dof(self):
        return np.arange(DOF_PER_NODE)

    @property
    def global_dof(self):
        return self.local_dof + self.global_index * DOF_PER_NODE
 
    def distance_to(self, other):
        return np.linalg.norm(self.coordinates - other.coordinates)

    def set_boundary_condition(boundary_condition):
        pass
