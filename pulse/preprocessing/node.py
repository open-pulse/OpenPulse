import numpy as np

DOF_PER_NODE_STRUCTURAL = 6
DOF_PER_NODE_ACOUSTIC = 1

def distance(a, b):
    return np.linalg.norm(a.coordinates - b.coordinates)

class Node:
    """A node class.
    This class creates a node object from input data.

    Parameters
    ----------
    x : float
        Node x coordinate.

    y : float
        node y coordinate.

    z : float
        Node z coordinate.

    global_index : int, optional
        Internal node index used for computing.
        Default is None.

    external_index : int
        Node index displayed to the user.
        Default is None.
    """
    def __init__(self, x, y, z, **kwargs):
        self.x = x
        self.y = y
        self.z = z

        self.global_index = kwargs.get('global_index', None)
        self.external_index = kwargs.get('external_index', None)

        # Structural boundary conditions and external lumped elements
        self.nodal_loads = [None, None, None, None, None, None]
        self.nodal_loads_table_names = [None, None, None, None, None, None]
        self.there_are_nodal_loads = False
        self.loaded_table_for_nodal_loads = False
        
        self.prescribed_dofs = [None, None, None, None, None, None]
        self.prescribed_dofs_table_names = [None, None, None, None, None, None]
        self.there_are_prescribed_dofs = False
        self.loaded_table_for_prescribed_dofs = False
        self.there_are_constrained_dofs = False
        
        self.lumped_masses = [None, None, None, None, None, None]
        self.lumped_masses_table_names = [None, None, None, None, None, None]
        self.there_are_lumped_masses = False
        self.loaded_table_for_lumped_masses = False

        self.lumped_stiffness = [None, None, None, None, None, None]
        self.lumped_stiffness_table_names = [None, None, None, None, None, None]
        self.there_are_lumped_stiffness = False
        self.loaded_table_for_lumped_stiffness = False

        self.lumped_dampings = [None, None, None, None, None, None]
        self.lumped_dampings_table_names = [None, None, None, None, None, None]
        self.there_are_lumped_dampings = False
        self.loaded_table_for_lumped_dampings = False
        
        self.elastic_nodal_link_stiffness = {}
        self.there_are_elastic_nodal_link_stiffness = False
        self.loaded_table_for_elastic_link_stiffness = False

        self.elastic_nodal_link_dampings = {}
        self.there_are_elastic_nodal_link_dampings = False
        self.loaded_table_for_elastic_link_dampings = False

        # Acoustic boundary conditions and specific impedance
        self.acoustic_pressure = None
        self.acoustic_pressure_table_name = None

        self.volume_velocity = None
        self.volume_velocity_table_name = None

        self.specific_impedance = None
        self.specific_impedance_table_name = None

        self.radiation_impedance = None
        self.radiation_impedance_type = None

        self.compressor_excitation_table_names = []
        self.dict_index_to_compressor_connection_info = {}
        self.compressor_excitation_table_indexes = []
        
        self.deformed_coordinates = None
        self.deformed_rotations_xyz_gcs = None
        self.deformed_displacements_xyz_gcs = None
        self.nodal_solution_gcs = None
        self.static_nodal_solution_gcs = None
        self.acoustic_solution = None

    @property
    def coordinates(self):
        """
        This method returns the node's coordinates as a array.

        Returns
        -------
        array
            Node coordinates
        """
        return np.array([self.x, self.y, self.z])

    @property
    def local_dof(self):
        """
        This method returns the node's structural degrees of freedom in the local coordinate system. The 3D Timoshenko beam theory implemented takes into account the three node's translations and the three node's rotations.

        Returns
        -------
        list
            Node's structural degrees of freedom in the local coordinate system.

        See also
        --------
        global_dof : Structural degrees of freedom in the global coordinate system.
        """
        return np.arange(DOF_PER_NODE_STRUCTURAL)

    @property
    def global_dof(self):
        """
        This method returns the node's structural degrees of freedom in the global coordinate system. The 3D Timoshenko beam theory implemented takes into account the three node's translations and the three node's rotations.

        Returns
        -------
        list
            Node's structural degrees of freedom in the global coordinate system

        See also
        --------
        local_dof : Structural degrees of freedom in the local coordinate system.
        """
        return self.local_dof + self.global_index * DOF_PER_NODE_STRUCTURAL
 
    def distance_to(self, other):
        """
        This method returns the distance between the actual node and other one.

        Parameters
        ----------
        other : Node object
            The node to calculate the distance to.

        Returns
        -------
        float
            Distance between the nodes.
        """
        return np.linalg.norm(self.coordinates - other.coordinates)

    # Structural Boundary Condition
    def set_prescribed_dofs_bc(self, boundary_condition):
        """
        This method attributes the node's structural displacement and rotation boundary conditions in the local coordinate system according to the degrees of freedom.

        Parameters
        ----------
        boundary_condition : array
            The structural boundary conditions to be prescribed into the node.

        See also
        --------
        get_prescribed_dofs : Returns the structural boundary conditions prescribed into the node.
        """
        self.prescribed_dofs = boundary_condition

    def get_prescribed_dofs(self):
        """
        This method returns the node's structural displacement and rotation boundary conditions in the local coordinate system according to the degrees of freedom.

        Returns
        ----------
        boundary_condition : array
            The boundary conditions prescribed into the node.

        See also
        --------
        set_prescribed_dofs_bc : Attributes the structural boundary conditions into the node.
        """
        return self.prescribed_dofs

    def get_lumped_dampings(self):
        """
        This method returns the node's lumped dampings in the local coordinate system according to the degrees of freedom.

        Returns
        ----------
        lumped_dampings : array
            The lumped dampings prescribed into the node.
        """
        return self.lumped_dampings

    def get_lumped_stiffness(self):
        """
        This method returns the node's lumped stiffness in the local coordinate system according to the degrees of freedom.

        Returns
        ----------
        lumped_stiffness : array
            The lumped stiffness prescribed into the node.
        """
        return self.lumped_stiffness

    def get_prescribed_dofs_bc_indexes(self):
        """
        This method returns the index(es) of the degrees of freedom in the local coordinate system which has(have) prescribed structural displacement or rotation boundary conditions. The array share the same structure of the get_prescribed_dofs_bc_values array.

        Returns
        ----------
        indexes : array
            Index(es) of the degrees of freedom which has(have) prescribed structural boundary conditions.

        See also
        --------
        get_prescribed_dofs_bc_values : Value(s) of the prescribed boundary conditions.
        """
        return [i for i, j in enumerate(self.prescribed_dofs) if j is not None]

    def get_prescribed_dofs_bc_values(self):
        """
        This method returns the value(s) of the prescribed structural displacement or rotation boundary conditions. The array share the same structure of the get_prescribed_dofs_bc_indexes array.

        Returns
        ----------
        indexes : array
            Value(s) of the prescribed structural boundary conditions.

        See also
        --------
        get_prescribed_dofs_bc_indexes : Index(es) of the degrees of freedom which has(have) prescribed boundary conditions.
        """
        return [value for value in self.prescribed_dofs if value is not None]
                
    def set_prescribed_loads(self, values):
        """
        This method attributes the nodal force and moment loads in the local coordinate system according to the the degrees of freedom.

        Parameters
        ----------
        indexes : array
            Value(s) of the nodal force and moments to be prescribed boundary conditions.

        See also
        --------
        get_prescribed_loads : Prescribed nodal loads in the local coordinate system.
        """
        self.nodal_loads = values

    def get_prescribed_loads(self):
        """
        This method returns the prescribed nodal forces and moments load in the local coordinate system according to the the degrees of freedom.

        Returns
        ----------
        indexes : array
            Value(s) of the prescribed nodal force and moments boundary conditions.

        See also
        --------
        set_prescribed_loads : Attributes nodal loads in the local coordinate system.
        """
        return self.nodal_loads
    
    # Acoustic Boundary Condition
    def set_acoustic_boundary_condition(self, acoustic_boundary_condition):
        """
        This method attributes the node's acoustic pressure boundary condition.

        Parameters
        ----------
        acoustic_boundary_condition : complex
            The acoustic pressure boundary condition to be prescribed into the node.

        See also
        --------
        getAcousticBoundaryCondition : Returns the acoustic pressure boundary condition prescribed into the node.
        """
        self.acoustic_boundary_condition = acoustic_boundary_condition

    def getAcousticBoundaryCondition(self):
        """
        This method returns the node's acoustic pressure boundary condition.

        Returns
        ----------
        acoustic_boundary_condition : complex
            The acoustic pressure boundary condition prescribed into the node.

        See also
        --------
        set_acoustic_boundary_condition : Attributes the acoustic pressure boundary condition into the node.
        """
        return self.acoustic_boundary_condition

    def getStructuralBondaryCondition(self):
        return self.prescribed_dofs
    
    def get_acoustic_boundary_condition_indexes(self):
        """
        This method returns the index of the acoustic degrees of freedom with prescribed pressure boundary condition.

        Returns
        ----------
        indexes : 0 or None
            Index of the acoustic degrees with prescribed pressure boundary conditions.

        See also
        --------
        get_acoustic_pressure_bc_values : Acoustic pressure boundary condition if it is prescribed.
        """
        return [i for i, j in enumerate([self.acoustic_pressure]) if j is not None]
    
    def get_acoustic_pressure_bc_values(self):
        """
        This method returns the value of the acoustic pressure boundary condition if it is prescribed.

        Returns
        ----------
        value : complex or None
            Acoustic pressure boundary condition if it is prescribed.

        See also
        --------
        get_acoustic_boundary_condition_indexes : Index of the acoustic degrees if it has prescribed pressure boundary conditions.
        """
        return [i for i in [self.acoustic_pressure] if i is not None]
    
    def haveAcousticBoundaryCondition(self):
        """
        This method evaluates the existence of acoustic pressure boundary condition.

        Returns
        ----------
        bool
            True when there is acoustic pressure boundary condition prescribed into the node.
        """
        return self.acoustic_boundary_condition.count(None) != 1

    def set_prescribed_volume_velocity(self, volume_velocity):
        """
        This method attributes the node's acoustic volume velocity boundary condition.

        Parameters
        ----------
        volume_velocity : complex
            The acoustic volume velocity boundary condition to be prescribed into the node.

        See also
        --------
        get_volume_velocity : Returns the volume velocity boundary condition prescribed into the node.
        """
        self.volume_velocity = volume_velocity

    def get_volume_velocity(self, frequencies):
        """
        This method returns the node's acoustic volume velocity boundary condition. The volume velocity array has the same length as the frequencies array. In terms of analysis, if volume velocity is constant in the frequency domain, the method returns a array filled with the constant value with the same length as the frequencies array.

        Parameters
        ----------
        frequencies : list
            Frequencies of analysis.

        Returns
        ----------
        complex array
            The acoustic volume velocity boundary condition prescribed into the node.
        
        Raises
        ------
        TypeError
            The frequencies array must have the same length of the volume velocity array when a table is prescribed.
            Please, check the frequency analysis setup.

        See also
        --------
        set_prescribed_volume_velocity : Attributes the node's acoustic volume velocity boundary condition.
        """
        if isinstance(self.volume_velocity, np.ndarray):
            if len(self.volume_velocity) == len(frequencies):
                return self.volume_velocity
            else:
                raise TypeError("The frequencies vector must have the same length of the volume velocity vector.\n Please, check the frequency analysis setup.")
        else:
            return self.volume_velocity * np.ones_like(frequencies)

    def haveVolumeVelocity(self):
        """
        This method evaluates the existence of volume velocity pressure boundary condition.

        Returns
        ----------
        bool
            True when there is volume velocity pressure boundary condition prescribed into the node, False otherwise.
        """
        return self.volume_velocity.count(0) != 1
    
    def admittance(self, area_fluid, frequencies):
        """
        This method returns the node's lumped acoustic admittance according to either prescribed specific impedance or prescribed radiation impedance. The admittance array has the same length as the frequencies array. In terms of analysis, if admittance is constant in the frequency domain, the method returns an array filled with the constant value with the same length as the frequencies array.

        Parameters
        ----------
        area_fluid : float
            Acoustic fluid cross section area.

        frequencies : list
            Frequencies of analysis.

        Returns
        ----------
        complex array
            Lumped acoustic admittance
        
        Raises
        ------
        TypeError
            The Specific Impedance array and frequencies array must have
            the same length.

        TypeError
            The Radiation Impedance array and frequencies array must have
            the same length.
        """
        admittance_specific = np.zeros(len(frequencies), dtype=complex)
        admittance_rad = np.zeros(len(frequencies), dtype=complex)

        if self.specific_impedance is not None:
            Z_specific = self.specific_impedance / area_fluid
            
            if isinstance(self.specific_impedance, complex):
                admittance_specific = 1/Z_specific * np.ones_like(frequencies)
            elif isinstance(self.specific_impedance, np.ndarray):
                if len(self.specific_impedance) != len(frequencies):
                    raise TypeError("The Specific Impedance array and frequencies array must have \nthe same length.")
                admittance_specific = np.divide(1, Z_specific)
              
        if self.radiation_impedance is not None:
            Z_rad = self.radiation_impedance / area_fluid

            if isinstance(self.radiation_impedance, complex):
                admittance_rad = np.divide(1, Z_rad) 
            elif isinstance(self.radiation_impedance, np.ndarray):
                if len(self.radiation_impedance) != len(frequencies):
                    raise TypeError("The Radiation Impedance array and frequencies array must have \nthe same length.")
                admittance_rad = np.divide(1, Z_rad)
        
        admittance = admittance_specific + admittance_rad
        
        return admittance.reshape(-1,1)#([len(frequencies),1])
    
    # def __str__(self):
    #     text = ''
    #     text += f'Node Id: {self.external_index} \n'
    #     text += f'Position: {self.coordinates} [m]\n'
    #     text += f'Displacement: {self.prescribed_dofs[:3]} [m]\n'
    #     text += f'Rotation: {self.prescribed_dofs[3:]} [rad]'
    #     return text