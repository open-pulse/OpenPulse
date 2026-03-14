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