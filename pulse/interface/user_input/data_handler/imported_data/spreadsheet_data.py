from pulse.interface.user_input.data_handler.imported_data.imported_data import ImportedData
from dataclasses import dataclass

from collections import defaultdict

import numpy as np


@dataclass
class SpreadsheetData(ImportedData):
    sheetnames: list[str] = list()
    data: dict[str, np.array] = defaultdict(np.array)