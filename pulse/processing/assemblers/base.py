from abc import ABC, abstractmethod

import numpy as np
from scipy.sparse import spmatrix


class Assembler(ABC):
    """
    Generic interface that every physics assembler must implement.

    Each solver uses only the subset of methods it needs:

    StaticSolver  :  get_stiffness_matrix()
                     get_load_vector(index=0, omega=0)
                     reinsert_prescribed_dofs(solution)

    ModalSolver   :  get_stiffness_matrix()
                     get_mass_matrix()
                     get_damping_matrix()          ← optional
                     reinsert_prescribed_dofs(solution, modal=True)

    HarmonicSolver:  get_system_matrix(index, omega)
                     get_load_vector(index, omega)
                     reinsert_prescribed_dofs(solution)

    The `index` parameter is the integer index within the frequencies vector.
    Passing the index together with omega avoids omega→index mappings in the
    assemblers and makes the code more robust.
    """

    # ── For ModalSolver and StaticSolver ─────────────────────────────────

    @abstractmethod
    def get_stiffness_matrix(self) -> spmatrix:
        """Stiffness matrix K (frequency-independent)."""

    @abstractmethod
    def get_mass_matrix(self) -> spmatrix:
        """Mass matrix M (frequency-independent)."""

    def get_damping_matrix(self) -> spmatrix | None:
        """
        Damping matrix C (frequency-independent), optional.
        Returns None if there is no nonproportional damping requiring
        a state-space formulation.
        """
        return None

    # ── For HarmonicSolver and StaticSolver ──────────────────────────────

    @abstractmethod
    def get_system_matrix(self, index: int, omega: float) -> spmatrix:
        """
        Dynamic system matrix for step `index` (frequency omega).
        Structural : K - ω²M + iC(ω)
        Acoustic   : K_fetm(ω)  (frequency-dependent admittance)
        Static     : call with index=0, omega=0.
        """

    @abstractmethod
    def get_load_vector(self, index: int, omega: float) -> np.ndarray:
        """
        Load vector for step `index` (frequency omega).
        Already includes the effects of prescribed DOFs (equivalent load).
        Static     : call with index=0, omega=0.
        """

    # ── For all solvers ───────────────────────────────────────────────────

    @abstractmethod
    def reinsert_prescribed_dofs(
        self, solution: np.ndarray, modal: bool = False
    ) -> np.ndarray:
        """
        Reinsert prescribed DOFs into the reduced solution.
        If modal=True, prescribed DOFs receive zero value.
        """

    # ── Utility ───────────────────────────────────────────────────────────

    def stop_processing(self) -> bool:
        """Returns True if the user requested processing interruption."""
        return False
