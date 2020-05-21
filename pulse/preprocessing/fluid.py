import numpy as np


def load_fluid(name):
    pass

def save_fluid(material):
    pass


class Fluid:
    def __init__(self,  name, density, sound_velocity, **kwargs):
        self.name = name
        self.density = density
        self.sound_velocity = sound_velocity
        self.color = kwargs.get("color", None)

    @property
    def impedance(self):
        return self.density * self.sound_velocity
    
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
