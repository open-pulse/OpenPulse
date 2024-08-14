from pulse.model.node import DOF_PER_NODE_STRUCTURAL

from pulse.model.mesh import Mesh
from pulse.model.preprocessor import Preprocessor
from pulse.model.properties.model_properties import ModelProperties

import numpy as np

class Model:

    def __init__(self, project):
        super().__init__()

        self.project = project

        self._initialize()

        self.preprocessor = Preprocessor()
        self.mesh = Mesh(self.preprocessor)

        # self.preprocessor.set_model(self)
        self.preprocessor.set_mesh(self.mesh)

        self.properties = ModelProperties()

    def _initialize(self):

        self.mesh = None
        self.preprocessor = None
        self.properties = None
        self.psd_data = dict()
        self.gravity_vector = np.zeros(DOF_PER_NODE_STRUCTURAL, dtype=float)

        self.set_static_analysis_setup(dict())

    def set_gravity_vector(self, gravity_vector: np.ndarray):
        self.gravity_vector = gravity_vector

    def set_static_analysis_setup(self, analysis_setup: dict):
        self.static_analysis_setup = analysis_setup
        self.weight_load = analysis_setup.get("weight_load", True) 
        self.internal_pressure_load = analysis_setup.get("internal_pressure_load", True)
        self.external_nodal_loads = analysis_setup.get("external_nodal_loads", True)
        self.element_distributed_load = analysis_setup.get("element_distributed_load", True)

    def set_frequency_setup(self, analysis_setup: dict):
        self.f_min = analysis_setup.get("f_min", None)
        self.f_max = analysis_setup.get("f_max", None)
        self.f_step = analysis_setup.get("f_step", None)
        if (self.f_min, self.f_max, self.f_step).count(None) != 3:
            self.frequencies = np.arange(self.f_min, self.f_max + self.f_step, self.f_step)

    def set_global_damping(self, analysis_setup: dict):
        self.global_damping = analysis_setup.get("global damping", [0., 0., 0., 0.])

    def set_psd_data(self, psd_data: dict):
        self.psd_data = psd_data