# from pulse.properties.material import Material

class Line:
    """A entity class.
    This class creates a entity object from input data.

    Parameters
    ----------
    tag : int
        Line tag name, which is displayed to the user in the UI.
    """
    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.nodes = []
        self.elements = []
        self.material = None
        self.fluid = None
        self.compressor_info = {}

        self.xaxis_beam_rotation = 0

        self.structural_element_type = None
        self.force_offset = None
        self.structural_element_wall_formulation = None
        self.capped_end = True

        self.stress_stiffening_parameters = None
        self.expansion_joint_parameters = None
        self.valve_parameters = None

    def insert_node(self, node):
        """
        This method appends a node to the list of nodes that belong to the entity.

        Parameters
        ----------
        node : Node object

        See also
        --------
        get_nodes : List of nodes that belong to the entity.
        """
        # self.nodes.append(node)
        self.nodes = node

    def insert_edge(self, edge):
        """
        This method appends an element to the list of elements that belong to the entity.

        Parameters
        ----------
        edge : gmesh element

        See also
        --------
        get_elements : List of elements that belong to the entity.
        """
        # self.elements.append(edge)
        self.elements = edge

    def get_tag(self):
        """
        This method returns entity tag.

        Returns
        ----------
        int
            Line tag.
        """
        return self.tag