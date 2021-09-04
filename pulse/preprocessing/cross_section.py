from time import time

import numpy as np
from math import pi, sqrt, cos, sin, atan, isnan, isinf
from numpy.linalg import inv, pinv, norm
from scipy.sparse import csc_matrix, coo_matrix
from scipy.sparse.linalg import spilu, svds, splu, spsolve
from scipy.linalg import svd

rows, cols = 4, 2
Nint_points = 4

def gauss_quadrature2D():
    """
    This method returns the Gauss quadrature data for 2D integration and two integration points.  

    Returns
    -------
    points : array
        Integration points in the normalized domain [-1,1]x[-1,1].

    weigths : array
        Weigths of the respective integration points in the sum approximation.

    See also
    --------
    get_all_shape_functions : Shape function and its derivative for all the integration points.
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

def shape_function(ksi,eta):
    """ This function returns the two dimensional quadratic shape function and its derivative (9-node quadrilateral element) for one point in the dimensionless coordinate system (ksi,eta).

    Parameters
    ----------
    ksi : float in [-1,1]
        Dimensionless x coordinate.

    eta : float in [-1,1]
        Dimensionless y coordinate.

    Returns
    -------
    phi : array
        One dimensional linear shape function.

    dphi : array
        Shape function derivative.

    See also
    --------
    get_all_shape_functions : Shape function and its derivative for all the integration points.
    """
    # Shape functions
    phi = np.zeros(9, dtype='float64') 
    phi[0] = (ksi**2 - ksi) * (eta**2 - eta) / 4
    phi[1] = (ksi**2 + ksi) * (eta**2 - eta) / 4
    phi[2] = (ksi**2 + ksi) * (eta**2 + eta) / 4
    phi[3] = (ksi**2 - ksi) * (eta**2 + eta) / 4
    phi[4] = (1 - ksi**2) * (eta**2 - eta)  / 2
    phi[5] = (ksi**2 + ksi) * (1 - eta**2)  / 2
    phi[6] = (1 - ksi**2.) * (eta**2 + eta)  / 2
    phi[7] = (ksi**2 - ksi) * (1 - eta**2)  / 2
    phi[8] = (1 - ksi**2) * (1 - eta**2)

    # Derivatives
    dphi=np.zeros((2, 9), dtype='float64')
    # ksi Derivative
    dphi[0,0] = (2*ksi - 1) * (eta**2 - eta) / 4
    dphi[0,1] = (2*ksi + 1) * (eta**2 - eta) / 4 
    dphi[0,2] = (2*ksi + 1) * (eta**2 + eta) / 4
    dphi[0,3] = (2*ksi - 1) * (eta**2 + eta) / 4
    dphi[0,4] = -ksi * (eta**2 - eta)
    dphi[0,5] = (2*ksi + 1) * (1 - eta**2) / 2
    dphi[0,6] = -ksi * (eta**2 + eta)
    dphi[0,7] = (2*ksi - 1) * (1 - eta**2) / 2
    dphi[0,8] = -2*ksi * (1 - eta**2)
    # eta Derivative
    dphi[1,0] = (ksi**2 - ksi) * (2*eta - 1) / 4
    dphi[1,1] = (ksi**2 + ksi) * (2*eta - 1) / 4
    dphi[1,2] = (ksi**2 + ksi) * (2*eta + 1) / 4
    dphi[1,3] = (ksi**2 - ksi) * (2*eta + 1) / 4
    dphi[1,4] = (1 - ksi**2) * (2*eta - 1) / 2
    dphi[1,5] = (ksi**2 + ksi) * (-2*eta) / 2
    dphi[1,6] = (1 - ksi**2) * (2*eta + 1) / 2
    dphi[1,7] = (ksi**2 - ksi) * (-2*eta) / 2
    dphi[1,8] = (1 - ksi**2) * (-2*eta)
    return phi, dphi

def get_all_shape_functions():
    """ This function returns the two dimensional quadratic shape function and its derivative (9-node quadrilateral element) for all Gauss quadrature 2D integration points in the dimensionless coordinate system (ksi,eta).

    Returns
    -------
    phi : array
        One dimensional linear shape function.

    dphi : array
        Shape function derivative.

    See also
    --------
    shape_function : Shape function and its derivative for one point.

    gauss_quadrature2D : Gauss quadrature data for 2D integration and two integration points.
    """
    points, _ = gauss_quadrature2D()
    mat_phi = np.zeros((rows, 9), dtype='float64')
    mat_dphi = np.zeros((rows, 2, 9), dtype='float64')
    for i, (ksi, eta) in enumerate(points): 
        mat_phi[i,:], mat_dphi[i,:,:] = shape_function(ksi,eta)
    return  mat_phi, mat_dphi

class CrossSection:
    """This class creates a tube Cross Section object from input data.

    Parameters
    ----------
    outer_diameter : float
        Tube outer diameter.

    thickness : float
        Tube wall thickness.

    offset_y : float
        y coordinate of the tube eccentricity offset.

    offset_z : float
        z coordinate of the tube eccentricity offset.

    poisson_ratio : float, optional
        Poisson's ration of the material attributed to the tube.
        Default is 0.

    element_type : ['pipe_1','pipe_2','beam_1'], optional
        Element type of the structural elements attributed to the tube.
        Default is 'pipe_1'.

    division_number : [8, 16, 32, 64, 128], optional
        Cross section division number. This number is directly associated with the number of elements used in the process of approximating the cross section shear properties.
        Default is 64.

    insulation_thickness : float, optional
        Tube insolation thickness.
        Default is 0.

    insulation_density : float, optional
        Tube insolation density.
        Default is 0.

    additional_section_info : , optional
        Cross section additional infos.
        Default is None.

    area : float, optional
        Cross section area. Only attributed if the cross section is not tubular.
        Default is 0.

    Iyy : float, optional
        Cross section second moment of area with respect to the y direction. Only attributed if the cross section is not tubular.
        Default is 0.

    Izz : float, optional
        Cross section second moment of area with respect to the z direction. Only attributed if the cross section is not tubular.
        Default is 0.

    Iyz : float, optional
        Cross section second moment of area with respect to the yz plane. Only attributed if the cross section is not tubular.
        Default is 0.

    shear_coefficient : float, optional
        Cross section shear coefficient. Only attributed if the cross section is not tubular.
        Default is 1.
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
        self.insulation_thickness = 0
        self.insulation_density = 0
        self.offset_virtual = None

        # Beam section properties
        self.area = kwargs.get('area', 0)
        self.first_moment_area_y = 0
        self.first_moment_area_z = 0
        self.second_moment_area_y = kwargs.get('Iyy', 0)
        self.second_moment_area_z = kwargs.get('Izz', 0)
        self.second_moment_area_yz = kwargs.get('Iyz', 0)
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
        self.expansion_joint_info = kwargs.get('expansion_joint_info', None)
        self.section_label = kwargs.get('section_label', None)
        self.section_parameters = kwargs.get('section_parameters', None)
        self.expansion_joint_plot_key = None

        # Unwrap cluster data for pipe sections 
        if self.pipe_section_info is not None:

            self.section_label = self.pipe_section_info["section_type_label"]
            self.section_parameters = self.pipe_section_info["section_parameters"]

            self.outer_diameter = self.section_parameters["outer_diameter"]
            self.thickness =  self.section_parameters["thickness"]
            self.offset_y = self.section_parameters["offset_y"]
            self.offset_z = self.section_parameters["offset_z"]
            self.insulation_thickness = self.section_parameters["insulation_thickness"]
            self.insulation_density = self.section_parameters["insulation_density"]
            self.offset = [self.offset_y, self.offset_z]
            self.section_info = self.pipe_section_info
        
        # Unwrap cluster data for beam sections 
        if self.beam_section_info is not None:
           
            self.section_label = self.beam_section_info["section_type_label"]
            self.section_parameters = self.beam_section_info["section_parameters"]
            self.section_properties = self.beam_section_info["section_properties"]

            self.area = self.section_properties['area']
            self.second_moment_area_y = self.section_properties['Iyy']
            self.second_moment_area_z = self.section_properties['Izz']
            self.second_moment_area_yz = self.section_properties['Iyz']
            self.offset_y = self.section_properties['Yc']
            self.offset_z = self.section_properties['Zc']
            self.offset = [self.offset_y, self.offset_z]
            
            if self.section_label == "Generic section":
                self.shear_coefficient = self.section_properties['shear factor']
            
            self.section_info = self.beam_section_info
        
        if self.expansion_joint_info is not None:
            self.section_label = self.expansion_joint_info[0]
            self.expansion_joint_plot_key = self.expansion_joint_info[1]
            self.outer_diameter = self.expansion_joint_info[2]


    @property
    def outer_radius(self):
        return self.outer_diameter/2

    @property
    def inner_diameter(self):
        return self.outer_diameter - 2*self.thickness

    @property
    def inner_radius(self):
        return self.inner_diameter/2

    @property
    def area_fluid(self):
        """
        This method returns the tube inner cross section area, which corresponds to the acoustic area.

        Returns
        -------
        float
            inner area.
        """
        return (self.inner_diameter**2) * pi / 4

    @property
    def area_insulation(self):
        """
        This method returns the insulation cross section area.

        Returns
        -------
        float
            insulation cross section area.
        """
        return (((self.outer_diameter+2*self.insulation_thickness)**2)-(self.outer_diameter**2)) * pi / 4

    def getExternalDiameter(self):
        """
        This method returns the tube cross section outer diameter.

        Returns
        -------
        float
            outer diameter.
        """
        return self.outer_diameter
    
    def getExternalRadius(self):
        """
        This method returns the tube cross section outer radius.

        Returns
        -------
        float
            outer radius.
        """
        return self.outer_radius

    def getThickness(self):
        """
        This method returns the tube cross section thickness.

        Returns
        -------
        float
            thickness.
        """
        return self.thickness

    def getInnerDiameter(self):
        """
        This method returns the tube cross section inner diameter.

        Returns
        -------
        float
            inner diameter.
        """
        return self.inner_diameter

    def mesh_connectivity(self):
        """
        This method returns the tube cross mesh connectivity formed by 9-node quadrilateral elements.

        Returns
        -------
        array
            Tube cross mesh connectivity.

        See also
        --------
        mesh_coordinate : Tube cross mesh nodal coordinates.
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
        This method returns the tube cross mesh nodal coordinates formed by 9-node quadrilateral elements.

        Returns
        -------
        array
            Tube cross mesh nodal coordinates.

        See also
        --------
        mesh_connectivity : Tube cross mesh connectivity.
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
    
    def preprocessing(self, el_type = None):
        """
        This method returns the tube cross mesh nodal coordinates formed by 9-node quadrilateral elements.

        Parameters
        -------
        el_type : ['pipe_1','pipe_2','beam_1'], optional
            Element type of the structural elements attributed to the tube.
            Default is None.

        Returns
        -------
        jac : array
            Jacobian matrix of each integration point. It's a 3D matrix such that jac[p,:] is the Jacobian matrix of the p-th integration point (in-line 2x2 matrix).

        inv_jac : array
            Inverse of the Jacobian matrix of each element. It's a 3D matrix such that inv_jac[p,:] is the inverse of the Jacobian matrix of the p-th integration point (in-line 2x2 matrix).

        dA : array
            Area differential of each integration point.

        y : array
            y-coordinate in the global coordinate system of each integration point.

        z : array
            z-coordinate in the global coordinate system of each integration point.
        """
        
        N = self.division_number*Nint_points
        _, weight = gauss_quadrature2D()
        self.mesh_connectivity()
        self.mat_phi, self.mat_dphi = get_all_shape_functions()
        phi = self.mat_phi
        dphi = self.mat_dphi

        if el_type == 'pipe_1':
            # for the pipe_1 element, offset and its dependence need to be updated as below
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
            for k in range(Nint_points):   # integration points
                jac[ind,:,:] = dphi[k,:,:]@coordinate[indexes,:]
                y[ind], z[ind] = phi[k,:]@coordinate[indexes,:]
                inv_jac[ind,:,:] = inv(jac[ind,:,:])
                ind += 1
        aux = jac.reshape(N,4)
        detjac = (aux[:,0]*aux[:,3])-(aux[:,1]*aux[:,2])
        return jac, inv_jac, detjac*weight, y, z
            
    def area_properties(self, el_type):
        """
        This method updates the tube cross area properties: area, first moment of area relative to y, first moment of area relative to z, second moment of area relative to y, second moment of area relative to z, second moment of area relative to yz, second moment of area relative to yz, second polar moment of area, and (y,z) centroid coordinate.

        Parameters
        -------
        el_type : ['pipe_1','pipe_2','beam_1']
            Element type of the structural elements attributed to the tube.
            Default is None.
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
        This method updates the assembly process rows and columns indexing.
        """
        rows, cols = self.division_number, 9
        cols_dofs = self.connectivity.reshape(-1,1)
        cols_dofs = cols_dofs.reshape(rows, cols)
        J = np.tile(cols_dofs, cols)
        I = cols_dofs.reshape(-1,1)@np.ones((1,cols), dtype=int) 
        self.rows_ind = I.reshape(-1)
        self.cols_ind = J.reshape(-1)
                            
    def shear_properties(self, poisson_ratio = 0, el_type = 'pipe_1'):
        """
        This method updates the tube cross shear properties: shear coefficients and (y,z) shear centroid coordinate.

        Parameters
        -------
        poisson_ratio : float, optional
            Poisson's ration of the material attributed to the tube.
            Default is 0.

        el_type : ['pipe_1','pipe_2','beam_1'], optional
            Element type of the structural elements attributed to the tube.
            Default is None.
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
        N = self.division_number*Nint_points

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
            for _ in range(Nint_points):                                               
                ## Previous version - Internal Loop
                # Fy[indexes] += ( poisson_ratio/2 * dphig_T[i,:,:] @ d[i,:] + 2*(1 + poisson_ratio)*phi[k,:]*(Iy*y[i] - Iyz*z[i]) ) * dA[i]
                # Fz[indexes] += ( poisson_ratio/2 * dphig_T[i,:,:] @ h[i,:] + 2*(1 + poisson_ratio)*phi[k,:]*(Iz*z[i] - Iyz*y[i]) ) * dA[i]
                # FT[indexes] += (dphig_T[i,:,:] @ vec[i,:]) * dA[i]
                Ke += mat_ke[i,:,:]
                Fy[indexes] += ( poisson_ratio/2 * dphig_T[i,:,:] @ d[i,:] + add_y[i])*dA[i]
                Fz[indexes] += ( poisson_ratio/2 * dphig_T[i,:,:] @ h[i,:] + add_z[i])*dA[i]
                FT[indexes] += ( dphig_T[i,:,:] @ vec_dA[i] )
                i += 1
            data_ke[el,:,:] = Ke
        # t0 = time()
        # print(True in [True if isnan(data) or isinf(data) else False for data in data_ke.reshape(-1)])
        K_lg = coo_matrix((data_ke.reshape(-1), (self.rows_ind, self.cols_ind)), shape=(NGL+1, NGL+1), dtype='float64')
                                            
        # Pseudo inverse used to remedy numerical instability
        inv_K_lg = pinv(K_lg.toarray())#, hermitian=True)

        u2 = inv_K_lg @ np.append(Fy, 0)
        u3 = inv_K_lg @ np.append(Fz, 0)
        psi_y = u2[:-1]
        psi_z = u3[:-1]
        # dt = time()-t0
        # print(dt)
        d_poisson = d*poisson_ratio/2
        h_poisson = h*poisson_ratio/2
        dA = dA.reshape(-1,1)
        mat_dptemp = np.zeros((N, 2), dtype='float64')
        mat_hptemp = np.zeros((N, 2), dtype='float64')

        i=0
        alpha_y = alpha_z = alpha_yz = 0
        for el in range( self.division_number ): # Integration over each cross 
            indexes = self.connectivity[el,:]
            Np = Nint_points*el
            mat_dptemp[0+Np:4+Np,:] = (dphig[0+Np:4+Np,:,:] @ psi_y[indexes]) - d_poisson[0+Np:4+Np,:]
            mat_hptemp[0+Np:4+Np,:] = (dphig[0+Np:4+Np,:,:] @ psi_z[indexes]) - h_poisson[0+Np:4+Np,:]
            
            ## Previous version - Internal Loop
            # for k in range(Nint_points):
                
            #     dptemp = (dphig[i,:,:] @ psi_y[indexes]) - d_poisson[i,:]
            #     hptemp = (dphig[i,:,:] @ psi_z[indexes]) - h_poisson[i,:]

            #     alpha_y += dptemp @ dptemp * dA[i]
            #     alpha_z += hptemp @ hptemp * dA[i]
            #     alpha_yz += dptemp @ hptemp * dA[i]
            #     i+=1
        
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
        This method updates the tube cross section rotation due to the shear effects and eccentricity offset.

        Parameters
        -------
        el_type : ['pipe_1','pipe_2','beam_1'], optional
            Element type of the structural elements attributed to the tube.
            Default is None.
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
        This method updates all the tube cross section properties.
        """
        # self.area_properties(None)
        if self.element_type == 'pipe_1':
            self.shear_properties(poisson_ratio = 0, el_type = None)
            self.offset_rotation(el_type = 'pipe_1')
            self.shear_properties(poisson_ratio = 0, el_type = self.element_type)
        else:
            self.shear_properties(poisson_ratio=self.poisson_ratio, el_type=self.element_type)

    def _polar_moment_area(self):
        """Cross section second polar moment of area [m**4]."""
        return self.second_moment_area_y + self.second_moment_area_z

    def get_cross_section_points(self):

        inner_points = []

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

        elif self.section_label == "Rectangular section": # Rectangular section

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
            
        elif self.section_label == "Circular section": # Circular section
            
            N = 24# element.cross_section.division_number
            d_out, thickness, offset_y, offset_z = self.section_parameters
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
            Y_out = [0, w2, w2, tw, tw, w1, w1, 0]
            Z_out = [-(h/2), -(h/2), -((h/2)-t2), -((h/2)-t2), ((h/2)-t1), ((h/2)-t1), (h/2), (h/2)]

            Ys = np.array(Y_out) + offset_y
            Zs = np.array(Z_out) + offset_z
            outer_points = list(zip(Ys, Zs))

        elif self.section_label == 'I-section': # Beam: I-section

            h, w1, t1, w2, t2, tw, offset_y, offset_z = self.section_parameters
            Y_out = [(w1/2), (w1/2), (tw/2), (tw/2), (w2/2), (w2/2), -(w2/2), -(w2/2), -(tw/2), -(tw/2), -(w1/2), -(w1/2)]
            Z_out = [(h/2), (h/2)-t1, (h/2)-t1, -(h/2)+t2, -(h/2)+t2, -(h/2), -(h/2), -(h/2)+t2, -(h/2)+t2, (h/2)-t1, (h/2)-t1, (h/2)]
            
            Ys = np.array(Y_out) + offset_y
            Zs = np.array(Z_out) + offset_z
            outer_points = list(zip(Ys, Zs))
    
        elif self.section_label == 'T-section': # Beam: T-section

            h, w1, t1, tw, offset_y, offset_z = self.section_parameters
            Y_out = [(w1/2), (w1/2), (tw/2), (tw/2), -(tw/2), -(tw/2), -(w1/2), -(w1/2)]
            Z_out = [(h/2), (h/2)-t1, (h/2)-t1, -(h/2), -(h/2), (h/2)-t1, (h/2)-t1, (h/2)]

            Ys = np.array(Y_out) + offset_y
            Zs = np.array(Z_out) + offset_z
            outer_points = list(zip(Ys, Zs))
        
        elif self.section_label == "Expansion joint section" :#8:
    
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

        else:

            # A very small triangle to prevent bugs
            Y_out = [0, 1e-10, 0]
            Z_out = [0, 0, 1e-10]
            outer_points = list(zip(Y_out, Z_out))

        # TODO: section_type == 6: creates an equivalent beam section
        return outer_points, inner_points

    def get_beam_shear_center(self):
        ''' This method returns the shear center coordinates relative to the centroid of the cross-section area under
            hypothesis so that the thickness of beams t_i -> 0. If the thickness is not small sufficiently greater. 
            deviations are expected.
        '''
        if self.section_label == "Rectangular section":
            _, _, _, _, offset_y, offset_z = self.section_parameters
            return 0, 0

        elif self.section_label == "Circular section":
            _, _, offset_y, offset_z = self.section_parameters
            return 0, 0
        
        elif self.section_label == "C-section":
            h, w1, t1, w2, t2, tw, offset_y, offset_z = self.section_parameters

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
            h, w1, t1, w2, t2, tw, offset_y, offset_z = self.section_parameters

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
            h, w1, t1, tw, offset_y, offset_z = self.section_parameters

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

# if __name__ == "__main__":

#     outer_diameter = 0.05
#     thickness = 0.002
#     offset = [0, 0]
#     cross = CrossSection(outer_diameter, thickness, offset[0], offset[1], 0.3, element_type = 'pipe', division_number = 64)
#     cross.update_properties()

    # %timeit cross.update_properties(poisson_ratio = 0.3, element_type = 'pipe_1')


#####################################################################################################################################
##                                                NEW CROSS-SECTION FIRST VERSION                                                  ##
#####################################################################################################################################

# import numpy as np
# from math import pi, sqrt, cos, sin, atan
# from numpy.linalg import inv, pinv, norm
# from scipy.sparse import csc_matrix

# def gauss_quadrature2D():
#     c = 1/sqrt(3)
#     points=np.zeros([4,2])
#     points[0,0]=-c
#     points[1,0]=c
#     points[2,0]=c
#     points[3,0]=-c

#     points[0,1]=-c
#     points[1,1]=-c
#     points[2,1]=c
#     points[3,1]=c
#     weight = 1
#     return points, weight

# def shape_function(ksi,eta):
#     """
#     - Quadratic shape functions and its derivatives
#     for calculation of section properties.
#     - Q9 element.
#     """

#     # Shape functions
#     phi = np.zeros(9) 
#     phi[0] = (ksi**2 - ksi) * (eta**2 - eta) / 4
#     phi[1] = (ksi**2 + ksi) * (eta**2 - eta) / 4
#     phi[2] = (ksi**2 + ksi) * (eta**2 + eta) / 4
#     phi[3] = (ksi**2 - ksi) * (eta**2 + eta) / 4
#     phi[4] = (1 - ksi**2) * (eta**2 - eta)  / 2
#     phi[5] = (ksi**2 + ksi) * (1 - eta**2)  / 2
#     phi[6] = (1 - ksi**2.) * (eta**2 + eta)  / 2
#     phi[7] = (ksi**2 - ksi) * (1 - eta**2)  / 2
#     phi[8] = (1 - ksi**2) * (1 - eta**2)

#     # Derivatives
#     dphi=np.zeros([2, 9])
#     # ksi Derivative
#     dphi[0,0] = (2*ksi - 1) * (eta**2 - eta) / 4
#     dphi[0,1] = (2*ksi + 1) * (eta**2 - eta) / 4 
#     dphi[0,2] = (2*ksi + 1) * (eta**2 + eta) / 4
#     dphi[0,3] = (2*ksi - 1) * (eta**2 + eta) / 4
#     dphi[0,4] = -ksi * (eta**2 - eta)
#     dphi[0,5] = (2*ksi + 1) * (1 - eta**2) / 2
#     dphi[0,6] = -ksi * (eta**2 + eta)
#     dphi[0,7] = (2*ksi - 1) * (1 - eta**2) / 2
#     dphi[0,8] = -2*ksi * (1 - eta**2)
#     # eta Derivative
#     dphi[1,0] = (ksi**2 - ksi) * (2*eta - 1) / 4
#     dphi[1,1] = (ksi**2 + ksi) * (2*eta - 1) / 4
#     dphi[1,2] = (ksi**2 + ksi) * (2*eta + 1) / 4
#     dphi[1,3] = (ksi**2 - ksi) * (2*eta + 1) / 4
#     dphi[1,4] = (1 - ksi**2) * (2*eta - 1) / 2
#     dphi[1,5] = (ksi**2 + ksi) * (-2*eta) / 2
#     dphi[1,6] = (1 - ksi**2) * (2*eta + 1) / 2
#     dphi[1,7] = (ksi**2 - ksi) * (-2*eta) / 2
#     dphi[1,8] = (1 - ksi**2) * (-2*eta)
#     return phi, dphi

# class CrossSection:
#     def __init__(self, outer_diameter, thickness, offset_y = 0, offset_z = 0, division_number = 64):
#         self.outer_diameter = outer_diameter
#         self.thickness = thickness
#         self.offset = np.array([offset_y, offset_z])
#         self.offset_virtual = None
#         self.division_number = division_number

#         self.outer_radius = outer_diameter/2
#         self.inner_diameter = outer_diameter - 2*thickness

#         # Area properties
#         self.area = 0
#         self.first_moment_area_y = 0
#         self.first_moment_area_z = 0
#         self.second_moment_area_y = 0
#         self.second_moment_area_z = 0
#         self.second_moment_area_yz = 0
#         self.polar_moment_area = 0
#         self.y_centroid = 0
#         self.z_centroid = 0

#         # Shear properties
#         self.y_shear = 0
#         self.z_shear = 0
#         self.res_y = 0
#         self.res_z = 0
#         self.res_yz = 0

#         # Principal Bending Axis Rotation
#         self.principal_axis = None

#     @property
#     def area_fluid(self):
#         return (self.inner_diameter**2) * pi / 4

#     def getExternalDiameter(self):
#         return self.outer_diameter
    
#     def getExternalRadius(self):
#         return self.outer_radius

#     def getThickness(self):
#         return self.thickness

#     def getInnerDiameter(self):
#         return self.inner_diameter

#     def mesh_connectivity(self):
#         connectivity = np.zeros([self.division_number, 9], dtype = int)
#         aux = 0
#         for i in range(self.division_number - 1):
#             connectivity[i,:] = aux + np.array([8,2,0,6,5,1,3,7,4]) 
#             aux += 6
        
#         connectivity[i + 1,:] = [2,2+aux,aux,0,5+aux,1+aux,3+aux,1,4+aux]

#         return connectivity
    
#     def mesh_coordinate(self):
#         # coordinates of points on the face
#         angular_increment = 2 * pi / (2 * self.division_number)
#         theta = 0
#         r_o = self.outer_diameter / 2
#         r_i = self.inner_diameter / 2

#         if self.offset_virtual is None:
#             offset = self.offset
#         else:
#             offset = self.offset_virtual # used in element_type = 'pipe_1'

#         coordinate = np.zeros([6 * self.division_number, 2])
#         for i in range( 2 * self.division_number ):
#             coordinate[3*i + 0, 0] = r_o * cos(theta) - offset[0]
#             coordinate[3*i + 0, 1] = r_o * sin(theta) - offset[1]
#             coordinate[3*i + 1, 0] = (r_o + r_i)/2 * cos(theta) - offset[0]
#             coordinate[3*i + 1, 1] = (r_o + r_i)/2 * sin(theta) - offset[1]
#             coordinate[3*i + 2, 0] = r_i * cos(theta) - offset[0]
#             coordinate[3*i + 2, 1] = r_i * sin(theta) - offset[1]

#             theta += angular_increment

#         return coordinate
    
#     def area_properties(self):
#         coordinate = self.mesh_coordinate()
#         points, weight = gauss_quadrature2D()
#         connectivity = self.mesh_connectivity()
        
#         # Geometry properties
#         A = Iy = Iz = Iyz = Qy = Qz = 0
#         for el in range( self.division_number ): # Integration over each element
#             for ksi, eta in points: # integration points
#                 phi, dphi = shape_function(ksi,eta)
#                 jacobian = np.zeros((2,2))
#                 y = z = 0
#                 for i, index in enumerate(connectivity[el,:]):
#                     jacobian[0,:] += coordinate[index, :] * dphi[0,i]
#                     jacobian[1,:] += coordinate[index, :] * dphi[1,i]
#                     y += coordinate[index, 0] * phi[i]
#                     z += coordinate[index, 1] * phi[i]
#                 det_jacobian = jacobian[0,0]*jacobian[1,1] - jacobian[0,1]*jacobian[1,0]
#                 dA = det_jacobian * weight
#                 A += dA
#                 Iy += z**2 * dA
#                 Iz += y**2 * dA
#                 Iyz += y * z * dA
#                 Qy += z * dA
#                 Qz += y * dA

#         self.area = A
#         self.first_moment_area_y = Qy
#         self.first_moment_area_z = Qz
#         self.second_moment_area_y = Iy
#         self.second_moment_area_z = Iz
#         self.second_moment_area_yz = Iyz
#         self.polar_moment_area = Iy + Iz
#         self.y_centroid = Qz/A
#         self.z_centroid = Qy/A
    

#     def shear_properties(self, poisson_ratio = 0, element_type = 'pipe_1'):
#         coordinate = self.mesh_coordinate()
#         points, weight = gauss_quadrature2D()
#         connectivity = self.mesh_connectivity()
        

#         if element_type == 'pipe_1':
#             # for the pipe_1 element, offset and its dependence need to be updated as below
#             self.offset_virtual = self.offset + np.array([self.y_centroid, self.z_centroid]) 
#             coordinate = self.mesh_coordinate()
#             self.area_properties()

#         Iy = self.second_moment_area_y 
#         Iz = self.second_moment_area_z
#         Iyz = self.second_moment_area_yz

#         # Shear Coefficients
#         NGL = len(coordinate)
#         Fy = np.zeros(NGL)
#         Fz = np.zeros(NGL)
#         FT = np.zeros(NGL)

#         # Initializing  Lagrangian multiplier matrix construction
#         row = np.r_[ np.arange(NGL), np.repeat(NGL, NGL)]  # list holding row indices
#         col = np.r_[ np.repeat(NGL, NGL), np.arange(NGL)]  # list holding column indices
#         data = np.r_[np.repeat(1, NGL), np.repeat(1, NGL)] 

#         matrix_aux2 =   np.array([[Iy, -Iyz],[Iyz, Iy]])
#         matrix_aux3 = - np.array([[Iyz, -Iz],[Iz, Iyz]])

#         for el in range( self.division_number ): # Integration over each cross sections element
#             ke =  0
#             indexes = connectivity[el,:]
#             for ksi, eta in points:   # integration points
#                 phi, dphi = shape_function(ksi,eta)
#                 jacobian = np.zeros((2,2))
#                 y, z = 0, 0
#                 for i, index in enumerate(connectivity[el,:]):
#                     jacobian[0,:] += coordinate[index, [0, 1]] * dphi[0,i]
#                     jacobian[1,:] += coordinate[index, [0, 1]] * dphi[1,i]
#                     y += coordinate[index, 0] * phi[i]
#                     z += coordinate[index, 1] * phi[i]
#                 det_jacobian = jacobian[0,0]*jacobian[1,1] - jacobian[0,1]*jacobian[1,0]
#                 dA = det_jacobian * weight
#                 inv_jacobian = np.linalg.inv(jacobian)
#                 dphig = inv_jacobian @ dphi
#                 ke +=  dphig.T @ dphig * dA
#                 vector_aux = np.array([y**2 - z**2, 2*y * z])
#                 d = matrix_aux2 @ vector_aux
#                 h = matrix_aux3 @ vector_aux
#                 vec = np.array([z, -y])
#                 #
#                 Fy[indexes] += ( poisson_ratio/2 * dphig.T @ d + 2*(1 + poisson_ratio)*phi*(Iy*y - Iyz*z) ) * dA
#                 Fz[indexes] += ( poisson_ratio/2 * dphig.T @ h + 2*(1 + poisson_ratio)*phi*(Iz*z - Iyz*y) ) * dA
#                 FT[indexes] += (dphig.T @ vec) * dA
#             # Appending new elements to the Lagrangian Mult Matrix
#             row = np.r_[row, np.repeat(indexes, 9) ]
#             col = np.r_[col, np.tile(indexes, 9) ]
#             data = np.r_[data, ke.flatten() ]
#         #
#         K_lg = csc_matrix((data, (row, col)), shape=(NGL+1, NGL+1))
#         # Pseudo inverse used to remedy numerical instability
#         inv_K_lg = pinv(K_lg.toarray()) 

#         u2 = inv_K_lg @ np.append(Fy, 0)
#         u3 = inv_K_lg @ np.append(Fz, 0)
#         psi_y = u2[:-1]
#         psi_z = u3[:-1]
#         #
#         alpha_y = alpha_z = alpha_yz = 0
#         for el in range( self.division_number ): # Integration over each cross 
#             psi_ye = np.zeros(9)
#             psi_ze = np.zeros(9)
#             for ksi, eta in points:   # integration points
#                 phi, dphi = shape_function(ksi,eta)
#                 jacobian = np.zeros((2,2))
#                 y, z = 0, 0
#                 for i, index in enumerate(connectivity[el,:]):
#                     jacobian[0,:] += coordinate[index, [0, 1]] * dphi[0,i]
#                     jacobian[1,:] += coordinate[index, [0, 1]] * dphi[1,i]
#                     y += coordinate[index, 0] * phi[i]
#                     z += coordinate[index, 1] * phi[i]
#                     psi_ye[i] = psi_y[index]
#                     psi_ze[i] = psi_z[index]
#                 det_jacobian = jacobian[0,0]*jacobian[1,1] - jacobian[0,1]*jacobian[1,0]
#                 dA = det_jacobian * weight
#                 inv_jacobian = inv(jacobian)
#                 dphig = inv_jacobian @ dphi
#                 vector_aux = np.array([y**2 - z**2, 2*y * z])
#                 d = poisson_ratio/2 * matrix_aux2 @ vector_aux
#                 h = poisson_ratio/2 * matrix_aux3 @ vector_aux
#                 dptemp = (dphig @ psi_ye) - d
#                 hptemp = (dphig @ psi_ze) - h
#                 alpha_y += dptemp @ dptemp * dA
#                 alpha_z += hptemp @ hptemp * dA
#                 alpha_yz += dptemp @ hptemp * dA
        
#         A = self.area
#         ccg = 2 * (1 + poisson_ratio) * (Iy*Iz - (Iyz**2))
#         self.res_y = (A/(ccg**2))*(alpha_y)
#         self.res_z = (A/(ccg**2))*(alpha_z)
#         self.res_yz = (A/(ccg**2))*(alpha_yz)

#         # shear center
#         self.y_shear = -(psi_z.T @ FT)/ccg
#         self.z_shear = (psi_y.T @ FT)/ccg

#     def offset_rotation(self, element_type = 'pipe_1'):
#         if element_type is 'pipe2':
#             self.principal_axis = np.eye(12)
#         else:
#             y_c = self.y_centroid
#             z_c = self.z_centroid
#             y_s = self.y_shear
#             z_s = self.z_shear
#             if norm(self.offset) > 0:
#                 Iy = self.second_moment_area_y 
#                 Iz = self.second_moment_area_z
#                 Iyz = self.second_moment_area_yz
#                 angle = atan(2*Iyz/(Iz-Iy))/2
#                 # Rotational part of transformation matrix
#                 rotation = np.array([[ 1. ,      0.   ,    0.    ],
#                                     [ 0. ,cos(angle) ,sin(angle)],
#                                     [ 0. ,-sin(angle),cos(angle)]])
#                 # Translational part of transformation matrix
#                 translation = np.array([[ 0  , z_c,-y_c],
#                                         [-z_s,  0 , 0  ],
#                                         [y_s ,  0 , 0  ]])
#                 T = np.eye(12)
#                 T[0:3,3:6]   = translation
#                 T[6:9,9:12]  = translation
#                 #
#                 R = np.zeros([12, 12])
#                 R[0:3, 0:3]  = R[3:6, 3:6] = R[6:9, 6:9] = R[9:12, 9:12] = rotation
#                 self.principal_axis = R @ T
#             else:
#                 translation = np.array([[ 0  , z_c,-y_c],
#                                         [-z_s,  0 , 0  ],
#                                         [y_s ,  0 , 0  ]])
#                 T = np.eye(12)
#                 T[0:3,3:6]   = translation
#                 T[6:9,9:12]  = translation
#                 self.principal_axis = T
    
#     def update_properties(self, poisson_ratio = 0, element_type = 'pipe_1'):
#         self.area_properties()

#         if element_type == 'pipe_1':
#             self.shear_properties(poisson_ratio = 0, element_type = None)
#             self.offset_rotation(element_type = 'pipe_1')
#             self.shear_properties(poisson_ratio = 0, element_type = element_type)
#         else:
#             self.shear_properties(poisson_ratio = poisson_ratio, element_type = element_type)