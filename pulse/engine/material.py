import numpy as np

class Material:
    """ Isotropic material used on tubes.
    Class used to create a isotropic material and define its properties.
    density and at least 2 arguments from E, G_s and Poisson should be
    provided.
    Parameters
    ----------
    name : str
        Material name.
    density : float
        Density [kg/m**3].
    young_modulus : float
        Young's modulus [N/m**2].
    poisson_ratio : float
        Poisson's ratio [ ]
    shear_modulus : float
        Shear modulus [N/m**2].
    color : str
        Can be used on plots.
    Examples
    --------
    >>> AISI4140 = Material(name='AISI4140', density=7850, young_modulus=203.2e9, shear_modulus=80e9)
    >>> Steel = Material(name="Steel", density=7810, young_modulus=211e9, shear_modulus=81.2e9)
    >>> AISI4140.poisson_ratio
    0.27
    """

    def __init__(self, name, density, **kwargs):

        assert (
            sum([1 if i in ["young_modulus", "shear_modulus", "poisson_ratio"] else 0 for i in kwargs]) > 1
        ), "At least 2 arguments from young_modulus, shear_modulus and poisson_ratio should be provided"

        self.name = name
        self.density = density
        self.young_modulus = kwargs.get("young_modulus", None)
        self.poisson_ratio = kwargs.get("poisson_ratio", None)
        self.shear_modulus = kwargs.get("shear_modulus", None)
        self.color = kwargs.get("color", "#525252")

        if self.young_modulus is None:
            self.young_modulus = self.shear_modulus * (2 * (1 + self.poisson_ratio))
        elif self.shear_modulus is None:
            self.shear_modulus = self.young_modulus / (2 * (1 + self.poisson_ratio))
        elif self.poisson_ratio is None:
            self.poisson_ratio = (self.young_modulus / (2 * self.shear_modulus)) - 1

    def mu_parameter(self):
        return self.young_modulus / (2 * (1 + self.poisson_ratio ) )
    
    def lambda_parameter(self):
        return self.poisson_ratio * self.young_modulus /( (1 + self.poisson_ratio) * (1 - 2 * self.poisson_ratio) )

    def __eq__(self, other):
        """Material is considered equal if its properties are equal."""
        self_list = [v for v in self.__dict__.values() if isinstance(v, (float, int))]
        other_list = [v for v in self.__dict__.values() if isinstance(v, (float, int))]

        if np.allclose(self_list, other_list):
            return True
        else:
            return False

    def __repr__(self):
        selfyoung_modulus = "{:.3e}".format(self.young_modulus)
        selfpoisson_ratio = "{:.3e}".format(self.poisson_ratio)
        selfdensity = "{:.3e}".format(self.density)
        selfshear_modulus = "{:.3e}".format(self.shear_modulus)

        return (
            f"Material"
            f'(name="{self.name}", density={selfdensity}, shear_modulus={selfshear_modulus}, '
            f"E={selfyoung_modulus}, poisson_ratio={selfpoisson_ratio}, color={self.color!r})"
        )

    def __str__(self):
        return (
            f"{self.name}"
            f'\n{35*"-"}'
            f"\nDensity        [kg/m**3]: {float(self.density):{2}.{8}}"
            f"\nYoung`s modulus [N/m**2]: {float(self.young_modulus):{2}.{8}}"
            f"\nShear modulus   [N/m**2]: {float(self.shear_modulus):{2}.{8}}"
            f"\nPoisson coefficient     : {float(self.poisson_ratio):{2}.{8}}"
        )
