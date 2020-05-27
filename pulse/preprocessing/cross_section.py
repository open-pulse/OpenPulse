from math import pi


class CrossSection:
    def __init__(self, external_diameter, thickness, internal_diameter = 0):
        self.external_diameter = external_diameter
        self.external_radius = external_diameter/2
        self.thickness = thickness
        self.internal_diameter = internal_diameter

    # @property
    # def thickness(self):
    #     return (self.external_diameter - self.internal_diameter)/2

    @property
    def area_fluid(self):
        self.internal_diameter = self.external_diameter - 2*self.thickness
        return self.internal_diameter**2 * pi / 4

    @property
    def area(self):
        self.internal_diameter = self.external_diameter - 2*self.thickness
        return (self.external_diameter**2 - self.internal_diameter**2) * pi / 4
    
    @property
    def moment_area(self):
        self.internal_diameter = self.external_diameter - 2*self.thickness
        return (self.external_diameter**4 - self.internal_diameter**4) * pi / 64
    
    @property
    def polar_moment_area(self):
        return 2 * self.moment_area

    @property
    def shear_form_factor(self):
        self.internal_diameter = self.external_diameter - 2*self.thickness
        alpha = self.internal_diameter / self.external_diameter
        auxiliar = alpha / (1 + alpha**2)
        return 6 / (7 + 20 * auxiliar**2)
    
    def shear_area(self, element_length, young_modulus):
        temp = self.area * self.shear_form_factor
        return 1 / (( 1 / temp) + (element_length**2 / (12 * young_modulus * self.moment_area)))

    def getExternalDiameter(self):
        return self.external_diameter

    def getInternalDiameter(self):
        self.internal_diameter = self.external_diameter - 2*self.thickness
        return self.internal_diameter