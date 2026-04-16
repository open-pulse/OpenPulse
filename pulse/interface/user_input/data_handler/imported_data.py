from dataclasses import dataclass
import numpy as np


@dataclass
class ImportedData:
    filename: str = str()
    extension: str = str()
    path: str = str()


@dataclass
class TextData(ImportedData):
    data: np.array = None


@dataclass
class SimulationData(ImportedData):
    nodal_area: np.array = None
    nodal_coordinates: np.array = None


@dataclass
class SpreadsheetSheet:
    name: str
    data: np.ndarray
    source_file: str = ""

    
@dataclass
class SpreadsheetData(ImportedData):
    sheets: list[SpreadsheetSheet] = None

