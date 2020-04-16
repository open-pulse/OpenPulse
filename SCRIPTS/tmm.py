import numpy as np

from math import pi, cos, sin

class Gas:
    def __init__(self, density, sound_velocity):
        self.density = density
        self.sound_velocity = sound_velocity
    
    @property
    def impedance(self):
        return self.density * self.sound_velocity

class Tube:
    def __init__(self, length, D_external, thickness, number_elements):
        self.length = length
        self.D_external = D_external
        self.thickness = thickness
        self.number_elements = number_elements

    @property
    def D_internal(self):
        return self.D_external - 2 * self.thickness

    @property
    def radius_internal(self):
        return self.D_internal / 2

    @property
    def area_internal(self):
        return self.D_internal**2 * pi/4


class TMM:
    def __init__(self, gas, tube):
        self.gas = gas
        self.tube = tube
    
    def section_impedance(self):
        area = self.tube.area_internal
        fluid_impedance = self.gas.impedance
        return fluid_impedance / area
    
    @staticmethod
    def end_correction(outer_radius):
        return 0.6133 * outer_radius

    def terminal_impedance(self, wave_number, outer_radius):
        aux_vector = self.gas.impedance / 4 * wave_number 
        end_correction = TMM.end_correction(outer_radius)

        return aux_vector * (outer_radius**2 + 1j*end_correction)

    @staticmethod
    def connect_matrix():
        matrix = np.array([[1,0,-1,0],
                           [0,1,0,-1]])
        return matrix

    def elementar_matrix(self, wave_number, x):
        aux = wave_number * x
        Z = self.section_impedance()
        transfer_element = np.array([[cos(aux), -1j / Z * sin(aux)],
                                     [-1j * Z * sin(aux), cos(aux)]])
        return np.c_[transfer_element, - np.eye(2)]


#%% gas properties

sound_velocity = 1149.4 / 3.281 #[m/s]
density = 0.0482/0.00194 # [kg/m³]
gas = Gas(density, sound_velocity)
#%% Duct definition

# The information can be taken from tube / section_fem class
D_external = 0.154 #[m]
thickness = 0.01 #[m]
length = 2 #[m]
number_elements = 10 #[-]

tube1 = Tube(length, D_external, thickness, number_elements)

D_external = 0.205 #[m]
thickness = 0.012 #[m]
tube2 = Tube(length, D_external, thickness, number_elements)

# 
pressure = 100 #[pa]
volume_velocity = 0 #[m³/s]


#%% analysis
frequency = np.arange(1,251)

omega = 2*pi * frequency
wave_number = omega / gas.sound_velocity