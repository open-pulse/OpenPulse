from pulse.interface.user_input.data_handler.file_managers import (
    HDF5FileManager,
    TextFileManager,
    SpreadsheetFileManager
)
from polars import DataFrame as PolarsDataFrame
from pathlib import Path

import numpy as np  


class FileManager:

    def __init__(self):
        self.__hdf5_file_manager = HDF5FileManager()
        self.__text_file_manager = TextFileManager()
        self.__spreadsheet_file_manager = SpreadsheetFileManager()

    def read(self, file_path: str):
        file_path = Path(file_path)

        if file_path.suffix in [".txt", ".dat", ".csv"]:
            self.__text_file_manager.read(file_path)

        elif file_path.suffix in [".xls", ".xlsx"]:
            self.__spreadsheet_file_manager.read(file_path)

        elif file_path.suffix in ["h5", "hdf5", "hdf", "he5"]:
            self.__hdf5_file_manager.read(file_path)
        else:
            raise ValueError(
            f"Invalid suffix {file_path.suffix}. The FileManager class don't read {file_path.suffix} files"
        )
    
    def save_text_file(self, file_path: str, data: np.array, delimiter = ",", header = ""):
        self.__text_file_manager.save(file_path, data, delimiter=delimiter, header=header)
    
    def save_spreadsheet_file(self, file_path: str, sheetname: str, data: PolarsDataFrame, index_rows: bool = False):
        self.__spreadsheet_file_manager.save(file_path, sheetname, data, index_rows)