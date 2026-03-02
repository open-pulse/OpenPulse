import numpy as np

from pulse.interface.user_input.model.setup.nodes_input import NodesInput


class StructuralNodesInput(NodesInput):
    def __init__(self):
        super().__init__()

    def process_table_file_removal(self, table_names):
        super().process_table_file_removal("structural", table_names)

    def text_label(self, mask: list[bool], labels: np.array):
        _labels = labels[mask]
        n = list(mask).count(True)

        return f"[{','.join(['{}'] * n)}]".format(*_labels)
