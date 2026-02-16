from pulse.interface.user_input.data_handler.imported_data.imported_data import ImportedData
from dataclasses import dataclass

import numpy as np


@dataclass
class TextData(ImportedData):
    data: np.array