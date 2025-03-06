from numpy import allclose

class Material:
    """A material class.
    This class creates a material object from material properties input data.

    Parameters
    ----------
    name : str
        Text to be used as material's name.

    density : float
        Material density.

    elasticity_modulus : float, optional
        Material Young's modulus.
        Default is None.

    poisson_ratio : float, optional
        Material Poisson's ratio.
        Default is None.

    shear_modulus : float, optional
        Material shear modulus.
        Default is None.

    color : tuple, optional
        The color associated with the material. Line objects with this material object attributed will be shown with this color in the UI.
        Default is None.

    identifier : int, optional
        Material identifier displayed in the UI list of materials.
        Default is -1.
    """
    def __init__(self, name, density, **kwargs):
        self.name = name
        self.density = density
        self.identifier = kwargs.get("identifier", -1)
        self.elasticity_modulus = kwargs.get("elasticity_modulus", None)
        self.poisson_ratio = kwargs.get("poisson_ratio", None)
        self.shear_modulus = kwargs.get("shear_modulus", None)
        self.color = kwargs.get("color", None)

        self.thermal_expansion_coefficient = kwargs.get('thermal_expansion_coefficient', None)
        self._calculate_remaining_properties()

    @property
    def mu_parameter(self):
        """
        This method evaluates the Lamé's second parameter `mu`.

        Returns
        ----------
        float
            Lamé constant `mu`.

        See also
        --------
        lambda_parameter : Evaluate Lamé constant `lambda`.
        """
        return self.elasticity_modulus / (2 * (1 + self.poisson_ratio))

    @property
    def lambda_parameter(self):
        """
        This method evaluates the Lamé's first parameter `lambda`.

        Returns
        ----------
        float
            Lamé constant `lambda`.

        See also
        --------
        mu_parameter : Evaluate Lamé constant `mu`.
        """
        return (self.poisson_ratio * self.elasticity_modulus) / ((1 + self.poisson_ratio) * (1 - 2 * self.poisson_ratio))

    def _calculate_remaining_properties(self):
        """
        This method evaluates the material property among Young's modulus, Poisson's ratio and shear modulus that was not attributed to the material.
        
        Raises
        ------
        TypeError
            At least two arguments among Young's modulus, Poisson's ratio
            and shear modulus have to be attributed to the material.
        """
        if (self.elasticity_modulus and self.poisson_ratio) is not None:
            self.shear_modulus = self.elasticity_modulus / (2 * (1 + self.poisson_ratio))

        elif (self.poisson_ratio and self.shear_modulus) is not None:
            self.elasticity_modulus = self.shear_modulus * (2 * (1 + self.poisson_ratio))

        elif (self.shear_modulus and self.elasticity_modulus) is not None:
            self.poisson_ratio = (self.elasticity_modulus / (2 * self.shear_modulus)) - 1

        else:
            message = "At least two arguments among Young's modulus, Poisson's ratio"
            message += "\n and shear modulus have to be attributed to the material."
            raise TypeError(message)

    def __eq__(self, other):
        self_parameters = [v for v in self.__dict__.values() if isinstance(v, (float, int))]
        other_parameters = [v for v in self.__dict__.values() if isinstance(v, (float, int))]
        return allclose(self_parameters, other_parameters)
