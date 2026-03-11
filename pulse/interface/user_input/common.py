from PySide6.QtWidgets import QDialog, QLineEdit, QTreeWidgetItem
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt

from pulse.interface.user_input.project.print_message import PrintMessageInput

from pulse import app
from pathlib import Path
import numpy as np


def get_spectral_data_from_array(data: np.ndarray | None, return_frequencies: bool=False):
    """
    This function returns two vectors containing the spectral data of interest.
    The first one is the frequencies vector and the second is the vector of 
    complex values.
    
    Parameters
    ----------
    data : np.ndarray
        The array that gathers spectral data.

    return_frequencies: bool, optional
        It controls whether the frequencies vector will be returned.
    """
    if data is None:
        return None
  
    complex_values = data[:, 1] + 1j * data[:, 2]

    if return_frequencies:
        frequencies = data[:, 0]
        return frequencies, complex_values

    return complex_values


def update_analysis_setup_in_file(frequencies: np.ndarray):

    analysis_setup = app().project.file.read_analysis_setup_from_file()

    analysis_setup.update(
        {
        "frequency_spacing" : "tabular",
        "f_min" : float(frequencies[0]),
        "f_max" : float(frequencies[-1]),
        "f_step" : float(frequencies[1] - frequencies[0]),
        "frequencies" : None,
        }
        )

    app().project.model.set_analysis_setup(analysis_setup)
    app().project.file.write_analysis_setup_in_file(analysis_setup)


def get_table_name(_label: str, node_id: int | None = None, element_id: int | None = None, line_id: int | None = None):

    if isinstance(node_id, int):
        return f"{_label}_node_{node_id}"
    
    if isinstance(node_id, list | tuple | np.ndarray):
        if len(node_id) == 2:
            return f"{_label}_nodes_{int(node_id[0])}_{int(node_id[1])}"

    if isinstance(element_id, int):
        return f"{_label}_element_{element_id}"

    if isinstance(line_id, int):
        return f"{_label}_line_{line_id}"
    
    return ""

def check_table_frequency_vector(frequencies: np.ndarray):
    if len(frequencies) == 1:
        return False

    f_steps = frequencies[1:] - frequencies[:-1]

    return not np.allclose(f_steps, f_steps[0], atol=1e-8)

class CommonUserInputs(QDialog):

    def load_table(self, line_edit: QLineEdit, bc_label: str, dof_label: str = "", direct_load: bool = False):

        error_title = "Error"
        title = "Error while loading table"

        try:
            if direct_load:
                table_path = line_edit.text()

            else:

                last_path = app().main_window.config.get_last_folder_for("imported_table_folder")
                if last_path is None:
                    last_path = str(Path().home())

                caption = f"Choose a table to import the {bc_label}"
                if dof_label != "":
                    caption += f" ({dof_label})"

                table_path, check = app().main_window.file_dialog.get_open_file_name(
                    caption, 
                    last_path, 
                    'Table File (*.csv; *.dat; *.txt)'
                    )

                if not check:
                    return None, None

            if table_path == "":
                return None, None

            line_edit.setText(table_path)         
            imported_data = np.loadtxt(table_path, delimiter=",")

            if imported_data.shape[1] < 3:
                self.parent().hide()
                message = "The imported table has an insufficient number of columns. The spectrum "
                message += "data must have frequencies, real and imaginary columns."
                PrintMessageInput([error_title, title, message])
                line_edit.setFocus()
                return None, None
           
            if check_table_frequency_vector(imported_data[:, 0]):
                self.parent().hide()
                message = "The frequencies vector from imported table has a non-uniform frequency "
                message += "spacing. The frequencies vector must be equally spaced."
                PrintMessageInput([error_title, title, message])
                line_edit.setFocus()
                return None, None

            app().main_window.config.write_last_folder_path_in_file("imported_table_folder", table_path)

            return imported_data, table_path

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([error_title, title, message])
            line_edit.setFocus()
            return None, None