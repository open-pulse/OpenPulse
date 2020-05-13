import numpy as np

DOF_PER_NODE_STRUCTURAL = 6

def distance(a, b):
    return np.linalg.norm(a.coordinates - b.coordinates)

class Node:
    def __init__(self, x, y, z, global_index=None, external_index=None):
        self.x = x
        self.y = y
        self.z = z
        self.structural_boundary_condition = [None, None, None, None, None, None]
        self.forces = [0,0,0,0,0,0]
        
        self.mass   = [0,0,0,0,0,0]
        self.spring = [0,0,0,0,0,0]
        self.damper = [0,0,0,0,0,0]
        
        self.global_index = global_index
        self.external_index = external_index

    @property
    def coordinates(self):
        return np.array([self.x, self.y, self.z])

    @property
    def local_dof(self):
        return np.arange(DOF_PER_NODE_STRUCTURAL)

    @property
    def global_dof(self):
        return self.local_dof + self.global_index * DOF_PER_NODE_STRUCTURAL
 
    def distance_to(self, other):
        return np.linalg.norm(self.coordinates - other.coordinates)

    def set_structural_boundary_condition(self, boundary_condition):
        self.structural_boundary_condition = boundary_condition

    def getStructuralBondaryCondition(self):
        return self.structural_boundary_condition

    def get_structural_boundary_condition_indexes(self):
        return [i for i, j in enumerate(self.structural_boundary_condition) if j is not None]

    def get_structural_boundary_condition_values(self):
        return [i for i in self.structural_boundary_condition if i is not None]

    def set_prescribed_forces(self, forces):
        self.forces = forces

    def get_prescribed_forces(self):
        return self.forces

    def haveBoundaryCondition(self):
        if None in self.structural_boundary_condition:
            if list(self.structural_boundary_condition).count(None) != 6:
                return True
            else:
                return False
        elif len(self.structural_boundary_condition) == 6:
            return True
    
    def haveForce(self):
        return self.forces.count(0) != 6