from dataclasses import dataclass, field
from numpy import allclose

@dataclass
class Material:
    """
    This class creates a material object from material properties input data.
    """

    name: str = None
    identifier: int = 0
    density: float = 0.0
    elasticity_modulus: float = 0.0
    poisson_ratio: float = 0.0
    thermal_expansion_coefficient: float = 0.0
    color: tuple = (0, 0, 0)

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

    @property
    def shear_modulus(self):
        """
        This method returns the shear modulus G calculated
        from the elasticity modulus and poisson ratio.
        """
        return self.elasticity_modulus / (2 * (1 + self.poisson_ratio))

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
