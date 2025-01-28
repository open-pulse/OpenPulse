from PyQt5.QtWidgets import QDialog, QFileDialog, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import numpy as np

from pulse import app, UI_DIR
from pulse.interface.user_input.project.print_message import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"

class ExportModelResults(QFileDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_window = app().main_window

        self._initialize()

    def _initialize(self):
        self.data = dict()

    def _set_data_to_export(self, data : dict):
        self.data = data
        if data:
            self.call_file_dialog_and_export_data()

    def export_data_in_text_format(self, export_path, delimiter=","):

        for key, data in self.data.items():

            # selection_type, selection_id = key
            # suffix = f"{selection_type}_{selection_id}"
            
            x_label = data["x_label"]
            y_label = data["y_label"]

            x_data = data["x_data"]
            y_data = data["y_data"]
            unit = data["unit"]

            if isinstance(y_data[0], complex):
                header = f"{x_label}, Real part [{unit}], Imaginary part [{unit}], Absolute [{unit}]"
                data_to_export = np.array([x_data, np.real(y_data), np.imag(y_data), np.abs(y_data)]).T

            else:
                header = f"{x_label}, {y_label} [{unit}]"
                data_to_export = np.array([x_data, y_data]).T

            np.savetxt(export_path, data_to_export, delimiter=delimiter, header=header)

    def export_data_in_spreadsheet_format(self, export_path):
        from pandas import DataFrame, ExcelWriter

        with ExcelWriter(export_path) as writer:

            for key, data in self.data.items():

                selection_type, selection_id = key
                sheet_name = f"{selection_type}_{selection_id}"

                x_label = data["x_label"]
                y_label = data["y_label"]

                x_data = data["x_data"]
                y_data = data["y_data"]
                unit = data["unit"]

                if isinstance(y_data[0], complex):
                    header = [x_label, f"Real part [{unit}]", f"Imaginary part [{unit}]", f"Absolute [{unit}]"]
                    data_to_export = np.array([x_data, np.real(y_data), np.imag(y_data), np.abs(y_data)]).T

                else:
                    header = [x_label, f"{y_label} [{unit}]"]
                    data_to_export = np.array([x_data, y_data]).T

                df = DataFrame(data_to_export, columns=header)
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    def call_file_dialog_and_export_data(self):

        caption = "Export the model results"

        path = app().config.get_last_folder_for("export_data_folder")
        if path is None:
            directory_path = os.path.expanduser("~")
        else:
            directory_path = path

        if len(self.data) == 1:
            _filter = "Text file (*.dat);;Text file (*.txt);; Text file (*.csv);; Spreadsheet (*.xlsx)"
        else:
            _filter = "Spreadsheet (*.xlsx)"

        file_path, check = self.getSaveFileName(self.main_window, 
                                                caption, 
                                                directory_path, 
                                                filter = _filter)

        if not check:
            return

        app().config.write_last_folder_path_in_file("export_data_folder", file_path)

        sufix = Path(file_path).suffix      
        if sufix == ".xlsx":
            self.export_data_in_spreadsheet_format(file_path)
        else:
            self.export_data_in_text_format(file_path)

        # self.print_final_message()

    def print_final_message(self):
        title = "Information"
        message = "The results have been exported."
        PrintMessageInput([window_title_2, title, message], auto_close=True)