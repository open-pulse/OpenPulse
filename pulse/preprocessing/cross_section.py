import numpy as np
from math import pi, sqrt, cos, sin, atan, isnan, isinf
from numpy.linalg import inv, pinv, norm
from scipy.sparse import csc_matrix, coo_matrix
from scipy.sparse.linalg import spilu, svds, splu, spsolve
from scipy.linalg import svd

rows, cols = 4, 2
N_int_points = 4

def _gauss_quadrature2D():
    """
    This function returns the Gauss quadrature points and wights for a 2D integration over a square with two integration points. The nodes coordinates are :math:`n_i=\\frac{1}{\\sqrt{3}}(\\pm 1, \\pm 1)` as illustrated: ::

            
              y
              ^
              |
        +-----------+       
        |  *  |  *  |       
        |     |     |       
        |     +---- | --> x 
        |           |       
        |  *     *  |       
        +-----------+       

    Returns
    -------
    points : (4,2) array
        Each line corresponds to an integration points :math: `(x,y)` in the normalized domain :math:`[-1,1]\\times[-1,1]`.

    weights : float
        Weights of the respective integration points in the sum approximation. In this case, the weights are all equal to 1.

    See also
    --------
    _get_all_shape_functions : Shape function and its derivative for all the integration points.
    """
    c = 1/sqrt(3)
    points=np.zeros((rows, cols))
    points[0,0]=-c
    points[1,0]=c
    points[2,0]=c
    points[3,0]=-c

    points[0,1]=-c
    points[1,1]=-c
    points[2,1]=c
    points[3,1]=c
    weight = 1
    return points, weight

def _shape_function(s,t):
    """ This function returns the Q9 (9-node quadrilateral element) two dimensional quadratic shape function and its derivative for a given point in the normalized coordinate system :math:`(s,t) \\in [-1,1]\\times[-1,1]`. The shape functions are:

    .. math::
        \\varphi_i (s, t) &= \\frac{1}{4}(s^2 + s_i s)(t^2 + t_i t),\\; \\text{nodes } (s_i,t_i),\\; i=1,\\dots,4. \\\\
        \\varphi_i (s, t) &= \\frac{1}{2}(1 - s^2)(t^2 + t_i t),\\; \\text{nodes } (s_i,t_i),\\; i=5,7. \\\\
        \\varphi_i (s, t) &= \\frac{1}{2}(s^2 + s_i s)(1 - t^2),\\; \\text{nodes } (s_i,t_i),\\; i=6,8. \\\\
        \\varphi_9 (s, t) &= (1 - s^2)(1 - t^2).

    The nodes coordinates are:

    ====  ===========  ===========
    Node  :math:`s_i`  :math:`t_i`
    ====  ===========  ===========
    1     -1           -1
    2     1            -1
    3     1             1
    4     -1            1
    5     0            -1
    6     1             0
    7     0             1
    8     -1            0
    9     0             0
    ====  ===========  ===========

    Parameters
    ----------
    xi : float in :math:`[-1,1]`.
        Dimensionless :math:`x` coordinate.

    eta : float in :math:`[-1,1]`.
        Dimensionless :math:`y` coordinate.

    Returns
    -------
    phi : (9,) array
        Quadratic shape functions :math:`\\varphi_i (s,t), \\; i=1,\\dots,9`.
        
    dphi : (9,2) array
        Derivatives of the shape functions:

    .. math::
        \\begin{bmatrix}
        \\frac{\\partial \\varphi_1}{\\partial s} (s,t), &\\frac{\\partial \\varphi_1}{\\partial t} (s,t) \\\\
        \\vdots & \\vdots \\\\
        \\frac{\\partial \\varphi_9}{\\partial s} (s,t), &\\frac{\\partial \\varphi_9}{\\partial t} (s,t)
        \\end{bmatrix}

    See also
    --------
    _get_all_shape_functions : Shape function and its derivative for all the integration points.
    """
    # Shape functions
    phi = np.zeros(9, dtype='float64') 
    phi[0] = (s**2 - s) * (t**2 - t) / 4
    phi[1] = (s**2 + s) * (t**2 - t) / 4
    phi[2] = (s**2 + s) * (t**2 + t) / 4
    phi[3] = (s**2 - s) * (t**2 + t) / 4
    phi[4] = (1 - s**2) * (t**2 - t) / 2
    phi[5] = (s**2 + s) * (1 - t**2) / 2
    phi[6] = (1 - s**2) * (t**2 + t) / 2
    phi[7] = (s**2 - s) * (1 - t**2) / 2
    phi[8] = (1 - s**2) * (1 - t**2)

    # Derivatives
    dphi=np.zeros((2, 9), dtype='float64')
    # ksi Derivative
    dphi[0,0] = (2*s - 1) * (t**2 - t) / 4
    dphi[0,1] = (2*s + 1) * (t**2 - t) / 4 
    dphi[0,2] = (2*s + 1) * (t**2 + t) / 4
    dphi[0,3] = (2*s - 1) * (t**2 + t) / 4
    dphi[0,4] = -s * (t**2 - t)
    dphi[0,5] = (2*s + 1) * (1 - t**2) / 2
    dphi[0,6] = -s * (t**2 + t)
    dphi[0,7] = (2*s - 1) * (1 - t**2) / 2
    dphi[0,8] = -2*s * (1 - t**2)
    # eta Derivative
    dphi[1,0] = (s**2 - s) * (2*t - 1) / 4
    dphi[1,1] = (s**2 + s) * (2*t - 1) / 4
    dphi[1,2] = (s**2 + s) * (2*t + 1) / 4
    dphi[1,3] = (s**2 - s) * (2*t + 1) / 4
    dphi[1,4] = (1 - s**2) * (2*t - 1) / 2
    dphi[1,5] = (s**2 + s) * (-2*t) / 2
    dphi[1,6] = (1 - s**2) * (2*t + 1) / 2
    dphi[1,7] = (s**2 - s) * (-2*t) / 2
    dphi[1,8] = (1 - s**2) * (-2*t)
    return phi, dphi

def _get_all_shape_functions():
    """ This function returns the Q9 (9-node quadrilateral element) two dimensional quadratic shape functions and its derivatives for all 2D Gauss quadrature integration points in the normalized coordinate system :math:`(s,t) \\in [-1,1]\\times[-1,1]`.

    Returns
    -------
    phi : (4,9) array
        Quadratic shape function. The row ``phi[i,:]`` corresponds to the ``i``-th integration point and the column ``phi[:,j]`` corresponds to the ``j``-th shape function.

    dphi : (4,9,2) array
        Derivatives of the shape functions. The layer ``dphi[i,:,:]`` corresponds to the ``i``-th integration point, the row ``dphi[:,j,:]`` corresponds to the ``j``-th shape function and the column ``dphi[:,:,k]`` corresponds to the derivatives:
        
        .. math::        
            \\left[\\frac{\\partial \\varphi}{\\partial s} (s,t), \\frac{\\partial \\varphi}{\\partial t} (s,t)\\right].

    See also
    --------
    _shape_function : Shape function and its derivative for one point.

    _gauss_quadrature2D : Gauss quadrature data for 2D integration and two integration points.
    """
    points, _ = _gauss_quadrature2D()
    mat_phi = np.zeros((rows, 9), dtype='float64')
    mat_dphi = np.zeros((rows, 2, 9), dtype='float64')
    for i, (ksi, eta) in enumerate(points): 
        mat_phi[i,:], mat_dphi[i,:,:] = _shape_function(ksi,eta)
    return  mat_phi, mat_dphi

class CrossSection:
    """
    This class creates either a **beam** or a **pipe** cross-section object from input data. The **cross-section** defines the **structural element domain** and the Timoshenko theory makes use of several of its properties:

    .. _tabDefinitions:

    ===================================  ============
           Property                       Definition
    ===================================  ============
    First moment of area in :math:`y`    :math:`Q_y = \\int_{A} y \mathrm{dA}`
    First moment of area in :math:`z`    :math:`Q_z = \\int_{A} z \mathrm{dA}`
    Second moment of area in :math:`y`   :math:`I_y = \\int_{A} y^2 \mathrm{dA}`
    Second moment of area in :math:`z`   :math:`I_z = \\int_{A} z^2 \mathrm{dA}`
    Second moment of area in :math:`yz`  :math:`I_{yz} = \\int_{A} yz \mathrm{dA}`
    Polar moment of area                 :math:`J = I_y + I_z`
    Centroid                             :math:`c = \\frac{1}{A}(Q_y, Q_z)`
    ===================================  ============

    Here, :math:`A` is the cross-section area. Those integrals area approximated by numeric integration when  or ``element_type = 'pipe_2'``. Futhermore, these formulations approximates shear properties like the shear coefficients and the shear center coordinates :math:`c_s` by solving a Differential Problem within the section. On the other hand, when ``element_type = 'beam_1'``, analytical approximation of each property is computed. The user is also allowed to provide the properties of any cross-section through the parameters ``self.area``, ``self.Iyy``, ``self.Izz``, ``self.Iyz``, and ``self.shear_coefficient``. From the acoustic point of view, the **pipes** element types also provide the acoustic cross-section area called ``self.fluid_area``.

    Parameters
    ----------
    element_type : ['pipe_1','pipe_2','beam_1'], optional
        Element type of the structural elements associated to the cross-section.
        Default is 'pipe_1'.

    poisson_ratio : float, optional
        Poisson's ration of the material attributed to the structural elements. Only needed when ``element_type = 'pipe_1'``.
        Default is 0.

    division_number : [8, 16, 32, 64, 128], optional
        Cross-section division number. This number is directly associated with the number of elements used in the process of approximating the cross-section shear properties. Only needed when ``element_type = 'pipe_1'``.
        Default is 64.
    
    pipe_section_info : dict, optional
        Pipe section data is stored in a dictionary with the following structure ``{"outer_diameter" : , "thickness" : , "offset_y" : , "offset_z" : , "insulation_thickness" : , "insulation_density" : }``, and whose visual definitions and orientation can be seen in the :ref:`figure <figPipe>`. The expected values, its data types and descriptions are: ::

            "outer_diameter" : float
                Pipe outer diameter.

            "thickness" : float
                Pipe wall thickness.

            "offset_y" : float
                y coordinate of the pipe eccentricity offset.

            "offset_z" : float
                z coordinate of the pipe eccentricity offset.

            "insulation_thickness" : float
                Pipe insolation thickness.

            "insulation_density" : float
                Pipe insolation density.
        
        .. _figPipe:

        .. figure:: /figures/Pipe_section.svg
            :align: center

            Pipe section parameters and offset orientation.

    beam_section_info : dict, optional
        Beam section data is stored in a dictionary with the following structure ``{"section_type_label" : , "section_parameters" : }``. The pared value of ``"section_type_label"`` must be one of the following ``str``: ``'C-section', 'Circular section', 'I-section', 'Rectangular section', 'T-section'`` according to the wished beam section. And ``"section_parameters"`` is a list whose unwraping depends on the chosen one. For each section, it is shown up next the expected list structure.
        
        - **C-section** unwraps as follows:

            >>> [h, w1, t1, w2, t2, tw, offset_y, offset_z] = section_parameters
        
        Their visual definitions and orientation are presented in :ref:`figure <figCsection>`, and their data types and description are: ::

            h : float
                Profile height.

            w1 : float
                Upper profile width.

            t1 : float
                Upper profile thickness.

            w2 : float
                Lower profile width.

            t2 : float
                Lower profile thickness.

            tw : float
                Thickness.

            offset_y : float
                y coordinate of the centroid offset.

            offset_z : float
                z coordinate of the centroid offset.
        
        .. _figCsection:

        .. figure:: /figures/C_profile.svg
            :align: center

            C-section parameters and offset orientation.
        
        - **Circular section** unwraps as follows:

            >>> [d_out, thickness, offset_y, offset_z] = section_parameters
            
        Their visual definitions and orientation are presented in :ref:`figure <figCircularsection>`, and their data types and description are: ::

            d_out : float
                External diameter.

            thickness : float
                Thickness.

            offset_y : float
                y coordinate of the centroid offset.

            offset_z : float
                z coordinate of the centroid offset.
        
        .. _figCircularsection:

        .. figure:: /figures/Circular.svg
            :align: center

            Circular section parameters and offset orientation.
        
        - **I-section** unwraps as follows:
        
            >>> [h, w1, t1, w2, t2, tw, offset_y, offset_z] = section_parameters
        
        Their visual definitions and orientation are presented in :ref:`figure <figIsection>`, and their data types and description are: ::

            h : float
                Profile height.

            w1 : float
                Upper profile width.

            t1 : float
                Upper profile thickness.

            w2 : float
                Lower profile width.

            t2 : float
                Lower profile thickness.

            tw : float
                Thickness.

            offset_y : float
                y coordinate of the centroid offset.

            offset_z : float
                z coordinate of the centroid offset.
        
        .. _figIsection:

        .. figure:: /figures/I_profile.svg
            :align: center

            I-section parameters and offset orientation.
        
        - **T-section** unwraps as follows:
        
            >>> [h, w1, t1, tw, offset_y, offset_z] = section_parameters
            
        Their visual definitions and orientation are presented in :ref:`figure <figTsection>`, and their data types and description are: ::

            h : float
                Profile height.

            w1 : float
                Upper profile width.

            t1 : float
                Upper profile thickness.

            tw : float
                Thickness.

            offset_y : float
                y coordinate of the centroid offset.

            offset_z : float
                z coordinate of the centroid offset.
        
        .. _figTsection:

        .. figure:: /figures/T_profile.svg
            :align: center

            T-section parameters and offset orientation.

    valve_section_info : dict, optional
        Valve section data is stored in a dictionary with the following structure ``{"section_parameters" : , "diameters_to_plot" : }``. The pared value of ``"diameters_to_plot"`` are used in rendering of the UI and it's suggested to attribute ``[None, None]``. Likewise the ``pipe_section_info``, the paired value of ``"section_parameters"`` is another dictionary with the structure ``{"outer_diameter" : , "thickness" : , "offset_y" : , "offset_z" : , "insulation_thickness" : , "insulation_density" : }``, and whose visual definitions and orientation is the same as seen in the :ref:`figure <figPipe>` for the Pipe section. The expected values, its data types and descriptions are: ::

            "outer_diameter" : float
                Pipe outer diameter.

            "thickness" : float
                Pipe wall thickness.

            "offset_y" : float
                y coordinate of the pipe eccentricity offset.

            "offset_z" : float
                z coordinate of the pipe eccentricity offset.

            "insulation_thickness" : float
                Pipe insolation thickness.

            "insulation_density" : float
                Pipe insolation density.

    generic_section_info : list, optional
        Generic section data is stored in a list that unwraps as follows ``[area, Iyy, Izz, Iyz, shear_factor, Yc, Zc] = generic_section_info``. Their definitions were presented in the <table `tabDefinitions`_>, and their data types and description are: ::

            "area" : float
                cross-section area.

            "Yc" : float
                y coordinate of the centroid.

            "Zc" : float
                z coordinate of the centroid.

            "Iyy" : float
                cross-section second moment of area with respect to the y direction.

            "Izz" : float
                cross-section second moment of area with respect to the z direction.

            "Iyz" : float
                cross-section second moment of area with respect to the yz plane.

            "shear_coefficient" : float
                cross-section shear coefficient.
        
    """
    
    def __init__(self, **kwargs):
            
        self.division_number = kwargs.get('division_number', 64)
        self.element_type = kwargs.get('element_type', 'pipe_1')
        self.poisson_ratio = kwargs.get('poisson_ratio', 0)
                
        # Pipe section parameters
        self.outer_diameter = 0
        self.thickness = 0
        self.offset_y = 0
        self.offset_z = 0
        self.offset = [self.offset_y, self.offset_z]
        self.insulation_thickness = 0
        self.insulation_density = 0
        self.offset_virtual = None

        # Beam section properties
        self.area = 0
        self.first_moment_area_y = 0
        self.first_moment_area_z = 0
        self.second_moment_area_y = 0
        self.second_moment_area_z = 0
        self.second_moment_area_yz = 0
        self.polar_moment_area = 0
        self.y_centroid = 0
        self.z_centroid = 0
        self.shear_coefficient = 1

        # Shear properties
        self.y_shear = 0
        self.z_shear = 0
        self.res_y = 0
        self.res_z = 0
        # self.res_yz = 0

        # Principal Bending Axis Rotation
        self.principal_axis = None
        self.principal_axis_translation = None

        # Input cluster data for pipe and beam sections 
        self.pipe_section_info = kwargs.get('pipe_section_info', None)
        self.beam_section_info = kwargs.get('beam_section_info', None)
        self.generic_section_info = kwargs.get('generic_section_info', None)
        self.expansion_joint_info = kwargs.get('expansion_joint_info', None)
        self.valve_section_info = kwargs.get('valve_section_info', None)
      
        self.section_label = kwargs.get('section_label', None)
        self.section_parameters = kwargs.get('section_parameters', None)
        self.expansion_joint_plot_key = None

        # Unwrap cluster data for pipe sections 
        if self.pipe_section_info:
            self.section_label = "Pipe section"

            self.outer_diameter = self.pipe_section_info["outer_diameter"]
            self.thickness =  self.pipe_section_info["thickness"]
            self.offset_y = self.pipe_section_info["offset_y"]
            self.offset_z = self.pipe_section_info["offset_z"]
            self.insulation_thickness = self.pipe_section_info["insulation_thickness"]
            self.insulation_density = self.pipe_section_info["insulation_density"]
            self.offset = [self.offset_y, self.offset_z]

            self.section_info = {  "section_type_label" : self.section_label,
                                   "section_parameters" : self.pipe_section_info }

        # Unwrap cluster data for valve sections 
        if self.valve_section_info:
            self.section_label = "Valve section"
            self.section_parameters = self.valve_section_info["section_parameters"]

            self.outer_diameter = self.section_parameters["outer_diameter"]
            self.thickness =  self.section_parameters["thickness"]
            self.offset_y = self.section_parameters["offset_y"]
            self.offset_z = self.section_parameters["offset_z"]
            self.insulation_thickness = self.section_parameters["insulation_thickness"]
            self.insulation_density = self.section_parameters["insulation_density"]
            self.offset = [self.offset_y, self.offset_z]

            self.section_info = self.valve_section_info
            self.section_info["section_type_label"] = self.section_label
            try:
                self.outer_diameter_to_plot, self.inner_diameter_to_plot = self.valve_section_info["diameters_to_plot"]
            except:
                self.outer_diameter_to_plot, self.inner_diameter_to_plot = None, None

        # Unwrap cluster data for beam sections 
        if self.beam_section_info:
            self.section_label = self.beam_section_info["section_type_label"]
            self.section_parameters = self.beam_section_info["section_parameters"]

            self.section_properties = get_beam_section_properties(self.section_label, self.section_parameters)
            
            self.section_info = {  "section_type_label" : self.section_label,
                                   "section_parameters" : self.section_parameters,
                                   "section_properties" : self.section_properties  }

            self.area = self.section_properties['area']
            self.second_moment_area_y = self.section_properties['Iyy']
            self.second_moment_area_z = self.section_properties['Izz']
            self.second_moment_area_yz = self.section_properties['Iyz']
            self.offset_y = self.section_properties['Yc']
            self.offset_z = self.section_properties['Zc']
            self.offset = [self.offset_y, self.offset_z]

        if self.generic_section_info is not None:
            self.section_label = "Generic section"
            self.section_parameters = None

            self.section_properties = get_beam_section_properties(self.section_label, self.generic_section_info)
            
            self.section_info = {  "section_type_label" : self.section_label,
                                   "section_parameters" : self.section_parameters,
                                   "section_properties" : self.section_properties  }

            self.area = self.section_properties['area']
            self.second_moment_area_y = self.section_properties['Iyy']
            self.second_moment_area_z = self.section_properties['Izz']
            self.second_moment_area_yz = self.section_properties['Iyz']
            self.offset_y = self.section_properties['Yc']
            self.offset_z = self.section_properties['Zc']
            self.offset = [self.offset_y, self.offset_z]
            self.shear_coefficient = self.section_properties['shear factor']
        
        if self.expansion_joint_info is not None:
            self.section_label = self.expansion_joint_info[0]
            self.expansion_joint_plot_key = self.expansion_joint_info[1]
            self.outer_diameter = self.expansion_joint_info[2]
                    
    @property
    def outer_radius(self):
        """:float: Cross-section outer radius
        """
        return self.outer_diameter/2

    @property
    def inner_diameter(self):
        """:float: Cross-section inner diameter
        """
        return self.outer_diameter - 2*self.thickness

    @property
    def inner_radius(self):
        """:float: Cross-section inner radius
        """
        return self.inner_diameter/2

    @property
    def area_fluid(self):
        """:float: Cross-section inner area, which corresponds to the acoustic domain cross-section area.
        """
        return (self.inner_diameter**2) * pi / 4

    @property
    def area_insulation(self):
        """:float: Cross-section insulation area.
        """
        return (((self.outer_diameter+2*self.insulation_thickness)**2)-(self.outer_diameter**2)) * pi / 4

    def mesh_connectivity(self):
        """
        This method returns the tube cross mesh connectivity formed by Q9 (9-node quadrilateral element). The element-wise reference numbering follows the pattern: ::

                 y, r
                  ^
                  |
            2-----6-----3
            |           |
            |           |
            5     8     7 --> x, θ
            |           |
            |           |
            1-----4-----0

        Returns
        -------
        (N, 9) array
            Connectivity of the tube cross mesh, where ``N = self.division_number``.

        See also
        --------
        mesh_coordinate : Nodal coordinates of the tube cross mesh.
        """
        connectivity = np.zeros([self.division_number, 9], dtype = int)
        ind = 6*np.arange(self.division_number)
        connectivity[:-1,:] = np.array([8,2,0,6,5,1,3,7,4]) + ind[:-1].reshape(-1,1)
        aux = ind[-1]
        connectivity[-1,:] = [2,2+aux,aux,0,5+aux,1+aux,3+aux,1,4+aux]
        self.connectivity = connectivity
        return connectivity
    
    def mesh_coordinate(self):
        """
        This method returns nodal coordinates of the tube cross mesh formed by Q9 (9-node quadrilateral element). The node coordinates and global numbering are created following the pattern: ::

                 y, r
                  ^
                  |
            0-----3      N-3
            |     |      |
            |     |      |
            1     4 ...  N-2   --> x, θ
            |     |      |
            |     |      |
            2-----5      N-1

        Returns
        -------
        (N, 2) array
            Nodal coordinates of the tube cross mesh. Here, ``N = 6*self.division_number`` because each element has 9 nodes, but it shares 3 nodes with each neighbor element. The ``i``-th row has the ``(x, y)`` coordinates of the ``i``-th node.

        See also
        --------
        mesh_connectivity : Connectivity of the tube cross mesh.
        """
        # coordinates of points on the face
        r_o = self.outer_diameter / 2
        r_i = self.inner_diameter / 2

        if self.offset_virtual is None:
            offset = self.offset
        else:
            offset = self.offset_virtual # used in element_type = 'pipe_1'

        angular_increment = 2*pi / (2*self.division_number)
        aux = np.arange( 2*self.division_number )
        theta = aux*angular_increment
        ind = 3*aux
                    
        self.number_nodes = 6 * self.division_number
        coordinate = np.zeros((self.number_nodes, 2))
        sine = np.sin(theta, dtype='float64')
        cossine = np.cos(theta, dtype='float64')
        coordinate[ind + 0, 0] = r_o * cossine - offset[0]
        coordinate[ind + 0, 1] = r_o * sine - offset[1]
        coordinate[ind + 1, 0] = (r_o + r_i)/2 * cossine - offset[0]
        coordinate[ind + 1, 1] = (r_o + r_i)/2 * sine - offset[1]
        coordinate[ind + 2, 0] = r_i * cossine - offset[0]
        coordinate[ind + 2, 1] = r_i * sine - offset[1]
        return coordinate
    
    def preprocessing(self, el_type = 'pipe_1'):
        """
        This method process the cross-section mesh to generate in advance the arrays necessary to compute the section's shear properties. The arrays have the dimension of the total number of integration points ``N = N_int_points*self.division_number``, where ``N_int_points = 4`` is standard in OpenPulse.

        Parameters
        ----------
        el_type : ['pipe_1','pipe_2'], optional
            Element type of the structural elements attributed to the tube.
            Default is 'pipe_1'.

        Returns
        -------
        jac : (N, 2, 2) array
            Jacobian matrix of each integration point. It's a 3D matrix such that ``jac[p,:,:]`` is the Jacobian matrix of the ``p``-th integration point (2-by-2 matrix).

        inv_jac : (N, 2, 2) array
            Inverse of the Jacobian matrix of integration point. It's a 3D matrix such that ``inv_jac[p,:,:]`` is the inverse of the Jacobian matrix of the ``p``-th integration point (2-by-2 matrix).

        dA : (N,) array
            Differential of area of each integration point.

        y : (N,) array
            `y`-coordinate in the global coordinate system of each integration point.

        z : (N,) array
            `z`-coordinate in the global coordinate system of each integration point.
        """
        
        N = self.division_number*N_int_points
        _, weight = _gauss_quadrature2D()
        self.mesh_connectivity()
        self.mat_phi, self.mat_dphi = _get_all_shape_functions()
        phi = self.mat_phi
        dphi = self.mat_dphi

        if el_type == 'pipe_1':
            # for the pipe_1 element, offset and its dependence need to be updated
            self.offset_virtual = self.offset + np.array([self.y_centroid, self.z_centroid]) 
            coordinate = self.mesh_coordinate()
        else:
            coordinate = self.mesh_coordinate()
        
        # Preallocating the variables
        jac = np.zeros((N,2,2), dtype='float64')
        inv_jac = np.zeros((N,2,2), dtype='float64')
        y = np.zeros(N, dtype='float64')
        z = np.zeros(N, dtype='float64')

        ind=0
        for el in range( self.division_number ): # Integration over each element
            indexes = self.connectivity[el,:]
            for k in range(N_int_points):   # integration points
                jac[ind,:,:] = dphi[k,:,:]@coordinate[indexes,:]
                y[ind], z[ind] = phi[k,:]@coordinate[indexes,:]
                inv_jac[ind,:,:] = inv(jac[ind,:,:])
                ind += 1
        aux = jac.reshape(N,4)
        detjac = (aux[:,0]*aux[:,3])-(aux[:,1]*aux[:,2])
        return jac, inv_jac, detjac*weight, y, z
            
    def area_properties(self, el_type = 'pipe_1'):
        """
        This method updates the tube cross area properties: area ``self.area``, first moment of area relative to y ``self.first_moment_area_y``, first moment of area relative to z ``self.first_moment_area_z``, second moment of area relative to y ``self.second_moment_area_y``, second moment of area relative to z ``self.second_moment_area_z``, second moment of area relative to yz ``self.second_moment_area_yz``, second polar moment of area ``self.polar_moment_area``, and centroid coordinate ``(self.y_centroid, self.z_centroid)``.

        Parameters
        ----------
        el_type : ['pipe_1','pipe_2','beam_1']
            Element type of the structural elements attributed to the tube or beam.
            Default is 'pipe_1'.
        """
        self.jac, self.inv_jac, self.dA, self.y, self.z = self.preprocessing(el_type = el_type)

        A = np.sum(self.dA)
        Iy = np.sum(((self.z**2)*self.dA))
        Iz = np.sum(((self.y**2)*self.dA))
        Iyz = np.sum(((self.z*self.y)*self.dA))
        Qy = np.sum(self.z*self.dA)
        Qz = np.sum(self.y*self.dA)
        self.area = A
        self.first_moment_area_y = Qy
        self.first_moment_area_z = Qz
        self.second_moment_area_y = Iy
        self.second_moment_area_z = Iz
        self.second_moment_area_yz = Iyz
        self.polar_moment_area = Iy + Iz
        self.y_centroid = Qz/A
        self.z_centroid = Qy/A

    def assembly_indexes(self):
        """
        This method updates rows and columns index maps used in the assembly process. ``self.rows_ind`` and ``self.cols_ind`` are **(N,) arrays** that map all degrees of freedom onto the respective row and column of the system's global matrix. 
        """
        cols = 9
        cols_dofs = self.connectivity
        J = np.tile(cols_dofs, cols)
        I = cols_dofs.reshape(-1,1)@np.ones((1,cols), dtype=int) 
        self.rows_ind = I.reshape(-1)
        self.cols_ind = J.reshape(-1)
                            
    def shear_properties(self, poisson_ratio = 0, el_type = 'pipe_1'):
        """
        This method updates the tube cross shear properties shear coefficients ``self.res_y``, ``self.res_z`` and ``self.res_yz``, and shear center coordinates ``(self.y_shear, self.z_shear)``.

        Parameters
        ----------
        poisson_ratio : float, optional
            Poisson's ration of the material attributed to the tube.
            Default is 0.

        el_type : ['pipe_1','pipe_2','beam_1'], optional
            Element type of the structural elements attributed to the tube.
            Default is 'pipe_1'.
        """
        self.area_properties(el_type)
        self.assembly_indexes()

        phi = self.mat_phi
        dphi = self.mat_dphi

        inv_jac = self.inv_jac
        A = self.area
        dA = self.dA
        y = self.y
        z = self.z
        Iy = self.second_moment_area_y 
        Iz = self.second_moment_area_z
        Iyz = self.second_moment_area_yz

        NGL = self.number_nodes#*DOFS_PER_NODE
        N = self.division_number*N_int_points

        # Shear Coefficients
        Fy = np.zeros(NGL)
        Fz = np.zeros(NGL)
        FT = np.zeros(NGL)
        # 
        matrix_aux2 =   np.array([[Iy, -Iyz],[Iyz, Iy]])
        matrix_aux3 = - np.array([[Iyz, -Iz],[Iz, Iyz]])
        mat_aux_dphi = (np.ones((self.division_number,1))@dphi.reshape(1,-1)).reshape(-1)
        aux_dphi = mat_aux_dphi.reshape([N,2,9])
        mat_aux_phi = (np.ones((self.division_number,1))@phi.reshape(1,-1)).reshape(-1)
        aux_phi = mat_aux_phi.reshape(N,9)
        vec = np.array([z, -y]).T
        vec_dA = vec*dA.reshape(-1,1)
        vector_aux = (np.array([y**2 - z**2, 2*y*z]).T).reshape(-1,2,1)
        add_y = 2*(1 + poisson_ratio)*aux_phi*(Iy*y - Iyz*z).reshape(-1,1)
        add_z = 2*(1 + poisson_ratio)*aux_phi*(Iz*z - Iyz*y).reshape(-1,1)

        d = (matrix_aux2@vector_aux).reshape(-1,2)
        h = (matrix_aux3@vector_aux).reshape(-1,2)
        dphig = inv_jac@aux_dphi
        dphig_T = np.transpose(dphig,(0,2,1)) 
        mat_ke = (dphig_T@dphig)*dA.reshape(-1,1,1)
        data_ke = np.zeros((self.division_number, 9, 9), dtype='float64')

        i = 0
        for el in range( self.division_number ): # Integration over each cross-sections element
            Ke =  0
            indexes = self.connectivity[el,:]
            for _ in range(N_int_points):
                Ke += mat_ke[i,:,:]
                Fy[indexes] += ( poisson_ratio/2 * dphig_T[i,:,:] @ d[i,:] + add_y[i])*dA[i]
                Fz[indexes] += ( poisson_ratio/2 * dphig_T[i,:,:] @ h[i,:] + add_z[i])*dA[i]
                FT[indexes] += ( dphig_T[i,:,:] @ vec_dA[i] )
                i += 1
            data_ke[el,:,:] = Ke
        K_lg = coo_matrix((data_ke.reshape(-1), (self.rows_ind, self.cols_ind)), shape=(NGL+1, NGL+1), dtype='float64')
                                            
        # Pseudo inverse used to remedy numerical instability
        inv_K_lg = pinv(K_lg.toarray())

        u2 = inv_K_lg @ np.append(Fy, 0)
        u3 = inv_K_lg @ np.append(Fz, 0)
        psi_y = u2[:-1]
        psi_z = u3[:-1]
        d_poisson = d*poisson_ratio/2
        h_poisson = h*poisson_ratio/2
        dA = dA.reshape(-1,1)
        mat_dptemp = np.zeros((N, 2), dtype='float64')
        mat_hptemp = np.zeros((N, 2), dtype='float64')

        i=0
        alpha_y = alpha_z = alpha_yz = 0
        for el in range( self.division_number ): # Integration over each cross 
            indexes = self.connectivity[el,:]
            Np = N_int_points*el
            mat_dptemp[0+Np:4+Np,:] = (dphig[0+Np:4+Np,:,:] @ psi_y[indexes]) - d_poisson[0+Np:4+Np,:]
            mat_hptemp[0+Np:4+Np,:] = (dphig[0+Np:4+Np,:,:] @ psi_z[indexes]) - h_poisson[0+Np:4+Np,:]
        
        alpha_y =  np.sum( mat_dptemp*mat_dptemp*dA )
        alpha_z =  np.sum( mat_hptemp*mat_hptemp*dA )
        alpha_yz = np.sum( mat_dptemp*mat_hptemp*dA )
        
        ccg = 2 * (1 + poisson_ratio) * (Iy*Iz - (Iyz**2))
        A_ccg2 = (A/(ccg**2))

        self.res_y = A_ccg2*(alpha_y)
        self.res_z = A_ccg2*(alpha_z)
        self.res_yz = A_ccg2*(alpha_yz)

        # shear center
        self.y_shear = -(psi_z.T @ FT)/ccg
        self.z_shear = (psi_y.T @ FT)/ccg

    def offset_rotation(self, el_type = 'pipe_1'):
        """
        This method updates the tube cross-section rotation due to the shear effects and eccentricity offset.

        Parameters
        ----------
        el_type : ['pipe_1','pipe_2','beam_1'], optional
            Element type of the structural elements attributed to the tube.
            Default is 'pipe_1'.
        """
        if el_type == 'pipe_2':
            self.principal_axis = np.eye(12)
            return

        if el_type == 'beam_1':
            self.y_shear, self.z_shear = self.get_beam_shear_center()
            y_c = self.y_centroid + self.offset_y
            z_c = self.z_centroid + self.offset_z
            y_s = self.y_shear + self.offset_y
            z_s = self.z_shear + self.offset_z
        else:
            y_c = self.y_centroid
            z_c = self.z_centroid
            y_s = self.y_shear
            z_s = self.z_shear

        if norm(self.offset) > 0:
            Iy = self.second_moment_area_y 
            Iz = self.second_moment_area_z
            Iyz = self.second_moment_area_yz
            if Iz==Iy:
                if Iyz>0:
                    angle = pi/2
                elif Iyz<0:
                    angle = -pi/2
            else:
                angle = atan(2*Iyz/(Iz-Iy))/2
            # Rotational part of transformation matrix
            rotation = np.array([[ 1. ,      0.   ,    0.    ],
                                [ 0. ,cos(angle) ,sin(angle)],
                                [ 0. ,-sin(angle),cos(angle)]])
            # Translational part of transformation matrix
            translation = np.array([[ 0  , z_c,-y_c],
                                    [-z_s,  0 , 0  ],
                                    [y_s ,  0 , 0  ]])
            T = np.eye(12)
            T[0:3,3:6]   = translation
            T[6:9,9:12]  = translation
            #
            R = np.zeros([12, 12])
            R[0:3, 0:3]  = R[3:6, 3:6] = R[6:9, 6:9] = R[9:12, 9:12] = rotation
            self.principal_axis_translation = T
            self.principal_axis = R @ T
        else:
            translation = np.array([[ 0  , z_c,-y_c],
                                    [-z_s,  0 , 0  ],
                                    [y_s ,  0 , 0  ]])
            T = self.principal_axis_rotation = np.eye(12)
            T[0:3,3:6]   = translation
            T[6:9,9:12]  = translation
            self.principal_axis_translation = T
            self.principal_axis = T

    def update_properties(self):
        """
        This method updates all the tube cross-section properties.
        """
        # self.area_properties(None)
        if self.element_type == 'pipe_1':
            self.shear_properties(poisson_ratio = 0, el_type = None)
            self.offset_rotation(el_type = 'pipe_1')
            self.shear_properties(poisson_ratio = 0, el_type = 'pipe_1')
        else:
            self.shear_properties(poisson_ratio=self.poisson_ratio, el_type=self.element_type)
    
    ## Beam related methods
    def get_beam_shear_center(self):
        """
        """
        if self.section_label == "Rectangular section":
            return 0, 0

        elif self.section_label == "Circular section":
            return 0, 0
        
        elif self.section_label == "C-section":
            h, w1, t1, w2, t2, tw, _, _ = self.section_parameters

            b1 = w1
            b2 = w2

            kw = tw/t1
            k2 = t2/t1
            t1 = 1e-8
            t2 = k2*t1
            tw = kw*t1

            y1 = b1/2
            y2 = b2/2
            y3 = 0

            z1 = h
            z2 = 0
            z3 = h/2

            A1 = b1*t1
            A2 = b2*t2
            A3 = tw*h
            A = A1 + A2 + A3

            yc = (y1*A1 + y2*A2 + y3*A3)/A
            zc = (z1*A1 + z2*A2 + z3*A3)/A

            Iyy_1 = (b1*(t1**3))/12 + ((z1-zc)**2)*A1
            Iyy_2 = (b2*(t2**3))/12 + ((z2-zc)**2)*A2
            Iyy_3 = (tw*(h**3))/12 + ((z3-zc)**2)*A3
            Iyy = Iyy_1 + Iyy_2 + Iyy_3

            Izz_1 = (t1*(b1**3))/12 + ((y1-yc)**2)*A1
            Izz_2 = (t2*(b2**3))/12 + ((y2-yc)**2)*A2
            Izz_3 = (h*(tw**3))/12 + ((y3-yc)**2)*A3
            Izz = Izz_1 + Izz_2 + Izz_3

            Iyz_1 = (y1-yc)*(z1-zc)*A1
            Iyz_2 = (y2-yc)*(z2-zc)*A2
            Iyz_3 = (y3-yc)*(z3-zc)*A3
            Iyz = Iyz_1 + Iyz_2 + Iyz_3

            F1_Vz = -((b1**2)*t1/(6*(Iyy*Izz-Iyz**2)))*(Iyz*(2*b1-3*yc) - 3*Izz*(h-zc))
            F1_Vy = -((b1**2)*t1/(6*(Iyy*Izz-Iyz**2)))*(-Iyy*(2*b1-3*yc) + 3*Iyz*(h-zc))

            e_y = h*F1_Vz
            e_z = h*F1_Vy
            
            return e_y, e_z

        elif self.section_label == "I-section":
            h, w1, t1, w2, t2, tw, _, _ = self.section_parameters

            b1 = w1
            b2 = w2

            kw = tw/t1
            k2 = t2/t1
            t1 = 1e-8
            t2 = k2*t1
            tw = kw*t1

            y1 = 0
            y2 = 0
            y3 = 0

            z1 = h
            z2 = 0
            z3 = h/2

            A1 = b1*t1
            A2 = b2*t2
            A3 = tw*h
            A = A1 + A2 + A3

            yc = (y1*A1 + y2*A2 + y3*A3)/A
            zc = (z1*A1 + z2*A2 + z3*A3)/A

            Iyy_1 = (b1*(t1**3))/12 + ((z1-zc)**2)*A1
            Iyy_2 = (b2*(t2**3))/12 + ((z2-zc)**2)*A2
            Iyy_3 = (tw*(h**3))/12 + ((z3-zc)**2)*A3
            Iyy = Iyy_1 + Iyy_2 + Iyy_3

            Izz_1 = (t1*(b1**3))/12 + ((y1-yc)**2)*A1
            Izz_2 = (t2*(b2**3))/12 + ((y2-yc)**2)*A2
            Izz_3 = (h*(tw**3))/12 + ((y3-yc)**2)*A3
            Izz = Izz_1 + Izz_2 + Izz_3

            Iyz_1 = (y1-yc)*(z1-zc)*A1
            Iyz_2 = (y2-yc)*(z2-zc)*A2
            Iyz_3 = (y3-yc)*(z3-zc)*A3
            Iyz = Iyz_1 + Iyz_2 + Iyz_3

            F1_Vy = ((b1**3)*t1/(12*Izz))
            # F1_Vz = ((b1**2)*t1/(8*Iyy))*(h-zc)

            e_y = 0
            e_z = h*F1_Vy

            return e_y, e_z

        elif self.section_label == "T-section":
            h, w1, t1, tw, _, _ = self.section_parameters

            b1 = w1

            kw = tw/t1
            t1 = 1e-8
            kw = 1000
            tw = kw*t1

            y1 = 0
            y2 = 0

            z1 = h
            z2 = h/2

            A1 = b1*t1
            A2 = tw*h
            A = A1 + A2

            yc = (y1*A1 + y2*A2)/A
            zc = (z1*A1 + z2*A2)/A

            Iyy_1 = (b1*(t1**3))/12 + ((z1-zc)**2)*A1
            Iyy_2 = (tw*(h**3))/12 + ((z2-zc)**2)*A2
            Iyy = Iyy_1 + Iyy_2

            Izz_1 = (t1*(b1**3))/12 + ((y1-yc)**2)*A1
            Izz_2 = (h*(tw**3))/12 + ((y2-yc)**2)*A2
            Izz = Izz_1 + Izz_2

            Iyz_1 = (y1-yc)*(z1-zc)*A1
            Iyz_2 = (y2-yc)*(z2-zc)*A2
            Iyz = Iyz_1 + Iyz_2

            F1_Vy = ((b1**3)*t1/(12*Izz))
            # F1_Vz = ((b1**2)*t1/(8*Iyy))*(h-zc)

            e_y = 0
            e_z = h*F1_Vy
     
            return e_y, e_z
    
    def get_cross_section_points(self, length):
        """
        """

        inner_points = []
        length = round(length, 4)

        if self.section_label == "Pipe section": # Pipe section - It's a pipe section, so ignore for beam plots

            # N = element.cross_section.division_number
            N = 32 # temporary number of divisions for pipe sections
 
            d_out = self.outer_diameter
            d_in = d_out - 2*self.thickness

            d_theta = 2*np.pi/N
            theta = -np.arange(0, 2*np.pi, d_theta)
            sine = np.sin(theta)
            cossine = np.cos(theta)
            
            Y_out = (d_out/2)*cossine + self.offset_y
            Z_out = (d_out/2)*sine + self.offset_z
            Y_in = (d_in/2)*cossine + self.offset_y
            Z_in = (d_in/2)*sine + self.offset_z

            if self.insulation_thickness != float(0):
                Y_out = ((d_out + 2*self.insulation_thickness)/2)*cossine + self.offset_y
                Z_out = ((d_out + 2*self.insulation_thickness)/2)*sine + self.offset_z

            outer_points = list(zip(Y_out, Z_out))
            inner_points = list(zip(Y_in, Z_in))

        elif self.section_label == "Rectangular section": # Beam: Rectangular section

            b, h, b_in, h_in, offset_y, offset_z = self.section_parameters           
            # Y_out = np.array([(b/2), (b/2), -(b/2), -(b/2), (b/2)]
            # Z_out = np.array([(h/2), -(h/2), -(h/2), (h/2), (h/2)]
            Y_out = np.array([(b/2), (b/2),  (b/2), 0, -(b/2), -(b/2), -(b/2), 0]) + offset_y
            Z_out = np.array([(h/2), 0, -(h/2), -(h/2), -(h/2), 0, (h/2), (h/2)]) + offset_z
            outer_points = list(zip(Y_out, Z_out))

            if b_in != 0:
                Y_in = np.array([(b_in/2), (b_in/2), -(b_in/2),  -(b_in/2)]) + offset_y
                Z_in = np.array([(h_in/2), -(h_in/2), -(h_in/2), (h_in/2)]) + offset_z
                inner_points = list(zip(Y_in, Z_in))
            
        elif self.section_label == "Circular section": # Beam: Circular section
            
            N = 24# element.cross_section.division_number
            d_out, thickness, offset_y, offset_z = self.section_parameters
            if thickness == 0:
                d_in = 0
            else:
                d_in = d_out - 2*thickness

            d_theta = np.pi/N
            theta = -np.arange(0, 2*np.pi, d_theta)

            sine = np.sin(theta)
            cossine = np.cos(theta)

            Y_out = (d_out/2)*cossine + offset_y 
            Z_out = (d_out/2)*sine + offset_z
            outer_points = list(zip(Y_out, Z_out))
                        
            if d_in != 0.:
                Y_in = (d_in/2)*cossine + offset_y
                Z_in = (d_in/2)*sine + offset_z
                inner_points = list(zip(Y_in, Z_in))
            
        elif self.section_label == 'C-section': # Beam: C-section

            h, w1, t1, w2, t2, tw, offset_y, offset_z = self.section_parameters
            Yp_out = [0, w2, w2, tw, tw, w1, w1, 0]
            Zp_out = [-(h/2), -(h/2), -((h/2)-t2), -((h/2)-t2), ((h/2)-t1), ((h/2)-t1), (h/2), (h/2)]

            Y_out = np.array(Yp_out) + offset_y
            Z_out = np.array(Zp_out) + offset_z
            outer_points = list(zip(Y_out, Z_out))

        elif self.section_label == 'I-section': # Beam: I-section

            h, w1, t1, w2, t2, tw, offset_y, offset_z = self.section_parameters
            Yp_out = [(w1/2), (w1/2), (tw/2), (tw/2), (w2/2), (w2/2), -(w2/2), -(w2/2), -(tw/2), -(tw/2), -(w1/2), -(w1/2)]
            Zp_out = [(h/2), (h/2)-t1, (h/2)-t1, -(h/2)+t2, -(h/2)+t2, -(h/2), -(h/2), -(h/2)+t2, -(h/2)+t2, (h/2)-t1, (h/2)-t1, (h/2)]
            
            Y_out = np.array(Yp_out) + offset_y
            Z_out = np.array(Zp_out) + offset_z
            outer_points = list(zip(Y_out, Z_out))
    
        elif self.section_label == 'T-section': # Beam: T-section

            h, w1, t1, tw, offset_y, offset_z = self.section_parameters
            Yp_out = [(w1/2), (w1/2), (tw/2), (tw/2), -(tw/2), -(tw/2), -(w1/2), -(w1/2)]
            Zp_out = [(h/2), (h/2)-t1, (h/2)-t1, -(h/2), -(h/2), (h/2)-t1, (h/2)-t1, (h/2)]

            Y_out = np.array(Yp_out) + offset_y
            Z_out = np.array(Zp_out) + offset_z
            outer_points = list(zip(Y_out, Z_out))
        
        elif self.section_label == "Expansion joint section" : #
    
            N = 32 # temporary number of divisions for pipe sections
    
            if self.expansion_joint_plot_key == "major":
              r_out = self.outer_radius*1.25 
            
            elif self.expansion_joint_plot_key == "minor":
                r_out = self.outer_radius*1.1            
            
            else:
                r_out = self.outer_radius*1.4
            
            r_in = self.outer_radius*0.8

            d_theta = 2*np.pi/N
            theta = -np.arange(0, 2*np.pi, d_theta)
            sine = np.sin(theta)
            cossine = np.cos(theta)
            
            Y_out = r_out*cossine + self.offset_y
            Z_out = r_out*sine + self.offset_z
            Y_in = r_in*cossine + self.offset_y
            Z_in = r_in*sine + self.offset_z
            
            outer_points = list(zip(Y_out, Z_out))
            inner_points = list(zip(Y_in, Z_in))

        elif self.section_label == "Valve section" : #
    
            N = 32 # temporary number of divisions for pipe sections

            d_out = self.outer_diameter_to_plot
            d_in = self.inner_diameter_to_plot
            # d_in = d_out - 2*self.thickness

            if d_in < 0:
                d_in = 0.004
                self.inner_diameter_to_plot = d_in

            d_theta = 2*np.pi/N
            theta = -np.arange(0, 2*np.pi, d_theta)
            sine = np.sin(theta)
            cossine = np.cos(theta)
            
            Y_out = (d_out/2)*cossine + self.offset_y
            Z_out = (d_out/2)*sine + self.offset_z
            Y_in = (d_in/2)*cossine + self.offset_y
            Z_in = (d_in/2)*sine + self.offset_z

            if self.insulation_thickness != float(0):
                Y_out = ((d_out + 2*self.insulation_thickness)/2)*cossine + self.offset_y
                Z_out = ((d_out + 2*self.insulation_thickness)/2)*sine + self.offset_z

            outer_points = list(zip(Y_out, Z_out))
            inner_points = list(zip(Y_in, Z_in))

        else:

            # A very small triangle to prevent bugs
            Y_out = [0, 1e-10, 0]
            Z_out = [0, 0, 1e-10]
            outer_points = list(zip(Y_out, Z_out))

        # TODO: section_type == 6: creates an equivalent beam section
        # return outer_points, inner_points

        if inner_points == []:
            Y_in, Z_in = 0, 0
            max_min = str([max(Y_out), max(Z_out), 0, 0, min(Y_out), min(Z_out), 0, 0, self.section_label, length])
        else:
            max_min = str([max(Y_out), max(Z_out), max(Y_in), max(Z_in), min(Y_out), min(Z_out), min(Y_in), min(Z_in), self.section_label, length])        
        
        return outer_points, inner_points, max_min

def get_circular_section_points(parameters, section_label):

    N = 32 # temporary number of divisions for circular sections
    
    if section_label == "Expansion joint section":

        d_out, d_in, offset_y, offset_z, insulation_thickness, key = parameters

        if key == "major":
            d_out *= 1.25 
        elif key == "minor":
            d_out *= 1.1            
        else:
            d_out *= 1.4
            
    else:

        d_out, d_in, offset_y, offset_z, insulation_thickness = parameters
    
    r_out = d_out/2
    r_in = d_in/2
    
    d_theta = 2*np.pi/N
    theta = -np.arange(0, 2*np.pi, d_theta)
    sine = np.sin(theta)
    cossine = np.cos(theta)
    
    Y_out = r_out*cossine + offset_y
    Z_out = r_out*sine + offset_z
    Y_in = r_in*cossine + offset_y
    Z_in = r_in*sine + offset_z

    if insulation_thickness != float(0):
        Y_out = (r_out + insulation_thickness)*cossine + offset_y
        Z_out = (r_out + insulation_thickness)*sine + offset_z

    outer_points = list(zip(Y_out, Z_out))
    inner_points = list(zip(Y_in, Z_in))

    max_min = str([max(Y_out), max(Z_out), max(Y_in), max(Z_in), min(Y_out), min(Z_out), min(Y_in), min(Z_in), section_label])
    
    return outer_points, inner_points, max_min

def get_points_to_plot_section(section_label, section_parameters):   
    
    if section_label != "Pipe section":

        section_properties = get_beam_section_properties(section_label, section_parameters)
        Yc = section_properties["Yc"]
        Zc = section_properties["Zc"]

    else:

        N = 60
        d_out = section_parameters["outer_diameter"]
        thickness = section_parameters["thickness"]
        offset_y = section_parameters["offset_y"]
        offset_z = section_parameters["offset_z"]
        insulation_thickness = section_parameters["insulation_thickness"]

        Yc = 0
        Zc = 0    

        Yc_offset = Yc + offset_y
        Zc_offset = Zc + offset_z

        d_theta = np.pi/N
        theta = np.arange(-np.pi/2, (np.pi/2)+d_theta, d_theta)
        d_in = d_out - 2*thickness

        Yp_out = (d_out/2)*np.cos(theta)
        Zp_out = (d_out/2)*np.sin(theta)
        Yp_in = (d_in/2)*np.cos(-theta)
        Zp_in = (d_in/2)*np.sin(-theta)

        Yp_list = [list(Yp_out), list(Yp_in),[0]]
        Zp_list = [list(Zp_out), list(Zp_in), [-(d_out/2)]]

        Yp_right = [value for _list in Yp_list for value in _list]
        Zp_right = [value for _list in Zp_list for value in _list]

        Yp_left = -np.flip(Yp_right)
        Zp_left =  np.flip(Zp_right)
        
        Yp = np.array([Yp_right, Yp_left]).flatten() + offset_y
        Zp = np.array([Zp_right, Zp_left]).flatten() + offset_z
        
        if insulation_thickness != float(0):

            Yp_out_ins = ((d_out + 2*insulation_thickness)/2)*np.cos(theta)
            Zp_out_ins = ((d_out + 2*insulation_thickness)/2)*np.sin(theta)
            Yp_in_ins = (d_out/2)*np.cos(-theta)
            Zp_in_ins = (d_out/2)*np.sin(-theta)

            Yp_list_ins = [list(Yp_out_ins), list(Yp_in_ins), [0]]
            Zp_list_ins = [list(Zp_out_ins), list(Zp_in_ins), [-(d_out/2)]]

            Yp_right_ins = [value for _list in Yp_list_ins for value in _list]
            Zp_right_ins = [value for _list in Zp_list_ins for value in _list]

            Yp_left_ins = -np.flip(Yp_right_ins)
            Zp_left_ins =  np.flip(Zp_right_ins)

            Yp_ins = np.array([Yp_right_ins, Yp_left_ins]).flatten() + offset_y
            Zp_ins = np.array([Zp_right_ins, Zp_left_ins]).flatten() + offset_z

            return Yp, Zp, Yp_ins, Zp_ins, Yc_offset, Zc_offset
        return Yp, Zp, None, None, Yc_offset, Zc_offset
            
    if section_label == "Rectangular section":

        b, h, b_in, h_in, offset_y, offset_z = section_parameters
            
        Yp_right = [0, (b/2), (b/2), 0, 0, (b_in/2), (b_in/2), 0, 0]
        Zp_right = [-(h/2), -(h/2), (h/2), (h/2), (h_in/2), (h_in/2), -(h_in/2), -(h_in/2), -(h/2)]

        Yp_left = -np.flip(Yp_right)
        Zp_left =  np.flip(Zp_right)

        Yp = np.array([Yp_right, Yp_left]).flatten() + offset_y
        Zp = np.array([Zp_right, Zp_left]).flatten() + offset_z

    elif section_label == "Circular section":

        N = 60
        d_out, thickness, offset_y, offset_z = section_parameters
        if thickness == 0:
            d_in = 0
        else:
            d_in = d_out - 2*thickness
        
        d_theta = np.pi/N
        theta = np.arange(-np.pi/2, (np.pi/2)+d_theta, d_theta)

        Yp_out = (d_out/2)*np.cos(theta)
        Zp_out = (d_out/2)*np.sin(theta)
        Yp_in = (d_in/2)*np.cos(-theta)
        Zp_in = (d_in/2)*np.sin(-theta)

        Yp_list = [list(Yp_out), list(Yp_in), [0]]
        Zp_list = [list(Zp_out), list(Zp_in), [-(d_out/2)]]

        Yp_right = [value for _list in Yp_list for value in _list]
        Zp_right = [value for _list in Zp_list for value in _list]

        Yp_left = -np.flip(Yp_right)
        Zp_left =  np.flip(Zp_right)

        Yp = np.array([Yp_right, Yp_left]).flatten() + offset_y
        Zp = np.array([Zp_right, Zp_left]).flatten() + offset_z

    elif section_label == "C-section":

        h, w1, t1, w2, t2, tw, offset_y, offset_z = section_parameters
        hw = h - t1 - t2

        Yp = np.array([0, w2, w2, tw, tw, w1, w1, 0, 0]) + offset_y 
        Zp = np.array([-(h/2), -(h/2), -(hw/2), -(hw/2), (h/2)-t1, (h/2)-t1, (h/2), (h/2), -(h/2)]) + offset_z

    elif section_label == "I-section":

        h, w1, t1, w2, t2, tw, offset_y, offset_z = section_parameters
        hw = h - t1 - t2

        Yp_right = [0, w2/2, w2/2, tw/2, tw/2, w1/2, w1/2, 0]
        Zp_right = [-(h/2), -(h/2), -((h/2)-t2), -((h/2)-t2), (h/2)-t1, (h/2)-t1, (h/2), (h/2)]

        Yp_left = -np.flip(Yp_right)
        Zp_left =  np.flip(Zp_right)

        Yp = np.array([Yp_right, Yp_left]).flatten() + offset_y
        Zp = np.array([Zp_right, Zp_left]).flatten() + offset_z

    elif section_label == "T-section":

        h, w1, tw, t1, offset_y, offset_z = section_parameters
        hw = h - t1

        Yp_right = [0, tw/2, tw/2, w1/2, w1/2, 0]
        Zp_right = [-(hw/2), -(hw/2), (hw/2), (hw/2), (hw/2)+t1, (hw/2)+t1]

        Yp_left = -np.flip(Yp_right)
        Zp_left =  np.flip(Zp_right)

        Yp = np.array([Yp_right, Yp_left]).flatten() + offset_y
        Zp = np.array([Zp_right, Zp_left]).flatten() + offset_z

    elif section_label == "Generic section":

        message = "The GENERIC BEAM SECTION cannot be ploted."
        title = "Error while graphing cross-section"
        info_text = [title, message]

        #TODO: breaks execution of code
        # PrintMessageInput(info_text)

        return 0, 0, 0, 0
    
    Yc = section_properties['Yc']
    Zc = section_properties['Zc']

    Yc_offset = Yc + offset_y
    Zc_offset = Zc + offset_z    

    return Yp, Zp, Yc_offset, Zc_offset

def get_beam_section_properties(section_label, data):

    if section_label == "Generic section":

        [area, Iyy, Izz, Iyz, shear_factor, Yc, Zc] = data

        section_properties = {  "area" : area, 
                                "Iyy" : Iyy, 
                                "Izz" : Izz, 
                                "Iyz" : Iyz, 
                                "Yc" : Yc, 
                                "Zc" : Zc,   
                                "shear_factor": shear_factor    }
        
        return section_properties

    if section_label == "Rectangular section":

        [base, height, base_in, height_in, offset_y, offset_z] = data
        
        area = base*height - base_in*height_in
        Iyy = ((height**3)*base/12) - ((height_in**3)*base_in/12)
        Izz = ((base**3)*height/12) - ((base_in**3)*height_in/12)
        Iyz = 0.
        Yc, Zc = 0, 0
    
    elif section_label == "Circular section":
        
        [outer_diameter_beam, thickness, offset_y, offset_z] = data
        
        if thickness == 0:
            inner_diameter_beam = 0
        else:
            inner_diameter_beam = outer_diameter_beam - 2*thickness

        area = np.pi*((outer_diameter_beam**2)-(inner_diameter_beam**2))/4
        Iyy = np.pi*((outer_diameter_beam**4)-(inner_diameter_beam**4))/64
        Izz = np.pi*((outer_diameter_beam**4)-(inner_diameter_beam**4))/64
        Iyz = 0
        Yc, Zc = 0, 0 

    elif section_label == "C-section":

        [h, w1, t1, w2, t2, tw, offset_y, offset_z] = data
        hw = h - t1 - t2
        
        A_i = np.array([w1*t1, tw*hw, w2*t2])
        A_t = np.sum(A_i)

        y_ci = np.array([w1/2, tw/2, w2/2])
        z_ci = np.array([((t1+hw)/2), 0, -((hw+t2)/2)])
        
        I_yi = np.array([(w1*t1**3)/12, (tw*hw**3)/12, (w2*t2**3)/12])
        I_zi = np.array([(t1*w1**3)/12, (hw*tw**3)/12, (t2*w2**3)/12])
        I_yzi = np.array([0, 0, 0])

    elif section_label == "I-section":

        [h, w1, t1, w2, t2, tw, offset_y, offset_z] = data
        hw = h - t1 - t2
        
        A_i = np.array([w1*t1, tw*hw, w2*t2])
        A_t = np.sum(A_i)  

        y_ci = np.array([0, 0, 0])
        z_ci = np.array([((t1+hw)/2), 0, -((hw+t2)/2)])

        I_yi = np.array([(w1*t1**3)/12, (tw*hw**3)/12, (w2*t2**3)/12])
        I_zi = np.array([(t1*w1**3)/12, (hw*tw**3)/12, (t2*w2**3)/12])
        I_yzi = np.array([0, 0, 0])

    elif section_label == "T-section":

        [h, w1, t1, tw, offset_y, offset_z] = data

        hw = h - t1

        A_i = np.array([w1*t1, tw*hw])
        A_t = np.sum(A_i)

        y_ci = np.array([0, 0])
        z_ci = np.array([((t1+hw)/2), 0])

        I_yi = np.array([(w1*t1**3)/12, (tw*hw**3)/12])
        I_zi = np.array([(t1*w1**3)/12, (hw*tw**3)/12])
        I_yzi = np.array([0, 0])  

    if section_label in ["C-section", "I-section", "T-section"]:
        area = A_t
        Yc = (y_ci@A_i)/A_t
        Zc = (z_ci@A_i)/A_t
        Iyy = np.sum(I_yi + ((z_ci-Zc)**2)*A_i)
        Izz = np.sum(I_zi + ((y_ci-Yc)**2)*A_i)
        Iyz = np.sum(I_yzi + ((y_ci-Yc)*(z_ci-Zc))*A_i)
    
    section_properties = [area, Iyy, Izz, Iyz, Yc, Zc]

    section_properties = {  "area" : area, 
                            "Iyy" : Iyy, 
                            "Izz" : Izz, 
                            "Iyz" : Iyz, 
                            "Yc" : Yc, 
                            "Zc" : Zc   }
    
    return section_properties
