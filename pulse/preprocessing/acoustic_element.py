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
    a = np.array([0.6110035017201978, 0.028476407937161143, -0.26371506544764184, 0.24363292796929378, -0.11627424586622058, 0.027516286514019005, -0.00254838451051438])
    b = np.arange(7)
    x = x.reshape(-1, 1) @ np.ones([1,7])
    return (x**b ) @ a

def unflanged_termination_impedance(kappa_complex, pipe_radius, impedance_complex):
    kr = kappa_complex * pipe_radius
    mask = kr<=1
    
    kr_less_t_1 = kr[mask]
    gamma = np.exp(0.5772)
    aux_1_1 = np.abs(np.exp((-kr_less_t_1**2)/2) * (1 + kr_less_t_1**4 / 6 * np.log(1 / (gamma * kr_less_t_1) + 19/12)))

    kr_great_t_1 = kr[~mask]
    if np.any(kr_great_t_1 > 3.83):
        info_messages("The unflanged radiation impedance model is out of \nits validity frequency range.")
    aux_1_2 = np.abs(np.sqrt(pi * kr_great_t_1) * np.exp(-kr_great_t_1) * (1 + 3 / (32 * kr_great_t_1**2)))

    aux_1 = np.r_[aux_1_1, aux_1_2]

    aux_2 = - aux_1 * np.exp( -2j * kr * poly_function(kr))

    return impedance_complex * (1 + aux_2)/(1 - aux_2) +0j

def flanged_termination_impedance(kappa_complex, pipe_radius, impedance_complex):
    kr = kappa_complex * pipe_radius
    return impedance_complex * (1 - jv(1,2*kr)/ kr  + 1j * struve(1,2*kr)/ kr  ) +0j

def j2j0(z):
    mask = np.abs(np.imag(z))<700
    value = np.zeros_like(z, dtype = complex)
    value[mask] = jv(2, z[mask]) / jv(0, z[mask])
    value[~mask] = -1
    return value

class AcousticElement:
    def __init__(self, first_node, last_node, index, **kwargs):
        self.first_node = first_node
        self.last_node = last_node
        self.index = index
        self.element_type = kwargs.get('element_type', 'dampingless')
        self.hysteretic_damping = kwargs.get('hysteretic_damping', None)
        self.material = kwargs.get('material', None)
        self.fluid = kwargs.get('fluid', None)   
        self.cross_section = kwargs.get('cross_section', None)
        self.loaded_pressure = kwargs.get('loaded_forces', np.zeros(DOF_PER_NODE))
        self.acoustic_length_correction = kwargs.get('acoustic_length_correction', None)
        # 0 -> expansion
        # 1 -> side_branch
        # 2 -> loop (to be defined. Use expansion insteed)

        self.element_type = kwargs.get('element_type', 0)
        # index: 0 - Dampingless
        # index: 1 - Hysteretic
        # index: 2 - Wide-duct
        # index: 3 - LRF fluid equivalent
        # index: 4 - LRF full
        
        self.damping_model = kwargs.get('damping_model', 0)
        # for FETM 1D element type:
        # 0 -> dampingless
        # 1 -> hysteric damping
        # 2 -> Wide duct attenuation model
        # 3 -> Equivalent fluid LRF thermoviscous model

    @property
    def length(self):
        return distance(self.first_node, self.last_node) 

    @property
    def orientation(self):
        return self.last_node.coordinates - self.first_node.coordinates

    @property
    def impedance(self):
        ''' Returns acoustic impedance as a ratio between specific_impedance and area '''
        return self.fluid.impedance / self.cross_section.area_fluid

    @property
    def global_dof(self):
        global_dof = np.zeros(DOF_PER_ELEMENT, dtype=int)
        global_dof[:DOF_PER_NODE] = self.first_node.global_index
        global_dof[DOF_PER_NODE:] = self.last_node.global_index
        return global_dof

    def global_matrix_indexes(self):
        rows = self.global_dof.reshape(DOF_PER_ELEMENT, 1) @ np.ones((1, DOF_PER_ELEMENT))
        cols = rows.T
        return rows, cols

    def speed_of_sound_corrected(self):
        factor = self.cross_section.internal_diameter * self.fluid.bulk_modulus / (self.material.young_modulus * self.cross_section.thickness)
        return (1 / sqrt(1 + factor))*self.fluid.speed_of_sound
        
    def matrix(self, frequencies, ones, length_correction=0):
        if self.element_type in ['dampingless','hysteretic','wide-duct','LRF fluid equivalent']:
            return self.fetm_1d_matrix(frequencies, ones, length_correction)
        elif self.element_type == 'LRF full':
            return self.lrf_thermoviscous_matrix(frequencies, ones, length_correction)

    def lrf_thermoviscous_matrix(self, frequencies, ones, length_correction=0):
        omega = 2 * pi * frequencies
        rho = self.fluid.density
        mu = self.fluid.dynamic_viscosity
        gamma = self.fluid.isentropic_exponent
        pr = self.fluid.prandtl
        area = self.cross_section.area_fluid
        c = self.speed_of_sound_corrected()
        length = self.length + length_correction
        radius = self.cross_section.internal_diameter / 2

        s = radius * np.sqrt(rho * omega / mu)
        sigma = sqrt(pr)

        aux1 = j2j0(1j**(3/2) * s * sigma)
        aux2 = j2j0(1j**(3/2) * s)
        
        n = 1 + aux1 * (gamma - 1)/gamma

        T = np.sqrt( gamma * n / aux2 )

        kappa_complex = T * omega / c
        impedance_complex = c * rho * T
        self.radiation_impedance(kappa_complex, impedance_complex)

        G = - 1j * gamma * n / T

        sinh = np.sinh(kappa_complex * length)
        cosh = np.cosh(kappa_complex * length)

        matrix = - ((area * G / (impedance_complex * sinh)) * np.array([cosh, -ones, -ones, cosh])).T
        return matrix    
    
    def fetm_1d_matrix(self, frequencies, ones, length_correction = 0):
        omega = 2 * pi * frequencies
        kappa_complex, impedance_complex = self.fetm_damping_models(omega)
        
        area_fluid = self.cross_section.area_fluid

        kappaLe = kappa_complex * (self.length + length_correction)
        sine = np.sin(kappaLe)
        cossine = np.cos(kappaLe)
        matrix = ((area_fluid*1j/(sine*impedance_complex))*np.array([-cossine, ones, ones, -cossine])).T

        self.radiation_impedance(kappa_complex, impedance_complex)
        return matrix

    def fetm_damping_models(self, omega):
        c0 = self.speed_of_sound_corrected()
        rho_0 = self.fluid.density
        kappa_real = omega/c0
        if self.element_type == 'dampingless':
            return kappa_real, c0 * rho_0

        elif self.element_type == 'hysteretic':
            hysteresis = (1 - 1j*self.hysteretic_damping)
            kappa_complex = kappa_real * hysteresis
            impedance_complex = c0 * rho_0 * hysteresis
            return kappa_complex, impedance_complex

        elif self.element_type == 'wide-duct':
            nu = self.fluid.kinematic_viscosity
            pr = self.fluid.prandtl
            gamma = self.fluid.isentropic_exponent
            k = self.fluid.thermal_conductivity
            radius = self.cross_section.internal_diameter / 2
            
            omega_min = min(omega)
            omega_max = max(omega)

            criterion_1 = radius > 0.1 * sqrt(2  * nu / omega_min)
            criterion_2 = radius > 0.1 * sqrt(2  * k / omega_min)
            criterion_3 = sqrt(omega_max * nu / c0**2) > 0.1
            if np.any([criterion_1, criterion_2, criterion_3]):
                pass
            #     info_messages("Verification.")

            const = 1 - 1j* np.sqrt(nu/(2*omega)) * ((1 + (gamma-1)/sqrt(pr))/radius)

            kappa_complex = kappa_real*const
            impedance_complex = rho_0*c0*const
            return kappa_complex, impedance_complex

        elif self.element_type == 'LRF fluid equivalent':
            nu = self.fluid.kinematic_viscosity
            gamma = self.fluid.isentropic_exponent
            alpha = self.fluid.thermal_diffusivity
            radius = self.cross_section.internal_diameter / 2

            aux = np.sqrt(omega)
            kappa_v = aux * np.sqrt(-1j / nu)
            kappa_t = aux * np.sqrt(-1j / alpha)

            y_v = - j2j0(kappa_v * radius)
            y_t =   j2j0(kappa_t * radius) * (gamma-1) + gamma

            kappa_complex = kappa_real * np.sqrt(y_t / y_v)
            impedance_complex = c0 * rho_0 / np.sqrt(y_t * y_v)

            return kappa_complex, impedance_complex

    def radiation_impedance(self, kappa_complex, impedance_complex):
        radius = self.cross_section.internal_diameter / 2
        if self.first_node.radiation_impedance_type == 0:
            self.first_node.radiation_impedance = impedance_complex + 0j
        elif self.first_node.radiation_impedance_type == 1:
            self.first_node.radiation_impedance = unflanged_termination_impedance(kappa_complex, radius, impedance_complex)
        elif self.first_node.radiation_impedance_type == 2:
            self.first_node.radiation_impedance = flanged_termination_impedance(kappa_complex, radius, impedance_complex)

        if self.last_node.radiation_impedance_type == 0:
            self.last_node.radiation_impedance = impedance_complex + 0j
        elif self.last_node.radiation_impedance_type == 1:
            self.last_node.radiation_impedance = unflanged_termination_impedance(kappa_complex, radius, impedance_complex)
        elif self.last_node.radiation_impedance_type == 2:
            self.last_node.radiation_impedance = flanged_termination_impedance(kappa_complex, radius, impedance_complex)
    
    def fem_1d_matrix(self, length_correction=0 ):
        length = self.length + length_correction
        rho = self.fluid.density
        area = self.cross_section.area_fluid
        c = self.speed_of_sound_corrected()

        Ke = area/(rho*length) * np.array([[1,-1],[-1,1]])
        Me = area * length / (6*rho*c**2) * np.array([[2,1],[1,2]]) 
        return Ke, Me