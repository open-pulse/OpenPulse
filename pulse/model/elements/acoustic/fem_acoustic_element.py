
import numpy as np

from pulse.model.elements.acoustic.acoustic_element import AcousticElement
from pulse.model.data_classes.data_classes import PerforatedPlateData, PerforatedPlateFormulation
from pulse.model.elements.element_attributes import ElementAttributes


class FEMAcousticElement(AcousticElement):
    """An acoustic element.
    This class creates an acoustic element from input data.
    """
    def __init__(self, element_attributes: ElementAttributes, **kwargs):
        super().__init__(element_attributes, **kwargs)


    def fem_elementary_matrices(self, length: float | None = None, length_correction: float = 0):
        """
        This method returns the FEM acoustic 1D elementary matrices. The method allows to include 
        the length correction due to  acoustic discontinuities (loop, expansion, side branch). The 
        FEM is not compatible with any damping model.


        Parameters
        ----------
        length : float, optional
            Element length defined as an argument.

        length_correction : float, optional
            Element length correction to be added to the element length.

        Returns
        -------
        Ke : 2D array
            Element acoustic stiffness matrix.

        Me : 2D array
            Element acoustic inertia matrix.
        """
        if length is None:
            length = self.length

        _length = length + length_correction

        rho = self.fluid.density
        c = self.speed_of_sound_corrected()

        perforated_plate_data = self.element_attributes.perforated_plate_data

        if isinstance(perforated_plate_data, PerforatedPlateData):
            if perforated_plate_data.type == PerforatedPlateFormulation.COMMON_PIPE:
                d = perforated_plate_data.hole_diameter
                self.area_fluid = np.pi * (d**2) / 4

        Ke = (self.area_fluid / (rho * _length)) * np.array([[1, -1], [-1, 1]], dtype=float)

        Me = (self.area_fluid * length / (6 * rho * c**2)) * np.array([[2, 1], [1, 2]], dtype=float)

        return Ke, Me

    def fem_elementary_link_matrices(self, length: float, length_correction: float = 0):
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

        return self.fem_elementary_matrices(length = length, length_correction = length_correction)