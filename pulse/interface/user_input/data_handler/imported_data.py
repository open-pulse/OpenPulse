from dataclasses import dataclass, field
from pathlib import Path

import numpy as np


@dataclass
class ImportedDataInterface:
    path: Path = Path()
    filename: str = field(init=False)
    extension: str = field(init=False)

    def __post_init__(self):
        self.path = Path(self.path)
        self.filename = self.path.name
        self.extension = self.path.suffix

    def to_dict(self) -> dict:
        return dict(vars(self))

@dataclass
class TextData(ImportedDataInterface):
    data: np.array = None


@dataclass
class SimulationData(ImportedDataInterface):
    nodal_area: np.array = None
    nodal_coordinates: np.array = None


@dataclass
class SpreadsheetSheet:
    sheetname: str
    data: np.ndarray


@dataclass
class SpreadsheetData(ImportedDataInterface):
    sheets: list[SpreadsheetSheet] = None

    def to_dict(self) -> dict:
        data = {"path": self.path, 
                "filename": self.filename, 
                "extension": self.extension
                }

        for sheet in self.sheets:
            data[sheet.sheetname] = sheet.data

        return data

    @property
    def data(self):
        if len(self.sheets) == 0:
            return None
        
        return self.sheets[0].data


ImportedData = TextData | SpreadsheetSheet | SimulationData