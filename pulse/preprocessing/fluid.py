import numpy as np


def load_fluid(name):
    pass

def save_fluid(material):
    pass

class Fluid:
    def __init__(self,  name, density, speed_of_sound, **kwargs):
        self.name = name
        self.density = density
        self.speed_of_sound = speed_of_sound
        self.color = kwargs.get("color", None)
        self.identifier = kwargs.get("identifier", -1)

    @property
    def impedance(self):
        return self.density * self.speed_of_sound
    
    @property
    def bulk_modulus(self):
        return self.density * self.speed_of_sound**2

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
