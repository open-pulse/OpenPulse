from pathlib import Path

import numpy as np
from polars import DataFrame as PolarsDataFrame

from pulse.interface.user_input.data_handler.file_handlers.io_handler import IOHandler
from pulse.interface.user_input.data_handler.imported_data import (
    SpreadsheetData,
    SpreadsheetSheet,
)


class SpreadsheetFileHandler(IOHandler):
    READ_EXTENSIONS = [".xls", ".xlsx"]
    WRITE_EXTENSIONS = [".xlsx"]

    @staticmethod
    def read(file_path: Path) -> SpreadsheetData:
        from polars import read_excel

        imported_spreadsheet = SpreadsheetData(file_path)

        sheets_data = read_excel(
            file_path,
            sheet_id=0,
            engine="calamine",
            has_header=False,
            raise_if_empty=False
        )

        sheets = []
        for sheetname, df in sheets_data.items():
            if df.is_empty():
                continue

            sheet_data = SpreadsheetFileHandler._remove_unnecesary_header_in_data(df.to_numpy())
            sheets.append(SpreadsheetSheet(sheetname, sheet_data))

        imported_spreadsheet.sheets = sheets

        return imported_spreadsheet

    @staticmethod
    def save(file_path: str | Path, sheet_name: str, data: PolarsDataFrame, index_rows: bool = False, append: bool = False):
        from pandas import ExcelWriter

        mode = "a" if append else "w"
        kwargs = {"if_sheet_exists": "replace"} if append else {}

        with ExcelWriter(str(file_path), engine="openpyxl", mode=mode, **kwargs) as writer:
            data.to_pandas().to_excel(writer, sheet_name=sheet_name, index=index_rows)

    @staticmethod
    def _remove_unnecesary_header_in_data(data: np.ndarray) -> np.ndarray:
        filtered_data = [row for row in data if SpreadsheetFileHandler._is_valid_row(row)]
        return np.array(filtered_data, dtype=float)

    @staticmethod
    def _is_valid_row(row: np.ndarray) -> bool:
        try:
            float(row[0])
            return True
        except (ValueError, TypeError):
            return False