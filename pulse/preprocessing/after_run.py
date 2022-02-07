from collections import defaultdict
from data.user_input.project.printMessageInput import PrintMessageInput
import numpy as np

window_title_1 = "ERROR"
window_title_2 = "WARNING"

class AfterRun:
    def __init__(self, project, opv, **kwargs):
        self.project = project
        self.opv = opv
        self.preprocessor = project.preprocessor
        self.nodes = project.preprocessor.nodes
        self.structural_elements = project.preprocessor.structural_elements
        self.acoustic_elements = project.preprocessor.acoustic_elements
        self.dict_tag_to_entity = project.preprocessor.dict_tag_to_entity
        # self.acoustic_criteria = defaultdict(list)

    def check_the_acoustic_criterias_related_to_elements(self):
        for element_id, element in self.acoustic_elements.items():
            pass

    def check_the_acoustic_criterias_related_to_nodes(self, ratio_criteria=2):
        
        non_linear_criteria = []
        for node_id, node in self.nodes.items():
            if node.acoustic_solution is not None:
                nodal_pressure = node.acoustic_solution
                if max(np.abs(nodal_pressure))/np.abs(nodal_pressure[0]) >= ratio_criteria:
                    non_linear_criteria.append(node_id)
     
        if non_linear_criteria != []:
            list_nodes = non_linear_criteria
            self.opv.changePlotToMesh()
            self.opv.opvRenderer.highlight_nodes(list_nodes, reset_colors=False)
            window_title = "WARNING"
            title = "Acoustic criteria not satisfied"
            message_non_linear = "The acoustic model is out of its linear validity range at the following nodes:"
            message_non_linear += f"\n\nNodes: {list_nodes}\n\n"     
            message_non_linear += "it is recommended to check the results carefully."
            PrintMessageInput([title, message_non_linear, window_title])

    def check_all_acoustic_criterias(self):
        self.check_the_acoustic_criterias_related_to_elements()
        self.check_the_acoustic_criterias_related_to_nodes()
            