from pulse.interface.user_input.data_handler.imported_data.imported_data import ImportedData
from dataclasses import dataclass

import numpy as np


@dataclass
class SimulationData(ImportedData):
    nodal_area: np.array = None
    nodal_coordinates: np.array = None