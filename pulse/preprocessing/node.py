import numpy as np
from pulse.utils import error

DOF_PER_NODE_STRUCTURAL = 6
DOF_PER_NODE_ACOUSTIC = 1

def distance(a, b):
    return np.linalg.norm(a.coordinates - b.coordinates)

class Node:
    def __init__(self, x, y, z, **kwargs):
        self.x = x
        self.y = y
        self.z = z

        # Structural boundary conditions and external lumped elements
        self.nodal_loads = [None, None, None, None, None, None]
        self.there_are_nodal_loads = False
        self.loaded_table_for_nodal_loads = False
        
        self.prescribed_dofs = [None, None, None, None, None, None]
        self.there_are_prescribed_dofs = False
        self.loaded_table_for_prescribed_dofs = False
        self.there_are_constrained_dofs = False
        
        self.lumped_masses = [None, None, None, None, None, None]
        self.there_are_lumped_masses = False
        self.loaded_table_for_lumped_masses = False

        self.lumped_stiffness = [None, None, None, None, None, None]
        self.there_are_lumped_stiffness = False
        self.loaded_table_for_lumped_stiffness = False

        self.lumped_dampings = [None, None, None, None, None, None]
        self.there_are_lumped_dampings = False
        self.loaded_table_for_lumped_dampings = False
        
        self.elastic_nodal_link_stiffness = {}
        self.there_are_elastic_nodal_link_stiffness = False
        self.loaded_table_for_elastic_link_stiffness = False

        self.elastic_nodal_link_damping = {}
        self.there_are_elastic_nodal_link_damping = False
        self.loaded_table_for_elastic_link_damping = False

        # Acoustic boundary conditions and specific impedance
        self.acoustic_pressure = None
        self.volume_velocity = None
        self.specific_impedance = None
        self.radiation_impedance = None
        self.radiation_impedance_type = None # radiation_impedance_type : 0 -> anechoic termination; 1 -> unflanged pipe; 2 -> flanged pipe.
        
        self.compressor_connection_info = None
        self.volume_velocity_table_index = 0

        self.global_index = kwargs.get('global_index', None)
        self.external_index = kwargs.get('external_index', None)
        
        self.deformed_coordinates = None
        self.deformed_rotations_xyz_gcs = None
        self.deformed_displacements_xyz_gcs = None
        self.nodal_solution_gcs = None

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
        self.prescribed_dofs = boundary_condition

    def get_prescribed_dofs(self):
        return self.prescribed_dofs

    def get_lumped_dampings(self):
        return self.lumped_dampings

    def get_lumped_stiffness(self):
        return self.lumped_stiffness

    def get_prescribed_dofs_bc_indexes(self):
        return [i for i, j in enumerate(self.prescribed_dofs) if j is not None]

    def get_prescribed_dofs_bc_values(self):
        return [value for value in self.prescribed_dofs if value is not None]
                
    def set_prescribed_loads(self, values):
        self.nodal_loads = values

    def get_prescribed_loads(self):
        return self.nodal_loads
    
    # Acoustic Boundary Condition
    def set_acoustic_boundary_condition(self, acoustic_boundary_condition):
        self.acoustic_boundary_condition = acoustic_boundary_condition

    def getAcousticBoundaryCondition(self):
        return self.acoustic_boundary_condition

    def getStructuralBondaryCondition(self):
        return self.prescribed_dofs
    
    def get_acoustic_boundary_condition_indexes(self):
        return [i for i, j in enumerate([self.acoustic_pressure]) if j is not None]
    
    def get_acoustic_pressure_bc_values(self):
        return [i for i in [self.acoustic_pressure] if i is not None]
    
    def haveAcousticBoundaryCondition(self):
        return self.acoustic_boundary_condition.count(None) != 1

    def set_prescribed_volume_velocity(self, volume_velocity):
        self.volume_velocity = volume_velocity

    #TODO: load a table of real+imaginary components    

    def get_volume_velocity(self, frequencies):
        if isinstance(self.volume_velocity, np.ndarray):
            if len(self.volume_velocity) == len(frequencies):
                return self.volume_velocity
            else:
                error("The frequencies vector should have same length.\n Please, check the frequency analysis setup.")
                return
        else:
            return self.volume_velocity * np.ones_like(frequencies)

    def haveVolumeVelocity(self):
        return self.volume_velocity.count(0) != 1
    
    def admittance(self, area_fluid, frequencies):
        admittance_specific = np.zeros(len(frequencies), dtype=complex)
        admittance_rad = np.zeros(len(frequencies), dtype=complex)

        if self.specific_impedance is not None:
            Z_specific = self.specific_impedance / area_fluid
            
            if isinstance(self.specific_impedance, complex):
                admittance_specific = 1/Z_specific * np.ones_like(frequencies)
            elif isinstance(self.specific_impedance, np.ndarray):
                if len(self.specific_impedance) != len(frequencies):
                    error(" The vectors of Specific Impedance and frequencies must be\n the same lengths to calculate the admittance properly!")
                    return
                admittance_specific = np.divide(1, Z_specific)
              
        if self.radiation_impedance is not None:
            Z_rad = self.radiation_impedance / area_fluid

            if isinstance(self.radiation_impedance, complex):
                admittance_rad = np.divide(1, Z_rad) 
            elif isinstance(self.radiation_impedance, np.ndarray):
                if len(self.radiation_impedance) != len(frequencies):
                    error(" The vectors of Radiation Impedance and frequencies must be\n the same lengths to calculate the admittance properly!")
                    return
                admittance_rad = np.divide(1, Z_rad)
        
        admittance = admittance_specific + admittance_rad
        
        return admittance.reshape(-1,1)#([len(frequencies),1])
    
    def __str__(self):
        text = ''
        text += f'Node Id: {self.external_index} \n'
        text += f'Position: {self.coordinates} [m]\n'
        text += f'Displacement: {self.prescribed_dofs[:3]} [m]\n'
        text += f'Rotation: {self.prescribed_dofs[3:]} [rad]'
        return text