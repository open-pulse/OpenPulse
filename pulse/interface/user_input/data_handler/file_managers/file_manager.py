from pulse.interface.user_input.data_handler.file_managers import (
    HDF5FileManager,
    TextFileManager,
    SpreadsheetFileManager
)
from pulse.interface.user_input.data_handler.imported_data import (
    SimulationData,
    TextData,
    SpreadsheetData
)

from polars import DataFrame as PolarsDataFrame
from pathlib import Path

import numpy as np  


class FileManager:

    def __init__(self):
        self._hdf5_file_manager = HDF5FileManager()
        self._text_file_manager = TextFileManager()
        self._spreadsheet_file_manager = SpreadsheetFileManager()
    
    def read(self, file_path: str | Path) -> TextData | SimulationData | SpreadsheetData:
        file_path = Path(file_path)

        if file_path.suffix in [".txt", ".dat", ".csv"]:
            return self._text_file_manager.read(file_path)
        elif file_path.suffix in [".h5", "hdf5"]:
            return self._hdf5_file_manager.read(file_path)
        elif file_path.suffix in [".xls", ".xlsx"]:
            return self._spreadsheet_file_manager.read(file_path)

    def read_text_file(self, file_path: str | Path) -> TextData:
        return self._text_file_manager.read(file_path)

    def read_hdf5_file(self, file_path: str| Path) -> SimulationData:
        return self._hdf5_file_manager.read(file_path)

    def read_spreadsheet_file(self, file_path: str | Path) -> SpreadsheetData:
        return self._spreadsheet_file_manager.read(file_path)

    def save_text_file(self, file_path: str, data: np.array, delimiter = ",", header = ""):
        self._text_file_manager.save(file_path, data, delimiter=delimiter, header=header)
    
    def save_spreadsheet_file(self, file_path: str, sheetname: str, data: PolarsDataFrame, index_rows: bool = False):
        self._spreadsheet_file_manager.save(file_path, sheetname, data, index_rows)