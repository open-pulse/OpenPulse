
from pulse.model import AnalysisID
from pulse.model.mesh import Mesh
from pulse.model.node import DOF_PER_NODE_STRUCTURAL
from pulse.model.preprocessor import Preprocessor
from pulse.model.properties.model_properties import ModelProperties

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.project.project import Project

from pulse.model.acoustic_element import AcousticElement
from pulse.model.structural_element import StructuralElement
from pulse.model.cross_sections.expansion_joint_cross_section import ExpansionJointCrossSection

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
        elif self.analysis_id == AnalysisID.COUPLED_HARMONIC:
            return "Coupled Harmonic Analysis"
        else:
            return "Analysis not identified"

    @property
    def analysis_method(self):
        return self.analysis_setup.get("analysis_method", "--")

    @property
    def acoustic_formulation(self):
        return self.analysis_setup.get("acoustic_formulation", "fetm")

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

        self.frequencies = None
        self.analysis_setup.update(analysis_setup)

        self.f_min = analysis_setup.get("f_min", None)
        self.f_max = analysis_setup.get("f_max", None)
        self.f_step = analysis_setup.get("f_step", None)
        frequencies = analysis_setup.get("frequencies", None)

        if isinstance(frequencies, list):
            self.frequencies = np.round(np.array(frequencies, dtype=float), 14)

        elif isinstance(frequencies, np.ndarray):
            self.frequencies = frequencies

        elif (self.f_min, self.f_max, self.f_step).count(None) == 0:

            try:
                frequencies = np.arange(self.f_min, self.f_max + self.f_step, self.f_step, dtype=float)
                frequencies = np.round(frequencies, 14)

                # filters the frequencies vector
                mask = frequencies <= self.f_max + self.f_step / 20
                _frequencies = frequencies[mask]

            except Exception as error_log:
                self.frequencies = None
                print(str(error_log))
                return

            self.frequencies = _frequencies
            self.analysis_setup["frequencies"] = list(_frequencies)

        if "weight_load" in analysis_setup.keys():
            self.set_static_analysis_setup(analysis_setup)

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
            self.list_frequencies = frequencies
            return False

        if self.list_frequencies != frequencies:
            return True

        # if condition_1 or condition_2:

        #     f_min = frequencies[0]
        #     f_max = frequencies[-1]
        #     f_step = frequencies[1] - frequencies[0]

        #     frequency_setup = { 
        #         "f_min" : f_min,
        #         "f_max" : f_max,
        #         "f_step" : f_step,
        #         }

        #     self.set_analysis_setup(frequency_setup)

        #     self.list_frequencies = frequencies

        #     return False

        # if self.list_frequencies != frequencies:
        #     return True

    def enhance_pipe_sections_appearance(self):
        """ 
        This method adds lids to cross-section variations and terminations.
        """
        for elements in self.preprocessor.structural_elements_connected_to_node.values():

            element = None
            if len(elements) == 2:

                first_element, last_element = elements
                first_element: StructuralElement
                last_element: StructuralElement

                if 'beam_1' in [first_element.element_type, last_element.element_type]:
                    continue

                first_cross = first_element.cross_section
                last_cross = last_element.cross_section
                
                if (first_cross, last_cross).count(None):
                    continue

                first_outer_diameter = first_cross.outer_diameter
                first_inner_diameter = first_cross.inner_diameter
                last_outer_diameter = last_cross.outer_diameter
                last_inner_diameter = last_cross.inner_diameter

                if first_outer_diameter < last_inner_diameter:
                    inner_diameter = first_inner_diameter 
                    element = last_element

                if last_outer_diameter < first_inner_diameter:
                    inner_diameter = last_inner_diameter 
                    element = first_element

            elif len(elements) == 1: 

                element = elements[0]
                element: StructuralElement
 
                if element.element_type == 'beam_1':
                    continue  

                first_node = element.first_node
                last_node = element.last_node  

                if element.cross_section is None:
                    continue

                inner_diameter = element.cross_section.inner_diameter 

                if len(self.preprocessor.neighbors[first_node]) == 1:
                    first_node_id = first_node.external_index
                    if self.properties.is_there_an_acoustic_attribute_in_the_node(first_node_id) == 0:
                        inner_diameter = 0

                elif len(self.preprocessor.neighbors[last_node]) == 1:
                    last_node_id = last_node.external_index
                    if self.properties.is_there_an_acoustic_attribute_in_the_node(last_node_id) == 0:
                        inner_diameter = 0

            if isinstance(element, AcousticElement | StructuralElement):

                if element.element_type == 'expansion_joint':
                    section_info = element.cross_section.section_info
                    if isinstance(section_info, ExpansionJointCrossSection):
                        element.section_parameters_render = section_info._as_list()

                else:

                    section_info = element.cross_section.section_info
                    outer_diameter, _, offset_y, offset_z, t_ins, *_ = section_info.section_parameters

                    thickness = (outer_diameter - inner_diameter) / 2
                    element.section_parameters_render = [outer_diameter, thickness, offset_y, offset_z, t_ins]