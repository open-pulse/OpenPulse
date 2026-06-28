
import numpy as np
from numpy import pi, sqrt

from pulse.model.elements.acoustic.acoustic_element import AcousticElement, j2_j0
from pulse.model.data_classes.model_setup_data_classes import PerforatedPlateData, PerforatedPlateFormulation
from pulse.model.elements.element_attributes import ElementAttributes


class FETMAcousticElement(AcousticElement):
    """ 
    This class creates an acoustic element based on the FETM theory.
    """
    def __init__(self, element_attributes: ElementAttributes, **kwargs):
        super().__init__(element_attributes, **kwargs)


    def fetm_admittance_matrix(self, frequencies: np.ndarray, length_correction: float = 0):
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

        perforated_plate_data = self.element_attributes.perforated_plate_data

        if isinstance(perforated_plate_data, PerforatedPlateData):
            if perforated_plate_data.type == PerforatedPlateFormulation.COMMON_PIPE:
                d = perforated_plate_data.hole_diameter
                self.area_fluid = pi*(d**2) / 4
            else:
                return self.perforated_plate_matrix(frequencies)

        self.reset()
        if self.acoustic_element_type in ["undamped_mean_flow", "peters", "howe"]:
            return self.fetm_mean_flow_matrix(frequencies, length_correction)

        elif self.acoustic_element_type in ["undamped", "proportional", "wide_duct", "LRF_fluid_equivalent", "damped_liquid"]:
            return self.fetm_admittance_matrix_various(frequencies, length_correction)

        elif self.acoustic_element_type == "LRF full":
            return self.fetm_lrf_thermoviscous_matrix(frequencies, length_correction)


    def fetm_admittance_matrix_various(self, frequencies: np.ndarray, length_correction: float = 0):
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
        kappa_complex, impedance_complex = self.get_wave_number_and_acoustic_impedance(frequencies)
        # self.radiation_impedance(kappa_complex, impedance_complex)

        kappaLe = kappa_complex * (self.length + length_correction)
        sine = np.sin(kappaLe)
        cossine = np.cos(kappaLe)
        Zf = impedance_complex / self.area_fluid

        # TODO: check this
        admittance_matrix = ((1j / (Zf * sine)) * np.array([-cossine, ones, ones, -cossine])).T

        return admittance_matrix


    def fetm_lrf_thermoviscous_matrix(self, frequencies: np.ndarray, length_correction: float = 0):
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

        omega = 2 * pi * frequencies
        rho = self.fluid.density
        nu = self.fluid.kinematic_viscosity
        gamma = self.fluid.isentropic_exponent
        pr = self.fluid.prandtl
        
        c = self.speed_of_sound_corrected()
        length = self.length + length_correction
        radius = self.cross_section.inner_radius
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
        ones = np.ones(len(frequencies), dtype='float64')

        admittance_matrix = - ((self.area_fluid * G / (impedance_complex * sinh)) * np.array([cosh, -ones, -ones, cosh])).T

        aux = np.real(kappa_complex * radius) > 1.84118
        if np.any(aux):
            self.flag_plane_wave = True
            self.max_valid_freq = np.min([np.min(frequencies[aux]), self.max_valid_freq])

        return admittance_matrix  


    def fetm_mean_flow_matrix(self, frequencies: np.ndarray, length_correction: float = 0):

        k, z, M = self.get_mean_flow_damping_data(frequencies)
        # self.radiation_impedance(k, z* (1-M**2))
        
        kLe = k * (self.length + length_correction)
        cotanh = 1 / np.tanh(1j * kLe)
        sineh = np.sinh(1j * kLe)
        exp_neg_sin = -np.exp(-1j * kLe * M) / sineh
        exp_sin = -np.exp(1j * kLe * M) / sineh
        adm = self.area_fluid / (z * (1 - M**2))
        admittance_matrix = (adm * np.array([cotanh - M, exp_neg_sin, exp_sin, cotanh + M])).T

        return admittance_matrix


    def fetm_admittance_link_matrix(self, frequencies: np.ndarray, length: float, length_correction: float = 0):
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
        kappa_complex, impedance_complex = self.get_wave_number_and_acoustic_impedance(frequencies)

        kappaLe = kappa_complex * (length + length_correction)
        sine = np.sin(kappaLe)
        cossine = np.cos(kappaLe)

        admittance_matrix = ((self.area_fluid * 1j / (sine * impedance_complex)) * np.array([-cossine, ones, ones, -cossine])).T

        return admittance_matrix