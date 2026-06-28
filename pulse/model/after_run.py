import numpy as np

from pulse import app
from pulse.interface import warning_title
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.model import AnalysisID


class AfterRun:
    def __init__(self):

        self.main_window = app().main_window
        self.project = app().project
        self.model = app().project.model
        self.preprocessor = app().project.model.preprocessor

        self.load_model_and_analysis_data()

    def load_model_and_analysis_data(self):
        self.solution_acoustic = app().project.acoustic_solution
        self.frequencies = self.model.frequencies
        self.map_nodes = self.preprocessor.map_global_to_external_index
        self.nodes = self.preprocessor.nodes

    def check_the_acoustic_criterias_related_to_elements(self, nl_criteria=0.08):

        if self.solution_acoustic is None:
            return

        if AnalysisID(self.project.analysis_id).is_harmonic():

            static_pressure = [[] for _ in range(len(self.nodes))]
            for element_attributes in self.preprocessor.elements_attributes.values():

                fluid = element_attributes.fluid
                first_node = element_attributes.first_node
                last_node = element_attributes.last_node

                static_pressure[first_node.global_index].append(1e9 if fluid is None else fluid.pressure)
                static_pressure[last_node.global_index].append(1e9 if fluid is None else fluid.pressure)
            
            aux = [min(p0) for p0 in static_pressure]
            static_pressure = np.array(aux).reshape(-1, 1)
            pressure_ratio = np.abs(self.solution_acoustic / static_pressure)

            criteria = pressure_ratio > nl_criteria
            aux_freq = np.any(criteria, axis=0)
            aux_nodes = np.any(criteria, axis=1)
            self.list_freq = self.frequencies[aux_freq]
            nodes_internal = np.arange(len(self.nodes))[aux_nodes]
            self.list_nodes = [self.map_nodes[global_index] for global_index in nodes_internal]
            self.list_nodes.sort()
    
            if np.any(criteria):
                self.main_window.plot_mesh()
                self.highlight_selection(nodes = self.list_nodes)
                title = "Acoustic nonlinearity criteria not satisfied"
                message_nl = "The acoustic model is out of its linear validity range at "
                message_nl += f"{len(self.list_nodes)} nodes and at {len(self.list_freq)} frequencies."
                message_nl += "It is recommended to check the results carefully."
                PrintMessageInput([warning_title, title, message_nl])

    def check_the_acoustic_criterias_related_to_nodes(self):
        pass

    def check_all_acoustic_criterias(self):
        self.check_the_acoustic_criterias_related_to_elements()
        self.check_the_acoustic_criterias_related_to_nodes()

    def highlight_selection(self, nodes=None, elements=None, lines=None):
        app().main_window.set_selection(nodes=nodes, elements=elements, lines=lines)