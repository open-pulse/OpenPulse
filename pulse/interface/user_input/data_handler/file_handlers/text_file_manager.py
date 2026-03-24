from pulse.interface.user_input.data_handler.imported_data.text_data import TextData
from pulse.interface.user_input.data_handler.file_handlers.io_handler import IOHandler
from pathlib import Path

import numpy as np


class TextFileHandler(IOHandler):

    EXTENSIONS = [".txt", ".dat", ".csv"]

    def __init__(self, delimiter=",", header: str = ""):
        self.delimiter = delimiter
        self.header = header

        super().__init__()

    def read(self, file_path: str | Path) -> TextData:
        file_path = Path(file_path)

        if file_path.suffix not in self.EXTENSIONS:
            self.raise_extensions_error(file_path, self.EXTENSIONS)

        try:
            loaded_data = np.loadtxt(file_path, delimiter = self.delimiter)
        except:
            loaded_data = self._load_text_file_data(file_path)

        loaded_data = self._remove_unnecesary_header_in_data(loaded_data)

        return TextData(file_path.stem, 
                        file_path.suffix, 
                        str(file_path),
                        loaded_data)
    
    def save(self, file_path: str | Path, data: np.array, delimiter = ",", header = ""):
        file_path = Path(file_path)

        if not file_path.parent.exists():
            raise FileNotFoundError(f"The path {file_path.parent} does not exist")
        
        if file_path.suffix not in self.EXTENSIONS:
            self.raise_extensions_error(file_path, self.EXTENSIONS)
        
        np.savetxt(str(file_path), data, delimiter=delimiter, header=header)

    def _remove_unnecesary_header_in_data(self, data: np.ndarray) -> np.ndarray:
        filtered_data = [row for row in data if not isinstance(row[0], str)]
        return np.array(filtered_data, dtype=float)
    
    def _load_text_file_data(self, file_path: str | Path):
        output_data = list()
        if isinstance(file_path, str):
            file_path = Path(file_path)

        with open(file_path, 'r') as file:
            for line in file.readlines():
                try:
                    modif_line = line.replace(",", " ").strip().split(" ")
                    line_values = [float(value) for value in modif_line if value != ""]
                except:
                    continue

                output_data.append(line_values)

        return np.array(output_data, dtype=float)
