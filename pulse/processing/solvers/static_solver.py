from __future__ import annotations

import numpy as np
from scipy.sparse.linalg import spsolve

from pulse.processing.assemblers.base import Assembler


class StaticSolver:
    """
    Generic static solver.

    Solves the linear system  K·u = F  (omega = 0) using any assembler
    that implements the Assembler interface.

    Parameters
    ----------
    assembler : Assembler
        Assembler providing the stiffness matrix and load vector for omega = 0.
    """

    def __init__(self, assembler: Assembler):
        self.assembler = assembler
        self.solution: np.ndarray | None = None
        self.frequencies: np.ndarray = np.array([0.0])

    def solve(self) -> np.ndarray:
        """
        Solve the static analysis.

        Returns
        -------
        np.ndarray
            Full displacement vector (with prescribed DOFs reinserted).
        """

        assembler = self.assembler
        K = assembler.get_stiffness_matrix()
        F = assembler.get_load_vector(index=0, omega=0.0)

        u_reduced = spsolve(K, F)

        # spsolve returns 1-D when F is 1-D; ensure 2-D (n_dofs × 1)
        if u_reduced.ndim == 1:
            u_reduced = u_reduced[:, np.newaxis]

        result = assembler.reinsert_prescribed_dofs(u_reduced)
        self.solution = result
        return result
