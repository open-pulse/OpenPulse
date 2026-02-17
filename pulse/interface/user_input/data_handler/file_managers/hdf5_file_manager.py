from pulse.interface.user_input.data_handler.file_managers.io_handler import IOHandler
from pulse.interface.user_input.data_handler.imported_data.simulation_data import SimulationData

from pathlib import Path

import numpy as np
import h5py


class HDF5FileManager(IOHandler):

    def __init__(self):
        super().__init__()

    def read(self, file_path: str | Path) -> SimulationData:
        file_path = Path(file_path)

        if file_path.suffix not in [".h5", ".hdf5"]:
            raise ValueError(
            f"Invalid suffix {file_path.suffix}. Use .h5 or .hdf5"
        )

        simulation_data = SimulationData(
            file_path.stem,
            file_path.suffix,
            str(file_path)
        )

        with h5py.File(file_path, 'r') as hf:

            # Read key data
            nodal_data = hf.get("nodal_data")
            variables = hf.get("variables")
            metadata = hf.get("metadata")

            # Save the nodal coordinates matrix
            simulation_data.nodal_area = np.array(nodal_data.get("nodal_area"), dtype=float)
            simulation_data.nodal_coordinates = np.array(nodal_data.get("coords"), dtype=float)

            # Save other attributes
            for attr_key in metadata.attrs:
                setattr(simulation_data, attr_key, metadata.attrs[attr_key])

            # Calculate the start point from last revolution
            delta_theta = metadata.attrs["delta_theta"]
            steps_per_rev = int(360 / delta_theta)
            start = steps_per_rev + 1

            # filter the last revolution data for metadata
            for key, values in metadata.items():
                setattr(simulation_data, key, values[-start:])

            # filter the last revolution data for variables
            for key, values in variables.items():
                setattr(simulation_data, key, values[:, -start:])

        return simulation_data