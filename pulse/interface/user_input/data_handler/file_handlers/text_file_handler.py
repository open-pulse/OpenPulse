from pathlib import Path

import numpy as np

from pulse.interface.user_input.data_handler.file_handlers.io_handler import IOHandler
from pulse.interface.user_input.data_handler.imported_data import TextData


class TextFileHandler(IOHandler):
    EXTENSIONS = [".txt", ".dat", ".csv"]

    @staticmethod
    def read(file_path: Path, delimiter: str = ",") -> TextData:
        try:
            loaded_data = np.loadtxt(file_path, delimiter=delimiter)
        except:
            loaded_data = TextFileHandler._load_text_file_data(file_path)

        loaded_data = TextFileHandler._remove_unnecesary_header_in_data(loaded_data)

        return TextData(file_path, loaded_data)

    @staticmethod
    def save(file_path: str | Path, data: np.array, delimiter=",", header=""):
        np.savetxt(str(file_path), data, delimiter=delimiter, header=header)

    @staticmethod
    def _remove_unnecesary_header_in_data(data: np.ndarray) -> np.ndarray:
        filtered_data = [row for row in data if not isinstance(row[0], str)]
        return np.array(filtered_data, dtype=float)

    @staticmethod
    def _load_text_file_data(file_path: Path):
        output_data = list()

        with open(file_path, "r") as file:
            for line in file.readlines():
                try:
                    modif_line = line.replace(",", " ").strip().split(" ")
                    line_values = [float(value) for value in modif_line if value != ""]
                except:
                    continue

                output_data.append(line_values)

        return np.array(output_data, dtype=float)