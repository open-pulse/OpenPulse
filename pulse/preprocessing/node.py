import numpy as np

from pulse.preprocessing.boundary_condition import BoundaryCondition

DOF_PER_NODE = 6


def distance(a, b):
    return np.linalg.norm(a.coordinates - b.coordinates)


class Node:
    def __init__(self, x, y, z, global_index=None):
        self.x = x
        self.y = y
        self.z = z
        self.boundary_condition = [None, None, None, None, None, None]
        self.forces = [0,0,0,0,0,0]
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

    def set_boundary_condition(self, boundary_condition):
        self.boundary_condition = boundary_condition

    def getBondaryCondition(self):
        return self.boundary_condition

    def get_boundary_condition_indexes(self):
        return [i for i, j in enumerate(self.boundary_condition) if j is not None]

    def get_boundary_condition_values(self):
        return [i for i in self.boundary_condition if i is not None]

    def set_prescribed_forces(self, forces):
        self.forces = forces

    def get_prescribed_forces(self):
        return self.forces

    def haveBoundaryCondition(self):
        for i in self.boundary_condition:
            if i is not None:
                return True
        return False