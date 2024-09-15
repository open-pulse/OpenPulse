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

        self.f_min = 1
        self.f_max = 200
        self.f_step = 1
        self.frequencies = None
        self.list_frequencies = list()

        self.global_damping = [0., 0., 0., 0.]

        self.gravity_vector = np.zeros(DOF_PER_NODE_STRUCTURAL, dtype=float)

        self.weight_load = False
        self.internal_pressure_load = False
        self.external_nodal_loads = False
        self.element_distributed_load = False

        self.set_static_analysis_setup(dict())

    def set_gravity_vector(self, gravity_vector: np.ndarray):
        self.gravity_vector = gravity_vector

    def set_analysis_setup(self, analysis_setup: dict):
        self.analysis_setup = analysis_setup
        if "f_min" in analysis_setup.keys():
            self.set_frequency_setup(analysis_setup)
        if "global_damping" in analysis_setup.keys():
            self.set_global_damping(analysis_setup)
        if "weight_load" in analysis_setup.keys():
            self.set_static_analysis_setup(analysis_setup)

    def set_frequency_setup(self, analysis_setup: dict):
        self.frequencies = None
        self.f_min = analysis_setup.get("f_min", None)
        self.f_max = analysis_setup.get("f_max", None)
        self.f_step = analysis_setup.get("f_step", None)
        if "frequencies" in analysis_setup.keys():
            self.frequencies = analysis_setup.get("frequencies", None)
        elif (self.f_min, self.f_max, self.f_step).count(None) != 3:
            self.frequencies = np.arange(self.f_min, self.f_max + self.f_step, self.f_step)

    def set_global_damping(self, analysis_setup: dict):
        self.global_damping = analysis_setup.get("global_damping", [0., 0., 0., 0.])

    def set_static_analysis_setup(self, analysis_setup: dict):
        self.static_analysis_setup = analysis_setup
        self.weight_load = analysis_setup.get("weight_load", True) 
        self.internal_pressure_load = analysis_setup.get("internal_pressure_load", True)
        self.external_nodal_loads = analysis_setup.get("external_nodal_loads", True)
        self.element_distributed_load = analysis_setup.get("element_distributed_load", True)

    def set_psd_data(self, psd_data: dict):
        self.psd_data = psd_data

    def change_analysis_frequency_setup(self, frequencies: list | np.ndarray | None):

        if frequencies is None:
            return False

        if isinstance(frequencies, np.ndarray):
            frequencies = list(frequencies)

        condition_1 = self.list_frequencies == list() 
        condition_2 = not self.properties.check_if_there_are_tables_at_the_model()

        if condition_1 or condition_2:

            f_min = frequencies[0]
            f_max = frequencies[-1]
            f_step = frequencies[1] - frequencies[0]

            frequency_setup = { "f_min" : f_min,
                                "f_max" : f_max,
                                "f_step" : f_step }

            self.set_frequency_setup(frequency_setup)

            self.list_frequencies = frequencies

            return False

        if self.list_frequencies != frequencies:
            return True