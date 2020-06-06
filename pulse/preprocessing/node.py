import numpy as np
from pulse.utils import error

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
        self.prescribed_dofs_bc = [None, None, None, None, None, None]
        self.loads = [0,0,0,0,0,0]
        
        self.mass   = [0,0,0,0,0,0]
        self.spring = [0,0,0,0,0,0]
        self.damper = [0,0,0,0,0,0]

        # Acoustic physical quantities
        self.acoustic_pressure = None
        self.volume_velocity = 0

        self.specific_impedance = 0
        self.acoustic_impedance = 0
        self.radiation_impedance = 0
        
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
    def set_prescribed_dofs_bc(self, boundary_condition):
        self.prescribed_dofs_bc = boundary_condition

    def getStructuralBondaryCondition(self):
        return self.prescribed_dofs_bc

    def get_prescribed_dofs_bc_indexes(self):
        return [i for i, j in enumerate(self.prescribed_dofs_bc) if j is not None]

    def get_prescribed_dofs_bc_values(self):
        return [i for i in self.prescribed_dofs_bc if i is not None]

    def haveBoundaryCondition(self):
        if None in self.prescribed_dofs_bc:
            if list(self.prescribed_dofs_bc).count(None) != 6:
                return True
            else:
                return False
        elif len(self.prescribed_dofs_bc) == 6:
            return True
    
    def haveForce(self):
        return self.loads.count(0) != 6

    def set_prescribed_loads(self, loads):
        self.loads = loads

    def get_prescribed_loads(self):
        return self.loads
    
    # Acoustic Boundary Condition
    def set_acoustic_boundary_condition(self, acoustic_boundary_condition):
        self.acoustic_boundary_condition = acoustic_boundary_condition

    def getAcousticBoundaryCondition(self):
        return self.acoustic_boundary_condition
    
    def get_acoustic_boundary_condition_indexes(self):
        return [i for i, j in enumerate([self.acoustic_pressure]) if j is not None]
    
    def get_acoustic_pressure_bc_values(self):
        return [i for i in [self.acoustic_pressure] if i is not None]
    
    def haveAcousticBoundaryCondition(self):
        return self.acoustic_boundary_condition.count(None) != 1

    def set_prescribed_volume_velocity(self, volume_velocity):
        self.volume_velocity = volume_velocity

    #TODO: load a table of real+imaginary components    

    def get_prescribed_volume_velocity(self, frequencies):
        # if isinstance(self.volume_velocity, np.float64):
            return self.volume_velocity * np.ones_like(frequencies)
        # elif len(self.volume_velocity) != len(frequencies):
        #     #error!!
        #     pass
        # return self.volume_velocity

    def haveVolumeVelocity(self):
        return self.volume_velocity.count(0) != 1
    
    def admittance(self, area_fluid, frequencies):
        # Only one impedance can be given.
        # More than one must raise an error
        if self.acoustic_impedance != 0:
            Z = self.acoustic_impedance
        elif self.specific_impedance != 0:
            Z = self.specific_impedance / area_fluid
        elif self.radiation_impedance != 0:
            Z = self.radiation_impedance / area_fluid
        
        if isinstance(Z, float):
            admittance = 1/Z * np.ones_like(frequencies)
        elif len([Z]) != len(frequencies):
            error(" The vectors of Impedance Z and frequencies must be\n the same lengths to calculate the admittance properly!")
            return
        else:
            admittance = np.divide(1,Z)

        return admittance.reshape([len(frequencies),1])