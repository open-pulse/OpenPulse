from enum import IntEnum

import numpy as np
from numpy import pi, sqrt
from scipy.optimize import root
from scipy.special import hankel1, jv

from pulse.model.elements.acoustic.acoustic_calculator import AcousticCalculator
from pulse.model.data_classes.model_setup_data_classes import Foks_function, PerforatedPlateFormulation
from pulse.model.elements.element_attributes import ElementAttributes
from pulse.model.properties.fluid import Fluid

DOF_PER_NODE = 1
NODES_PER_ELEMENT = 2
DOF_PER_ELEMENT = DOF_PER_NODE * NODES_PER_ELEMENT
ENTRIES_PER_ELEMENT = DOF_PER_ELEMENT ** 2


class ElementLengthCorrection(IntEnum):
    EXPANSION = 0
    SIDE_BRANCH = 1
    LOOP = 2


class AcousticElement(AcousticCalculator):
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

    """
    def __init__(self, element_attributes: ElementAttributes, **kwargs):
        super().__init__(element_attributes, **kwargs)

        self.first_node = element_attributes.first_node
        self.last_node = element_attributes.last_node

        self.reset()

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


    def fem_elementary_matrices(self, length: float | None = None, length_correction: float = 0):
        pass

    def fem_elementary_link_matrices(self, length: float, length_correction: float = 0):
        pass
    
    def fetm_admittance_matrix(self, frequencies: np.ndarray, length_correction: float = 0):
        pass

    def fetm_admittance_matrix_various(self, frequencies: np.ndarray, length_correction: float = 0):
        pass

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
        global_dof[:DOF_PER_NODE] = self.first_node.index
        global_dof[DOF_PER_NODE:] = self.last_node.index
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

    def update_pp_impedance(self, frequencies):

        if frequencies[0]==0:
            frequencies[0] = float(1e-4)

        if not isinstance(self.fluid, Fluid):
            self.pp_impedance = None
            return

        # Fluid physical quantities
        rho = self.fluid.density
        mu = self.fluid.dynamic_viscosity
        gamma = self.fluid.isentropic_exponent
        kappa = self.fluid.thermal_conductivity
        c_p = self.fluid.specific_heat_Cp
        c = self.speed_of_sound_corrected()
        z = self.fluid.impedance

        # Perforated plate physical quantities
        perforated_plate_data = self.element_attributes.perforated_plate_data

        d = perforated_plate_data.hole_diameter
        t = perforated_plate_data.plate_thickness
        sigma = perforated_plate_data.area_porosity
        t_foks = t + perforated_plate_data.foks_delta
        c_l = perforated_plate_data.discharge_coefficient

        omega = 2 * pi * frequencies
        k = omega / c

        if isinstance(self.pp_impedance, np.ndarray):
            u_n = np.abs(self.delta_pressure / self.pp_impedance)
        else:
            u_n = 0

        self.u_n = u_n

        if perforated_plate_data.type == PerforatedPlateFormulation.OPENPULSE:

            theta_rad = perforated_plate_data.radiation_impedance(k)

            #TODO: use mach number as input when the formulation is validated
            # theta_flow = perforated_plate_data.flow_impedance(0) 
            theta_flow = 0

            #TODO: use mach number as input when the formulation is validated
            if perforated_plate_data.bias_flow_effects:
                theta_g = perforated_plate_data.bias_impedance(0)
            else:
                theta_g = 0

            if perforated_plate_data.nonlinear_effects:
                theta_nl = perforated_plate_data.nonlinear_impedance(c, u_n)
            else:
                theta_nl = 0

            if isinstance(perforated_plate_data.dimensionless_impedance, (complex, np.ndarray)):
                theta_user = perforated_plate_data.dimensionless_impedance
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

        elif perforated_plate_data.type == PerforatedPlateFormulation.MELLING: # Melling's model
            nu = self.fluid.kinematic_viscosity

            k_stokes = np.sqrt( -1j*omega / nu)
            k_ef = np.sqrt( -1j*omega / (2.179 * nu))
            foks_porosity = Foks_function(np.sqrt(sigma))

            xi_l = 1j*k/(sigma*c_l)*( t / f_function(k_ef * d/2) + 8* d/(3*pi * f_function(k_stokes * d/2))*foks_porosity )
            xi_nl = 4 * u_n * (1-sigma**2)/(3*pi*c*(sigma*c_l)**2)
            z_orif = - (xi_l + xi_nl) * z 

        # Common pipe perforated plate impedance
        if perforated_plate_data.type == PerforatedPlateFormulation.COMMON_PIPE:
            self.pp_impedance = self.impedance

        # OpenPulse and Melling perforated plate impedance
        else:
            self.pp_impedance = z_orif

    def perforated_plate_matrix(self, frequencies):
        self.update_pp_impedance(frequencies)
        admittance = self.area_fluid / self.pp_impedance       
        return np.c_[- admittance, admittance, admittance, - admittance]
    
    def update_delta_pressure(self, delta_pressure):
        self.delta_pressure = delta_pressure

    def get_mean_flow_damping_data(self, frequencies):

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
