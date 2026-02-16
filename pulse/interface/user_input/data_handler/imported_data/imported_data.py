from dataclasses import dataclass
import numpy as np


@dataclass
class ImportedData:
    filename: str = str()
    extension: str = str()
    path: str = str()
