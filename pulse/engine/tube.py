import numpy as np
from math import pi, sqrt

class TubeCrossSection:
    """ Tube cross section.
    Class used to create the tube's cross section and define its properties.
    External diameter D_external and internal diameter D_internal or thickness 
    should be provided.
    Parameters
    ----------
    D_external : float
        External diameter [m].
    D_internal : float
        Internal diameter [m].
    thickness : float
        thickness [m].
    Examples
    --------
    poisson_ratio : float
        Poisson's ratio [ ]
    Examples
    --------
    """
    def __init__(self, D_external, **kwargs):
        #TODO: review this warning
        assert (
            sum([1 if i in ["D_internal", "thickness"] else 0 for i in kwargs]) > 0
        ), "At least 1 arguments from D_internal and thickness should be provided."

        self.D_external = D_external
        self.D_internal = kwargs.get("D_internal", None)
        self.thickness = kwargs.get("thickness", None)
        self.index = kwargs.get("index", None)

        if self.D_internal is None:
            self.D_internal = self.D_external - 2 * self.thickness
        elif self.thickness is None:
            self.thickness = ( self.D_external - self.D_internal) / 2

    def area(self):
        """Cross section area [m**2]."""
        return (self.D_external**2 - self.D_internal**2) * pi / 4
        
    def moment_area(self):
        """Cross section second moment of area [m**4]."""
        return (self.D_external**4 - self.D_internal**4) * pi / 64
    
    def polar_moment_area(self):
        """Cross section second polar moment of area [m**4]."""
        return 2 * self.moment_area()

    def shear_form_factor(self):
        """Shear form factor for a tube.
        Parameter
        ---------
        poisson_ratio : float
            Poisson's ratio [ ]"""
        alpha = self.D_internal / self.D_external
        auxiliar = alpha / (1 + (alpha**2))
        return 6 / (7 + 20 * auxiliar**2)
    
    def shear_area(self, element_length, young_modulus):
        shear_area = self.area() * self.shear_form_factor()
        return 1 / (( 1 / shear_area) + element_length**2/(12 * young_modulus * self.moment_area()))

#TODO: organizar a forma como o PRINT é usado para a classe.