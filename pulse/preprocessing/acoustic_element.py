from numpy import sqrt, pi
import numpy as np
from scipy.special import jv, hankel1
from scipy.optimize import root
from pulse.preprocessing.perforated_plate import Foks_function
from pulse.preprocessing.node import distance

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
    Auxiliary polynomial function to define the unflanged radiation impedance.

    Parameters
    ----------
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

def j2j0(z):
    """
    Auxiliary function to compute the ratio between the Bessel functions J2 and J0. When the imaginary part of input z reaches 700, the following syntonic approximation is used:
    
    .. math::
        \\frac{J_2(z)}{J_0(z)} = -1, \\quad \\text{if } \\Im\\{z\\} > 700.

    Parameters
    ----------
    array
    """
    mask = np.abs(np.imag(z))<700
    value = np.zeros_like(z, dtype = complex)
    value[mask] = jv(2, z[mask]) / jv(0, z[mask])
    value[~mask] = -1
    return value

class AcousticElement:
    """
    This class creates an acoustic element from input data. The FETM element formulation has two **nodes** (**first** and **last** nodes), where pressure is evaluated: ::
    
        n0-----------n1 --> x 

    The acoustic domain is delimited by its **nodes** and **cross section**. Externally, there is an associated **structural element** (pipe), whose domain is constituted by a **material**. Futhermore, the acoustic domain is constituted by a **fluid** and, if it is moving, the **volumetric flow rate** must be set. The FETM formulation implemented in OpenPulse can model damping through several theories, namely **proportional**, **wide-duct**, **LRF fluid equivalent**, **LRF full**, **peters**, and **howe**. Peters' and Howe's models are suitable for mean flow systems, i.e., **volumetric flow rate** not equal to 0.

    Parameters
    ----------
    first_node : Node object
        Element's first node.

    last_node : Node object
        Element's last node.

    index : int
        Element's index.

    element_type : ['undamped', 'proportional', 'wide-duct', 'LRF fluid equivalent', 'LRF full', 'undamped mean flow','peters','howe'], optional
        Element damping formulation. When ``'undamped mean flow'``, ``'peters'`` or ``'howe'`` is set, the volumetric flow rate must be set, i.e., ``vol_flow !=0``. Default is ``'undamped'``.

    proportional_damping : float, optional
        Proportional damping coefficient. Set this parameter when ``element_type = 'proportional'``. Default is ``'None'``.

    material : Material object, optional
        Structural domain material. Default is ``'None'``.

    fluid : Fluid object, optional
        Acoustic domain fluid. Default is ``'None'``.

    cross_section : CrossSection object, optional
        Element's cross section. Default is ``'None'``.

    perforated_plate : PerforatedPlate object, optional
        Element's perforated plate. Default is ``'None'``.

    vol_flow : float, optional
        Volumetric flow rate in the element's acoustic domain. Default ``0``.

    loaded_pressure : (2,) array, optional
        Acoustic pressure on the nodes. Default is ``[0, 0]``.

    acoustic_length_correction : [0, 1, 2], optional
        Acoustic length correction due to acoustic discontinuities. The prescription is done through the following labeling: ::

            None : disable
            0 : expansion
            1 : side_branch
            2 : loop 
        2 : loop 
            2 : loop 

        Default is ``'None'``.
    """
    def __init__(self, first_node, last_node, index, **kwargs):
        self.first_node = first_node
        self.last_node = last_node
        self.index = index

        self.element_type = kwargs.get('element_type', 'undamped')
        self.proportional_damping = kwargs.get('proportional_damping', None)
        self.material = kwargs.get('material', None)
        self.fluid = kwargs.get('fluid', None)   
        self.cross_section = kwargs.get('cross_section', None)
        self.perforated_plate = kwargs.get('perforated_plate', None)
        self.vol_flow = kwargs.get('vol_flow', 0)

        self.loaded_pressure = kwargs.get('loaded_forces', np.zeros(DOF_PER_NODE))
        self.acoustic_length_correction = kwargs.get('acoustic_length_correction', None)

        self.cross_section_points = None
        self.delta_pressure = 0
        self.pp_impedance = None

        self._reset_flags()

    @property
    def length(self):
        """:float: Element's length. """
        return distance(self.first_node, self.last_node) 

    @property
    def orientation(self):
        """:(3,) array: Element's axial orientation in the global coordinate system. """
        return self.last_node.coordinates - self.first_node.coordinates

    @property
    def impedance(self):
        """:float: Element's acoustic impedance based on its fluid and cross section."""
        return self.fluid.impedance / self.area_fluid

    @property
    def mach(self):
        """:float: Mach number in the element domain."""
        return self.vol_flow / (self.speed_of_sound_corrected()*self.area_fluid)

    @property
    def global_dof(self):
        """:(2,) array: Element's global degree of freedom indexes."""
        global_dof = np.zeros(DOF_PER_ELEMENT, dtype=int)
        global_dof[:DOF_PER_NODE] = self.first_node.global_index
        global_dof[DOF_PER_NODE:] = self.last_node.global_index
        return global_dof
    
    def _reset_flags(self):
        """
        This method reset element's check flags.
        """
        self.flag_plane_wave = False
        self.flag_wide_duct = False
        self.flag_lrf_fluid_eq = False
        self.flag_lrf_full = False
        self.flag_unflanged_radiation_impedance = False

        self.max_valid_freq = np.inf
        self.min_valid_freq = 0

    def update_pressure(self, solution):
        """
        Auxiliary method used in the perforated plate model.

        Parameters
        ----------
        solution : (N, M) array
            System's acoustic solution. ``N`` is the number of acoustic degree of freedom and ``M`` is the number of frequencies of analysis.
        """
        pressure_first = solution[self.first_node.global_index, :]
        pressure_last = solution[self.last_node.global_index, :]
        self.delta_pressure =  pressure_last - pressure_first

    def global_matrix_indexes(self):
        """
        This method returns the rows' and columns' indexes that place the element's matrices in the global matrices. The created array are appropriated to generate sparse matrices.

        Returns
        -------
        rows : (2,2) array
            Indexes of the global matrices' rows where the element's matrices have to be added.

        cols : (2,2) array
            Indexes of the global matrices' columns where the element's matrices have to be added.
        """
        rows = self.global_dof.reshape(DOF_PER_ELEMENT, 1) @ np.ones((1, DOF_PER_ELEMENT))
        cols = rows.T
        return rows, cols

    def speed_of_sound_corrected(self):
        """
        This method computes the corrected speed of sound due to the mechanical compliance of the pipe wall.

        Returns
        -------
        float
            Speed of sound in the element.
            
        References
        ----------

        T. C. Lin and G. W. Morgan, *Wave Propagation through Fluid Contained in a Cylindrical, Elastic Shell,* The Journal of the Acoustical Society of America 28:6, 1165-1176, 1956.
        """
        if self.cross_section.section_label == 'Expansion joint section':
            return self.fluid.speed_of_sound
        else:
            factor = self.cross_section.inner_diameter * self.fluid.bulk_modulus / (self.material.young_modulus * self.cross_section.thickness)
            return (1 / sqrt(1 + factor))*self.fluid.speed_of_sound
        
    def matrix(self, frequencies, length_correction=0):
        """
        This method computes the element's admittance matrix for each frequency of analysis according to the element type. It allows to include the length correction due to acoustic discontinuities (``'loop'``, ``'expansion'``, ``'side branch'``).

        Parameters
        ----------
        frequencies : (N,) array
            Frequencies of analysis in Hz.

        length_correction : float, optional
            Element length correction to be added into the element length.
            Default is 0.

        Returns
        -------
        (N, 4) array 
            Element's admittance matrix. Each row of the output array ``matrix[i,:]`` may be rewritten to a 2-by-2 element's admittance matrix corresponding to the ``i``-th frequency of analysis ``frequencies[i]``.
            
            The vector to vector mapping is: ::

                +-                                -+        +-                -+ 
                | M[0,0]   M[0,1]  M[1,0]   M[1,1] |  <-->  | M[0,0]   M[0,1]  |   
                +-                                -+        | M[1,0]   M[1,1]  | 
                                                            +-                -+
        """
        self._reset_flags()
        self.area_fluid = self.cross_section.area_fluid
        if self.perforated_plate:
            if self.perforated_plate.type in [0,1]:
                return self.perforated_plate_matrix(frequencies, self.perforated_plate.nonlinear_effect)  
            else:
                d = self.perforated_plate.hole_diameter
                self.area_fluid = pi*(d**2)/4
        if self.element_type in ['undamped mean flow','peters','howe']:
            return self._fetm_mean_flow_matrix(frequencies, length_correction)
        elif self.element_type in ['undamped','proportional','wide-duct','LRF fluid equivalent']:
            return self._fetm_matrix(frequencies, length_correction)
        elif self.element_type == 'LRF full':
            return self._lrf_thermoviscous_matrix(frequencies, length_correction)  
    
    def _fetm_matrix(self, frequencies, length_correction = 0):
        """
        This method computes the FETM 1D element's admittance matrix for each frequency of analysis. It allows to include the length correction due to acoustic discontinuities (`loop`, `expansion`, `side branch`). The damping models compatible with FETM 1D are ``'undamped'``, ``'proportional'``, ``'wide-duct'``, and ``'LRF fluid equivalent'``.

        Parameters
        ----------
        frequencies : (N,) array
            Frequencies of analysis in Hz.
            
        length_correction : float, optional
            Element length correction to be added into the element length.

        Returns
        -------
        (N, 4) array 
            Element's admittance matrix. Each row of the output array ``matrix[i,:]`` may be rewritten to a 2-by-2 element's admittance matrix corresponding to the ``i``-th frequency of analysis ``frequencies[i]``.
        """
        ones = np.ones(len(frequencies), dtype='float64')
        kappa_complex, impedance_complex = self._fetm_damping_models(frequencies)
        self.radiation_impedance(kappa_complex, impedance_complex)
        
        kappaLe = kappa_complex * (self.length + length_correction)
        sine = np.sin(kappaLe)
        cossine = np.cos(kappaLe)
        matrix = ((self.area_fluid*1j/(sine*impedance_complex))*np.array([-cossine, ones, ones, -cossine])).T

        return matrix

    def _fetm_damping_models(self, frequencies):
        """
        This method computes the wavenumber and fluid impedance for the FETM 1D theory according to the element's damping model (element type). The damping models compatible with FETM 1D are ``'undamped'``, ``'proportional'``, ``'wide-duct'``, and ``'LRF fluid equivalent'``.

        Parameters
        ----------
        frequencies : (N,) array
            Frequencies of analysis in Hz.

        Returns
        -------
        kappa : (N,) complex-array
            Complex acoustic wavenumber.

        z : (N,) complex-array
            Complex acoustic impedance.
        """
        omega = 2 * pi * frequencies
        c0 = self.speed_of_sound_corrected()
        rho_0 = self.fluid.density
        kappa_real = omega/c0
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

        elif self.element_type == 'wide-duct':
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

        elif self.element_type == 'LRF fluid equivalent':
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

            y_v = - j2j0(kappa_v * radius)
            y_t =   j2j0(kappa_t * radius) * (gamma-1) + gamma

            kappa_complex = kappa_real * np.sqrt(y_t / y_v)
            impedance_complex = c0 * rho_0 / np.sqrt(y_t * y_v)

            aux = np.real(kappa_complex * radius) > 1.84118
            if np.any(aux):
                self.flag_plane_wave = True
                self.max_valid_freq = np.min([np.min(frequencies[aux]), self.max_valid_freq]) 

            return kappa_complex, impedance_complex

    def _lrf_thermoviscous_matrix(self, frequencies, length_correction=0):
        """
        This method computes the LRF thermoviscous 1D elementary admittance matrix for each frequency of analysis. It allows to include the length correction due to acoustic discontinuities (`loop`, `expansion`, `side branch`).

        Parameters
        ----------
        frequencies : (N,) array
            Frequencies of analysis in Hz.
            
        length_correction : float, optional
            Element length correction to be added into the element length.

        Returns
        -------
        (N, 4) array 
            Element's admittance matrix. Each row of the output array ``matrix[i,:]`` may be rewritten to a 2-by-2 element's admittance matrix corresponding to the ``i``-th frequency of analysis ``frequencies[i]``.
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

        aux1 = j2j0(1j**(3/2) * s * sigma)
        aux2 = j2j0(1j**(3/2) * s)
        
        n = 1 + aux1 * (gamma - 1)/gamma

        T = np.sqrt( gamma * n / aux2 )

        kappa_complex = T * kappa_real
        impedance_complex = c * rho / T
        self.radiation_impedance(kappa_complex, impedance_complex)

        G = - 1j * gamma * n / T

        sinh = np.sinh(kappa_complex * length)
        cosh = np.cosh(kappa_complex * length)

        matrix = - ((self.area_fluid * G / (impedance_complex * sinh)) * np.array([cosh, -ones, -ones, cosh])).T

        aux = np.real(kappa_complex * radius) > 1.84118
        if np.any(aux):
            self.flag_plane_wave = True
            self.max_valid_freq = np.min([np.min(frequencies[aux]), self.max_valid_freq]) 
        return matrix  
  
    def _fetm_mean_flow_matrix(self, frequencies, length_correction = 0):
        """
        This method computes the FETM 1D elementary admittance matrix including the acoustic domain mean flow velocity effects in the formulation, for each frequency of analysis. It allows to include the length correction due to acoustic discontinuities (`loop`, `expansion`, `side branch`).

        Parameters
        ----------
        frequencies : (N,) array
            Frequencies of analysis in Hz.
            
        length_correction : float, optional
            Element length correction to be added into the element length.

        Returns
        -------
        (N, 4) array 
            Element's admittance matrix. Each row of the output array ``matrix[i,:]`` may be rewritten to a 2-by-2 element's admittance matrix corresponding to the ``i``-th frequency of analysis ``frequencies[i]``.
        """
        k, z, M = self._fetm_mean_flow_damping_models(frequencies)
        self.radiation_impedance(k, z* (1-M**2))
        
        kLe = k * (self.length + length_correction)
        cotanh = 1/np.tanh(1j*kLe)
        sineh = np.sinh(1j*kLe)
        exp_neg_sin = -np.exp(-1j*kLe*M)/sineh
        exp_sin = -np.exp(1j*kLe*M)/sineh
        adm = self.area_fluid / (z * (1-M**2))
        matrix = (adm*np.array([cotanh - M, exp_neg_sin, exp_sin, cotanh + M])).T
        return matrix

    def _fetm_mean_flow_damping_models(self, frequencies):
        """
        This method computes the wavenumber, fluid impedance and mach number for the FETM 1D theory including the mean flow velocity effects in the acoustic domain according to the element's damping model (element type). The damping models compatible with mean flow FETM 1D are ``'undamped mean flow'``, ``'howe'``, and ``'peters'``.

        Parameters
        ----------
        frequencies : (N,) array
            Frequencies of analysis in Hz.

        Returns
        -------
        kappa : (N,) complex-array
            Complex acoustic wavenumber.

        z : (N,) complex-array
            Complex acoustic impedance.

        mach : (N,) complex-array
            Complex mach number.
        """
        omega = 2 * pi * frequencies
        c0 = self.speed_of_sound_corrected()
        rho_0 = self.fluid.density
        kappa_real = omega/c0
        di = self.cross_section.inner_diameter
        radius = di / 2
        if self.element_type == 'undamped mean flow':
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

            # TODO: prt warning por pr<0.5
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

    def _update_pp_impedance(self, frequencies, nonlinear_effect):
        """
        Auxiliary method used to update the perforated plate impedance model.

        Parameters
        ----------
        frequencies : (N,) array
            Frequencies of analysis in Hz.
            
        nonlinear_effect : bool
            If true, include nonlinear effect formulation in the analysis. This leads to a iterative process that may time a while to conclude.
        """
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
            u_n = np.abs(self.delta_pressure/self.pp_impedance)
        else:
            u_n = 0
        self.u_n = u_n

        if self.perforated_plate.type == 0:
            theta_rad = self.perforated_plate.radiation_impedance(k)

            #TODO: use mach number as input when the formulation is validated
            # theta_flow = self.perforated_plate.flow_impedance(0) 
            theta_flow = 0

            #TODO: use mach number as input when the formulation is validated
            if self.perforated_plate.bias_effect:
                theta_g = self.perforated_plate.bias_impedance(0)
            else:
                theta_g = 0
            
            if nonlinear_effect:
                theta_nl = self.perforated_plate.nonlinear_impedance(c, u_n)
            else:
                theta_nl = 0

            if isinstance(self.perforated_plate.dimensionless_impedance, (complex, np.ndarray)):
                theta_user = self.perforated_plate.dimensionless_impedance
            else:
                theta_user = 0

            k_viscous = np.sqrt(-1j * omega * rho / mu)
            mean_viscous_field = - j2j0(k_viscous*d/2)
            
            k_thermal = np.sqrt(-1j * omega * rho * c_p / kappa)
            mean_thermal_field = (gamma + (gamma - 1) *j2j0(k_thermal*d/2)) 

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

    def perforated_plate_matrix(self, frequencies, nonlinear_effect):
        """
        This method computes the Perforated Plate 1D elementary admittance matrix for each frequency of analysis. The setup is done through the element ``perforated_plate`` attribute.

        Parameters
        ----------
        frequencies : (N,) array
            Frequencies of analysis in Hz.
            
        nonlinear_effect : bool
            If true include nonlinear effect formulation in the analysis. This leads to a iterative process that may time a while to conclude.

        Returns
        -------
        (N, 4) array 
            Element's admittance matrix. Each row of the output array ``matrix[i,:]`` may be rewritten to a 2-by-2 element's admittance matrix corresponding to the ``i``-th frequency of analysis ``frequencies[i]``.
        """
        self._update_pp_impedance(frequencies, nonlinear_effect)
        admittance = self.area_fluid / self.pp_impedance
        
        return np.c_[- admittance, admittance, admittance, - admittance]

    def radiation_impedance(self, kappa_complex, impedance_complex):
        """
        This method attributes the radiation impedance to the element nodes according to the `anechoic`, `flanged`, and `unflanged` prescription.

        Parameters
        ----------
        kappa : (N,) complex-array
            Complex acoustic wavenumber.

        z : (N,) complex-array
            Complex acoustic impedance.
        """
        if self.first_node.radiation_impedance_type == 0:
            self.first_node.radiation_impedance = impedance_complex + 0j
        elif self.first_node.radiation_impedance_type == 1:
            self.first_node.radiation_impedance = self._unflanged_termination_impedance(kappa_complex, impedance_complex)
        elif self.first_node.radiation_impedance_type == 2:
            self.first_node.radiation_impedance = self._flanged_termination_impedance(kappa_complex, impedance_complex)

        if self.last_node.radiation_impedance_type == 0:
            self.last_node.radiation_impedance = impedance_complex + 0j
        elif self.last_node.radiation_impedance_type == 1:
            self.last_node.radiation_impedance = self._unflanged_termination_impedance(kappa_complex, impedance_complex)
        elif self.last_node.radiation_impedance_type == 2:
            self.last_node.radiation_impedance = self._flanged_termination_impedance(kappa_complex, impedance_complex)

    def _unflanged_termination_impedance(self, kappa_complex, impedance_complex):
        """
        This method computes the radiation impedance according to the `unflanged` model.

        Parameters
        ----------
        kappa_complex : (N,) complex-array
            Complex acoustic wavenumber.

        impedance_complex : (N,) complex-array
            Complex acoustic impedance.

        Returns
        -------
        (N,) array
            Unflanged pipe termination impedance.
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

        return impedance_complex * (1 + aux_2)/(1 - aux_2) +0j

    def _flanged_termination_impedance(self, kappa_complex, impedance_complex):
        """
        This method computes the radiation impedance according to the `flanged` model.

        Parameters
        ----------
        kappa_complex : (N,) complex-array
            Complex acoustic wavenumber.

        impedance_complex : (N,) complex-array
            Complex acoustic impedance.

        Returns
        -------
        (N,) array
            Flanged pipe termination impedance.
        """
        radius = self.cross_section.inner_radius
        kr = kappa_complex * radius
        return impedance_complex * (1 - jv(1,2*kr)/ kr  + 1j * H1(2*kr)/ kr  ) +0j 

    def fem_1d_matrix(self, length_correction=0):
        """
        This method computes the FEM acoustic 1D elementary matrices. It allows to include the length correction due to acoustic discontinuities (`loop`, `expansion`, `side branch`). The FEM is not compatible with any damping model.

        .. note::
            In OpenPulse, this formulation is only used to evaluate the acoustic modal analysis.

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

        Ke = self.area_fluid/(rho*length) * np.array([[1,-1],[-1,1]])
        Me = self.area_fluid * length / (6*rho*c**2) * np.array([[2,1],[1,2]]) 
        
        return Ke, Me