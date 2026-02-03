from dataclasses import dataclass
import numpy as np


@dataclass
class ImportedFile:
    data: np.ndarray
    filename: str = str()
    extension: str = str()
    sheetname: str = str()
    path: str = str()
