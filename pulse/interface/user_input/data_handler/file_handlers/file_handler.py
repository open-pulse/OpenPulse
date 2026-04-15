from pathlib import Path

import numpy as np
from polars import DataFrame as PolarsDataFrame

from pulse.interface.user_input.data_handler.file_handlers.hdf5_file_handler import HDF5FileHandler
from pulse.interface.user_input.data_handler.file_handlers.text_file_handler import TextFileHandler
from pulse.interface.user_input.data_handler.file_handlers.spreadsheet_file_handler import SpreadsheetFileHandler
from pulse.interface.user_input.data_handler.imported_data import SimulationData, SpreadsheetData, TextData


class FileHandler:

    def __init__(self):
        self._hdf5_file_handler = HDF5FileHandler()
        self._text_file_handler = TextFileHandler()
        self._spreadsheet_file_handler = SpreadsheetFileHandler()
    
    def read(self, file_path: str | Path) -> TextData | SimulationData | SpreadsheetData:
        file_path = Path(file_path)

        if file_path.suffix in TextFileHandler.EXTENSIONS:
            return self._text_file_handler.read(file_path)
        elif file_path.suffix in HDF5FileHandler.EXTENSIONS:
            return self._hdf5_file_handler.read(file_path)
        elif file_path.suffix in SpreadsheetFileHandler.EXTENSIONS:
            return self._spreadsheet_file_handler.read(file_path)
        else:
            all_extensions = (
                TextFileHandler.EXTENSIONS + 
                HDF5FileHandler.EXTENSIONS + 
                SpreadsheetFileHandler.EXTENSIONS
            )
            raise self.raise_extensions_error(file_path, all_extensions)

    def save_text_file(self, file_path: str, data: np.array, delimiter = ",", header = ""):
        file_path = Path(file_path)

        if not file_path.parent.exists():
            raise FileNotFoundError(f"The path {file_path.parent} does not exist")

        if file_path.suffix not in self._text_file_handler.EXTENSIONS:
            raise self.raise_extensions_error(file_path, self._text_file_handler.EXTENSIONS)

        self._text_file_handler.save(file_path, data, delimiter=delimiter, header=header)
    
    def save_spreadsheet_file(self, file_path: str, sheetname: str, data: PolarsDataFrame, index_rows: bool = False):
        file_path = Path(file_path)

        if not file_path.parent.exists():
            raise FileNotFoundError(f"The path {file_path.parent} does not exist")

        if file_path.suffix not in self._spreadsheet_file_handler.EXTENSIONS:
            raise self.raise_extensions_error(file_path, self._spreadsheet_file_handler.EXTENSIONS)

        self._spreadsheet_file_handler.save(file_path, sheetname, data, index_rows)
    
    def generate_extensions_string_for_error_message(self, extensions: list[str]) -> str:
        if not extensions:
            return ""

        if len(extensions) == 1:
            return extensions[0]

        return ", ".join(extensions[:-1]) + " or " + extensions[-1]

    def raise_extensions_error(self, file_path: str | Path, extensions: list[str]) -> ValueError:
        extensions_text = self.generate_extensions_string_for_error_message(extensions)
        file_path = Path(file_path)

        raise ValueError(
            f"Invalid suffix {file_path.suffix}. Use {extensions_text}"
        )