import numpy as np

from pulse.model.model import Model
from pulse.processing.assemblers.acoustic_assembler import AcousticAssembler


class AcousticPostProcessor:
    """
    Post-processor for acoustic results.

    Stores acoustic solution metadata (perforated plate convergence,
    unstable frequencies) and provides access to the solution by node/DOF.

    Parameters
    ----------
    model : Model
    assembler : AcousticAssembler
    solution : np.ndarray
        Acoustic solution of shape (n_dofs_total, n_freqs).
    frequencies : np.ndarray
        Frequency vector in Hz.
    """

    def __init__(
        self,
        model: Model,
        assembler: AcousticAssembler,
        solution: np.ndarray,
        frequencies: np.ndarray,
    ):
        self.model = model
        self.assembler = assembler
        self.solution = solution
        self.frequencies = frequencies

    # ── Perforated plate convergence data ────────────────────────────────

    @property
    def convergence_data_log(self) -> list | None:
        """
        Convergence log from the nonlinear iteration (perforated plate).
        Format: [iterations, pressure_residues, delta_residues, target_pct].
        None if no nonlinear analysis was run or if it did not converge with log.
        """
        return self.assembler.convergence_data_log

    @property
    def has_nl_elements(self) -> bool:
        """True if the model has nonlinear perforated plate elements."""
        return bool(self.assembler.nl_elements)

    # ── Solution access ───────────────────────────────────────────────────

    def get_pressure_at_node(self, node_id: int) -> np.ndarray:
        """
        Returns the acoustic pressure vector (n_freqs,) at node `node_id`.
        """
        node = self.model.preprocessor.nodes[node_id]
        idx = node.global_index
        return self.solution[idx, :]

    def get_pressure_field(self) -> np.ndarray:
        """
        Returns the full solution (n_dofs, n_freqs).
        """
        return self.solution
