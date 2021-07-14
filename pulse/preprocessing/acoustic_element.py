from math import sqrt, pi
import numpy as np
from scipy.special import jv, struve
from pulse.preprocessing.node import Node, distance
from pulse.utils import error, info_messages

DOF_PER_NODE = 1
NODES_PER_ELEMENT = 2
DOF_PER_ELEMENT = DOF_PER_NODE * NODES_PER_ELEMENT
ENTRIES_PER_ELEMENT = DOF_PER_ELEMENT ** 2

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

def j2j0(z):
    """
    Auxiliary function to compute the ratio between the Bessel functions J2 and J0. When the imaginary part of input z reaches 700, the following syntonic approximation is used:
    
    ``j2/j0 = -1``, when ``z --> \infty.``

    Parameters
    -------
    z : array
    """
    mask = np.abs(np.imag(z))<700
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

    element_type : str, ['undamped', 'hysteretic', 'wide-duct', 'LRF fluid equivalent', 'LRF full'], optional
        Element type
        Default is 'undamped'.

    hysteretic_damping : float, optional
        Hysteretic damping coefficient 
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
        Acoustic length correction due to acoustic discontinuities. The prescription is done through the following labeling:
        None: disable
        0 : expansion
        1 : side_branch
        2 : loop 
        Default is None.
    """
    def __init__(self, first_node, last_node, index, **kwargs):
        self.first_node = first_node
        self.last_node = last_node
        self.index = index
        self.element_type = kwargs.get('element_type', 'undamped')
        self.hysteretic_damping = kwargs.get('hysteretic_damping', None)
        self.material = kwargs.get('material', None)
        self.fluid = kwargs.get('fluid', None)   
        self.cross_section = kwargs.get('cross_section', None)
        self.loaded_pressure = kwargs.get('loaded_forces', np.zeros(DOF_PER_NODE))
        self.acoustic_length_correction = kwargs.get('acoustic_length_correction', None)

        self.element_type = kwargs.get('element_type', 'undamped')

        self.flag_plane_wave = False
        self.flag_wide_duct = False
        self.flag_lrf_fluid_eq = False
        self.flag_lrf_full = False
        self.flag_unflanged_radiation_impedance = False

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
        return self.fluid.impedance / self.cross_section.area_fluid

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
        This method returns the rows' and columns' indexes that place the element's matrices in the global matrices. The created lists are  such that the method is useful to generate sparse matrices.

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
        if self.cross_section.section_label == 'expansion joint':
            return self.fluid.speed_of_sound
        else:
            factor = self.cross_section.inner_diameter * self.fluid.bulk_modulus / (self.material.young_modulus * self.cross_section.thickness)
            return (1 / sqrt(1 + factor))*self.fluid.speed_of_sound
        
    def matrix(self, frequencies, length_correction=0):
        """
        This method returns the element's admittance matrix for each frequency of analysis according to the element type. The method allows to include the length correction due to acoustic discontinuities (loop, expansion, side branch).

        Parameters
        ----------
        frequencies : array
            Frequencies of analysis in Hz.

        length_correction : float, optional
            Element length correction to be added into the element length.

        Returns
        -------
        2D array
            Element's admittance matrix. Each row of the output array is an element's admittance matrix corresponding to a frequency of analysis.
        """
        if self.element_type in ['undamped','hysteretic','wide-duct','LRF fluid equivalent']:
            return self.fetm_1d_matrix(frequencies, length_correction)
        elif self.element_type == 'LRF full':
            return self.lrf_thermoviscous_matrix(frequencies, length_correction)  
    
    def fetm_1d_matrix(self, frequencies, length_correction = 0):
        """
        This method returns the FETM 1D element's admittance matrix for each frequency of analysis. The method allows to include the length correction due to  acoustic discontinuities (loop, expansion, side branch). The damping models compatible with FETM 1D are Undamped, Hysteretic, Wide-duct, and LRF fluid equivalent.

        Parameters
        ----------
        frequencies : array
            Frequencies of analysis in Hertz.
            
        length_correction : float, optional
            Element length correction to be added into the element length.

        Returns
        -------
        2D array
            Element's admittance matrix. Each row of the output array is an element's admittance matrix corresponding to a frequency of analysis.
        """
        ones = np.ones(len(frequencies), dtype='float64')
        kappa_complex, impedance_complex = self._fetm_damping_models(frequencies)
        self.radiation_impedance(kappa_complex, impedance_complex)
        
        area_fluid = self.cross_section.area_fluid

        kappaLe = kappa_complex * (self.length + length_correction)
        sine = np.sin(kappaLe)
        cossine = np.cos(kappaLe)
        matrix = ((area_fluid*1j/(sine*impedance_complex))*np.array([-cossine, ones, ones, -cossine])).T

        return matrix

    def _fetm_damping_models(self, frequencies):
        """
        This method returns wavenumber and fluid impedance for the FETM 1D theory according to the element's damping model (element type). The damping models compatible with FETM 1D are Undamped, Hysteretic, Wide-duct, and LRF fluid equivalent.

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
        omega = 2 * pi * frequencies
        c0 = self.speed_of_sound_corrected()
        rho_0 = self.fluid.density
        kappa_real = omega/c0
        radius = self.cross_section.inner_diameter / 2
        if self.element_type == 'undamped':
            criterion = np.real(kappa_real[-1] * radius) > 3.83
            if criterion:
                self.flag_plane_wave = True
            return kappa_real, c0 * rho_0

        elif self.element_type == 'hysteretic':
            hysteresis = (1 - 1j*self.hysteretic_damping)
            kappa_complex = kappa_real * hysteresis
            impedance_complex = c0 * rho_0 * hysteresis
            
            criterion = np.real(kappa_real[-1] * radius) > 3.83
            if criterion:
                self.flag_plane_wave = True
            return kappa_complex, impedance_complex

        elif self.element_type == 'wide-duct':
            nu = self.fluid.kinematic_viscosity
            pr = self.fluid.prandtl
            gamma = self.fluid.isentropic_exponent
            k = self.fluid.thermal_conductivity
            
            omega_min = max([min(omega), 1])
            omega_max = max(omega)

            criterion_1 = radius < 10 * sqrt(2  * nu / omega_min)
            criterion_2 = radius < 10 * sqrt(2  * k / omega_min)
            criterion_3 = sqrt(omega_max * nu / c0**2) > 0.1
            if np.any(np.array([criterion_1, criterion_2, criterion_3])):
                self.flag_wide_duct = True

            criterion = np.real(kappa_real[-1] * radius) > 3.83
            if criterion:
                self.flag_plane_wave = True

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

            criterion_1 = np.abs(kappa_t[-1] / kappa_real[-1]) < 10
            criterion_2 = np.abs(kappa_v[-1] / kappa_real[-1]) < 10
            if np.any(np.array([criterion_1, criterion_2])):
                self.flag_lrf_fluid_eq = True

            y_v = - j2j0(kappa_v * radius)
            y_t =   j2j0(kappa_t * radius) * (gamma-1) + gamma

            kappa_complex = kappa_real * np.sqrt(y_t / y_v)
            impedance_complex = c0 * rho_0 / np.sqrt(y_t * y_v)

            criterion = np.real(kappa_real[-1] * radius)  > 1
            if criterion:
                self.flag_plane_wave = True

            return kappa_complex, impedance_complex

    def lrf_thermoviscous_matrix(self, frequencies, length_correction=0):
        """
        This method returns the LRF thermoviscous 1D elementary admittance matrix for each frequency of analysis. The method allows to include the length correction due to acoustic discontinuities (loop, expansion, side branch).

        Parameters
        ----------
        frequencies : array
            Frequencies of analysis in Hertz.
            
        length_correction : float, optional
            Element length correction to be added into the element length.

        Returns
        -------
        2D array
            Elementary admittance matrix. Each row of the output array is an element admittance matrix corresponding to a frequency of analysis.
        """
        ones = np.ones(len(frequencies), dtype='float64')
        omega = 2 * pi * frequencies
        rho = self.fluid.density
        mu = self.fluid.dynamic_viscosity
        gamma = self.fluid.isentropic_exponent
        pr = self.fluid.prandtl
        area = self.cross_section.area_fluid
        c = self.speed_of_sound_corrected()
        length = self.length + length_correction
        radius = self.cross_section.inner_diameter / 2
        kappa_real = omega / c

        s = radius * np.sqrt(rho * omega / mu)
        sigma = sqrt(pr)

        criterion_1 = kappa_real[-1] * radius / s[-1] > 0.1
        criterion_2 = s[0]< 4
        if np.any(np.array([criterion_1, criterion_2])):
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

        matrix = - ((area * G / (impedance_complex * sinh)) * np.array([cosh, -ones, -ones, cosh])).T

        criterion = np.real(kappa_complex[-1] * radius) > 1
        if criterion:
            self.flag_plane_wave = True
        return matrix  

    def radiation_impedance(self, kappa_complex, impedance_complex):
        """
        This method update the radiation impedance attributed to the element nodes according to the anechoic, flanged, and unflanged prescription.

        Parameters
        -------
        kappa : complex-array
            Complex wavenumber.

        z : complex-array
            Complex impedance.
        """
        radius = self.cross_section.inner_diameter / 2
        if self.first_node.radiation_impedance_type == 0:
            self.first_node.radiation_impedance = impedance_complex + 0j
        elif self.first_node.radiation_impedance_type == 1:
            self.first_node.radiation_impedance = self.unflanged_termination_impedance(kappa_complex, impedance_complex)
        elif self.first_node.radiation_impedance_type == 2:
            self.first_node.radiation_impedance = self.flanged_termination_impedance(kappa_complex, impedance_complex)

        if self.last_node.radiation_impedance_type == 0:
            self.last_node.radiation_impedance = impedance_complex + 0j
        elif self.last_node.radiation_impedance_type == 1:
            self.last_node.radiation_impedance = self.unflanged_termination_impedance(kappa_complex, impedance_complex)
        elif self.last_node.radiation_impedance_type == 2:
            self.last_node.radiation_impedance = self.flanged_termination_impedance(kappa_complex, impedance_complex)

    def unflanged_termination_impedance(self, kappa_complex, impedance_complex):
        """
        This method updates the radiation impedance attributed to the element nodes according to the unflanged prescription.

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

        if np.any(kr_great_t_1 > 3.83):
            self.flag_unflanged_radiation_impedance = True

        aux_1_2 = np.abs(np.sqrt(pi * kr_great_t_1) * np.exp(-kr_great_t_1) * (1 + 3 / (32 * kr_great_t_1**2)))
        aux_1 = np.r_[aux_1_1, aux_1_2]
        aux_2 = - aux_1 * np.exp( -2j * kr * poly_function(kr))

        return impedance_complex * (1 + aux_2)/(1 - aux_2) +0j

    def flanged_termination_impedance(self, kappa_complex, impedance_complex):
        """
        This method updates the radiation impedance attributed to the element nodes according to the flanged prescription.

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
        return impedance_complex * (1 - jv(1,2*kr)/ kr  + 1j * struve(1,2*np.real(kr))/ kr  ) +0j 

    def fem_1d_matrix(self, length_correction=0 ):
        """
        This method returns the FEM acoustic 1D elementary matrices. The method allows to include the length correction due to  acoustic discontinuities (loop, expansion, side branch). The FEM is not compatible with any damping model.
        
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
        area = self.cross_section.area_fluid
        c = self.speed_of_sound_corrected()

        Ke = area/(rho*length) * np.array([[1,-1],[-1,1]])
        Me = area * length / (6*rho*c**2) * np.array([[2,1],[1,2]]) 
        return Ke, Me