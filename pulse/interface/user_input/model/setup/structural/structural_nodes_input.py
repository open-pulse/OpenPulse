import numpy as np
from PySide6.QtWidgets import QLineEdit

from pulse import app
from pulse.interface import error_title
from pulse.interface.user_input.model.setup.nodes_input import NodesInput
from pulse.interface.user_input.project.print_message import PrintMessageInput


class StructuralNodesInput(NodesInput):
    def __init__(self):
        super().__init__()

    def text_label(self, mask: list[bool], labels: np.array):
        _labels = labels[mask]
        n = list(mask).count(True)

        return f"[{','.join(['{}'] * n)}]".format(*_labels)

    def check_entries(self, lineEdit: QLineEdit) -> list[bool, complex | None]: 

        value = 0
        if lineEdit.text() != "":
            value = float(lineEdit.text())

        if value == 0:
            return None

        return value

    def table_values_attribution_callback(
        self,
        node_ids: list[int],
        property_label: str,
        dof_labels: list[str],
        properties_to_remove: list[str] | str,
        ignore_empty: bool = False,
    ):

        self.remove_properties_from_node(node_ids, properties_to_remove)

        table_paths = list()

        for label in dof_labels:
            table_path_name = f"{label}_table_path"
            imported_values_name = f"imported_{label}_values"
            _imported_values = getattr(self, imported_values_name)

            if _imported_values is None:
                line_edit = getattr(self, f"lineEdit_{label}_table_path")

                _imported_values, _table_path = self.load_table(
                    line_edit, property_label, dof_label=label, direct_load=True
                )
                setattr(self, imported_values_name, _imported_values)
                setattr(self, table_path_name, _table_path)

            _table_path_attr = getattr(self, table_path_name)
            table_paths.append(_table_path_attr)

        for node_id in node_ids:
            table_names = list()

            for i, label in enumerate(dof_labels):
                imported_values_name = f"imported_{label}_values"
                _imported_values = getattr(self, imported_values_name)

                _table_name = None
                if isinstance(_imported_values, np.ndarray):
                    _table_name = self.get_table_name(
                        f"{property_label}_{label}", node_id=node_id
                    )

                    if self.save_table_values(_table_name, _imported_values):
                        return

                table_names.append(_table_name)

            if (table_names).count(None) == 6:

                if ignore_empty:
                    return False

                title = "Additional inputs required"
                message = f"You must inform at least one {property_label.replace('_', ' ')} "
                message += "table path before confirming the input!"
                PrintMessageInput([error_title, title, message])
                return False

            node = app().project.model.preprocessor.nodes[node_id]
            coords = np.round(node.coordinates, 5)

            data = {
                "coords": list(coords),
                "table_names": table_names,
                "table_paths": table_paths,
            }

            self.properties._set_nodal_property(property_label, data, node_id)

        app().project.file.write_nodal_properties_in_file()

        self.actions_to_finalize()

        return True

    def save_table_values(self, table_name: str, imported_values: np.ndarray, filter_zero: bool = False):

        if filter_zero:
            mask_filter = imported_values[:, 0] > 0
            _imported_values = imported_values[mask_filter, :]
        else:
            _imported_values = imported_values

        # define the frequencies vector
        frequencies = _imported_values[:, 0]

        if app().project.model.change_analysis_frequency_setup(list(frequencies)):
            self.hide()
            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup "
            message += "different from the others already imported ones. The current "
            message += "project frequency setup will not be modified."
            message += f"\n\n{table_name}"
            PrintMessageInput(["Error", title, message])
            return True

        self.update_analysis_setup_in_file(frequencies)

        # real values vector
        real_values = _imported_values[:, 1]
        
        # imaginary values vector
        imag_values = _imported_values[:, 2]

        # data to be stored
        data = np.array([frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("structural", table_name, data)

        return False