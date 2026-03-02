import numpy as np
from PySide6.QtWidgets import QLineEdit

from pulse import app
from pulse.interface.user_input.model.setup.nodes_input import NodesInput
from pulse.interface.user_input.project.print_message import PrintMessageInput


class AcousticNodesInput(NodesInput):
    def __init__(self):
        super().__init__()

        self.before_run = app().project.get_pre_solution_model_checks()

    def process_table_file_removal(self, table_names):
        super().process_table_file_removal("acoustic", table_names)

    def text_label(self, value):
        text = ""
        if isinstance(value, complex):
            value_label = str(value)
        elif isinstance(value, np.ndarray):
            value_label = "Table"
        text = "{}".format(value_label)
        return text

    def check_complex_entries(
        self, lineEdit_real: QLineEdit, lineEdit_imag: QLineEdit, input_name: str
    ):
        error_title = "Error"

        title = f"Invalid entry to the {input_name}"

        if lineEdit_real.text() != "":
            _str_real = lineEdit_real.text()
            str_real = _str_real.replace(",", ".")

            try:
                real_F = float(str_real)
            except Exception:
                self.hide()
                message = f"Wrong input for real part of {input_name}."
                PrintMessageInput([error_title, title, message])
                lineEdit_real.setFocus()
                app().main_window.set_input_widget(self)
                return True, None
        else:
            real_F = 0

        if lineEdit_imag.text() != "":
            _str_imag = lineEdit_imag.text()
            str_imag = _str_imag.replace(",", ".")

            try:
                imag_F = float(str_imag)
            except Exception:
                self.hide()
                message = f"Wrong input for imaginary part of {input_name}."
                PrintMessageInput([error_title, title, message])
                lineEdit_imag.setFocus()
                app().main_window.set_input_widget(self)
                return True, None
        else:
            imag_F = 0

        if real_F == 0 and imag_F == 0:
            self.hide()
            message = f"You must inform at least one {input_name} "
            message += "before confirming the input!"
            PrintMessageInput([error_title, title, message])
            self.lineEdit_real_value.setFocus()
            app().main_window.set_input_widget(self)
            return True, None

        else:
            return False, real_F + 1j * imag_F

    def constant_values_attribution_callback(
        self,
        lineEdit_nodes: QLineEdit,
        lineEdit_real: QLineEdit,
        lineEdit_imag: QLineEdit,
        input_name: str,
        properties: str | list[str],
        reset_camera=True,
    ):

        lineEdit = lineEdit_nodes.text()
        stop, node_ids = self.before_run.check_selected_ids(lineEdit, "nodes")
        if stop:
            lineEdit_nodes.setFocus()
            return

        stop, value = self.check_complex_entries(
            lineEdit_real, lineEdit_imag, input_name
        )

        if stop:
            return

        self.remove_conflicting_data(properties, node_ids)

        real_values = [np.real(value)]
        imag_values = [np.imag(value)]

        for node_id in node_ids:
            node = app().project.model.preprocessor.nodes[node_id]
            coords = list(np.round(node.coordinates, 5))

            data = {
                "coords": coords,
                "real_values": real_values,
                "imag_values": imag_values,
            }

            self.properties._set_nodal_property(input_name, data, node_id)

        self.actions_to_finalize(reset_camera)
        print(f"[Set {input_name.title().replace('_', ' ')}] - defined at node(s) {node_ids}")

    def table_values_attribution_callback(
        self,
        lineEdit_nodes: QLineEdit,
        lineEdit_table_path: QLineEdit,
        input_name: str,
        properties: str | list[str],
        reset_camera=True,
    ):

        str_nodes = lineEdit_nodes.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            lineEdit_nodes.setFocus()
            return

        self.remove_conflicting_data(properties, node_ids)

        if lineEdit_table_path:
            if self.table_path is None:
                self.table_values, self.table_path = self.load_table(
                    lineEdit_table_path, direct_load=True
                )

                if self.table_values is None:
                    return

            for node_id in node_ids:
                self.table_name, self.array = self.save_table_file(
                    node_id, self.table_values
                )

                basenames = [self.table_name]
                table_paths = [self.table_path]

                node = app().project.model.preprocessor.nodes[node_id]
                coords = np.round(node.coordinates, 5)

                data = {
                    "coords": list(coords),
                    "table_names": basenames,
                    "table_paths": table_paths,
                }

                self.properties._set_nodal_property(input_name, data, node_id)

            self.actions_to_finalize(reset_camera)

            print(f"[Set {input_name.title()}] - defined at node(s) {node_ids}")

        else:
            title = "Additional inputs required"
            message = f"You must inform at least one {input_name} "
            message += "table path before confirming the input!"
            PrintMessageInput(["Error", title, message])
            lineEdit_table_path.setFocus()

    def save_table_file(self, node_id: int, values: np.ndarray, input_name: str):

        table_name = f"{input_name}_node_{node_id}"

        real_values = np.real(values)
        imag_values = np.imag(values)
        data = np.array([self.frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("acoustic", table_name, data)

        return table_name, data

    def lineEdit_reset(self, lineEdit: QLineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()
