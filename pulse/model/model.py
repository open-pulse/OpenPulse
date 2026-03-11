
from pulse.model import AnalysisID
from pulse.model.mesh import Mesh
from pulse.model.node import DOF_PER_NODE_STRUCTURAL
from pulse.model.preprocessor import Preprocessor
from pulse.model.properties.model_properties import ModelProperties

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.project.project import Project

import numpy as np

class Model:

    def __init__(self, project: 'Project'):
        super().__init__()

        self.project = project

        self._initialize()

        self.mesh = Mesh(self.project)
        self.preprocessor = Preprocessor(self.mesh)
        self.properties = ModelProperties()

    def _initialize(self):

        self.mesh = None
        self.preprocessor = None
        self.properties = None
        self.psd_data = dict()
        self.analysis_setup = dict()

        self.f_min = 1
        self.f_max = 200
        self.f_step = 1
        self.frequencies = None
        self.list_frequencies = list()

        self.gravity_vector = np.zeros(DOF_PER_NODE_STRUCTURAL, dtype=float)

        self.weight_load = False
        self.internal_pressure_load = False
        self.external_nodal_loads = False
        self.element_distributed_load = False

        self.set_static_analysis_setup(dict())

    def set_gravity_vector(self, gravity_vector: np.ndarray):
        self.gravity_vector = gravity_vector

    def reset_analysis_setup(self):
        self.analysis_setup.clear()

    @property
    def analysis_id(self):
        return self.analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)

    @property
    def analysis_type_label(self):
        if self.analysis_id == AnalysisID.STRUCTURAL_HARMONIC:
            return "Structural Harmonic Analysis"
        elif self.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            return "Acoustic Harmonic Analysis"
        elif self.analysis_id == AnalysisID.STRUCTURAL_MODAL:
            return "Structural Modal Analysis"
        elif self.analysis_id == AnalysisID.ACOUSTIC_MODAL:
            return "Acoustic Modal Analysis"
        elif self.analysis_id == AnalysisID.STRUCTURAL_STATIC:
            return "Structural Static Analysis"
        else:
            return "Analysis not identified"

    @property
    def analysis_method(self):
        return self.analysis_setup.get("analysis_method", "--")

    @property
    def number_of_modes(self):
        return self.analysis_setup.get("number_of_modes", 40)

    @property
    def sigma_factor(self):
        return self.analysis_setup.get("sigma_factor", 1e-2)

    @property
    def global_damping(self):
        return self.analysis_setup.get("global_damping", (0., 0., 0.))

    def set_analysis_setup(self, analysis_setup: dict):

        self.analysis_setup.update(analysis_setup)

        if "f_min" in analysis_setup.keys():
            self.set_frequency_setup(analysis_setup)

        if "weight_load" in analysis_setup.keys():
            self.set_static_analysis_setup(analysis_setup)

    def set_frequency_setup(self, analysis_setup: dict):

        self.frequencies = None
        self.f_min = analysis_setup.get("f_min", None)
        self.f_max = analysis_setup.get("f_max", None)
        self.f_step = analysis_setup.get("f_step", None)

        if "frequencies" in analysis_setup.keys():
            self.frequencies = analysis_setup["frequencies"]

        elif (self.f_min, self.f_max, self.f_step).count(None) == 0:

            try:
                self.frequencies = np.arange(self.f_min, self.f_max + self.f_step, self.f_step)

                # filters the frequencies vector to mitigate the already identified rounding errors
                mask = self.frequencies <= self.f_max
                self.frequencies = self.frequencies[mask]

            except:
                self.frequencies = None
                return

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

            frequency_setup = { 
                "f_min" : f_min,
                "f_max" : f_max,
                "f_step" : f_step,
                }

            self.set_analysis_setup(frequency_setup)

            self.list_frequencies = frequencies

            return False

        if self.list_frequencies != frequencies:
            return True