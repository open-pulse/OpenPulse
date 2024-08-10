from pulse.properties.model_properties import ModelProperties

class Model:

    def __init__(self):
        super().__init__()

        self.properties = ModelProperties()

        self.mesh = None

    def _initialize(self):
        pass