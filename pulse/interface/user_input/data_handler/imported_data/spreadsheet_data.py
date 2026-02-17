from pulse.interface.user_input.data_handler.imported_data.imported_data import ImportedData
from pulse.interface.user_input.data_handler.imported_data.spreadsheet_sheet import SpreadsheetSheet
from dataclasses import dataclass

import numpy as np


@dataclass
class SpreadsheetData(ImportedData):
    sheets: list[SpreadsheetSheet] = None