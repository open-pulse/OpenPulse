import numpy as np
from data.user_input.project.printMessageInput import PrintMessageInput

window_title_1 = "ERROR"
window_title_2 = "WARNING"

class AfterRun:
    def __init__(self, project, opv):
        self.project = project
        self.opv = opv

        self.solution_acoustic = project.solution_acoustic
        self.frequencies = project.frequencies
        self.map_nodes = project.preprocessor.map_global_to_external_index
        self.nodes = project.preprocessor.nodes
        self.structural_elements = project.preprocessor.structural_elements
        self.acoustic_elements = project.preprocessor.acoustic_elements
        self.dict_tag_to_entity = project.preprocessor.dict_tag_to_entity
        # self.acoustic_criteria = defaultdict(list)

    def check_the_acoustic_criterias_related_to_elements(self, nl_criteria=0.08):
        # list_non_linear = []
        if self.solution_acoustic is None:
            pass
        else:
            if self.project.analysis_ID in [3,5,6]:
                static_pressure = [[] for _ in range(len(self.nodes))]
                for element in self.acoustic_elements.values():
                    if element.fluid is None:
                        static_pressure[element.first_node.global_index].append(1e9)
                        static_pressure[element.last_node.global_index].append(1e9)
                    else:
                        static_pressure[element.first_node.global_index].append(element.fluid.pressure)
                        static_pressure[element.last_node.global_index].append(element.fluid.pressure)

                aux = [min(p0) for p0 in static_pressure]
                static_pressure = np.array(aux).reshape(-1,1)
                pressure_ratio = np.abs(self.solution_acoustic/static_pressure)
                criteria = pressure_ratio > nl_criteria
                aux_freq = np.any(criteria, axis=0)
                aux_nodes = np.any(criteria, axis=1)
                self.list_freq = self.frequencies[aux_freq]
                nodes_internal = np.arange(len(self.nodes))[aux_nodes]
                self.list_nodes = [self.map_nodes[global_index] for global_index in nodes_internal]
                self.list_nodes.sort()
        
                if np.any(criteria):
                    self.opv.changePlotToMesh()
                    self.opv.opvRenderer.highlight_nodes(self.list_nodes, reset_colors=False)
                    window_title = "WARNING"
                    title = "Acoustic nonlinearity criteria not satisfied"
                    message_non_linear = f"The acoustic model is out of its linear validity range at {len(self.list_nodes)} nodes and at {len(self.list_freq)} frequencies."
                    message_non_linear += "it is recommended to check the results carefully."
                    PrintMessageInput([title, message_non_linear, window_title])

    def check_the_acoustic_criterias_related_to_nodes(self):
        pass

    def check_all_acoustic_criterias(self):
        self.check_the_acoustic_criterias_related_to_elements()
        self.check_the_acoustic_criterias_related_to_nodes()
            