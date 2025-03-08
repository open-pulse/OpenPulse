# fmt: off

from pulse.model.perforated_plate import Foks_function
from pulse.model.node import Node, distance

from numpy import sqrt, pi
import numpy as np
from scipy.special import jv, hankel1
from scipy.optimize import root, fsolve


DOF_PER_NODE = 1
NODES_PER_ELEMENT = 2
DOF_PER_ELEMENT = DOF_PER_NODE * NODES_PER_ELEMENT
ENTRIES_PER_ELEMENT = DOF_PER_ELEMENT ** 2

def f_function(x):
    return 1 - 2 * jv(1,x)/(x * jv(0,x))

def H1(x):
    return 2/np.pi - jv(0,x) + (16/np.pi - 5)*np.sin(x)/x + (12 - 36/np.pi)*(1 - np.cos(x))/x**2

def poly_function(x):
    """
    This function compute a auxiliary polynomial to define the unflanged radiation impedance.

    Parameters
    -------
    array
        Independent variable. 

    Returns
    -------
    array
        Polynomial output.
    """
    a = np.array([0.6110035017201978, 0.028476407937161143, -0.26371506544764184, 0.24363292796929378, -0.11627424586622058, 0.027516286514019005, -0.00254838451051438])
    b = np.arange(7)
    x = x.reshape(-1, 1) @ np.ones([1,7])
    return (x**b ) @ a

def j2_j0(z):
    """
    Auxiliary function to compute the ratio between the Bessel functions J2 and J0. When the 
    imaginary part of input z reaches 700, the following syntonic approximation is used:
    
    ``j2/j0 = -1``, when ``z --> \infty.``

    Parameters
    -------
    z : array
    """
    mask = np.abs(np.imag(z)) < 700
    value = np.zeros_like(z, dtype = complex)
    value[mask] = jv(2, z[mask]) / jv(0, z[mask])
    value[~mask] = -1
    return value

class AcousticElement:
    """An acoustic element.
    This class creates an acoustic element from input data.

    Parameters
    ----------
    first_node : Node object
        Fist node of element.

    last_node : Node object
        Last node of element.

    index : int
        Element index.

    element_type : str, ['undamped', 'proportional', 'wide_duct', 'LRF_fluid_equivalent', 'LRF_full'], optional
        Element type
        Default is 'undamped'.

    proportional_damping : float, optional
        Proportional damping coefficient 
        Default is 'None'.

    material : Material object, optional
        Element structural material.
        Default is 'None'.

    fluid : Fluid object, optional
        Element acoustic fluid.
        Default is 'None'.

    cross_section : CrossSection object, optional
        Element cross section.
        Default is 'None'.

    loaded_pressure : array, optional
        Acoustic pressure on the nodes.
        Default is [0, 0].

    acoustic_length_correction : int, [0, 1, 2], optional
        Acoustic length correction due to acoustic discontinuities. 
        The prescription is done through the following labeling:
        None: disable
        0 : expansion
        1 : side_branch
        2 : loop 
        Default is None.
    """
    def __init__(self, first_node: Node, last_node: Node, index: int, **kwargs):

        self.first_node = first_node
        self.last_node = last_node
        self.index = index

        self.element_type = kwargs.get('element_type', 'undamped')
        self.proportional_damping = kwargs.get('proportional_damping', None)
        self.material = kwargs.get('material', None)
        self.fluid = kwargs.get('fluid', None)   
        self.cross_section = kwargs.get('cross_section', None)
        self.cross_section_points = kwargs.get('cross_section_points', None)
        self.loaded_pressure = kwargs.get('loaded_forces', np.zeros(DOF_PER_NODE))
        self.perforated_plate = kwargs.get('perforated_plate', None)
        self.vol_flow = kwargs.get('vol_flow', 0)
        self.length_correction_data = kwargs.get('length_correction_data', None)
        self.turned_off = kwargs.get("turned_off", False)
        self.volumetric_flow_rate = kwargs.get("volumetric_flow_rate", None)

        self.reset()

    @property
    def length(self):
        """
        This method returns the element's length.

        Returns
        -------
        float
            Element length.
        """
        return distance(self.first_node, self.last_node) 

    @property
    def orientation(self):
        """
        This method returns element's axial orientation in the global coordinate system.

        Returns
        -------
        array
            x-axis vector.
        """
        return self.last_node.coordinates - self.first_node.coordinates

    @property
    def impedance(self):
        """
        This method returns the element's acoustic impedance based on its fluid and cross section.

        Returns
        -------
        float
            The element impedance.
        """
        return self.fluid.impedance / self.area_fluid

    @property
    def mach(self):
        return self.vol_flow / (self.speed_of_sound_corrected()*self.area_fluid)
    
    def reset(self):

        self.pp_impedance = None

        self.flag_plane_wave = False
        self.flag_wide_duct = False
        self.flag_lrf_fluid_eq = False
        self.flag_lrf_full = False
        self.flag_unflanged_radiation_impedance = False

        self.max_valid_freq = np.inf
        self.min_valid_freq = 0
        self.delta_pressure = 0

        self.acoustic_link_diameters = list()

        self.section_parameters_render = None

    def update_delta_pressure(self, delta_pressure):
        self.delta_pressure = delta_pressure

    @property
    def global_dof(self):
        """
        This method returns a list of the element's global degree of freedom.

        Returns
        -------
        list
            Indexes of the global degree of freedom.
        """
        global_dof = np.zeros(DOF_PER_ELEMENT, dtype=int)
        global_dof[:DOF_PER_NODE] = self.first_node.global_index
        global_dof[DOF_PER_NODE:] = self.last_node.global_index
        return global_dof

    def global_matrix_indexes(self):
        """
        This method returns the rows' and columns' indexes that place the element's matrices 
        in the global matrices. The created lists are  such that the method is useful to 
        generate sparse matrices.

        Returns
        -------
        rows : list
            List of indexes of the global matrices' rows where the element's matrices have to be added.

        cols : list
            List of indexes of the global matrices' columns where the element's matrices have to be added.
        """
        rows = self.global_dof.reshape(DOF_PER_ELEMENT, 1) @ np.ones((1, DOF_PER_ELEMENT))
        cols = rows.T
        return rows, cols

    def speed_of_sound_corrected(self):
        """
        This method returns the corrected speed of sound due to the mechanical compliance of the pipe wall.

        Returns
        -------
        float
            Speed of sound in the element.
            
        References
        ----------
        .. T. C. Lin and G. W. Morgan, "Wave Propagation through Fluid Contained in a Cylindrical, Elastic Shell," The Journal of the Acoustical Society of America 28:6, 1165-1176, 1956.
        """
        if self.cross_section.section_type_label == 'Expansion joint':
            return self.fluid.speed_of_sound
        else:
            factor = self.cross_section.inner_diameter * self.fluid.bulk_modulus / (self.material.elasticity_modulus * self.cross_section.thickness)
            return (1 / sqrt(1 + factor))*self.fluid.speed_of_sound
        
    def get_damping_for_shear_stress_in_liquids(self, frequencies: np.ndarray):

        Q = self.volumetric_flow_rate

        if Q is None:
            return 0.

        rho = self.fluid.density
        c_0 = self.fluid.speed_of_sound
        mu = self.fluid.dynamic_viscosity
        v = mu / rho

        A = self.cross_section.area_fluid
        d = self.cross_section.outer_diameter
        u = Q / A

        Re = u * d * rho / mu

        # Colebrook equation for determining the Darcy friction factor
        def colebrook_equation(x):
            return 2*np.log10(Re*(x**0.5)) - 0.8 - (1/(x**0.5))

        # use Haaland approximation for Colebrook equation as initial guess value for Darcy friction factor
        x_initial = 1 / ((-1.8 * np.log10(6.9 / Re))**0.5)

        f_d = fsolve(colebrook_equation, x_initial)

        omega = 2 * np.pi * frequencies
        k_0 = omega / c_0

        kappa = 14.3 / (Re**0.05)
        beta = 0.54 * (v / (d**2)) * (Re**kappa)

        # shear stress term
        alpha_r = -1j * f_d * abs(Q) / (omega * d * A) + (4 / d) * np.sqrt(v / (beta + 1j*omega))

        # viscous elasticity term
        alpha_v = 0.

        # complex wave number
        k = k_0 * np.sqrt(1 + alpha_r) * np.sqrt(1 + alpha_v)

        # complex speed of sound
        c = k / omega

        # acoustic impedance
        Z = rho * c

        return k, Z
        
    def matrix(self, frequencies, length_correction=0):
        """
        This method returns the element's admittance matrix for each frequency of analysis 
        according to the element type. The method allows to include the length correction due 
        to acoustic discontinuities (loop, expansion, side branch).

        Parameters
        ----------
        frequencies : array
            Frequencies of analysis in Hz.

        length_correction : float, optional
            Element length correction to be added into the element length.

        Returns
        -------
        2D array
            Element's admittance matrix. Each row of the output array is an element's 
            admittance matrix corresponding to a frequency of analysis.
        """
        self.area_fluid = self.cross_section.area_fluid
        if self.perforated_plate:
            if self.perforated_plate.type in [0, 1]:
                return self.perforated_plate_matrix(frequencies)
            else:
                d = self.perforated_plate.hole_diameter
                self.area_fluid = pi*(d**2) / 4

        self.reset()
        if self.element_type in ['undamped_mean_flow','peters','howe']:
            return self.fetm_mean_flow_matrix(frequencies, length_correction)

        elif self.element_type in ['undamped', 'proportional', 'wide_duct','LRF_fluid_equivalent']:
            return self.fetm_matrix(frequencies, length_correction)

        elif self.element_type == 'LRF full':
            return self.lrf_thermoviscous_matrix(frequencies, length_correction)

    def fetm_matrix(self, frequencies, length_correction = 0):
        """
        This method returns the FETM 1D element's admittance matrix for each frequency of analysis. 
        The method allows to include the length correction due to  acoustic discontinuities 
        (loop, expansion, side branch). The damping models compatible with FETM 1D are Undamped, 
        Proportional, Wide-duct, and LRF fluid equivalent.

        Parameters
        ----------
        frequencies : array
            Frequencies of analysis in Hertz.
            
        length_correction : float, optional
            Element length correction to be added into the element length.

        Returns
        -------
        2D array
            Element's admittance matrix. Each row of the output array is an element's 
            admittance matrix corresponding to a frequency of analysis.
        """
        ones = np.ones(len(frequencies), dtype='float64')
        kappa_complex, impedance_complex = self.get_fetm_damping_data(frequencies)
        # self.radiation_impedance(kappa_complex, impedance_complex)

        kappaLe = kappa_complex * (self.length + length_correction)
        sine = np.sin(kappaLe)
        cossine = np.cos(kappaLe)
        Zf = impedance_complex / self.area_fluid

        # TODO: check this
        matrix = ((1j/(Zf*sine))*np.array([-cossine, ones, ones, -cossine])).T
        
        return matrix

    def lrf_thermoviscous_matrix(self, frequencies, length_correction=0):
        """
        This method returns the LRF thermoviscous 1D elementary admittance matrix for each 
        frequency of analysis. The method allows to include the length correction due to 
        acoustic discontinuities (loop, expansion, side branch).

        Parameters
        ----------
        frequencies : array
            Frequencies of analysis in Hertz.
            
        length_correction : float, optional
            Element length correction to be added into the element length.

        Returns
        -------
        2D array
            Elementary admittance matrix. Each row of the output array is an element 
            admittance matrix corresponding to a frequency of analysis.
        """
        ones = np.ones(len(frequencies), dtype='float64')
        omega = 2 * pi * frequencies
        rho = self.fluid.density
        nu = self.fluid.kinematic_viscosity
        gamma = self.fluid.isentropic_exponent
        pr = self.fluid.prandtl
        
        c = self.speed_of_sound_corrected()
        length = self.length + length_correction
        radius = self.cross_section.inner_diameter / 2
        kappa_real = omega / c

        s = radius * np.sqrt(omega / nu)
        sigma = sqrt(pr)

        aux_lrft2 = s < 4

        if np.any(aux_lrft2):
            self.min_valid_freq = np.max(frequencies[aux_lrft2])
            self.flag_lrf_full = True

        aux1 = j2_j0(1j**(3/2) * s * sigma)
        aux2 = j2_j0(1j**(3/2) * s)
        
        n = 1 + aux1 * (gamma - 1)/gamma

        T = np.sqrt( gamma * n / aux2 )

        kappa_complex = T * kappa_real
        impedance_complex = c * rho / T
        # self.radiation_impedance(kappa_complex, impedance_complex)

        G = - 1j * gamma * n / T

        sinh = np.sinh(kappa_complex * length)
        cosh = np.cosh(kappa_complex * length)

        matrix = - ((self.area_fluid * G / (impedance_complex * sinh)) * np.array([cosh, -ones, -ones, cosh])).T

        aux = np.real(kappa_complex * radius) > 1.84118
        if np.any(aux):
            self.flag_plane_wave = True
            self.max_valid_freq = np.min([np.min(frequencies[aux]), self.max_valid_freq])

        return matrix  

    def fetm_mean_flow_matrix(self, frequencies, length_correction = 0):

        k, z, M = self.get_fetm_mean_flow_damping_data(frequencies)
        # self.radiation_impedance(k, z* (1-M**2))
        
        kLe = k * (self.length + length_correction)
        cotanh = 1/np.tanh(1j*kLe)
        sineh = np.sinh(1j*kLe)
        exp_neg_sin = -np.exp(-1j*kLe*M)/sineh
        exp_sin = -np.exp(1j*kLe*M)/sineh
        adm = self.area_fluid / (z * (1-M**2))
        matrix = (adm*np.array([cotanh - M, exp_neg_sin, exp_sin, cotanh + M])).T

        return matrix

    def fem_1d_matrix(self, length_correction=0 ):
        """
        This method returns the FEM acoustic 1D elementary matrices. The method allows to include 
        the length correction due to  acoustic discontinuities (loop, expansion, side branch). The 
        FEM is not compatible with any damping model.
        
        Obs.: In the OpenPulse, this formulation is only used to evaluate the acoustic modal analysis.

        Parameters
        ----------
        length_correction : float, optional
            Element length correction to be added into the element length.

        Returns
        -------
        Ke : 2D array
            Element acoustic stiffness matrix.

        Me : 2D array
            Element acoustic inertia matrix.
        """
        length = self.length + length_correction
        rho = self.fluid.density
        c = self.speed_of_sound_corrected()

        self.area_fluid = self.cross_section.area_fluid
        if self.perforated_plate:
            if self.perforated_plate.type in [2]:
                d = self.perforated_plate.hole_diameter
                self.area_fluid = pi*(d**2)/4

        Ke = (self.area_fluid / (rho*length)) * np.array([[ 1,-1],
                                                          [-1, 1]], dtype=float)

        Me = (self.area_fluid * length / (6*rho*c**2)) * np.array([[2, 1],
                                                                   [1, 2]], dtype=float)

        return Ke, Me

    def fetm_link_matrix(self, frequencies):
        """
        This method returns the FETM 1D element's admittance matrix for each frequency of analysis. 
        The method allows to include the length correction due to  acoustic discontinuities 
        (loop, expansion, side branch). The damping models compatible with FETM 1D are Undamped, 
        Proportional, Wide-duct, and LRF fluid equivalent.

        Parameters
        ----------
        frequencies : array
            Frequencies of analysis in Hertz.
            
        length_correction : float, optional
            Element length correction to be added into the element length.

        Returns
        -------
        2D array
            Element's admittance matrix. Each row of the output array is an element's admittance 
            matrix corresponding to a frequency of analysis.
        """
        ones = np.ones(len(frequencies), dtype='float64')
        kappa_complex, impedance_complex = self.get_fetm_damping_data(frequencies)
        
        kappaLe = kappa_complex * (self.length / 10)
        sine = np.sin(kappaLe)
        cossine = np.cos(kappaLe)
        matrix = ((self.area_fluid*1j/(sine*impedance_complex))*np.array([-cossine, ones, ones, -cossine])).T

        return matrix

    def fem_1d_link_matrix(self):
        """
        This method returns the FEM acoustic 1D elementary matrices. The method allows to include the 
        length correction due to  acoustic discontinuities (loop, expansion, side branch). The FEM is 
        not compatible with any damping model.
        
        Obs.: In the OpenPulse, this formulation is only used to evaluate the acoustic modal analysis.

        Parameters
        ----------
        length_correction : float, optional
            Element length correction to be added into the element length.

        Returns
        -------
        Ke : 2D array
            Element acoustic stiffness matrix.

        Me : 2D array
            Element acoustic inertia matrix.
        """
        length = self.length / 10
        rho = self.fluid.density
        c = self.speed_of_sound_corrected()

        self.area_fluid = self.cross_section.area_fluid
        if self.perforated_plate:
            if self.perforated_plate.type in [2]:
                d = self.perforated_plate.hole_diameter
                self.area_fluid = pi*(d**2)/4

        Ke = self.area_fluid / (rho*length) * np.array([[1,-1],[-1,1]])
        Me = self.area_fluid * length / (6*rho*c**2) * np.array([[2,1],[1,2]]) 
        
        return Ke.flatten(), Me.flatten()

    def get_fetm_damping_data(self, frequencies: np.ndarray):
        """
        This method returns wavenumber and fluid impedance for the FETM 1D theory according to 
        the element's damping model (element type). The damping models compatible with FETM 1D 
        are Undamped, Proportional, Wide-duct, and LRF fluid equivalent.

        Parameters
        ----------
        frequencies : array
            Frequencies of analysis in Hz.

        Returns
        -------
        kappa : complex-array
            Complex wavenumber. This array have the same structure of the frequencies array.

        z : complex-array
            Complex impedance. This array have the same structure of the frequencies array.
        """

        c0 = self.speed_of_sound_corrected()
        rho_0 = self.fluid.density

        omega = 2 * pi * frequencies
        kappa_real = omega / c0

        radius = self.cross_section.inner_diameter / 2

        if self.element_type == 'undamped':
            aux = np.real(kappa_real * radius) > 1.84118
            if np.any(aux):
                self.flag_plane_wave = True
                self.max_valid_freq = np.min(frequencies[aux])
            return kappa_real, c0 * rho_0

        elif self.element_type == 'proportional':
            hysteresis = (1 - 1j*self.proportional_damping)
            kappa_complex = kappa_real * hysteresis
            impedance_complex = c0 * rho_0 * hysteresis

            aux = np.real(kappa_real * radius) > 1.84118
            if np.any(aux):
                self.flag_plane_wave = True
                self.max_valid_freq = np.min(frequencies[aux])
            return kappa_complex, impedance_complex

        elif self.element_type == 'wide_duct':
            nu = self.fluid.kinematic_viscosity
            pr = self.fluid.prandtl
            gamma = self.fluid.isentropic_exponent
            k0 = self.fluid.thermal_conductivity

            aux_wd1 = radius < 10*sqrt(2*nu/omega) 
            aux_wd2 = radius < 10*sqrt(2*k0/omega) 
            aux = np.any(np.array([aux_wd1, aux_wd2]), axis=0)

            aux_wd3 = sqrt(2*omega * nu)/c0 > 1/10

            if np.any(aux):
                self.min_valid_freq = np.max(frequencies[aux])
                self.flag_wide_duct = True

            if np.any(aux_wd3):
                self.max_valid_freq = np.min(frequencies[aux_wd3])
                self.flag_wide_duct = True

            aux = np.real(kappa_real * radius) > 1.84118
            if np.any(aux):
                self.flag_plane_wave = True
                self.max_valid_freq = np.min([np.min(frequencies[aux]), self.max_valid_freq]) 

            const = 1 - 1j* np.sqrt(nu/(2*omega)) * ((1 + (gamma-1)/sqrt(pr))/radius)

            kappa_complex = kappa_real*const
            impedance_complex = rho_0*c0*const
            return kappa_complex, impedance_complex

        elif self.element_type == 'LRF_fluid_equivalent':
            nu = self.fluid.kinematic_viscosity
            gamma = self.fluid.isentropic_exponent
            alpha = self.fluid.thermal_diffusivity
            radius = self.cross_section.inner_diameter / 2

            aux = np.sqrt(omega)
            kappa_v = aux * np.sqrt(-1j / nu)
            kappa_t = aux * np.sqrt(-1j / alpha)

            aux_lrfeq1 = np.abs(kappa_t / kappa_real) < 10
            aux_lrfeq2 = np.abs(kappa_v / kappa_real) < 10
            aux = np.any(np.array([aux_lrfeq1, aux_lrfeq2]), axis=0)

            if np.any(aux):
                self.max_valid_freq = np.min(frequencies[aux]) 
                self.flag_lrf_fluid_eq = True

            y_v = - j2_j0(kappa_v * radius)
            y_t =   j2_j0(kappa_t * radius) * (gamma-1) + gamma

            kappa_complex = kappa_real * np.sqrt(y_t / y_v)
            impedance_complex = c0 * rho_0 / np.sqrt(y_t * y_v)

            aux = np.real(kappa_complex * radius) > 1.84118
            if np.any(aux):
                self.flag_plane_wave = True
                self.max_valid_freq = np.min([np.min(frequencies[aux]), self.max_valid_freq]) 

            return kappa_complex, impedance_complex

    def get_fetm_mean_flow_damping_data(self, frequencies):

        omega = 2 * pi * frequencies
        c0 = self.speed_of_sound_corrected()
        rho_0 = self.fluid.density
        kappa_real = omega/c0
        di = self.cross_section.inner_diameter
        radius = di / 2

        if self.element_type == 'undamped_mean_flow':
            aux = np.real(kappa_real*(1-self.mach**2) * radius) > 1.84118
            if np.any(aux):
                self.flag_plane_wave = True
                self.max_valid_freq = np.min(frequencies[aux])
            return kappa_real, c0 * rho_0, self.mach

        elif self.element_type == 'howe':
            nu = self.fluid.kinematic_viscosity
            alpha = self.fluid.thermal_diffusivity
            pr = self.fluid.prandtl
            gamma = self.fluid.isentropic_exponent
            U = self.mach * self.speed_of_sound_corrected()
            Karmank = 0.41

            # TODO: prt warning por p < 0.5
            prt = 0.87
            transc = lambda x: (U/x - (2.44 * np.log(x * di/(2*nu)) + 2))**2
            res = root(transc, 1e-4, method='hybr')

            ur = res.x[0]
            w_ast = 0.01*ur**2/nu
            delta_vs = nu/ur*6.5*(1 + (1.7*(omega/w_ast)**3)/(1+(omega/w_ast)**3))

            aux1 = np.sqrt(1j*omega*nu)/(Karmank*ur)
            aux2 = delta_vs * np.sqrt(1j*omega/nu)
            aux3 = np.sqrt(1j*omega*alpha)*prt/(Karmank*ur)
            aux4 = delta_vs * np.sqrt(1j*omega/alpha)

            F1 = 1j*(hankel1(1,aux1)*np.cos(aux2) -  hankel1(0,aux1)*np.sin(aux2))/(hankel1(0,aux1)*np.cos(aux2) +  hankel1(1,aux1)*np.sin(aux2))
            F2 = 1j*(hankel1(1,aux3)*np.cos(aux4) -  hankel1(0,aux3)*np.sin(aux4))/(hankel1(0,aux3)*np.cos(aux4) +  hankel1(1,aux3)*np.sin(aux4))

            aux1 = np.sqrt(2)*(1-1j)*np.sqrt(omega*nu)/(c0*di)
            aux2_m = np.conj(F1/(1-self.mach)**2 + (gamma-1)*F2*np.sqrt(alpha/nu))
            aux2_M = np.conj(F1/(1+self.mach)**2 + (gamma-1)*F2*np.sqrt(alpha/nu))

            kappa_m = 1/(1-self.mach)*(kappa_real + aux1*aux2_m)
            kappa_M = 1/(1+self.mach)*(kappa_real + aux1*aux2_M)

            kappa = (kappa_M + kappa_m)/2
            c = omega/kappa
            z = rho_0 * c
            mach_ef = U/c

            aux = np.real(kappa*(1-mach_ef**2) * radius) > 1.84118
            if np.any(aux):
                self.flag_plane_wave = True
                self.max_valid_freq = np.min(frequencies[aux])

            return kappa, z, mach_ef

        elif self.element_type == 'peters':
            nu = self.fluid.kinematic_viscosity
            gamma = self.fluid.isentropic_exponent
            pr = self.fluid.prandtl

            U = self.mach * self.speed_of_sound_corrected()
            ur = np.sqrt(0.03955) * (nu/di)**(1/8) * U**(7/8)

            delta_vs = 12.5
            delta_a = np.sqrt(2*nu/omega)
            delta_ap = delta_a*ur/nu

            aux1 = delta_a/di
            aux2 = (1 + np.exp(-2*(1+1j)*(delta_vs / delta_ap) -200j/delta_ap**2 ))/(1 - np.exp(-2*(1+1j)*(delta_vs / delta_ap)))
            aux3 = (1 + (gamma - 1)/np.sqrt(pr))

            kappa_m = kappa_real/(1-self.mach) * ( -1 - (1-1j)*aux1*aux2*aux3)
            kappa_M = kappa_real/(1+self.mach) * ( +1 + (1-1j)*aux1*aux2*aux3)

            kappa = (kappa_M - kappa_m)/2
            c = omega/kappa
            z = rho_0 * c
            mach_ef = U/c

            aux = np.real(kappa*(1-mach_ef**2) * radius) > 1.84118
            if np.any(aux):
                self.flag_plane_wave = True
                self.max_valid_freq = np.min(frequencies[aux])
            return kappa, z, mach_ef
  
    def get_fetm_thermoviscous_damping_data(self, frequencies: np.ndarray):

        omega = 2 * pi * frequencies
        rho = self.fluid.density
        nu = self.fluid.kinematic_viscosity
        gamma = self.fluid.isentropic_exponent
        pr = self.fluid.prandtl

        c = self.speed_of_sound_corrected()

        radius = self.cross_section.inner_diameter / 2
        kappa_real = omega / c

        s = radius * np.sqrt(omega / nu)
        sigma = sqrt(pr)

        aux1 = j2_j0(1j**(3/2) * s * sigma)
        aux2 = j2_j0(1j**(3/2) * s)

        n = 1 + aux1 * (gamma - 1)/gamma

        T = np.sqrt( gamma * n / aux2 )

        kappa_complex = T * kappa_real
        impedance_complex = c * rho / T

        return kappa_complex, impedance_complex

    def update_pp_impedance(self, frequencies):

        # Fluid physical quantities
        if frequencies[0]==0:
            frequencies[0] = float(1e-4)

        rho = self.fluid.density
        mu = self.fluid.dynamic_viscosity
        gamma = self.fluid.isentropic_exponent
        kappa = self.fluid.thermal_conductivity
        c_p = self.fluid.specific_heat_Cp
        c = self.speed_of_sound_corrected()
        z = self.fluid.impedance

        # Perforated plate physical quantities
        d = self.perforated_plate.hole_diameter
        t = self.perforated_plate.thickness
        sigma = self.perforated_plate.porosity
        t_foks = t + self.perforated_plate.foks_delta
        c_l = self.perforated_plate.linear_discharge_coefficient

        omega = 2 * pi * frequencies
        k = omega / c

        if isinstance(self.pp_impedance, np.ndarray):
            u_n = np.abs(self.delta_pressure / self.pp_impedance)
        else:
            u_n = 0

        self.u_n = u_n

        if self.perforated_plate.type == 0:
            theta_rad = self.perforated_plate.radiation_impedance(k)

            #TODO: use mach number as input when the formulation is validated
            # theta_flow = self.perforated_plate.flow_impedance(0) 
            theta_flow = 0

            #TODO: use mach number as input when the formulation is validated
            if self.perforated_plate.bias_flow_effects:
                theta_g = self.perforated_plate.bias_impedance(0)
            else:
                theta_g = 0

            if self.perforated_plate.nonlinear_effects:
                theta_nl = self.perforated_plate.nonlinear_impedance(c, u_n)
            else:
                theta_nl = 0

            if isinstance(self.perforated_plate.dimensionless_impedance, (complex, np.ndarray)):
                theta_user = self.perforated_plate.dimensionless_impedance
            else:
                theta_user = 0

            k_viscous = np.sqrt(-1j * omega * rho / mu)
            mean_viscous_field = - j2_j0(k_viscous*d/2)
            
            k_thermal = np.sqrt(-1j * omega * rho * c_p / kappa)
            mean_thermal_field = (gamma + (gamma - 1) *j2_j0(k_thermal*d/2)) 

            k_vt = k * np.sqrt(mean_thermal_field/mean_viscous_field) 
            z_vt = z / np.sqrt(mean_thermal_field * mean_viscous_field)

            theta = - z *(theta_rad + theta_flow + theta_g + theta_nl + theta_user)

            z_orif = - 2j * z_vt * np.sin(k_vt * t_foks / 2) / (sigma*c_l) + theta

        elif self.perforated_plate.type == 1: # Melling's model
            nu = self.fluid.kinematic_viscosity

            k_stokes = np.sqrt( -1j*omega / nu)
            k_ef = np.sqrt( -1j*omega / (2.179 * nu))
            foks_porosity = Foks_function(np.sqrt(sigma))

            xi_l = 1j*k/(sigma*c_l)*( t / f_function(k_ef * d/2) + 8* d/(3*pi * f_function(k_stokes * d/2))*foks_porosity )
            xi_nl = 4 * u_n * (1-sigma**2)/(3*pi*c*(sigma*c_l)**2)
            z_orif = - (xi_l + xi_nl) * z 

        self.pp_impedance = z_orif

    def perforated_plate_matrix(self, frequencies):
        self.update_pp_impedance(frequencies)
        admittance = self.area_fluid / self.pp_impedance       
        return np.c_[- admittance, admittance, admittance, - admittance]

    def unflanged_termination_impedance(self, kappa_complex, impedance_complex):
        """
        This method updates the radiation impedance attributed to the element nodes according 
        to the unflanged prescription.

        Parameters
        -------
        kappa_complex : complex-array
            Complex wavenumber.

        impedance_complex : complex-array
            Complex system impedance.

        Returns
        -------
        array
            Unflanged pipe termination impedance. The array has the same length as kappa_complex parameter.
        """

        radius = self.cross_section.inner_radius
        
        kr = kappa_complex * radius
        mask = kr<=1
        
        kr_less_t_1 = kr[mask]
        gamma = np.exp(0.5772)
        aux_1_1 = np.abs(np.exp((-kr_less_t_1**2)/2) * (1 + kr_less_t_1**4 / 6 * np.log(1 / (gamma * kr_less_t_1) + 19/12)))

        kr_great_t_1 = kr[~mask]

        if np.any(kr_great_t_1 > 1.84118):
            self.flag_unflanged_radiation_impedance = True

        aux_1_2 = np.abs(np.sqrt(pi * kr_great_t_1) * np.exp(-kr_great_t_1) * (1 + 3 / (32 * kr_great_t_1**2)))
        aux_1 = np.r_[aux_1_1, aux_1_2]
        aux_2 = - aux_1 * np.exp( -2j * kr * poly_function(kr))

        return impedance_complex * (1 + aux_2)/(1 - aux_2) + 0j

    def flanged_termination_impedance(self, kappa_complex, impedance_complex):
        """
        This method updates the radiation impedance attributed to the element nodes 
        according to the flanged prescription.

        Parameters
        -------
        kappa_complex : complex-array
            Complex wavenumber.

        impedance_complex : complex-array
            Complex impedance.

        Returns
        -------
        array
            Flanged termination impedance. The array has the same length as kappa_complex parameter.
        """
        radius = self.cross_section.inner_radius
        kr = kappa_complex * radius
        return impedance_complex * (1 - jv(1, 2 * kr) / kr  + 1j * H1(2 * kr) / kr  ) + 0j 

    def get_radiation_impedance(self, impedance_type: int, frequencies: np.ndarray | None) -> (np.ndarray | complex):

        """
        This method returns the radiation impedance attributed to the element node termination 
        according to the impedance type, element type and damping model.

        Parameters
        -------
        impedance_type : int
            Integer number relative to radiation impedance type.

            0 -> anechoic termination
            1 -> flanged termination
            2 -> unflanged termination

        frequencies : float-array
            The frequencies vector of the harmonic analysis.

        Returns
        -------
        array
            Radiation impedance. The array has the same length as frequencies parameter.
        """
        if frequencies is None:
            frequencies = np.array([0], dtype=float)

        if self.element_type in ['undamped_mean_flow', 'peters', 'howe']:
            k, z, M = self.get_fetm_mean_flow_damping_data(frequencies)
            kappa_complex = k
            impedance_complex = z * (1 - M**2)

        elif self.element_type in ['undamped', 'proportional', 'wide_duct', 'LRF_fluid_equivalent']:
            kappa_complex, impedance_complex = self.get_fetm_damping_data(frequencies)

        elif self.element_type == 'LRF full':
            kappa_complex, impedance_complex = self.get_fetm_thermoviscous_damping_data(frequencies)

        if impedance_type == 0:
            return impedance_complex + 0j

        elif impedance_type == 1:
            return self.flanged_termination_impedance(kappa_complex, impedance_complex)

        elif impedance_type == 2:
            return self.unflanged_termination_impedance(kappa_complex, impedance_complex)

# fmt: on