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

import numpy as np  


class FileManager:

    def __init__(self):
        self.__hdf5_file_manager = HDF5FileManager()
        self.__text_file_manager = TextFileManager()
        self.__spreadsheet_file_manager = SpreadsheetFileManager()

    def read_text_file(self, file_path: str) -> TextData:
        return self.__text_file_manager.read(file_path)

    def read_hdf5_file(self, file_path: str) -> SimulationData:
        return self.__hdf5_file_manager.read(file_path)

    def read_spreadsheet_file(self, file_path: str) -> SpreadsheetData:
        return self.__spreadsheet_file_manager.read(file_path)

    def save_text_file(self, file_path: str, data: np.array, delimiter = ",", header = ""):
        self.__text_file_manager.save(file_path, data, delimiter=delimiter, header=header)
    
    def save_spreadsheet_file(self, file_path: str, sheetname: str, data: PolarsDataFrame, index_rows: bool = False):
        self.__spreadsheet_file_manager.save(file_path, sheetname, data, index_rows)