from numpy import allclose
from dataclasses import dataclass, field


@dataclass
class Fluid:
    """
    This class creates a fluid object from fluid properties input data.
    """

    name: str = None
    identifier: int = 0
    temperature: float = 0.0
    pressure: float = 0.0
    density: float = 0.0
    speed_of_sound: float = 0.0
    isentropic_exponent: float = 0.0
    thermal_conductivity: float = 0.0
    specific_heat_Cp: float = 0.0
    dynamic_viscosity: float = 0.0
    adiabatic_bulk_modulus: float | None = None
    vapor_pressure : float | None = None
    key_mixture : str | None = None
    molar_mass: float = 0.0
    key_mixture: str | None = None
    molar_fractions: list | None = None
    color: tuple = (0, 0, 0)

    @property
    def impedance(self):
        """
        This method evaluates the fluid specific impedance.

        Returns
        ----------
        float
            Fluid specific impedance.
        """
        return self.density * self.speed_of_sound

    @property
    def bulk_modulus(self):
        """
        This method evaluates the fluid Bulk modulus.

        Returns
        ----------
        float
            Fluid Bulk modulus.
        """
        return self.density * self.speed_of_sound**2

    @property
    def kinematic_viscosity(self):
        """
        This method evaluates the fluid kinematic viscosity.

        Returns
        ----------
        float
            Fluid kinematic viscosity.
        """
        return self.dynamic_viscosity / self.density

    @property
    def thermal_diffusivity(self):
        """
        This method evaluates the fluid thermal diffusivity.

        Returns
        ----------
        float
            Fluid thermal diffusivity.
        """
        return self.thermal_conductivity / (self.density * self.specific_heat_Cp) 

    @property
    def prandtl(self):
        """
        This method evaluates the fluid Prandtl number.

        Returns
        ----------
        float
            Fluid Prandtl number.
        """
        return self.specific_heat_Cp * self.dynamic_viscosity / self.thermal_conductivity

    def __eq__(self, other):
        self_parameters = [v for v in self.__dict__.values() if isinstance(v, (float, int))]
        other_parameters = [v for v in self.__dict__.values() if isinstance(v, (float, int))]
        return allclose(self_parameters, other_parameters)