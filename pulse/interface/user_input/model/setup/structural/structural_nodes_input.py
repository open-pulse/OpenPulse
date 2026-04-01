import inspect
import numpy as np

from PySide6.QtCore import QLocale
from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QDoubleValidator, QValidator

from pulse import app
from pulse.interface.user_input.model.setup.nodes_input import NodesInput
from pulse.interface.user_input.project.print_message import PrintMessageInput

error_title = "Error"


class StructuralNodesInput(NodesInput):
    def __init__(self):
        super().__init__()

        self.validator = QDoubleValidator()
        self.validator.setLocale(QLocale.c())

    def text_label(self, mask: list[bool], labels: np.array):
        _labels = labels[mask]
        n = list(mask).count(True)

        return f"[{','.join(['{}'] * n)}]".format(*_labels)

    def check_entries(self, lineEdit: QLineEdit, label: str):

        str_value = lineEdit.text()
        if str_value != "":
            state, _, _ = self.validator.validate(str_value, 0)
            
            if state != QValidator.Acceptable:
                title = f"Invalid entry to the {label}"
                message = f"Wrong input for {label}."
                PrintMessageInput([error_title, title, message])
                return True, None
            value = float(str_value)
        else:
            value = 0

        if value == 0:
            return False, None
        else:
            return False, value

    def table_values_attribution_callback(
        self,
        line_edit_node_ids: QLineEdit,
        properties_to_remove: list[str] | str,
        load_labels: list[str],
        input_name: str,
        save_table_function: callable,
    ):

        str_nodes = line_edit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            line_edit_node_ids.setFocus()
            return

        self.remove_properties_from_node(node_ids, properties_to_remove)

        table_paths = list()

        for label in load_labels:
            table_path_name = f"{label}_table_path"
            imported_values_name = f"imported_{label}_values"
            _imported_values = getattr(self, imported_values_name)

            if _imported_values is None:
                line_edit = getattr(self, f"lineEdit_{label}_table_path")

                _imported_values, _table_path = self.load_table(
                    line_edit, input_name, dof_label=label, direct_load=True
                )
                setattr(self, imported_values_name, _imported_values)
                setattr(self, table_path_name, _table_path)

            _table_path_attr = getattr(self, table_path_name)
            table_paths.append(str(_table_path_attr))

        for node_id in node_ids:
            table_names = list()

            for i, label in enumerate(load_labels):
                imported_values_name = f"imported_{label}_values"
                _imported_values = getattr(self, imported_values_name)

                _table_name = None
                if isinstance(_imported_values, np.ndarray):
                    _table_name = self.get_table_name(
                        f"{input_name}_{label}", node_id=node_id
                    )
                    function_parameters = inspect.signature(save_table_function).parameters

                    if "linear" in function_parameters and "angular" in function_parameters:
                        if save_table_function(_table_name, _imported_values, 
                                               linear= i <= 2,
                                               angular= i >= 3):
                            return

                    if save_table_function(_table_name, _imported_values):
                        return

                table_names.append(_table_name)

            if (table_names).count(None) == 6:
                title = "Additional inputs required"
                message = f"You must inform at least one {input_name.replace('_', ' ')} "
                message += "table path before confirming the input!"
                PrintMessageInput([error_title, title, message])
                return

            node = app().project.model.preprocessor.nodes[node_id]
            coords = np.round(node.coordinates, 5)

            data = {
                "coords": list(coords),
                "table_names": table_names,
                "table_paths": table_paths,
            }

            self.properties._set_nodal_property(input_name, data, node_id)

        app().project.file.write_nodal_properties_in_file()

        self.actions_to_finalize()