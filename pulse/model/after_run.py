import numpy as np

from pulse import app
from pulse.interface import warning_title
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.model import AnalysisID


class AfterRun:
    def __init__(self):

        self.load_model_and_analysis_data()

    @property
    def project(self):
        return app().project

    @property
    def model(self):
        return app().project.model

    @property
    def mesh(self):
        return app().project.model.mesh

    @property
    def properties(self):
        return app().project.model.properties

    @property
    def preprocessor(self):
        return app().project.model.preprocessor

    def load_model_and_analysis_data(self):
        self.frequencies = self.model.frequencies
        self.nodes = self.preprocessor.nodes

    def check_the_acoustic_criterias_related_to_elements(self, nl_criteria=0.08):

        if self.model.acoustic_solution is None:
            return

        if AnalysisID(self.project.analysis_id).is_harmonic():

            static_pressure = [[] for _ in range(len(self.nodes))]
            for element_attributes in self.preprocessor.elements_attributes.values():

                fluid = element_attributes.fluid
                first_node = element_attributes.first_node
                last_node = element_attributes.last_node

                static_pressure[first_node.index].append(1e9 if fluid is None else fluid.pressure)
                static_pressure[last_node.index].append(1e9 if fluid is None else fluid.pressure)
            
            aux = [min(p0) for p0 in static_pressure]
            static_pressure = np.array(aux).reshape(-1, 1)
            pressure_ratio = np.abs(self.model.acoustic_solution / static_pressure)

            criteria = pressure_ratio > nl_criteria
            if not np.any(criteria):
                return

            mask_freq = np.any(criteria, axis=0)
            mask_nodes = np.any(criteria, axis=1)
            invalid_frequencies = self.frequencies[mask_freq]
            invalid_nodes_array = self.mesh.nodal_coordinates[:, 0][mask_nodes]
            invalid_nodes = list(invalid_nodes_array.astype(int))
    
            app().main_window.plot_mesh()
            self.highlight_selection(nodes = invalid_nodes)
            title = "Acoustic nonlinearity criteria not satisfied"
            message_nl = "The acoustic model is out of its linear validity range at "
            message_nl += f"{len(invalid_nodes)} nodes and at {len(invalid_frequencies)} frequencies."
            message_nl += "It is recommended to check the results carefully."
            PrintMessageInput([warning_title, title, message_nl])

    def check_the_acoustic_criterias_related_to_nodes(self):
        pass

    def check_all_acoustic_criterias(self):
        self.check_the_acoustic_criterias_related_to_elements()
        self.check_the_acoustic_criterias_related_to_nodes()

    def highlight_selection(self, nodes=None, elements=None, lines=None):
        app().main_window.set_selection(nodes=nodes, elements=elements, lines=lines)