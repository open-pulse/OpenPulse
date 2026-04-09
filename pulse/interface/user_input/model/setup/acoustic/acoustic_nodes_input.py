import numpy as np
from PySide6.QtWidgets import QLineEdit

from pulse import app
from pulse.interface.user_input.model.setup.nodes_input import NodesInput
from pulse.interface.user_input.project.print_message import PrintMessageInput


class AcousticNodesInput(NodesInput):
    def __init__(self):
        super().__init__()

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
            lineEdit_real.setFocus()
            app().main_window.set_input_widget(self)
            return True, None

        else:
            return False, real_F + 1j * imag_F

    def constant_values_attribution_callback(
        self,
        lineEdit_node_ids: QLineEdit,
        lineEdit_real: QLineEdit,
        lineEdit_imag: QLineEdit,
        input_name: str,
        properties: str | list[str],
        reset_camera=True,
    ):

        lineEdit = lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(lineEdit, "nodes")
        if stop:
            lineEdit_node_ids.setFocus()
            return

        stop, value = self.check_complex_entries(
            lineEdit_real, lineEdit_imag, input_name
        )

        if stop:
            return
        
        self.remove_properties_from_node(node_ids, properties)

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

    def table_values_attribution_callback(
        self,
        lineEdit_node_ids: QLineEdit,
        lineEdit_table_path: QLineEdit,
        input_name: str,
        properties: str | list[str],
        reset_camera=True,
    ):

        str_nodes = lineEdit_node_ids.text()
        stop, node_ids = self.before_run.check_selected_ids(str_nodes, "nodes")
        if stop:
            lineEdit_node_ids.setFocus()
            return

        self.remove_properties_from_node(node_ids, properties)

        if lineEdit_table_path == "":
            self.hide()
            title = "Additional inputs required"
            message = f"You must inform at least one {input_name.replace('_', '')} " 
            message += "table path before confirming the input!"
            PrintMessageInput(["Error", title, message])
            lineEdit_table_path.setFocus()
            return
    
        if self.table_path is None:
            self.table_values, self.table_path = self.load_table(
                                                                    lineEdit_table_path,
                                                                    direct_load=True,
                                                                    )

            if self.table_values is None:
                return

        for node_id in node_ids:

            _table_name = None
            if isinstance(self.imported_values, np.ndarray):
                _table_name = self.get_table_name(input_name, node_id=node_id)
                if self.save_table_values(_table_name, self.imported_values):
                    return

            node = app().project.model.preprocessor.nodes[node_id]
            coords = np.round(node.coordinates, 5)

            data = {
                "coords" : list(coords),
                "table_names" : [_table_name],
                "table_paths" : [self.table_path],
                }

            self.properties._set_nodal_property(input_name, data, node_id)

        self.actions_to_finalize(reset_camera)

    def save_table_values(self, table_name: str, imported_values: np.ndarray, filter_zero: bool = True):

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

        self.properties.add_imported_tables("acoustic", table_name, data)

        return False

    def line_edit_reset(self, lineEdit: QLineEdit):
        lineEdit.clear()
        lineEdit.setFocus()
    
    def reset_input_fields(self):
        line_edits = self.findChildren(QLineEdit)
        for line_edit in line_edits:
            line_edit.clear()
