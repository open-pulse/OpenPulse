from pulse.interface.user_input.data_handler.file_handlers.io_handler import IOHandler
from pulse.interface.user_input.data_handler.imported_data import SpreadsheetData
from pulse.interface.user_input.data_handler.imported_data import SpreadsheetSheet

from polars import DataFrame as PolarsDataFrame
from pathlib import Path

import numpy as np


class SpreadsheetFileHandler(IOHandler):

    EXTENSIONS = [".xls", ".xlsx"]

    def __init__(self):
        super().__init__()

    def read(self, file_path: str | Path) -> SpreadsheetData:
        from polars import read_excel
        from openpyxl import load_workbook

        wb = load_workbook(file_path)

        imported_spreadsheet = SpreadsheetData(file_path.stem,
                                               file_path.suffix,
                                               str(file_path),
                                               )
        sheets = list()
        for sheetname in wb.sheetnames:
            max_cols = wb[sheetname].max_column 

            for i in range(max_cols, 1, -1):
                cols = list(range(i))

                try:
                    sheet_data = read_excel(
                                            str(file_path), 
                                            sheet_name = sheetname,  
                                            columns = cols,
                                            engine = "openpyxl",
                                            has_header = False,
                                            infer_schema_length = 100
                                            ).to_numpy()
                    break
                except:
                    pass

            sheet_data = self._remove_unnecesary_header_in_data(sheet_data)
            sheets.append(SpreadsheetSheet(sheetname, sheet_data))

        imported_spreadsheet.sheets = sheets

        return imported_spreadsheet

    def save(self, file_path: str | Path, sheet_name: str, data: PolarsDataFrame, index_rows: bool = False):
        from pandas import ExcelWriter

        with ExcelWriter(str(file_path)) as writer:
            data.to_pandas().to_excel(writer, sheet_name=sheet_name, index=index_rows)
    
    def _remove_unnecesary_header_in_data(self, data: np.ndarray) -> np.ndarray:
        filtered_data = [row for row in data if self._is_valid_row(row)]
        return np.array(filtered_data, dtype=float)

    def _is_valid_row(self, row: np.ndarray) -> bool:
        try:
            float(row[0])
            return True
        except (ValueError, TypeError):
            return False