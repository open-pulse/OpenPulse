from enum import IntEnum

import numpy as np
from numpy import pi, sqrt
from scipy.optimize import fsolve, root
from scipy.special import hankel1, jv

from pulse.model import RadiationImpedanceType
from pulse.model.elements.element_attributes import ElementAttributes


class ElementLengthCorrection(IntEnum):
    EXPANSION = 0
    SIDE_BRANCH = 1
    LOOP = 2


class AcousticCalculator:
    """
        This class is used to compute a set of acoustic parameters, such as
        impedance, wavenumber, corrected speed of sound, Mach number, among others.
    """
    def __init__(self, element_attributes: ElementAttributes, **kwargs):

        self.element_attributes = element_attributes

    @property
    def fluid(self):
        return self.element_attributes.fluid

    @property
    def material(self):
        return self.element_attributes.material

    @property
    def acoustic_element_type(self):
        return self.element_attributes.acoustic_element_type

    @property
    def cross_section(self):
        return self.element_attributes.cross_section

    @property
    def length(self):
        return self.element_attributes.length

    @property
    def volumetric_flow_rate(self):
        return self.element_attributes.volumetric_flow_rate

    @property
    def area_fluid(self):
        return self.element_attributes.cross_section.area_fluid

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
        return self.volumetric_flow_rate / (self.speed_of_sound_corrected() * self.area_fluid)

    def wave_number(self, omega: np.ndarray):
        """
        This method returns the element's wave number based on its fluid.

        Returns
        -------
        float
            The wave number.
        """
        return omega / self.speed_of_sound_corrected()

    def speed_of_sound_corrected(self):
        """
        This method returns the corrected speed of sound due to the mechanical compliance of the pipe wall.

        Returns
        -------
        float
            Speed of sound in the element.
            
        References
        ----------
        .. T. C. Lin and G. W. Morgan, "Wave Propagation through Fluid Contained in a Cylindrical, 
        Elastic Shell," The Journal of the Acoustical Society of America 28:6, 1165-1176, 1956.
        """
        if self.cross_section.section_type_label == 'expansion_joint':
            return self.fluid.speed_of_sound

        else:
            D_in = self.cross_section.inner_diameter
            K_0 = self.fluid.bulk_modulus
            E = self.material.elasticity_modulus
            t = self.cross_section.thickness
            factor = (D_in * K_0) / (E * t)
            return (1 / sqrt(1 + factor)) * self.fluid.speed_of_sound

    def get_wave_number_and_acoustic_impedance(self, frequencies: np.ndarray):
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

        if self.acoustic_element_type == 'undamped':
            return self.get_undamped_wave_number_and_acoustic_impedance(frequencies)

        elif self.acoustic_element_type == 'proportional':
            return self.get_proportional_wave_number_and_acoustic_impedance(frequencies)

        elif self.acoustic_element_type == 'wide_duct':
            return self.get_wide_duct_wave_number_and_acoustic_impedance(frequencies)

        elif self.acoustic_element_type == 'LRF_fluid_equivalent':
            return self.get_LRF_fluid_equivalent_wave_number_and_acoustic_impedance(frequencies)

        elif self.acoustic_element_type == "damped_liquid":
            return self.get_damped_liquid_wave_number_and_acoustic_impedance(frequencies)

    def get_undamped_wave_number_and_acoustic_impedance(self, frequencies: np.ndarray):

        omega = 2 * np.pi * frequencies
        kappa_real = self.wave_number(omega)

        radius = self.cross_section.inner_radius

        rho_0 = self.fluid.density
        c_0 = self.speed_of_sound_corrected()       
        Z_0 = c_0 * rho_0

        aux = np.real(kappa_real * radius) > 1.84118
        if np.any(aux):
            self.flag_plane_wave = True
            self.max_valid_freq = np.min(frequencies[aux])

        return kappa_real, Z_0

    def get_proportional_wave_number_and_acoustic_impedance(self, frequencies: np.ndarray):

        omega = 2 * np.pi * frequencies
        kappa_real = self.wave_number(omega)
        radius = self.cross_section.inner_radius

        rho_0 = self.fluid.density
        c_0 = self.speed_of_sound_corrected()
        Z_0 = c_0 * rho_0

        hysteresis = 1 - 1j * self.element_attributes.proportional_damping

        kappa_complex = kappa_real * hysteresis
        impedance_complex = Z_0 * hysteresis

        aux = np.real(kappa_real * radius) > 1.84118
        if np.any(aux):
            self.flag_plane_wave = True
            self.max_valid_freq = np.min(frequencies[aux])

        return kappa_complex, impedance_complex

    def get_wide_duct_wave_number_and_acoustic_impedance(self, frequencies: np.ndarray):

        omega = 2 * np.pi * frequencies
        kappa_real = self.wave_number(omega)
        radius = self.cross_section.inner_radius

        rho_0 = self.fluid.density
        c_0 = self.speed_of_sound_corrected()       
        Z_0 = c_0 * rho_0

        nu = self.fluid.kinematic_viscosity
        pr = self.fluid.prandtl
        gamma = self.fluid.isentropic_exponent
        k0 = self.fluid.thermal_conductivity
        c0 = self.speed_of_sound_corrected()

        aux_wd1 = radius < 10*sqrt(2*nu/omega) 
        aux_wd2 = radius < 10*sqrt(2*k0/omega) 
        aux = np.any(np.array([aux_wd1, aux_wd2]), axis=0)

        aux_wd3 = sqrt(2*omega * nu) / c0 > 1 / 10

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

        kappa_complex = kappa_real * const
        impedance_complex = Z_0 * const

        return kappa_complex, impedance_complex

    def get_LRF_fluid_equivalent_wave_number_and_acoustic_impedance(self, frequencies: np.ndarray):

        omega = 2 * np.pi * frequencies
        kappa_real = self.wave_number(omega)

        rho_0 = self.fluid.density
        c_0 = self.speed_of_sound_corrected()       
        Z_0 = c_0 * rho_0

        nu = self.fluid.kinematic_viscosity
        gamma = self.fluid.isentropic_exponent
        alpha = self.fluid.thermal_diffusivity
        radius = self.cross_section.inner_radius

        aux = np.sqrt(2 * np.pi * frequencies)
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
        impedance_complex = Z_0 / np.sqrt(y_t * y_v)

        aux = np.real(kappa_complex * radius) > 1.84118
        if np.any(aux):
            self.flag_plane_wave = True
            self.max_valid_freq = np.min([np.min(frequencies[aux]), self.max_valid_freq])

        return kappa_complex, impedance_complex

    def get_damped_liquid_wave_number_and_acoustic_impedance(self, frequencies: np.ndarray):

        omega = 2 * np.pi * frequencies
        kappa_real = self.wave_number(omega)

        rho_0 = self.fluid.density
        mu = self.fluid.dynamic_viscosity
        v = mu / rho_0

        Q = self.volumetric_flow_rate
        if Q == 0:
            # c_0 = self.fluid.speed_of_sound
            c_0 = self.speed_of_sound_corrected()
            Z_0 = rho_0 * c_0
            return kappa_real, Z_0

        A = self.cross_section.area_fluid
        d = self.cross_section.inner_diameter
        u = Q / A

        Re = u * d * rho_0 / mu

        # Colebrook equation for determining the Darcy friction factor
        def colebrook_equation(x):
            return 2 * np.log10(Re * (x**0.5)) - 0.8 - (1 / (x**0.5))

        # use Haaland approximation for Colebrook equation as initial guess value for Darcy friction factor
        x_initial = 1 / ((-1.8 * np.log10(6.9 / Re))**2)

        # Get the Darcy friction factor
        f_d = fsolve(colebrook_equation, x_initial)

        k = np.log10(14.3 / (Re**0.05))
        beta = 0.54 * (v / (d**2)) * (Re**k)

        # shear stress term
        alpha_r = -1j * (f_d * abs(Q) / (omega * d * A)) + (4 / d) * np.sqrt(v / (beta + 1j*omega))

        # viscous elasticity term (neglected due to the high pipe wall stiffness)
        alpha_v = 0.

        # complex wave number
        kappa_complex = kappa_real * np.sqrt(1 + alpha_r) * np.sqrt(1 + alpha_v)

        # complex speed of sound
        c_complex = omega / kappa_complex

        # acoustic impedance
        Z = rho_0 * c_complex

        return kappa_complex, Z

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
        impedance_type : str
            A string or a integer number that represents radiation impedance type.

            anechoic or 0 -> anechoic termination
            flanged or 1 -> flanged termination
            unflanged or 2 -> unflanged termination

        frequencies : float-array
            The frequencies vector of the harmonic analysis.

        Returns
        -------
        array
            Radiation impedance. The array has the same length as frequencies parameter.
        """
        if frequencies is None:
            frequencies = np.array([0], dtype=float)

        if self.acoustic_element_type in ['undamped_mean_flow', 'peters', 'howe']:
            k, z, M = self.get_mean_flow_damping_data(frequencies)
            kappa_complex = k
            impedance_complex = z * (1 - M**2)

        elif self.acoustic_element_type in ['undamped', 'proportional', 'wide_duct', 'LRF_fluid_equivalent', 'damped_liquid']:
            kappa_complex, impedance_complex = self.get_wave_number_and_acoustic_impedance(frequencies)

        elif self.acoustic_element_type == 'LRF full':
            kappa_complex, impedance_complex = self.get_thermoviscous_damping_data(frequencies)

        # the integer numbers ensure the backwards compatibility
        if impedance_type == RadiationImpedanceType.ANECHOIC:
            return impedance_complex + 0j

        elif impedance_type == RadiationImpedanceType.FLANGED:
            return self.flanged_termination_impedance(kappa_complex, impedance_complex)

        elif impedance_type == RadiationImpedanceType.UNFLANGED:
            return self.unflanged_termination_impedance(kappa_complex, impedance_complex)

    def get_mean_flow_damping_data(self, frequencies: np.ndarray):

        omega = 2 * pi * frequencies
        kappa_real = self.wave_number(omega)

        rho_0 = self.fluid.density
        c_0 = self.speed_of_sound_corrected()
        Z_0 = rho_0 * c_0

        di = self.cross_section.inner_diameter
        radius = di / 2

        if self.acoustic_element_type == 'undamped_mean_flow':
            aux = np.real(kappa_real*(1-self.mach**2) * radius) > 1.84118
            if np.any(aux):
                self.flag_plane_wave = True
                self.max_valid_freq = np.min(frequencies[aux])

            return kappa_real, Z_0, self.mach

        elif self.acoustic_element_type == 'howe':
            nu = self.fluid.kinematic_viscosity
            alpha = self.fluid.thermal_diffusivity
            pr = self.fluid.prandtl
            gamma = self.fluid.isentropic_exponent
            U = self.mach * c_0
            Karmank = 0.41

            # TODO: prt warning por p < 0.5
            prt = 0.87

            def transc(x):
                return (U / x - (2.44 * np.log(x * di/(2*nu)) + 2))**2

            # transc = lambda x: (U/x - (2.44 * np.log(x * di/(2*nu)) + 2))**2
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

            aux1 = np.sqrt(2) * (1 - 1j) * np.sqrt(omega * nu) / (c_0 * di)
            aux2_m = np.conj(F1 / (1 - self.mach)**2 + (gamma - 1)* F2 * np.sqrt(alpha / nu))
            aux2_M = np.conj(F1 / (1 + self.mach)**2 + (gamma - 1)* F2 * np.sqrt(alpha / nu))

            kappa_m = 1 / (1 - self.mach) * (kappa_real + aux1 * aux2_m)
            kappa_M = 1 / (1 + self.mach) * (kappa_real + aux1 * aux2_M)

            kappa = (kappa_M + kappa_m)/2
            c = omega / kappa
            z = rho_0 * c
            mach_ef = U / c

            aux = np.real(kappa*(1-mach_ef**2) * radius) > 1.84118
            if np.any(aux):
                self.flag_plane_wave = True
                self.max_valid_freq = np.min(frequencies[aux])

            return kappa, z, mach_ef

        elif self.acoustic_element_type == 'peters':
            nu = self.fluid.kinematic_viscosity
            gamma = self.fluid.isentropic_exponent
            pr = self.fluid.prandtl

            U = self.mach * c_0
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
            mach_ef = U / c

            aux = np.real(kappa*(1-mach_ef**2) * radius) > 1.84118
            if np.any(aux):
                self.flag_plane_wave = True
                self.max_valid_freq = np.min(frequencies[aux])

            return kappa, z, mach_ef
  
    def get_thermoviscous_damping_data(self, frequencies: np.ndarray):

        omega = 2 * pi * frequencies
        rho = self.fluid.density
        nu = self.fluid.kinematic_viscosity
        gamma = self.fluid.isentropic_exponent
        pr = self.fluid.prandtl

        c = self.speed_of_sound_corrected()

        radius = self.cross_section.inner_radius
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
    
    j2/j0 = -1, when z --> /infty.

    Parameters
    -------
    z : array
    """
    mask = np.abs(np.imag(z)) < 700
    value = np.zeros_like(z, dtype = complex)
    value[mask] = jv(2, z[mask]) / jv(0, z[mask])
    value[~mask] = -1
    return value