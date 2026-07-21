from abc import abstractmethod
from functools import partial
from pathlib import Path

import numpy as np
from molde.colors import color_names
from PySide6.QtGui import QCloseEvent, QColor, Qt
from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QWidget

from pulse import app
from pulse.interface import error_title
from pulse.interface.formatters import icons
from pulse.interface.user_input.data_handler.file_dialog_service import (
    FileDialogService,
)
from pulse.interface.user_input.data_handler.file_handlers.file_handler import (
    FileHandler,
)
from pulse.interface.user_input.data_handler.imported_data import (
    SpreadsheetData,
    TextData,
)
from pulse.interface.user_input.project.print_message import PrintMessageInput


class UserInput(QDialog):
    def __init__(self):
        super().__init__()

        app().main_window.set_input_widget(self)

        self._config_window()
        self._paint_icons()

        app().main_window.theme_changed.connect(self._paint_icons)

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _paint_icons(self):
        theme = app().main_window.config.user_preferences.interface_theme

        if theme == "dark":
            icon_color = QColor(color_names.BLUE_6.to_hex())

        elif theme == "light":
            icon_color = QColor(color_names.BLUE_4.to_hex())

        widgets = self.findChildren(QWidget)

        icons.change_icon_color_for_widgets(widgets, icon_color)
    
    def _check_table_frequency_vector(self, frequencies: np.ndarray):
        if len(frequencies) == 1:
            return False

        f_steps = frequencies[1:] - frequencies[:-1]

        return not np.allclose(f_steps, f_steps[0], atol=1e-8)
    
    def load_table(self, line_edit: QLineEdit, bc_label: str, dof_label: str = "", direct_load: bool = False):

        title = "Error while loading table"

        try:
            if direct_load:
                table_path = Path(line_edit.text())

                if not table_path.name:
                    return None, None

            else:

                last_path = app().main_window.config.get_last_folder_for("imported_table_folder")
                if last_path is None:
                    last_path = str(Path().home())

                caption = f"Choose a table to import the {bc_label}"
                if dof_label != "":
                    caption += f" ({dof_label})"
                
                extensions = ["xls", "xlsx", "csv", "dat", "txt"]

                table_path = FileDialogService.open_file(extensions, caption, last_path)

                if table_path is None:
                    return None, None

            line_edit.setText(str(table_path))
            imported_file = FileHandler().read(table_path)
   
            if isinstance(imported_file, SpreadsheetData):
                imported_data = imported_file.sheets[0].data

            elif isinstance(imported_file, TextData):
                imported_data = imported_file.data

            else:
                self.hide()
                message = "The imported table file extension is not supported. "
                PrintMessageInput([error_title, title, message])
                line_edit.setFocus()
                return None, None

            if imported_data.shape[1] < 3:
                self.hide()
                message = "The imported table has an insufficient number of columns. The spectrum "
                message += "data must have frequencies, real and imaginary columns."
                PrintMessageInput([error_title, title, message])
                line_edit.setFocus()
                return None, None
           
            if self._check_table_frequency_vector(imported_data[:, 0]):
                self.hide()
                message = "The frequencies vector from imported table has a non-uniform frequency "
                message += "spacing. The frequencies vector must be equally spaced."
                PrintMessageInput([error_title, title, message])
                line_edit.setFocus()
                return None, None

            app().main_window.config.write_last_folder_path_in_file("imported_table_folder", table_path)

            return imported_data, str(table_path)

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([error_title, title, message])
            line_edit.setFocus()
            return None, None
    
    def connect_load_table_push_buttons(self, line_edits: list[QLineEdit], labels: list[str]):
        for line_edit, label in zip(line_edits, labels):
            push_button: QPushButton = getattr(self, f"pushButton_load_{label}_table")

            push_button.clicked.connect(partial(self.load_table_for_line_edit, line_edit=line_edit, dof_label=label))
    
    def load_table_for_line_edit(self, line_edit: QLineEdit, dof_label: str, bc_label: str):
        imported_values, table_path = self.load_table(
            line_edit,
            bc_label
        )

        values_attr = f"imported_{dof_label}_values"
        table_attr = f"{dof_label}_table_path"

        setattr(self, values_attr, imported_values)
        setattr(self, table_attr, table_path)

        if table_path is None:
            self.line_edit_reset(line_edit)
    
    def get_spectral_data_from_array(self, data: np.ndarray | None, return_frequencies: bool=False):
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

    def update_analysis_setup_in_file(self, frequencies: np.ndarray):

        analysis_setup = app().project.file.read_analysis_setup_from_file()
        if not isinstance(analysis_setup, dict):
            analysis_setup = dict()

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

    def get_table_name(self, _label: str, node_id: int | None = None, element_id: int | None = None, line_id: int | None = None):

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

    def line_edit_reset(self, lineEdit : QLineEdit):
        lineEdit.clear()
        lineEdit.setFocus()

    @abstractmethod
    def selection_callback(self):
        pass

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        app().main_window.selection_changed.disconnect(self.selection_callback)
        return super().closeEvent(a0)