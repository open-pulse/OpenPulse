
from dataclasses import dataclass

import numpy as np

from pulse.model.node import Node, distance


@dataclass
class SpatialData:

    index: int
    first_node: Node
    last_node: Node

    xaxis_rotation = 0
    transf_mat = None
    section_directional_vectors = None
    deformed_rotation_xyz = None

    @property
    def length(self):
        """
        This method returns the element length.

        Returns
        -------
        float
            Element length.
        """
        return distance(self.first_node, self.last_node) 

    @ property
    def delta_x(self):
        return self.last_node.x - self.first_node.x

    @ property
    def delta_y(self):
        return self.last_node.y - self.first_node.y

    @ property
    def delta_z(self):
        return self.last_node.z - self.first_node.z

    @ property
    def center_coordinates(self):
        return np.array([(self.last_node.x + self.first_node.x) / 2, 
                         (self.last_node.y + self.first_node.y) / 2,
                         (self.last_node.z + self.first_node.z) / 2 ], dtype=float)

    @property
    def directional_vector(self):
        return np.array([self.delta_x, self.delta_y, self.delta_z], dtype=float)

    @property
    def normalized_directional_vector(self):
        v = np.array([self.delta_x, self.delta_y, self.delta_z], dtype=float)
        return v / np.linalg.norm(v)