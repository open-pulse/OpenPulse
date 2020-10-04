import numpy as np

class Material:
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
        return self.young_modulus / (2 * (1 + self.poisson_ratio))

    @property
    def lambda_parameter(self):
        return (self.poisson_ratio * self.young_modulus) / ((1 + self.poisson_ratio) * (1 - 2 * self.poisson_ratio))

    def _calculate_remaining_properties(self):
        if (self.young_modulus and self.poisson_ratio) is not None:
            self.shear_modulus = self.young_modulus / (2 * (1 + self.poisson_ratio))

        elif (self.poisson_ratio and self.shear_modulus) is not None:
            self.young_modulus = self.shear_modulus * (2 * (1 + self.poisson_ratio))

        elif (self.shear_modulus and self.young_modulus) is not None:
            self.poisson_ratio = (self.young_modulus / (2 * self.shear_modulus)) - 1

        else:
            raise TypeError('At least 2 arguments from young_modulus, shear_modulus and poisson_ratio should be provided')
    
    def getColorRGB(self):
        temp = self.color[1:-1] #Remove "[ ]"
        tokens = temp.split(',')
        return list(map(int, tokens))

    def getNormalizedColorRGB(self):
        #VTK works with type of color
        color = self.getColorRGB()
        for i in range(3):
            if color[i] != 0:
                color[i] = color[i]/255
        return color

    def getName(self):
        return self.name

    def __eq__(self, other):
        self_parameters = [v for v in self.__dict__.values() if isinstance(v, (float, int))]
        other_parameters = [v for v in self.__dict__.values() if isinstance(v, (float, int))]
        return np.allclose(self_parameters, other_parameters)
