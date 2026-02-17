from dataclasses import dataclass

import numpy as np


@dataclass
class SpreadsheetSheet:
    name: str 
    data: np.ndarray