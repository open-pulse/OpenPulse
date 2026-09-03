from pathlib import Path
from typing import overload

import numpy as np
from polars import DataFrame as PolarsDataFrame

from pulse.interface.user_input.data_handler.file_handlers.hdf5_file_handler import HDF5FileHandler
from pulse.interface.user_input.data_handler.file_handlers.spreadsheet_file_handler import SpreadsheetFileHandler
from pulse.interface.user_input.data_handler.file_handlers.text_file_handler import TextFileHandler
from pulse.interface.user_input.data_handler.imported_data import ImportedData


class FileHandler:

    @overload
    @staticmethod
    def read(file_path: str | Path | None) -> ImportedData | None:
        ...

    @overload
    @staticmethod
    def read(file_path: list[str] | list[Path]) -> list[ImportedData] | None:
        ...

    @staticmethod
    def read(file_path: str | Path | list[str] | list[Path]) -> ImportedData | list[ImportedData] | None:
        if file_path == "":
            return None

        if isinstance(file_path, (str | Path)):
            return FileHandler._read(file_path)

        if not isinstance(file_path, list):
            return None

        imported_paths = [] 
        for path in file_path:
            imported_path = FileHandler._read(path)

            if imported_path is None:
                continue
            
            imported_paths.append(imported_path) 
            
        return imported_paths if len(imported_paths) > 0 else None
        
    @staticmethod
    def _read(file_path: str | Path) -> ImportedData | None:
        file_path = Path(file_path)
        
        if file_path.suffix in TextFileHandler.EXTENSIONS:
            return TextFileHandler.read(file_path)
        elif file_path.suffix in HDF5FileHandler.EXTENSIONS:
            return HDF5FileHandler.read(file_path)
        elif file_path.suffix in SpreadsheetFileHandler.EXTENSIONS:
            return SpreadsheetFileHandler.read(file_path)
        else:
            all_extensions = TextFileHandler.EXTENSIONS + HDF5FileHandler.EXTENSIONS + SpreadsheetFileHandler.EXTENSIONS
            raise FileHandler.raise_extensions_error(file_path, all_extensions)
            
    @staticmethod
    def save_text_file(file_path: str | Path, data: np.array, delimiter=",", header=""):
        file_path = Path(file_path)

        if not file_path.parent.exists():
            raise FileNotFoundError(f"The path {file_path.parent} does not exist")

        if file_path.suffix not in TextFileHandler.EXTENSIONS:
            raise FileHandler.raise_extensions_error(file_path, TextFileHandler.EXTENSIONS)

        TextFileHandler.save(file_path, data, delimiter=delimiter, header=header)

    @staticmethod
    def save_spreadsheet_file(file_path: str | Path, sheetname: str, data: PolarsDataFrame, index_rows: bool = False, append=False):
        file_path = Path(file_path)

        if not file_path.parent.exists():
            raise FileNotFoundError(f"The path {file_path.parent} does not exist")

        if file_path.suffix not in SpreadsheetFileHandler.EXTENSIONS:
            raise FileHandler.raise_extensions_error(file_path, SpreadsheetFileHandler.EXTENSIONS)

        SpreadsheetFileHandler.save(file_path, sheetname, data, index_rows, append)

    @staticmethod
    def generate_extensions_string_for_error_message(extensions: list[str]) -> str:
        if not extensions:
            return ""

        if len(extensions) == 1:
            return extensions[0]

        return ", ".join(extensions[:-1]) + " or " + extensions[-1]

    @staticmethod
    def raise_extensions_error(file_path: str | Path, extensions: list[str]) -> ValueError:
        extensions_text = FileHandler.generate_extensions_string_for_error_message(extensions)
        file_path = Path(file_path)

        raise ValueError(f"Invalid suffix {file_path.suffix}. Use {extensions_text}")