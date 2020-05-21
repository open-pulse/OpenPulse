import numpy as np

DOF_PER_NODE_STRUCTURAL = 6
DOF_PER_NODE_ACOUSTIC = 1

def distance(a, b):
    return np.linalg.norm(a.coordinates - b.coordinates)

class Node:
    def __init__(self, x, y, z, global_index=None, external_index=None):
        self.x = x
        self.y = y
        self.z = z

        # Structural physical quantities
        self.structural_boundary_condition = [None, None, None, None, None, None]
        self.forces = [0,0,0,0,0,0]
        
        self.mass   = [0,0,0,0,0,0]
        self.spring = [0,0,0,0,0,0]
        self.damper = [0,0,0,0,0,0]

        # Acoustic physical quantities
        self.acoustic_boundary_condition = None
        self.volume_velocity = 0

        self.impedance_specific = 0
        self.impedance_acoustic = 0
        self.impedance_specific_radiation = 0
        
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

    # Structural Boundary Condition
    def set_structural_boundary_condition(self, boundary_condition):
        self.structural_boundary_condition = boundary_condition

    def getStructuralBondaryCondition(self):
        return self.structural_boundary_condition

    def get_structural_boundary_condition_indexes(self):
        return [i for i, j in enumerate(self.structural_boundary_condition) if j is not None]

    def get_structural_boundary_condition_values(self):
        return [i for i in self.structural_boundary_condition if i is not None]

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

    def set_prescribed_forces(self, forces):
        self.forces = forces

    def get_prescribed_forces(self):
        return self.forces
    
    # Acoustic Boundary Condition
    def set_acoustic_boundary_condition(self, acoustic_boundary_condition):
        self.acoustic_boundary_condition = acoustic_boundary_condition

    def getAcousticBoundaryCondition(self):
        return self.acoustic_boundary_condition
    
    def get_acoustic_boundary_condition_indexes(self):
        return [i for i, j in enumerate([self.acoustic_boundary_condition]) if j is not None]
    
    def get_acoustic_boundary_condition_values(self):
        return [i for i in [self.acoustic_boundary_condition] if i is not None]
    
    def haveAcousticBoundaryCondition(self):
        return self.acoustic_boundary_condition.count(None) != 1

    def set_prescribed_volume_velocity(self, volume_velocity):
        self.volume_velocity = volume_velocity

    def get_prescribed_volume_velocity(self, frequencies):
        if isinstance(self.volume_velocity, np.float64):
            return self.volume_velocity * np.ones_like(frequencies)
        elif len(self.volume_velocity) != len(frequencies):
            #error!!
            pass

        return self.volume_velocity

    def haveVolumeVelocity(self):
        return self.volume_velocity.count(0) != 1
    
    def admittance(self, area_fluid, frequencies):
        # Only one impedance can be given.
        # More than one must raise an error
        if self.impedance_acoustic != 0:
            Z = self.impedance_acoustic
        elif self.impedance_specific != 0:
            Z = self.impedance_specific / area_fluid
        elif self.impedance_acoustic != 0:
            Z = self.impedance_acoustic / area_fluid
        
        if isinstance(Z, np.float64):
            admittance = 1/Z * np.ones_like(frequencies)
        elif len(Z) != len(frequencies):
            #error!!
            pass
        else:
            admittance = np.divide(1,Z)

        return admittance.reshape([len(frequencies),1])