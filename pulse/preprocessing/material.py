import numpy as np

class Material:
    """A material class.
    This class creates a material object from material properties input data.

    Parameters
    ----------
    name : str
        Text to be used as material's name.

    density : float
        Material density.

    young_modulus : float, optional
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
        self.identifier = kwargs.get("identifier", -1)
        self.density = density
        self.young_modulus = kwargs.get("young_modulus", None)
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
        return self.young_modulus / (2 * (1 + self.poisson_ratio))

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
        return (self.poisson_ratio * self.young_modulus) / ((1 + self.poisson_ratio) * (1 - 2 * self.poisson_ratio))

    def _calculate_remaining_properties(self):
        """
        This method evaluates the material property among Young's modulus, Poisson's ratio and shear modulus that was not attributed to the material.
        
        Raises
        ------
        TypeError
            At least two arguments among Young's modulus, Poisson's ratio
            and shear modulus have to be attributed to the material.
        """
        if (self.young_modulus and self.poisson_ratio) is not None:
            self.shear_modulus = self.young_modulus / (2 * (1 + self.poisson_ratio))

        elif (self.poisson_ratio and self.shear_modulus) is not None:
            self.young_modulus = self.shear_modulus * (2 * (1 + self.poisson_ratio))

        elif (self.shear_modulus and self.young_modulus) is not None:
            self.poisson_ratio = (self.young_modulus / (2 * self.shear_modulus)) - 1

        else:
            message = "At least two arguments among Young's modulus, Poisson's ratio"
            message += "\n and shear modulus have to be attributed to the material."
            raise TypeError(message)
    
    def getColorRGB(self):
        """
        This method returns the material color.

        Returns
        ----------
        tuple
            Material color.
        """
        # Ugly hack, will be corrected (I hope)
        temp = str(self.color)[1:-1] #Remove "[ ]"
        tokens = temp.split(',')
        return list(map(int, tokens))

    def getNormalizedColorRGB(self):
        """
        This method returns the material normalized color.

        Returns
        ----------
        tuple
            Material color.
        """
        #VTK works with type of color
        color = self.getColorRGB()
        for i in range(3):
            if color[i] != 0:
                color[i] = color[i]/255
        return color

    def getName(self):
        """
        This method returns the material name.

        Returns
        ----------
        str
            Mataerial name.
        """
        return self.name

    def __eq__(self, other):
        self_parameters = [v for v in self.__dict__.values() if isinstance(v, (float, int))]
        other_parameters = [v for v in self.__dict__.values() if isinstance(v, (float, int))]
        return np.allclose(self_parameters, other_parameters)
