import numpy as np


def load_fluid(name):
    pass

def save_fluid(material):
    pass

class Fluid:
    """A fluid class.
    This class creates a fluid object from fluid properties input data.

    Parameters
    ----------
    name : str
        Text to be used as fluid's name.

    density : float
        Fluid density.

    speed_of_sound : float
        Speed of the sound wave propagating in the fluid.

    isentropic_exponent : float, optional
        Fluid isentropic exponent, also know as the heat capacity ratio, the adiabatic index,  the ratio of specific heats, or Laplace's coefficient.
        Default is None.

    thermal_conductivity : float, optional
        Fluid thermal conductivity.
        Default is None.

    specific_heat_Cp : float, optional
        Fluid specific heat capacity at constant pressure.
        Default is None.

    dynamic_viscosity : float, optional
        Fluid dynamic viscosity.
        Default is None.

    color : tuple, optional
        The color associated with the fluid. Entity objects with this fluid object attributed will be shown with this color in the UI.
        Default is None.

    identifier : int, optional
        Fluid identifier displayed in the UI list of fluids.
        Default is -1.
    """
    def __init__(self,  name, density, speed_of_sound, **kwargs):
        self.name = name
        self.density = density
        self.speed_of_sound = speed_of_sound
        self.color = kwargs.get("color", None)
        self.identifier = kwargs.get("identifier", -1)
        self.isentropic_exponent = kwargs.get("isentropic_exponent", None)
        self.thermal_conductivity = kwargs.get("thermal_conductivity", None)
        self.specific_heat_Cp = kwargs.get("specific_heat_Cp", None)
        self.dynamic_viscosity = kwargs.get("dynamic_viscosity", None)  
        self.temperature = kwargs.get("temperature", None)
        self.pressure = kwargs.get("pressure", None)   

    @property
    def impedance(self):
        """
        This method evaluates the fluid specific impedance.

        Returns
        -------
        float
            Fluid specific impedance.
        """
        return self.density * self.speed_of_sound
    
    @property
    def bulk_modulus(self):
        """
        This method evaluates the fluid Bulk modulus.

        Returns
        -------
        float
            Fluid Bulk modulus.
        """
        return self.density * self.speed_of_sound**2

    @property
    def kinematic_viscosity(self):
        """
        This method evaluates the fluid kinematic viscosity.

        Returns
        -------
        float
            Fluid kinematic viscosity.
        """
        return self.dynamic_viscosity / self.density

    @property
    def thermal_diffusivity(self):
        """
        This method evaluates the fluid thermal diffusivity.

        Returns
        -------
        float
            Fluid thermal diffusivity.
        """
        return self.thermal_conductivity / (self.density * self.specific_heat_Cp) 

    @property
    def prandtl(self):
        """
        This method evaluates the fluid Prandtl number.

        Returns
        -------
        float
            Fluid Prandtl number.
        """
        return self.specific_heat_Cp * self.dynamic_viscosity / self.thermal_conductivity

    def getColorRGB(self):
        """
        This method returns the fluid color.

        Returns
        -------
        tuple
            Fluid color.
        """
        temp = self.color[1:-1] #Remove "[ ]"
        tokens = temp.split(',')
        return list(map(int, tokens))

    def getNormalizedColorRGB(self):
        """
        This method returns the fluid normalized color.

        Returns
        -------
        tuple
            Fluid color.
        """
        #VTK works with type of color
        color = self.getColorRGB()
        for i in range(3):
            if color[i] != 0:
                color[i] = color[i]/255
        return color

    def getName(self):
        """
        This method returns the fluid name.

        Returns
        -------
        str
            Fluid name.
        """
        return self.name

    def __eq__(self, other):
        self_parameters = [v for v in self.__dict__.values() if isinstance(v, (float, int))]
        other_parameters = [v for v in self.__dict__.values() if isinstance(v, (float, int))]
        return np.allclose(self_parameters, other_parameters)
