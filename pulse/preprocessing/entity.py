# from pulse.preprocessing.material import Material

class Entity:
    """A entity class.
    This class creates a entity object from input data.

    Parameters
    ----------
    tag : int
        Entity tag name, which is displayed to the user in the UI.
    """
    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.nodes = []
        self.elements = []
        self.material = None
        self.fluid = None
        self.compressor_info = {}
        self.cross_section = None
        self.variable_cross_section_data = None
        self.xaxis_beam_rotation = 0
        self.acoustic_element_type = None
        self.vol_flow = None
        self.proportional_damping = None
        self.structural_element_type = None
        self.force_offset = None
        self.structural_element_wall_formulation = None
        self.capped_end = False
        self.length_correction = None
        self.stress_stiffening_parameters = None
        self.expansion_joint_parameters = None
        self.valve_parameters = None

    def insertNode(self, node):
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

    def insertEdge(self, edge):
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
        
    def get_nodes(self):
        """
        This method returns the list of nodes that belong to the entity.

        Returns
        ----------
        list
            Nodes that belong to the entity.

        See also
        --------
        insertNode : Appends a node to the list of nodes.
        """
        return self.nodes

    def get_elements(self):
        """
        This method returns the list of elements that belong to the entity.

        Returns
        ----------
        list
            Elements that belong to the entity.

        See also
        --------
        insertEdge : Appends a element to the list of elements.
        """
        return self.elements

    def get_tag(self):
        """
        This method returns entity tag.

        Returns
        ----------
        int
            Entity tag.
        """
        return self.tag

    def getColor(self):
        """
        This method returns entity color.

        Returns
        ----------
        tuple
            Entity color.

        See also
        --------
        getNormalizedColor : Normalized entity color.
        """
        if self.material is None:
            return [255,255,255]
        return self.material.getColorRGB()

    def getNormalizedColor(self):
        """
        This method returns normalized entity color.

        Returns
        ----------
        tuple
            Normalized entity color.

        See also
        --------
        getColor : Entity color.
        """
        if self.material is None:
            return [1,1,1]
        return self.material.getNormalizedColorRGB()

    def getCrossSection(self):
        """
        This method returns entity cross section.

        Returns
        ----------
        CrossSection object
            Entity cross section.
        """
        return self.cross_section
    
    def getElementType(self):
        """
        This method returns entity structural element type.

        Returns
        ----------
        int
            structural element type.
        """
        return self.structural_element_type

    def getMaterial(self):
        """
        This method returns entity material.

        Returns
        ----------
        Material object
            Entity material.
        """
        return self.material
        
    def getFluid(self):
        """
        This method returns entity fluid.

        Returns
        ----------
        Fluid object
            Entity fluid.
        """
        return self.fluid
    
    def getcappedEnd(self):
        """
        This method returns entity capped end configuration.

        Returns
        ----------
        boll
            Capped end configuration.
        """
        return self.capped_end
