import numpy as np

class Node:
    """ Node

    Parameters
    ----------
    x : float
        x node's coordinate [m].
    y : float
        y node's coordinate [m].
    z : float
        z node's coordinate [m].
    user_index : int
        User node identifier.
    index : int, optional
        Internal node identifier.
    boundary : , optional
        Boundary conditions
    Examples
    --------

    """
    # Number of degree of freedom for each node
    degree_freedom = 6

    def __init__(self, x, y, z, user_index, **kwargs):
        self.x = x
        self.y = y
        self.z = z
        self.user_index = user_index

        self.index = kwargs.get("index", None)
        # self.boundary = boundary
        # boundary must be 0,1,2,3,4,5 to fix u_x, u_y, u_z, theta_x, theta_y, theta_z, respectively.

    def dofs(self):
        """ For a node, define its global degree of freedom.

        Parameter
        ---------
        Node
        
        output: array with 6 integers."""
        if self.index == None:
            #TODO: warning, self.index must be defined
            pass

        local_dof = np.arange( self.degree_freedom, dtype=int )
        global_dof = self.degree_freedom * self.index + local_dof

        return global_dof, local_dof

    def coordinates(self):
        """ Give coordinates as array."""
        return np.array([self.x, self.y, self.z])

    def distance(self, other):
        """ Give the distance between the actual node and other one."""
        if type(other) != Node:
            #TODO: define the warning. 'other' must be a node.
            return
        return np.linalg.norm( self.coordinates() - other.coordinates() )