
from dataclasses import dataclass

import numpy as np


@dataclass
class ElementConnectivityData:
    indexes: np.ndarray
    connectivities: np.ndarray


def get_connectivity(input_data: dict[tuple[int, int], dict[str, ElementConnectivityData]]):
    """
    The returned value is an array where each line is a connectivity
    and the colums follow this order:

    Element index || Line/Face/Solid tag || Element type || Nodes per element || Connectivity
    """

    if not isinstance(input_data, dict):
        raise TypeError("get_connectivity_data only accepts dicts as input.")

    rows_cols = list()
    for data_0 in input_data.values():
        for econnect_data in data_0.values():
            connectivities = econnect_data.connectivities
            rows_cols.append(connectivities.shape)

    n_rows = sum([rows for (rows, _) in rows_cols])
    n_cols = max([cols for (_, cols) in rows_cols])

    gmsh_elements = np.zeros(n_rows, dtype=int)
    output_data = np.zeros((n_rows, n_cols + 4), dtype=int)

    internal_indexes = np.arange(n_rows, dtype=int)
    output_data[:, 0] = internal_indexes

    start, end, ind = 0, 0, 0
    for (entity_dim, entity_tag), data_0 in input_data.items():
        for etype_tag, econnect_data in data_0.items():

            rows, cols = rows_cols[ind]
            ones = np.ones(rows, dtype=int)
            
            indexes = econnect_data.indexes
            connectivities = econnect_data.connectivities

            end += rows

            output_data[start:end, 1] = ones * entity_tag
            output_data[start:end, 2] = ones * etype_tag
            output_data[start:end, 3] = ones * cols
            output_data[start:end, 4 : 4 + cols] = connectivities
            gmsh_elements[start:end] = indexes

            start = end
            ind += 1

    map_elements = dict(zip(gmsh_elements, internal_indexes))

    return output_data, map_elements
